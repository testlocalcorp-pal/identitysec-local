# Contributing

Multi-team monorepo — stay inside your team's directory unless a change is
explicitly cross-cutting (shared schema in `data-platform/schemas/`, or a
`platform-packages/` library bump).

- Cross-team changes require review from both `CODEOWNERS` groups.
- `apps/billing-service` requires a security review on every PR (handles
  subscription/payment data).
- `apps/identity-api-gateway` requires a security review on every PR
  (issues and verifies auth tokens for the whole platform).
- `.infrastructure/` changes require platform-team approval regardless of
  who authored them.
- Local setup per app is documented in that app's own README.
