"""Thin compatibility boundaries for portability targets.

These adapters intentionally do not import framework SDKs. They translate a
framework-shaped call into the portable adapter contract and can be tested
without external framework packages.
"""
from collections.abc import Mapping
from .portable_adapter import PortableAdapter


class FrameworkAdapter:
    framework = "generic"

    def __init__(self, portable: PortableAdapter):
        self.portable = portable

    def invoke(self, tool_name: str, payload: Mapping):
        return self.portable.invoke(tool_name, payload)


class OpenAIAdapter(FrameworkAdapter):
    framework = "openai"


class CrewAIAdapter(FrameworkAdapter):
    framework = "crewai"


class ClaudeCodeAdapter(FrameworkAdapter):
    framework = "claude-code"


class LyzrAdapter(FrameworkAdapter):
    framework = "lyzr"
