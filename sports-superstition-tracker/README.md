# Sports Superstition Tracker — 60s Demo

A simple social web app that mocks a 60-second basketball game and lets you click your superstitions (turn hat, sip beer, knock on wood) during play to see if your rituals actually correlate with your team scoring. Mobile-first, best with friends.

## How it works

1. Join a game — pick a name and pick Red or Blue team
2. Someone clicks **Start Game** — a deterministic 60-second scripted basketball game runs (8 baskets, same script every run for a clean demo)
3. While watching, click one of the **3 superstition buttons** (Turn Hat 🧢, Sip Beer 🍺, Knock on Wood 🪵) whenever you do a ritual
4. The system watches for baskets that happen within 10 seconds of your click
5. Scoring curve: basket within 0.5s of your click = **+10**, linear decay to 0 at 10s
6. If the *other* team scores after your click, you lose points on the same scale
7. Leaderboard shows who has the most **magic power** and which superstitions are most effective

Each action has a 3-second cooldown to prevent spamming. You get a personal toast notification whenever a basket connects to one of your clicks.

## Prerequisites

- Python 3.11+
- [Poetry](https://python-poetry.org/docs/#installation)

## Setup

```bash
cd sports-superstition-tracker
poetry install
```

## Run

```bash
poetry run uvicorn app.main:app --reload
```

Open http://localhost:8000 in a browser. Open multiple tabs or share the URL on your local network to play with friends.

To make the server accessible to other devices on your network:

```bash
poetry run uvicorn app.main:app --reload --host 0.0.0.0
```

Then open `http://<your-ip>:8000` on any phone or laptop on the same network.

## Test

```bash
poetry run pytest
```

## Tech

- **Backend:** FastAPI + Server-Sent Events (one-way live updates) + HTTP POST for actions
- **Frontend:** Vanilla HTML/CSS/JS (single page, no build step, mobile-first), `EventSource` for live state
- **Game sim:** Deterministic 60-second script with 8 baskets — repeatable for demo purposes
- **Package manager:** Poetry
