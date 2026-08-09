"""
Komara Agency — AI Response Engine
Génère des réponses intelligentes basées sur le contexte et l'historique.
"""

import re
from typing import Optional, List, Dict
from dataclasses import dataclass


@dataclass
class ConversationContext:
    sender_id: str
    sender_name: str
    platform: str
    history: List[Dict]  # [{"role": "user"|"agent", "text": "..."}]
    intent: str = ""
    language: str = "fr"


# Knowledge base
SERVICES = {
    "logo": {
        "name": "Logo Pro",
        "price": "300k - 500k GNF",
        "delivery": "48h-72h",
        "includes": "2 propositions + 2 revisions gratuites",
    },
    "affiche": {
        "name": "Affiche & Flyer",
        "price": "300k GNF",
        "delivery": "24h-48h",
        "includes": "2 revisions gratuites",
    },
    "retouche": {
        "name": "Retouche Photo",
        "price": "sur discussion",
        "delivery": "24h-48h",
        "includes": "Rendu 8K naturel",
    },
    "bots": {
        "name": "Bots WhatsApp/Telegram",
        "price": "sur devis",
        "delivery": "sur discussion",
        "includes": "Automatisation complete",
    },
    "branding": {
        "name": "Branding Complet",
        "price": "sur devis",
        "delivery": "sur discussion",
        "includes": "Logo, couleurs, typographie, guidelines",
    },
    "video": {
        "name": "Montage Video/Reels",
        "price": "sur devis",
        "delivery": "24h-72h",
        "includes": "Reels Instagram, TikTok, videos promos",
    },
}

PRICING = {
    "express_surcharge": "+30%",
    "free_revisions": 2,
    "extra_revision_cost": "50k GNF",
    "payment_methods": ["Orange Money", "MTN Money", "Virement bancaire", "PayPal"],
}

CONTACT = {
    "whatsapp": "+212 701-986219",
    "email": "ndinekomara2442@gmail.com",
    "portfolio": "https://ndinekomara2442-cmd.github.io/komara-agency-portfolio/",
    "hours": "7j/7 de 8h a 22h (GMT)",
    "slogan": "Vision. Impact. Excellence.",
}


class IntentDetector:
    """Detecte l'intention du message client."""

    INTENT_PATTERNS = {
        "greeting": [
            r"\b(salut|salam|bonjour|hello|slt|coucou|bonsoir|cc)\b",
            r"\b( iyi gun| iyi morning)\b",
        ],
        "logo": [r"\b(logo|logotype|identite)\b", r"\b1\b"],
        "affiche": [r"\b(affiche|flyer|poster|affichage)\b", r"\b2\b"],
        "retouche": [r"\b(retouche|photo|image|edit)\b", r"\b3\b"],
        "bots": [r"\b(bot|automatisation|robot|auto)\b", r"\b4\b"],
        "branding": [r"\b(branding|marque|charte|identite visuelle)\b", r"\b5\b"],
        "video": [r"\b(video|reel|tiktok|montage|clip)\b", r"\b6\b"],
        "pricing": [r"\b(prix|tarif|combien|cout|cher|budget)\b"],
        "order": [r"\b(commander|commande|je veux|je souhaite|demander)\b"],
        "contact": [r"\b(contact|telephone|numero|whatsapp|joindre)\b"],
        "portfolio": [r"\b(portfolio|portfolio|travaux|realisations|site)\b"],
        "payment": [r"\b(paiement|payer|orange money|mtn|virement|paypal)\b"],
        "delivery": [r"\b(delai|quand|livraison|temps|rapidite)\b"],
        "thanks": [r"\b(merci|thanks|thank you|baraka)\b"],
        "express": [r"\b(express|urgent|rapidement|vite|aujourd)\b"],
    }

    @classmethod
    def detect(cls, text: str) -> str:
        text_lower = text.lower().strip()
        for intent, patterns in cls.INTENT_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    return intent
        return "unknown"


class ResponseEngine:
    """Genere des reponses basees sur l'intention et le contexte."""

    def __init__(self):
        self.detector = IntentDetector()

    def generate(self, context: ConversationContext, message_text: str) -> Optional[str]:
        intent = self.detector.detect(message_text)
        context.intent = intent

        # Detecter la langue
        if re.search(r"\b(iyi|gun|morning|soussou|malinke)\b", message_text.lower()):
            context.language = "local"

        handler = self._get_handler(intent)
        if handler:
            return handler(context, message_text)
        return self._handle_unknown(context, message_text)

    def _get_handler(self, intent: str):
        handlers = {
            "greeting": self._handle_greeting,
            "logo": self._handle_logo,
            "affiche": self._handle_affiche,
            "retouche": self._handle_retouche,
            "bots": self._handle_bots,
            "branding": self._handle_branding,
            "video": self._handle_video,
            "pricing": self._handle_pricing,
            "order": self._handle_order,
            "contact": self._handle_contact,
            "portfolio": self._handle_portfolio,
            "payment": self._handle_payment,
            "delivery": self._handle_delivery,
            "thanks": self._handle_thanks,
            "express": self._handle_express,
        }
        return handlers.get(intent)

    def _handle_greeting(self, ctx, text):
        return (
            "Salut! Bienvenue chez Komara Agency\n\n"
            "Je suis Ndine, ton createur digital.\n\n"
            "1. Logo pro\n"
            "2. Affiche & Flyer\n"
            "3. Retouche photo\n"
            "4. Bots WhatsApp/Telegram\n"
            "5. Branding complet\n"
            "6. Montage video/Reels\n\n"
            "Tape le numero du service qui t'interesse"
        )

    def _handle_logo(self, ctx, text):
        s = SERVICES["logo"]
        return (
            f"Logo Pro\n\n"
            f"Logo unique et sur mesure pour ta marque.\n\n"
            f"Tarif: {s['price']}\n"
            f"Delai: {s['delivery']}\n"
            f"Inclus: {s['includes']}\n"
            f"Express 24h: {PRICING['express_surcharge']}\n\n"
            f"Tape 'commander' pour lancer"
        )

    def _handle_affiche(self, ctx, text):
        s = SERVICES["affiche"]
        return (
            f"Affiche & Flyer\n\n"
            f"Design percutant pour tes evenements.\n\n"
            f"Tarif: {s['price']}\n"
            f"Delai: {s['delivery']}\n"
            f"Inclus: {s['includes']}\n"
            f"Express 24h: {PRICING['express_surcharge']}\n\n"
            f"Tape 'commander' pour lancer"
        )

    def _handle_retouche(self, ctx, text):
        s = SERVICES["retouche"]
        return (
            f"Retouche Photo\n\n"
            f"Retouche pro: fond, lumiere, couleur, peau.\n"
            f"Rendu {s['includes']}.\n\n"
            f"Tarif: {s['price']}\n"
            f"Delai: {s['delivery']}\n\n"
            f"Envoie ta photo"
        )

    def _handle_bots(self, ctx, text):
        s = SERVICES["bots"]
        return (
            f"Bots WhatsApp/Telegram\n\n"
            f"Automatise ta communication client:\n"
            f"- Messages de bienvenue\n"
            f"- Reponses automatiques\n"
            f"- Relances de paiement\n"
            f"- Suivi de commandes\n\n"
            f"Tarif: {s['price']}\n"
            f"Tape 'commander'"
        )

    def _handle_branding(self, ctx, text):
        s = SERVICES["branding"]
        return (
            f"Branding Complet\n\n"
            f"Identite visuelle complete:\n"
            f"- Logo, couleurs, typographie\n"
            f"- Guidelines de marque\n\n"
            f"Tarif: {s['price']}\n"
            f"Tape 'commander'"
        )

    def _handle_video(self, ctx, text):
        s = SERVICES["video"]
        return (
            f"Montage Video/Reels\n\n"
            f"Reels Instagram, TikTok et videos promos.\n\n"
            f"Tarif: {s['price']}\n"
            f"Delai: {s['delivery']}\n\n"
            f"Tape 'commander'"
        )

    def _handle_pricing(self, ctx, text):
        lines = ["Tarifs Komara Agency", ""]
        for key, s in SERVICES.items():
            lines.append(f"{s['name']}: {s['price']}")
        lines.extend([
            "",
            f"2 revisions gratuites",
            f"Revision sup: {PRICING['extra_revision_cost']}",
            f"Express 24h: {PRICING['express_surcharge']}",
            f"Paiement: {', '.join(PRICING['payment_methods'])}",
        ])
        return "\n".join(lines)

    def _handle_order(self, ctx, text):
        return (
            "Super! Pour lancer ta commande:\n\n"
            "1. Type de projet (logo, affiche...)\n"
            "2. Description de ce que tu veux\n"
            "3. Delai souhaite (normal ou express 24h)\n\n"
            "Ecris les details ici"
        )

    def _handle_contact(self, ctx, text):
        return (
            f"Contact Komara Agency\n\n"
            f"WhatsApp: {CONTACT['whatsapp']}\n"
            f"Email: {CONTACT['email']}\n"
            f"Portfolio: {CONTACT['portfolio']}\n\n"
            f"{CONTACT['hours']}"
        )

    def _handle_portfolio(self, ctx, text):
        return (
            f"Portfolio Komara Agency\n\n"
            f"Decouvre mes travaux ici:\n"
            f"{CONTACT['portfolio']}"
        )

    def _handle_payment(self, ctx, text):
        methods = "\n".join(f"{i+1}. {m}" for i, m in enumerate(PRICING["payment_methods"]))
        return (
            f"Modes de paiement\n\n"
            f"{methods}\n\n"
            f"Le paiement se fait apres validation du devis."
        )

    def _handle_delivery(self, ctx, text):
        return (
            f"Delais de livraison\n\n"
            f"Normal: 24h-72h selon le projet\n"
            f"Express 24h: {PRICING['express_surcharge']} sur le tarif\n\n"
            f"Le delai commence apres validation du devis et paiement."
        )

    def _handle_thanks(self, ctx, text):
        return f"Avec plaisir! Komara Agency - {CONTACT['slogan']}"

    def _handle_express(self, ctx, text):
        return (
            f"Service Express 24h\n\n"
            f"Majoration: {PRICING['express_surcharge']}\n"
            f"Tu as besoin d'un projet en urgence?\n\n"
            f"Tape 'commander' avec ton brief"
        )

    def _handle_unknown(self, ctx, text):
        return (
            "Je n'ai pas bien compris\n\n"
            "Tape: logo, affiche, prix, commander, ou contact"
        )
