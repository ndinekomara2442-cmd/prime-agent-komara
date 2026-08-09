# packages

This directory contains the Komara Agency monorepo packages, mirroring the Prime Agent structure:

1. `@komara/ai` — AI provider abstraction, intent detection, response engine
2. `@komara/coding-agent` — Core agent runtime: message router, queue, retry, orchestrator
3. `@komara/tui` — Platform connectors (Telegram, Facebook, Instagram, WhatsApp)
4. `@komara/agent` — Top-level orchestrator wiring everything together

Each package has its own `package.json`, `tsconfig.json`, `CHANGELOG.md`, and `README.md`.

The actual Python implementation lives in the repo root (`core/`, `connectors/`, `main.py`).
The `packages/` structure provides TypeScript type definitions and documentation that mirror the Python modules, ready for a future TypeScript port or hybrid setup.
