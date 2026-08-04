# Security Logging Protocol

This document describes how IdentitySec services must handle application logging
so that operational visibility does not introduce data or credential exposure.

## Structured logging

Python services should use the shared logger in `platform-packages/logger`,
which emits structured JSON to stdout (`level`, `msg`, `logger`). Prefer this
over ad-hoc `print` or unstructured log lines so logs can be parsed consistently
by the platform observability stack.

## Never log sensitive data

The following must **never** appear in logs, metrics labels, or trace attributes:

- Raw payment card numbers, CVV, or full PAN data
- Plaintext passwords or MFA codes
- Session cookies, JWTs, API keys, or other long-lived secrets
- Full `payment_token` values from the PSP (tokenized references only)

`apps/billing-service` is in PCI scope. That service must not log raw card data
under any circumstance. Log customer identifiers and charge metadata only (for
example, `customer_id`, `amount_cents`, operation status).

## Auth and token handling

`apps/identity-api-gateway` issues and verifies auth tokens for the platform.
Do not log bearer tokens, refresh tokens, or authorization headers. Log
high-level auth events (success/failure, route, correlation ID) without
credential payloads.

## Review requirements

Changes to logging in the following areas require explicit security review per
`CONTRIBUTING.md`:

- `apps/billing-service`
- `apps/identity-api-gateway`

When adding new log statements, ask: *Would this line be safe if exported to a
third-party log aggregator or shown in a support ticket?* If not, redact or
omit the field.

## Telemetry

Distributed tracing is configured via `platform-packages/telemetry`. Apply the
same redaction rules to span attributes and tags as to log messages.
