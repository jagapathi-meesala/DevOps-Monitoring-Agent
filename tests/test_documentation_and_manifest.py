from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def test_required_files_exist():
    required = ["agent.yaml", "SOUL.md", "AGENTS.md", "DUTIES.md", "RULES.md", "EXPLAINABILITY.md", ".env.example", "README.md"]
    assert all((ROOT / f).is_file() for f in required)


def test_structural_audit():
    subprocess.run([sys.executable, str(ROOT / "verification" / "audit.py")], check=True, capture_output=True, text=True)


def test_manifest_local_check():
    subprocess.run([sys.executable, str(ROOT / "verification" / "manifest_schema_check.py")], check=True, capture_output=True, text=True)


def test_no_conflicting_explainability_headings():
    text = (ROOT / "EXPLAINABILITY.md").read_text()
    assert "\n## Inputs\n" not in text
    assert "\n## Decision\n" not in text
    assert "\n## Limits\n" not in text
