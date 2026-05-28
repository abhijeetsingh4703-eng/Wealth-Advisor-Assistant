from typing import Any, Dict
from .base_agent import BaseAgent
from .data_fetcher import DataFetcherAgent
from .analyzer import AnalyzerAgent
from .report_generator import ReportGeneratorAgent
from backend.memory.short_term import memory_store
from backend.memory.long_term import long_term_store

class OrchestratorAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Orchestrator", memory_store=memory_store)
        self.data_fetcher = DataFetcherAgent(memory_store=memory_store)
        self.analyzer = AnalyzerAgent(memory_store=memory_store)
        self.report_generator = ReportGeneratorAgent(memory_store=memory_store)

    def execute(self, session_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Coordinates the workflow between agents.
        Returns the final state or pauses for HITL if needed.
        """
        self.log_action(session_id, "Starting orchestration workflow")
        client_id = payload.get("client_id")
        
        self.log_action(session_id, "Delegating to DataFetcher")
        data_payload = self.data_fetcher.execute(session_id, {"client_id": client_id})
        memory_store.update_context(session_id, "profile", data_payload["profile"])
        memory_store.update_context(session_id, "transactions", data_payload["transactions"])

        self.log_action(session_id, "Delegating to Analyzer")
        analysis_payload = self.analyzer.execute(session_id, data_payload)
        memory_store.update_context(session_id, "analysis", analysis_payload)

        if analysis_payload.get("requires_hitl"):
            self.log_action(session_id, "HITL Checkpoint Reached: Waiting for human review of anomalies")
            memory_store.set_status(session_id, "awaiting_review")
            return {
                "status": "awaiting_review",
                "session_id": session_id,
                "message": "Human review required for detected anomalies",
                "anomalies": analysis_payload["anomalies"]
            }
        
        return self.resume_workflow(session_id)

    def resume_workflow(self, session_id: str) -> Dict[str, Any]:
        """Resumes workflow after HITL review"""
        self.log_action(session_id, "Resuming workflow after HITL check")
        memory_store.set_status(session_id, "generating_report")
        
        profile = memory_store.get_context(session_id, "profile")
        analysis = memory_store.get_context(session_id, "analysis")
        
        self.log_action(session_id, "Delegating to ReportGenerator")
        report = self.report_generator.execute(session_id, {
            "profile": profile,
            "analysis": analysis
        })
        memory_store.update_context(session_id, "report", report)
        memory_store.set_status(session_id, "completed")
        
        self.log_action(session_id, "Workflow completed successfully")
        
        long_term_store.save_session_report(session_id, profile["client_id"], report["summary"])
        if analysis.get("anomalies"):
             long_term_store.save_anomalies(session_id, profile["client_id"], analysis["anomalies"])
        self.log_action(session_id, "Saved to long term memory")
        
        return {
            "status": "completed",
            "session_id": session_id,
            "report": report
        }
