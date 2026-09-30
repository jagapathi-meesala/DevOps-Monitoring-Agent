---
name: health-assessment
description: Assess supplied DevOps service states and infrastructure metrics using deterministic thresholds.
---

# Health Assessment

## Purpose
Assess a supplied monitoring snapshot without contacting external systems.

## Inputs
Provide service objects with `name` and `status`, plus numeric CPU, memory, and disk utilization metrics. Optional thresholds can be supplied for those metrics.

## Behavior
Validate the snapshot, compare metrics with supplied thresholds, identify down or degraded services, and produce a structured health result. The skill does not invent missing telemetry.

## Outputs
Return an overall status of `healthy`, `degraded`, or `critical`, together with reasons and threshold breaches.

## Invalid Inputs
Reject missing required fields, unsupported service states, non-numeric metrics, and values outside the 0–100 range.
