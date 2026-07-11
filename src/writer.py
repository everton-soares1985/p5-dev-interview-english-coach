"""
Section parser and Markdown file writer for P5 outputs.
Parses Gemini's structured response into 7 named sections and writes .md files.
"""
import re
from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.table import Table

console = Console()

SECTION_KEYS = [
    "TRANSCRIPT",
    "ENGLISH_FEEDBACK",
    "FLUENCY_SCORE",
    "CORRECTED_ANSWERS",
    "IMPROVED_INTERVIEW_ANSWERS",
    "VOCABULARY_TO_STUDY",
    "GRAMMAR_PATTERNS",
    "NEXT_PRACTICE_PLAN",
]

FILE_NAMES = {
    "TRANSCRIPT": "transcript.md",
    "ENGLISH_FEEDBACK": "english_feedback.md",
    "FLUENCY_SCORE": "fluency_score.md",
    "CORRECTED_ANSWERS": "corrected_answers.md",
    "IMPROVED_INTERVIEW_ANSWERS": "improved_interview_answers.md",
    "VOCABULARY_TO_STUDY": "vocabulary_to_study.md",
    "GRAMMAR_PATTERNS": "grammar_patterns.md",
    "NEXT_PRACTICE_PLAN": "next_practice_plan.md",
}


def parse_sections(response_text: str) -> dict:
    """
    Split Gemini's response into a dict keyed by section name.
    Expects sections prefixed with ## SECTION_KEY (as instructed in the prompts).
    """
    if not response_text.strip():
        return {}

    pattern = r"##\s+(" + "|".join(SECTION_KEYS) + r")\b"
    parts = re.split(pattern, response_text)

    sections = {}
    i = 1
    while i < len(parts) - 1:
        key = parts[i].strip()
        content = parts[i + 1].strip() if i + 1 < len(parts) else ""
        if key in SECTION_KEYS:
            sections[key] = content
        i += 2

    return sections


def create_output_dir(base_dir: Path = Path("outputs")) -> Path:
    """Create and return a timestamped output directory."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = base_dir / timestamp
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def write_outputs(
    sections: dict, output_dir: Path, dry_run: bool = False
) -> tuple[list, list]:
    """
    Write each parsed section to its .md file.
    Returns (written_paths, missing_keys).
    In dry-run mode, prints previews to terminal instead of writing files.
    """
    written = []
    missing = []

    for key in SECTION_KEYS:
        filename = FILE_NAMES[key]
        content = sections.get(key, "")

        if not content:
            missing.append(filename)
            content = "*No content generated for this section.*\n"

        if dry_run:
            console.print(f"\n[bold yellow]── {filename} (dry-run preview) ──[/bold yellow]")
            preview = content[:400] + ("…" if len(content) > 400 else "")
            console.print(preview)
        else:
            file_path = output_dir / filename
            file_path.write_text(content, encoding="utf-8")
            written.append(file_path)

    return written, missing


def print_summary(written: list, missing: list, output_dir: Path) -> None:
    """Print a rich table summarising generated files."""
    table = Table(
        title="\n✅  P5 — Interview English Coach — Output Summary",
        show_header=True,
        header_style="bold cyan",
    )
    table.add_column("File", style="white")
    table.add_column("Status", justify="right")

    for file_path in written:
        size = file_path.stat().st_size
        table.add_row(file_path.name, f"[green]✓  {size:,} bytes[/green]")

    for filename in missing:
        table.add_row(filename, "[yellow]⚠  empty[/yellow]")

    console.print(table)
    console.print(f"\n[bold green]Saved to → {output_dir.resolve()}[/bold green]\n")
