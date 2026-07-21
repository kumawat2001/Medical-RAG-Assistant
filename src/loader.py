from pathlib import Path
from pypdf import PdfReader


def load_pdfs(folder_path):
    """
    Loads all PDFs from the given folder
    and all of its subfolders.

    Returns:
        documents (list)
    """

    documents = []

    folder_path = Path(folder_path)

    # Search recursively for every PDF
    pdf_files = folder_path.rglob("*.pdf")

    for pdf_path in pdf_files:

        reader = PdfReader(str(pdf_path))

        pages = []

        for page_number, page in enumerate(reader.pages, start=1):

            extracted_text = page.extract_text()

            if extracted_text:

                pages.append(
                    {
                        "page": page_number,
                        "text": extracted_text
                    }
                )

        documents.append(
            {
                "pdf_name": pdf_path.name,
                "pages": pages
            }
        )

    return documents