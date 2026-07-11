# SPEC — P5: Dev Interview English Coach

> Architect: GEMS
> Builder: Antigravity
> Status: Draft — Not approved for build
> Created: 09 July 2026

## 1. Problem

Everton is studying English and preparing for remote USD/EUR job interviews. He can practice interviews using AI tools and record sessions with OBS Studio, but the practice does not automatically become structured learning. Mistakes disappear, weak answers are not tracked, and there is no clear improvement plan.

This project transforms interview transcripts into actionable English improvement reports.

## 2. Target User

Primary: Everton Soares — AI & Automation Engineer in Brazil preparing for remote international interviews.

Secondary: Developers and technical professionals who are non-native English speakers and want to improve interview communication.

## 3. Expected Result

A CLI Python tool that receives a text transcript of an English interview practice session and generates a structured improvement package as Markdown files.

## 4. Minimum Scope — V1 Only

V1 must do exactly this:

1. Accept a `.txt` interview transcript as input
2. Send the transcript to an AI model with structured prompts
3. Generate Markdown reports
4. Save results to `outputs/[timestamp]/`
5. Print a terminal summary
6. Include fictional examples only
7. Include tests with mocked AI calls

## 5. Out of Scope — V1

* No direct OBS integration
* No video upload
* No audio processing
* No FFmpeg in V1
* No automatic speech-to-text
* No pronunciation scoring
* No facial/emotion analysis
* No dashboard
* No database
* No real interview data
* No automatic posting to LinkedIn, YouTube, or GitHub

## 6. Input Data

Input is a `.txt` transcript.

Example:

```txt
Interviewer: Tell me about yourself.
Candidate: I am automation engineer and I working with Python and AI tools.
Interviewer: What kind of projects have you built?
Candidate: I built automations for content and data process.
```

All examples must be fictional.

## 7. Output Files

Generated inside `outputs/YYYYMMDD_HHMMSS/`:

```txt
english_feedback.md
corrected_transcript.md
improved_interview_answers.md
vocabulary_to_study.md
grammar_patterns.md
next_practice_plan.md
```

### english_feedback.md

General review of the candidate's English level, clarity, confidence, and main improvement areas.

### corrected_transcript.md

Original transcript with corrected grammar and sentence structure.

### improved_interview_answers.md

Professional versions of weak answers, rewritten for remote technical interviews.

### vocabulary_to_study.md

Useful vocabulary, repeated words, stronger alternatives, and example sentences.

### grammar_patterns.md

Recurring grammar mistakes and simple explanations.

### next_practice_plan.md

Small study plan with exercises for the next practice session.

## 8. Suggested Folder Structure

```txt
p5-dev-interview-english-coach/
├── README.md
├── .env.example
├── requirements.txt
├── SPEC_DRAFT.md
├── src/
│   ├── main.py
│   ├── analyzer.py
│   ├── writer.py
│   └── prompts/
│       ├── english_feedback.txt
│       ├── corrected_transcript.txt
│       ├── improved_answers.txt
│       ├── vocabulary.txt
│       ├── grammar_patterns.txt
│       └── practice_plan.txt
├── examples/
│   ├── fake_interview_transcript.txt
│   └── fake_output/
├── outputs/
│   └── .gitkeep
├── tests/
│   ├── test_analyzer.py
│   └── test_writer.py
└── docs/
    └── screenshot.png
```

## 9. Security Checklist

* [ ] No API keys in code
* [ ] `.env.example` with placeholder values only
* [ ] No real interview transcripts
* [ ] No Wellfound account screenshots
* [ ] No real recordings
* [ ] No personal/client data
* [ ] Fictional examples only
* [ ] Mocked AI calls in tests
* [ ] `outputs/` must be gitignored
* [ ] README must include responsible use disclaimer

## 10. Tech Stack

```txt
Python 3.11+
google-generativeai or openai
python-dotenv
rich
pytest
```

## 11. Target CLI Usage

```bash
python src/main.py --input examples/fake_interview_transcript.txt
python src/main.py --dry-run
python src/main.py --output-dir outputs/my_session
```

## 12. Completion Criteria

P5 is DONE only when all criteria are complete:

* [ ] CLI runs without errors
* [ ] `.txt` transcript input works
* [ ] All 6 Markdown output files are generated
* [ ] Outputs are saved to timestamped folder
* [ ] README is written in English
* [ ] Fictional example transcript exists
* [ ] Fictional output example exists
* [ ] `.env.example` exists
* [ ] Tests pass with mocked AI calls
* [ ] Screenshot or short demo video exists
* [ ] GitHub repository is public when safe
* [ ] LinkedIn post or YouTube script is created
* [ ] Commit history uses Conventional Commits

## 13. Anti-Scope Check

Is this scope achievable in 1-2 weeks working in focused sessions?
If not, cut anything related to V2, audio, video, OBS, pronunciation, or dashboards.

## 14. Approval Status

This SPEC is a draft only.

Do not implement until Everton explicitly approves it.
