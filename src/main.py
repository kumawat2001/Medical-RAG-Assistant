from retriever import initialize_retriever, retrieve_context
from llm import generate_answer


def main():

    print("=" * 50)
    print("       Medical RAG Chatbot")
    print("=" * 50)

    print("\nInitializing Retriever...")

    chunks, index = initialize_retriever()

    print("Retriever Initialized Successfully!")

    print("\nYou can now ask questions about the PDF.")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:

        question = input("Ask a Question: ")

        if question.lower() in ["exit", "quit"]:

            print("\nThank you for using the Medical RAG Chatbot!")

            break

        print("\nSearching relevant information...\n")

        context, sources = retrieve_context(
            question,
            chunks,
            index
        )

        print("Generating Answer...\n")

        answer = generate_answer(
            context,
            question
        )

        print("=" * 50)

        print(answer)

        print("\nSources Used:")

        unique_sources = []

        for source in sources:

            source_text = (
                f"{source['pdf_name']} "
                f"(Page {source['page']})"
            )

            if source_text not in unique_sources:

                unique_sources.append(source_text)

        for source in unique_sources:

            print(f"- {source}")

        print("=" * 50)
        print()


if __name__ == "__main__":
    main()