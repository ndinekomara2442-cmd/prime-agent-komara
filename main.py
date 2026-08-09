"""
Komara Agency — Main Orchestrator
Orchestrateur central qui coordonne tous les agents et plateformes.
"""

import asyncio
import logging
import json
from typing import Dict, Optional

from core import (
    MessageRouter,
    MessageQueue,
    IncomingMessage,
    OutgoingMessage,
    Platform,
    MessageStatus,
    ResponseEngine,
    ConversationContext,
)
from connectors import (
    TelegramConnector,
    TelegramConfig,
    FacebookConnector,
    FacebookConfig,
    InstagramConnector,
    InstagramConfig,
    WhatsAppConnector,
    WhatsAppConfig,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s"
)
logger = logging.getLogger("komara.orchestrator")


class KomaraOrchestrator:
    """
    Orchestrateur central de Komara Agency.
    Coordonne les bots Telegram, Facebook, Instagram et WhatsApp.
    """

    def __init__(self):
        # AI Engine
        self.ai_engine = ResponseEngine()

        # Router
        self.router = MessageRouter()

        # Connectors
        self.telegram: Optional[TelegramConnector] = None
        self.facebook: Optional[FacebookConnector] = None
        self.instagram: Optional[InstagramConnector] = None
        self.whatsapp: Optional[WhatsAppConnector] = None

        # Sessions par plateforme
        self._sessions: Dict[str, ConversationContext] = {}

        self._setup_router()

    def _setup_router(self):
        """Configure les handlers du router pour chaque plateforme."""
        self.router.register_handler(Platform.TELEGRAM, self._handle_telegram)
        self.router.register_handler(Platform.FACEBOOK, self._handle_facebook)
        self.router.register_handler(Platform.INSTAGRAM, self._handle_instagram)
        self.router.register_handler(Platform.WHATSAPP, self._handle_whatsapp)

    def init_telegram(self, bot_token: str):
        """Initialise le connector Telegram."""
        config = TelegramConfig(bot_token=bot_token)
        self.telegram = TelegramConnector(config)
        logger.info("Telegram connector initialized")

    def init_facebook(self, page_token: str):
        """Initialise le connector Facebook."""
        config = FacebookConfig(page_access_token=page_token)
        self.facebook = FacebookConnector(config)
        logger.info("Facebook connector initialized")

    def init_instagram(self, access_token: str, business_account_id: str):
        """Initialise le connector Instagram."""
        config = InstagramConfig(
            access_token=access_token,
            business_account_id=business_account_id,
            status="active",
        )
        self.instagram = InstagramConnector(config)
        logger.info("Instagram connector initialized")

    def init_whatsapp(self, access_token: str, phone_number_id: str):
        """Initialise le connector WhatsApp."""
        config = WhatsAppConfig(
            access_token=access_token,
            phone_number_id=phone_number_id,
        )
        self.whatsapp = WhatsAppConnector(config)
        logger.info("WhatsApp connector initialized")

    def _get_session(self, platform: str, sender_id: str, sender_name: str = "") -> ConversationContext:
        session_key = f"{platform}:{sender_id}"
        if session_key not in self._sessions:
            self._sessions[session_key] = ConversationContext(
                sender_id=sender_id,
                sender_name=sender_name,
                platform=platform,
                history=[],
            )
        return self._sessions[session_key]

    async def _handle_telegram(self, message: IncomingMessage) -> Optional[str]:
        """Handler pour les messages Telegram."""
        ctx = self._get_session("telegram", message.sender_id, message.sender_name)
        ctx.history.append({"role": "user", "text": message.text})
        response = self.ai_engine.generate(ctx, message.text)
        if response:
            ctx.history.append({"role": "agent", "text": response})
        return response

    async def _handle_facebook(self, message: IncomingMessage) -> Optional[str]:
        """Handler pour les messages Facebook."""
        ctx = self._get_session("facebook", message.sender_id, message.sender_name)
        ctx.history.append({"role": "user", "text": message.text})
        response = self.ai_engine.generate(ctx, message.text)
        if response:
            ctx.history.append({"role": "agent", "text": response})
        return response

    async def _handle_instagram(self, message: IncomingMessage) -> Optional[str]:
        """Handler pour les messages Instagram."""
        ctx = self._get_session("instagram", message.sender_id, message.sender_name)
        ctx.history.append({"role": "user", "text": message.text})
        response = self.ai_engine.generate(ctx, message.text)
        if response:
            ctx.history.append({"role": "agent", "text": response})
        return response

    async def _handle_whatsapp(self, message: IncomingMessage) -> Optional[str]:
        """Handler pour les messages WhatsApp."""
        ctx = self._get_session("whatsapp", message.sender_id, message.sender_name)
        ctx.history.append({"role": "user", "text": message.text})
        response = self.ai_engine.generate(ctx, message.text)
        if response:
            ctx.history.append({"role": "agent", "text": response})
        return response

    async def process_message(self, message: IncomingMessage) -> Optional[OutgoingMessage]:
        """Traite un message entrant et retourne la reponse."""
        return await self.router.process_incoming(message)

    def get_status(self) -> Dict:
        """Retourne l'etat de tous les connectors."""
        status = {
            "telegram": self.telegram.get_stats() if self.telegram else {"status": "not initialized"},
            "facebook": self.facebook.get_stats() if self.facebook else {"status": "not initialized"},
            "instagram": self.instagram.get_stats() if self.instagram else {"status": "not initialized"},
            "whatsapp": self.whatsapp.get_stats() if self.whatsapp else {"status": "not initialized"},
            "sessions": len(self._sessions),
            "router_stats": self.router.get_stats(),
        }
        return status

    def print_status(self):
        """Affiche l'etat du systeme."""
        status = self.get_status()
        print("\n" + "=" * 60)
        print("Komara Agency - System Status")
        print("=" * 60)

        for platform, info in status.items():
            if platform in ["sessions", "router_stats"]:
                continue
            platform_name = platform.upper()
            if isinstance(info, dict) and "status" in info and info["status"] == "not initialized":
                print(f"  [!] {platform_name}: not initialized")
            else:
                print(f"  [OK] {platform_name}: {json.dumps(info, indent=2, default=str)}")

        print(f"\n  Active sessions: {status['sessions']}")
        print(f"  Router: {json.dumps(status['router_stats'], indent=2)}")
        print("=" * 60)


async def main():
    """Point d'entree principal."""
    orchestrator = KomaraOrchestrator()

    # Initialiser les connectors disponibles
    import os

    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if telegram_token:
        orchestrator.init_telegram(telegram_token)

    fb_token = os.getenv("FACEBOOK_PAGE_TOKEN")
    if fb_token:
        orchestrator.init_facebook(fb_token)

    ig_token = os.getenv("INSTAGRAM_ACCESS_TOKEN")
    ig_account = os.getenv("INSTAGRAM_BUSINESS_ACCOUNT_ID")
    if ig_token and ig_account:
        orchestrator.init_instagram(ig_token, ig_account)

    wa_token = os.getenv("WHATSAPP_API_TOKEN")
    wa_phone_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
    if wa_token and wa_phone_id:
        orchestrator.init_whatsapp(wa_token, wa_phone_id)

    orchestrator.print_status()


if __name__ == "__main__":
    asyncio.run(main())
