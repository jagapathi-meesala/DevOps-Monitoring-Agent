# DevOps Monitoring Agent

A framework-independent OpenGAP agent for deterministic DevOps monitoring analysis.

## What it does

- Evaluates service states and CPU, memory, and disk thresholds.
- Summarizes monitoring checks into a reproducible operational status.
- Uses explicit tool contracts and a dynamic registry.
- Keeps domain logic independent from OpenAI, CrewAI, Claude Code, and Lyzr SDKs.
- Rejects invalid inputs instead of fabricating telemetry.

## Structure

- `agent.yaml` — OpenGAP manifest.
- `core/` — deterministic domain logic.
- `contracts/` — framework-independent contracts.
- `tools/` — tool schemas and implementations.
- `skills/` — declared Agent Skills.
- `adapters/` — portable and framework compatibility boundaries.
- `verification/` — local validation scripts and reports.
- `tests/` — pytest suite.

## Local setup

Create a virtual environment and install `requirements.txt`. Runtime configuration is intentionally environment-only; copy `.env.example` to `.env` and provide the required values without committing `.env`.

## Validation

Run `pytest -q`. The project also contains local structural checks for the manifest and explainability document. The OpenGAP CLI is not installed in the build environment used for this repository, so CLI validation must be performed separately with a configured OpenGAP installation.

## Portability

The adapters expose the same portable contract to OpenAI, CrewAI, Claude Code, and Lyzr-shaped callers. These are compatibility boundaries, not claims that those external SDKs are installed or that live framework integrations were executed here.
