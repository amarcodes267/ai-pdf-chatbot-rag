import os
from io import BytesIO
from services.pdf_service import save_pdf


class DummyUploaded:
    def __init__(self, name: str, data: bytes):
        self.name = name
        self._buf = BytesIO(data)

    def getbuffer(self):
        return self._buf.getbuffer()


def test_save_pdf_writes_file_and_returns_path(tmp_path):
    # Create a small dummy PDF-like byte content
    dummy = DummyUploaded("sample.pdf", b"%PDF-1.4\n%EOF")

    # Temporarily change uploads dir via environment if needed - here function writes to data/uploads
    saved = save_pdf(dummy)

    assert os.path.exists(saved)

    # Clean up
    try:
        os.remove(saved)
    except Exception:
        pass
