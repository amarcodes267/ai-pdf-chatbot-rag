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


def create_chunks_from_pages(
    page_texts: list[str],
    filename: str | None = None,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
) -> tuple[list[str], list[dict]]:
    """
    Create chunks from a list of page texts and return both the chunks
    and corresponding metadata entries for each chunk.
    """

    all_chunks: list[str] = []
    metadatas: list[dict] = []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    for page_idx, page_text in enumerate(page_texts, start=1):
        if not page_text:
            continue

        chunks = splitter.split_text(page_text)

        for chunk_idx, chunk in enumerate(chunks, start=1):
            all_chunks.append(chunk)
            metadatas.append({
                "source": filename,
                "page": page_idx,
                "chunk": chunk_idx,
            })

    return all_chunks, metadatas