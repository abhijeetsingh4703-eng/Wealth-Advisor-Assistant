from typing import Any, Dict
from .base_agent import BaseAgent
from backend.tools.tool_registry import registry
from backend.tools.crm_api import get_client_profile, get_client_transactions

registry.register("get_client_profile", get_client_profile)
registry.register("get_client_transactions", get_client_transactions)

class DataFetcherAgent(BaseAgent):
    def __init__(self, memory_store=None):
        super().__init__(name="DataFetcher", memory_store=memory_store)

    def execute(self, session_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        client_id = payload.get("client_id")
        if not client_id:
            raise ValueError("DataFetcherAgent requires 'client_id' in payload")

        self.log_action(session_id, f"Fetching data for client: {client_id}")
        
        try:
            profile = registry.execute("get_client_profile", client_id=client_id)
            transactions = registry.execute("get_client_transactions", client_id=client_id)
            
            self.log_action(session_id, "Successfully fetched profile and transactions")
            
            return {
                "profile": profile,
                "transactions": transactions
            }
        except Exception as e:
            self.log_action(session_id, f"Error fetching data: {str(e)}")
            raise e
