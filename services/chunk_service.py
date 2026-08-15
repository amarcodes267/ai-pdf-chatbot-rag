def _split_text(text: str, chunk_size: int, chunk_overlap: int) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive.")
    if not 0 <= chunk_overlap < chunk_size:
        raise ValueError("chunk_overlap must be at least 0 and smaller than chunk_size.")

    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        if end < len(text):
            boundary = max(text.rfind("\n", start, end), text.rfind(" ", start, end))
            if boundary > start + (chunk_size // 2):
                end = boundary
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= len(text):
            break
        start = max(end - chunk_overlap, start + 1)
    return chunks


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

    return _split_text(text, chunk_size, chunk_overlap)


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

    for page_idx, page_text in enumerate(page_texts, start=1):
        if not page_text:
            continue

        chunks = _split_text(page_text, chunk_size, chunk_overlap)

        for chunk_idx, chunk in enumerate(chunks, start=1):
            all_chunks.append(chunk)
            metadatas.append({
                "source": filename,
                "page": page_idx,
                "chunk": chunk_idx,
            })

    return all_chunks, metadatas
