@echo off
echo ========================================
echo AIAG01 - Starting Complete System
echo ========================================
echo.

echo [1/2] Starting Backend Server...
start cmd /k "cd agentic_system && py main.py"

timeout /t 3 /nobreak >nul

echo [2/2] Opening Dashboard...
start dashboard\index.html

echo.
echo ========================================
echo System Started Successfully!
echo ========================================
echo.
echo Backend: http://localhost:8000
echo Dashboard: Opened in browser
echo API Docs: http://localhost:8000/docs
echo.
echo Press any key to exit this window...
pause >nul
