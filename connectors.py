"""
Komara Agency — Prime Agent Connectors
Connecte les bots Telegram, Facebook, Instagram et WhatsApp à Prime Agent.
"""

import json
import os
from typing import Dict, Optional


class KomaraConnectors:
    """Gestionnaire de connexions pour les agents Komara."""

    def __init__(self):
        self.agents = {
            "telegram": {
                "name": "Komara Telegram Bot",
                "username": "@Komara_Agency_botbot",
                "bot_id": "8787499105",
                "status": "active",
                "type": "realtime",
                "webhook": "komaraTelegramBot",
            },
            "facebook": {
                "name": "Komara Facebook Messenger",
                "page": "N-dine K fans",
                "page_id": "105344997852517",
                "status": "active",
                "type": "polling",
                "poll_schedule": "9h, 13h, 18h (GMT)",
                "webhook": "komaraFacebookBot",
            },
            "instagram": {
                "name": "Komara Instagram DM",
                "status": "pending",
                "type": "pending",
                "note": "Requires Instagram Business account linked to Facebook Page",
            },
            "whatsapp": {
                "name": "Komara WhatsApp Business",
                "number": "+212 701-986219",
                "status": "manual",
                "type": "manual",
            },
        }

    def get_agent(self, platform: str) -> Optional[Dict]:
        """Récupère la config d'un agent par plateforme."""
        return self.agents.get(platform.lower())

    def list_agents(self) -> Dict:
        """Liste tous les agents connectés."""
        return self.agents

    def get_active_agents(self) -> Dict:
        """Retourne seulement les agents actifs."""
        return {k: v for k, v in self.agents.items() if v.get("status") == "active"}

    def connect_agent(self, platform: str, config: Dict) -> str:
        """Connecte un nouvel agent ou met à jour la config."""
        self.agents[platform] = config
        return f"Agent {platform} connecté avec succès."

    def disconnect_agent(self, platform: str) -> str:
        """Déconnecte un agent."""
        if platform in self.agents:
            self.agents[platform]["status"] = "disconnected"
            return f"Agent {platform} déconnecté."
        return f"Agent {platform} introuvable."

    def get_routing_table(self) -> Dict:
        """Table de routage des messages entre agents."""
        return {
            "telegram": "komaraTelegramBot",
            "facebook": "komaraFacebookBot",
            "instagram": "komaraInstagramBot",
            "whatsapp": "komaraWhatsAppBot",
        }

    def health_check(self) -> Dict:
        """Vérifie l'état de tous les agents."""
        report = {}
        for platform, config in self.agents.items():
            report[platform] = {
                "name": config.get("name"),
                "status": config.get("status"),
                "type": config.get("type"),
            }
        return report


# Knowledge base partagée entre tous les agents
KOMARA_KNOWLEDGE = {
    "agency": {
        "name": "Komara Agency",
        "slogan": "Vision. Impact. Excellence.",
        "founder": "Ndine Komara",
        "location": "Guinée / Maroc",
        "whatsapp": "+212 701-986219",
        "email": "ndinekomara2442@gmail.com",
        "portfolio": "https://ndinekomara2442-cmd.github.io/komara-agency-portfolio/",
        "hours": "7j/7 de 8h à 22h (GMT)",
    },
    "services": {
        "logo": {"name": "Logo Pro", "price": "300k-500k GNF", "delivery": "48h-72h"},
        "affiche": {"name": "Affiche & Flyer", "price": "300k GNF", "delivery": "24h-48h"},
        "retouche": {"name": "Retouche Photo", "price": "sur discussion", "delivery": "24h-48h"},
        "bots": {"name": "Bots WhatsApp/Telegram", "price": "sur devis", "delivery": "sur discussion"},
        "branding": {"name": "Branding Complet", "price": "sur devis", "delivery": "sur discussion"},
        "video": {"name": "Montage Vidéo/Reels", "price": "sur devis", "delivery": "24h-72h"},
    },
    "pricing": {
        "express_surcharge": "+30%",
        "free_revisions": 2,
        "extra_revision_cost": "50k GNF",
    },
    "payment": ["Orange Money", "MTN Money", "Virement bancaire", "PayPal"],
    "languages": ["Français", "Soussou", "Malinké"],
}


if __name__ == "__main__":
    connectors = KomaraConnectors()

    print("=" * 60)
    print("Komara Agency — Prime Agent Connectors")
    print("=" * 60)

    print("\n📊 État des agents:")
    health = connectors.health_check()
    for platform, info in health.items():
        emoji = "✅" if info["status"] == "active" else "⏳" if info["status"] == "pending" else "❌"
        print(f"  {emoji} {platform}: {info['name']} ({info['status']})")

    print("\n🔀 Table de routage:")
    for src, dst in connectors.get_routing_table().items():
        print(f"  {src} → {dst}")

    print("\n📚 Knowledge Base:")
    print(json.dumps(KOMARA_KNOWLEDGE["agency"], indent=2, ensure_ascii=False))
