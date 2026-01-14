@echo off
echo ========================================
echo AIAG01 - API Testing Suite
echo ========================================
echo.

echo Checking if backend is running...
curl -s http://localhost:8000/api/health >nul 2>&1
if errorlevel 1 (
    echo ERROR: Backend not running!
    echo Please start backend first: cd agentic_system ^&^& py main.py
    pause
    exit /b 1
)

echo ✓ Backend is running
echo.

echo ========================================
echo Test 1: Health Check
echo ========================================
curl http://localhost:8000/api/health
echo.
echo.

echo ========================================
echo Test 2: Get Suppliers
echo ========================================
curl http://localhost:8000/api/suppliers
echo.
echo.

echo ========================================
echo Test 3: Run Analysis Pipeline
echo ========================================
curl -X POST http://localhost:8000/api/analysis/run
echo.
echo.

echo ========================================
echo Test 4: Get Risk Scores
echo ========================================
curl http://localhost:8000/api/risk-scores
echo.
echo.

echo ========================================
echo Test 5: Get Predicted Stock
echo ========================================
curl http://localhost:8000/api/predicted-stock
echo.
echo.

echo ========================================
echo Test 6: Get Alerts
echo ========================================
curl http://localhost:8000/api/alerts
echo.
echo.

echo ========================================
echo Test 7: Get Dashboard Summary
echo ========================================
curl http://localhost:8000/api/dashboard
echo.
echo.

echo ========================================
echo Running Phantom Detection Test
echo ========================================
py test_phantom_detection.py
echo.

echo ========================================
echo All Tests Completed!
echo ========================================
echo.
echo API Documentation: http://localhost:8000/docs
echo.
pause
