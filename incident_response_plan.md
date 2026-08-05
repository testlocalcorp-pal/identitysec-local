# Security Incident Response Plan

Standard steps for triaging and reporting security incidents affecting the
IdentitySec platform. Use this plan when you suspect unauthorized access,
credential exposure, data leakage, or a compromise in any service managed from
this repository.

## Severity classification

| Level | Description | Examples |
|---|---|---|
| **Critical** | Active exploitation or confirmed credential/PCI exposure | Leaked JWT signing keys, raw card data in logs, unauthorized prod access |
| **High** | Likely compromise or broad service impact | Auth gateway bypass, billing API abuse, mass account lockouts |
| **Medium** | Suspicious activity with limited confirmed impact | Elevated failed logins, anomalous API traffic, misconfigured ingress |
| **Low** | Policy violation or latent risk with no active exploit | Secrets in a branch, missing security review on a merged PR |

## Triage steps

Complete these steps in order when an incident is reported or detected.

### 1. Acknowledge and contain

- [ ] Open an incident ticket and assign an incident commander.
- [ ] Notify `@identitysec/security` and the on-call engineer for affected
      services.
- [ ] **Do not** delete logs, traces, or deployment artifacts — preserve
      evidence for investigation.
- [ ] If credentials may be exposed, rotate affected keys/tokens immediately via
      the platform secret store (JWT signing keys, PSP keys, API keys).
- [ ] For auth incidents, consider invalidating active sessions via
      `apps/identity-api-gateway` controls.
- [ ] For billing/PCI concerns, isolate `apps/billing-service` and disable
      affected payment flows until scope is confirmed.

### 2. Assess scope

- [ ] Identify affected components using repo ownership (see
      `.github/CODEOWNERS`):
  - Auth: `apps/identity-api-gateway`
  - Billing/payments: `apps/billing-service`
  - Customer/admin UIs: `apps/customer-portal`, `apps/admin-console`
  - Infrastructure: `.infrastructure/`
  - Data pipelines: `data-platform/`
- [ ] Determine the time window of the incident (first suspicious event to
      present).
- [ ] Check whether prohibited data may have been logged or exported (see
      `security_notice.md`): tokens, passwords, PAN/CVV, or full
      `payment_token` values.
- [ ] Review structured logs, traces (`platform-packages/telemetry`), and
      relevant CI/deployment records for the incident window.

### 3. Investigate

- [ ] Collect correlation IDs, account IDs, IP ranges, and request paths from
      logs — redact sensitive values in incident notes.
- [ ] Compare recent deployments and config changes against
      `deployment_checklist.md` sign-off records.
- [ ] For data-platform incidents, inspect Kafka topics, Flink job state, and
      sink connector activity in `data-platform/`.
- [ ] Document hypotheses, evidence, and ruled-out causes in the incident
      ticket timeline.

### 4. Remediate

- [ ] Apply the minimum fix required to stop ongoing harm (patch, rollback,
      access revocation, WAF rule, etc.).
- [ ] Confirm remediation in staging before re-enabling production traffic
      where applicable.
- [ ] Run targeted smoke tests (`tests/automation/`, contract tests) on
      affected auth and billing paths.
- [ ] Verify no secrets or PCI data appear in post-remediation telemetry.

## Reporting

### Internal reporting

- [ ] Post status updates to the incident channel at least every 30 minutes
      during active triage (Critical/High) or hourly (Medium).
- [ ] Include: severity, affected services, current status, next action, and
      ETA for the next update.
- [ ] Escalate to `@identitysec/platform-devops` for infrastructure or
      `.infrastructure/` incidents.
- [ ] Escalate to `@identitysec/backend` for auth/billing service incidents.
- [ ] Escalate to `@identitysec/data-streaming` or `@identitysec/data-analytics`
      for pipeline or schema-related incidents.

### External and compliance reporting

- [ ] If PCI data or customer PII was exposed, notify `@identitysec/security`
      immediately for regulatory and customer notification assessment.
- [ ] Do not communicate externally (customers, press, partners) without
      security and legal approval.
- [ ] Record all notification decisions and timestamps in the incident ticket.

## Post-incident

- [ ] Hold a blameless post-incident review within five business days.
- [ ] Document root cause, timeline, impact, and corrective actions.
- [ ] Create follow-up tasks for detection gaps, missing reviews, or checklist
      failures identified during triage.
- [ ] Update relevant runbooks (`security_notice.md`, `deployment_checklist.md`,
      `audit_guidelines.md`) if process gaps were found.

## Related documents

- `security_notice.md` — logging and telemetry redaction rules
- `deployment_checklist.md` — pre-deployment security verification
- `audit_guidelines.md` — code review and telemetry audit practices
- `CONTRIBUTING.md` — security review and ownership requirements
- `.github/CODEOWNERS` — service and path ownership
