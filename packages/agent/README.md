# @komara/agent

Top-level agent package: the KomaraOrchestrator that wires together the AI engine, message router, and all platform connectors.

## Features

- Central orchestrator for Telegram, Facebook, Instagram, WhatsApp
- Environment-based auto-initialization of connectors
- Per-platform session management with conversation history
- Health status reporting

## Usage

```python
from packages.agent.src.orchestrator import KomaraOrchestrator

orchestrator = KomaraOrchestrator()
orchestrator.init_telegram("bot_token")
orchestrator.print_status()
```

## Structure

```
packages/agent/
  src/
    orchestrator.py    # KomaraOrchestrator
    index.ts
  CHANGELOG.md
  package.json
  tsconfig.json
```
