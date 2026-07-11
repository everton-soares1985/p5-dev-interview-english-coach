"""Tests for transcript analysis mode — Gemini API fully mocked."""
import pytest
from pathlib import Path
from unittest.mock import patch

FAKE_TRANSCRIPT = """Interviewer: Tell me about yourself.
Candidate: I am automation engineer and I working with Python and AI tools.
Interviewer: What kind of projects have you built?
Candidate: I built automations for content and data process.
Interviewer: How do you handle errors in production?
Candidate: I use try except and I log the errors.
"""

FAKE_GEMINI_RESPONSE = """## TRANSCRIPT
Interviewer: Tell me about yourself.
Candidate: I am automation engineer and I working with Python and AI tools.

## ENGLISH_FEEDBACK
The candidate demonstrates a B1 level of English communication.

## FLUENCY_SCORE
Overall: 5.5/10
Clarity: 6/10
Grammar: 4/10
Vocabulary: 5/10
Fluency: 6/10
Confidence: 6/10

## CORRECTED_ANSWERS
Original: I am automation engineer and I working with Python and AI tools.
Corrected: I am an automation engineer, and I work with Python and AI tools.

## IMPROVED_INTERVIEW_ANSWERS
I am an AI and automation engineer specializing in Python-based solutions.

## VOCABULARY_TO_STUDY
- automation workflows
- AI-powered solutions
- production-ready systems

## GRAMMAR_PATTERNS
Pattern: Missing article before job title.
Example: "I am automation engineer" → "I am an automation engineer".

## NEXT_PRACTICE_PLAN
Day 1: Practice the corrected "Tell me about yourself" answer aloud.
Day 2: Study the vocabulary list and use each phrase in a sentence.
"""


def test_run_transcript_analysis_calls_gemini(tmp_path):
    """Transcript mode should call generate_from_transcript with the file content."""
    transcript_file = tmp_path / "test_transcript.txt"
    transcript_file.write_text(FAKE_TRANSCRIPT, encoding="utf-8")

    with patch(
        "src.gemini_client.generate_from_transcript",
        return_value=FAKE_GEMINI_RESPONSE,
    ) as mock_generate:
        from src.analyzer import run_transcript_analysis
        result = run_transcript_analysis(transcript_file)

    mock_generate.assert_called_once()
    # Verify the transcript content was passed
    call_args = mock_generate.call_args[0]
    assert "automation engineer" in call_args[0]  # transcript_text
    assert result == FAKE_GEMINI_RESPONSE


def test_run_transcript_analysis_raises_on_missing_file():
    from src.analyzer import run_transcript_analysis
    with pytest.raises(FileNotFoundError, match="not found"):
        run_transcript_analysis(Path("nonexistent/transcript.txt"))


def test_run_transcript_analysis_raises_on_empty_file(tmp_path):
    empty_file = tmp_path / "empty.txt"
    empty_file.write_text("   \n  ", encoding="utf-8")

    from src.analyzer import run_transcript_analysis
    with pytest.raises(ValueError, match="empty"):
        run_transcript_analysis(empty_file)


def test_run_transcript_analysis_full_pipeline(tmp_path):
    """End-to-end: transcript → parse → write files."""
    from src.writer import parse_sections, write_outputs, SECTION_KEYS

    transcript_file = tmp_path / "interview.txt"
    transcript_file.write_text(FAKE_TRANSCRIPT, encoding="utf-8")
    output_dir = tmp_path / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    with patch("src.gemini_client.generate_from_transcript", return_value=FAKE_GEMINI_RESPONSE):
        from src.analyzer import run_transcript_analysis
        response = run_transcript_analysis(transcript_file)

    sections = parse_sections(response)
    written, missing = write_outputs(sections, output_dir)

    assert len(missing) == 0, f"Missing sections: {missing}"
    assert len(written) == len(SECTION_KEYS)
    for file_path in written:
        assert file_path.exists()
        assert file_path.stat().st_size > 0
