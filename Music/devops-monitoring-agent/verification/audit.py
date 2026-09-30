from pathlib import Path
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]


def audit_manifest():
    data = yaml.safe_load((ROOT / "agent.yaml").read_text())
    assert data["spec_version"] == "0.1.0"
    assert re.fullmatch(r"^[a-z][a-z0-9-]*$", data["name"])
    assert re.fullmatch(r"^\d+\.\d+\.\d+$", str(data["version"]))
    assert isinstance(data["skills"], list) and all(isinstance(x, str) for x in data["skills"])
    assert isinstance(data["tools"], list) and all(isinstance(x, str) for x in data["tools"])
    assert set(data) <= {"spec_version", "name", "version", "description", "author", "license", "model", "extends", "dependencies", "skills", "tools", "agents", "delegation", "runtime", "a2a", "compliance", "registries", "tags", "mcp_servers", "metadata"}
    for skill in data["skills"]:
        assert (ROOT / "skills" / skill / "SKILL.md").is_file(), skill
    for tool in data["tools"]:
        assert (ROOT / "tools" / f"{tool}.yaml").is_file(), tool
        assert (ROOT / "tools" / f"{tool}.py").is_file(), tool


def audit_explainability():
    text = (ROOT / "EXPLAINABILITY.md").read_text()
    headings = re.findall(r"^## .+$", text, re.MULTILINE)
    assert headings[:3] == [
        "## Inputs and Data Sources",
        "## Decision and Reasoning",
        "## Limits and Constraints",
    ]
    for h in headings[:3]:
        assert len([s for s in re.split(r"(?<=[.!?])\s+", text[text.index(h) + len(h):].split("\n## ", 1)[0].strip()) if s.strip()]) >= 2
    assert "\n## Inputs\n" not in text
    assert "\n## Decision\n" not in text
    assert "\n## Limits\n" not in text


if __name__ == "__main__":
    audit_manifest()
    audit_explainability()
    print("Local structural audit passed")
