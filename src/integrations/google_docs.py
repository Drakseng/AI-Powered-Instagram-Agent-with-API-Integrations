from google.oauth2 import service_account
from googleapiclient.discovery import build


def read_google_doc(service_account_json: str, document_id: str) -> str:
    """
    Read and return the full plain text of a Google Docs document.

    Args:
        service_account_json: Path to the Google service account JSON file.
        document_id: Google Docs document ID (not the full URL).

    Returns:
        The full text content of the document as a single string.
    """
    scopes = ["https://www.googleapis.com/auth/documents.readonly"]

    credentials = service_account.Credentials.from_service_account_file(
        service_account_json, scopes=scopes
    )

    docs_service = build("docs", "v1", credentials=credentials)
    doc = docs_service.documents().get(documentId=document_id).execute()
    content = doc.get("body", {}).get("content", [])

    full_text_chunks = []

    for element in content:
        paragraph = element.get("paragraph")
        if not paragraph:
            continue
        for run in paragraph.get("elements", []):
            text_run = run.get("textRun", {})
            text = text_run.get("content", "")
            full_text_chunks.append(text)

    return "".join(full_text_chunks).strip()
