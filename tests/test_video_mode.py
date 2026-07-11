"""Tests for video analysis mode — Gemini Files API fully mocked."""
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

from src.analyzer import SUPPORTED_VIDEO_EXTENSIONS, MAX_FILE_SIZE_MB


# ── Helpers ────────────────────────────────────────────────────────────────────

def _make_video_file(tmp_path: Path, name: str = "mock_interview.mp4", size_bytes: int = 1024) -> Path:
    """Create a small fake video file for testing."""
    video = tmp_path / name
    video.write_bytes(b"\x00" * size_bytes)
    return video


def _fake_uploaded_file(state_name: str = "ACTIVE") -> MagicMock:
    """Return a mock Gemini file object with the given state."""
    f = MagicMock()
    f.name = "files/abc123"
    f.uri = "https://generativelanguage.googleapis.com/files/abc123"
    f.state = MagicMock()
    f.state.name = state_name
    return f


FAKE_VIDEO_RESPONSE = """## TRANSCRIPT
Interviewer: Tell me about yourself.
Candidate: I am automation engineer working with Python and AI.

## ENGLISH_FEEDBACK
Candidate shows B1 level English with some grammar errors.

## FLUENCY_SCORE
Overall: 5.5/10
Clarity: 6/10
Grammar: 4/10
Vocabulary: 5/10
Fluency: 6/10
Confidence: 6/10

## CORRECTED_ANSWERS
Original: I am automation engineer working with Python and AI.
Corrected: I am an automation engineer working with Python and AI.

## IMPROVED_INTERVIEW_ANSWERS
I am an AI and automation engineer specializing in Python-based systems.

## VOCABULARY_TO_STUDY
- automation workflows
- production-ready systems

## GRAMMAR_PATTERNS
Pattern: Missing article before job title.

## NEXT_PRACTICE_PLAN
Day 1: Practice the corrected "Tell me about yourself" answer.
"""


# ── Validation tests ────────────────────────────────────────────────────────────

def test_video_missing_file_raises():
    from src.analyzer import run_video_analysis
    with pytest.raises(FileNotFoundError, match="not found"):
        run_video_analysis(Path("inputs/nonexistent.mp4"))


def test_video_unsupported_extension_raises(tmp_path):
    bad_file = tmp_path / "recording.txt"
    bad_file.write_bytes(b"fake content")
    from src.analyzer import run_video_analysis
    with pytest.raises(ValueError, match="Unsupported file type"):
        run_video_analysis(bad_file)


def test_video_supported_extensions_are_valid():
    """All declared extensions should be lowercase with leading dot."""
    for ext in SUPPORTED_VIDEO_EXTENSIONS:
        assert ext.startswith("."), f"Extension should start with dot: {ext}"
        assert ext == ext.lower(), f"Extension should be lowercase: {ext}"


def test_video_file_too_large_raises(tmp_path):
    large_file = tmp_path / "huge.mp4"
    large_file.write_bytes(b"\x00")
    size_bytes = int((MAX_FILE_SIZE_MB + 1) * 1024 * 1024)
    with patch.object(Path, "stat") as mock_stat:
        mock_stat.return_value = MagicMock(st_size=size_bytes)
        from src.analyzer import run_video_analysis
        with pytest.raises(ValueError, match="maximum allowed"):
            run_video_analysis(large_file)


# ── Upload + analysis pipeline tests ───────────────────────────────────────────

def test_video_analysis_calls_upload_and_generate(tmp_path):
    """Full video pipeline should call upload → wait → generate."""
    video = _make_video_file(tmp_path)
    active_file = _fake_uploaded_file("ACTIVE")

    with (
        patch("src.gemini_client.upload_video", return_value=active_file) as mock_upload,
        patch("src.gemini_client.wait_for_active", return_value=active_file) as mock_wait,
        patch("src.gemini_client.generate_from_video", return_value=FAKE_VIDEO_RESPONSE) as mock_gen,
    ):
        from src.analyzer import run_video_analysis
        result = run_video_analysis(video)

    mock_upload.assert_called_once_with(video)
    mock_wait.assert_called_once_with(active_file)
    mock_gen.assert_called_once()
    assert "TRANSCRIPT" in result


def test_video_analysis_raises_on_empty_gemini_response(tmp_path):
    """Empty Gemini response should raise a clear ValueError."""
    video = _make_video_file(tmp_path)
    active_file = _fake_uploaded_file("ACTIVE")

    with (
        patch("src.gemini_client.upload_video", return_value=active_file),
        patch("src.gemini_client.wait_for_active", return_value=active_file),
        patch("src.gemini_client.generate_from_video", return_value="   "),
    ):
        from src.analyzer import run_video_analysis
        with pytest.raises(ValueError, match="empty response"):
            run_video_analysis(video)


def test_video_full_pipeline_end_to_end(tmp_path):
    """End-to-end: video → parse → write 7 .md files."""
    from src.writer import parse_sections, write_outputs, SECTION_KEYS

    video = _make_video_file(tmp_path)
    output_dir = tmp_path / "outputs"
    output_dir.mkdir()
    active_file = _fake_uploaded_file("ACTIVE")

    with (
        patch("src.gemini_client.upload_video", return_value=active_file),
        patch("src.gemini_client.wait_for_active", return_value=active_file),
        patch("src.gemini_client.generate_from_video", return_value=FAKE_VIDEO_RESPONSE),
    ):
        from src.analyzer import run_video_analysis
        response = run_video_analysis(video)

    sections = parse_sections(response)
    written, missing = write_outputs(sections, output_dir)

    assert len(written) == len(SECTION_KEYS)
    assert len(missing) == 0
    for f in written:
        assert f.exists() and f.stat().st_size > 0
