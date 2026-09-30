---
name: incident-triage
description: Summarize monitoring checks into a deterministic incident severity signal.
---

# Incident Triage

## Purpose
Aggregate named monitoring checks into a simple, reproducible status for operational triage.

## Inputs
Each check must contain a non-empty name and one status: `pass`, `warn`, or `fail`.

## Behavior
A failed check produces `critical`; otherwise a warning produces `degraded`; otherwise the result is `healthy`. The skill reports the exact failed and warning checks so the result is traceable.

## Outputs
Return overall status, counts by check status, failed check names, and warning check names.

## Invalid Inputs
Reject non-list check collections, malformed check objects, missing names, and unsupported statuses.
