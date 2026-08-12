import fitz  # PyMuPDF
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
        document = fitz.open(pdf_path)

        page_texts: list[str] = []

        for page in document:
            page_text = page.get_text()
            page_texts.append(page_text or "")

        document.close()

        return page_texts

    except Exception as error:
        raise RuntimeError(f"Error extracting text from PDF: {error}")