@echo off
echo ========================================
echo AIAG01 - Production Deployment Setup
echo ========================================
echo.

set /p BACKEND_URL="Enter your deployed backend URL (e.g., https://aiag01-backend.onrender.com): "

echo.
echo Updating dashboard API URL...

powershell -Command "(Get-Content dashboard\index.html) -replace 'const API_BASE = ''http://localhost:8000/api'';', 'const API_BASE = ''%BACKEND_URL%/api'';' | Set-Content dashboard\index.html"

echo.
echo ========================================
echo API URL Updated Successfully!
echo ========================================
echo.
echo Backend URL: %BACKEND_URL%
echo.
echo Next steps:
echo 1. git add dashboard/index.html
echo 2. git commit -m "Update API URL for production"
echo 3. git push
echo 4. Deploy to Vercel/Netlify
echo.
pause
