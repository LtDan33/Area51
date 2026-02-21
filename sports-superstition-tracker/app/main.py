import asyncio
import json
import random
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")


# --- Domain models ---

@dataclass
class GameEvent:
    timestamp: float
    team: str  # "red" or "blue"
    points: int  # 2 or 3
    red_score: int
    blue_score: int
    quarter: int
    clock: str  # "M:SS"


@dataclass
class ScoreBreakdown:
    """What a single click earned when a basket happened."""
    player_id: str
    player_name: str
    action: str
    points: float
    basket_team: str
    gap_seconds: float


@dataclass
class SuperstitionClick:
    player_id: str
    player_name: str
    action: str
    timestamp: float
    team: str
    scored: bool = False


@dataclass
class Player:
    id: str
    name: str
    team: str
    magic_score: float = 0.0
    clicks: int = 0
    last_click_time: dict = field(default_factory=dict)  # action_id -> timestamp


# --- Scoring engine ---

CLICK_COOLDOWN = 3.0  # seconds before same action can be clicked again

def compute_correlation_score(seconds_gap: float, positive: bool) -> float:
    """Sliding scale: 0s -> 10 pts, 10s -> 1 pt, >10s -> 0."""
    if seconds_gap > 10.0 or seconds_gap < 0:
        return 0.0
    raw = 10.0 - 0.9 * seconds_gap
    return round(raw, 1) if positive else round(-raw, 1)


# --- Game state ---

SUPERSTITIONS = [
    {"id": "cap", "label": "Turn Cap Around", "emoji": "🧢"},
    {"id": "beer", "label": "Take a Sip", "emoji": "🍺"},
    {"id": "stand", "label": "Stand Up", "emoji": "🧍"},
    {"id": "clap", "label": "Clap 3 Times", "emoji": "👏"},
    {"id": "cross", "label": "Cross Fingers", "emoji": "🤞"},
    {"id": "blow", "label": "Blow on Screen", "emoji": "💨"},
]

SUPERSTITION_MAP = {s["id"]: s for s in SUPERSTITIONS}

QUARTER_SECONDS = 120  # 2 min real-time per quarter
SCORING_INTERVAL_MIN = 4
SCORING_INTERVAL_MAX = 12


class GameState:
    def __init__(self):
        self.players: dict[str, Player] = {}
        self.activity_log: list[dict] = []  # recent activity for the feed
        self.reset()

    def reset(self):
        self.red_score = 0
        self.blue_score = 0
        self.quarter = 1
        self.clock_seconds = QUARTER_SECONDS
        self.events: list[GameEvent] = []
        self.clicks: list[SuperstitionClick] = []
        self.action_scores: dict[str, float] = {s["id"]: 0.0 for s in SUPERSTITIONS}
        self.action_counts: dict[str, int] = {s["id"]: 0 for s in SUPERSTITIONS}
        self.running = False
        self.finished = False
        self.next_basket_in: float = random.uniform(SCORING_INTERVAL_MIN, SCORING_INTERVAL_MAX)
        self.activity_log = []
        for player in self.players.values():
            player.magic_score = 0.0
            player.clicks = 0
            player.last_click_time = {}

    def format_clock(self) -> str:
        m = int(self.clock_seconds) // 60
        s = int(self.clock_seconds) % 60
        return f"{m}:{s:02d}"

    def add_activity(self, entry: dict):
        self.activity_log.append(entry)
        if len(self.activity_log) > 50:
            self.activity_log = self.activity_log[-50:]

    def score_event(self, event: GameEvent) -> list[ScoreBreakdown]:
        """Score clicks against a basket. Returns per-player breakdown."""
        now = event.timestamp
        breakdowns: list[ScoreBreakdown] = []
        for click in self.clicks:
            if click.scored:
                continue
            gap = now - click.timestamp
            if gap < 0 or gap > 10:
                continue
            positive = click.team == event.team
            pts = compute_correlation_score(gap, positive)
            if pts == 0:
                continue
            click.scored = True
            player = self.players.get(click.player_id)
            if player:
                player.magic_score += pts
            self.action_scores[click.action] += pts
            breakdowns.append(ScoreBreakdown(
                player_id=click.player_id,
                player_name=click.player_name,
                action=click.action,
                points=pts,
                basket_team=event.team,
                gap_seconds=round(gap, 1),
            ))
        cutoff = now - 15.0
        self.clicks = [c for c in self.clicks if c.timestamp > cutoff]
        return breakdowns


game = GameState()


# --- WebSocket hub ---

class ConnectionManager:
    def __init__(self):
        self.connections: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.connections.append(ws)

    def disconnect(self, ws: WebSocket):
        if ws in self.connections:
            self.connections.remove(ws)

    async def broadcast(self, message: dict):
        data = json.dumps(message)
        dead = []
        for ws in self.connections:
            try:
                await ws.send_text(data)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.connections.remove(ws)


manager = ConnectionManager()


def build_state_message(msg_type: str = "state", **extra) -> dict:
    top_players = sorted(game.players.values(), key=lambda p: p.magic_score, reverse=True)[:10]
    top_actions = sorted(
        [(aid, game.action_scores[aid], game.action_counts[aid]) for aid in game.action_scores],
        key=lambda x: x[1],
        reverse=True,
    )
    recent_events = game.events[-15:]
    msg = {
        "type": msg_type,
        "red_score": game.red_score,
        "blue_score": game.blue_score,
        "quarter": game.quarter,
        "clock": game.format_clock(),
        "clock_seconds": game.clock_seconds,
        "running": game.running,
        "finished": game.finished,
        "leaderboard": [
            {"id": p.id, "name": p.name, "team": p.team,
             "score": round(p.magic_score, 1), "clicks": p.clicks}
            for p in top_players
        ],
        "actions": [
            {"id": a[0], "score": round(a[1], 1), "count": a[2]}
            for a in top_actions
        ],
        "game_events": [
            {"team": e.team, "points": e.points, "red": e.red_score, "blue": e.blue_score,
             "quarter": e.quarter, "clock": e.clock}
            for e in recent_events
        ],
        "activity": game.activity_log[-20:],
    }
    msg.update(extra)
    return msg


# --- Game simulation loop ---

async def run_game():
    game.reset()
    game.running = True
    game.add_activity({"kind": "system", "text": "Game started!"})
    await manager.broadcast(build_state_message())

    for q in range(1, 5):
        game.quarter = q
        game.clock_seconds = QUARTER_SECONDS
        game.next_basket_in = random.uniform(SCORING_INTERVAL_MIN, SCORING_INTERVAL_MAX)

        quarter_label = "Halftime" if q == 3 else f"Quarter {q}"
        if q > 1:
            game.add_activity({"kind": "system", "text": f"{quarter_label} begins"})
        await manager.broadcast(build_state_message())

        while game.clock_seconds > 0:
            await asyncio.sleep(1)
            game.clock_seconds -= 1
            game.next_basket_in -= 1

            if game.next_basket_in <= 0:
                team = random.choice(["red", "blue"])
                pts = random.choices([2, 3], weights=[75, 25])[0]
                if team == "red":
                    game.red_score += pts
                else:
                    game.blue_score += pts

                evt = GameEvent(
                    timestamp=time.time(),
                    team=team,
                    points=pts,
                    red_score=game.red_score,
                    blue_score=game.blue_score,
                    quarter=q,
                    clock=game.format_clock(),
                )
                game.events.append(evt)
                breakdowns = game.score_event(evt)
                game.next_basket_in = random.uniform(SCORING_INTERVAL_MIN, SCORING_INTERVAL_MAX)

                team_name = "Red" if team == "red" else "Blue"
                game.add_activity({
                    "kind": "basket",
                    "team": team,
                    "text": f"{team_name} scores +{pts}! ({game.red_score}-{game.blue_score})",
                })

                await manager.broadcast(build_state_message(
                    "basket",
                    basket_team=team,
                    basket_points=pts,
                    scoring_breakdowns=[
                        {"player_id": b.player_id, "player_name": b.player_name,
                         "action": b.action, "points": b.points,
                         "gap": b.gap_seconds}
                        for b in breakdowns
                    ],
                ))
            elif int(game.clock_seconds) % 5 == 0:
                await manager.broadcast(build_state_message())

        # Quarter break
        if q < 4:
            label = "Halftime" if q == 2 else f"End of Q{q}"
            game.add_activity({"kind": "system", "text": label})
            await manager.broadcast(build_state_message("quarter_break", break_label=label))
            await asyncio.sleep(5)

    game.running = False
    game.finished = True
    winner = "Red" if game.red_score > game.blue_score else "Blue" if game.blue_score > game.red_score else "Tie"
    game.add_activity({"kind": "system", "text": f"Game over! {winner} wins!" if winner != "Tie" else "Game over! It's a tie!"})
    await manager.broadcast(build_state_message("game_over"))


game_task: asyncio.Task | None = None


# --- Routes ---

@app.get("/", response_class=HTMLResponse)
async def index():
    return (static_dir / "index.html").read_text()


@app.post("/api/start")
async def start_game():
    global game_task
    if game.running:
        return {"status": "already_running"}
    game_task = asyncio.create_task(run_game())
    return {"status": "started"}


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await manager.connect(ws)
    await ws.send_text(json.dumps(build_state_message()))
    try:
        while True:
            raw = await ws.receive_text()
            data = json.loads(raw)

            if data.get("type") == "register":
                pid = data.get("player_id")
                if not pid or pid not in game.players:
                    pid = str(uuid.uuid4())[:8]
                name = data.get("name", "Anon")[:20]
                team = data.get("team", "red")
                if pid not in game.players:
                    game.players[pid] = Player(id=pid, name=name, team=team)
                    game.add_activity({"kind": "join", "text": f"{name} joined {team.title()} Team"})
                await ws.send_text(json.dumps({
                    "type": "registered",
                    "player_id": pid,
                    "player_name": game.players[pid].name,
                    "player_team": game.players[pid].team,
                }))
                await manager.broadcast(build_state_message())

            elif data.get("type") == "click":
                pid = data.get("player_id", "")
                action = data.get("action", "")
                player = game.players.get(pid)
                if not player or action not in game.action_scores or not game.running:
                    continue

                # Cooldown check
                now = time.time()
                last = player.last_click_time.get(action, 0)
                if now - last < CLICK_COOLDOWN:
                    remaining = round(CLICK_COOLDOWN - (now - last), 1)
                    await ws.send_text(json.dumps({
                        "type": "cooldown",
                        "action": action,
                        "remaining": remaining,
                    }))
                    continue

                player.last_click_time[action] = now
                click = SuperstitionClick(
                    player_id=pid,
                    player_name=player.name,
                    action=action,
                    timestamp=now,
                    team=player.team,
                )
                game.clicks.append(click)
                player.clicks += 1
                game.action_counts[action] += 1

                label = SUPERSTITION_MAP[action]["label"]
                emoji = SUPERSTITION_MAP[action]["emoji"]
                game.add_activity({
                    "kind": "click",
                    "team": player.team,
                    "text": f"{emoji} {player.name} — {label}",
                })

                await manager.broadcast(build_state_message(
                    "click_ack",
                    click_player=player.name,
                    click_action=action,
                    click_team=player.team,
                ))
    except WebSocketDisconnect:
        manager.disconnect(ws)
