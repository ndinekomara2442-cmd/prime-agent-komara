#!/usr/bin/env python3
"""
scripts/health_check.py
Verifie l'etat de sante de tous les connectors Komara Agency.
"""

import os
import sys
import asyncio

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import KomaraOrchestrator


async def run_health_check():
    orchestrator = KomaraOrchestrator()

    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if telegram_token:
        orchestrator.init_telegram(telegram_token)

    fb_token = os.getenv("FACEBOOK_PAGE_TOKEN")
    if fb_token:
        orchestrator.init_facebook(fb_token)

    orchestrator.print_status()

    status = orchestrator.get_status()
    all_ok = all(
        v.get("status") != "not initialized"
        for k, v in status.items()
        if k in ["telegram", "facebook", "instagram", "whatsapp"]
    )

    return 0 if all_ok else 1


if __name__ == "__main__":
    exit_code = asyncio.run(run_health_check())
    sys.exit(exit_code)
