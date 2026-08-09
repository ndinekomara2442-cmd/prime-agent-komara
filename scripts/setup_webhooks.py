#!/usr/bin/env python3
"""
scripts/setup_webhooks.py
Configure les webhooks pour Telegram et WhatsApp Business.
"""

import os
import sys
import json
import urllib.request
import urllib.error


def set_telegram_webhook(bot_token: str, webhook_url: str) -> dict:
    """Configure le webhook Telegram."""
    url = f"https://api.telegram.org/bot{bot_token}/setWebhook"
    data = json.dumps({"url": webhook_url}).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return {"ok": False, "error": e.read().decode()}


def get_telegram_webhook_info(bot_token: str) -> dict:
    """Recupere les infos du webhook Telegram actuel."""
    url = f"https://api.telegram.org/bot{bot_token}/getWebhookInfo"
    with urllib.request.urlopen(url) as resp:
        return json.loads(resp.read())


def main():
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    webhook_url = os.getenv("TELEGRAM_WEBHOOK_URL")

    if not bot_token:
        print("Error: TELEGRAM_BOT_TOKEN not set", file=sys.stderr)
        sys.exit(1)

    if len(sys.argv) > 1 and sys.argv[1] == "info":
        info = get_telegram_webhook_info(bot_token)
        print(json.dumps(info, indent=2))
        return

    if not webhook_url:
        print("Error: TELEGRAM_WEBHOOK_URL not set", file=sys.stderr)
        sys.exit(1)

    result = set_telegram_webhook(bot_token, webhook_url)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
