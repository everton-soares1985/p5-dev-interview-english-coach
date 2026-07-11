"""Tests for section parser and file writer (no Gemini API calls)."""
import pytest
from pathlib import Path

from src.writer import (
    FILE_NAMES,
    SECTION_KEYS,
    create_output_dir,
    parse_sections,
    write_outputs,
)

SAMPLE_RESPONSE = """
## TRANSCRIPT
Interviewer: Tell me about yourself.
Candidate: I am automation engineer and I working with Python and AI tools.
Interviewer: What projects have you built?
Candidate: I built automations for content and data process.

## ENGLISH_FEEDBACK
The candidate shows intermediate English with recurring grammar errors.
Estimated level: B1.
Top 3 improvement areas: articles, verb forms, vocabulary range.

## FLUENCY_SCORE
Overall: 5.5/10
Clarity: 6.0/10
Grammar: 4.0/10
Vocabulary: 5.0/10
Fluency: 6.0/10
Confidence: 6.0/10

## CORRECTED_ANSWERS
Original: I am automation engineer and I working with Python and AI tools.
Corrected: I am an automation engineer, and I work with Python and AI tools.
Error type: missing article (an), wrong verb form (working → work).

## IMPROVED_INTERVIEW_ANSWERS
Question: Tell me about yourself.
Improved: I am an AI and automation engineer with 3+ years of experience building
Python-based systems that automate repetitive workflows and improve team efficiency.

## VOCABULARY_TO_STUDY
| Word/Phrase | Example |
|---|---|
| automation workflows | I design automation workflows for data pipelines. |
| production-ready | The system is production-ready and fully tested. |

## GRAMMAR_PATTERNS
Pattern: Missing article before job title.
Example: "I am automation engineer" → "I am an automation engineer".
Rule: Use 'an' before singular countable nouns that describe a role.

## NEXT_PRACTICE_PLAN
Day 1: Practice the improved "Tell me about yourself" answer for 10 minutes.
Day 2: Study the vocabulary table — use each phrase in a new sentence.
Day 3: Record yourself answering the 3 weakest questions. Compare to improvements.
"""


def test_parse_sections_finds_all_keys():
    sections = parse_sections(SAMPLE_RESPONSE)
    for key in SECTION_KEYS:
        assert key in sections, f"Section '{key}' not found"


def test_parse_sections_content_not_empty():
    sections = parse_sections(SAMPLE_RESPONSE)
    for key, content in sections.items():
        assert content.strip(), f"Section '{key}' is empty"


def test_parse_sections_transcript_content():
    sections = parse_sections(SAMPLE_RESPONSE)
    assert "automation engineer" in sections["TRANSCRIPT"]


def test_parse_sections_empty_response_returns_empty_dict():
    assert parse_sections("") == {}


def test_parse_sections_partial_response():
    partial = "## TRANSCRIPT\nSome transcript.\n## ENGLISH_FEEDBACK\nSome feedback."
    sections = parse_sections(partial)
    assert "TRANSCRIPT" in sections
    assert "ENGLISH_FEEDBACK" in sections
    # Keys absent from response should not appear
    assert "GRAMMAR_PATTERNS" not in sections


def test_write_outputs_creates_all_files(tmp_path):
    sections = parse_sections(SAMPLE_RESPONSE)
    written, missing = write_outputs(sections, tmp_path, dry_run=False)

    assert len(missing) == 0, f"Unexpected missing sections: {missing}"
    for key in SECTION_KEYS:
        expected = tmp_path / FILE_NAMES[key]
        assert expected.exists(), f"File not created: {expected.name}"
        assert expected.stat().st_size > 0, f"File is empty: {expected.name}"


def test_write_outputs_dry_run_creates_no_files(tmp_path):
    sections = parse_sections(SAMPLE_RESPONSE)
    written, _ = write_outputs(sections, tmp_path, dry_run=True)
    assert len(written) == 0
    # tmp_path should be empty (dry-run never writes)
    assert not any(tmp_path.iterdir())


def test_write_outputs_missing_section_creates_placeholder(tmp_path):
    # Provide only one section
    sections = {"TRANSCRIPT": "Some transcript content."}
    written, missing = write_outputs(sections, tmp_path, dry_run=False)
    # All other sections should be flagged as missing
    assert len(missing) == len(SECTION_KEYS) - 1
    # transcript.md should still be written
    assert (tmp_path / "transcript.md").exists()


def test_create_output_dir_creates_folder(tmp_path):
    output_dir = create_output_dir(base_dir=tmp_path)
    assert output_dir.exists()
    assert output_dir.is_dir()
    # Name should be a timestamp pattern YYYYMMDD_HHMMSS
    assert len(output_dir.name) == 15
