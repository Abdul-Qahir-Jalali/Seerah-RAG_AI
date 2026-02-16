@echo off
echo ============================================================
echo   SEERAH RAG SYSTEM - STARTING SERVERS
echo ============================================================
echo.

echo [1/2] Starting Backend Server (FastAPI)...
start "Backend Server" cmd /k "cd /d "%~dp0" && uv run uvicorn src.api:app --reload"

timeout /t 3 /nobreak > nul

echo [2/2] Starting Frontend Server (Vite)...
start "Frontend Server" cmd /k "cd /d "%~dp0frontend" && npm run dev"

timeout /t 5 /nobreak > nul

echo.
echo ============================================================
echo   SERVERS STARTED SUCCESSFULLY!
echo ============================================================
echo.
echo   Backend API:  http://127.0.0.1:8000
echo   Frontend UI:  http://localhost:5173
echo.
echo   To test the API documentation:
echo   http://127.0.0.1:8000/docs
echo.
echo ============================================================
echo   Press any key to stop all servers...
echo ============================================================

pause > nul

echo.
echo Stopping servers...
taskkill /FI "WindowTitle eq Backend Server*" /T /F > nul 2>&1
taskkill /FI "WindowTitle eq Frontend Server*" /T /F > nul 2>&1

echo Servers stopped.
pause
