# @komara/ai

AI provider abstraction layer for Komara Agency bots.

## Features

- Intent detection (FR, Soussou, Malinke)
- Response generation engine
- Conversation context management
- Knowledge base: services, pricing, contact info

## Usage

```python
from packages.ai.src.response_engine import ResponseEngine, ConversationContext

engine = ResponseEngine()
ctx = ConversationContext(sender_id="123", sender_name="Client", platform="telegram", history=[])
response = engine.generate(ctx, "je veux un logo")
```

## Structure

```
packages/ai/
  src/
    types.ts          # Shared types (API, StreamOptions, Model)
    response_engine.py  # Response generation
    intent_detector.py  # Intent detection
    knowledge_base.py   # Services, pricing, contact data
  test/
    test_ai_engine.py # Tests
  CHANGELOG.md
  package.json
  tsconfig.json
```
