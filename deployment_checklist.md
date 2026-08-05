# Deployment Security Checklist

Pre-deployment verification steps for releases from this repository. Complete
this checklist before promoting changes to staging or production.

## Code and review gates

- [ ] All required CI workflows passed for changed paths (see
      `.github/workflows/`).
- [ ] `CODEOWNERS` approvals are in place for every touched area.
- [ ] Changes to `apps/billing-service` or `apps/identity-api-gateway` include
      `@identitysec/security` review.
- [ ] Changes to `.infrastructure/` include `@identitysec/platform-devops`
      approval.
- [ ] Cross-team schema or shared-library changes were reviewed by all affected
      owner groups per `CONTRIBUTING.md`.

## Secrets and configuration

- [ ] No secrets, API keys, tokens, or credentials are committed in source
      files, Dockerfiles, Terraform, or Kubernetes manifests.
- [ ] Runtime secrets are injected via the platform secret store — not baked
      into container images or config maps.
- [ ] Environment-specific values (database URLs, PSP keys, JWT signing keys)
      are verified for the target environment only.
- [ ] `.env` or local credential files are not included in the deployment
      artifact.

## Application security

### Auth services (`apps/identity-api-gateway`)

- [ ] Token issuance and verification paths behave correctly in staging.
- [ ] No bearer tokens, refresh tokens, or authorization headers are logged.
- [ ] Session and routing rules match the intended release scope.

### Billing (`apps/billing-service`)

- [ ] PCI scope controls remain intact — no raw card data in logs or responses.
- [ ] Only tokenized payment references (`payment_token`) are handled; PAN/CVV
      never appear in code paths or telemetry.
- [ ] Subscription charge flows were smoke-tested against the PSP sandbox.

## Infrastructure

- [ ] Terraform plans were reviewed for overly broad IAM roles, open security
      groups, or unintended resource changes.
- [ ] Kubernetes deployments specify resource limits and use approved internal
      registry images (for example,
      `registry.identitysec.internal/identity-api-gateway`).
- [ ] Do not run `terraform apply` locally against shared state — use the
      platform-devops pipeline only.
- [ ] Network policies and ingress rules restrict access to backend services.

## Telemetry and observability

- [ ] Structured JSON logging is enabled via `platform-packages/logger` for
      Python services.
- [ ] Sample staging logs and traces were checked for prohibited data (see
      `security_notice.md`).
- [ ] OpenTelemetry span attributes and metric labels follow the same redaction
      rules as application logs.
- [ ] Alerting and dashboards cover auth failures, billing errors, and pipeline
      job failures for the deployed components.

## Data platform

- [ ] Kafka topic and schema changes in `data-platform/schemas/` are backward
      compatible or have a documented migration plan.
- [ ] Flink jobs and dbt models were validated in a non-production environment.
- [ ] Sink connectors (for example, Snowflake) use least-privilege credentials.

## Final sign-off

- [ ] Deployment scope and rollback plan are documented in the release ticket.
- [ ] On-call engineer is notified for auth, billing, or infrastructure changes.
- [ ] Post-deploy smoke tests pass for customer portal, admin console, auth
      gateway, and billing endpoints as applicable.

## Related documents

- `CONTRIBUTING.md` — review and ownership requirements
- `security_notice.md` — logging and telemetry redaction rules
- `audit_guidelines.md` — code review and telemetry audit practices
