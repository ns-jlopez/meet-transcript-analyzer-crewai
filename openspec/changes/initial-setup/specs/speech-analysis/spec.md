## ADDED Requirements

### Requirement: Speech and pronunciation coach agent
The system SHALL run a CrewAI agent that analyzes spoken language patterns in the transcript and produces a structured analysis.

#### Scenario: Agent produces speech analysis
- **WHEN** the speech agent receives a transcript
- **THEN** it returns a report covering: filler words (frequency and examples), repetitive phrases or verbal tics, sentence cadence issues (run-ons, abrupt stops), and speaking confidence indicators

#### Scenario: Agent is powered by Claude on Bedrock
- **WHEN** the crew is initialized
- **THEN** the speech agent uses `LLM(model="bedrock/us.anthropic.claude-sonnet-4-20250514-v1:0")`

#### Scenario: Agent has no tools
- **WHEN** the speech agent is created
- **THEN** it has an empty tools list — the transcript is injected directly into the task description
