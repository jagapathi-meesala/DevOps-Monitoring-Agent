"""Validate the manifest against the v0.1.0 fields used by this project.

The authoritative schema was inspected from the OpenGAP repository. The build
container cannot fetch remote files, so this check mirrors only the exact
constraints exercised by this minimal manifest; it is not a replacement for
`opengap validate`.
"""
from pathlib import Path
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]
ALLOWED = {"spec_version", "name", "version", "description", "author", "license", "model", "extends", "dependencies", "skills", "tools", "agents", "delegation", "runtime", "a2a", "compliance", "registries", "tags", "mcp_servers", "metadata"}

data = yaml.safe_load((ROOT / "agent.yaml").read_text())
assert set(data).issubset(ALLOWED)
assert data.get("spec_version") == "0.1.0"
assert re.fullmatch(r"^[a-z][a-z0-9-]*$", data["name"])
assert re.fullmatch(r"^\d+\.\d+\.\d+(-[a-zA-Z0-9.]+)?(\+[a-zA-Z0-9.]+)?$", str(data["version"]))
assert isinstance(data["description"], str) and data["description"]
assert all(re.fullmatch(r"^[a-z][a-z0-9-]*$", x) for x in data["skills"])
assert all(re.fullmatch(r"^[a-z][a-z0-9-]*$", x) for x in data["tools"])
print("Manifest local schema check passed")
