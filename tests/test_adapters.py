from adapters import ToolRegistry, PortableAdapter, OpenAIAdapter, CrewAIAdapter, ClaudeCodeAdapter, LyzrAdapter
from contracts import ToolContract


def test_all_framework_boundaries_use_same_portable_contract():
    r = ToolRegistry()
    r.register(ToolContract("status", "status", {}, "object", lambda p: None, lambda p: {"status": "ok"}))
    portable = PortableAdapter(r)
    for cls in (OpenAIAdapter, CrewAIAdapter, ClaudeCodeAdapter, LyzrAdapter):
        result = cls(portable).invoke("status", {})
        assert result["ok"] is True
