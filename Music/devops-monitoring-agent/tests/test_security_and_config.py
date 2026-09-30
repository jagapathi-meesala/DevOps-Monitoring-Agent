import os
import pytest
from config.settings import ConfigurationError, load_settings


def test_missing_runtime_config_fails(monkeypatch):
    monkeypatch.delenv("DEVOPS_MONITORING_LOG_LEVEL", raising=False)
    monkeypatch.delenv("DEVOPS_MONITORING_TIMEOUT_SECONDS", raising=False)
    with pytest.raises(ConfigurationError):
        load_settings()


def test_runtime_config_reads_environment(monkeypatch):
    monkeypatch.setenv("DEVOPS_MONITORING_LOG_LEVEL", "INFO")
    monkeypatch.setenv("DEVOPS_MONITORING_TIMEOUT_SECONDS", "30")
    assert load_settings() == {"log_level": "INFO", "timeout_seconds": 30}


def test_no_dotenv_file_is_tracked():
    assert not os.path.exists(".env")
