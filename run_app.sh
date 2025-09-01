#!/bin/bash

# SaaS Pricing Calculator Launch Script

echo "🚀 Starting SaaS Pricing Calculator..."
echo "=================================="

# Navigate to the project directory
cd /Users/linus/PrisBeregner

# Activate virtual environment and run Streamlit
echo "📦 Activating virtual environment..."
source .venv/bin/activate

echo "🌟 Launching Streamlit app..."
echo "The app will open in your default browser at: http://localhost:8501"
echo ""
echo "To stop the app, press Ctrl+C in this terminal"
echo ""

# Run the Streamlit app from the app files directory
cd "app files"
streamlit run app.py
