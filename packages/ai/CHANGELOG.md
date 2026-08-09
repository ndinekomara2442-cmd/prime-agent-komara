# Changelog

All notable changes to this package will be documented in this file.

The format is based on the Prime Agent changelog format: a flat list of plain bullets under `## [Unreleased]`. No subsection headers.

## [Unreleased]

- Added intent detection engine with support for FR, Soussou, and Malinke keywords
- Added ConversationContext dataclass for per-session state tracking
- Added pricing, contact, portfolio, payment, delivery, and express intent handlers
- Changed ResponseEngine to use dataclass-based context instead of raw dicts
