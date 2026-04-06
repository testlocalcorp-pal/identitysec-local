# IdentitySec Local Platform

Monorepo for the IdentitySec identity & access management product: customer
and admin apps, the identity/billing services, the data platform, and ML
systems for fraud/risk scoring, sharing infra and internal libraries.

## Structure

| Path | Owning team | Purpose |
|---|---|---|
| `apps/customer-portal`, `apps/admin-console` | Frontend | Customer + internal admin UIs |
| `apps/identity-api-gateway`, `apps/billing-service` | Backend | AuthN/AuthZ ingress, subscription billing |
| `.infrastructure/` | Platform/DevOps | Terraform, k8s, base images |
| `data-platform/` | Data Streaming & Analytics | Kafka/Flink, dbt, Airflow |
| `data-science/` | Data Science | Risk/fraud scoring models |
| `platform-packages/` | Platform Engineers | Shared internal libraries |
| `tests/` | QA / Automation | E2E, load, and contract tests |

Team boundaries enforced by `.github/CODEOWNERS`. CI only builds what
changed — see `.github/workflows/`.
