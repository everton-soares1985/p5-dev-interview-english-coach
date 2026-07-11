"""
P5 — Dev Interview English Coach
CLI entrypoint. Accepts OBS .mp4 recordings or .txt transcripts and generates
structured English improvement reports using the Gemini multimodal API.

Usage:
    python src/main.py --video inputs/session.mp4
    python src/main.py --transcript examples/fake_interview_transcript.txt
    python src/main.py --video inputs/session.mp4 --dry-run
    python src/main.py --video inputs/session.mp4 --output-dir outputs/session_001
"""
import argparse
import sys
from pathlib import Path

# Force UTF-8 stdout/stderr on Windows console to prevent UnicodeEncodeError with rich symbols
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Ensure project root is in sys.path so running `python src/main.py` works directly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv
from rich.console import Console

load_dotenv(override=True)

from src import gemini_client
from src.analyzer import run_video_analysis, run_transcript_analysis
from src.writer import create_output_dir, parse_sections, print_summary, write_outputs

console = Console()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="p5-interview-coach",
        description=(
            "Dev Interview English Coach — "
            "Analyze OBS interview recordings with Gemini AI."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
examples:
  python src/main.py --video inputs/session.mp4
  python src/main.py --transcript examples/fake_interview_transcript.txt
  python src/main.py --video inputs/session.mp4 --dry-run
  python src/main.py --video inputs/session.mp4 --output-dir outputs/session_001
        """,
    )

    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "--video",
        type=Path,
        metavar="FILE",
        help=".mp4 interview recording from OBS Studio",
    )
    input_group.add_argument(
        "--transcript",
        type=Path,
        metavar="FILE",
        help=".txt interview transcript (fallback / demo mode)",
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        metavar="DIR",
        help="Custom output folder (default: outputs/YYYYMMDD_HHMMSS/)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview outputs in terminal without writing files",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    console.print("\n[bold cyan]🎙  P5 — Dev Interview English Coach[/bold cyan]")
    console.print("Powered by Gemini Multimodal AI\n")

    try:
        gemini_client.configure_client()

        if args.video:
            console.print(f"[dim]Input (video):[/dim] {args.video}")
            response_text = run_video_analysis(args.video)
        else:
            console.print(f"[dim]Input (transcript):[/dim] {args.transcript}")
            response_text = run_transcript_analysis(args.transcript)

        sections = parse_sections(response_text)

        if args.dry_run:
            console.print("\n[bold yellow]DRY-RUN — no files will be saved.[/bold yellow]")
            write_outputs(sections, Path("outputs/dry-run"), dry_run=True)
            found = list(sections.keys())
            missing = [k for k in ["TRANSCRIPT","ENGLISH_FEEDBACK","CORRECTED_ANSWERS",
                                    "IMPROVED_INTERVIEW_ANSWERS","VOCABULARY_TO_STUDY",
                                    "GRAMMAR_PATTERNS","NEXT_PRACTICE_PLAN"] if k not in found]
            if missing:
                console.print(f"\n[yellow]⚠ Missing sections: {missing}[/yellow]")
        else:
            output_dir = args.output_dir or create_output_dir()
            if args.output_dir:
                output_dir.mkdir(parents=True, exist_ok=True)
            written, missing = write_outputs(sections, output_dir)
            print_summary(written, missing, output_dir)

    except FileNotFoundError as exc:
        console.print(f"\n[red]File error: {exc}[/red]")
        sys.exit(1)
    except ValueError as exc:
        console.print(f"\n[red]Input error: {exc}[/red]")
        sys.exit(1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Cancelled.[/yellow]")
        sys.exit(0)


if __name__ == "__main__":
    main()
