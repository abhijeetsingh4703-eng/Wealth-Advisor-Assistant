from typing import Any, Dict
from .base_agent import BaseAgent

class ReportGeneratorAgent(BaseAgent):
    def __init__(self, memory_store=None):
        super().__init__(name="ReportGenerator", memory_store=memory_store)

    def execute(self, session_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        self.log_action(session_id, "Generating final advisory report")
        
        profile = payload.get("profile", {})
        analysis = payload.get("analysis", {})
        anomalies = analysis.get("anomalies", [])
        risk_score = analysis.get("risk_score", 50)
        
        client_name = profile.get("name", "Client")
        
        unresolved = [a for a in anomalies if a.get("is_approved") is False]
        
        summary = f"Wealth Advisory Report for {client_name}. "
        summary += f"Portfolio Risk Score is {risk_score}/100. "
        
        if unresolved:
             summary += f"WARNING: There are {len(unresolved)} unresolved anomalies in recent transactions that require immediate attention."
        elif anomalies:
             summary += f"Note: {len(anomalies)} anomalies were flagged and reviewed."
        else:
             summary += "No anomalies detected in recent activity."

        action_items = []
        if risk_score > 70:
             action_items.append("Schedule urgent portfolio review call to discuss risk exposure.")
        if profile.get("portfolio", {}).get("allocations", {}).get("cash", 0) > 0.15:
             action_items.append("Discuss deploying excess cash reserves.")
        if unresolved:
             action_items.append("Investigate rejected anomalous transactions.")
             
        if not action_items:
             action_items.append("Continue current strategy. No immediate actions required.")
             
        report = {
             "client_id": profile.get("client_id"),
             "summary": summary,
             "action_items": action_items,
             "anomalies_flagged": len(anomalies),
             "portfolio_health_score": max(100 - risk_score, 0)
        }
        
        self.log_action(session_id, "Report generation complete")
        return report
