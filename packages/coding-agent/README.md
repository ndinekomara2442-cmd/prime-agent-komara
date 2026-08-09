# @komara/coding-agent

Core agent runtime: message router, orchestrator, and session management for Komara Agency bots.

## Features

- Multi-platform message routing (Telegram, Facebook, Instagram, WhatsApp)
- Async message queue with exponential backoff retry
- Middleware pipeline for message preprocessing
- Central orchestrator coordinating all connectors
- Per-session conversation context and history

## Usage

```python
from packages.coding-agent.src.router import MessageRouter, Platform, IncomingMessage

router = MessageRouter()
router.register_handler(Platform.TELEGRAM, my_handler)
```

## Structure

```
packages/coding-agent/
  src/
    router.py        # Message router, queue, retry
    orchestrator.py   # Central coordinator
    session.py        # Session management
  test/
    test_router.py    # Router tests
  docs/
    usage.md          # CLI and usage reference
    architecture.md   # Architecture overview
  CHANGELOG.md
  package.json
  tsconfig.json
```
