import fitz  # PyMuPDF
from pathlib import Path


def extract_text(pdf_path: Path) -> str:
    """
    Extracts all text from a PDF file.

    Args:
        pdf_path (Path): Path to the PDF file.

    Returns:
        str: Extracted text from all pages.

    Raises:
        FileNotFoundError: If the PDF file does not exist.
        RuntimeError: If the PDF cannot be opened or read.
    """

    # Check if the file exists
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    try:
        # Open the PDF
        document = fitz.open(pdf_path)

        extracted_text = []

        # Loop through every page
        for page in document:
            page_text = page.get_text()

            if page_text:
                extracted_text.append(page_text)

        # Close the document
        document.close()

        # Combine all page text
        return "\n".join(extracted_text)

    except Exception as error:
        raise RuntimeError(f"Error extracting text from PDF: {error}")