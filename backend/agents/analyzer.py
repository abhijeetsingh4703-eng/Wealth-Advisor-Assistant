from typing import Any, Dict
from .base_agent import BaseAgent
from backend.tools.tool_registry import registry
from backend.tools.anomaly_detector import detect_anomalies

registry.register("detect_anomalies", detect_anomalies)

class AnalyzerAgent(BaseAgent):
    def __init__(self, memory_store=None):
        super().__init__(name="Analyzer", memory_store=memory_store)

    def execute(self, session_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        self.log_action(session_id, "Analyzing client portfolio and transactions")
        
        profile = payload.get("profile", {})
        transactions = payload.get("transactions", [])
        
        self.log_action(session_id, "Running anomaly detection algorithms")
        anomalies = registry.execute("detect_anomalies", transactions=transactions)
        self.log_action(session_id, f"Detected {len(anomalies)} anomalies")
        
        risk_score = 50
        if anomalies:
             risk_score += min(len(anomalies) * 10, 30) 
             if any(a["severity"] == "high" for a in anomalies):
                 risk_score += 20
                 
        if profile.get("risk_profile") == "aggressive":
             risk_score += 10
             
        risk_score = min(risk_score, 100)
        self.log_action(session_id, f"Calculated risk score: {risk_score}")
        
        return {
            "anomalies": anomalies,
            "risk_score": risk_score,
            "requires_hitl": len(anomalies) > 0
        }
