"""
Tests pour le AI Response Engine de Komara Agency.
"""

import pytest
from core.ai_engine import ResponseEngine, ConversationContext, IntentDetector


@pytest.fixture
def engine():
    return ResponseEngine()


@pytest.fixture
def context():
    return ConversationContext(
        sender_id="12345",
        sender_name="Test User",
        platform="telegram",
        history=[],
    )


class TestIntentDetector:
    def test_greeting(self):
        assert IntentDetector.detect("salut") == "greeting"
        assert IntentDetector.detect("bonjour") == "greeting"
        assert IntentDetector.detect("salam") == "greeting"
        assert IntentDetector.detect("hello") == "greeting"

    def test_logo(self):
        assert IntentDetector.detect("je veux un logo") == "logo"
        assert IntentDetector.detect("logo pro") == "logo"

    def test_pricing(self):
        assert IntentDetector.detect("combien ca coute") == "pricing"
        assert IntentDetector.detect("quel est le prix") == "pricing"
        assert IntentDetector.detect("tarif") == "pricing"

    def test_order(self):
        assert IntentDetector.detect("je veux commander") == "order"
        assert IntentDetector.detect("commander un logo") == "order"

    def test_contact(self):
        assert IntentDetector.detect("contact") == "contact"
        assert IntentDetector.detect("numero de telephone") == "contact"

    def test_unknown(self):
        assert IntentDetector.detect("xyzabc random text") == "unknown"


class TestResponseEngine:
    def test_greeting_response(self, engine, context):
        response = engine.generate(context, "salut")
        assert response is not None
        assert "Komara Agency" in response
        assert "Logo" in response

    def test_logo_response(self, engine, context):
        response = engine.generate(context, "je veux un logo")
        assert response is not None
        assert "300k" in response
        assert "500k" in response

    def test_pricing_response(self, engine, context):
        response = engine.generate(context, "combien")
        assert response is not None
        assert "300k" in response
        assert "Orange Money" in response

    def test_contact_response(self, engine, context):
        response = engine.generate(context, "contact")
        assert response is not None
        assert "+212" in response

    def test_unknown_response(self, engine, context):
        response = engine.generate(context, "xyzabc")
        assert response is not None
        assert "compris" in response

    def test_history_tracking(self, engine, context):
        engine.generate(context, "salut")
        assert len(context.history) == 0  # history is tracked by orchestrator, not engine
        assert context.intent == "greeting"
