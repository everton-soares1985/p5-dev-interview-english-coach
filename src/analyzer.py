"""
Analyzer module for P5 Dev Interview English Coach.
Orchestrates video and transcript analysis via the Gemini client.
"""
from pathlib import Path

from src import gemini_client

MAX_FILE_SIZE_MB = 1024          # Hard limit — Gemini Files API supports up to 2 GB
WARN_FILE_SIZE_MB = 300          # Soft warning — uploads above this may be slow
SUPPORTED_VIDEO_EXTENSIONS = {".mp4", ".mov", ".mkv", ".webm", ".avi"}


def _load_prompt(prompt_filename: str) -> str:
    """Load a prompt template from the prompts directory."""
    prompt_path = Path("src/prompts") / prompt_filename
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
    return prompt_path.read_text(encoding="utf-8")


def _validate_video(video_path: Path) -> None:
    """Ensure video file exists, has a supported extension, and is within size limit."""
    if not video_path.exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")

    ext = video_path.suffix.lower()
    if ext not in SUPPORTED_VIDEO_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type: '{ext}'. "
            f"Supported formats: {', '.join(sorted(SUPPORTED_VIDEO_EXTENSIONS))}"
        )

    size_mb = video_path.stat().st_size / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        raise ValueError(
            f"Video is {size_mb:.0f} MB — maximum allowed is {MAX_FILE_SIZE_MB} MB "
            "(Gemini Files API limit is 2 GB).\n"
            "Tip: Trim the OBS recording to the interview section only before running."
        )
    if size_mb > WARN_FILE_SIZE_MB:
        console.print(
            f"[yellow]⚠ File is {size_mb:.0f} MB. Upload may take a moment — "
            "this is normal for longer recordings.[/yellow]"
        )


def run_video_analysis(video_path: Path) -> str:
    """Upload .mp4 to Gemini Files API and return the raw text response."""
    _validate_video(video_path)
    prompt = _load_prompt("video_review_prompt.txt")
    uploaded = gemini_client.upload_video(video_path)
    active = gemini_client.wait_for_active(uploaded)
    response = gemini_client.generate_from_video(active, prompt)
    if not response or not response.strip():
        raise ValueError(
            "Gemini returned an empty response for the video. "
            "Try trimming the video or re-running the analysis."
        )
    return response


def run_transcript_analysis(transcript_path: Path) -> str:
    """Read .txt transcript and return the raw text response from Gemini."""
    if not transcript_path.exists():
        raise FileNotFoundError(f"Transcript file not found: {transcript_path}")
    text = transcript_path.read_text(encoding="utf-8")
    if not text.strip():
        raise ValueError("Transcript file is empty.")
    prompt = _load_prompt("transcript_review_prompt.txt")
    response = gemini_client.generate_from_transcript(text, prompt)
    if not response or not response.strip():
        raise ValueError(
            "Gemini returned an empty response for the transcript. "
            "Check your API key and try again."
        )
    return response
