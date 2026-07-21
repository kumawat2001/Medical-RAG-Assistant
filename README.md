# 🩺 Medical RAG Assistant

An AI-powered Medical Retrieval-Augmented Generation (RAG) application that allows users to upload medical PDF documents and ask natural language questions. The application retrieves relevant information from the uploaded document using semantic search (FAISS) and generates context-aware responses using Google's Gemini model.

---

## 🚀 Features

- 🔐 User Authentication (Login & Signup)
- 📄 Upload Medical PDF Documents
- ✂️ Automatic Text Chunking
- 🧠 Hugging Face Embeddings
- 🔍 Semantic Search using FAISS
- 🤖 AI-powered Question Answering with Gemini
- 💬 Conversation Memory for Follow-up Questions
- 📚 Source Citation with Page Numbers
- 📱 Responsive Streamlit Interface
- ☁️ Deployed on Streamlit Community Cloud

---

## 🛠️ Tech Stack

### Frontend
- Streamlit

### Backend
- Python

### AI & Machine Learning
- LangChain
- Hugging Face Sentence Transformers
- Google Gemini API
- FAISS Vector Database

### Authentication
- SQLite
- bcrypt

### Libraries
- PyPDF
- NumPy
- Pandas
- Pickle

---

## 📂 Project Structure

```
Medical-RAG-Assistant/
│
├── src/
│   ├── app.py
│   ├── auth.py
│   ├── database.py
│   ├── retriever.py
│   ├── loader.py
│   ├── chunker.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── llm.py
│   ├── memory.py
│   ├── chat_manager.py
│   └── pdf_uploader.py
│
├── data/
├── database/
├── requirements.txt
└── README.md
```

---

## ⚙️ How It Works

1. User signs up or logs into the application.
2. Upload a medical PDF document.
3. The document is:
   - Loaded
   - Split into text chunks
   - Converted into embeddings
   - Indexed using FAISS
4. User asks a question.
5. The retriever searches for the most relevant chunks.
6. Gemini generates an answer using only the retrieved context.
7. The application displays the answer along with source page citations.

---

## 🧠 RAG Pipeline

```
PDF Upload
      │
      ▼
Text Extraction
      │
      ▼
Chunking
      │
      ▼
Embeddings
(Hugging Face)
      │
      ▼
FAISS Vector Store
      │
      ▼
Similarity Search
      │
      ▼
Gemini LLM
      │
      ▼
Answer + Source Citations
```

---

## 📸 Application Workflow

- Login / Signup
- Upload Medical PDF
- Knowledge Base Creation
- Ask Questions
- View AI-generated Responses
- View Source Citations
- Continue Conversation using Memory

---

## 💡 Example Questions

- What is cardiopulmonary bypass?
- What are the components of a heart-lung machine?
- Explain cardioplegia.
- What are the complications of CPB?
- Compare roller pumps and centrifugal pumps.

---

## 🔑 Environment Variables

Create a `.streamlit/secrets.toml` file:

```toml
HF_TOKEN="YOUR_HUGGINGFACE_TOKEN"
GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
```

---

## ▶️ Run Locally

Clone the repository

```bash
git clone https://github.com/kumawat2001/Medical-RAG-Assistant.git
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run Streamlit

```bash
streamlit run src/app.py
```

---

## 🌐 Live Demo

(Add your Streamlit URL here)

---

## 📈 Future Improvements

- Support multiple PDF documents
- Hybrid Retrieval (BM25 + Dense Retrieval)
- Persistent Vector Database (ChromaDB/Pinecone)
- Streaming Responses
- OCR Support for Scanned PDFs
- Admin Dashboard
- Progress Bar for Knowledge Base Generation

---

## 👨‍💻 Author

**Akshat Kumawat**

LinkedIn: https://linkedin.com/in/akshatku/

GitHub: https://github.com/kumawat2001

---
