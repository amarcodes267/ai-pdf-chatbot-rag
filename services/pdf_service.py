from pathlib import Path
from uuid import uuid4

from utils.constants import ALLOWED_FILE_TYPES, MAX_FILE_SIZE

PROJECT_ROOT = Path(__file__).resolve().parents[1]
UPLOAD_DIR = PROJECT_ROOT / "data" / "uploads"


def save_pdf(uploaded_file):
    """
    Saves the uploaded PDF to the uploads directory
    and returns the saved file path.
    """

    if uploaded_file is None:
        raise ValueError("No file uploaded.")

    filename = Path(str(getattr(uploaded_file, "name", ""))).name
    if not filename:
        raise ValueError("Uploaded file must have a filename.")
    ext = Path(filename).suffix.lower().lstrip(".")

    if ext not in ALLOWED_FILE_TYPES:
        raise ValueError(
            f"Unsupported file type '{ext}'. Allowed types: {ALLOWED_FILE_TYPES}"
        )

    file_size = getattr(uploaded_file, "size", None)
    if file_size is not None and file_size > MAX_FILE_SIZE:
        raise ValueError(
            f"File size {file_size / (1024 * 1024):.1f} MB exceeds the maximum allowed size of {MAX_FILE_SIZE / (1024 * 1024):.0f} MB."
        )

    # Create uploads folder if it doesn't exist
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    # Keep the original name for display while preventing path traversal and
    # collisions between uploads received in the same second.
    safe_name = f"{uuid4().hex}_{filename}"

    file_path = UPLOAD_DIR / safe_name

    # Save the uploaded file
    with open(file_path, "wb") as file:
        file.write(uploaded_file.getbuffer())

    return file_path
