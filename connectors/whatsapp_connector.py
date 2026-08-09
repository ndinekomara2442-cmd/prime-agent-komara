"""
Komara Agency — WhatsApp Business Connector
Connector pour WhatsApp Business API avec templates, sessions et automatisation.
"""

import logging
import time
from typing import Dict, Optional, List, Any
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger("komara.whatsapp")


class WhatsAppMessageType(str, Enum):
    TEXT = "text"
    TEMPLATE = "template"
    IMAGE = "image"
    DOCUMENT = "document"
    INTERACTIVE = "interactive"
    LOCATION = "location"


@dataclass
class WhatsAppConfig:
    phone_number_id: str = ""
    business_phone_number: str = "+212 701-986219"
    access_token: str = ""
    api_version: str = "v25.0"
    verify_token: str = "komara_verify_2026"


@dataclass
class WhatsAppSession:
    phone_number: str
    contact_name: str = ""
    state: str = "idle"  # idle, browsing, ordering, waiting_brief, waiting_photo
    history: List[Dict] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    last_interaction: float = field(default_factory=time.time)


class WhatsAppConnector:
    """Connector WhatsApp Business API avec gestion de sessions."""

    def __init__(self, config: WhatsAppConfig):
        self.config = config
        self.base_url = f"https://graph.facebook.com/{config.api_version}"
        self._sessions: Dict[str, WhatsAppSession] = {}
        self._templates: Dict[str, Dict] = {}
        self._register_templates()

    def _register_templates(self):
        """Enregistre les templates de messages WhatsApp Business."""
        self._templates = {
            "welcome": {
                "name": "komara_welcome",
                "language": {"code": "fr"},
                "components": [
                    {
                        "type": "body",
                        "parameters": [
                            {"type": "text", "text": "{{1}}"},  # Nom du client
                        ],
                    }
                ],
            },
            "order_confirmation": {
                "name": "komara_order_confirm",
                "language": {"code": "fr"},
                "components": [
                    {
                        "type": "body",
                        "parameters": [
                            {"type": "text", "text": "{{1}}"},  # Service
                            {"type": "text", "text": "{{2}}"},  # Prix
                            {"type": "text", "text": "{{3}}"},  # Delai
                        ],
                    }
                ],
            },
            "payment_reminder": {
                "name": "komara_payment_reminder",
                "language": {"code": "fr"},
                "components": [
                    {
                        "type": "body",
                        "parameters": [
                            {"type": "text", "text": "{{1}}"},  # Nom client
                            {"type": "text", "text": "{{2}}"},  # Montant
                        ],
                    }
                ],
            },
            "delivery_ready": {
                "name": "komara_delivery_ready",
                "language": {"code": "fr"},
                "components": [
                    {
                        "type": "body",
                        "parameters": [
                            {"type": "text", "text": "{{1}}"},  # Nom client
                            {"type": "text", "text": "{{2}}"},  # Type de projet
                        ],
                    }
                ],
            },
        }

    def get_session(self, phone_number: str, contact_name: str = "") -> WhatsAppSession:
        if phone_number not in self._sessions:
            self._sessions[phone_number] = WhatsAppSession(
                phone_number=phone_number,
                contact_name=contact_name,
            )
        session = self._sessions[phone_number]
        session.last_interaction = time.time()
        return session

    async def send_text(self, recipient_phone: str, text: str) -> Dict:
        """Envoie un message texte WhatsApp."""
        if not self.config.access_token:
            return {"error": "No access token configured"}

        import aiohttp
        url = f"{self.base_url}/{self.config.phone_number_id}/messages"
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_phone,
            "type": "text",
            "text": {"body": text},
        }
        headers = {
            "Authorization": f"Bearer {self.config.access_token}",
            "Content-Type": "application/json",
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as resp:
                return await resp.json()

    async def send_template(self, recipient_phone: str, template_name: str, params: List[str]) -> Dict:
        """Envoie un template WhatsApp Business approuve."""
        if not self.config.access_token:
            return {"error": "No access token configured"}

        template = self._templates.get(template_name)
        if not template:
            return {"error": f"Template {template_name} not found"}

        import aiohttp
        url = f"{self.base_url}/{self.config.phone_number_id}/messages"
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_phone,
            "type": "template",
            "template": {
                "name": template["name"],
                "language": template["language"],
                "components": [
                    {
                        "type": "body",
                        "parameters": [
                            {"type": "text", "text": param} for param in params
                        ],
                    }
                ],
            },
        }
        headers = {
            "Authorization": f"Bearer {self.config.access_token}",
            "Content-Type": "application/json",
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as resp:
                return await resp.json()

    async def send_interactive_menu(self, recipient_phone: str) -> Dict:
        """Envoie un menu interactif WhatsApp avec boutons."""
        if not self.config.access_token:
            return {"error": "No access token configured"}

        import aiohttp
        url = f"{self.base_url}/{self.config.phone_number_id}/messages"
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_phone,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "header": {"type": "text", "text": "Komara Agency"},
                "body": {"text": "Bienvenue! Choisis un service:"},
                "action": {
                    "button": "Voir les services",
                    "sections": [
                        {
                            "title": "Services",
                            "rows": [
                                {"id": "service_logo", "title": "Logo Pro", "description": "300k-500k GNF | 48h-72h"},
                                {"id": "service_affiche", "title": "Affiche & Flyer", "description": "300k GNF | 24h-48h"},
                                {"id": "service_retouche", "title": "Retouche Photo", "description": "Rendu 8K | 24h-48h"},
                                {"id": "service_bots", "title": "Bots IA", "description": "WhatsApp/Telegram | sur devis"},
                                {"id": "service_branding", "title": "Branding", "description": "Identite complete | sur devis"},
                                {"id": "service_video", "title": "Montage Video", "description": "Reels/TikTok | 24h-72h"},
                            ],
                        },
                        {
                            "title": "Infos",
                            "rows": [
                                {"id": "show_pricing", "title": "Voir les tarifs", "description": "Tous nos prix"},
                                {"id": "show_contact", "title": "Nous contacter", "description": "WhatsApp +212 701-986219"},
                                {"id": "show_portfolio", "title": "Portfolio", "description": "Voir nos travaux"},
                            ],
                        },
                    ],
                },
            },
        }
        headers = {
            "Authorization": f"Bearer {self.config.access_token}",
            "Content-Type": "application/json",
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as resp:
                return await resp.json()

    async def send_quick_reply_buttons(self, recipient_phone: str, text: str, buttons: List[Dict]) -> Dict:
        """Envoie des boutons de reponse rapide."""
        if not self.config.access_token:
            return {"error": "No access token configured"}

        import aiohttp
        url = f"{self.base_url}/{self.config.phone_number_id}/messages"
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_phone,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {"text": text},
                "action": {
                    "buttons": [
                        {
                            "type": "reply",
                            "reply": {"id": btn["id"], "title": btn["title"]},
                        }
                        for btn in buttons[:3]
                    ],
                },
            },
        }
        headers = {
            "Authorization": f"Bearer {self.config.access_token}",
            "Content-Type": "application/json",
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as resp:
                return await resp.json()

    def verify_webhook(self, mode: str, token: str, challenge: str) -> Optional[str]:
        """Verifie le webhook WhatsApp."""
        if mode == "subscribe" and token == self.config.verify_token:
            return challenge
        return None

    def get_stats(self) -> Dict:
        return {
            "phone_number": self.config.business_phone_number,
            "phone_number_id": self.config.phone_number_id or "not configured",
            "active_sessions": len(self._sessions),
            "templates": list(self._templates.keys()),
            "webhook_verify_token": self.config.verify_token,
        }
