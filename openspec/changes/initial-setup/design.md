## Context

New project. No existing code. We have a working pattern from `browser-tool` (same repo owner) that uses CrewAI with Claude on Bedrock — we'll follow that pattern directly.

Key constraint: transcript files already exist in Google Drive as `.txt` files produced by Google Meet's auto-transcription. The job is to fetch and analyze them, not produce them.

## Goals / Non-Goals

**Goals:**
- Fetch the latest transcript from a Google Drive folder via OAuth2
- Run two sequential CrewAI agents (speech coach → grammarian) powered by Claude on Bedrock
- Produce a timestamped Markdown report in `output/`
- Expose a CLI entry point (`python -m meet_analyzer`)

**Non-Goals:**
- Real-time or audio analysis
- Web UI, scheduling, or cron automation
- Multi-language support
- YAML-driven `@CrewBase` pattern (we use the functional style from browser-tool)

## Decisions

### D1: Drive fetch happens before the crew runs (not as a CrewAI tool)

The transcript fetch is deterministic and mechanical — there's no agent reasoning involved. Fetching inside `__main__.py` before `crew.kickoff()` keeps agents simple (no tools, no tool-call parsing issues) and makes the fetch independently testable.

**Alternative considered**: GoogleDriveTool subclassing `BaseTool`, given to Agent 1. Rejected because it adds the Bedrock tool-call normalization complexity (see D4) and gives the agent unnecessary decision-making over a mechanical step.

### D2: LLM is Claude on Bedrock via CrewAI's LiteLLM wrapper

```
LLM(model="bedrock/us.anthropic.claude-sonnet-4-20250514-v1:0")
```

Identical pattern to `browser-tool/browser_tool/crew/llm.py`. No AWS SDK config beyond standard env vars (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION`). A `create_llm()` helper in `crew/llm.py` mirrors browser-tool exactly.

### D3: Functional crew style, no @CrewBase or YAML configs

Plain `Agent(...)`, `Task(...)`, `Crew(...)` constructors. Agent configs live in Python, not `config/agents.yaml`. Matches browser-tool's style and avoids the indirection of YAML-driven wiring for a two-agent system this simple.

### D4: Bedrock tool-call patch included at startup

browser-tool contains `_patch_bedrock_tool_arg_parsing()` that normalizes Bedrock's dict-style tool calls (`{name, input}`) into OpenAI-style objects (`{function: {name, arguments}}`). Even though agents currently have no tools, the patch is included in `crew/crew.py` at module import time — it's a one-time safety net that costs nothing and prevents silent failures if a tool is added later.

### D5: Grammar agent receives speech agent output via context=[]

```python
grammar_task = Task(context=[speech_task], ...)
```

Explicit context dependency rather than `Process.sequential`. Both approaches produce the same result, but `context=[speech_task]` is more readable and doesn't require setting `process=Process.sequential` on the Crew.

### D6: OAuth2 with stored token

User credentials OAuth2 flow. Token stored in `~/.config/meet-analyzer/token.json` (or path from env var). First run triggers browser consent; subsequent runs use the stored token silently. Service account was considered but requires Drive sharing configuration — stored token is simpler for a personal tool.

## File Structure

```
src/meet_analyzer/
├── __init__.py
├── __main__.py          ← argparse CLI, fetches transcript, runs crew, writes report
├── crew/
│   ├── __init__.py
│   ├── llm.py           ← create_llm(provider, model)
│   ├── agents.py        ← create_speech_agent(llm), create_grammar_agent(llm)
│   ├── tasks.py         ← create_speech_task(agent, transcript), create_grammar_task(agent, speech_task)
│   └── crew.py          ← _patch_bedrock_tool_arg_parsing(), TranscriptAnalyzerCrew
└── drive/
    ├── __init__.py
    ├── auth.py          ← get_credentials() — OAuth2 load/refresh
    └── fetch.py         ← fetch_latest_transcript(folder_name, credentials) → str
```

## Risks / Trade-offs

- **OAuth2 first-run UX**: Requires a browser on first run. Not headless-friendly. Acceptable for a personal CLI tool. → Mitigation: clear error message if token is missing, instructions in README.
- **Transcript size**: Very long meetings may exceed context window. → Mitigation: truncate at a safe limit (e.g. 100k chars) with a warning; add `--file` flag to test with local files without Drive.
- **Bedrock availability**: Requires AWS credentials and Bedrock model access enabled in the account. → Mitigation: `.env.example` documents required vars; clear error if credentials are missing.
- **Sequential agents, no parallelism**: Grammar agent waits for speech agent to finish. For a CLI tool processing one transcript this is fine; not worth the complexity of parallel execution.

## Open Questions

None — all design decisions were resolved during exploration.
