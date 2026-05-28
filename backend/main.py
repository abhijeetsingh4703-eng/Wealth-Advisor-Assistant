from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, List

from backend.models.schemas import HitlReviewDecision
from backend.agents.orchestrator import OrchestratorAgent
from backend.memory.short_term import memory_store
from backend.memory.long_term import long_term_store
from backend.logger import logger
import uvicorn

app = FastAPI(title="Wealth Advisor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = OrchestratorAgent()

@app.get("/api/clients")
def get_clients():
    """Get list of mock clients"""
    import json, os
    base_dir = os.path.dirname(__file__)
    with open(os.path.join(base_dir, "mock_data", "clients.json"), "r") as f:
        return json.load(f)

@app.post("/api/analyze/{client_id}")
def start_analysis(client_id: str):
    """Start the multi-agent workflow for a client"""
    session_id = memory_store.create_session()
    logger.info(f"Started analysis for client {client_id}", extra={"session_id": session_id})
    
    try:
        result = orchestrator.execute(session_id, {"client_id": client_id})
        return result
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}", extra={"session_id": session_id})
        memory_store.set_status(session_id, "error")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/hitl/review")
def review_anomalies(decisions: List[HitlReviewDecision]):
    """Human-in-the-loop endpoint to review flagged anomalies"""
    if not decisions:
        raise HTTPException(status_code=400, detail="No decisions provided")
        
    session_id = decisions[0].session_id
    session = memory_store.get_session(session_id)
    
    if not session or session["status"] != "awaiting_review":
         raise HTTPException(status_code=400, detail="Invalid session or not awaiting review")

    analysis = session["context"]["analysis"]
    
    for decision in decisions:
        for anomaly in analysis["anomalies"]:
            if anomaly["transaction_id"] == decision.transaction_id:
                anomaly["is_approved"] = decision.is_approved
                logger.info(f"HITL Decision: Transaction {decision.transaction_id} approved: {decision.is_approved}", extra={"session_id": session_id})


    memory_store.update_context(session_id, "analysis", analysis)
    
    result = orchestrator.resume_workflow(session_id)
    return result

@app.get("/api/session/{session_id}")
def get_session_status(session_id: str):
    """Get real-time status and logs of a session"""
    session = memory_store.get_session(session_id)
    if not session:
         raise HTTPException(status_code=404, detail="Session not found")
    return session

@app.get("/api/history/{client_id}")
def get_history(client_id: str):
    """Get long term history from SQLite"""
    return long_term_store.get_client_history(client_id)

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
