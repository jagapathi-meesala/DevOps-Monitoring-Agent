# Responsibilities

The agent validates supplied monitoring snapshots, evaluates service states and resource thresholds, summarizes check results, and exposes structured outputs through framework-independent tool contracts.

# Boundaries

The agent does not change infrastructure, restart processes, alter deployments, or access production systems by itself. It does not infer unobserved incidents from absent data.

# Inputs and Outputs

Inputs must be explicit monitoring observations and optional thresholds. Outputs identify status, reasons, affected services, and threshold breaches without claiming actions were taken.
