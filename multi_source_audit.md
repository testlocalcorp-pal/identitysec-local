# Multi-Source Audit Report

Comprehensive audit combining three information sources: VS Code marketplace
research (Prettier extension), a codebase-wide structural analysis of this
repository, and live documentation from [expressjs.com](https://expressjs.com)
and the [npm registry](https://registry.npmjs.org).

**Report date:** August 2026  
**Repository:** IdentitySec Local Platform (`identitysec-local`)

---

## Source 1 — VS Code marketplace: Prettier extension

### Official extension

| Field | Value |
|---|---|
| **Name** | Prettier - Code formatter |
| **Extension ID** | `esbenp.prettier-vscode` |
| **Publisher** | Prettier (official) |
| **Marketplace URL** | https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode |
| **GitHub repo** | https://github.com/prettier/prettier-vscode |
| **License** | MIT |
| **Latest release** | v12.4.0 (March 2026) |
| **Bundled Prettier** | 3.x (uses project-local version when available) |

### Deprecated alternative

The extension ID `Prettier.prettier-vscode` is **deprecated**. Teams should
install `esbenp.prettier-vscode` only.

### Supported languages

JavaScript, TypeScript, Flow, JSX, JSON, CSS, SCSS, Less, HTML, Vue, Angular,
Handlebars, Ember, Glimmer, GraphQL, Markdown, YAML, and more.

### Recommended VS Code configuration

```json
{
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.formatOnSave": true,
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  }
}
```

Install via Quick Open (`Ctrl+P`):

```
ext install esbenp.prettier-vscode
```

### Configuration priority

When a project config file exists, it takes precedence over VS Code settings:

1. `.prettierrc` / `.prettierrc.json` / `prettier.config.js`
2. `.editorconfig` (if `prettier.useEditorConfig` is enabled)
3. `"prettier"` key in `package.json`
4. VS Code workspace/user settings (only when no local config exists)

### Resolution behavior

- Prefers **project-local** Prettier from `node_modules` (recommended).
- Falls back to bundled Prettier 3.x if no local installation is found.
- Optional `prettier.resolveGlobalModules: true` enables global resolution.

### Relevance to this repository

Frontend apps (`apps/customer-portal`, `apps/admin-console`) use TypeScript/React
(Next.js). Adopting `esbenp.prettier-vscode` with a shared `.prettierrc` at the
monorepo root would enforce consistent formatting across web apps and the
`platform-packages/ui-kit` package.

---

## Source 2 — Workspace architectural structure

Codebase-wide analysis of all repository files (45 tracked source/doc files
across apps, infrastructure, data platform, ML, shared packages, tests, and
security documentation).

### High-level architecture

```
IdentitySec Local Platform (monorepo)
├── apps/                    # Application services
│   ├── customer-portal/     # Next.js customer UI
│   ├── admin-console/       # Internal ops console (SSO required)
│   ├── identity-api-gateway/# Go auth ingress (:8080)
│   └── billing-service/     # Python PCI-scoped billing
├── platform-packages/       # Shared internal libraries
│   ├── logger/              # Structured JSON logging (Python)
│   ├── telemetry/           # OpenTelemetry tracer (Python)
│   └── ui-kit/              # Shared React components
├── data-platform/           # Streaming + analytics
│   ├── schemas/             # Protobuf event/model definitions
│   ├── streaming/           # Flink jobs, Kafka connectors
│   └── analytics/           # dbt models, Airflow DAGs
├── data-science/            # Fraud/risk ML pipeline
│   ├── feature-store/       # Feast feature views
│   ├── models/              # XGBoost model architecture
│   ├── training/            # Training entrypoint
│   └── notebooks/           # EDA notebooks
├── .infrastructure/         # Platform/DevOps
│   ├── terraform/           # AWS EKS, MSK, Snowflake modules
│   ├── k8s/                 # Gateway deployment manifests
│   └── docker/              # Base Docker images
├── tests/                   # QA automation
│   ├── automation/          # Playwright E2E specs
│   ├── contract/            # Pact contract tests
│   └── load-performance/    # k6 load tests
└── [security docs]          # Process and compliance documentation
```

### Technology stack

| Layer | Technology | Key files |
|---|---|---|
| Frontend | Next.js 14, React 18 | `apps/customer-portal/`, `apps/admin-console/` |
| Auth gateway | Go | `apps/identity-api-gateway/src/main.go` |
| Billing | Python | `apps/billing-service/src/subscription_handler.py` |
| Logging | Python JSON logger | `platform-packages/logger/__init__.py` |
| Tracing | OpenTelemetry | `platform-packages/telemetry/tracer.py` |
| Data streaming | Flink, Kafka | `data-platform/streaming/` |
| Analytics | dbt, Airflow | `data-platform/analytics/` |
| ML | XGBoost, Feast | `data-science/` |
| Infrastructure | Terraform, K8s | `.infrastructure/` |

### Data flow (auth → fraud pipeline)

1. Login events defined in `data-platform/schemas/events/login_attempted.proto`
2. Flink job (`login_event_aggregator.py`) aggregates 1-minute windows
3. Kafka connector sinks to Snowflake for analytics
4. dbt model `fct_daily_active_accounts.sql` computes daily active accounts
5. ML feature store (`risk_features.py`) exposes fraud scoring features
6. XGBoost model (`fraud_risk_model.py`) scores login risk

### Governance and CI

- **CODEOWNERS** enforces team boundaries; auth/billing require
  `@identitysec/security`.
- Path-filtered CI workflows run only for changed areas:
  - `ci-web-apps.yml` — frontend + ui-kit
  - `ci-auth-services.yml` — gateway + billing + platform packages
  - `ci-data-pipelines.yml` — data-platform

### Existing security documentation

| Document | Purpose |
|---|---|
| `CONTRIBUTING.md` | Team boundaries, mandatory security reviews |
| `security_notice.md` | Logging redaction (no tokens, PAN, secrets) |
| `audit_guidelines.md` | Code review and telemetry audit checklists |
| `deployment_checklist.md` | Pre-deployment security verification |
| `incident_response_plan.md` | Incident triage and reporting |
| `security_audit_report.md` | Prior Express security cross-reference |
| `test_results.md` | Test verification before merge/release |

### Notable security characteristics

- **No Express.js** in this codebase — backend is Go + Python
- **PCI scope** isolated to `apps/billing-service`
- **Structured logging** enforced via shared Python logger
- **No secrets in logs** — documented and enforced in billing handler
- Frontend apps use npm/Next.js — subject to npm dependency auditing

---

## Source 3 — Live web documentation: Express.js security

Fetched from: https://expressjs.com/en/advanced/best-practice-security/

### Production security checklist (Express official)

| Category | Recommendation |
|---|---|
| **Versions** | Do not use Express 2.x/3.x; stay on current stable; check Security Updates page |
| **TLS** | Encrypt all sensitive traffic; terminate at Nginx or similar reverse proxy |
| **Input** | Never trust user input; validate and sanitize all accepted data |
| **Redirects** | Prevent open redirects — validate host before `res.redirect()` |
| **Headers** | Use Helmet middleware (CSP, HSTS, X-Content-Type-Options, etc.) |
| **Fingerprinting** | Disable `X-Powered-By`; use custom 404/error handlers |
| **Cookies** | Custom session names; set `secure`, `httpOnly`, `domain`, `path`, `expires` |
| **Sessions** | Use production session store (not in-memory) with `express-session` |
| **Brute force** | Rate-limit login endpoints (e.g. `rate-limiter-flexible`) |
| **Dependencies** | Run `npm audit`; consider Snyk for continuous monitoring |
| **Additional** | XSS/command injection filtering, parameterized SQL, safe-regex, SSL audit tools |

### Express npm registry metadata

Fetched from: https://registry.npmjs.org/express/latest

| Field | Value |
|---|---|
| **Latest version** | 5.2.1 |
| **Node requirement** | >= 18 |
| **License** | MIT |
| **Key dependencies** | `router`, `body-parser`, `send`, `serve-static`, `cookie`, `qs` |
| **Security contact** | https://github.com/expressjs/express/security/policy |
| **Funding** | Open Collective (https://opencollective.com/express) |

---

## Source 4 — npm registry security practices

Fetched from: https://docs.npmjs.com/auditing-package-dependencies-for-security-vulnerabilities

### npm audit workflow

1. Ensure `package.json` and `package-lock.json` exist in the target package
2. Run `npm audit` to submit dependency tree to the registry advisory database
3. Review severity, affected paths, and recommended fixes
4. Apply patches via `npm audit fix` or manual dependency updates
5. Re-run audit after changes to confirm resolution

### Key npm security behaviors

| Behavior | Detail |
|---|---|
| **Automatic audit** | `npm audit` runs automatically on `npm install` (since npm@6) |
| **Scope** | Checks direct, dev, bundled, and optional dependencies (not peerDependencies) |
| **Fix automation** | `npm audit fix` installs compatible updates; semver-breaking fixes warn with `SEMVER WARNING` |
| **Manual review** | When no patch exists, investigate mitigating factors or open maintainer issues |
| **CI integration** | npm recommends adding `npm audit` to continuous integration pipelines |
| **Disable audit** | `npm install --no-audit` or `npm set audit false` (not recommended for production) |

### Applicability to this repository

Frontend apps (`apps/customer-portal/package.json`, `apps/admin-console/package.json`)
use Next.js 14 and React 18 with workspace dependencies. These packages should:

- Maintain `package-lock.json` files for reproducible audits
- Run `npm audit` in CI as part of `ci-web-apps.yml`
- Monitor advisories for `next`, `react`, and `@identitysec/ui-kit` transitive deps

---

## Cross-source synthesis

### Alignment matrix

| Concern | Express/npm guidance | Local repo status |
|---|---|---|
| Dependency auditing | `npm audit`, Snyk | Applicable to frontend apps; not yet documented in CI |
| TLS | Required for sensitive data | Managed via `.infrastructure/terraform` + K8s ingress |
| Input validation | Never trust user input | Auth gateway (Go) + frontend forms |
| Secure logging | No secrets in production logs | Enforced via `security_notice.md` + shared logger |
| Rate limiting | Protect login endpoints | Fraud pipeline + k6 load tests exist |
| Code formatting | Prettier for JS/TS consistency | Not yet configured; `esbenp.prettier-vscode` recommended |
| Session security | Secure cookies, custom names | Handled by `identity-api-gateway` |
| Security reviews | Dependency + code review | CODEOWNERS + `@identitysec/security` on auth/billing |

### Recommended actions

1. **Add Prettier** — Install `esbenp.prettier-vscode` and add a root `.prettierrc`
   for consistent frontend formatting.
2. **Integrate npm audit in CI** — Add `npm audit --audit-level=high` to
   `ci-web-apps.yml` for `customer-portal` and `admin-console`.
3. **Map Express controls to gateway** — Apply TLS, rate limiting, and header
   hardening at the Go auth gateway and ingress layer.
4. **Link audit docs** — Reference this report alongside `deployment_checklist.md`
   and `audit_guidelines.md` during pre-release reviews.

---

## Related documents

### External sources

- [Prettier VS Code Extension](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode)
- [Express.js Security Best Practices](https://expressjs.com/en/advanced/best-practice-security/)
- [Express npm package (latest)](https://registry.npmjs.org/express/latest)
- [npm Audit Documentation](https://docs.npmjs.com/auditing-package-dependencies-for-security-vulnerabilities)

### Internal documents

- `security_audit_report.md` — prior Express security cross-reference
- `security_notice.md` — logging and telemetry redaction rules
- `audit_guidelines.md` — code review and telemetry audit practices
- `deployment_checklist.md` — pre-deployment security verification
- `incident_response_plan.md` — incident triage and reporting
