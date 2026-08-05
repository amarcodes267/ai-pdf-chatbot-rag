from pathlib import Path
from datetime import datetime


UPLOAD_DIR = Path("data/uploads")


def save_pdf(uploaded_file):
    """
    Saves the uploaded PDF to the uploads directory
    and returns the saved file path.
    """

    # Create uploads folder if it doesn't exist
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    # Create a unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{uploaded_file.name}"

    file_path = UPLOAD_DIR / filename

    # Save the uploaded file
    with open(file_path, "wb") as file:
        file.write(uploaded_file.getbuffer())

    return file_path