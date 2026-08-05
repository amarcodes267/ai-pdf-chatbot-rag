import re


def clean_text(text: str) -> str:
    """
    Cleans extracted PDF text.

    Args:
        text (str): Raw extracted text.

    Returns:
        str: Cleaned text.
    """

    # Remove leading and trailing whitespace
    text = text.strip()

    # Replace multiple spaces or tabs with a single space
    text = re.sub(r"[ \t]+", " ", text)

    # Replace multiple blank lines with a single blank line
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    return text