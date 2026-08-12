import streamlit as st


def render_upload_box():
    """
    Displays the PDF upload widget
    and returns the uploaded file.
    """

    uploaded_file = st.file_uploader(
        label="Upload PDF(s)",
        type=["pdf"],
        accept_multiple_files=True,
        help="You can upload one or more PDF files."
    )

    return uploaded_file
