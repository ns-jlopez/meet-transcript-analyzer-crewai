import io
import sys

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

_MAX_CHARS = 100_000


def fetch_latest_transcript(folder_name, credentials):
    service = build("drive", "v3", credentials=credentials)

    folders = service.files().list(
        q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false",
        fields="files(id, name)",
    ).execute().get("files", [])

    if not folders:
        raise RuntimeError(f"Google Drive folder '{folder_name}' not found.")

    folder_id = folders[0]["id"]

    files = service.files().list(
        q=f"'{folder_id}' in parents and mimeType='text/plain' and trashed=false",
        orderBy="modifiedTime desc",
        pageSize=1,
        fields="files(id, name, modifiedTime)",
    ).execute().get("files", [])

    if not files:
        raise RuntimeError(f"No .txt files found in Drive folder '{folder_name}'.")

    latest = files[0]
    print(f"Fetching transcript: {latest['name']} (modified {latest['modifiedTime']})")

    request = service.files().get_media(fileId=latest["id"])
    buffer = io.BytesIO()
    downloader = MediaIoBaseDownload(buffer, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()

    content = buffer.getvalue().decode("utf-8")

    if len(content) > _MAX_CHARS:
        print(
            f"Warning: transcript is {len(content):,} characters — truncating to {_MAX_CHARS:,}.",
            file=sys.stderr,
        )
        content = content[:_MAX_CHARS]

    return content
