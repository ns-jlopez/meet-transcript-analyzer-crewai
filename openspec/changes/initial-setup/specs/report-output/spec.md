## ADDED Requirements

### Requirement: Timestamped Markdown report
The system SHALL write the combined analysis to `output/report_<YYYYMMDD_HHMMSS>.md` after both agents complete.

#### Scenario: Report is written after crew completes
- **WHEN** the crew finishes successfully
- **THEN** a Markdown file is written to `output/` with a timestamp in the filename (e.g. `report_20260601_143022.md`)

#### Scenario: Output directory is created if absent
- **WHEN** the `output/` directory does not exist
- **THEN** system creates it before writing the report

#### Scenario: Report structure
- **WHEN** the report is written
- **THEN** it contains clearly separated sections for Speech & Pronunciation Analysis and Grammar & Syntax Analysis, each with the respective agent's findings

### Requirement: Token usage summary printed to stdout
The system SHALL print a token usage and estimated cost summary to stdout after the crew completes, following the same pattern as browser-tool.

#### Scenario: Crew completes with token data
- **WHEN** `result.token_usage` is available after `crew.kickoff()`
- **THEN** system prints input tokens, cached tokens (if any), output tokens, and estimated total cost in USD
