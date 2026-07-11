# SPEC — P5: Dev Interview English Coach
> **Architect:** GPT Architect B
> **Builder:** Antigravity
> **Created:** 10 July 2026
> **Status:** APPROVED — Ready to build ✅
> **Architecture:** Gemini multimodal video review + transcript fallback

---

## 1. Problem

Everton practices English job interviews using the Wellfound AI Interview feature and records
the sessions with OBS Studio. After each session, the recording exists but the feedback
disappears. Mistakes are not tracked, weak answers are not corrected, and there is no
structured improvement plan for the next session.

This tool receives the OBS `.mp4` recording of a Wellfound interview practice session,
sends it to Gemini multimodal API, and generates a structured English improvement package
as Markdown files. The user studies the reports, practices again, and repeats.

---

## 2. Target User

**Primary:** Everton Soares — AI & Automation Engineer in Brazil preparing for remote
USD/EUR job interviews. Practices on Wellfound AI Interview, records with OBS Studio.

**Secondary (after open-sourcing):** Any non-native English speaking developer preparing
for remote technical job interviews.

---

## 3. Expected Result

A CLI Python tool that:
1. Receives an OBS `.mp4` recording of an English interview practice session
2. Uploads the video to the Gemini Files API
3. Analyzes audio and visible screen context using Gemini multimodal
4. Generates 7 structured Markdown improvement reports
5. Saves them to a timestamped output folder

The user's feedback loop becomes:

```
Practice interview on Wellfound
↓
OBS records the session → session.mp4
↓
python src/main.py --video inputs/session.mp4
↓
7 improvement reports generated
↓
User studies reports and practices again
```

---

## 4. Minimum Scope — V1 Only

V1 must do exactly this — nothing more:

1. Accept `.mp4` video file as primary input via `--video` flag
2. Accept `.txt` transcript as fallback input via `--transcript` flag
3. Upload `.mp4` to Gemini Files API (if video mode)
4. Wait for file processing status to be `ACTIVE`
5. Send file reference + structured prompt to Gemini
6. Parse the 7 output sections from Gemini response
7. Write each section to a separate `.md` file
8. Save all outputs to `outputs/YYYYMMDD_HHMMSS/`
9. Print a summary table to the terminal using `rich`
10. Support `--dry-run` flag (prints outputs without saving files)

---

## 5. Out of Scope — V1

Do NOT build any of this in V1:

```
Direct OBS integration (starting/stopping recording)
Automatic speech-to-text with FFmpeg or Whisper
Pronunciation scoring or accent analysis
Facial or emotion analysis
Progress dashboard or history tracking
Database or SQLite storage
Automatic LinkedIn or YouTube posting
GitHub Actions or automation
Wellfound browser automation
Real interview storage or replay
Camera or video editing
Vertical video cropping
```

---

## 6. Input

### Primary input — Video mode

```bash
python src/main.py --video inputs/mock_interview.mp4
```

- `.mp4` file recorded by OBS Studio
- Maximum file size recommendation: 500 MB (Gemini Files API supports up to 2 GB,
  but we enforce 500 MB locally for reliability)
- Typical Wellfound AI interview: 10–25 minutes — fits comfortably

### Fallback input — Transcript mode

```bash
python src/main.py --transcript examples/fake_interview_transcript.txt
```

- Plain `.txt` file with interview dialogue
- Used for testing, demo, and debugging without real video
- Required for public GitHub examples

### Example transcript format

```txt
Interviewer: Tell me about yourself.
Candidate: I am automation engineer and I working with Python and AI tools.
Interviewer: What kind of projects have you built?
Candidate: I built automations for content and data process.
Interviewer: How do you handle errors in production?
Candidate: I use try except and I log the errors.
```

---

## 7. Output Files

All files saved to `outputs/YYYYMMDD_HHMMSS/`:

| File | Purpose |
| :--- | :--- |
| `transcript.md` | Full transcript of candidate answers with timestamps if available |
| `english_feedback.md` | General English level review: clarity, fluency, grammar, confidence |
| `corrected_answers.md` | Original answers rewritten with correct English |
| `improved_interview_answers.md` | Professional-level rewrites for remote tech interviews |
| `vocabulary_to_study.md` | Key words and phrases to learn, with example sentences |
| `grammar_patterns.md` | Recurring grammar mistakes with simple explanations |
| `next_practice_plan.md` | Short study plan and exercises for the next session |

### What each file contains

#### `transcript.md`
Generated transcript of candidate's spoken answers. Gemini extracts this from the audio.
Include timestamps when possible. Marks unclear speech with `[unclear]`.

#### `english_feedback.md`
Overall evaluation:
- Clarity of communication
- Fluency and natural flow
- Grammar accuracy
- Vocabulary range
- Confidence and structure
- Main improvement areas (top 3)
- Estimated English level (A2 / B1 / B2 / C1)

#### `corrected_answers.md`
Side-by-side correction of each answer:
```
Original:
I am automation engineer and I working with Python.

Corrected:
I am an automation engineer, and I work with Python.

Error type: missing article (an), wrong verb form (working → work)
```

#### `improved_interview_answers.md`
Professional rewrites suitable for remote USD/EUR interviews:
```
Question: Tell me about yourself.

Improved answer:
I am an AI and automation engineer with experience building Python-based systems
that automate repetitive workflows and improve operational efficiency. I focus on
production-ready solutions and clean, maintainable code.
```

#### `vocabulary_to_study.md`
Words and phrases detected as weak or missing:
```
| Word/Phrase | Example in context |
| automation workflows | "I design automation workflows for data pipelines." |
| production-ready | "The system is production-ready and fully tested." |
| technical ownership | "I take technical ownership of the full stack." |
```

#### `grammar_patterns.md`
Recurring patterns and how to fix them:
```
Pattern: Missing articles (a / an / the)
Example: "I am automation engineer" → "I am an automation engineer"
Rule: Use "an" before words starting with a vowel sound.

Pattern: Wrong verb form after subject
Example: "I working with Python" → "I work with Python"
Rule: Simple present tense does not use -ing form without "am/is/are".
```

#### `next_practice_plan.md`
Short study plan for the next 3–5 days:
```
Day 1: Practice the "Tell me about yourself" answer using the improved version.
Day 2: Study the 10 vocabulary words from vocabulary_to_study.md.
Day 3: Record yourself answering the 3 weakest questions. Compare to improved versions.
Day 4: Practice grammar patterns. Focus on articles and verb forms.
Day 5: Redo the full Wellfound interview. Record with OBS. Run P5 again.
```

---

## 8. Gemini Prompt Design

The prompt must instruct Gemini to:
1. Focus ONLY on English language quality
2. NOT capture personal data, account names, emails, or private UI content
3. Return clearly separated sections for each output file

### Video mode prompt (stored in `src/prompts/video_review_prompt.txt`)

```
You are an English interview coach for software developers.

Analyze this video recording of an English job interview practice session.

Focus ONLY on:
- The candidate's spoken English (audio)
- Grammar accuracy
- Vocabulary range and appropriateness
- Clarity and fluency of communication
- Answer structure for technical job interviews
- Specific improvements for remote international interviews

Do NOT include:
- Private UI content visible on screen
- Account names, email addresses, or profile information
- URLs or platform-specific data
- Any information not related to English language quality

Return your analysis in the following sections, each clearly labeled:

## TRANSCRIPT
(full transcript of candidate answers)

## ENGLISH_FEEDBACK
(general English level review)

## CORRECTED_ANSWERS
(original answers with corrections shown)

## IMPROVED_INTERVIEW_ANSWERS
(professional rewrites)

## VOCABULARY_TO_STUDY
(key words and phrases to learn)

## GRAMMAR_PATTERNS
(recurring mistakes and rules)

## NEXT_PRACTICE_PLAN
(study plan for next session)
```

### Transcript mode prompt (stored in `src/prompts/transcript_review_prompt.txt`)

Same structure but starts with:
```
You are an English interview coach for software developers.

Analyze this text transcript of an English job interview practice session.
[same instructions]
```

---

## 9. Folder Structure

```
p5-dev-interview-english-coach/
├── README.md                          ← English, public-ready
├── SPEC.md                            ← This file
├── .env.example                       ← GEMINI_API_KEY=your_key_here
├── requirements.txt                   ← google-generativeai, rich, python-dotenv
├── .gitignore                         ← inputs/, outputs/, .env, __pycache__
├── src/
│   ├── main.py                        ← CLI entrypoint (argparse)
│   ├── analyzer.py                    ← Gemini API calls (video + transcript modes)
│   ├── writer.py                      ← Parses sections + writes .md files
│   ├── gemini_client.py               ← File upload, polling, API calls
│   └── prompts/
│       ├── video_review_prompt.txt    ← Main prompt for .mp4 input
│       └── transcript_review_prompt.txt ← Fallback prompt for .txt input
├── inputs/
│   └── .gitkeep                       ← gitignored — real videos go here
├── outputs/
│   └── .gitkeep                       ← gitignored — generated reports go here
├── examples/
│   ├── fake_interview_transcript.txt  ← Fictional demo input
│   └── fake_output/                   ← Fictional demo outputs (7 .md files)
├── tests/
│   ├── test_writer.py                 ← Tests for section parser + file writer
│   └── test_transcript_mode.py        ← Tests for transcript mode (mocked API)
└── docs/
    └── screenshot.png                 ← CLI screenshot for README
```

---

## 10. Tech Stack

```
Python 3.11+
google-generativeai >= 0.7.0   # Gemini API + Files API (video upload)
python-dotenv                   # .env loading
rich                            # Terminal output table
pytest                          # Tests
```

No FFmpeg. No Whisper. No extra dependencies in V1.

---

## 11. CLI Design

```bash
# Video mode (primary)
python src/main.py --video inputs/mock_interview.mp4

# Transcript fallback
python src/main.py --transcript examples/fake_interview_transcript.txt

# Dry run (no files saved, prints to terminal only)
python src/main.py --video inputs/mock_interview.mp4 --dry-run

# Custom output directory
python src/main.py --video inputs/mock_interview.mp4 --output-dir outputs/session_001

# Help
python src/main.py --help
```

---

## 12. Security Rules (Non-Negotiable)

```
No API keys in code — .env only
No real interview recordings in the repository
inputs/ must be in .gitignore
outputs/ must be in .gitignore
All examples must be fictional
No Wellfound account data, screenshots, or session logs
No real names or email addresses in examples
Mocked Gemini API calls in all tests
README must include a privacy warning
```

---

## 13. Error Handling Requirements

| Failure case | Required behavior |
| :--- | :--- |
| File not found | Clear error message, exit with code 1 |
| File too large (> 500 MB) | Warn user, suggest compressing video, exit |
| Gemini upload fails | Retry once, then exit with error message |
| Gemini processing timeout | Wait max 120 seconds, then exit with message |
| Gemini response is empty | Save what exists, warn about missing sections |
| API key missing | Clear message: "Set GEMINI_API_KEY in your .env file" |

---

## 14. Completion Criteria

P5 is DONE only when ALL of the following are true:

- [ ] `python src/main.py --video` runs without errors on a real `.mp4` file
- [ ] `python src/main.py --transcript` runs without errors on a `.txt` file
- [ ] All 7 Markdown output files are generated correctly
- [ ] Outputs are saved to a correctly named timestamped folder
- [ ] `--dry-run` flag works (prints without saving)
- [ ] `README.md` written in English with usage instructions and privacy warning
- [ ] `examples/fake_interview_transcript.txt` exists with fictional dialogue
- [ ] `examples/fake_output/` contains all 7 fictional `.md` output examples
- [ ] `.env.example` exists with placeholder key only
- [ ] `inputs/` and `outputs/` are in `.gitignore`
- [ ] `pytest tests/` passes with 0 failures (all API calls mocked)
- [ ] `docs/screenshot.png` exists showing CLI running
- [ ] GitHub repository is public
- [ ] Commit history uses Conventional Commits in English
- [ ] LinkedIn post OR YouTube script about the project exists

---

## 15. Build Order

### Phase 1 — Foundation (Day 1)
```
.gitignore
.env.example
requirements.txt
src/gemini_client.py (upload + polling + call)
src/prompts/transcript_review_prompt.txt
src/analyzer.py (transcript mode only)
src/writer.py (section parser + file writer)
src/main.py (--transcript flag only)
tests/test_writer.py
tests/test_transcript_mode.py
```

### Phase 2 — Video Mode (Day 2)
```
src/prompts/video_review_prompt.txt
src/analyzer.py (add video mode)
src/main.py (add --video flag)
error handling (file size, upload timeout, empty response)
```

### Phase 3 — Polish & Demo (Day 3)
```
examples/fake_interview_transcript.txt
examples/fake_output/ (7 fictional .md files)
README.md
docs/screenshot.png
final pytest run
LinkedIn post text
git push → public GitHub
```
