"""
Komara Agency — Facebook Messenger Connector
Connector pour Facebook Messenger avec polling, sessions et gestion de conversations.
"""

import logging
from typing import Dict, Optional, List, Any
from dataclasses import dataclass, field
import time

logger = logging.getLogger("komara.facebook")


@dataclass
class FacebookConfig:
    page_id: str = "105344997852517"  # N-dine K fans
    page_name: str = "N-dine K fans"
    page_access_token: str = ""
    api_version: str = "v25.0"
    poll_interval_seconds: int = 7200  # 2h par defaut


@dataclass
class FacebookConversation:
    conversation_id: str
    participant_id: str
    participant_name: str
    last_message: str = ""
    last_message_time: float = 0
    unread_count: int = 0
    read: bool = True
    context: Dict[str, Any] = field(default_factory=dict)


class FacebookConnector:
    """Connector Facebook Messenger avec polling et gestion de conversations."""

    def __init__(self, config: FacebookConfig):
        self.config = config
        self.base_url = f"https://graph.facebook.com/{config.api_version}"
        self._conversations: Dict[str, FacebookConversation] = {}
        self._message_handlers: List = []

    async def fetch_conversations(self, page_token: str) -> List[Dict]:
        """Recupere les conversations de la page."""
        import aiohttp

        url = (
            f"{self.base_url}/{self.config.page_id}/conversations"
            f"?fields=id,snippet,unread_count,updated_time,participants"
            f"&access_token={page_token}"
        )
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.json()
                return data.get("data", [])

    async def fetch_messages(self, conversation_id: str, page_token: str, limit: int = 10) -> List[Dict]:
        """Recupere les messages d'une conversation."""
        import aiohttp

        url = (
            f"{self.base_url}/{conversation_id}/messages"
            f"?fields=id,message,from,created_time&limit={limit}"
            f"&access_token={page_token}"
        )
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.json()
                return data.get("data", [])

    async def send_message(self, recipient_id: str, text: str, page_token: str) -> Dict:
        """Envoie un message via Facebook Send API."""
        import aiohttp

        url = f"{self.base_url}/{self.config.page_id}/messages?access_token={page_token}"
        payload = {
            "recipient": {"id": recipient_id},
            "message": {"text": text},
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as resp:
                return await resp.json()

    async def send_template(self, recipient_id: str, template: Dict, page_token: str) -> Dict:
        """Envoie un template riche (boutons, carousel, etc.)."""
        import aiohttp

        url = f"{self.base_url}/{self.config.page_id}/messages?access_token={page_token}"
        payload = {
            "recipient": {"id": recipient_id},
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": template,
                }
            },
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as resp:
                return await resp.json()

    def build_services_template(self) -> Dict:
        """Template carousel des services."""
        return {
            "template_type": "generic",
            "elements": [
                {
                    "title": "Logo Pro",
                    "subtitle": "300k - 500k GNF | 48h-72h",
                    "buttons": [
                        {"type": "postback", "title": "Commander", "payload": "order_logo"}
                    ],
                },
                {
                    "title": "Affiche & Flyer",
                    "subtitle": "300k GNF | 24h-48h",
                    "buttons": [
                        {"type": "postback", "title": "Commander", "payload": "order_affiche"}
                    ],
                },
                {
                    "title": "Retouche Photo",
                    "subtitle": "Rendu 8K naturel | 24h-48h",
                    "buttons": [
                        {"type": "postback", "title": "Commander", "payload": "order_retouche"}
                    ],
                },
                {
                    "title": "Bots WhatsApp/Telegram",
                    "subtitle": "Automatisation complete | sur devis",
                    "buttons": [
                        {"type": "postback", "title": "Commander", "payload": "order_bots"}
                    ],
                },
            ],
        }

    def build_pricing_buttons(self) -> Dict:
        """Template boutons pour les tarifs."""
        return {
            "template_type": "button",
            "text": "Tarifs Komara Agency - choisis un service:",
            "buttons": [
                {"type": "postback", "title": "Logo", "payload": "price_logo"},
                {"type": "postback", "title": "Affiche", "payload": "price_affiche"},
                {"type": "postback", "title": "Tous les tarifs", "payload": "price_all"},
            ],
        }

    def update_conversation(self, conv_data: Dict) -> FacebookConversation:
        """Met a jour ou cree une conversation."""
        conv_id = conv_data.get("id", "")
        participants = conv_data.get("participants", {}).get("data", [])
        participant = next((p for p in participants if p.get("id") != self.config.page_id), participants[0] if participants else {})

        if conv_id not in self._conversations:
            self._conversations[conv_id] = FacebookConversation(
                conversation_id=conv_id,
                participant_id=participant.get("id", ""),
                participant_name=participant.get("name", ""),
            )

        conv = self._conversations[conv_id]
        conv.last_message = conv_data.get("snippet", "")
        conv.unread_count = conv_data.get("unread_count", 0)
        conv.read = conv.unread_count == 0

        return conv

    def get_unread(self) -> List[FacebookConversation]:
        """Retourne les conversations non lues."""
        return [c for c in self._conversations.values() if not c.read]

    def mark_read(self, conversation_id: str):
        if conversation_id in self._conversations:
            self._conversations[conversation_id].read = True
            self._conversations[conversation_id].unread_count = 0

    def get_stats(self) -> Dict:
        return {
            "page_id": self.config.page_id,
            "page_name": self.config.page_name,
            "total_conversations": len(self._conversations),
            "unread": len(self.get_unread()),
            "conversations": [
                {
                    "id": c.conversation_id,
                    "participant": c.participant_name,
                    "unread": c.unread_count,
                    "last_message": c.last_message[:50],
                }
                for c in self._conversations.values()
            ],
        }
