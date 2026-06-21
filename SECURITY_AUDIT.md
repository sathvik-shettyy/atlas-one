# Atlas One — Security Audit & Accepted Risk Register

> **Generated:** 2026-06-21  
> **Version:** v0.1.0-alpha

---

## Accepted Framework Risk

| Attribute | Value |
|---|---|
| **Component** | Starlette (transitive dependency through FastAPI) |
| **Status** | Accepted Risk |
| **Decision Date** | 2026-06-21 |
| **Risk Owner** | Atlas One Security |
| **Review Frequency** | Every release cycle |

### Reason

Patched Starlette versions suggested by pip-audit are currently not compatible with the FastAPI ecosystem used by Atlas One. Upgrading these transitive dependencies would require upgrading FastAPI itself to a version that introduces breaking changes to the existing authentication flow and API surface.

### Mitigation

- Keep FastAPI pinned to a compatible stable version
- Maintain Bandit SAST scanning for application-level vulnerabilities
- Maintain pip-audit scanning for all dependencies (ignored CVEs documented below)
- Review ignored CVEs every release cycle for upstream compatibility changes
- Upgrade when FastAPI ecosystem supports patched transitive versions

### Ignored CVEs

| ID | Component | Severity | Notes |
|---|---|---|---|
| PYSEC-2026-161 | Starlette | High | Transitive via FastAPI. Patching requires FastAPI major upgrade |
| CVE-2025-54121 | Starlette | High | Transitive via FastAPI. No compatible patched version in current ecosystem |
| CVE-2025-62727 | Starlette | Medium | Transitive via FastAPI. No compatible patched version in current ecosystem |
| CVE-2026-48818 | Starlette | High | Transitive via FastAPI. No compatible patched version in current ecosystem |
| CVE-2026-48817 | Starlette | High | Transitive via FastAPI. No compatible patched version in current ecosystem |
| CVE-2026-54283 | Starlette | Medium | Transitive via FastAPI. No compatible patched version in current ecosystem |
| CVE-2026-54282 | Starlette | Medium | Transitive via FastAPI. No compatible patched version in current ecosystem |

---

## CI/CD Security Status

| Check | Status |
|---|---|
| Bandit (SAST) | ✅ PASS — Application-level static analysis |
| pip-audit (Dependency Scan) | ✅ PASS — 7 framework CVEs accepted as documented risk |
| Trivy (Container Scan) | ⚠️ Scans base images for OS-level CVEs |
| TruffleHog (Secret Scan) | ❌ Blocked by `.env` in repository |

---

## Dependency Security Posture

### Direct Dependencies (All Clean)

| Package | Version | Status |
|---|---|---|
| fastapi | 0.115.12 | ✅ Clean (direct) |
| uvicorn | 0.30.6 | ✅ Clean |
| SQLAlchemy | 2.0.35 | ✅ Clean |
| psycopg2-binary | 2.9.9 | ✅ Clean |
| python-jose | 3.4.0 | ✅ Clean |
| passlib | 1.7.4 | ✅ Clean |
| bcrypt | 4.1.3 | ✅ Clean |
| pydantic-settings | 2.4.0 | ✅ Clean |
| python-multipart | 0.0.20 | ✅ Clean |
| pytest | 8.3.5 | ✅ Clean |
| httpx | 0.27.2 | ✅ Clean |
| ruff | 0.6.2 | ✅ Clean |
| bandit | 1.7.9 | ✅ Clean |

### Transitive Dependencies (Accepted Risk)

| Component | Patched Version | Status |
|---|---|---|
| starlette (via fastapi) | Not compatible | ⚠️ Accepted Risk |

---

## Review Checklist

- [ ] Every release: Review ignored CVEs for upstream patches
- [ ] Every release: Verify Bandit scan passes
- [ ] Every release: Verify pip-audit scan passes (no new CVEs beyond accepted list)
- [ ] Every release: Review Trivy container scan results
- [ ] When possible: Upgrade FastAPI ecosystem to resolve transitive CVEs