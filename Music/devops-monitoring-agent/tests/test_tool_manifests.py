from pathlib import Path
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_tool_manifests_follow_inspected_opengap_shape():
    for path in sorted((ROOT / "tools").glob("*.yaml")):
        data = yaml.safe_load(path.read_text())
        assert set(data) <= {"name", "description", "version", "input_schema", "output_schema", "implementation", "annotations"}
        assert re.fullmatch(r"^[a-z][a-z0-9-]*$", data["name"])
        assert data["input_schema"]["type"] == "object"
        assert "properties" in data["input_schema"]
        impl = data["implementation"]
        assert impl["type"] == "script"
        assert impl["runtime"] == "python3"
        assert (ROOT / "tools" / impl["path"]).is_file()
