# AGENTS.md

Instructions for AI coding agents working in this repository.
See `agent.md` for full development rules and conventions.

## Quick Reference

- This is the Komara Agency multi-platform bot integration repo, built on the Prime Agent RLM framework.
- Core logic lives in `core/` (router, AI engine). Platform connectors live in `connectors/`.
- Read `agent.md` before making any code, commit, or PR changes.
- Read files in full before wide-ranging edits. Do not rely on search snippets alone.
- No emojis in commits, issues, PR comments, or code.
- Run tests from the package root: `pytest tests/ -v`.
- Never commit secrets. Use `.env.example` as the template; real values go in `.env` (gitignored).

## Structure

```
prime-agent-komara/
  core/            # Message router, AI response engine
  connectors/      # Telegram, Facebook, Instagram, WhatsApp connectors
  scripts/         # Setup and maintenance scripts
  assets/brand/    # Logos, brand assets
  tests/           # Test suite
  main.py          # Orchestrator entry point
```

## Before Committing

1. Read the full `agent.md` rules.
2. Only stage files you changed (`git add <specific-files>`, never `git add -A`).
3. Run `pytest tests/ -v` and fix failures before committing.
4. Keep commit messages short, technical, no emojis.
