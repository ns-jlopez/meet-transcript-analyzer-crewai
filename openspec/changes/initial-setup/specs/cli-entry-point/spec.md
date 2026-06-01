## ADDED Requirements

### Requirement: CLI entry point
The system SHALL be runnable via `python -m meet_analyzer` with optional arguments to control Drive folder name and local file override.

#### Scenario: Run with defaults
- **WHEN** user runs `python -m meet_analyzer`
- **THEN** system fetches the latest transcript from the "Meet Recordings" folder and runs analysis

#### Scenario: Custom folder name
- **WHEN** user runs `python -m meet_analyzer --folder "My Meetings"`
- **THEN** system fetches from the specified folder name instead of the default

#### Scenario: Local file override
- **WHEN** user runs `python -m meet_analyzer --file path/to/transcript.txt`
- **THEN** system reads the transcript from the local file, skipping Drive entirely

#### Scenario: Missing credentials
- **WHEN** required env vars (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION`) are absent
- **THEN** system exits with a clear error message naming the missing variable(s)
