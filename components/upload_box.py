import streamlit as st


def render_upload_box():
    """
    Displays the PDF upload widget
    and returns the uploaded file.
    """

    uploaded_file = st.file_uploader(
        label="Upload a PDF",
        type=["pdf"],
        accept_multiple_files=False,
        help="Only PDF files are allowed."
    )

    return uploaded_file
