# ATLAS ONE — Project Memory & Complete Analysis

> **Generated:** 2026-06-21  
> **Role:** Senior Software Architect / Cybersecurity Engineer / Project Auditor  
> **Status:** Comprehensive audit complete — no code modifications made.

---

## Table of Contents

1. [Phase 1: Repository Discovery](#phase-1-repository-discovery)
2. [Phase 2: Architecture Analysis](#phase-2-architecture-analysis)
3. [Phase 3: Current Project State](#phase-3-current-project-state)
4. [Phase 4: Security Audit](#phase-4-security-audit)
5. [Phase 5: Future Roadmap](#phase-5-future-roadmap)

---

## Phase 1: Repository Discovery

### Project Identity

| Attribute | Value |
|---|---|
| **Name** | Atlas One |
| **Description** | Zero Trust Secure Access Platform — protects web applications through centralized identity, MFA, policy enforcement, and gateway-based access control without modifying protected application code. |
| **Repository** | `https://github.com/sathvik-shettyy/atlas-one.git` |
| **License** | (See LICENSE file) |
| **Latest Commit** | `a233e7029cb2546b5699a74bc77ac06cf6451034` |

### Tech Stack

| Layer | Technology | Version |
|---|---|---|
| **Frontend** | React + TypeScript + Vite | React 18.3.1, TS 5.5.4, Vite 5.4.2 |
| **Backend** | Python + FastAPI + SQLAlchemy | Python 3.12, FastAPI 0.112.2, SQLAlchemy 2.0.35 |
| **Database** | PostgreSQL | 16 Alpine |
| **Identity** | Keycloak (OIDC/OAuth2) | 25.0.4 |
| **Gateway** | NGINX | 1.27 Alpine |
| **Protected App** | Dashy (internal) | latest (lissy93/dashy) |
| **Containerization** | Docker Compose | — |
| **CI/CD** | GitHub Actions | — |

### Folder Structure

```
atlas-one/
├── .env                          # LIVE secrets (COMMITTED - SECURITY ISSUE)
├── .env.example                  # Template for environment variables
├── .gitignore
├── docker-compose.yml            # 6-service stack definition
├── README.md
├── SECURITY.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── LICENSE
│
├── gateway/
│   ├── nginx.conf                # NGINX reverse proxy with auth_request
│   └── conf.d/                   # (empty - future additional configs)
│
├── dashboard/                    # React SPA frontend
│   ├── Dockerfile
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── eslint.config.js
│   ├── index.html
│   ├── dist/                     # Pre-built production output
│   └── src/
│       ├── main.tsx              # Entry point
│       ├── App.tsx               # Router config
│       ├── styles.css            # Global styles
│       ├── vite-env.d.ts
│       ├── components/
│       │   └── StatusCard.tsx    # Reusable status indicator
│       └── pages/
│           ├── LoginPage.tsx     # Login form (username + password + OTP)
│           ├── DashboardPage.tsx # Main dashboard after login
│           └── WorkspacePage.tsx # Redirects to /workspace/ (via gateway)
│
├── policy-engine/                # FastAPI backend
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py               # API routes (login, logout, refresh, session, policy, password reset, SSO stubs)
│   │   ├── config.py             # Pydantic Settings (reads .env)
│   │   ├── database.py           # SQLAlchemy engine + session
│   │   ├── models.py             # User, PasswordResetToken ORM models
│   │   ├── schemas.py            # Pydantic request/response models
│   │   ├── security.py           # bcrypt hashing, MFA verification
│   │   ├── seed.py               # Seed users (admin/developer/guest)
│   │   ├── jwt/
│   │   │   └── tokens.py         # JWT create/decode (HS256)
│   │   └── rbac/
│   │       └── engine.py         # Role-based policy decisions
│   └── tests/
│       ├── conftest.py
│       └── test_health.py        # Single health endpoint test
│
├── keycloak/
│   └── realm/
│       └── atlas-one-realm.json  # Keycloak realm import (OIDC client, roles)
│
├── database/
│   └── postgres/
│       └── init/
│           └── 001-init.sql      # Enables uuid-ossp extension
│
├── apps/
│   └── dashy/
│       └── conf/
│           └── conf.yml          # Dashy workspace configuration
│
├── auth/                         # (empty - .gitkeep only)
├── realm/                        # (empty - .gitkeep only)
├── routing/                      # (empty - .gitkeep only)
├── themes/                       # (empty - .gitkeep only)
│
├── docs/
│   ├── architecture/
│   │   └── atlas-one.mmd         # Mermaid architecture diagram
│   └── screenshots/              # (empty - .gitkeep only)
│
└── .github/
    ├── pull_request_template.md
    ├── ISSUE_TEMPLATE/
    │   ├── bug_report.yml
    │   ├── config.yml
    │   ├── feature_request.yml
    │   └── security_report.yml
    └── workflows/
        ├── ci.yml                # CI: backend lint/test, frontend lint/build, Docker build, security scan
        └── release.yml           # CD: GitHub Release on version tags
```

### API Endpoints

| Method | Path | Description | Auth Required |
|---|---|---|---|
| GET | `/health` | Health check | No |
| POST | `/auth/login` | Login (username + password + OTP) | No |
| POST | `/auth/logout` | Clear auth cookies | No |
| POST | `/auth/refresh` | Refresh access token | Refresh cookie |
| GET | `/auth/session` | Get current session status | No (returns unauthenticated if no token) |
| POST | `/policy/evaluate` | Evaluate policy for resource | Access token |
| GET | `/gateway/authorize` | NGINX auth_request subrequest target | Access token |
| POST | `/auth/password-reset/request` | Request password reset | No |
| POST | `/auth/password-reset/confirm` | Confirm password reset | Reset token |
| GET | `/auth/sso/start` | SSO bootstrap (STUB) | No |
| GET | `/auth/sso/callback` | SSO callback (STUB) | No |

### Database Schema

**Table: `users`**
| Column | Type | Constraints |
|---|---|---|
| id | Integer | PK, Index |
| username | String(100) | UNIQUE, NOT NULL, Index |
| password_hash | String(255) | NOT NULL |
| role | String(32) | NOT NULL, default: "guest" |
| mfa_mode | String(16) | NOT NULL, default: "required" |
| is_active | Boolean | NOT NULL, default: true |
| created_at | DateTime(tz) | server_default: now() |

**Table: `password_reset_tokens`**
| Column | Type | Constraints |
|---|---|---|
| id | Integer | PK, Index |
| username | String(100) | NOT NULL, Index |
| token | String(255) | NOT NULL, UNIQUE |
| is_used | Boolean | NOT NULL, default: false |
| created_at | DateTime(tz) | server_default: now() |

### Seed Users

| Username | Password | Role | MFA Mode |
|---|---|---|---|
| admin | AtlasOneAdmin123! | admin | required |
| developer | AtlasOneDev123! | developer | optional |
| guest | AtlasOneGuest123! | guest | disabled |

---

## Phase 2: Architecture Analysis

### Overall Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        User (Browser)                           │
│                    http://localhost:8080                         │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│              NGINX Gateway (port 8080)                           │
│  ┌─────────────┬──────────────────┬──────────────────────┐      │
│  │ / → Dashboard│ /workspace →     │ /api/* → Policy     │      │
│  │   (React SPA)│ auth_request     │   Engine (FastAPI)  │      │
│  │              │ → /_atlas_auth   │                      │      │
│  └─────────────┴──────────────────┴──────────────────────┘      │
└──────────────────────────────────────────────────────────────────┘
                           │
          ┌────────────────┼────────────────────┐
          ▼                ▼                    ▼
┌─────────────────┐ ┌─────────────────┐ ┌──────────────────────┐
│   Dashboard     │ │  Policy Engine  │ │   Dashy Workspace    │
│   (React SPA)   │ │  (FastAPI)      │ │   (Internal App)     │
│   :3000         │ │  :8081          │ │   :4000              │
│                 │ │                 │ │                      │
│ Serves UI for   │ │ Auth, JWT, RBAC │ │ Protected app behind │
│ login, dashboard│ │ MFA, Password   │ │ gateway auth_request │
│ workspace page  │ │ Reset, SSO stub │ │                      │
└─────────────────┘ └────────┬────────┘ └──────────────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   PostgreSQL    │
                    │   :5432         │
                    │                 │
                    │ Users, Reset    │
                    │ Tokens          │
                    └─────────────────┘

                    ┌─────────────────┐
                    │   Keycloak      │
                    │   :8090         │
                    │                 │
                    │ OIDC Provider   │
                    │ (NOT integrated │
                    │  into auth flow)│
                    └─────────────────┘
```

### Frontend to Backend Communication

1. **React SPA** makes all API calls to `/api/*` which NGINX proxies to the Policy Engine at `policy-engine:8081`.
2. **Authentication state** is managed via HttpOnly cookies (`atlas_access_token`, `atlas_refresh_token`) — the JavaScript cannot read the JWT payload directly.
3. **Session check** is done via `GET /api/auth/session` which returns `{authenticated, username, role, mfa_mode}`.
4. **Workspace access** is a full page redirect (`window.location.assign("/workspace/")`) which triggers NGINX's `auth_request` subrequest to `/_atlas_auth` → `/gateway/authorize`.

### Authentication Flow

```
1. User navigates to http://localhost:8080
2. DashboardPage checks /api/auth/session
3. If not authenticated → redirect to /login
4. User submits username + password + OTP to POST /api/auth/login
5. Policy Engine:
   a. Queries User by username
   b. Verifies password with bcrypt
   c. Resolves MFA mode (user-level or default)
   d. Validates OTP against static code
   e. Creates JWT access token (30min) + refresh token (7 days)
   f. Sets both as HttpOnly cookies
6. Frontend navigates to / (DashboardPage)
7. DashboardPage checks session again → authenticated
8. User clicks "Open Workspace" → navigates to /workspace
9. WorkspacePage does window.location.assign("/workspace/")
10. NGINX intercepts /workspace:
    a. Sends auth_request to /_atlas_auth → /gateway/authorize
    b. Policy Engine decodes JWT from cookie, checks user active + MFA + role
    c. If 200 → proxy to Dashy
    d. If 401 → redirect to /login
    e. If 403 → return JSON error
```

### Authorization Model

- **RBAC** with 3 roles: `admin`, `developer`, `guest`
- All 3 roles have access to the `workspace` resource
- Policy decision checks (in order):
  1. Is user active? (DB field)
  2. Is MFA verified? (JWT claim)
  3. Is role allowed for resource? (RBAC policy map)
- **Key finding:** All roles have identical permissions — RBAC is technically implemented but functionally flat.

### Data Flow

```
Login:     User → Browser → NGINX → Policy Engine → PostgreSQL → JWT → Cookies → Browser
Session:   Browser → NGINX → Policy Engine → PostgreSQL → Session JSON → Browser
Workspace: Browser → NGINX → auth_request → Policy Engine → 200/401/403 → Dashy proxy
Password:  Browser → NGINX → Policy Engine → PostgreSQL → Reset Token → Response
```

### External Services & APIs

| Service | Purpose | Status |
|---|---|---|
| **Keycloak** | OIDC identity provider | Deployed but NOT integrated into auth flow |
| **Dashy** | Protected workspace application | Fully integrated behind gateway |
| **PostgreSQL** | Data persistence | Fully integrated |

### Docker Architecture

```
Network: atlas-net (bridge, internal)

Services:
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│  gateway     │────▶│  dashboard   │     │  postgres    │
│  :8080       │     │  :3000       │     │  :5432       │
│  nginx:1.27  │     │  node:20     │     │  postgres:16 │
│  (public)    │     │  (internal)  │     │  (internal)  │
└──────┬───────┘     └──────────────┘     └──────┬───────┘
       │                                         │
       │           ┌──────────────┐              │
       ├──────────▶│ policy-engine│◄─────────────┘
       │           │  :8081       │
       │           │  python:3.12 │
       │           └──────────────┘
       │
       │           ┌──────────────┐
       └──────────▶│  dashy       │
                   │  :4000       │
                   │  lissy93/    │
                   │  dashy:latest│
                   └──────────────┘

Volumes:
  atlas-postgres-data → /var/lib/postgresql/data

Health Checks:
  All services have health checks with retries
  Restart policy: unless-stopped
```

### CI/CD Workflow

**CI (Pull Request / Push to main):**
1. **Backend job:** Python 3.12 → pip install → Ruff lint → Pytest → py_compile
2. **Frontend job:** Node 20 → npm install → ESLint → TypeScript check → Vite build
3. **Docker job:** Validate compose config → Build images (gateway, dashboard, policy-engine)
4. **Security job:** Bandit (SAST) → Safety (dependency vulns) → Trivy (container scan) → TruffleHog (secret scan)

**CD (Tag push v*.*.*):**
- Generate changelog → Create GitHub Release

### Security Architecture

```
Defense Layers (outside-in):

1. Network Layer:
   - Single public port (8080) via NGINX
   - Internal services on isolated bridge network
   - No exposed internal ports

2. Gateway Layer (NGINX):
   - Security headers: X-Frame-Options, X-Content-Type-Options, Referrer-Policy
   - server_tokens off (hides NGINX version)
   - auth_request subrequest for protected routes
   - Internal location block (/_atlas_auth) not accessible externally

3. Authentication Layer (Policy Engine):
   - Password hashing with bcrypt
   - JWT access + refresh token pattern
   - HttpOnly cookies (not accessible via JS)
   - MFA verification (static OTP)
   - Session validation on every protected request

4. Authorization Layer (Policy Engine):
   - RBAC policy engine
   - User active status check
   - MFA verification status check
   - Role-based resource permission check

5. CI/CD Security:
   - Bandit SAST scanning
   - Safety dependency vulnerability scanning
   - Trivy container image scanning
   - TruffleHog secret scanning
```

---

## Phase 3: Current Project State

### Completed ✅

| Feature | Status |
|---|---|
| Docker Compose orchestration (6 services) | ✅ Complete |
| NGINX gateway with routing, auth_request, security headers | ✅ Complete |
| Policy Engine FastAPI application | ✅ Complete |
| JWT access/refresh token creation and validation | ✅ Complete |
| RBAC engine with admin/developer/guest roles | ✅ Complete |
| User database model with password hashing (bcrypt) | ✅ Complete |
| Seed users (admin, developer, guest) | ✅ Complete |
| Login endpoint (username + password + OTP) | ✅ Complete |
| Logout endpoint (cookie clearing) | ✅ Complete |
| Session status endpoint | ✅ Complete |
| Token refresh endpoint | ✅ Complete |
| Password reset flow (request + confirm) | ✅ Complete |
| Gateway authorization subrequest endpoint | ✅ Complete |
| Policy evaluation endpoint | ✅ Complete |
| React SPA with routing (login, dashboard, workspace) | ✅ Complete |
| Dashboard UI with status cards, session info, logout | ✅ Complete |
| Login form with credential fields | ✅ Complete |
| Workspace redirect page | ✅ Complete |
| CSS styling (cyber/tech theme) | ✅ Complete |
| CI/CD pipeline (GitHub Actions) | ✅ Complete |
| Keycloak realm configuration | ✅ Complete |
| Dashy workspace configuration | ✅ Complete |
| PostgreSQL init script (uuid-ossp) | ✅ Complete |
| Issue templates (bug, feature, security) | ✅ Complete |
| Pull request template | ✅ Complete |
| Community files (README, LICENSE, SECURITY, CONTRIBUTING, CODE_OF_CONDUCT) | ✅ Complete |
| Architecture diagram (Mermaid) | ✅ Complete |

### In Progress / Partially Implemented ⚠️

| Feature | Status | Details |
|---|---|---|
| **Keycloak OIDC Integration** | ⚠️ Stub only | Keycloak is deployed and configured, but `/auth/sso/start` and `/auth/sso/callback` return placeholder messages. The actual OIDC redirect flow is NOT implemented. |
| **MFA** | ⚠️ Static only | MFA uses a hardcoded static OTP code (`123456`). No TOTP/HOTP, no authenticator app, no SMS/email. |
| **Password Reset** | ⚠️ Demo mode | Reset token is returned directly in the API response. No email/SMS delivery. No token expiration. |
| **Tests** | ⚠️ Minimal | Only 1 test exists (`test_health.py`). No tests for auth, RBAC, JWT, or any business logic. |
| **Frontend Error Handling** | ⚠️ Basic | Generic error messages. No retry logic. No offline detection. |

### Broken / Failing ❌

| Issue | Details |
|---|---|
| **No known runtime failures** | — (Cannot verify without running the stack) |

### Missing / Not Implemented 🚧

| Feature | Details |
|---|---|
| **CSRF Protection** | No CSRF tokens. Cookies use `samesite=lax` which provides partial protection but no CSRF token pattern. |
| **Rate Limiting** | No rate limiting on login, password reset, or any endpoint. |
| **Audit Logging** | No audit trail for logins, policy decisions, password changes. |
| **Account Lockout** | No brute-force protection. No account lockout after failed attempts. |
| **Session Revocation** | No way to invalidate sessions server-side. JWT tokens remain valid until expiry. |
| **HTTPS/TLS** | No TLS termination. Cookies set with `secure=False`. |
| **Content Security Policy** | No CSP header. |
| **HSTS Header** | No Strict-Transport-Security header. |
| **Admin UI** | No UI for managing users, policies, or viewing audit logs. |
| **Dynamic App Registry** | Workspace is hardcoded. No way to onboard new protected apps dynamically. |
| **Device Posture Checks** | No device trust evaluation. |
| **Multi-Tenancy** | Single-tenant only. |
| **SIEM Export** | No audit log export. |
| **Keycloak Theme Customization** | Uses default `keycloak` theme. Custom themes directory is empty. |
| **Gateway conf.d** | Empty directory for additional NGINX configs. |
| **Screenshots** | `docs/screenshots/` is empty. |

### Existing TODOs / FIXMEs

None found in source code comments. The codebase is clean of inline TODOs.

### CI/CD Status

| Check | Status (Expected) |
|---|---|
| Backend Ruff lint | ✅ Should pass |
| Backend Pytest | ✅ Should pass (1 test) |
| Backend Build verification | ✅ Should pass |
| Frontend ESLint | ✅ Should pass |
| Frontend TypeScript check | ✅ Should pass |
| Frontend Build | ✅ Should pass |
| Docker compose validation | ✅ Should pass |
| Docker image builds | ✅ Should pass |
| Bandit SAST | ⚠️ May flag hardcoded secrets |
| Safety dependency check | ⚠️ May flag known vulns |
| Trivy container scan | ⚠️ May flag vulns in base images |
| TruffleHog secret scan | ❌ **WILL FAIL** — .env contains real secrets |

---

## Phase 4: Security Audit

### Executive Summary

The project has a **solid architectural foundation** for a Zero Trust platform, but contains **critical security vulnerabilities** in its current state that would prevent production deployment. The most urgent issues are hardcoded secrets in version control, static MFA bypass, and lack of transport security.

### Vulnerability Rankings

---

#### 🔴 CRITICAL

| # | Finding | File | Description | Remediation |
|---|---|---|---|---|
| **C1** | **Secrets committed to Git** | `.env` | Live secrets (DB password, JWT secret, Keycloak admin creds, OTP code) are committed to the repository. `.env` is NOT in `.gitignore`. | 1. Add `.env` to `.gitignore` immediately. 2. Rotate ALL secrets. 3. Use `git filter-branch` or `bfg` to remove from history. 4. Use secrets manager (GitHub Secrets, Vault, etc.) for CI. |
| **C2** | **Static OTP bypasses MFA** | `policy-engine/app/security.py:22-23` | MFA uses a hardcoded static code (`123456`). Anyone who knows this code can bypass MFA. In "optional" mode, empty string also passes. | 1. Implement TOTP (RFC 6238) using `pyotp`. 2. Store TOTP secret per-user in database. 3. Remove static fallback. 4. Never accept empty OTP in "optional" mode. |
| **C3** | **JWT secret is placeholder** | `policy-engine/app/config.py:8` | `atlas_jwt_secret` defaults to `"replace-with-64-char-random-secret"`. If `.env` is not loaded, this weak secret is used. | 1. Generate cryptographically random 64-char secret. 2. Fail at startup if secret is the default value. 3. Use `secrets.token_urlsafe(64)` for generation. |
| **C4** | **No HTTPS — cookies insecure** | `policy-engine/app/main.py:37,46` | Cookies set with `secure=False`. All traffic over HTTP. JWT tokens transmitted in cleartext. | 1. Add TLS termination at NGINX. 2. Set `secure=True` on cookies. 3. Redirect HTTP → HTTPS. 4. Use Let's Encrypt for certs. |
| **C5** | **Password reset token leaked** | `policy-engine/app/main.py:194` | Reset token is returned directly in API response body. Anyone who intercepts the response can reset the password. | 1. Never return the token in the response. 2. Send via email/SMS only. 3. Add token expiration (e.g., 15 minutes). 4. Rate-limit reset requests. |

---

#### 🟠 HIGH

| # | Finding | File | Description | Remediation |
|---|---|---|---|---|
| **H1** | **No CSRF protection** | `policy-engine/app/main.py` | No CSRF tokens. Cookies use `samesite=lax` which helps but is insufficient for state-changing requests. | 1. Implement CSRF token pattern. 2. Use `samesite=strict` where possible. 3. Add `Origin`/`Referer` validation. |
| **H2** | **No rate limiting** | `policy-engine/app/main.py` | Login, password reset, and refresh endpoints have no rate limiting. Brute-force attacks are trivial. | 1. Add `slowapi` or middleware for rate limiting. 2. Limit login to 5 attempts/minute/IP. 3. Limit password reset to 3/hour/user. |
| **H3** | **Keycloak admin creds in .env** | `.env` | Keycloak bootstrap admin credentials stored in plaintext in `.env` which is committed to Git. | 1. Remove from `.env` and use Docker secrets. 2. Rotate credentials. 3. Restrict Keycloak admin access. |
| **H4** | **No input sanitization on password reset** | `policy-engine/app/main.py:186-194` | Password reset request accepts arbitrary username. No rate limiting. Could be used for username enumeration. | 1. Return generic message (already done — good). 2. Add rate limiting. 3. Add CAPTCHA for reset flow. |
| **H5** | **CORS allows credentials** | `policy-engine/app/main.py:25-29` | CORS configured with `allow_credentials=True` and specific origin. While better than wildcard, this still exposes cookies. | 1. Restrict to exact production origin. 2. Consider removing CORS entirely if same-origin. 3. Validate Origin header server-side. |

---

#### 🟡 MEDIUM

| # | Finding | File | Description | Remediation |
|---|---|---|---|---|
| **M1** | **No audit logging** | — | No logging of authentication events, policy decisions, or admin actions. | 1. Add structured logging (JSON). 2. Log all auth attempts (with PII redaction). 3. Log all policy decisions. 4. Consider SIEM integration. |
| **M2** | **No session revocation** | `policy-engine/app/jwt/tokens.py` | JWT tokens cannot be revoked server-side. They remain valid until expiry (30 min access, 7 days refresh). | 1. Add token blacklist (Redis or DB). 2. Implement refresh token rotation. 3. Add `jti` (JWT ID) for tracking. |
| **M3** | **No account lockout** | `policy-engine/app/main.py:81-98` | No lockout after failed login attempts. Unlimited brute-force attempts. | 1. Track failed attempts per user. 2. Lock account after N failures (e.g., 10). 3. Implement exponential backoff. |
| **M4** | **Password reset tokens don't expire** | `policy-engine/app/models.py:19-26` | `PasswordResetToken` has no expiration field. Tokens remain valid indefinitely until used. | 1. Add `expires_at` column. 2. Set expiration to 15 minutes. 3. Clean up expired tokens periodically. |
| **M5** | **No Content Security Policy** | `gateway/nginx.conf:27-29` | No CSP header. XSS in the dashboard could lead to token theft. | 1. Add `Content-Security-Policy` header. 2. Restrict script sources. 3. Use nonce-based CSP for inline scripts. |
| **M6** | **JWT uses HS256 (symmetric)** | `policy-engine/app/jwt/tokens.py` | HS256 uses the same secret for signing and verification. If secret is compromised, attacker can forge tokens. | 1. Migrate to RS256 (asymmetric). 2. Use Keycloak's public key for verification. 3. Rotate signing keys regularly. |
| **M7** | **No password complexity enforcement** | `policy-engine/app/schemas.py:5-6` | Password validation only checks length (8-128 chars). No complexity requirements. | 1. Add password strength validation. 2. Require uppercase, lowercase, digit, special char. 3. Check against common password list. |

---

#### 🟢 LOW

| # | Finding | File | Description | Remediation |
|---|---|---|---|---|
| **L1** | **No HSTS header** | `gateway/nginx.conf` | No `Strict-Transport-Security` header. | Add `add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;` |
| **L2** | **FastAPI version disclosure** | `policy-engine/app/main.py:21` | FastAPI exposes version in OpenAPI docs and response headers. | Set `docs_url=None, redoc_url=None` in production. Remove version from app title. |
| **L3** | **No XSS protection header** | `gateway/nginx.conf` | No `X-XSS-Protection` header (deprecated but defense-in-depth). | Add `add_header X-XSS-Protection "0" always;` (modern browsers use CSP instead). |
| **L4** | **Debug mode not explicitly disabled** | `policy-engine/app/main.py` | FastAPI debug mode not explicitly set to False. | Add `debug=False` in production. |
| **L5** | **Password reset token predictable prefix** | `policy-engine/app/main.py:191` | Token uses `atlas-reset-` prefix, making tokens identifiable. | Remove prefix or use purely random tokens. |

### Security Scorecard

| Category | Score | Notes |
|---|---|---|
| **Architecture** | 🟢 Strong | Zero Trust model, gateway chokepoint, internal services isolated |
| **Authentication** | 🟡 Needs work | Good JWT pattern, but static MFA and no Keycloak integration |
| **Authorization** | 🟢 Good | RBAC implemented, but functionally flat (all roles same access) |
| **Transport Security** | 🔴 Critical | No HTTPS, cookies in cleartext |
| **Secrets Management** | 🔴 Critical | Secrets committed to Git, default placeholder values |
| **Input Validation** | 🟡 Needs work | Basic Pydantic validation, but no sanitization |
| **Rate Limiting** | 🔴 Missing | No protection against brute-force |
| **Logging/Monitoring** | 🔴 Missing | No audit trail |
| **Dependency Security** | 🟡 Needs work | Safety scan in CI, but no Dependabot |
| **CI/CD Security** | 🟡 Needs work | Good tooling, but TruffleHog will fail on committed secrets |

---

## Phase 5: Future Roadmap

### Immediate (Must Fix Before Production)

1. **🔴 Remove secrets from Git** — Add `.env` to `.gitignore`, rotate all secrets, purge from history
2. **🔴 Implement real MFA** — Replace static OTP with TOTP (pyotp)
3. **🔴 Add HTTPS/TLS** — TLS termination at NGINX, secure cookies
4. **🔴 Generate strong JWT secret** — Cryptographically random, validate at startup
5. **🔴 Fix password reset** — Never return token in response, add expiration
6. **🟠 Add rate limiting** — Login, password reset, refresh endpoints
7. **🟠 Add CSRF protection** — CSRF tokens or SameSite=Strict

### Short Term (Next Sprint)

8. Integrate Keycloak OIDC flow (replace custom JWT with Keycloak tokens)
9. Add audit logging (structured JSON logs, log all auth/policy events)
10. Implement token blacklisting for session revocation
11. Add account lockout after failed attempts
12. Add Content Security Policy header
13. Expand test coverage (auth, RBAC, JWT, MFA, password reset)
14. Add Dependabot for automated dependency updates

### Medium Term

15. Migrate JWT from HS256 to RS256 (asymmetric keys via Keycloak)
16. Admin UI for user and policy management
17. Dynamic application onboarding registry
18. Device posture checks (device trust evaluation)
19. Multi-tenant support
20. SIEM integration and audit log export

### Long Term

21. Custom Keycloak themes for Atlas One branding
22. Advanced MFA (WebAuthn/FIDO2, push notifications)
23. Zero Trust Network Access (ZTNA) features
24. Service mesh integration
25. Compliance reporting (SOC2, HIPAA, etc.)

---

## Key Files Reference

| File | Purpose | Importance |
|---|---|---|
| `docker-compose.yml` | Service orchestration, networking, volumes | 🔴 Core |
| `gateway/nginx.conf` | Reverse proxy, auth_request, security headers | 🔴 Core |
| `policy-engine/app/main.py` | All API routes, auth logic | 🔴 Core |
| `policy-engine/app/config.py` | Environment configuration | 🔴 Core |
| `policy-engine/app/security.py` | Password hashing, MFA verification | 🔴 Core |
| `policy-engine/app/jwt/tokens.py` | JWT creation and validation | 🔴 Core |
| `policy-engine/app/rbac/engine.py` | Policy decision engine | 🔴 Core |
| `policy-engine/app/models.py` | Database ORM models | 🔴 Core |
| `policy-engine/app/seed.py` | Seed user creation | 🔴 Core |
| `dashboard/src/pages/LoginPage.tsx` | Login form UI | 🟡 Important |
| `dashboard/src/pages/DashboardPage.tsx` | Main dashboard UI | 🟡 Important |
| `keycloak/realm/atlas-one-realm.json` | Keycloak realm configuration | 🟡 Important |
| `.env` | Live secrets (CRITICAL: committed to Git) | 🔴 Security |
| `.github/workflows/ci.yml` | CI pipeline with security scanning | 🟡 Important |

---

## Current Blockers

| Blocker | Impact | Severity |
|---|---|---|
| `.env` committed to Git with real secrets | Secret exposure, CI pipeline will fail on TruffleHog scan | 🔴 Critical |
| Static OTP code (`123456`) | MFA is trivially bypassed | 🔴 Critical |
| No HTTPS | All credentials and tokens transmitted in cleartext | 🔴 Critical |
| JWT secret is placeholder default | Token forgery if `.env` not loaded | 🔴 Critical |
| No rate limiting | Brute-force attacks on login and password reset | 🟠 High |
| No CSRF protection | Cross-site request forgery attacks | 🟠 High |
| Keycloak not integrated into auth flow | OIDC SSO is non-functional | 🟡 Medium |

---