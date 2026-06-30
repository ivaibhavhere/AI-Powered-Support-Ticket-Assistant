# End-to-End AI System: Support Ticket Assistant

This is an AI-powered system that ingests customer support tickets, allows users to ask natural language questions against the data, and detects anomalies. It was built for the AI Engineer assessment at DOTMappers IT Pvt. Ltd.

## Features
1. **Data Ingestion:** Automatically reads `support_tickets.csv` and loads it into a SQLite database with indexed columns for fast querying.
2. **Natural Language Querying:** Uses LangChain's SQL Agent to translate English questions into SQL, execute them, and return answers.
3. **Anomaly Detection:**
   - **Rule-based:** Identifies Unresolved (Open/Escalated) High & Critical priority tickets older than 24 hours.
   - **Statistical:** Flags tickets with abnormally long resolution times (Z-score > 2.5) grouped by category.
4. **API & UI:** Exposes functionality via a FastAPI REST backend and a Streamlit frontend.

## Architecture Overview
- **Data Layer:** SQLite DB created by Pandas (`data_ingestion.py`).
- **LLM/Agent Layer:** LangChain `create_sql_agent` (`agent.py`) using Groq API (Llama 3) for fast and free text-to-SQL capabilities.
- **Anomaly Detection:** Rule and statistical heuristics implemented in `anomalies.py`.
- **Backend:** FastAPI application (`main.py`) running on `localhost:8000`.
- **Frontend:** Streamlit application (`app.py`) running on `localhost:8501`.

## Setup Instructions

### Prerequisites
- Python 3.9+
- A free Groq API key (from [console.groq.com](https://console.groq.com)) or a Google Gemini API Key.

### 1. Install Dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment
Copy `.env.example` to `.env` and add your API key:
```bash
cp .env.example .env
# Edit .env and paste your GROQ_API_KEY
```

### 3. Ensure Dataset exists
Place your `support_tickets.csv` in the root folder. A small dummy dataset has been provided if you just want to test.

### 4. Run the Application
Start the system with a single command:
```bash
bash start.sh
```
This will:
- Ingest the CSV into `tickets.db`.
- Start the FastAPI backend on `http://localhost:8000` (Swagger UI at `/docs`).
- Start the Streamlit frontend on `http://localhost:8501`.

## Example Queries to Try in the UI
- "How many tickets are currently open?"
- "Show me all Critical tickets not resolved."
- "What is the average response time for Technical category tickets?"
- "Which agent resolved the ticket TKT-001?"

## Known Limitations
- The LangChain Zero-Shot React agent can sometimes hallucinate columns if the prompt isn't highly constrained.
- Statistical anomaly detection requires at least 3 resolved tickets per category to calculate standard deviation.
- Data ingestion is currently set to `replace` the table on every run for simplicity. In production, this should be an upsert pipeline.
