import uuid
from typing import Dict, Any

class ShortTermMemory:
    def __init__(self):
        self._sessions: Dict[str, Dict[str, Any]] = {}

    def create_session(self) -> str:
        session_id = str(uuid.uuid4())
        self._sessions[session_id] = {
            "status": "created",
            "context": {},
            "history": []
        }
        return session_id

    def update_context(self, session_id: str, key: str, value: Any):
        if session_id in self._sessions:
            self._sessions[session_id]["context"][key] = value

    def get_context(self, session_id: str, key: str) -> Any:
        if session_id in self._sessions:
            return self._sessions[session_id]["context"].get(key)
        return None

    def add_history(self, session_id: str, event: str):
        if session_id in self._sessions:
            self._sessions[session_id]["history"].append(event)
            
    def get_session(self, session_id: str) -> Dict[str, Any]:
        return self._sessions.get(session_id)

    def set_status(self, session_id: str, status: str):
        if session_id in self._sessions:
             self._sessions[session_id]["status"] = status

memory_store = ShortTermMemory()
