# Seerah RAG System - Islamic Q&A Assistant 🕌

An intelligent Question-Answering system for Islamic texts using Retrieval-Augmented Generation (RAG). Query authentic Hadith collections and Quran with AI-powered responses and precise source citations.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-green.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-teal.svg)
![React](https://img.shields.io/badge/React-18+-blue.svg)

## 🌟 Features

- **Zero Hallucination**: Answers strictly from authentic Islamic sources
- **Source Citations**: Every response includes detailed references with Arabic text
- **47,000+ Documents**: 9 Hadith collections + Quran (English translation)
- **Modern UI**: Beautiful dark-themed interface with glassmorphism effects
- **Token-Efficient**: Uses Groq's `llama-3.1-8b-instant` model
- **Fast Retrieval**: ChromaDB vector database for semantic search
- **RESTful API**: Easy integration with other applications

## 📚 Data Sources

### Hadith Collections
- Sahih al-Bukhari (~7,563 hadiths)
- Sahih Muslim (~7,563 hadiths)
- Sunan Abu Dawood (~5,274 hadiths)
- Jami` at-Tirmidhi (~3,956 hadiths)
- Sunan an-Nasa'i (~5,758 hadiths)
- Sunan Ibn Majah (~4,341 hadiths)
- Muwatta Malik (~1,849 hadiths)
- Musnad Ahmad (~27,647 hadiths)
- Sunan al-Darimi (~3,567 hadiths)

### Quran
- Complete English translation (6,236 verses)
- Arabic text included in responses

**Total**: 47,179 documents

## 🛠️ Tech Stack

### Backend
- **FastAPI** - High-performance web framework
- **LangChain** - RAG orchestration
- **ChromaDB** - Vector database
- **Groq API** - LLM inference (llama-3.1-8b-instant)
- **Sentence Transformers** - Embeddings (all-MiniLM-L6-v2)
- **UV** - Fast Python package manager

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Axios** - HTTP client

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- UV package manager
- Groq API key ([Get one free](https://console.groq.com))

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Abdul-Qahir-Jalali/Seerah-RAG_AI.git
cd Seerah-RAG_AI
```

2. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

3. **Download Islamic data** (Hadith & Quran JSON files)
```
Place your JSON data files in:
- data/ahadees/ (9 Hadith collection files)
- data/quran/ (Quran translation file)
```

4. **Install backend dependencies**
```bash
uv sync
```

5. **Install frontend dependencies**
```bash
cd frontend
npm install
cd ..
```

6. **Ingest data into vector database**
```bash
uv run python scripts/ingest_data.py
```
*This will process 47,000+ documents and may take 30-45 minutes.*

7. **Start the servers**
```bash
# Option 1: One-command startup (Windows)
start.bat

# Option 2: Manual startup
# Terminal 1 - Backend
uv run uvicorn src.api:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

8. **Open your browser**
```
http://localhost:5173/
```

## 📖 Usage

### Example Questions

✅ **Specific Queries Work Best:**
- "What did the Prophet say about prayer?"
- "What is the importance of fasting in Ramadan?"
- "What does the Quran say about patience?"
- "What is the reward for charity?"
- "What did the Prophet say about good manners?"

❌ **Avoid Very Broad Questions:**
- "Explain Islamic jurisprudence" (too broad)
- "What are the five pillars?" (may not be explicitly listed together in sources)

### API Endpoints

#### Health Check
```bash
GET /api/health
```

#### Query
```bash
POST /api/query
Content-Type: application/json

{
  "question": "What did the Prophet say about prayer?"
}
```

#### Statistics
```bash
GET /api/stats
```

## 🎨 Screenshots

*Coming soon - Add screenshots of your UI here*

## 📁 Project Structure

```
Seerah-RAG_AI/
├── src/
│   ├── api.py              # FastAPI server
│   ├── config.py           # Configuration
│   ├── data_ingestion.py   # Data loading
│   ├── embeddings.py       # Embedding generator
│   ├── llm.py              # Groq LLM integration
│   ├── rag_pipeline.py     # RAG orchestration
│   └── vector_store.py     # ChromaDB manager
├── scripts/
│   └── ingest_data.py      # Data ingestion script
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # Main chat interface
│   │   └── components/     # React components
│   └── package.json
├── data/                   # Data files (not in repo)
│   ├── ahadees/            # Hadith collections
│   ├── quran/              # Quran translation
│   └── chroma_db/          # Vector database (auto-generated)
├── .env.example            # Environment template
├── pyproject.toml          # Python dependencies
├── start.bat               # One-command startup (Windows)
└── README.md
```

## ⚙️ Configuration

Edit `.env` file:

```env
# Groq API
GROQ_API_KEY=your_api_key_here

# LLM Configuration
LLM_MODEL=llama-3.1-8b-instant
LLM_TEMPERATURE=0.1

# Vector Store
CHROMA_PATH=./data/chroma_db
CHROMA_COLLECTION_NAME=seerah_collection

# Embeddings
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

## 🔒 Security

- `.env` file excluded from git (contains API keys)
- Data files excluded (large JSON files)
- ChromaDB excluded (generated locally)
- Always use `.env.example` as template

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Hadith data from authentic Islamic sources
- Quran translation data
- Groq for providing fast LLM inference
- LangChain for RAG framework
- ChromaDB for vector storage

## 📧 Contact

Abdul Qahir Jalali - [@Abdul-Qahir-Jalali](https://github.com/Abdul-Qahir-Jalali)

Project Link: [https://github.com/Abdul-Qahir-Jalali/Seerah-RAG_AI](https://github.com/Abdul-Qahir-Jalali/Seerah-RAG_AI)

---

**Note**: This system prioritizes accuracy over completeness. If a specific answer isn't found in the sources, the AI will honestly say so rather than hallucinate. This is a feature, not a bug! 🌙
