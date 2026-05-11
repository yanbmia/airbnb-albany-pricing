#!/bin/bash
# START_APP.sh - Quick launcher for the Albany Airbnb Dashboard

echo "🏡 Albany Airbnb Pricing & Occupancy Dashboard"
echo "=============================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

# Check if dependencies are installed
echo "📦 Checking dependencies..."
python3 -c "import streamlit; import pandas; import lightgbm; import plotly" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Dependencies not found. Installing..."
    pip install -r requirements.txt
fi

# Check if models exist
if [ ! -d "models" ]; then
    echo "⚠️  Models not found. Training models..."
    python3 model_trainer.py
    if [ $? -ne 0 ]; then
        echo "❌ Model training failed. Check your data files."
        exit 1
    fi
fi

# Start the app
echo ""
echo "✅ All checks passed!"
echo ""
echo "🚀 Starting app at http://localhost:8501"
echo "   Press Ctrl+C to stop"
echo ""

streamlit run app.py
