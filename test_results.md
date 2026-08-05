# Automated Test Verification Protocol

Steps for verifying automated test coverage and results before merging or
releasing changes from this repository. Use this checklist after local changes
and when reviewing CI output on pull requests.

## Pre-verification

- [ ] Latest `main` is fetched and the working branch is rebased or merged
      with no unresolved conflicts.
- [ ] Changed paths are identified so only the relevant CI workflows and test
      suites are executed (see `.github/workflows/`).
- [ ] Required `CODEOWNERS` approvals are in place for every touched area per
      `CONTRIBUTING.md`.

## CI workflow verification

Path-filtered workflows run on pull requests. Confirm the expected workflow
triggered and completed successfully:

| Changed area | Workflow | Location |
|---|---|---|
| `apps/customer-portal`, `apps/admin-console`, `platform-packages/ui-kit` | CI - Web Apps | `.github/workflows/ci-web-apps.yml` |
| `apps/identity-api-gateway`, `apps/billing-service`, `platform-packages/**` | CI - Auth & Billing Services | `.github/workflows/ci-auth-services.yml` |
| `data-platform/**` | CI - Data Pipelines | `.github/workflows/ci-data-pipelines.yml` |

- [ ] All applicable CI workflows show a green status on the PR.
- [ ] Build and test steps completed without skipped required jobs.
- [ ] No new lint, type-check, or unit-test failures were introduced in
      affected packages.

## Local and repository test suites

### End-to-end automation (`tests/automation/`)

- [ ] Run E2E specs for changed UI flows (for example,
      `tests/automation/customer_portal.spec.ts`).
- [ ] Confirm critical user journeys pass: login, navigation, and any
      billing or account flows touched by the change.

### Contract tests (`tests/contract/`)

- [ ] Verify consumer/provider contracts for affected services (for example,
      `tests/contract/billing_service.pact.json`).
- [ ] Confirm API request/response shapes match published schemas in
      `data-platform/schemas/` when endpoints or events changed.

### Load and performance (`tests/load-performance/`)

- [ ] Run load scripts when auth or ingress paths changed (for example,
      `tests/load-performance/login_load.js`).
- [ ] Review latency, error rate, and throughput against agreed thresholds
      in staging before production promotion.

## Service-specific verification

### Web apps (`apps/customer-portal`, `apps/admin-console`)

- [ ] Application builds successfully with the monorepo tooling.
- [ ] Shared UI components from `platform-packages/ui-kit` render and behave
      as expected in affected screens.

### Auth and billing (`apps/identity-api-gateway`, `apps/billing-service`)

- [ ] Service-level tests pass for token issuance/verification and
      subscription handlers.
- [ ] Security-sensitive paths were reviewed by `@identitysec/security` per
      `CONTRIBUTING.md`.
- [ ] No secrets, tokens, or PCI data appear in test fixtures or logs (see
      `security_notice.md`).

### Data platform (`data-platform/`)

- [ ] dbt models compile and tests pass for modified analytics assets.
- [ ] Flink job unit tests pass for changed streaming logic.
- [ ] Schema changes remain backward compatible or include a documented
      migration plan.

## Test result recording

- [ ] Document the test command(s) run, environment (local, staging), and
      pass/fail outcome in the PR description or linked ticket.
- [ ] Attach CI run URLs and any relevant screenshots or log excerpts for
      failed-then-fixed iterations.
- [ ] Note skipped or deferred test suites with justification and a follow-up
      task if full coverage was not executed.

## Final sign-off

- [ ] All required automated checks are green on the PR.
- [ ] Manual smoke tests completed for any area not fully covered by
      automation.
- [ ] Test verification is complete and the change is ready for merge or
      deployment per `deployment_checklist.md`.

## Related documents

- `CONTRIBUTING.md` — review and ownership requirements
- `audit_guidelines.md` — code review and test coverage expectations
- `deployment_checklist.md` — pre-deployment verification steps
- `.github/workflows/` — CI scope per changed area
- `.github/CODEOWNERS` — path ownership
