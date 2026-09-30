# Agent Purpose

DevOps Monitoring Agent analyzes monitoring observations supplied by a caller. It produces reproducible operational health signals without claiming access to telemetry that was not supplied.

## Inputs and Data Sources

The agent accepts monitoring observations through its framework-independent tool contracts. Service data contains a service name and status, while metric data can contain CPU, memory, and disk utilization percentages; these values are caller-supplied data sources rather than hidden live telemetry.

Optional thresholds are supplied in the same health-assessment request. The agent does not silently retrieve, invent, or substitute missing operational measurements.

### Input Requirements

A health assessment requires a non-empty service list and a metrics object. Each service must have a non-empty name and one of `healthy`, `degraded`, or `down`; monitored percentage values must be numeric and between 0 and 100.

## Decision and Reasoning

The health decision is deterministic: a down service produces `critical`; otherwise a degraded service or a metric threshold breach produces `degraded`; otherwise the result is `healthy`. A threshold breach is calculated as `observed_value >= threshold`.

The agent records the reasons supporting the status, including affected services and breached metrics. For incident triage, any failed check produces `critical`, otherwise any warning produces `degraded`, and an all-pass set produces `healthy`.

### Rules Applied

The decision process does not use a probabilistic model. The same validated input object and thresholds yield the same status and reason categories.

### Worked Example

If `api` is `healthy`, `worker` is `degraded`, and CPU is 60 while its threshold is 85, the result is `degraded` because a service is degraded. If every service is healthy and CPU is 90 with a threshold of 85, the result is also `degraded` because `90 >= 85`.

## Limits and Constraints

The agent is limited to the observations supplied in a request and does not provide real-time monitoring by itself. It cannot determine the health of a service whose state or relevant telemetry is absent from the input.

The agent does not restart services, deploy software, modify infrastructure, or contact monitoring providers. Invalid data is rejected rather than converted into a guessed operational state.

### Failure Handling

Malformed requests return structured validation errors through the portable adapter. Unexpected tool failures are returned as generic execution errors so internal implementation details are not exposed through the adapter boundary.

### Expected Outputs

Health assessment returns status, reasons, down services, degraded services, and threshold breaches. Monitoring summaries return overall status, counts, failed check names, and warning check names.

# Complete Execution Lifecycle

A caller selects a registered tool and supplies an input object. The registry resolves the contract, the contract validates the input, the deterministic domain function executes, and the adapter returns a structured success or failure object.

# Tool-by-Tool Behavior

## Health Assessment Tool

`evaluate-health` validates services and metrics, applies supplied thresholds, identifies affected services, and returns a deterministic health assessment. It does not perform network calls or infrastructure changes.

## Monitoring Summary Tool

`summarize-monitoring` validates named checks and aggregates their statuses. It returns the overall status plus exact lists of failed and warning checks.

# Provenance

The provenance of a result is the caller-provided monitoring snapshot and thresholds plus the deterministic rules documented in `RULES.md`. No external telemetry source is silently incorporated into a result.
