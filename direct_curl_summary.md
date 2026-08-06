# Direct curl Security Summary

Summary extracted by fetching live homepages with `curl.exe` and parsing
returned HTML. Commands were run locally on August 6, 2026.

## Fetch commands

```powershell
C:\Windows\System32\curl.exe -sL https://owasp.org -o owasp-home.html
C:\Windows\System32\curl.exe -sL https://developer.mozilla.org -o mdn-home.html
```

| Site | Response size | Status |
|---|---|---|
| https://owasp.org | 58,654 bytes | Success |
| https://developer.mozilla.org | 119,471 bytes | Success |

> **Note:** `curl.exe` was invoked via full path (`C:\Windows\System32\curl.exe`)
> because it was not on the shell PATH in this environment.

---

## OWASP.org — parsed security guidelines

**Page title:** OWASP Foundation, the Open Source Foundation for Application Security

**Mission (from meta description and hero):**
- Nonprofit foundation that works to improve the security of software.
- Volunteer-driven resources accessible to everyone.
- Goal: make software security **visible** so individuals and organizations
  can make informed decisions about true software security risks.

### Security headers on OWASP's own homepage

The fetched HTML includes these response meta directives in `<head>`:

```
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
```

### Flagship security resources (highlighted on homepage)

| Resource | Type | Description | URL |
|---|---|---|---|
| **Top Ten** | Documentation | Reference standard for the most critical web application security risks | `/www-project-top-ten/` |
| **ASVS** | Documentation | Application Security Verification Standard | `/www-project-application-security-verification-standard/` |
| **Cheat Sheets** | Documentation | Crucial app security information for developers and defenders | `/www-project-cheat-sheets/` |

### Additional flagship projects (from embedded JSON on homepage)

| Project | Purpose |
|---|---|
| **Dependency-Check** | SCA tool — identifies known vulnerabilities in project dependencies |
| **Dependency-Track** | Component analysis platform for software supply chain risk |
| **CycloneDX** | Bill of Materials (BOM) standard for supply chain cyber risk reduction |
| **DefectDojo** | Open source vulnerability management for DevSecOps |
| **ZAP** | Web application security scanning tool |
| **Juice Shop** | Intentionally insecure web app for security training and CTFs |
| **WSTG** | Web Security Testing Guide for developers and security professionals |
| **ModSecurity CRS** | WAF rule set protecting against OWASP Top Ten attacks |
| **SAMM** | Software Assurance Maturity Model for improving security posture |
| **Mobile App Security (MAS)** | Mobile application security verification and testing standard |
| **Amass** | Network attack surface mapping and external asset discovery |

### Recent security content (homepage blog)

- **CVE Lite CLI** graduated to OWASP Lab Project — fast open source dependency
  vulnerability scanner for JavaScript and TypeScript projects.

### Community and events

Homepage promotes AppSec conferences (Germany, Portugal, India, LASCON,
Israel, France) focused on application security for developers, architects,
and security engineers.

### Key takeaway

OWASP emphasizes **documentation standards** (Top 10, ASVS, Cheat Sheets),
**dependency/supply chain scanning** (Dependency-Check, CycloneDX),
**testing tools** (ZAP, WSTG, Juice Shop), and **maturity models** (SAMM) as
foundational security guidance.

---

## MDN (developer.mozilla.org) — parsed security guidelines

**Page title:** MDN Web Docs

**Mission (from meta description and hero):**
- Documents open web technologies: HTML, CSS, JavaScript, and Web APIs.
- "Resources for Developers, by Developers" — documenting web standards since 2005.

### Security-related navigation (from homepage HTML)

MDN homepage navigation links directly to these security-relevant doc sections:

| Section | Path | Relevance |
|---|---|---|
| **Web Security** | `/en-US/docs/Web/Security` | Core web security guidance |
| **Web Privacy** | `/en-US/docs/Web/Privacy` | Privacy on the web |
| **HTTP** | `/en-US/docs/Web/HTTP` | HTTP protocol including security headers |
| **HTTP Observatory** | `/en-US/observatory` | Tool to test website security configuration |
| **Accessibility** | `/en-US/docs/Web/Accessibility` | Inclusive and safe web development |

### Featured security article (homepage)

**Trusted Types API** (`/en-US/docs/Web/API/Trusted_Types_API`):

> The Trusted Types API gives web developers a way to ensure that input has
> been passed through a user-specified transformation function before being
> passed to an API that might execute that input. This can help to protect
> against client-side cross-site scripting (XSS) attacks.

This is a key MDN security guideline surfaced on the homepage: sanitize or
transform untrusted input before it reaches DOM XSS injection sinks.

### HTTP security tooling

MDN promotes **HTTP Observatory** (`/en-US/observatory`) in its Tools menu —
a site security testing tool (shield-check icon) for evaluating HTTP security
header configuration, complementing the HTTP headers documentation.

### HTTP documentation scope

The HTTP section (`/en-US/docs/Web/HTTP`) covers protocol-level security
including response headers such as:

- **Content-Security-Policy (CSP)** — control resource loading, mitigate XSS
- **Strict-Transport-Security (HSTS)** — enforce HTTPS connections
- **X-Content-Type-Options** — prevent MIME sniffing (`nosniff`)
- **X-Frame-Options** — prevent clickjacking via iframe embedding
- **Cross-Origin-Opener-Policy (COOP)** — isolate browsing contexts
- **Cross-Origin-Resource-Policy (CORP)** — restrict cross-origin resource loading
- **Referrer-Policy** — control Referer header leakage
- **Permissions-Policy** — allow/deny browser feature access

*(These headers are catalogued under MDN's HTTP Headers → Security section.)*

### Key takeaway

MDN provides **developer-facing security guidance** through dedicated Security
and Privacy doc sections, HTTP header reference documentation, the Trusted Types
API for XSS prevention, and the HTTP Observatory tool for configuration testing.

---

## Cross-site comparison

| Aspect | OWASP.org | MDN |
|---|---|---|
| **Primary audience** | Security professionals, pentesters, AppSec teams | Web developers, frontend/backend engineers |
| **Focus** | Application security risks, testing, standards, supply chain | Web platform security headers, APIs, browser features |
| **Top resources** | Top 10, ASVS, Cheat Sheets, ZAP, Dependency-Check | HTTP Security docs, Trusted Types, HTTP Observatory |
| **Dependency security** | Dependency-Check, CycloneDX, CVE Lite CLI | (not primary focus on homepage) |
| **Header guidance** | ModSecurity CRS, Cheat Sheets | Full HTTP header reference + Observatory scanner |
| **Own site practices** | Uses `X-Content-Type-Options: nosniff` | Promotes security testing via Observatory |

---

## Relevance to IdentitySec Local Platform

- **OWASP Top 10 / ASVS** — applicable to auth gateway and billing service security reviews.
- **Dependency-Check / npm audit** — applicable to Next.js frontend apps.
- **MDN HTTP headers** — configure at ingress/K8s for customer portal and admin console.
- **Trusted Types / CSP** — relevant for frontend XSS hardening.
- **HTTP Observatory** — can test staging deployments for header misconfiguration.

---

## Sources

- Fetched via curl: https://owasp.org (58,654 bytes HTML)
- Fetched via curl: https://developer.mozilla.org (119,471 bytes HTML)
- OWASP Top Ten: https://owasp.org/www-project-top-ten/
- MDN Web Security: https://developer.mozilla.org/en-US/docs/Web/Security
- MDN HTTP Headers: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers#security
- MDN HTTP Observatory: https://developer.mozilla.org/en-US/observatory
