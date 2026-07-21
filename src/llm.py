import os

from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# -----------------------------
# Load Environment Variables
# -----------------------------

load_dotenv()

hf_token = os.getenv("HF_TOKEN")

if not hf_token:
    raise ValueError("HF_TOKEN not found in .env file")

# -----------------------------
# Hugging Face Client
# -----------------------------

client = InferenceClient(
    provider="auto",
    api_key=hf_token,
)

# -----------------------------
# Generate Answer
# -----------------------------

def generate_answer(context, question):
    """
    Generates an answer using the retrieved context.
    """

    prompt = f"""
You are an expert medical AI assistant.

Your job is to answer questions using the retrieved medical documents.

Instructions:

- Use the retrieved context as your primary source of information.
- Give clear, complete, and natural explanations.
- If the user asks for more detail, elaborate using the available context.
- If the user asks a follow-up question (for example: "explain more", "what about treatment?", "what are the symptoms?", "can you elaborate?"), understand it in relation to the current conversation.
- Do NOT invent medical facts that are not supported by the retrieved context.
- If the retrieved context does not contain enough information, reply exactly:

"I don't have enough information in the provided documents to answer that question."

Retrieved Context:
{context}

User Question:
{question}

Answer:
"""

    try:

        response = client.chat.completions.create(
            model="google/gemma-2-2b-it",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=512,
            temperature=0.2,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Error: {e}"