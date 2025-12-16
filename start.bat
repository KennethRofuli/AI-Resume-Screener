@echo off
echo ========================================
echo   AI Resume Screener - Startup Script
echo ========================================
echo.

REM Start Backend API
echo Starting Backend API...
start "Backend API" cmd /k "cd /d "%~dp0backend" && ..\venv\Scripts\activate && python api.py"

REM Wait a moment for backend to start
timeout /t 3 /nobreak > nul

REM Start Frontend
echo Starting Frontend...
start "Frontend React" cmd /k "cd /d "%~dp0frontend" && npm start"

echo.
echo ========================================
echo Both servers are starting!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo ========================================
echo.
pause
