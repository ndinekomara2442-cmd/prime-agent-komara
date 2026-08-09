"""
Komara Agency — Telegram Connector
Connector avancé pour le bot Telegram avec gestion de sessions,
callbacks inline keyboard et commandes riches.
"""

import json
import logging
from typing import Dict, Optional, Callable, Any, List
from dataclasses import dataclass

logger = logging.getLogger("komara.telegram")


@dataclass
class TelegramConfig:
    bot_token: str
    bot_username: str = "@Komara_Agency_botbot"
    bot_id: str = "8787499105"
    webhook_url: str = ""
    allowed_updates: List[str] = None

    def __post_init__(self):
        if self.allowed_updates is None:
            self.allowed_updates = ["message", "callback_query"]


class InlineKeyboardBuilder:
    """Construit des claviers inline Telegram."""

    def __init__(self):
        self._keyboard: List[List[Dict]] = []

    def add_row(self, buttons: List[Dict]):
        self._keyboard.append(buttons)
        return self

    def add_url_button(self, text: str, url: str):
        self._keyboard.append([{"text": text, "url": url}])
        return self

    def add_callback_button(self, text: str, callback_data: str):
        self._keyboard.append([{"text": text, "callback_data": callback_data}])
        return self

    def add_services_menu(self):
        """Menu principal des services."""
        self._keyboard = [
            [{"text": "Logo Pro", "callback_data": "service_logo"},
             {"text": "Affiche/Flyer", "callback_data": "service_affiche"}],
            [{"text": "Retouche Photo", "callback_data": "service_retouche"},
             {"text": "Bots IA", "callback_data": "service_bots"}],
            [{"text": "Branding", "callback_data": "service_branding"},
             {"text": "Montage Video", "callback_data": "service_video"}],
            [{"text": "Voir les tarifs", "callback_data": "show_pricing"},
             {"text": "Nous contacter", "callback_data": "show_contact"}],
        ]
        return self

    def add_order_actions(self):
        """Actions pour une commande."""
        self._keyboard = [
            [{"text": "Commander maintenant", "callback_data": "start_order"}],
            [{"text": "Voir le portfolio", "url": "https://ndinekomara2442-cmd.github.io/komara-agency-portfolio/"}],
            [{"text": "Retour au menu", "callback_data": "main_menu"}],
        ]
        return self

    def build(self) -> Dict:
        return {"inline_keyboard": self._keyboard}


class TelegramSession:
    """Session utilisateur Telegram avec historique et etat."""

    def __init__(self, chat_id: str, user_name: str = ""):
        self.chat_id = chat_id
        self.user_name = user_name
        self.state: str = "idle"  # idle, ordering, waiting_photo, waiting_brief
        self.history: List[Dict] = []
        self.context: Dict[str, Any] = {}
        self.last_interaction: float = 0

    def add_message(self, role: str, text: str):
        self.history.append({"role": role, "text": text})
        if len(self.history) > 50:
            self.history = self.history[-50:]

    def set_state(self, state: str, **context):
        self.state = state
        self.context.update(context)


class TelegramConnector:
    """Connector Telegram avec gestion de sessions et callbacks."""

    def __init__(self, config: TelegramConfig):
        self.config = config
        self.base_url = f"https://api.telegram.org/bot{config.bot_token}"
        self._sessions: Dict[str, TelegramSession] = {}
        self._callback_handlers: Dict[str, Callable] = {}
        self._register_callbacks()

    def _register_callbacks(self):
        self._callback_handlers = {
            "main_menu": self._cb_main_menu,
            "service_logo": self._cb_service_logo,
            "service_affiche": self._cb_service_affiche,
            "service_retouche": self._cb_service_retouche,
            "service_bots": self._cb_service_bots,
            "service_branding": self._cb_service_branding,
            "service_video": self._cb_service_video,
            "show_pricing": self._cb_show_pricing,
            "show_contact": self._cb_show_contact,
            "start_order": self._cb_start_order,
        }

    def get_session(self, chat_id: str, user_name: str = "") -> TelegramSession:
        if chat_id not in self._sessions:
            self._sessions[chat_id] = TelegramSession(chat_id, user_name)
        return self._sessions[chat_id]

    def handle_update(self, update: Dict) -> Optional[Dict]:
        """Traite un update Telegram (message ou callback_query)."""
        if "callback_query" in update:
            return self._handle_callback(update["callback_query"])
        elif "message" in update:
            return self._handle_message(update["message"])
        return None

    def _handle_message(self, message: Dict) -> Optional[Dict]:
        chat_id = str(message.get("chat", {}).get("id", ""))
        text = message.get("text", "")
        user_name = message.get("from", {}).get("first_name", "")

        session = self.get_session(chat_id, user_name)
        session.add_message("user", text)

        if text.startswith("/"):
            return self._handle_command(chat_id, text, session)

        return {
            "chat_id": chat_id,
            "text": text,
            "session": session,
        }

    def _handle_callback(self, callback: Dict) -> Optional[Dict]:
        data = callback.get("data", "")
        chat_id = str(callback.get("message", {}).get("chat", {}).get("id", ""))
        user_name = callback.get("from", {}).get("first_name", "")
        query_id = callback.get("id", "")

        session = self.get_session(chat_id, user_name)

        handler = self._callback_handlers.get(data)
        if handler:
            result = handler(session)
            return {
                "chat_id": chat_id,
                "query_id": query_id,
                "text": result.get("text", ""),
                "keyboard": result.get("keyboard"),
                "session": session,
            }
        return None

    def _handle_command(self, chat_id: str, text: str, session: TelegramSession) -> Dict:
        cmd = text.split()[0].lower()
        if cmd == "/start":
            session.set_state("idle")
            keyboard = InlineKeyboardBuilder().add_services_menu().build()
            return {
                "chat_id": chat_id,
                "text": (
                    "Salut! Bienvenue chez Komara Agency\n\n"
                    "Je suis Ndine, ton createur digital.\n\n"
                    "Choisis un service dans le menu ci-dessous"
                ),
                "keyboard": keyboard,
                "session": session,
            }
        elif cmd == "/help":
            return {
                "chat_id": chat_id,
                "text": (
                    "Commandes disponibles:\n\n"
                    "/start - Menu principal\n"
                    "/services - Liste des services\n"
                    "/prix - Voir les tarifs\n"
                    "/contact - Nous contacter\n"
                    "/portfolio - Voir nos travaux\n"
                    "/commander - Lancer une commande"
                ),
                "session": session,
            }
        elif cmd == "/services":
            keyboard = InlineKeyboardBuilder().add_services_menu().build()
            return {
                "chat_id": chat_id,
                "text": "Voici nos services:",
                "keyboard": keyboard,
                "session": session,
            }
        elif cmd == "/prix":
            return {
                "chat_id": chat_id,
                "text": self._cb_show_pricing(session).get("text", ""),
                "session": session,
            }
        elif cmd == "/contact":
            return {
                "chat_id": chat_id,
                "text": self._cb_show_contact(session).get("text", ""),
                "session": session,
            }
        elif cmd == "/portfolio":
            return {
                "chat_id": chat_id,
                "text": "Portfolio: https://ndinekomara2442-cmd.github.io/komara-agency-portfolio/",
                "session": session,
            }
        return {
            "chat_id": chat_id,
            "text": "Commande inconnue. Tape /help pour voir les commandes.",
            "session": session,
        }

    # Callback handlers
    def _cb_main_menu(self, session):
        keyboard = InlineKeyboardBuilder().add_services_menu().build()
        return {
            "text": "Menu principal - choisis un service:",
            "keyboard": keyboard,
        }

    def _cb_service_logo(self, session):
        keyboard = InlineKeyboardBuilder().add_order_actions().build()
        return {
            "text": (
                "Logo Pro\n\n"
                "Logo unique et sur mesure pour ta marque.\n\n"
                "Tarif: 300k - 500k GNF\n"
                "Delai: 48h-72h\n"
                "Inclus: 2 propositions + 2 revisions gratuites\n"
                "Express 24h: +30%"
            ),
            "keyboard": keyboard,
        }

    def _cb_service_affiche(self, session):
        keyboard = InlineKeyboardBuilder().add_order_actions().build()
        return {
            "text": (
                "Affiche & Flyer\n\n"
                "Design percutant pour tes evenements.\n\n"
                "Tarif: 300k GNF\n"
                "Delai: 24h-48h\n"
                "Inclus: 2 revisions gratuites\n"
                "Express 24h: +30%"
            ),
            "keyboard": keyboard,
        }

    def _cb_service_retouche(self, session):
        keyboard = InlineKeyboardBuilder().add_order_actions().build()
        return {
            "text": (
                "Retouche Photo\n\n"
                "Retouche pro: fond, lumiere, couleur, peau.\n"
                "Rendu 8K naturel.\n\n"
                "Tarif: sur discussion\n"
                "Delai: 24h-48h\n\n"
                "Envoie ta photo"
            ),
            "keyboard": keyboard,
        }

    def _cb_service_bots(self, session):
        keyboard = InlineKeyboardBuilder().add_order_actions().build()
        return {
            "text": (
                "Bots WhatsApp/Telegram\n\n"
                "Automatise ta communication client:\n"
                "- Messages de bienvenue\n"
                "- Reponses automatiques\n"
                "- Relances de paiement\n"
                "- Suivi de commandes\n\n"
                "Tarif: sur devis"
            ),
            "keyboard": keyboard,
        }

    def _cb_service_branding(self, session):
        keyboard = InlineKeyboardBuilder().add_order_actions().build()
        return {
            "text": (
                "Branding Complet\n\n"
                "Identite visuelle complete:\n"
                "- Logo, couleurs, typographie\n"
                "- Guidelines de marque\n\n"
                "Tarif: sur devis"
            ),
            "keyboard": keyboard,
        }

    def _cb_service_video(self, session):
        keyboard = InlineKeyboardBuilder().add_order_actions().build()
        return {
            "text": (
                "Montage Video/Reels\n\n"
                "Reels Instagram, TikTok et videos promos.\n\n"
                "Tarif: sur devis\n"
                "Delai: 24h-72h"
            ),
            "keyboard": keyboard,
        }

    def _cb_show_pricing(self, session):
        return {
            "text": (
                "Tarifs Komara Agency\n\n"
                "Logo: 300k - 500k GNF\n"
                "Affiche: 300k GNF\n"
                "Retouche: sur discussion\n"
                "Bots: sur devis\n"
                "Branding: sur devis\n"
                "Video: sur devis\n\n"
                "2 revisions gratuites\n"
                "Revision sup: 50k GNF\n"
                "Express 24h: +30%\n"
                "Paiement: Orange Money, MTN, Virement, PayPal"
            ),
        }

    def _cb_show_contact(self, session):
        return {
            "text": (
                "Contact Komara Agency\n\n"
                "WhatsApp: +212 701-986219\n"
                "Portfolio: https://ndinekomara2442-cmd.github.io/komara-agency-portfolio/\n\n"
                "7j/7 de 8h a 22h (GMT)"
            ),
        }

    def _cb_start_order(self, session):
        session.set_state("waiting_brief")
        return {
            "text": (
                "Super! Pour lancer ta commande:\n\n"
                "1. Type de projet (logo, affiche...)\n"
                "2. Description de ce que tu veux\n"
                "3. Delai souhaite (normal ou express 24h)\n\n"
                "Ecris les details ici"
            ),
        }

    def get_stats(self) -> Dict:
        return {
            "bot_id": self.config.bot_id,
            "bot_username": self.config.bot_username,
            "active_sessions": len(self._sessions),
            "sessions": list(self._sessions.keys()),
        }
