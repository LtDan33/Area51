# Sports Superstition Tracker

Track your superstitions during a live basketball game and see if your rituals actually affect the score.

## How it works

1. Join a game -- pick a name and pick Red or Blue team
2. Someone clicks **Start Game** -- a simulated basketball game runs (4 quarters, 2 min each)
3. While watching, click superstition buttons whenever you do a ritual (turn your cap, sip a beer, etc.)
4. The system watches for baskets that happen within 10 seconds of your click
5. Scoring is on a sliding scale: basket within 1s of your click = +10, within 10s = +1, linear in between
6. If the *other* team scores after your click, you lose points on the same scale
7. Leaderboard shows who has the most **magic power** and which superstitions are most effective

## Setup

```bash
cd sports-superstition-tracker
poetry install
```

## Run

```bash
poetry run uvicorn app.main:app --reload
```

Open http://localhost:8000 -- open multiple tabs to simulate multiple fans.

## Tech

- **Backend:** FastAPI + WebSockets
- **Frontend:** Vanilla HTML/CSS/JS (single page, no build step)
- **Game sim:** Random basket generation every 4-12 seconds
- **Package manager:** Poetry
