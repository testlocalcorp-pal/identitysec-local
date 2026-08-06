# Multi-Site Security Summary

Research summary combining live documentation from [OWASP](https://owasp.org),
[MDN Web Docs](https://developer.mozilla.org), and recent discussions on
[Hacker News](https://news.ycombinator.com) related to API authentication and
security.

**Report date:** August 2026

---

## Source 1 — OWASP API Security Top 10 (2023)

**URLs fetched:**
- https://owasp.org/API-Security/
- https://owasp.org/www-project-api-security/
- https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/

### Project overview

The OWASP API Security Project provides risk documentation and best practices
for builders, breakers, and defenders of API-based applications. APIs expose
application logic and sensitive data (PII), making them high-value attack
targets. The project maintains a living Top 10 risks document (stable 2023
release, June 2023) licensed under Creative Commons Attribution-ShareAlike 4.0.

### OWASP API Security Top 10 — 2023 edition

| ID | Risk | Summary |
|---|---|---|
| **API1:2023** | Broken Object Level Authorization (BOLA) | Endpoints accepting object IDs without verifying the caller owns that object. Attackers manipulate IDs in paths, query strings, headers, or payloads. |
| **API2:2023** | Broken Authentication | Flawed auth implementations allow token compromise or identity assumption. |
| **API3:2023** | Broken Object Property Level Authorization | Missing property-level auth leads to excessive data exposure or mass assignment. |
| **API4:2023** | Unrestricted Resource Consumption | No limits on CPU, bandwidth, or paid third-party API calls enable DoS or cost abuse. |
| **API5:2023** | Broken Function Level Authorization | Complex role hierarchies allow access to admin or other users' functions. |
| **API6:2023** | Unrestricted Access to Sensitive Business Flows | Automated abuse of business flows (ticket buying, commenting) without rate controls. |
| **API7:2023** | Server Side Request Forgery (SSRF) | APIs fetching remote resources without validating user-supplied URIs. |
| **API8:2023** | Security Misconfiguration | Missing or incorrect security settings in API infrastructure. |
| **API9:2023** | Improper Inventory Management | Undocumented, deprecated, or debug API endpoints left exposed. |
| **API10:2023** | Unsafe Consumption of APIs | Trusting third-party API responses without validation enables indirect compromise. |

### Deep dive: API1 — Broken Object Level Authorization

From the OWASP 2023 edition detail page:

- **Exploitability:** Easy — object IDs (integers, UUIDs, strings) are trivially
  identifiable in requests.
- **Prevalence:** Widespread — common in API apps because servers rely on
  client-supplied IDs rather than tracking full client state.
- **Impact:** Data disclosure, manipulation, destruction, or full account takeover.

**Prevention guidance:**

1. Implement authorization that checks user policies and hierarchy on every
   object-access function.
2. Validate permissions in every function using client-supplied IDs to access
   database records.
3. Prefer random, unpredictable GUIDs for record IDs.
4. Write automated authorization tests; block deployment if tests fail.

**Important distinction:** Comparing JWT user ID to a path parameter is
insufficient for BOLA — the violation occurs at the object level, not the
endpoint level (that would be Broken Function Level Authorization / BFLA).

---

## Source 2 — MDN HTTP security headers

**URLs fetched:**
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers#security
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Strict-Transport-Security
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Content-Type-Options
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Frame-Options

### Security headers catalog (MDN)

MDN groups the following as standard HTTP security response headers:

| Header | Purpose |
|---|---|
| **Content-Security-Policy (CSP)** | Controls which resources the browser may load; primary defense against XSS |
| **Content-Security-Policy-Report-Only** | Monitors CSP violations without enforcing (useful during testing) |
| **Strict-Transport-Security (HSTS)** | Forces HTTPS for future connections; blocks certificate bypass |
| **X-Content-Type-Options** | `nosniff` — prevents MIME type sniffing; blocks script/style execution on wrong MIME types |
| **X-Frame-Options** | `DENY` or `SAMEORIGIN` — prevents clickjacking via iframe embedding |
| **Cross-Origin-Opener-Policy (COOP)** | Isolates browsing context from cross-origin openers |
| **Cross-Origin-Resource-Policy (CORP)** | Restricts cross-origin loading of resources |
| **Cross-Origin-Embedder-Policy (COEP)** | Declares embedder policy for cross-origin isolation |
| **Referrer-Policy** | Controls Referer header leakage |
| **Permissions-Policy** | Allows/denies browser features (camera, geolocation, etc.) |
| **Upgrade-Insecure-Requests** | Signals client preference for HTTPS upgrade |
| **X-Powered-By** | Should be unset — exposes server fingerprinting information |
| **Reporting-Endpoints** | Defines endpoints for CSP and other violation reports |

### Key header details

#### Strict-Transport-Security (HSTS)

```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```

- Browsers remember the host must use HTTPS for `max-age` seconds.
- Must be sent over HTTPS only (ignored over HTTP to prevent MITM tampering).
- `includeSubDomains` extends policy to all subdomains.
- `preload` enables inclusion in browser HSTS preload lists (requires
  `max-age >= 31536000` and `includeSubDomains`).
- Set `max-age=0` to disable (only effective after a secure request).

#### Content-Security-Policy (CSP)

```
Content-Security-Policy: default-src https:; script-src 'self'; object-src 'none'
```

- Restricts script, style, image, font, and other resource origins.
- Supports nonces and hashes for inline script/style allowlisting.
- `'unsafe-inline'` and `'unsafe-eval'` defeat much of CSP's purpose — avoid.
- Use `Content-Security-Policy-Report-Only` during testing with `report-to`
  or `report-uri` directives.
- Multiple CSP headers combine restrictively (strictest policy wins per directive).

#### X-Content-Type-Options

```
X-Content-Type-Options: nosniff
```

- Prevents browsers from MIME-sniffing responses away from declared `Content-Type`.
- Blocks script/style execution when MIME type doesn't match expected type.
- Prevents user-uploaded plain text from being interpreted as HTML (XSS vector).

#### X-Frame-Options

```
X-Frame-Options: SAMEORIGIN
```

- `DENY` — no framing allowed.
- `SAMEORIGIN` — framing only from same origin.
- MDN recommends `frame-ancestors` in CSP as a more comprehensive alternative.
- Must be set via HTTP headers (not `<meta>` tags).

### MDN deployment note

MDN documents setting these headers at the reverse-proxy level (Nginx, Apache,
HAProxy, IIS) or via Express + Helmet middleware for Node.js applications.

---

## Source 3 — Hacker News: API authentication security discussions

**URL fetched:** https://hn.algolia.com/api/v1/search?query=API+authentication+security

HN search returned 113 stories. Key themes from recent and highly-voted
discussions:

### Recurring community concerns

| Theme | Example discussion | Key takeaway |
|---|---|---|
| **Auth method selection** | "Comparing 4 REST API Authentication Methods" (2025) | Developers actively compare OAuth, JWT, API keys, and session-based auth |
| **Production-grade auth setup** | "Ask HN: How to add production-grade security/authentication to my REST API?" | Common questions: API keys, tokens, rate limiting, third-party vs. roll-your-own |
| **Third-party auth provider flaws** | "Tell HN: Stytch Login SaaS Unicorn has common auth vulnerabilities" (58 pts, 48 comments) | Login CSRF, long-lived OTP tokens, missing security policies in auth SaaS APIs |
| **Declarative backend security** | "Ask HN: Would You Use a Declarative Back End (APIs, DB, Auth, Sync)?" (2025) | Interest in YAML-defined auth rules, API keys, OAuth, JWT in config-as-code |
| **Automated API security testing** | "Show HN: Quickly Create Security Tests for All Your APIs" (Metlo, YC S21) | Generic scanners miss business-logic vulns; OWASP Top 10 templates (BOLA, broken auth) needed |
| **Crypto library vulnerabilities** | "Bouncy Castle cryptography bug enables auth bypass" | Low-level crypto bugs can bypass API authentication entirely |
| **JWT vs OAuth vs Sessions** | "Do you use all three for an API?" | Confusion persists about when to use each mechanism |

### Notable HN insight: auth SaaS scrutiny

The Stytch discussion (high engagement) highlighted that even well-funded auth
providers can lack CSRF protection on login APIs, use overly long-lived magic
link tokens, and omit disclosure policies — reinforcing OWASP API2 (Broken
Authentication) as a real-world priority.

### Notable HN insight: testing gaps

The Metlo Show HN post noted that automated scanners typically catch
misconfigured HSTS/CORS headers but miss API-specific business logic
vulnerabilities like BOLA and broken authentication — aligning with OWASP's
focus on API-specific (not just web-app) risks.

---

## Cross-source synthesis

### Mapping OWASP API risks to HTTP headers and HN themes

| OWASP risk | MDN header mitigation | HN community signal |
|---|---|---|
| API2: Broken Authentication | HSTS, secure cookies, CSP | High discussion volume; auth SaaS failures reported |
| API4: Unrestricted Resource Consumption | (rate limiting at gateway) | Rate limiting frequently asked about for public APIs |
| API5: Broken Function Level Authorization | — | Declarative auth rules gaining interest |
| API8: Security Misconfiguration | CSP, HSTS, X-Frame-Options, X-Content-Type-Options | Scanners catch header misconfigs but miss logic bugs |
| API1: BOLA | — | Metlo/Owasp testing tools specifically target this |

### Recommended actions for API security programs

1. **Authorization** — Implement object-level and function-level checks per
   OWASP API1/API5; do not rely on JWT user ID comparison alone.
2. **Authentication** — Follow OWASP API2; validate token lifetimes, CSRF on
   login flows, and auth provider security policies (per HN Stytch discussion).
3. **HTTP headers** — Deploy MDN-documented security headers (CSP, HSTS,
   X-Content-Type-Options, X-Frame-Options) at ingress/gateway.
4. **Rate limiting** — Address OWASP API4/API6 with gateway-level throttling
   on auth and business-flow endpoints.
5. **Testing** — Combine header scanners with OWASP API Top 10 test templates
   for BOLA, broken auth, and business logic abuse (per HN Metlo discussion).
6. **Inventory** — Maintain API endpoint inventory per OWASP API9; deprecate
   debug and legacy versions.

---

## Relevance to IdentitySec Local Platform

This repository's auth gateway (`apps/identity-api-gateway`) and billing service
(`apps/billing-service`) are the primary API security surfaces. Existing local
docs (`security_notice.md`, `audit_guidelines.md`, `incident_response_plan.md`)
cover logging redaction and review processes. This multi-site summary adds
external OWASP, MDN, and community context for API authorization, HTTP header
hardening, and authentication testing priorities.

---

## References

### OWASP
- [OWASP API Security Project](https://owasp.org/www-project-api-security/)
- [OWASP API Security Top 10 2023](https://owasp.org/API-Security/)
- [API1:2023 Broken Object Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/)

### MDN
- [HTTP Headers — Security section](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers#security)
- [Strict-Transport-Security](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Strict-Transport-Security)
- [Content-Security-Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy)
- [X-Content-Type-Options](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Content-Type-Options)
- [X-Frame-Options](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Frame-Options)

### Hacker News
- [HN search: API authentication security](https://hn.algolia.com/api/v1/search?query=API+authentication+security)
- [Tell HN: Stytch auth vulnerabilities](https://news.ycombinator.com/item?id=33162854)
- [Show HN: Metlo API security tests](https://news.ycombinator.com/item?id=34584391)

### Internal
- `security_notice.md` — logging and telemetry redaction
- `audit_guidelines.md` — code review and telemetry audit
- `incident_response_plan.md` — incident triage and reporting
