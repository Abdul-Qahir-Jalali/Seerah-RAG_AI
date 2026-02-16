# Quick Start Guide - One Command Setup

## Start Everything with ONE Command

### Step 1: Run the Startup Script
Double-click on **`start.bat`** in the project folder

OR open PowerShell/Command Prompt and run:
```bash
cd "e:\gmal project"
start.bat
```

### Step 2: Wait for Servers to Start
Two terminal windows will open:
- **Backend Server** (black terminal)
- **Frontend Server** (another terminal)

Wait about 10-15 seconds for both to fully start.

### Step 3: Open Your Browser
Once both servers are ready, open your browser and go to:

**http://localhost:5173/**

### Step 4: Test the System
Try asking these questions:
- "What are the five pillars of Islam?"
- "What did the Prophet say about good manners?"
- "What is the reward for fasting in Ramadan?"

---

## Stop Everything

Go to the **original terminal** where you ran `start.bat` and press **any key**. 

This will stop both servers automatically.

---

## URLs Reference

| Service                       | URL                        |
| ----------------------------- | -------------------------- |
| **Frontend (Chat Interface)** | http://localhost:5173/     |
| **Backend API**               | http://127.0.0.1:8000      |
| **API Documentation**         | http://127.0.0.1:8000/docs |

---

## Troubleshooting

**Problem**: Terminals close immediately
- Open PowerShell and run: `cd "e:\gmal project"` then `.\start.bat`
- Check for error messages

**Problem**: "Port already in use"
- Close any existing servers running on ports 8000 or 5173
- Run: `taskkill /F /IM node.exe` and `taskkill /F /IM python.exe`
- Try again

**Problem**: Backend won't start
- Ensure `.env` file has your GROQ_API_KEY
- Run: `uv sync` to update dependencies

---

That's it! You now have a one-command startup for your entire RAG system. 🚀
