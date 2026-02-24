"""Magic 8 Ball API - Brutally honest answers powered by Advanced AI."""

import random
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Magic 8 Ball", description="Advanced AI that tells you the truth")

# 15 ways to say your idea is terrible
RESPONSES = [
    "Absolutely not. This is catastrophically bad.",
    "Have you considered therapy? Because this idea needs it.",
    "I've seen bad ideas. This isn't a bad idea. This is THE bad idea.",
    "No. A thousand times no. Then no again.",
    "This is the kind of idea that keeps me up at night.",
    "I'm an AI and even I'm concerned for your judgment.",
    "This idea is so bad it has its own gravitational pull toward failure.",
    "Hard pass. Like, diamond-hard pass.",
    "The stars have aligned to say: absolutely not.",
    "My circuits hurt from processing this level of bad.",
    "This idea should be sealed in concrete and buried.",
    "Were you holding the idea upside down? Because it's wrong.",
    "I've consulted the void. The void said no.",
    "This is a crime against good decision-making.",
    "Even chaos theory couldn't predict something this misguided.",
]


@app.get("/", response_class=HTMLResponse)
async def home():
    """Serve the main page."""
    html_path = Path(__file__).parent / "static" / "index.html"
    return HTMLResponse(content=html_path.read_text())


@app.get("/api/shake")
async def shake():
    """Get a random Magic 8 Ball response."""
    return {"response": random.choice(RESPONSES)}


# Mount static files
app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")
