from typing import Any, Dict
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def __init__(self, name: str, memory_store=None):
        self.name = name
        self.memory_store = memory_store

    @abstractmethod
    def execute(self, session_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes the agent's core responsibility.
        Should log to memory_store if provided.
        """
        pass

    def log_action(self, session_id: str, action: str):
        if self.memory_store:
            self.memory_store.add_history(session_id, f"[{self.name}] {action}")
            print(f"[{self.name}] {action}")
