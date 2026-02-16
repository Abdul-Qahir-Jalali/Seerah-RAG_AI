# How to Run and Test the Seerah RAG System

## Prerequisites Check
Before starting, verify:
- ✅ Groq API key is set in `.env` file
- ✅ Data ingestion completed (47,179 documents)
- ✅ ChromaDB database exists in `./data/chroma_db/`

---

## Step 1: Start the Backend Server

### Open Terminal 1 (Backend)
```bash
# Navigate to project root
cd "e:\gmal project"

# Start the FastAPI backend
uv run uvicorn src.api:app --reload
```

### Expected Output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**✅ Checkpoint**: Backend should be running on **http://127.0.0.1:8000**

---

## Step 2: Start the Frontend Server

### Open Terminal 2 (Frontend)
```bash
# Navigate to frontend directory
cd "e:\gmal project\frontend"

# Start Vite development server
npm run dev
```

### Expected Output:
```
VITE v6.4.1  ready in 1508 ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

**✅ Checkpoint**: Frontend should be running on **http://localhost:5173/**

---

## Step 3: Test the API (Optional - Using Terminal 3)

### Test 1: Health Check
```bash
curl http://localhost:8000/api/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "vector_store_status": "initialized",
  "document_count": 47179
}
```

### Test 2: Get Statistics
```bash
curl http://localhost:8000/api/stats
```

**Expected Response:**
```json
{
  "total_documents": 47179,
  "collections": ["seerah_collection"],
  "embedding_model": "sentence-transformers/all-MiniLM-L6-v2"
}
```

### Test 3: Ask a Question
```bash
curl -X POST http://localhost:8000/api/query -H "Content-Type: application/json" -d "{\"question\": \"What are the five pillars of Islam?\"}"
```

**Expected Response:**
```json
{
  "answer": "The five pillars of Islam are:\n\n1. Shahada (testimony of faith)...",
  "sources": [
    {
      "content": "...",
      "metadata": {
        "collection": "Sahih al-Bukhari",
        "chapter": "Belief",
        ...
      }
    }
  ]
}
```

---

## Step 4: Test the Frontend Chat Interface

### Access the Application
1. Open your web browser
2. Navigate to: **http://localhost:5173/**

### Test Questions
Try asking these questions in the chat interface:

**Basic Questions:**
- "What are the five pillars of Islam?"
- "What did the Prophet say about good manners?"

**Prayer Related:**
- "How many times should a Muslim pray daily?"
- "What is the importance of prayer in Ramadan?"

**Quran Related:**
- "What does the Quran say about patience?"
- "What is the first revelation to Prophet Muhammad?"

**Hadith Related:**
- "What is the reward for fasting in Ramadan?"
- "What are the signs of a hypocrite?"

### What to Check:
✅ Chat interface loads properly  
✅ Questions are sent and received  
✅ Answers appear with proper formatting  
✅ Source citations are displayed  
✅ Clicking sources expands to show details  
✅ Arabic text displays correctly (if available)

---

## Step 5: Verify Response Quality

### Good Response Characteristics:
- ✅ Answer is directly from Hadith/Quran context
- ✅ No hallucinations or made-up information
- ✅ Sources are properly cited with:
  - Collection name (e.g., "Sahih al-Bukhari")
  - Chapter title
  - Narrator name
  - Hadith ID or Verse reference
- ✅ If answer not found, says "I don't have enough information..."

---

## Troubleshooting

### Backend Issues

**Problem**: `Connection refused` error
```bash
# Solution: Ensure backend is running
# Check if process is active on port 8000
netstat -ano | findstr :8000
```

**Problem**: `ModuleNotFoundError`
```bash
# Solution: Sync UV dependencies
uv sync
```

**Problem**: `GROQ_API_KEY not found`
```bash
# Solution: Check your .env file
type .env
# Ensure it contains: GROQ_API_KEY=your-key-here
```

### Frontend Issues

**Problem**: `Cannot GET /`
```bash
# Solution: Ensure Vite is running
# Check terminal for errors
# Try restarting: npm run dev
```

**Problem**: API calls fail (CORS errors)
```bash
# Solution: Ensure Vite proxy is configured
# Check frontend/vite.config.js contains proxy settings
```

### Performance Issues

**Problem**: Slow responses (> 10 seconds)
- Check your internet connection (Groq API calls)
- Verify ChromaDB is not rebuilding index
- Consider switching to faster LLM model

---

## Quick Reference

| Component   | URL                        | Location   |
| ----------- | -------------------------- | ---------- |
| Backend API | http://127.0.0.1:8000      | Terminal 1 |
| Frontend UI | http://localhost:5173/     | Terminal 2 |
| API Docs    | http://127.0.0.1:8000/docs | Browser    |

### Stop Servers
- **Backend**: Press `Ctrl+C` in Terminal 1
- **Frontend**: Press `Ctrl+C` in Terminal 2

---

## Success Criteria

Your system is working correctly if:
1. ✅ Both servers start without errors
2. ✅ Health check returns document_count: 47179
3. ✅ Frontend loads at http://localhost:5173/
4. ✅ Questions get relevant answers with sources
5. ✅ No hallucinations in responses
6. ✅ Arabic text displays properly

**You're ready to use the Seerah RAG system!** 🌙
