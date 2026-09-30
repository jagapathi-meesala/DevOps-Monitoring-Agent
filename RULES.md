# Deterministic Rules

1. A service with status `down` makes the health result `critical`.
2. With no down service, a `degraded` service makes the result `degraded`.
3. With no down or degraded service, a metric at or above its supplied threshold makes the result `degraded`.
4. If there are no service failures and no threshold breaches, the result is `healthy`.
5. Incident-triage checks map `fail` to `critical`, `warn` to `degraded`, and all-pass to `healthy`.
6. Invalid or missing required data is rejected instead of being replaced with invented observations.

# Threshold Formula

For each monitored metric, a breach occurs when `observed_value >= threshold`. Metric values and thresholds are constrained to the range greater than 0 and at most 100.
