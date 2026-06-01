## ADDED Requirements

### Requirement: Professional English grammarian agent
The system SHALL run a CrewAI agent that analyzes grammar and syntax quality in the transcript, receiving the speech agent's output as context.

#### Scenario: Agent receives speech analysis as context
- **WHEN** the grammar task is created
- **THEN** it sets `context=[speech_task]` so the grammar agent sees the speech agent's findings before producing its own analysis

#### Scenario: Agent produces grammar analysis
- **WHEN** the grammar agent receives the transcript and speech context
- **THEN** it returns a report covering: sentence structure issues (fragments, run-ons, dangling modifiers), subject-verb agreement errors, tense consistency, word choice and vocabulary suggestions, and clarity/conciseness improvements

#### Scenario: Agent has no tools
- **WHEN** the grammar agent is created
- **THEN** it has an empty tools list — the transcript is injected directly into the task description

#### Scenario: Agent runs after speech agent
- **WHEN** the crew runs
- **THEN** the grammar task executes only after the speech task completes
