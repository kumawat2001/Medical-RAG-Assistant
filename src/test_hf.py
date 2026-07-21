import os

from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

client = InferenceClient(
    provider="auto",
    api_key=os.getenv("HF_TOKEN")
)

response = client.chat.completions.create(
    model="google/gemma-2-2b-it",
    messages=[
        {
            "role": "user",
            "content": "Say Hello"
        }
    ],
)

print(response.choices[0].message.content)