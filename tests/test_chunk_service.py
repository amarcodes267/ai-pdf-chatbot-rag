from services.chunk_service import create_chunks_from_pages


def test_create_chunks_from_pages_metadata():
    pages = ["This is a test page. " * 200]
    chunks, metadatas = create_chunks_from_pages(pages, filename="doc.pdf", chunk_size=500, chunk_overlap=50)

    assert len(chunks) == len(metadatas)
    assert len(chunks) > 0
    for m in metadatas:
        assert m.get("source") == "doc.pdf"
        assert "page" in m and m.get("page") >= 1
        assert "chunk" in m
