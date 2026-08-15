from io import BytesIO
from services import pdf_service


class DummyUploaded:
    def __init__(self, name: str, data: bytes):
        self.name = name
        self._buf = BytesIO(data)

    def getbuffer(self):
        return self._buf.getbuffer()


def test_save_pdf_writes_file_and_returns_path(tmp_path, monkeypatch):
    # Create a small dummy PDF-like byte content
    dummy = DummyUploaded("sample.pdf", b"%PDF-1.4\n%EOF")

    monkeypatch.setattr(pdf_service, "UPLOAD_DIR", tmp_path)
    saved = pdf_service.save_pdf(dummy)

    assert saved.exists()
    assert saved.read_bytes() == b"%PDF-1.4\n%EOF"
    assert saved.name.endswith("_sample.pdf")


def test_save_pdf_rejects_path_traversal_filename(tmp_path, monkeypatch):
    monkeypatch.setattr(pdf_service, "UPLOAD_DIR", tmp_path)

    saved = pdf_service.save_pdf(DummyUploaded("../sample.pdf", b"PDF"))

    assert saved.parent == tmp_path
    assert saved.name.endswith("_sample.pdf")
