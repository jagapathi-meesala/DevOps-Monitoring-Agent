# Architecture

The project separates domain logic in `core/`, tool contracts in `contracts/`, tool implementations and schemas in `tools/`, and framework boundaries in `adapters/`.

# Development Rules

Keep core logic independent of external agent frameworks. Prefer deterministic functions, explicit validation, structured outputs, and small changes.

# Tool Conventions

Every enabled tool has a kebab-case manifest name, a YAML contract, an implementation, validation, failure handling, and tests.

# Testing Rules

Run the complete pytest suite after changes. Documentation and manifest structure are tested locally; OpenGAP CLI status must be reported separately.

# Portability

Framework adapters translate calls into the portable contract and must not make the core depend on OpenAI, CrewAI, Claude Code, or Lyzr packages.
