# Seerah RAG - Islamic Q&A System 🕌

Modern RAG-based Question Answering system for Islamic texts powered by Groq AI, featuring 9 major Hadith collections and the Quran.

## ✨ Features

- 🤖 **Groq AI Integration** - Lightning-fast responses using Llama 3.3 70B
- 📚 **Rich Islamic Database** - 9 Hadith collections + Complete Quran
- 🎯 **No Hallucinations** - Answers only from authentic sources
- 📖 **Source Citations** - Every answer includes references
- 🌙 **Beautiful UI** - Modern dark theme with glassmorphism
- ⚡ **Fast Retrieval** - ChromaDB vector database for instant search
- 🔍 **Semantic Search** - Advanced embedding-based retrieval

## 📦 Tech Stack

**Backend:**
- **LLM**: Groq API (Llama 3.3 70B)
- **Vector DB**: ChromaDB
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **Framework**: FastAPI
- **Package Manager**: UV (modern Python package management)

**Frontend:**
- **Framework**: React 18 + Vite 6
- **Styling**: Tailwind CSS 3
- **Icons**: Lucide React
- **HTTP Client**: Axios

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- UV package manager
- Groq API key (free at [console.groq.com](https://console.groq.com))

### Installation

#### 1. Install UV (if not already installed)

**Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### 2. Clone and Setup Backend

```bash
cd "e:\gmal project"

# Create .env file from template
Copy-Item .env.example .env

# Edit .env and add your Groq API key
# GROQ_API_KEY=your_actual_api_key_here

# Sync dependencies (UV will create virtual environment automatically)
uv sync
```

#### 3. Ingest Data

This loads all Hadith collections and Quran into ChromaDB (takes 5-10 minutes):

```bash
uv run python scripts/ingest_data.py
```

You should see:
```
✓ Loaded X hadiths from Bukhari
✓ Loaded X hadiths from Muslim
...
✓ Loaded X verses from Quran
✅ Total documents loaded: XXXX
```

#### 4. Start Backend Server

```bash
uv run uvicorn src.api:app --reload --port 8000
```

Server runs at: `http://localhost:8000`

API docs available at: `http://localhost:8000/docs`

#### 5. Setup and Start Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend runs at: `http://localhost:5173`

## 📖 Usage

### Web Interface

1. Open `http://localhost:5173` in your browser
2. Type your question in the input box
3. Get instant answers with source citations
4. Click on sources to see full Hadith/Quran text with Arabic

### Example Questions

- "What are the pillars of Islam?"
- "Tell me about the first revelation to Prophet Muhammad"
- "What does Surah Al-Fatiha say?"
- "Describe the Battle of Badr"
- "What are the signs of a hypocrite?"

### API Usage

**Query Endpoint:**
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the pillars of Islam?"}'
```

**Health Check:**
```bash
curl http://localhost:8000/api/health
```

**Statistics:**
```bash
curl http://localhost:8000/api/stats
```

## 🏗️ Project Structure

```
e:\gmal project\
├── data/
│   ├── ahadees/          # 9 Hadith collections (JSON)
│   └── quran/            # Quran with translation (JSON)
├── src/
│   ├── config.py         # Configuration management
│   ├── data_ingestion.py # Data loading and parsing
│   ├── embeddings.py     # Embedding generation
│   ├── vector_store.py   # ChromaDB management
│   ├── llm.py           # Groq LLM integration
│   ├── rag_pipeline.py  # Complete RAG orchestration
│   └── api.py           # FastAPI server
├── scripts/
│   └── ingest_data.py   # Data ingestion script
├── frontend/
│   ├── src/
│   │   ├── App.jsx      # Main app component
│   │   ├── components/  # React components
│   │   └── index.css    # Tailwind styles
│   └── package.json
├── chroma_db/           # Vector database (created after ingestion)
├── pyproject.toml       # UV dependencies
└── .env                 # Environment variables
```

## 🔧 Configuration

Edit `.env` file to customize:

```env
# Groq API
GROQ_API_KEY=your_groq_api_key_here

# Models
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
LLM_MODEL=llama-3.3-70b-versatile
LLM_TEMPERATURE=0.1

# Database
CHROMA_DB_PATH=./chroma_db
CHROMA_COLLECTION_NAME=seerah_collection

# API
API_HOST=0.0.0.0
API_PORT=8000
```

## 📊 Data Sources

### Hadith Collections (9)
1. Sahih al-Bukhari
2. Sahih Muslim
3. Sunan Abu Dawud
4. Jami` at-Tirmidhi
5. Sunan an-Nasa'i
6. Sunan Ibn Majah
7. Muwatta Malik
8. Musnad Ahmad
9. Sunan ad-Darimi

### Quran
- Complete English translation
- Arabic text included
- Organized by Surah and Verse

## 🎨 UI Features

- **Glassmorphism Design** - Modern frosted glass effect
- **Dark Theme** - Islamic-inspired emerald/teal palette
- **Responsive Layout** - Works on mobile and desktop
- **Smooth Animations** - Elegant transitions
- **Source Cards** - Expandable citations with Arabic text
- **Real-time Loading** - Visual feedback during queries

## 🐛 Troubleshooting

**Issue: "Could not load Groq API key"**
- Make sure `.env` file exists and contains `GROQ_API_KEY`
- Restart the server after updating `.env`

**Issue: "No documents found in ChromaDB"**
- Run the ingestion script: `uv run python scripts/ingest_data.py`

**Issue: "Frontend can't connect to backend"**
- Ensure backend is running on port 8000
- Check Vite proxy configuration in `frontend/vite.config.js`

**Issue: "UV command not found"**
- Install UV: `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"`
- Restart your terminal

## 📝 Development

### Adding More Data

1. Add JSON files to `data/ahadees/` or `data/quran/`
2. Update `data_ingestion.py` if needed
3. Re-run ingestion: `uv run python scripts/ingest_data.py`

### Modifying UI

Edit files in `frontend/src/`:
- `App.jsx` - Main layout and logic
- `components/ChatMessage.jsx` - Message display
- `components/SourceCard.jsx` - Source citations
- `index.css` - Styles and animations

### Changing LLM Model

Edit `.env`:
```env
LLM_MODEL=llama-3.1-70b-versatile  # or other Groq models
```

Available Groq models:
- `llama-3.3-70b-versatile` (recommended)
- `llama-3.1-70b-versatile`
- `mixtral-8x7b-32768`

## 📄 License

This project is for educational purposes. Islamic texts are public domain.

## 🙏 Acknowledgments

- Groq for providing fast LLM inference
- OpenAI for embedding models
- ChromaDB for vector storage
- All contributors to Islamic text digitization

---

**Built with ❤️ for the Muslim community**
