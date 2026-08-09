"""
Komara Agency — Instagram Connector
Connector pour Instagram DM (necessite compte Business).
Structure prete pour quand le compte sera converti en Business.
"""

import logging
from typing import Dict, Optional, List, Any
from dataclasses import dataclass, field

logger = logging.getLogger("komara.instagram")


@dataclass
class InstagramConfig:
    access_token: str = ""
    business_account_id: str = ""
    api_version: str = "v25.0"
    status: str = "pending"  # pending -> active quand Business


@dataclass
class InstagramConversation:
    sender_id: str
    sender_username: str = ""
    last_message: str = ""
    timestamp: float = 0
    unread: bool = False


class InstagramConnector:
    """
    Connector Instagram DM.
    Prerequis: compte Instagram Business lie a une page Facebook.
    API: graph.instagram.com (pas graph.facebook.com)
    """

    def __init__(self, config: InstagramConfig):
        self.config = config
        self.base_url = "https://graph.instagram.com"
        self._conversations: Dict[str, InstagramConversation] = {}
        self._ready = bool(config.access_token and config.business_account_id)

    def is_ready(self) -> bool:
        return self._ready

    def get_setup_instructions(self) -> str:
        return (
            "Pour activer Instagram DM:\n\n"
            "1. Convertis ton compte Instagram personnel en Business\n"
            "   (Parametres > Type de compte > Passer a un compte professionnel)\n\n"
            "2. Lie ton Instagram Business a ta page Facebook\n"
            "   (Parametres Instagram > Partage > Facebook)\n\n"
            "3. Autorise la connexion Instagram dans Komara Agency\n\n"
            "4. Le bot sera automatiquement actif pour les DMs"
        )

    async def get_user_id(self) -> Optional[str]:
        """Recupere l'ID utilisateur Instagram."""
        if not self._ready:
            logger.warning("Instagram connector not ready")
            return None

        import aiohttp
        url = f"{self.base_url}/me?fields=id,username&access_token={self.config.access_token}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.json()
                return data.get("id")

    async def send_direct_message(self, recipient_id: str, text: str) -> Dict:
        """Envoie un DM Instagram."""
        if not self._ready:
            return {"error": "Instagram connector not ready"}

        import aiohttp
        url = f"{self.base_url}/v25.0/{self.config.business_account_id}/messages"
        payload = {
            "recipient": {"id": recipient_id},
            "message": {"text": text},
            "access_token": self.config.access_token,
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as resp:
                return await resp.json()

    async def get_conversations(self) -> List[Dict]:
        """Recupere les conversations Instagram DM."""
        if not self._ready:
            return []

        import aiohttp
        url = (
            f"{self.base_url}/{self.config.business_account_id}/conversations"
            f"?platform=instagram&access_token={self.config.access_token}"
        )
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.json()
                return data.get("data", [])

    def get_stats(self) -> Dict:
        return {
            "status": self.config.status,
            "ready": self._ready,
            "business_account_id": self.config.business_account_id or "not configured",
            "total_conversations": len(self._conversations),
            "setup_required": not self._ready,
        }
