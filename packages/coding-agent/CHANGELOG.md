# Changelog

All notable changes to this package will be documented in this file.

## [Unreleased]

- Added MessageRouter with async message queue and retry logic
- Added middleware pipeline for incoming message processing
- Added Platform enum (telegram, facebook, instagram, whatsapp)
- Added MessageStatus tracking (pending, processing, sent, failed, retry)
- Added OutgoingMessage with configurable max_retries and exponential backoff
