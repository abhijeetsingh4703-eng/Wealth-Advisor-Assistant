from typing import Callable, Dict, Any, Type, List
from pydantic import BaseModel
import inspect

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Callable] = {}
        self._schemas: Dict[str, Type[BaseModel]] = {}

    def register(self, name: str, func: Callable, schema: Type[BaseModel] = None):
        self._tools[name] = func
        self._schemas[name] = schema

    def execute(self, name: str, **kwargs) -> Any:
        if name not in self._tools:
            raise ValueError(f"Tool '{name}' not found in registry.")
        
        if name in self._schemas and self._schemas[name]:
            schema = self._schemas[name]
            schema(**kwargs)

        return self._tools[name](**kwargs)

    def get_available_tools(self) -> List[str]:
         return list(self._tools.keys())

registry = ToolRegistry()
