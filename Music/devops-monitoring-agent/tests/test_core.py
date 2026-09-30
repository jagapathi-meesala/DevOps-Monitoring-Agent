import pytest
from core.monitoring import evaluate_health, summarize_monitoring


def test_healthy_snapshot():
    result = evaluate_health({"services": [{"name": "api", "status": "healthy"}], "metrics": {"cpu_percent": 40}})
    assert result["status"] == "healthy"


def test_down_service_is_critical():
    result = evaluate_health({"services": [{"name": "api", "status": "down"}], "metrics": {}})
    assert result["status"] == "critical"


def test_degraded_service_is_degraded():
    result = evaluate_health({"services": [{"name": "worker", "status": "degraded"}], "metrics": {}})
    assert result["status"] == "degraded"


def test_metric_threshold_breach():
    result = evaluate_health({"services": [{"name": "api", "status": "healthy"}], "metrics": {"cpu_percent": 90}, "thresholds": {"cpu_percent": 85}})
    assert result["status"] == "degraded"
    assert result["threshold_breaches"][0]["metric"] == "cpu_percent"


def test_invalid_metric_rejected():
    with pytest.raises(ValueError, match="between 0 and 100"):
        evaluate_health({"services": [{"name": "api", "status": "healthy"}], "metrics": {"cpu_percent": 101}})


def test_invalid_service_status_rejected():
    with pytest.raises(ValueError, match="service status"):
        evaluate_health({"services": [{"name": "api", "status": "unknown"}], "metrics": {}})


def test_summary_fail_is_critical():
    result = summarize_monitoring({"checks": [{"name": "http", "status": "fail"}]})
    assert result["overall_status"] == "critical"
    assert result["failed_checks"] == ["http"]


def test_summary_warning_is_degraded():
    result = summarize_monitoring({"checks": [{"name": "latency", "status": "warn"}]})
    assert result["overall_status"] == "degraded"


def test_summary_all_pass_is_healthy():
    result = summarize_monitoring({"checks": [{"name": "http", "status": "pass"}, {"name": "cpu", "status": "pass"}]})
    assert result["overall_status"] == "healthy"


def test_summary_invalid_status_rejected():
    with pytest.raises(ValueError, match="check status"):
        summarize_monitoring({"checks": [{"name": "http", "status": "unknown"}]})
