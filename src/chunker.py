from langchain.text_splitter import RecursiveCharacterTextSplitter


def create_chunks(documents):
    """
    Creates chunks from all PDFs while preserving
    the PDF name and page number.

    Returns:
    [
        {
            "pdf_name": "...",
            "page": 1,
            "text": "..."
        }
    ]
    """

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = []

    for document in documents:

        pdf_name = document["pdf_name"]

        for page in document["pages"]:

            page_number = page["page"]
            page_text = page["text"]

            split_chunks = text_splitter.split_text(page_text)

            for chunk in split_chunks:

                chunks.append(
                    {
                        "pdf_name": pdf_name,
                        "page": page_number,
                        "text": chunk
                    }
                )

    return chunks