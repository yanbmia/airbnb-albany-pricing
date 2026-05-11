@echo off
REM START_APP.bat - Quick launcher for Windows

echo.
echo 🏡 Albany Airbnb Pricing 6 Occupancy Dashboard
echo ==============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.8+
    exit /b 1
)

REM Check if dependencies are installed
echo 📦 Checking dependencies...
python -c "import streamlit; import pandas; import lightgbm; import plotly" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Dependencies not found. Installing...
    pip install -r requirements.txt
)

REM Check if models exist
if not exist "models\" (
    echo ⚠️  Models not found. Training models...
    python model_trainer.py
    if errorlevel 1 (
        echo ❌ Model training failed. Check your data files.
        exit /b 1
    )
)

echo.
echo ✅ All checks passed!
echo.
echo 🚀 Starting app at http://localhost:8501
echo    Press Ctrl+C to stop
echo.

streamlit run app.py
