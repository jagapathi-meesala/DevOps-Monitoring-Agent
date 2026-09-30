"""Framework-independent tool contracts."""
from dataclasses import dataclass
from typing import Any, Callable, Mapping


class ContractError(ValueError):
    """Raised when a tool contract is invalid."""


@dataclass(frozen=True)
class ToolContract:
    name: str
    purpose: str
    input_schema: Mapping[str, Any]
    output_description: str
    validator: Callable[[Mapping[str, Any]], None]
    executor: Callable[[Mapping[str, Any]], Mapping[str, Any]]

    def validate(self, payload: Mapping[str, Any]) -> None:
        if not isinstance(payload, Mapping):
            raise ContractError("tool input must be an object")
        self.validator(payload)

    def execute(self, payload: Mapping[str, Any]) -> Mapping[str, Any]:
        self.validate(payload)
        result = self.executor(payload)
        if not isinstance(result, Mapping):
            raise ContractError("tool executor must return an object")
        return dict(result)
