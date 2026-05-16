#!/bin/bash

# IntelliTrade AI - Run Script

echo " Starting IntelliTrade AI..."
echo "================================"

# Navigate to streamlit app directory
cd /app/streamlit_app

# Check if requirements are installed
if [ ! -d "venv" ]; then

    echo "Installing dependencies..."

fi

pip install -r requirements.txt
# Run Streamlit app
echo "Launching Streamlit app..."
echo "Access the app at: http://localhost:8501"
echo "================================"

streamlit run app.py --server.port=8501 --server.address=0.0.0.0