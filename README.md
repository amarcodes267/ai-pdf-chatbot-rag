# AI PDF Chatbot (RAG)

A professional, production-minded Retrieval-Augmented Generation (RAG) demo built with Streamlit.

This repository provides a lightweight pipeline to:

- Upload one or more PDF documents
- Extract and clean text from PDFs (page-level)
- Split text into overlapping chunks with metadata (document, page, chunk)
- Generate semantic embeddings (SentenceTransformers)
- Persist embeddings and metadata in a ChromaDB vector store
- Perform semantic retrieval and produce grounded answers using an LLM (OpenAI optional)
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
- Embeddings via `sentence-transformers` (`all-MiniLM-L6-v2` by default)
- Persistence using ChromaDB (local persistent store in `data/chroma_db`)
- Semantic search and retrieval with source metadata and similarity scores
- Optional LLM generation using OpenAI (fallback summary available if not configured)
- Streamlit UI with conversation history, loading states, and error handling

---

## Architecture

The app follows a simple, modular pipeline:

PDF Upload → PDF Extraction (page-level) → Text Cleaning → Chunking → Embeddings → Vector Store (ChromaDB) → Retrieval → Prompting → LLM → Answer + Sources

Key modules are under `services/` and the UI components under `components/` with an overall `chat_ui.py` that coordinates the workflow.

---

## Tech Stack

- Python 3.11+
- Streamlit (UI)
- PyMuPDF (`fitz`) for PDF extraction
- LangChain text splitters (for chunking)
- Sentence Transformers for embeddings
- ChromaDB for vector storage
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
	- `embedding_service.py` — sentence-transformers embeddings
	- `vector_store.py` — ChromaDB wrapper (add/search/clear)
	- `retrieval_service.py` — query embedding + search wrapper
	- `rag_service.py` — retrieval + LLM orchestration
	- `llm_service.py` — LLM adapter (OpenAI optional fallback)
	- `chat_service.py` — Streamlit session-based chat history
- `data/` — stores `uploads/` and `chroma_db/` (persistent vector store)
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

Notes: Some packages (embedding models) will download model data at first run; ensure you have network access and sufficient disk space.

---

## Configuration and Environment Variables

The application uses environment variables to configure optional LLM behavior.

- `OPENAI_API_KEY` — Set this if you want the app to use OpenAI for responses. If omitted, a local deterministic fallback summary is used.
- `OPENAI_MODEL` — (optional) override the chat model (default `gpt-3.5-turbo`).

A template is provided in `.env.example`. Secrets are read from environment variables only — never hardcode them in source files. The `.env` file is gitignored.

ChromaDB persists data under `data/chroma_db` by default. Uploaded PDFs are stored in `data/uploads`. Both directories are regenerated at runtime and are gitignored (they are not part of the repository).

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

- **Ephemeral filesystem:** Render's native Python runtime does not persist files between deploys/restarts. Uploaded PDFs and the ChromaDB store in `data/` are recreated at runtime and **do not survive a redeploy**. Vector data must be re-ingested after each deploy.
- **Memory:** Loading the `all-MiniLM-L6-v2` embedding model plus ChromaDB needs roughly 1 GB RAM. The free plan (~512 MB) may restart under load; prefer the **Starter** plan or higher.
- **First build** downloads the embedding model (~90 MB), which can take several minutes — this is normal.
- **Health check:** `/_stcore/health` (Streamlit's built-in endpoint) is used so Render probes the running server.

---

## How the RAG Pipeline Works

1. PDF extraction: Each PDF is parsed page-by-page (PyMuPDF). Page texts are cleaned with `text_cleaner.py`.
2. Chunking: Each page is split into overlapping chunks using LangChain text splitters; metadata (source filename, page number, chunk index) is attached.
3. Embeddings: Chunks are converted to vector embeddings with SentenceTransformers.
4. Vector store: ChromaDB stores vectors, documents (the chunk text), and metadata for retrieval.
5. Retrieval: When the user asks a question, the question is embedded and used to query ChromaDB for the top-K similar chunks.
6. Prompting & LLM: Retrieved chunks are combined into a context and sent to the configured LLM (OpenAI by default). If no LLM is configured, a fallback summary is returned.
7. Sources: The app displays the retrieved chunks and their metadata alongside the answer so users can verify the citation.

---

## Testing

Basic tests to run manually:

1. Start the app and upload a small PDF (one or two pages).
2. Process the PDF and verify `data/uploads` and `data/chroma_db` contain artifacts.
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
- **File storage:** uploaded PDFs are written to `data/uploads`. On serverless/ephemeral filesystems, persisted PDFs are not kept across restarts — the ChromaDB index (which holds the chunk text) is the source of truth for retrieval.
- **ChromaDB persistence:** the vector store lives in `data/chroma_db`. This directory must be writable and persistent across restarts for stored documents to survive. It is local-only; multi-user/true serverless deployments should move to a remote ChromaDB backend or re-ingest documents per session.
- **Embedding model:** `all-MiniLM-L6-v2` is downloaded on first run (network + ~90 MB disk) and loaded into memory (~0.5 GB with the sentence-transformers stack).
- **Memory:** loading the embedding model plus ChromaDB requires roughly 1 GB RAM. For cloud platforms, request adequate memory.
- **LLM requirement:** OpenAI access (network + valid key) is required for production-quality answers. Ensure the runtime can reach `api.openai.com`.

> Note: The source `similarity` value displayed in the UI is a normalized score in `[0, 1]` derived from ChromaDB's distance (higher = more relevant). ChromaDB's default metric is squared-L2, so the ranking (not the raw number) is the meaningful signal.

---

## Troubleshooting and Tips

- Slow embedding/model loading: The `sentence-transformers` model will download on first run. This can take time and disk space.
- ChromaDB errors: If the vector store cannot initialize, ensure you have write permissions to `data/chroma_db` and no file locks.
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

