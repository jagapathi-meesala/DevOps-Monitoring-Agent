"""Deterministic DevOps monitoring logic."""
from __future__ import annotations

from typing import Any, Mapping


def _number(value: Any, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{field} must be a number")
    return float(value)


def validate_health_input(payload: Mapping[str, Any]) -> None:
    required = {"services", "metrics"}
    missing = required - set(payload)
    if missing:
        raise ValueError(f"missing required fields: {sorted(missing)}")
    if not isinstance(payload["services"], list) or not payload["services"]:
        raise ValueError("services must be a non-empty list")
    if not isinstance(payload["metrics"], Mapping):
        raise ValueError("metrics must be an object")
    for metric in ("cpu_percent", "memory_percent", "disk_percent"):
        if metric in payload["metrics"]:
            value = _number(payload["metrics"][metric], f"metrics.{metric}")
            if not 0 <= value <= 100:
                raise ValueError(f"metrics.{metric} must be between 0 and 100")
    for service in payload["services"]:
        if not isinstance(service, Mapping):
            raise ValueError("each service must be an object")
        if not isinstance(service.get("name"), str) or not service["name"].strip():
            raise ValueError("each service requires a non-empty name")
        if service.get("status") not in {"healthy", "degraded", "down"}:
            raise ValueError("service status must be healthy, degraded, or down")


def evaluate_health(payload: Mapping[str, Any]) -> dict[str, Any]:
    validate_health_input(payload)
    thresholds = payload.get("thresholds", {})
    if not isinstance(thresholds, Mapping):
        raise ValueError("thresholds must be an object")
    limits = {
        "cpu_percent": _number(thresholds.get("cpu_percent", 85), "thresholds.cpu_percent"),
        "memory_percent": _number(thresholds.get("memory_percent", 90), "thresholds.memory_percent"),
        "disk_percent": _number(thresholds.get("disk_percent", 90), "thresholds.disk_percent"),
    }
    for key, value in limits.items():
        if not 0 < value <= 100:
            raise ValueError(f"thresholds.{key} must be greater than 0 and at most 100")

    metric_flags = []
    for metric, limit in limits.items():
        value = payload["metrics"].get(metric)
        if value is not None and float(value) >= limit:
            metric_flags.append({"metric": metric, "value": float(value), "threshold": limit})

    down = [s["name"] for s in payload["services"] if s["status"] == "down"]
    degraded = [s["name"] for s in payload["services"] if s["status"] == "degraded"]
    if down:
        status = "critical"
    elif metric_flags or degraded:
        status = "degraded"
    else:
        status = "healthy"

    reasons = []
    if down:
        reasons.append("one or more services are down")
    if degraded:
        reasons.append("one or more services are degraded")
    reasons.extend(f"{f['metric']} reached or exceeded its threshold" for f in metric_flags)
    if not reasons:
        reasons.append("all supplied services are healthy and monitored metrics are below thresholds")

    return {
        "status": status,
        "reasons": reasons,
        "down_services": down,
        "degraded_services": degraded,
        "threshold_breaches": metric_flags,
    }


def validate_summary_input(payload: Mapping[str, Any]) -> None:
    if "checks" not in payload or not isinstance(payload["checks"], list):
        raise ValueError("checks must be a list")
    for check in payload["checks"]:
        if not isinstance(check, Mapping):
            raise ValueError("each check must be an object")
        if not isinstance(check.get("name"), str) or not check["name"].strip():
            raise ValueError("each check requires a name")
        if check.get("status") not in {"pass", "warn", "fail"}:
            raise ValueError("check status must be pass, warn, or fail")


def summarize_monitoring(payload: Mapping[str, Any]) -> dict[str, Any]:
    validate_summary_input(payload)
    counts = {"pass": 0, "warn": 0, "fail": 0}
    for check in payload["checks"]:
        counts[check["status"]] += 1
    if counts["fail"]:
        overall = "critical"
    elif counts["warn"]:
        overall = "degraded"
    else:
        overall = "healthy"
    return {
        "overall_status": overall,
        "counts": counts,
        "failed_checks": [c["name"] for c in payload["checks"] if c["status"] == "fail"],
        "warning_checks": [c["name"] for c in payload["checks"] if c["status"] == "warn"],
    }
