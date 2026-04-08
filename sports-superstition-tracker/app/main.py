import asyncio
import json
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
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
    streak: int = 0  # current positive-scoring streak after this click resolved


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
    positive_clicks: int = 0
    streak: int = 0  # current run of positive-scoring clicks
    max_streak: int = 0  # best streak this game
    best_click: dict | None = None  # {action, points, gap, basket_team, clock}
    action_scores: dict = field(default_factory=dict)  # per-action sum of points
    last_click_time: dict = field(default_factory=dict)  # action_id -> timestamp


# --- Scoring engine ---

CLICK_COOLDOWN = 3.0  # seconds before same action can be clicked again

def compute_correlation_score(seconds_gap: float, positive: bool) -> float:
    """Peak ±10 for gaps 0–0.5s, linear decay to 0 at 10s, 0 outside the window."""
    if seconds_gap < 0 or seconds_gap > 10.0:
        return 0.0
    if seconds_gap <= 0.5:
        raw = 10.0
    else:
        raw = 10.0 * (1.0 - (seconds_gap - 0.5) / 9.5)
    return round(raw if positive else -raw, 1)


# --- Game config ---

SUPERSTITIONS = [
    {"id": "cap",   "label": "Turn Hat Backwards", "emoji": "🧢"},
    {"id": "beer",  "label": "Take a Sip",          "emoji": "🍺"},
    {"id": "knock", "label": "Knock on Wood",       "emoji": "🪵"},
]

SUPERSTITION_MAP = {s["id"]: s for s in SUPERSTITIONS}

GAME_SECONDS = 60  # single-half 60-second test game

# Deterministic scripted basket events: (offset_seconds_from_start, team, points)
# Final score: Red 9 — Blue 10
GAME_SCRIPT: list[tuple[int, str, int]] = [
    (5,  "red",  2),
    (12, "blue", 3),
    (18, "red",  2),
    (25, "blue", 2),
    (32, "red",  3),
    (40, "blue", 2),
    (48, "red",  2),
    (55, "blue", 3),
]


class GameState:
    def __init__(self):
        self.players: dict[str, Player] = {}
        self.activity_log: list[dict] = []  # recent activity for the feed
        self.reset()

    def reset(self):
        self.red_score = 0
        self.blue_score = 0
        self.clock_seconds = GAME_SECONDS
        self.events: list[GameEvent] = []
        self.clicks: list[SuperstitionClick] = []
        self.action_scores: dict[str, float] = {s["id"]: 0.0 for s in SUPERSTITIONS}
        self.action_counts: dict[str, int] = {s["id"]: 0 for s in SUPERSTITIONS}
        self.running = False
        self.finished = False
        self.activity_log = []
        for player in self.players.values():
            player.magic_score = 0.0
            player.clicks = 0
            player.positive_clicks = 0
            player.streak = 0
            player.max_streak = 0
            player.best_click = None
            player.action_scores = {}
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
                player.action_scores[click.action] = (
                    player.action_scores.get(click.action, 0.0) + pts
                )
                if pts > 0:
                    player.positive_clicks += 1
                    player.streak += 1
                    if player.streak > player.max_streak:
                        player.max_streak = player.streak
                else:
                    player.streak = 0
                if player.best_click is None or pts > player.best_click["points"]:
                    player.best_click = {
                        "action": click.action,
                        "points": pts,
                        "gap": round(gap, 1),
                        "basket_team": event.team,
                        "clock": event.clock,
                    }
            self.action_scores[click.action] += pts
            breakdowns.append(ScoreBreakdown(
                player_id=click.player_id,
                player_name=click.player_name,
                action=click.action,
                points=pts,
                basket_team=event.team,
                gap_seconds=round(gap, 1),
                streak=player.streak if player else 0,
            ))
        cutoff = now - 15.0
        self.clicks = [c for c in self.clicks if c.timestamp > cutoff]
        return breakdowns


game = GameState()


# --- SSE hub ---

class SSEHub:
    """Fan-out async hub. Each subscriber owns a queue; broadcast pushes to all."""

    def __init__(self):
        self.subscribers: list[asyncio.Queue[str]] = []

    def subscribe(self) -> asyncio.Queue[str]:
        q: asyncio.Queue[str] = asyncio.Queue(maxsize=64)
        self.subscribers.append(q)
        return q

    def unsubscribe(self, q: asyncio.Queue[str]) -> None:
        if q in self.subscribers:
            self.subscribers.remove(q)

    async def broadcast(self, message: dict) -> None:
        data = json.dumps(message)
        for q in list(self.subscribers):
            try:
                q.put_nowait(data)
            except asyncio.QueueFull:
                # Slow subscriber — drop this message rather than block
                pass


hub = SSEHub()


def player_recap(p: Player) -> dict:
    """Per-player end-of-game recap snapshot."""
    top_action_id = None
    top_action_pts = 0.0
    for aid, pts in p.action_scores.items():
        if pts > top_action_pts:
            top_action_pts = pts
            top_action_id = aid
    return {
        "id": p.id,
        "name": p.name,
        "team": p.team,
        "score": round(p.magic_score, 1),
        "clicks": p.clicks,
        "positive_clicks": p.positive_clicks,
        "max_streak": p.max_streak,
        "best_click": p.best_click,
        "top_action": {
            "id": top_action_id,
            "points": round(top_action_pts, 1),
        } if top_action_id else None,
    }


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
        "clock": game.format_clock(),
        "clock_seconds": game.clock_seconds,
        "running": game.running,
        "finished": game.finished,
        "leaderboard": [
            {"id": p.id, "name": p.name, "team": p.team,
             "score": round(p.magic_score, 1), "clicks": p.clicks,
             "streak": p.streak, "max_streak": p.max_streak}
            for p in top_players
        ],
        "actions": [
            {"id": a[0], "score": round(a[1], 1), "count": a[2]}
            for a in top_actions
        ],
        "game_events": [
            {"team": e.team, "points": e.points, "red": e.red_score, "blue": e.blue_score,
             "clock": e.clock}
            for e in recent_events
        ],
        "activity": game.activity_log[-20:],
    }
    if msg_type == "game_over":
        msg["recap"] = [player_recap(p) for p in top_players]
    msg.update(extra)
    return msg


# --- Game simulation loop ---

async def run_game():
    game.reset()
    # Pre-game countdown phase. Game is not yet running so clicks are rejected.
    game.add_activity({"kind": "system", "text": "Tip-off in 3..."})
    await hub.broadcast(build_state_message("countdown", countdown=3))
    await asyncio.sleep(1)
    await hub.broadcast(build_state_message("countdown", countdown=2))
    await asyncio.sleep(1)
    await hub.broadcast(build_state_message("countdown", countdown=1))
    await asyncio.sleep(1)

    game.running = True
    game.add_activity({"kind": "system", "text": "Game on!"})
    await hub.broadcast(build_state_message("countdown", countdown=0))

    script = list(GAME_SCRIPT)
    next_idx = 0

    while game.clock_seconds > 0:
        await asyncio.sleep(1)
        game.clock_seconds -= 1
        elapsed = GAME_SECONDS - game.clock_seconds

        # Fire any scripted baskets that this tick crossed
        while next_idx < len(script) and script[next_idx][0] <= elapsed:
            offset, team, pts = script[next_idx]
            next_idx += 1

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
                clock=game.format_clock(),
            )
            game.events.append(evt)
            breakdowns = game.score_event(evt)

            team_name = "Red" if team == "red" else "Blue"
            game.add_activity({
                "kind": "basket",
                "team": team,
                "text": f"{team_name} scores +{pts}! ({game.red_score}-{game.blue_score})",
            })

            await hub.broadcast(build_state_message(
                "basket",
                basket_team=team,
                basket_points=pts,
                scoring_breakdowns=[
                    {"player_id": b.player_id, "player_name": b.player_name,
                     "action": b.action, "points": b.points,
                     "gap": b.gap_seconds, "streak": b.streak}
                    for b in breakdowns
                ],
            ))

        # Heartbeat every 5s so clients stay in sync even without a basket
        if int(game.clock_seconds) % 5 == 0:
            await hub.broadcast(build_state_message())

    game.running = False
    game.finished = True
    if game.red_score > game.blue_score:
        winner = "Red"
    elif game.blue_score > game.red_score:
        winner = "Blue"
    else:
        winner = "Tie"
    game.add_activity({
        "kind": "system",
        "text": f"Game over! {winner} wins!" if winner != "Tie" else "Game over! It's a tie!",
    })
    await hub.broadcast(build_state_message("game_over"))


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


@app.post("/api/register")
async def register_player(payload: dict):
    pid = payload.get("player_id")
    if not pid or pid not in game.players:
        pid = str(uuid.uuid4())[:8]
    name = str(payload.get("name", "Anon"))[:20] or "Anon"
    team = payload.get("team", "red")
    if team not in ("red", "blue"):
        team = "red"
    if pid not in game.players:
        game.players[pid] = Player(id=pid, name=name, team=team)
        game.add_activity({"kind": "join", "text": f"{name} joined {team.title()} Team"})
    else:
        # Allow updating name/team on re-register
        game.players[pid].name = name
        game.players[pid].team = team

    await hub.broadcast(build_state_message())
    return {
        "player_id": pid,
        "player_name": game.players[pid].name,
        "player_team": game.players[pid].team,
    }


@app.post("/api/click")
async def click_action(payload: dict):
    pid = payload.get("player_id", "")
    action = payload.get("action", "")
    player = game.players.get(pid)
    if not player:
        return JSONResponse({"error": "unknown_player"}, status_code=404)
    if action not in game.action_scores:
        return JSONResponse({"error": "unknown_action"}, status_code=400)
    if not game.running:
        return JSONResponse({"error": "game_not_running"}, status_code=409)

    now = time.time()
    last = player.last_click_time.get(action, 0)
    if now - last < CLICK_COOLDOWN:
        remaining = round(CLICK_COOLDOWN - (now - last), 1)
        return JSONResponse(
            {"error": "cooldown", "action": action, "remaining": remaining},
            status_code=429,
        )

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

    await hub.broadcast(build_state_message(
        "click_ack",
        click_player=player.name,
        click_action=action,
        click_team=player.team,
    ))
    return {"status": "ok"}


@app.get("/api/stream")
async def stream(request: Request):
    async def event_generator():
        q = hub.subscribe()
        try:
            # Send current state immediately so new clients paint right away
            yield f"data: {json.dumps(build_state_message())}\n\n"
            while True:
                if await request.is_disconnected():
                    break
                try:
                    data = await asyncio.wait_for(q.get(), timeout=15.0)
                    yield f"data: {data}\n\n"
                except asyncio.TimeoutError:
                    # Keep-alive comment so proxies don't close the stream
                    yield ": keep-alive\n\n"
        finally:
            hub.unsubscribe(q)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache, no-transform",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )
