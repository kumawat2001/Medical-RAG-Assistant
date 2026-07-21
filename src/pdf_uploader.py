from pathlib import Path


def save_uploaded_pdf(uploaded_file):
    """
    Save the uploaded PDF into the data/uploaded_pdfs folder.

    Parameters:
        uploaded_file: Streamlit UploadedFile object

    Returns:
        Path to the saved PDF.
    """

    # Project Root
    project_root = Path(__file__).resolve().parent.parent

    # Create folder if it doesn't exist
    upload_folder = project_root / "data" / "uploaded_pdfs"
    upload_folder.mkdir(parents=True, exist_ok=True)

    # Destination path
    file_path = upload_folder / uploaded_file.name

    # Save PDF
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path