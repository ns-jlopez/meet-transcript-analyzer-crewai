## ADDED Requirements

### Requirement: OAuth2 authentication with stored token
The system SHALL authenticate with Google Drive using OAuth2 user credentials, storing the token at `~/.config/meet-analyzer/token.json` (overridable via `GOOGLE_TOKEN_PATH` env var).

#### Scenario: First run — token absent
- **WHEN** no token file exists
- **THEN** system opens a browser OAuth2 consent flow and stores the resulting token

#### Scenario: Subsequent run — valid token
- **WHEN** a valid non-expired token exists
- **THEN** system loads the token silently without any browser interaction

#### Scenario: Expired token
- **WHEN** a stored token has expired but has a refresh token
- **THEN** system refreshes it silently and updates the stored token file

### Requirement: Fetch latest transcript from Drive folder
The system SHALL find the most recently modified `.txt` file in the named Google Drive folder and return its content as a string.

#### Scenario: Folder contains transcript files
- **WHEN** the target folder contains one or more `.txt` files
- **THEN** system downloads and returns the content of the most recently modified one

#### Scenario: Folder is empty or has no .txt files
- **WHEN** the target folder exists but contains no `.txt` files
- **THEN** system exits with a clear error message

#### Scenario: Folder does not exist
- **WHEN** no folder matching the given name is found in Drive
- **THEN** system exits with a clear error message naming the folder

### Requirement: Transcript truncation
The system SHALL truncate transcripts exceeding 100,000 characters and emit a warning.

#### Scenario: Transcript exceeds limit
- **WHEN** the downloaded transcript is longer than 100,000 characters
- **THEN** system truncates to 100,000 characters and prints a warning with the original length
