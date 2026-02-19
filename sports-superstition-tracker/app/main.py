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
    timestamp: float  # server time
    team: str  # "red" or "blue"
    points: int  # 2 or 3
    red_score: int
    blue_score: int
    quarter: int
    clock: str  # "MM:SS"


@dataclass
class SuperstitionClick:
    player_id: str
    player_name: str
    action: str
    timestamp: float
    team: str  # which team they're rooting for


@dataclass
class Player:
    id: str
    name: str
    team: str
    magic_score: float = 0.0
    clicks: int = 0


# --- Scoring engine ---

def compute_correlation_score(seconds_gap: float, positive: bool) -> float:
    """Sliding scale: 1s -> 10 pts, 10s -> 1 pt, >10s -> 0.
    Linear interpolation between those bounds.
    Negative events invert the sign."""
    if seconds_gap > 10.0 or seconds_gap < 0:
        return 0.0
    # 10 at 0s, 1 at 10s  =>  score = 10 - 9*(gap/10) = 10 - 0.9*gap
    raw = 10.0 - 0.9 * seconds_gap
    raw = max(raw, 0.0)
    return raw if positive else -raw


# --- Game state (in-memory, single instance for demo) ---

SUPERSTITIONS = [
    {"id": "cap", "label": "Turn Cap Around"},
    {"id": "beer", "label": "Take a Sip of Beer"},
    {"id": "stand", "label": "Stand Up"},
    {"id": "clap", "label": "Clap Three Times"},
    {"id": "cross", "label": "Cross Fingers"},
    {"id": "blow", "label": "Blow on the Screen"},
]

# Quarter length in simulated seconds (real-time seconds for demo)
QUARTER_SECONDS = 120  # 2 minutes real-time per quarter
SCORING_INTERVAL_MIN = 4  # min seconds between baskets
SCORING_INTERVAL_MAX = 12  # max seconds between baskets


class GameState:
    def __init__(self):
        self.reset()

    def reset(self):
        self.red_score = 0
        self.blue_score = 0
        self.quarter = 1
        self.clock_seconds = QUARTER_SECONDS
        self.events: list[GameEvent] = []
        self.clicks: list[SuperstitionClick] = []
        self.players: dict[str, Player] = {}
        self.action_scores: dict[str, float] = {s["id"]: 0.0 for s in SUPERSTITIONS}
        self.action_counts: dict[str, int] = {s["id"]: 0 for s in SUPERSTITIONS}
        self.running = False
        self.finished = False
        self.next_basket_in: float = random.uniform(SCORING_INTERVAL_MIN, SCORING_INTERVAL_MAX)

    def format_clock(self) -> str:
        m = int(self.clock_seconds) // 60
        s = int(self.clock_seconds) % 60
        return f"{m}:{s:02d}"

    def score_event(self, event: GameEvent):
        """After a basket, look back at recent clicks and award/deduct points."""
        now = event.timestamp
        for click in self.clicks:
            gap = now - click.timestamp
            if gap < 0 or gap > 10:
                continue
            # positive if click's team matches scoring team
            positive = click.team == event.team
            pts = compute_correlation_score(gap, positive)
            if pts == 0:
                continue
            player = self.players.get(click.player_id)
            if player:
                player.magic_score += pts
            self.action_scores[click.action] += pts
        # prune old clicks (older than 15s)
        cutoff = now - 15.0
        self.clicks = [c for c in self.clicks if c.timestamp > cutoff]


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


async def send_full_state(ws: WebSocket):
    """Send entire game state to a newly connected client."""
    await ws.send_text(json.dumps(build_state_message()))


def build_state_message() -> dict:
    top_players = sorted(game.players.values(), key=lambda p: p.magic_score, reverse=True)[:10]
    top_actions = sorted(
        [(aid, game.action_scores[aid], game.action_counts[aid]) for aid in game.action_scores],
        key=lambda x: x[1],
        reverse=True,
    )
    recent_events = game.events[-15:]  # last 15 baskets
    return {
        "type": "state",
        "red_score": game.red_score,
        "blue_score": game.blue_score,
        "quarter": game.quarter,
        "clock": game.format_clock(),
        "running": game.running,
        "finished": game.finished,
        "leaderboard": [
            {"name": p.name, "team": p.team, "score": round(p.magic_score, 1), "clicks": p.clicks}
            for p in top_players
        ],
        "actions": [
            {"id": a[0], "score": round(a[1], 1), "count": a[2]}
            for a in top_actions
        ],
        "events": [
            {"team": e.team, "points": e.points, "red": e.red_score, "blue": e.blue_score,
             "quarter": e.quarter, "clock": e.clock}
            for e in recent_events
        ],
    }


# --- Game simulation loop ---

async def run_game():
    game.reset()
    game.running = True
    await manager.broadcast(build_state_message())

    for q in range(1, 5):  # 4 quarters
        game.quarter = q
        game.clock_seconds = QUARTER_SECONDS
        game.next_basket_in = random.uniform(SCORING_INTERVAL_MIN, SCORING_INTERVAL_MAX)
        await manager.broadcast(build_state_message())

        while game.clock_seconds > 0:
            await asyncio.sleep(1)
            game.clock_seconds -= 1
            game.next_basket_in -= 1

            if game.next_basket_in <= 0:
                # a basket happens
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
                game.score_event(evt)
                game.next_basket_in = random.uniform(SCORING_INTERVAL_MIN, SCORING_INTERVAL_MAX)

                await manager.broadcast({
                    "type": "basket",
                    "team": team,
                    "points": pts,
                    **build_state_message(),
                })
            elif int(game.clock_seconds) % 5 == 0:
                # periodic clock update every 5s
                await manager.broadcast(build_state_message())

        # quarter break
        if q < 4:
            await manager.broadcast({
                "type": "quarter_end",
                "quarter": q,
                **build_state_message(),
            })
            await asyncio.sleep(3)

    game.running = False
    game.finished = True
    await manager.broadcast({
        "type": "game_over",
        **build_state_message(),
    })


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
    await send_full_state(ws)
    try:
        while True:
            raw = await ws.receive_text()
            data = json.loads(raw)

            if data.get("type") == "register":
                pid = str(uuid.uuid4())[:8]
                name = data.get("name", "Anon")[:20]
                team = data.get("team", "red")
                game.players[pid] = Player(id=pid, name=name, team=team)
                await ws.send_text(json.dumps({"type": "registered", "player_id": pid}))
                await manager.broadcast(build_state_message())

            elif data.get("type") == "click":
                pid = data.get("player_id", "")
                action = data.get("action", "")
                if pid in game.players and action in game.action_scores and game.running:
                    click = SuperstitionClick(
                        player_id=pid,
                        player_name=game.players[pid].name,
                        action=action,
                        timestamp=time.time(),
                        team=game.players[pid].team,
                    )
                    game.clicks.append(click)
                    game.players[pid].clicks += 1
                    game.action_counts[action] += 1
                    await manager.broadcast({
                        "type": "click_ack",
                        "player": game.players[pid].name,
                        "action": action,
                        **build_state_message(),
                    })
    except WebSocketDisconnect:
        manager.disconnect(ws)
