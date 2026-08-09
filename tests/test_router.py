"""
Tests pour le Message Router de Komara Agency.
"""

import pytest
import asyncio
from core.router import (
    MessageRouter,
    MessageQueue,
    IncomingMessage,
    OutgoingMessage,
    Platform,
    MessageStatus,
)


@pytest.fixture
def router():
    return MessageRouter()


@pytest.fixture
def incoming_msg():
    return IncomingMessage(
        platform=Platform.TELEGRAM,
        sender_id="12345",
        sender_name="Test User",
        text="salut",
    )


class TestMessageQueue:
    @pytest.mark.asyncio
    async def test_enqueue_dequeue(self):
        queue = MessageQueue()
        msg = OutgoingMessage(platform=Platform.TELEGRAM, recipient_id="123", text="test")
        assert await queue.enqueue(msg) is True
        dequeued = await queue.dequeue()
        assert dequeued.text == "test"

    def test_stats(self):
        queue = MessageQueue()
        assert queue.stats()["queue_size"] == 0


class TestMessageRouter:
    @pytest.mark.asyncio
    async def test_process_incoming_no_handler(self, router, incoming_msg):
        response = await router.process_incoming(incoming_msg)
        assert response is None

    @pytest.mark.asyncio
    async def test_process_incoming_with_handler(self, router, incoming_msg):
        async def handler(msg):
            return "Test response"

        router.register_handler(Platform.TELEGRAM, handler)
        response = await router.process_incoming(incoming_msg)
        assert response is not None
        assert response.text == "Test response"
        assert response.platform == Platform.TELEGRAM

    @pytest.mark.asyncio
    async def test_middleware(self, router, incoming_msg):
        async def middleware(msg):
            msg.text = "modified"
            return msg

        async def handler(msg):
            return f"Got: {msg.text}"

        router.add_middleware(middleware)
        router.register_handler(Platform.TELEGRAM, handler)
        response = await router.process_incoming(incoming_msg)
        assert response.text == "Got: modified"

    @pytest.mark.asyncio
    async def test_middleware_block(self, router, incoming_msg):
        async def blocking_middleware(msg):
            return None  # Block the message

        async def handler(msg):
            return "Should not reach"

        router.add_middleware(blocking_middleware)
        router.register_handler(Platform.TELEGRAM, handler)
        response = await router.process_incoming(incoming_msg)
        assert response is None
