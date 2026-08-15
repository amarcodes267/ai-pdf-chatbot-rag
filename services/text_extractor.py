try:
    import pymupdf as fitz
except ImportError:  # PyMuPDF versions before 1.24 expose the fitz module.
    import fitz
from pathlib import Path


def extract_text(pdf_path: Path) -> list[str]:
    """
    Extracts text from each page of a PDF file and returns a list of page texts.

    Args:
        pdf_path (Path): Path to the PDF file.

    Returns:
        list[str]: Extracted text for each page.

    Raises:
        FileNotFoundError: If the PDF file does not exist.
        RuntimeError: If the PDF cannot be opened or read.
    """

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    try:
        with fitz.open(pdf_path) as document:
            return [page.get_text() or "" for page in document]

    except Exception as error:
        raise RuntimeError(f"Error extracting text from PDF: {error}")
