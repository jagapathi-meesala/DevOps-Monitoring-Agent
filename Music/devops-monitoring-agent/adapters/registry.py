"""Dynamic registry for framework-independent tools."""
from contracts import ToolContract


class ToolRegistry:
    def __init__(self):
        self._tools = {}

    def register(self, contract: ToolContract) -> None:
        if not isinstance(contract, ToolContract):
            raise TypeError("only ToolContract instances can be registered")
        if contract.name in self._tools:
            raise ValueError(f"tool already registered: {contract.name}")
        self._tools[contract.name] = contract

    def get(self, name: str):
        return self._tools.get(name)

    def discover(self):
        return sorted(self._tools)
