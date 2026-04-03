from io import BytesIO

from PyPDF2 import PdfReader


def extract_text_from_pdf(file_bytes: bytes) -> str:
    pdf_reader = PdfReader(BytesIO(file_bytes))
    text_chunks: list[str] = []

    for page in pdf_reader.pages:
        extracted = page.extract_text() or ""
        if extracted.strip():
            text_chunks.append(extracted.strip())

    return "\n".join(text_chunks).strip()

