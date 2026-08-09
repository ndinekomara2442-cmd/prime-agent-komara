# @komara/tui

Terminal UI and connector layer for Komara Agency bots.

This package groups all platform connectors (Telegram, Facebook, Instagram, WhatsApp) and provides a unified interface for sending and receiving messages across platforms.

## Connectors

1. *Telegram* — Sessions, inline keyboards, callback queries, command handlers
2. *Facebook Messenger* — Polling, template carousels, conversation tracking
3. *Instagram DM* — Business account ready (pending activation)
4. *WhatsApp Business* — Templates, interactive menus, quick reply buttons

## Usage

```python
from packages.tui.src.connectors import (
    TelegramConnector, FacebookConnector,
    InstagramConnector, WhatsAppConnector,
)
```

## Structure

```
packages/tui/
  src/
    connectors/
      telegram_connector.py
      facebook_connector.py
      instagram_connector.py
      whatsapp_connector.py
    index.ts
  test/
  CHANGELOG.md
  package.json
  tsconfig.json
```
