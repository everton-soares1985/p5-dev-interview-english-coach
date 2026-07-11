"""
Gemini API client for P5 Dev Interview English Coach.
Uses the current google-genai SDK (replaces deprecated google.generativeai).
Handles file upload (video), polling for ACTIVE status, and content generation.
"""
import os
import time
from pathlib import Path

import google.genai as genai
from google.genai import types
from rich.console import Console

console = Console()

MODEL_NAME = "gemini-2.5-flash"
MAX_WAIT_SECONDS = 120
POLL_INTERVAL = 5

_client: genai.Client | None = None


def configure_client() -> None:
    """Configure Gemini client with API key from environment."""
    global _client
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        console.print("[red]Error: GEMINI_API_KEY not found in environment.[/red]")
        console.print("  Set it in your .env file: GEMINI_API_KEY=your_key_here")
        raise SystemExit(1)
    
    # Remove GOOGLE_API_KEY from os.environ so google-genai does not warn or override GEMINI_API_KEY
    if "GOOGLE_API_KEY" in os.environ:
        os.environ.pop("GOOGLE_API_KEY")
        
    _client = genai.Client(api_key=api_key)


def _get_client() -> genai.Client:
    if _client is None:
        raise RuntimeError("Call configure_client() before using the Gemini client.")
    return _client


def upload_video(video_path: Path):
    """Upload a video file to Gemini Files API and return the file object."""
    client = _get_client()
    console.print(f"[cyan]Uploading: {video_path.name}[/cyan]")
    uploaded_file = client.files.upload(
        file=str(video_path),
        config=types.UploadFileConfig(display_name=video_path.name),
    )
    console.print("[green]✓ Upload complete.[/green]")
    return uploaded_file


def wait_for_active(uploaded_file):
    """Poll until file processing state is ACTIVE. Raises SystemExit on timeout/failure."""
    client = _get_client()
    console.print("[cyan]Waiting for Gemini to process the video...[/cyan]")
    elapsed = 0
    while uploaded_file.state.name == "PROCESSING":
        if elapsed >= MAX_WAIT_SECONDS:
            console.print(
                f"[red]Error: Timeout after {MAX_WAIT_SECONDS}s waiting for video processing.[/red]"
            )
            raise SystemExit(1)
        time.sleep(POLL_INTERVAL)
        elapsed += POLL_INTERVAL
        uploaded_file = client.files.get(name=uploaded_file.name)
        console.print(f"  Processing... ({elapsed}s)")

    if uploaded_file.state.name == "FAILED":
        console.print("[red]Error: Gemini failed to process the video file.[/red]")
        raise SystemExit(1)

    console.print("[green]✓ Video ready for analysis.[/green]")
    return uploaded_file


def generate_from_video(uploaded_file, prompt: str) -> str:
    """Send uploaded video + prompt to Gemini and return the text response."""
    client = _get_client()
    console.print("[cyan]Analyzing with Gemini multimodal...[/cyan]")
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[uploaded_file, prompt],
    )
    return response.text


def generate_from_transcript(transcript_text: str, prompt: str) -> str:
    """Send transcript text + prompt to Gemini and return the text response."""
    client = _get_client()
    console.print("[cyan]Analyzing transcript with Gemini...[/cyan]")
    full_prompt = f"{prompt}\n\n---\n\nINTERVIEW TRANSCRIPT:\n\n{transcript_text}"
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=full_prompt,
    )
    return response.text
