from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import os

from anomalies import get_anomalies
from agent import query_agent

app = FastAPI(title="AI Support Ticket Analysis API")

class QueryRequest(BaseModel):
    question: str

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "1.0.0"}

@app.get("/anomalies")
def detect_anomalies():
    """
    Returns detected anomalies in the dataset.
    """
    try:
        anomalies = get_anomalies()
        if "error" in anomalies:
            raise HTTPException(status_code=500, detail=anomalies["error"])
        return anomalies
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
def process_query(req: QueryRequest):
    """
    Accepts natural language questions and returns AI-generated answers.
    """
    if not req.question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")
        
    answer = query_agent(req.question)
    return {"question": req.question, "answer": answer}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
