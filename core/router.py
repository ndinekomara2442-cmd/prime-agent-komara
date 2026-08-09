"""
Komara Agency — Message Router
Route les messages entrants entre toutes les plateformes vers le bon agent.
Supporte le load balancing, les retries et la file d'attente.
"""

import asyncio
import json
import time
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, field
from enum import Enum


class Platform(str, Enum):
    TELEGRAM = "telegram"
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    WHATSAPP = "whatsapp"


class MessageStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SENT = "sent"
    FAILED = "failed"
    RETRY = "retry"


@dataclass
class IncomingMessage:
    platform: Platform
    sender_id: str
    sender_name: str
    text: str
    timestamp: float = field(default_factory=time.time)
    message_id: str = ""
    raw_data: Dict = field(default_factory=dict)


@dataclass
class OutgoingMessage:
    platform: Platform
    recipient_id: str
    text: str
    timestamp: float = field(default_factory=time.time)
    status: MessageStatus = MessageStatus.PENDING
    retry_count: int = 0
    max_retries: int = 3
    error: str = ""


class MessageQueue:
    """File d'attente asynchrone pour les messages sortants."""

    def __init__(self, max_size: int = 1000):
        self._queue: asyncio.Queue = asyncio.Queue(maxsize=max_size)
        self._history: List[OutgoingMessage] = []
        self._max_history = 500

    async def enqueue(self, message: OutgoingMessage) -> bool:
        try:
            self._queue.put_nowait(message)
            return True
        except asyncio.QueueFull:
            return False

    async def dequeue(self) -> OutgoingMessage:
        return await self._queue.get()

    def record(self, message: OutgoingMessage):
        self._history.append(message)
        if len(self._history) > self._max_history:
            self._history = self._history[-self._max_history:]

    def stats(self) -> Dict:
        return {
            "queue_size": self._queue.qsize(),
            "history_size": len(self._history),
            "sent": sum(1 for m in self._history if m.status == MessageStatus.SENT),
            "failed": sum(1 for m in self._history if m.status == MessageStatus.FAILED),
        }


class MessageRouter:
    """Routeur central qui distribue les messages vers les bons handlers."""

    def __init__(self):
        self._handlers: Dict[Platform, Callable] = {}
        self._queue = MessageQueue()
        self._middleware: List[Callable] = []
        self._running = False

    def register_handler(self, platform: Platform, handler: Callable):
        self._handlers[platform] = handler

    def add_middleware(self, middleware: Callable):
        self._middleware.append(middleware)

    async def process_incoming(self, message: IncomingMessage) -> Optional[OutgoingMessage]:
        """Traite un message entrant et génère une réponse."""
        for mw in self._middleware:
            message = await mw(message)
            if message is None:
                return None

        handler = self._handlers.get(message.platform)
        if not handler:
            return None

        response_text = await handler(message)
        if not response_text:
            return None

        return OutgoingMessage(
            platform=message.platform,
            recipient_id=message.sender_id,
            text=response_text,
        )

    async def send(self, message: OutgoingMessage) -> bool:
        """Envoie un message via le handler de la plateforme."""
        handler = self._handlers.get(message.platform)
        if not handler:
            message.status = MessageStatus.FAILED
            message.error = f"No handler for {message.platform}"
            return False

        try:
            success = await handler.send(message)
            message.status = MessageStatus.SENT if success else MessageStatus.FAILED
            self._queue.record(message)
            return success
        except Exception as e:
            message.status = MessageStatus.FAILED
            message.error = str(e)
            self._queue.record(message)
            return False

    async def send_with_retry(self, message: OutgoingMessage) -> bool:
        """Envoie avec retry automatique."""
        while message.retry_count < message.max_retries:
            success = await self.send(message)
            if success:
                return True
            message.retry_count += 1
            await asyncio.sleep(2 ** message.retry_count)

        message.status = MessageStatus.FAILED
        self._queue.record(message)
        return False

    async def start_worker(self):
        """Démarre le worker de la file d'attente."""
        self._running = True
        while self._running:
            message = await self._queue.dequeue()
            await self.send_with_retry(message)

    def stop(self):
        self._running = False

    def get_stats(self) -> Dict:
        return self._queue.stats()
