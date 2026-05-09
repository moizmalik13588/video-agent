# 🎙️ AI Meeting Assistant — Video Agent

> Transform long meetings into structured, actionable insights using local and cloud AI models.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-0.x-1C3C3C?style=flat-square&logo=langchain&logoColor=white)
![Mistral AI](https://img.shields.io/badge/Mistral_AI-small--latest-FF7000?style=flat-square)
![Whisper](https://img.shields.io/badge/OpenAI-Whisper-412991?style=flat-square&logo=openai&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-10b950?style=flat-square)

---

## 📌 Overview

**AI Meeting Assistant** is a production-grade, end-to-end AI pipeline that ingests meeting recordings — from YouTube URLs or local files — and automatically produces:

- 📋 A professional meeting **summary**
- ✅ Extracted **action items** with owners & deadlines
- 🔑 Key **decisions** made during the meeting
- ❓ **Open questions** and unresolved topics
- 💬 A **RAG-powered chat interface** to query the meeting transcript

Built with LangChain, Mistral AI, OpenAI Whisper, Sarvam AI (for Hinglish), ChromaDB, and Streamlit.

---

## 🧠 Architecture

```
Input (YouTube URL / Local File)
        │
        ▼
┌─────────────────────┐
│  Audio Processing   │  yt-dlp → WAV → 10-min chunks
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│    Transcription    │  Whisper (English) / Sarvam AI (Hinglish→English)
└─────────────────────┘
        │
        ▼
┌──────────────────────────────────────────────┐
│              LangChain Pipeline              │
│  ┌──────────┐ ┌──────────┐ ┌─────────────┐  │
│  │ Summary  │ │ Actions  │ │  Decisions  │  │
│  └──────────┘ └──────────┘ └─────────────┘  │
│  ┌──────────────────────────────────────┐   │
│  │   RAG Chain (ChromaDB + Retriever)   │   │
│  └──────────────────────────────────────┘   │
└──────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────┐
│   Streamlit UI      │  Modern dark green theme
└─────────────────────┘
```

---

## 🚀 Features

| Feature | Description |
|---|---|
| 🎥 YouTube Ingestion | Download and process any YouTube meeting/lecture URL |
| 📁 Local File Support | Process MP4, MP3, WAV, and other audio/video formats |
| 🗣️ Dual Transcription | Whisper (local) for English, Sarvam AI for Hinglish→English |
| 📝 Map-Reduce Summarization | Handles long transcripts via chunked summarization |
| ✅ Action Item Extraction | Structured output with owner and deadline |
| 🔑 Decision Extraction | Key decisions made during the meeting |
| ❓ Open Questions | Unresolved topics flagged for follow-up |
| 💬 RAG Chat | Ask anything about the meeting using vector search |
| 🖥️ Modern UI | Streamlit frontend with custom dark green theme |

---

## 🗂️ Project Structure

```
video-agent/
│
├── app.py                  # Streamlit UI (main entry point)
├── main.py                 # Core pipeline orchestrator
│
├── core/
│   ├── transcriber.py      # Whisper + Sarvam AI transcription routing
│   ├── summarizer.py       # Map-reduce summarization via Mistral
│   ├── extractor.py        # Action items, decisions, questions extraction
│   ├── rag_engine.py       # LangChain RAG chain (build + query)
│   └── vector_store.py     # ChromaDB vector store management
│
├── utils/
│   └── audio_processing.py # yt-dlp download, WAV conversion, chunking
│
├── vector_db/              # Persisted ChromaDB embeddings (auto-created)
├── downloades/             # Downloaded audio cache (auto-created)
│
├── .env                    # API keys (not committed)
├── Requirements.txt        # Python dependencies
└── README.md
```

---

## ⚙️ Setup & Installation

### Prerequisites

- Python 3.10+
- [FFmpeg](https://ffmpeg.org/download.html) installed and in PATH
- Mistral AI API key
- (Optional) Sarvam AI API key for Hinglish support

### 1. Clone the repository

```bash
git clone https://github.com/moizmalik13588/video-agent.git
cd video-agent
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r Requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
# Required
MISTRAL_API_KEY=your_mistral_api_key_here

# Optional — required for Hinglish transcription
SARVAM_API_KEY=your_sarvam_api_key_here

# Optional — Whisper model size: tiny | base | small | medium | large
WHISPER_MODEL=small

# Optional — Sarvam STT model version
SARVAM_STT_MODEL=saaras:v2.5
```

### 5. Run the Streamlit app

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 🖥️ CLI Usage

You can also run the pipeline directly from the terminal without the UI:

```bash
python main.py
```

You will be prompted to enter a YouTube URL or local file path, then the language. Results are printed to the terminal, followed by an interactive chat session.

---

## 🔑 API Keys

| Service | Purpose | Get Key |
|---|---|---|
| [Mistral AI](https://console.mistral.ai/) | Summarization, extraction, RAG | Required |
| [Sarvam AI](https://www.sarvam.ai/) | Hinglish → English transcription | Optional |

Whisper runs **locally** — no API key required.

---

## 🧩 Models Used

| Task | Model | Provider |
|---|---|---|
| Transcription (English) | `whisper-small` (configurable) | Local / OpenAI Whisper |
| Transcription (Hinglish) | `saaras:v2.5` | Sarvam AI |
| Summarization | `mistral-small-latest` | Mistral AI |
| Action/Decision Extraction | `mistral-small-latest` | Mistral AI |
| RAG Q&A | `mistral-small-latest` | Mistral AI |
| Embeddings | `all-MiniLM-L6-v2` | HuggingFace (local) |
| Vector Store | ChromaDB | Local |

---

## 📦 Key Dependencies

```
streamlit
langchain
langchain-mistralai
langchain-chroma
langchain-community
langchain-text-splitters
openai-whisper
sentence-transformers
chromadb
yt-dlp
pydub
python-dotenv
requests
```

---

## 🔄 Pipeline Flow

1. **Input** — User provides a YouTube URL or local audio/video file
2. **Audio Processing** — `yt-dlp` downloads YouTube audio; `pydub` converts to mono 16kHz WAV and splits into 10-minute chunks
3. **Transcription** — Each chunk is transcribed using Whisper (English) or Sarvam AI (Hinglish→English translation)
4. **Summarization** — Transcript is chunked (3000 tokens) and summarized via map-reduce using Mistral
5. **Extraction** — Action items, key decisions, and open questions are extracted using targeted prompts
6. **RAG Indexing** — Transcript is embedded using `all-MiniLM-L6-v2` and stored in ChromaDB
7. **Chat** — Users can ask natural language questions; retrieved context is passed to Mistral for grounded answers

---

## ⚠️ Known Limitations

- Sarvam AI sync API has a 30-second audio limit per request — the pipeline automatically splits chunks into 25-second pieces
- Very long meetings (3+ hours) may take several minutes to process
- Whisper accuracy depends on audio quality and background noise
- ChromaDB is persisted locally in `vector_db/` — re-running with a new meeting will overwrite the previous index

---

## 🛣️ Roadmap

- [ ] Speaker diarization (who said what)
- [ ] Multi-meeting history and search
- [ ] Export results to PDF/Notion
- [ ] Docker containerization
- [ ] REST API backend (FastAPI)
- [ ] React frontend migration

---

## 👨‍💻 Author

**Moiz Malik**
[GitHub](https://github.com/moizmalik13588) · [LinkedIn](https://linkedin.com/in/moizmalik)

---

## 📄 License

MIT License — feel free to use, modify, and distribute.
