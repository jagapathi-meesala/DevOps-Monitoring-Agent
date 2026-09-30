"""Runtime configuration loaded from environment variables only."""
import os


class ConfigurationError(RuntimeError):
    pass


def load_settings():
    required = ["DEVOPS_MONITORING_LOG_LEVEL", "DEVOPS_MONITORING_TIMEOUT_SECONDS"]
    missing = [name for name in required if not os.getenv(name)]
    if missing:
        raise ConfigurationError("missing required environment variables: " + ", ".join(missing))
    try:
        timeout = int(os.environ["DEVOPS_MONITORING_TIMEOUT_SECONDS"])
    except ValueError as exc:
        raise ConfigurationError("DEVOPS_MONITORING_TIMEOUT_SECONDS must be an integer") from exc
    if timeout <= 0:
        raise ConfigurationError("DEVOPS_MONITORING_TIMEOUT_SECONDS must be greater than zero")
    return {"log_level": os.environ["DEVOPS_MONITORING_LOG_LEVEL"], "timeout_seconds": timeout}
