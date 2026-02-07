# Voice Alert for Claude Code

Get a spoken notification when Claude finishes all tasks in a plan.

Uses a **Claude Code hook** that fires on `TodoWrite` — when Claude marks every
todo as `completed`, the script speaks an alert through your chosen TTS backend.

## Quick Start (5 minutes)

### 1. Pick a TTS backend and install it

| Backend | Cost | Quality | Install |
|---------|------|---------|---------|
| **edge-tts** | Free | Great (Microsoft Neural) | `pip install edge-tts` |
| **OpenAI TTS** | ~$0.015/1K chars | Great | `pip install openai` |
| **ElevenLabs** | Free tier (10k chars/mo) | Best | `pip install elevenlabs` |
| **pyttsx3** | Free, offline | OK (Windows SAPI) | `pip install pyttsx3` |

For audio playback, also install: `pip install playsound`

### 2. Set environment variables

Only set the ones for your chosen backend:

```powershell
# Pick your backend (elevenlabs | openai | edge | pyttsx3)
$env:VOICE_ALERT_TTS = "edge"

# If using OpenAI TTS
$env:OPENAI_API_KEY = "sk-..."
$env:OPENAI_VOICE = "nova"          # alloy|echo|fable|onyx|nova|shimmer

# If using ElevenLabs
$env:ELEVENLABS_API_KEY = "..."
$env:ELEVENLABS_VOICE = "Rachel"    # name or voice ID

# If using edge-tts
$env:EDGE_VOICE = "en-US-JennyNeural"

# Custom completion message (optional)
$env:VOICE_ALERT_MESSAGE = "Hey, your tasks are all done!"
```

To make these permanent on Windows, add them via:
**Settings > System > About > Advanced system settings > Environment Variables**

### 3. Test it

```bash
python voice_alert/notify.py --test
python voice_alert/notify.py --test --tts edge --message "Testing edge voices"
python voice_alert/notify.py --test --tts openai
```

### 4. List available voices

```bash
python voice_alert/notify.py --list-voices --tts edge
python voice_alert/notify.py --list-voices --tts pyttsx3
```

### 5. Add the Claude Code hook

Add this to your Claude Code settings file. On Windows this is typically at:

- **Project-level:** `.claude/settings.json` in your repo
- **User-level:** `%USERPROFILE%\.claude\settings.json`

```jsonc
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": {
          "tool_name": "TodoWrite"
        },
        "hooks": [
          {
            "type": "command",
            "command": "python C:/path/to/your/voice_alert/notify.py"
          }
        ]
      }
    ]
  }
}
```

Replace `C:/path/to/your/voice_alert/notify.py` with the actual path to the
script on your machine.

## How It Works

```
Claude finishes all tasks
        │
        ▼
Claude calls TodoWrite (all todos → "completed")
        │
        ▼
Claude Code fires PostToolUse hook
        │
        ▼
notify.py receives hook JSON on stdin
        │
        ▼
Checks: are ALL todos completed?
        │
    ┌───┴───┐
    No      Yes ──► Speak the alert via your chosen TTS
    │
    (exit silently)
```

## Backend Comparison

### edge-tts (Recommended for free)
Completely free, no API key. Uses Microsoft Edge's online neural TTS service.
Good variety of natural-sounding voices.

### OpenAI TTS (Recommended for cheap + great)
About $0.015 per 1,000 characters — a short "task done" alert costs a fraction
of a penny. Six voice options, all sound natural. Requires an OpenAI API key.

### ElevenLabs (Best quality)
Most natural and expressive voices. Free tier gives 10,000 characters/month
(enough for ~200+ alerts). Paid plans start at $5/month.

### pyttsx3 (Offline fallback)
Uses whatever voices Windows has installed (SAPI). No internet needed, but the
voices sound more robotic. Good as a no-setup fallback.

## Customization

Set `VOICE_ALERT_MESSAGE` to change what gets spoken:

```powershell
$env:VOICE_ALERT_MESSAGE = "Yo, Claude is done. Go check it out."
```

You can also call the script directly from any other automation:

```python
from voice_alert.notify import speak
speak("Build succeeded!", backend="openai")
```
