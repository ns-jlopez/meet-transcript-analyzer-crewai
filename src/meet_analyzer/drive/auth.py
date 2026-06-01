import os
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

_DEFAULT_TOKEN_PATH = Path.home() / ".config" / "meet-analyzer" / "token.json"
_DEFAULT_CREDENTIALS_PATH = Path.home() / ".config" / "meet-analyzer" / "credentials.json"


def get_credentials():
    token_path = Path(os.environ.get("GOOGLE_TOKEN_PATH", _DEFAULT_TOKEN_PATH))
    credentials_path = Path(os.environ.get("GOOGLE_CREDENTIALS_PATH", _DEFAULT_CREDENTIALS_PATH))

    creds = None
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not credentials_path.exists():
                raise FileNotFoundError(
                    f"Google credentials file not found at {credentials_path}. "
                    "Download it from Google Cloud Console and set GOOGLE_CREDENTIALS_PATH."
                )
            flow = InstalledAppFlow.from_client_secrets_file(str(credentials_path), SCOPES)
            creds = flow.run_local_server(port=0)

        token_path.parent.mkdir(parents=True, exist_ok=True)
        token_path.write_text(creds.to_json())

    return creds
