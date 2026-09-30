"""Framework-neutral invocation boundary."""
from collections.abc import Mapping
from contracts import ToolContract


class PortableAdapter:
    def __init__(self, registry):
        self.registry = registry

    def invoke(self, tool_name: str, payload: Mapping):
        contract = self.registry.get(tool_name)
        if contract is None:
            return {"ok": False, "error": "unknown_tool", "tool": tool_name}
        try:
            return {"ok": True, "tool": tool_name, "result": contract.execute(payload)}
        except (ValueError, TypeError) as exc:
            return {"ok": False, "tool": tool_name, "error": "invalid_input", "message": str(exc)}
        except Exception:
            return {"ok": False, "tool": tool_name, "error": "execution_error", "message": "tool execution failed"}
