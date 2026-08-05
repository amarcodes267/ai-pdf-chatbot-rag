from langchain_text_splitters import RecursiveCharacterTextSplitter


def create_chunks(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200
) -> list[str]:
    """
    Splits cleaned text into overlapping chunks.

    Args:
        text (str): Cleaned document text.
        chunk_size (int): Maximum characters per chunk.
        chunk_overlap (int): Overlap between consecutive chunks.

    Returns:
        list[str]: List of text chunks.
    """

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    chunks = text_splitter.split_text(text)

    return chunks