#!/bin/bash

echo "🚀 Starting AI Support Ticket Analysis System"

# Check for .env file
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Copying .env.example to .env..."
    cp .env.example .env
fi

# Ingest data
echo "📊 Ingesting CSV data into SQLite..."
python3 data_ingestion.py

# Start FastAPI in the background
echo "🔌 Starting FastAPI Backend..."
uvicorn main:app --host 0.0.0.0 --port 8000 &
FASTAPI_PID=$!

# Wait for API to initialize
sleep 3

# Start Streamlit
echo "🖥️  Starting Streamlit Frontend..."
streamlit run app.py --server.port 8501

# Trap Ctrl+C to kill background processes
trap "kill $FASTAPI_PID; exit" INT TERM
