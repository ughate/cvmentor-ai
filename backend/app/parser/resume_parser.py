from pathlib import Path

from docx import Document
from pypdf import PdfReader


def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from a PDF resume."""

    reader = PdfReader(file_path)

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n".join(pages).strip()


def extract_text_from_docx(file_path: str) -> str:
    """Extract text from a DOCX resume.

    Handles both:
    - Normal Word paragraphs
    - Text stored inside Word tables
    """

    document = Document(file_path)

    text_parts = []

    # --------------------------------------------------
    # 1. Read normal paragraphs
    # --------------------------------------------------

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()

        if text:
            text_parts.append(text)

    # --------------------------------------------------
    # 2. Read tables
    # --------------------------------------------------

    for table in document.tables:

        for row in table.rows:

            row_parts = []

            for cell in row.cells:

                cell_text = cell.text.strip()

                if cell_text:
                    row_parts.append(cell_text)

            if row_parts:
                text_parts.append(" | ".join(row_parts))

    # --------------------------------------------------
    # 3. Combine everything
    # --------------------------------------------------

    return "\n".join(text_parts).strip()


def extract_resume_text(file_path: str) -> str:
    """Detect the file type and extract resume text."""

    extension = Path(file_path).suffix.lower()

    if extension == ".pdf":
        return extract_text_from_pdf(file_path)

    if extension == ".docx":
        return extract_text_from_docx(file_path)

    raise ValueError(
        "Unsupported file format. Please upload a PDF or DOCX file."
    )