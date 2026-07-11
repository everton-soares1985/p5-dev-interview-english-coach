# 🎙️ P5 — Dev Interview English Coach

![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-blue?style=for-the-badge&logo=python)
![Gemini Multimodal](https://img.shields.io/badge/Gemini_2.5-Multimodal_AI-8E75B2?style=for-the-badge&logo=google)
![Tests](https://img.shields.io/badge/Tests-20%2F20_Passed-00C853?style=for-the-badge)
![License MIT](https://img.shields.io/badge/License-MIT-gray?style=for-the-badge)

> **An AI-powered, multimodal English interview coach designed specifically for software engineers and engineering managers targeting remote international USD/EUR job opportunities.**

Upload your mock interview practice session (`.mp4`, `.mkv`, `.mov`) directly from **OBS Studio**, and receive **8 structured, highly visual Markdown reports** evaluating your spoken English, technical clarity, STAR-method structuring, and domain vocabulary.

---

## ⚡ Architecture & Workflow

```
[ OBS Studio .mp4 / .mkv ]
           │
           ▼
[ Gemini Files API Upload ] ──(Polling until ACTIVE)──┐
                                                      ▼
[ Multimodal Video & Audio Analysis ] ──► [ google-genai SDK (`gemini-2.5-flash`) ]
                                                      │
           ┌──────────────────────────────────────────┘
           ▼
[ Markdown Parser & Writer ]
           │
           ├─► transcript.md
           ├─► english_feedback.md
           ├─► fluency_score.md
           ├─► corrected_answers.md
           ├─► improved_interview_answers.md
           ├─► vocabulary_to_study.md
           ├─► grammar_patterns.md
           └─► next_practice_plan.md
```

---

## 🔒 Privacy & Security First

> [!CAUTION]
> **Your data stays strictly private.**
> * Interview video recordings (`inputs/`) and generated feedback reports (`outputs/`) are **gitignored by default** and are **never committed or uploaded to GitHub**.
> * The tool connects directly to your personal Google Gemini API endpoint using the `google-genai` SDK.
> * No intermediate servers, no databases, and no third-party tracking.

---

## 📑 Generated Reports Overview

Every analysis session automatically generates **8 Markdown files** formatted with clean tables, badges, blockquotes, and interactive checklists:

| Report File | Description | Check Demo |
| :--- | :--- | :---: |
| **`transcript.md`** | Clean dialogue transcript with clear speaker turns and timestamps. | [View Demo](examples/fake_output/transcript.md) |
| **`english_feedback.md`** | Proficiency estimation (`A2/B1/B2/C1`) and 5-dimension assessment table. | [View Demo](examples/fake_output/english_feedback.md) |
| **`fluency_score.md`** | Numerical breakdown on a 0–10 scale across Clarity, Fluency, and Grammar. | [View Demo](examples/fake_output/fluency_score.md) |
| **`corrected_answers.md`** | Side-by-side `Original vs. Corrected` grammatical rewrites with rules. | [View Demo](examples/fake_output/corrected_answers.md) |
| **`improved_interview_answers.md`** | Executive `C1/Native` STAR-method rewrites of your interview answers. | [View Demo](examples/fake_output/improved_interview_answers.md) |
| **`vocabulary_to_study.md`** | Curated table of domain-specific software engineering vocabulary. | [View Demo](examples/fake_output/vocabulary_to_study.md) |
| **`grammar_patterns.md`** | Deep-dive explanations into your recurring grammatical habits and fixes. | [View Demo](examples/fake_output/grammar_patterns.md) |
| **`next_practice_plan.md`** | Actionable 5-day daily study plan with interactive Markdown checkboxes. | [View Demo](examples/fake_output/next_practice_plan.md) |

*(Note: All files inside `examples/fake_output/` use fictional demo candidate "Alex Chen" and do not contain real interview data).*

---

## 🚀 Quickstart & Installation

### 1. Clone & Setup Virtual Environment
```bash
git clone https://github.com/everton-soares1985/p5-dev-interview-english-coach.git
cd p5-dev-interview-english-coach

python -m venv .venv
# On Windows PowerShell:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Configure Gemini API Key (100% Free Tier)
1. Get your free API key from [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
3. Add your key inside `.env`:
   ```env
   GEMINI_API_KEY=AIzaSy...your_api_key_here
   ```

---

## 💻 Usage

### Video Analysis Mode (`--video`)
Analyze an `.mp4`, `.mkv`, `.mov`, `.webm`, or `.avi` recording directly:
```bash
python src/main.py --video inputs/my_obs_recording.mkv
```
*Supports video files up to **1 GB** (Soft warning displayed above 300 MB).*

### Transcript Fallback Mode (`--transcript`)
Analyze a plain text `interview.txt` file if no video recording is available:
```bash
python src/main.py --transcript examples/fake_interview_transcript.txt
```

### Dry-Run Preview (`--dry-run`)
Preview the generated feedback directly in your terminal without saving files to disk:
```bash
python src/main.py --transcript examples/fake_interview_transcript.txt --dry-run
```

### Custom Output Directory (`--output-dir`)
Specify a custom folder path for your generated reports:
```bash
python src/main.py --video inputs/my_obs_recording.mkv --output-dir outputs/my_custom_session
```

---

## 🧪 Testing

The codebase includes an extensive unit test suite using `pytest` and `pytest-mock` to verify the section parser, file writer, and API pipeline without consuming API tokens or network bandwidth:

```bash
pytest tests/ -v
```

```
============================= test session starts =============================
tests/test_transcript_mode.py::test_run_transcript_analysis_calls_gemini PASSED
tests/test_transcript_mode.py::test_run_transcript_analysis_full_pipeline PASSED
tests/test_video_mode.py::test_video_analysis_calls_upload_and_generate PASSED
tests/test_video_mode.py::test_video_full_pipeline_end_to_end PASSED
tests/test_writer.py::test_parse_sections_finds_all_keys PASSED
...
============================= 20 passed in 1.12s ==============================
```

---

## 🗺️ Roadmap & Project Status

| Phase | Description | Status |
| :--- | :--- | :---: |
| **Phase 1** | CLI Foundation, Markdown Parser, API Wrapper & Transcript Mode | ✅ Completed |
| **Phase 2** | Gemini Files API Video Upload, Polling & Multimodal Video Mode | ✅ Completed |
| **Phase 3** | Rich Visual Markdown Polish, Fluency Score & GitHub Public Release | ✅ Completed |
| **Phase 4.1** | Session Comparison Mode (`--compare`) to track longitudinal growth | ⏳ Planned |
| **Phase 4.2** | Session History Management (`session_history.json` & Rich CLI table) | ⏳ Planned |
| **Phase 4.3** | High-fidelity PDF Export (`--export-pdf`) via ReportLab/FPDF2 | ⏳ Planned |

---

## 📝 License & Author

Built with ❤️ for remote engineering excellence. Licensed under the **MIT License**.
See [ROADMAP.md](ROADMAP.md) and [SPEC.md](SPEC.md) for full architectural guidelines and continuity notes.
