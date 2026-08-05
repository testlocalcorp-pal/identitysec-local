# Repository Audit Guidelines

Standard practices for code review and telemetry auditing across the
IdentitySec monorepo. Use this checklist during PR review and periodic
compliance audits.

## Code review

### Scope and ownership

- Changes should stay within the authoring team's directory unless the work is
  explicitly cross-cutting (shared schemas in `data-platform/schemas/`, or a
  `platform-packages/` library bump).
- Confirm the correct `CODEOWNERS` group has approved the PR.
- Cross-team changes require review from **both** affected owner groups.

### Mandatory security review

Every PR touching these paths requires `@identitysec/security` approval:

- `apps/billing-service` — subscription and payment data (PCI scope)
- `apps/identity-api-gateway` — token issuance, verification, and auth ingress

### Platform and infrastructure

- All `.infrastructure/` changes require `@identitysec/platform-devops` approval,
  regardless of who authored them.
- Verify Terraform, Kubernetes, and Docker changes do not introduce hard-coded
  secrets or overly broad IAM/network permissions.

### Review checklist

For each PR, reviewers should confirm:

1. **Correctness** — logic matches the stated intent; edge cases are handled.
2. **Tests** — affected paths have appropriate coverage (`tests/automation/`,
   contract tests, or service-level tests where applicable).
3. **CI** — the relevant workflow runs for changed paths (see
   `.github/workflows/`).
4. **Dependencies** — new packages are justified; shared libraries in
   `platform-packages/` remain backward compatible or version bumps are
   documented.
5. **Data contracts** — schema or event changes in `data-platform/schemas/` are
   reviewed by both streaming and analytics owners when both pipelines consume
   the data.

## Telemetry audit

Telemetry covers application logs, distributed traces, and metrics exported
from services in this repository.

### Logging standards

- Python services must use `platform-packages/logger` for structured JSON output.
- Audit log statements for prohibited content (see `security_notice.md`):
  - No raw card data, passwords, MFA codes, or full tokens
  - No bearer tokens, session cookies, or API keys in log messages
- Billing-service logs may include `customer_id`, `amount_cents`, and operation
  status — never full `payment_token` values or PAN data.

### Tracing and metrics

- Services using `platform-packages/telemetry` must apply the same redaction
  rules to span attributes and metric labels as to log lines.
- Verify new instrumentation does not attach PII or credentials to traces.
- Confirm high-cardinality or sensitive fields are not used as metric labels.

### Telemetry audit checklist

During a telemetry audit, verify:

1. **Coverage** — critical auth, billing, and data-pipeline paths emit
   structured logs and traces at appropriate levels.
2. **Redaction** — sample recent log and trace output in staging; confirm no
   secrets or PCI data appear.
3. **Consistency** — log fields use stable names (`level`, `msg`, `logger`) so
   downstream aggregators can parse them reliably.
4. **Change control** — logging or tracing changes in billing and auth services
   were reviewed by security per `CONTRIBUTING.md`.

## Related documents

- `CONTRIBUTING.md` — team boundaries and review requirements
- `security_notice.md` — security logging protocol
- `.github/CODEOWNERS` — path ownership
- `.github/workflows/` — CI scope per changed area
