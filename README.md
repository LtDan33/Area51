# Magic 8 Ball - Advanced AI Edition

A brutally honest Magic 8 Ball that tells you what you need to hear, not what you want to hear.

## Features

- Beautiful modern UI with smoke effects and animations
- 15 unique responses (all variations of "no")
- FastAPI backend
- Responsive design

## Installation

```bash
poetry install
```

## Running

```bash
poetry run uvicorn app.main:app --reload
```

Then open http://localhost:8000 in your browser.

## API

- `GET /` - Serves the main page
- `GET /api/shake` - Returns a random Magic 8 Ball response
