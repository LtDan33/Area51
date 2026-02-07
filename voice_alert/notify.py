"""
Voice notification for Claude Code task completion.

Designed to run as a Claude Code PostToolUse hook on Windows 10.
When Claude updates todos and all tasks are completed, speaks an alert.

Supports multiple TTS backends (configure via environment variables):
  - elevenlabs : Best quality voices, free tier (10k chars/month)
  - openai     : Cheap ($0.015/1K chars), good quality
  - edge       : Completely free, uses Microsoft Edge online TTS
  - pyttsx3    : Free, offline, uses Windows SAPI (built-in voices)

Usage as a hook (called automatically by Claude Code):
  python notify.py              # reads hook JSON from stdin

Manual test:
  python notify.py --test       # speaks a test message
  python notify.py --test --tts openai --message "Hello world"
"""

import argparse
import io
import json
import os
import sys
import tempfile
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration (override with env vars or a .env file next to this script)
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).parent

# Which TTS backend to use: elevenlabs | openai | edge | pyttsx3
TTS_BACKEND = os.getenv("VOICE_ALERT_TTS", "pyttsx3")

# API keys (only needed for the backend you pick)
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Voice settings
ELEVENLABS_VOICE = os.getenv("ELEVENLABS_VOICE", "Rachel")  # or voice ID
OPENAI_VOICE = os.getenv("OPENAI_VOICE", "nova")  # alloy|echo|fable|onyx|nova|shimmer
OPENAI_MODEL = os.getenv("OPENAI_TTS_MODEL", "tts-1")  # tts-1 or tts-1-hd
EDGE_VOICE = os.getenv("EDGE_VOICE", "en-US-JennyNeural")

# Default completion message
DEFAULT_MESSAGE = os.getenv(
    "VOICE_ALERT_MESSAGE",
    "All tasks are complete. Your Claude plan is finished.",
)


# ---------------------------------------------------------------------------
# TTS backends
# ---------------------------------------------------------------------------


def _play_audio_bytes(audio_bytes: bytes, fmt: str = "mp3"):
    """Write audio bytes to a temp file and play it on Windows."""
    suffix = f".{fmt}"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as f:
        f.write(audio_bytes)
        tmp_path = f.name

    try:
        if sys.platform == "win32":
            # Try playsound first, fall back to os.startfile
            try:
                from playsound import playsound
                playsound(tmp_path)
            except ImportError:
                os.startfile(tmp_path)
                import time
                time.sleep(5)  # give it time to play
        elif sys.platform == "darwin":
            import subprocess
            subprocess.run(["afplay", tmp_path], check=True)
        else:
            # Linux fallback
            import subprocess
            for player in ["mpv", "ffplay", "aplay", "paplay"]:
                try:
                    cmd = [player]
                    if player == "ffplay":
                        cmd += ["-nodisp", "-autoexit"]
                    cmd.append(tmp_path)
                    subprocess.run(cmd, check=True, capture_output=True)
                    break
                except (FileNotFoundError, subprocess.CalledProcessError):
                    continue
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass


def speak_elevenlabs(message: str):
    """Use ElevenLabs API for high-quality TTS."""
    from elevenlabs import ElevenLabs

    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio_iter = client.text_to_speech.convert(
        text=message,
        voice_id=ELEVENLABS_VOICE,
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )
    audio_bytes = b"".join(audio_iter)
    _play_audio_bytes(audio_bytes, "mp3")


def speak_openai(message: str):
    """Use OpenAI TTS API. Very cheap: ~$0.015 per 1K characters."""
    from openai import OpenAI

    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.audio.speech.create(
        model=OPENAI_MODEL,
        voice=OPENAI_VOICE,
        input=message,
    )
    _play_audio_bytes(response.content, "mp3")


def speak_edge(message: str):
    """Use edge-tts (free, no API key, good quality Microsoft voices)."""
    import asyncio
    import edge_tts

    async def _generate():
        communicate = edge_tts.Communicate(message, EDGE_VOICE)
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
            tmp_path = f.name
        await communicate.save(tmp_path)
        return tmp_path

    tmp_path = asyncio.run(_generate())
    with open(tmp_path, "rb") as f:
        audio_bytes = f.read()
    os.unlink(tmp_path)
    _play_audio_bytes(audio_bytes, "mp3")


def speak_pyttsx3(message: str):
    """Use pyttsx3 (offline, uses Windows SAPI voices). No API key needed."""
    import pyttsx3

    engine = pyttsx3.init()
    engine.setProperty("rate", 170)  # slightly slower for clarity
    engine.say(message)
    engine.runAndWait()


BACKENDS = {
    "elevenlabs": speak_elevenlabs,
    "openai": speak_openai,
    "edge": speak_edge,
    "pyttsx3": speak_pyttsx3,
}


def speak(message: str, backend: str | None = None):
    """Speak a message using the configured TTS backend."""
    backend = backend or TTS_BACKEND
    fn = BACKENDS.get(backend)
    if fn is None:
        print(f"[voice_alert] Unknown TTS backend: {backend}", file=sys.stderr)
        print(f"[voice_alert] Available: {', '.join(BACKENDS)}", file=sys.stderr)
        sys.exit(1)

    try:
        fn(message)
    except ImportError as e:
        print(f"[voice_alert] Missing dependency for '{backend}': {e}", file=sys.stderr)
        print(f"[voice_alert] Run: pip install -r requirements.txt", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[voice_alert] TTS error ({backend}): {e}", file=sys.stderr)
        sys.exit(1)


# ---------------------------------------------------------------------------
# Hook logic — parse stdin from Claude Code PostToolUse hook
# ---------------------------------------------------------------------------


def check_todos_complete(hook_data: dict) -> bool:
    """Return True if the TodoWrite hook input shows all tasks completed."""
    tool_input = hook_data.get("tool_input", {})

    # tool_input could be a string (JSON) or already a dict
    if isinstance(tool_input, str):
        try:
            tool_input = json.loads(tool_input)
        except json.JSONDecodeError:
            return False

    todos = tool_input.get("todos", [])
    if not todos:
        return False

    return all(t.get("status") == "completed" for t in todos)


def run_hook():
    """Entry point when called as a Claude Code hook."""
    stdin_data = sys.stdin.read().strip()
    if not stdin_data:
        return

    try:
        hook_data = json.loads(stdin_data)
    except json.JSONDecodeError:
        return

    # Only fire on TodoWrite where everything is done
    tool_name = hook_data.get("tool_name", "")
    if tool_name != "TodoWrite":
        return

    if check_todos_complete(hook_data):
        speak(DEFAULT_MESSAGE)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(description="Voice alert for Claude Code")
    parser.add_argument("--test", action="store_true", help="Speak a test message")
    parser.add_argument("--tts", choices=list(BACKENDS), help="TTS backend to use")
    parser.add_argument("--message", "-m", type=str, help="Custom message to speak")
    parser.add_argument(
        "--list-voices", action="store_true",
        help="List available voices for the current backend",
    )
    args = parser.parse_args()

    if args.list_voices:
        backend = args.tts or TTS_BACKEND
        if backend == "pyttsx3":
            import pyttsx3
            engine = pyttsx3.init()
            for voice in engine.getProperty("voices"):
                print(f"  {voice.id} — {voice.name}")
        elif backend == "edge":
            import asyncio
            import edge_tts
            voices = asyncio.run(edge_tts.list_voices())
            for v in voices:
                if v["Locale"].startswith("en-"):
                    print(f"  {v['ShortName']} — {v['FriendlyName']}")
        elif backend == "openai":
            print("  alloy, echo, fable, onyx, nova, shimmer")
        elif backend == "elevenlabs":
            print("  See https://elevenlabs.io/voice-library")
        return

    if args.test:
        msg = args.message or "Testing, testing. Your Claude plan is complete!"
        speak(msg, backend=args.tts)
        return

    # Default: run as hook (reads stdin)
    run_hook()


if __name__ == "__main__":
    main()
