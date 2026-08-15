# AI PDF Chatbot (RAG)

A professional, production-minded Retrieval-Augmented Generation (RAG) demo built with Streamlit.

This repository provides a lightweight pipeline to:

- Upload one or more PDF documents
- Extract and clean text from PDFs (page-level)
- Split text into overlapping chunks with metadata (document, page, chunk)
- Create lightweight hashed keyword vectors with no model download
- Persist vectors and metadata in a compact local JSON index
- Perform relevance retrieval and produce grounded answers using an LLM (OpenAI optional)
- Display source references (document, page, chunk, similarity)

---

Table of Contents
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Repository Layout](#repository-layout)
- [Installation](#installation)
- [Configuration and Environment Variables](#configuration-and-environment-variables)
- [Running the Application](#running-the-application)
- [How the RAG Pipeline Works](#how-the-rag-pipeline-works)
- [Testing](#testing)
- [Troubleshooting and Tips](#troubleshooting-and-tips)
- [Future Improvements](#future-improvements)
- [License](#license)

---

## Features

- Multi-file PDF upload and processing
- Page-level extraction and chunking with overlap for better context
- Lightweight, dependency-free hashed keyword vectors
- Persistence using a local JSON index (`data/document_index.json`)
- Relevance retrieval with source metadata and similarity scores
- Optional LLM generation using OpenAI (fallback summary available if not configured)
- Streamlit UI with conversation history, loading states, and error handling

---

## Architecture

The app follows a simple, modular pipeline:

PDF Upload → PDF Extraction (page-level) → Text Cleaning → Chunking → Lightweight vectors → JSON index → Retrieval → Prompting → LLM → Answer + Sources

Key modules are under `services/` and the UI components under `components/` with an overall `chat_ui.py` that coordinates the workflow.

---

## Tech Stack

- Python 3.11+
- Streamlit (UI)
- PyMuPDF (`fitz`) for PDF extraction
- LangChain text splitters (for chunking)
- Standard-library hashed vectors for retrieval
- JSON file for vector storage
- OpenAI (optional) for LLM responses

---

## Repository Layout

- `app.py` — Streamlit entry point that loads the sidebar and chat UI
- `chat_ui.py` — Main UI and orchestration for upload, processing, and chat
- `components/` — Streamlit UI parts (sidebar, upload box)
- `services/` — Core services:
	- `pdf_service.py` — save uploaded file
	- `text_extractor.py` — page-level extraction from PDFs
	- `text_cleaner.py` — basic text cleaning
	- `chunk_service.py` — chunking and metadata generation
	- `embedding_service.py` — lightweight hashed keyword vectors
	- `vector_store.py` — JSON index wrapper (add/search/clear)
	- `retrieval_service.py` — query embedding + search wrapper
	- `rag_service.py` — retrieval + LLM orchestration
	- `llm_service.py` — LLM adapter (OpenAI optional fallback)
	- `chat_service.py` — Streamlit session-based chat history
- `data/` — stores `uploads/` and `document_index.json` (local vector index)
- `requirements.txt` — minimal dependency list
- `render.yaml` — Render Blueprint for deploying the web service
- `.python-version` — pins the Python version used on Render / local tooling
- `README.md` — this document

---

## Installation

1. Clone the repository and change into it:

```powershell
git clone <repo-url>
cd ai-pdf-chatbot-rag
```

2. Create and activate a virtual environment (Windows example):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The app has no local model download, making it suitable for low-memory hosts.

---

## Configuration and Environment Variables

The application uses environment variables to configure optional LLM behavior.

- `OPENAI_API_KEY` — Set this if you want the app to use OpenAI for responses. If omitted, a local deterministic fallback summary is used.
- `OPENAI_MODEL` — (optional) override the chat model (default `gpt-4o-mini`).

A template is provided in `.env.example`. Secrets are read from environment variables only — never hardcode them in source files. The `.env` file is gitignored.

The local index persists under `data/document_index.json`. Uploaded PDFs are stored in `data/uploads`. Both are regenerated at runtime and are gitignored.

---

## Running the Application

Start Streamlit from the repository root:

```powershell
streamlit run app.py
```

Open the URL that Streamlit prints (usually `http://localhost:8501`).

Workflow inside the app:

1. Use the sidebar to learn about the app.
2. Upload one or more PDF files via the upload box.
3. Click `Process uploaded PDF(s)` to extract, chunk, embed, and index documents.
4. Enter a question in the chat input and click `Send`.
5. The assistant will return an answer and a list of source snippets showing where the answer came from.

---

## Deployment — Render

This repository ships a ready-to-use [Render Blueprint](https://render.com/docs/blueprint-spec) (`render.yaml`) plus a `.python-version` file that pins the Python runtime (3.12).

### One-click Blueprint deploy

1. Push the repository to GitHub or GitLab.
2. In the Render dashboard, choose **New → Blueprint**.
3. Select this repository — Render reads `render.yaml` and creates the `ai-pdf-chatbot-rag` web service automatically.
4. When prompted, enter your `OPENAI_API_KEY` (optional — the app falls back to a local summary if omitted).

The service starts with:

```bash
streamlit run app.py --server.address 0.0.0.0 --server.port $PORT --server.headless true
```

### Important deployment notes

- **Free-plan memory:** This version uses lightweight local vectors and a JSON index, so it is designed for Render's 512 MB free plan.
- **Ephemeral filesystem:** Render's native runtime does not persist uploaded PDFs or `data/document_index.json` after restarts/redeploys. Re-ingest documents after a restart.
- **Health check:** `/_stcore/health` (Streamlit's built-in endpoint) is used so Render probes the running server.

---

## How the RAG Pipeline Works

1. PDF extraction: Each PDF is parsed page-by-page (PyMuPDF). Page texts are cleaned with `text_cleaner.py`.
2. Chunking: Each page is split into overlapping chunks using LangChain text splitters; metadata (source filename, page number, chunk index) is attached.
3. Vectors: Chunks are converted to compact hashed keyword vectors.
4. Vector store: A JSON index stores vectors, chunk text, and metadata for retrieval.
5. Retrieval: The question vector ranks the top-K most relevant chunks.
6. Prompting & LLM: Retrieved chunks are combined into a context and sent to the configured LLM (OpenAI by default). If no LLM is configured, a fallback summary is returned.
7. Sources: The app displays the retrieved chunks and their metadata alongside the answer so users can verify the citation.

---

## Testing

Basic tests to run manually:

1. Start the app and upload a small PDF (one or two pages).
2. Process the PDF and verify `data/uploads` and `data/document_index.json` contain artifacts.
3. Ask a question that is clearly answered in the PDF and verify the answer and sources.
4. Upload additional PDFs and verify cross-document retrieval works.
5. Test edge cases: empty question, unsupported file type, corrupted PDF (app shows error messages).

Automated tests are not included in this repository by default; consider adding pytest-based unit tests for the services in `services/`.

---

## Deployment and Production Readiness

Before deploying, keep the following in mind:

- **Environment variables:** `OPENAI_API_KEY` must be set at runtime for grounded LLM answers. Without it, the app falls back to showing a retrieved-context summary (configurable path only).
- **Dependencies:** install with `pip install -r requirements.txt` (Python 3.11+ recommended).
- **Startup command:** `streamlit run app.py`.
- **File storage:** uploaded PDFs and the JSON index are written under `data/`; Render clears them after restarts.
- **Index persistence:** `data/document_index.json` is local-only. Re-ingest documents after a restart, or use external storage for durable multi-user deployments.
- **Retrieval quality:** keyword vectors are intentionally lightweight. Exact terms work well; semantic paraphrases are less reliable than transformer embeddings.
- **LLM requirement:** OpenAI access (network + valid key) is required for production-quality answers. Ensure the runtime can reach `api.openai.com`.

> Note: Source similarity is a normalized cosine score in `[0, 1]` from the hashed keyword vectors. Ranking is more meaningful than the raw number.

---

## Troubleshooting and Tips

- Index errors: Ensure the application has write permission for the `data/` directory.
- LLM errors: If using OpenAI, confirm `OPENAI_API_KEY` is set and has available quota.
- Large PDFs: Very large PDFs may create many chunks; consider increasing `CHUNK_SIZE` or reducing upload size.

---

## Future Improvements

- Add unit/integration tests and CI
- Add streaming LLM responses and token-level display
- Better UI for source cards, filtering, and pagination
- Authentication and user management for multi-user deployments
- Support additional LLM backends (local models, Ollama, etc.)

---

