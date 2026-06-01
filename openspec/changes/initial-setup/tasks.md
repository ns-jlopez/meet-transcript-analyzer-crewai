## 1. Project Scaffolding

- [x] 1.1 Create `pyproject.toml` with dependencies: `crewai`, `google-auth`, `google-auth-oauthlib`, `google-api-python-client`
- [x] 1.2 Create `.env.example` documenting `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION`, `GOOGLE_CREDENTIALS_PATH`, `GOOGLE_TOKEN_PATH`, `GOOGLE_DRIVE_FOLDER_NAME`
- [x] 1.3 Create `.gitignore` ignoring `output/`, `.env`, `token.json`, `.venv/`
- [x] 1.4 Create `src/meet_analyzer/__init__.py` and package structure

## 2. LLM Wiring

- [x] 2.1 Create `crew/llm.py` with `create_llm(provider="bedrock", model=None)` mirroring browser-tool's pattern
- [x] 2.2 Verify Bedrock model ID `bedrock/us.anthropic.claude-sonnet-4-20250514-v1:0` as default

## 3. Google Drive Integration

- [x] 3.1 Create `drive/auth.py` with `get_credentials()` — OAuth2 load/refresh, token stored at `~/.config/meet-analyzer/token.json`
- [x] 3.2 Create `drive/fetch.py` with `fetch_latest_transcript(folder_name, credentials) -> str` — lists `.txt` files, picks latest by `modifiedTime`, downloads content
- [x] 3.3 Add transcript truncation at 100,000 characters with stderr warning

## 4. CrewAI Agents and Tasks

- [x] 4.1 Create `crew/agents.py` with `create_speech_agent(llm)` and `create_grammar_agent(llm)` — no tools, role/goal/backstory defined
- [x] 4.2 Create `crew/tasks.py` with `create_speech_task(agent, transcript)` and `create_grammar_task(agent, speech_task)` — grammar task sets `context=[speech_task]`
- [x] 4.3 Create `crew/crew.py` with `_patch_bedrock_tool_arg_parsing()` (copied from browser-tool) and `TranscriptAnalyzerCrew` class

## 5. CLI Entry Point

- [x] 5.1 Create `__main__.py` with `argparse` CLI: `--folder` (default: "Meet Recordings"), `--file` (local override)
- [x] 5.2 Wire up: validate env vars → fetch transcript (Drive or local) → run crew → write report
- [x] 5.3 Add env var validation with clear error messages for missing AWS credentials

## 6. Report Output

- [x] 6.1 Create `output/` directory creation logic (mkdir if absent)
- [x] 6.2 Write `output/report_<YYYYMMDD_HHMMSS>.md` with sections for Speech Analysis and Grammar Analysis
- [x] 6.3 Print token usage and estimated cost summary to stdout after crew completes (same `_print_cost` pattern as browser-tool)
