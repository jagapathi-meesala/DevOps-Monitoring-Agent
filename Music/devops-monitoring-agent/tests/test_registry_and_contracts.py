import pytest
from contracts import ToolContract
from adapters import ToolRegistry, PortableAdapter


def contract():
    return ToolContract("echo", "echo input", {"type": "object"}, "object", lambda p: None, lambda p: {"value": p["value"]})


def test_register_and_discover():
    r = ToolRegistry(); r.register(contract())
    assert r.discover() == ["echo"]


def test_duplicate_registration_rejected():
    r = ToolRegistry(); r.register(contract())
    with pytest.raises(ValueError): r.register(contract())


def test_portable_success():
    r = ToolRegistry(); r.register(contract())
    result = PortableAdapter(r).invoke("echo", {"value": 3})
    assert result["ok"] is True and result["result"] == {"value": 3}


def test_portable_unknown_tool():
    result = PortableAdapter(ToolRegistry()).invoke("missing", {})
    assert result["error"] == "unknown_tool"


def test_portable_validation_failure():
    bad = ToolContract("bad", "bad", {}, "object", lambda p: (_ for _ in ()).throw(ValueError("bad input")), lambda p: {})
    r = ToolRegistry(); r.register(bad)
    result = PortableAdapter(r).invoke("bad", {})
    assert result["ok"] is False
