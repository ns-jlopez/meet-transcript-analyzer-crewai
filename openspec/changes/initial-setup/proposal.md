# Proposal: Meet Transcript Analyzer with CrewAI

## Summary

Build a CrewAI-based automation that analyzes Google Meet transcript files for language improvement. The system fetches the latest transcript from a Google Drive folder ("Meet Recordings"), runs it through two specialized AI agents powered by Google Gemini, and produces a consolidated Markdown report with actionable feedback.

## Motivation

Reviewing meeting transcripts manually for language improvement is tedious. This automation provides structured, expert-level feedback on both spoken patterns (filler words, cadence, pronunciation cues) and written grammar (syntax, sentence structure) — turning every meeting into a learning opportunity.

## Architecture

```
Google Drive ("Meet Recordings")
        │
        ▼
┌─────────────────────┐
│  Google Drive Tool   │  ← Fetches latest .txt file
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│  Agent 1: Speech &  │  ← Analyzes filler words, cadence,
│  Pronunciation Coach│     phonetic patterns
└─────────────────────┘
        │ (sequential)
        ▼
┌─────────────────────┐
│  Agent 2: English   │  ← Analyzes sentence structure,
│  Grammarian         │     syntax, word choice
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│  Final Markdown     │  ← Combined report with both
│  Report             │     agents' findings
└─────────────────────┘
```

## Technical Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Framework | CrewAI | Multi-agent orchestration with built-in sequential process support |
| LLM | Google Gemini (`gemini-2.5-flash` or `gemini-3.5-flash`) via `google-genai` SDK | Cost-effective, fast, good at language analysis |
| Google Drive access | Official `google-genai` SDK / Google Drive API | Direct access to Drive files with OAuth2 |
| Process type | Sequential | Agent 2 benefits from Agent 1's context about speech patterns |
| Output format | Markdown | Easy to read, version-controllable, shareable |
| Python version | 3.13+ | Latest stable, matches existing dev environment |
| Package manager | `uv` or `pip` with `pyproject.toml` | Modern Python packaging |

## Components

### 1. Google Drive Tool (`tools/google_drive.py`)

A custom CrewAI tool that:
- Authenticates via OAuth2 (service account or user credentials)
- Lists files in the "Meet Recordings" folder
- Finds the most recent `.txt` file by modified date
- Downloads and returns the transcript content

### 2. Speech & Pronunciation Coach Agent

**Role:** Analyze spoken language patterns from the transcript.

**Focus areas:**
- Filler words (um, uh, like, you know, so, basically)
- Sentence cadence and rhythm (run-on speech, abrupt stops)
- Phonetic error indicators (commonly confused words, mispronunciation markers in auto-transcription)
- Repetitive phrases or verbal tics
- Speaking confidence indicators

### 3. Professional English Grammarian Agent

**Role:** Analyze grammar and syntax quality from the transcript.

**Focus areas:**
- Sentence structure (fragments, run-ons, dangling modifiers)
- Subject-verb agreement
- Tense consistency
- Word choice and vocabulary level
- Clarity and conciseness suggestions

### 4. Sequential Crew Process

- Agent 1 runs first, produces speech analysis
- Agent 2 runs second with access to Agent 1's output for context
- Final output is a combined Markdown report

## Project Structure

```
meet-transcript-analyzer-crewai/
├── pyproject.toml
├── .env.example
├── .gitignore
├── README.md
├── src/
│   └── meet_analyzer/
│       ├── __init__.py
│       ├── crew.py          # Crew definition
│       ├── agents.py        # Agent definitions
│       ├── tasks.py         # Task definitions
│       └── tools/
│           ├── __init__.py
│           └── google_drive.py  # Custom Drive tool
├── config/
│   ├── agents.yaml          # Agent configs (CrewAI convention)
│   └── tasks.yaml           # Task configs (CrewAI convention)
└── output/                  # Generated reports (gitignored)
```

## Configuration

Required environment variables:
- `GOOGLE_API_KEY` — Gemini API key
- `GOOGLE_DRIVE_CREDENTIALS_PATH` — Path to OAuth2 credentials JSON
- `GOOGLE_DRIVE_FOLDER_NAME` — Target folder name (default: "Meet Recordings")

## Out of Scope

- Real-time meeting analysis (this processes after-the-fact transcripts)
- Audio file processing (text transcripts only)
- Multi-language support (English only for v1)
- Web UI or dashboard
- Scheduling/cron automation (manual trigger for v1)

## Success Criteria

1. Running `python -m meet_analyzer` fetches the latest transcript and produces a Markdown report
2. Both agents provide distinct, non-overlapping feedback
3. The final report is well-structured with clear sections for each analysis domain
4. The system handles missing credentials gracefully with clear error messages
