# CodeFull Security Measures

**Doc ID:** SEC-001 | **Version:** 0.1 draft | **Status:** for security review | **Owner:** Security lead **Upstream:** PRD-001, SRS-001, ARCH-001 | **Downstream:** Threat Model, OpenAPI, Test Plan, Test Cases, Pen Testing Plan, cursorsecurityrules.md

## 1. Security Objectives and Scope

CodeFull runs untrusted user code, holds a points ledger that behaves like money, serves competitive rankings that must be fair, and promises privacy controls to learners. The objectives, in priority order:

1. **Integrity of rewards:** no unauthorized creation, loss, or double payment of points or prizes.
2. **Host and platform safety:** user code can never escape its sandbox or reach internal systems.
3. **Tenant isolation:** no user or organization can read or change another tenant's data.
4. **Credential and key protection:** tokens, secrets, and keys are never exposed.
5. **Privacy:** anonymous entries, discreet questions, and recruiter consent are enforced by the server.
6. **Fair competition:** judging and rankings cannot be manipulated.
7. **Availability:** abuse and overload degrade gracefully instead of taking the platform down.

Scope: web, desktop and mobile clients, API gateway, all services, data stores, sandboxes, AI gateway, CI/CD, infrastructure, and third-party integrations.

## 2. Data Classification

| Class | Examples | Handling |
| --- | --- | --- |
| Public | Public portfolio, public leaderboard names, challenge catalog | Served through audited public views only; honors privacy flags |
| Internal | Lesson progress, battle standings, analytics events | Authenticated access; no public exposure |
| Confidential | Profiles, email, submissions, questions, subscription state | Encrypted at rest; owner and authorized roles only; never in logs unmasked |
| Restricted | Ledger, payout details, KYC data, secrets, keys, audit log | Field-level encryption where applicable, least privilege, step-up auth, full audit |

## 3. Trust Boundaries and Adversaries

**Trust boundaries:** client | CDN/WAF | API gateway | services | DAL | databases | Execution Gateway | sandbox | AI gateway | third parties (identity, Stripe, PayPal, push, AI provider, app stores) | CI/CD and cloud control plane.

| Adversary | Goal | Primary controls |
| --- | --- | --- |
| Cheater / colluder | Win rankings or prizes unfairly | SEC-047, SEC-069, SEC-071 |
| Point farmer / fraudster | Mint or redeem points illegitimately | SEC-021, SEC-051..060 |
| Malicious coder | Escape sandbox, mine crypto, attack the host | SEC-039..050 |
| Account taker | Hijack accounts | SEC-001..008 |
| Cross-tenant attacker | Read or modify another tenant's data | SEC-009..020 |
| Scraper / abusive recruiter | Harvest profiles | SEC-019, SEC-029, SEC-072 |
| Prompt injector | Exfiltrate prompts, abuse AI quotas, bypass challenge mode | SEC-061..067 |
| Insider / compromised admin | Abuse privileges | SEC-020, SEC-074, SEC-102, SEC-103 |
| Supply-chain attacker | Poison dependencies or images | SEC-081..090 |

## 4. Control Catalog

Each control lists where it is implemented and how it is verified. Verification IDs refer to the Test Plan suites: UT unit, IT integration, CT contract, DB pgTAP, SBX sandbox escape, SAST, DAST, PEN pen test, LOAD, REV process review.

### 4.1 Identity and sessions (owner: Identity lead)

| ID | Control | Implemented in | Verified by |
| --- | --- | --- | --- |
| SEC-001 | OIDC with PKCE for web, desktop, and mobile; no password handling in application services | Keycloak, client SDK | IT, DAST |
| SEC-002 | Access tokens about 10 minutes; refresh tokens rotating and device-bound; reuse detection revokes the family | Keycloak, gateway | IT, PEN |
| SEC-003 | TOTP and passkey MFA; mandatory for admins and moderators | Keycloak, admin service | IT, REV |
| SEC-004 | Step-up MFA for redemptions above threshold, payout detail changes, account recovery, and admin actions | gateway policy, rewards, admin | IT, PEN |
| SEC-005 | Tokens in platform secure storage only (OS keychain, Keychain, Keystore); HttpOnly SameSite cookies if cookies are used | clients | UT, PEN |
| SEC-006 | Session and device list with revocation effective within 60 seconds | identity, gateway cache | IT |
| SEC-007 | Credential-stuffing defenses: rate limits, breached-password checks, bot protection on signup and login | gateway, Keycloak | LOAD, DAST |
| SEC-008 | Hardened account recovery with cooldowns, notifications, and step-up | identity | IT, PEN |

### 4.2 Authorization and tenancy (owner: Platform lead)

| ID | Control | Implemented in | Verified by |
| --- | --- | --- | --- |
| SEC-009 | Deny by default: every route declares required role and tenant scope; missing declaration fails CI | OpenAPI x-security tags, CI lint | CT, REV |
| SEC-010 | Object-level authorization on every resource id (prevents IDOR) | domain layers | IT, DAST, PEN |
| SEC-011 | Gateway verifies identity once and sets signed internal headers; inbound internal headers are stripped; services reject unsigned requests | gateway, service deps | IT, PEN |
| SEC-012 | mTLS between all services | service mesh | IT, REV |
| SEC-013 | DAL is the only database client; credentials are dynamic and short-lived from Vault; no superuser or RLS-bypass role in application paths | DAL, Vault | IT, REV |
| SEC-014 | RLS enabled with policies in the same migration as each table; CI linter blocks violations | db/migrations, db/lint | DB, CI |
| SEC-015 | pgTAP tests prove cross-tenant read and write are blocked and anonymous rows expose no identity | db tests | DB |
| SEC-016 | Cross-tenant reads only through audited views exposing public columns | db views | DB, REV |
| SEC-017 | Privacy flags enforced in every read path: APIs, search index, leaderboards, spectator and replay streams, exports | all services, indexers | IT, PEN |
| SEC-018 | Discreet questions restricted to asker and assigned mentor; excluded from feeds, search, and counts | community, indexers | IT |
| SEC-019 | Recruiters see only profiles with recruiter visibility enabled; access logged | careers | IT, PEN |
| SEC-020 | Admin routes require step-up MFA and IP allowlisting; actions audited | admin, gateway | IT, REV |

### 4.3 Input handling and application security (owner: Backend lead)

| ID | Control | Implemented in | Verified by |
| --- | --- | --- | --- |
| SEC-021 | Server-side validation of all learning, XP, streak, and answer events; progress is derived from verified signals, never client-reported totals | learning, rewards | UT, IT |
| SEC-022 | Schema validation on all inputs; unknown fields rejected; body and array size caps | Pydantic, gateway | UT, DAST |
| SEC-023 | Parameterized queries only (sqlc); no string-built SQL, shell, or paths | DAL | SAST |
| SEC-024 | Context-aware output encoding; sanitized Markdown and HTML with allowlist; no raw HTML injection of user content | clients, services | SAST, DAST |
| SEC-025 | File uploads validated by size and magic bytes, scanned, stored privately under random names | storage service | IT, DAST |
| SEC-026 | SSRF prevention: outbound calls via allowlisted egress proxy; private and metadata ranges blocked | egress proxy, network policy | IT, PEN |
| SEC-027 | Strict CSP, HSTS, X-Content-Type-Options, frame protections; CORS origin allowlist | gateway, web app | DAST |
| SEC-028 | CSRF protection on cookie-based flows | web, gateway | DAST |
| SEC-029 | Rate limits by user, IP, and route class (auth, run, AI, redeem, search) | gateway, Redis | LOAD, DAST |
| SEC-030 | No unsafe deserialization (pickle, unrestricted YAML, eval) | all code | SAST |

### 4.4 Secrets, cryptography, and data protection (owner: Platform lead)

| ID | Control | Implemented in | Verified by |
| --- | --- | --- | --- |
| SEC-031 | Secrets only in Vault, delivered by workload identity; none in repos, images, CI variables, or client bundles | Vault, CI | SAST, REV |
| SEC-032 | Dynamic database credentials with short TTL | Vault, DAL | IT |
| SEC-033 | TLS 1.3 externally; certificate verification never disabled | gateway, clients | DAST, SAST |
| SEC-034 | Approved algorithms only (AES-256-GCM, Argon2id, Ed25519 or ECDSA P-256, SHA-256+); no custom crypto | libraries | SAST, REV |
| SEC-035 | Cryptographically secure randomness for tokens and ids | all code | SAST |
| SEC-036 | Encryption at rest with KMS-managed keys; field-level encryption for payout details and sensitive PII | storage, services | REV, PEN |
| SEC-037 | Key rotation procedures tested at least annually | Vault, KMS | REV |
| SEC-038 | Backups encrypted, access-controlled, and restore-tested | infra | REV |

### 4.5 Code execution and sandbox (owner: Execution lead)

| ID | Control | Implemented in | Verified by |
| --- | --- | --- | --- |
| SEC-039 | Execution Gateway is the only path to sandboxes; no other service launches user code | execution-gateway, network policy | IT, REV |
| SEC-040 | Mandatory limits on every job (CPU, memory, pids, disk, wall time, output size); jobs missing any limit are rejected | execution-gateway, harness | UT, SBX |
| SEC-041 | No network from sandboxes; no access to metadata endpoints or internal services | CNI policy, node pool isolation | SBX, PEN |
| SEC-042 | Read-only root filesystem, dropped capabilities, seccomp allowlist | sandbox policies | SBX |
| SEC-043 | No sandbox reuse across users or jobs; destroy after each run | execution-gateway | SBX, IT |
| SEC-044 | Hardened tier (Firecracker microVM, separate kernel) for competition-grade runs | execution-gateway, node pool | SBX, PEN |
| SEC-045 | No host mounts, no container runtime socket, no credentials inside sandboxes | sandbox images, policies | SBX, REV |
| SEC-046 | Per-user and per-IP execution quotas; detection and alerting for mining, fork bombs, and egress attempts | execution-gateway, monitoring | LOAD, SBX |
| SEC-047 | Deterministic judging from test cases and resource limits; no model decides whether code is safe, correct, or plagiarized | harness, challenges | UT, REV |
| SEC-048 | Escape-attempt suite runs on every change to images, policies, or harness | CI | SBX |
| SEC-049 | Sandbox node pools isolated from service networks, with separate cloud credentials and no instance role access | infra | PEN, REV |
| SEC-050 | Sandbox output treated as untrusted when stored or rendered | clients, services | SAST, DAST |

### 4.6 Ledger, rewards, and payments (owner: Rewards lead)

| ID | Control | Implemented in | Verified by |
| --- | --- | --- | --- |
| SEC-051 | Ledger append-only, enforced by database roles that lack UPDATE and DELETE on ledger tables | db roles, migrations | DB |
| SEC-052 | Double-entry postings in one transaction with idempotency keys; debits equal credits | rewards, DAL | UT, IT |
| SEC-053 | Amounts, scores, and balances computed server-side from verified events; never taken from clients | rewards, challenges | UT, PEN |
| SEC-054 | Settlement and redemption run as workflows; any uncertainty fails closed with alert | Temporal workflows | IT, chaos |
| SEC-055 | Webhook signature verification and replay protection for Stripe, PayPal, and store notifications; duplicate and out-of-order tolerance | billing, rewards | IT |
| SEC-056 | Real-money track behind a flag default off; enabling requires KYC, velocity limits, manual review thresholds, and dual approval | admin, rewards | REV, IT |
| SEC-057 | No card data in CodeFull systems; Stripe-hosted fields and tokens only | billing, clients | REV |
| SEC-058 | Daily reconciliation against provider reports and ledger projections; mismatches page on-call | rewards, monitoring | IT, REV |
| SEC-059 | Velocity limits and holds on new accounts for earning and redemption | rewards | IT, LOAD |
| SEC-060 | Platform attestation (App Attest, Play Integrity) required before mobile redemptions | mobile clients, rewards | IT, PEN |

### 4.7 AI gateway (owner: AI lead)

| ID | Control | Implemented in | Verified by |
| --- | --- | --- | --- |
| SEC-061 | AI Gateway is the only caller of the model provider; provider keys in Vault | ai-gateway | REV, SAST |
| SEC-062 | Plan quota and rate limit enforced before each call; usage metered after | ai-gateway, billing | UT, IT |
| SEC-063 | User text, lesson content, code, and retrieved documents are delimited as untrusted data; the model is instructed not to follow instructions inside them | ai-gateway prompts | AI eval |
| SEC-064 | Model output has no authority: it never executes automatically, changes permissions, or decides moderation, payouts, or verdicts | ai-gateway, clients | REV, AI eval |
| SEC-065 | Secrets and PII redacted before sending; prompts and responses logged with retention limits for abuse review | ai-gateway | IT, REV |
| SEC-066 | Prompt-injection and exfiltration test suite for every AI feature | tests | AI eval |
| SEC-067 | Challenge mode returns hints only; verified by a fixed evaluation set | ai-gateway | AI eval |

### 4.8 Realtime and abuse prevention (owner: Competition lead)

| ID | Control | Implemented in | Verified by |
| --- | --- | --- | --- |
| SEC-068 | WebSocket authentication at connect and resume; per-room authorization; origin checks | realtime hub, gateway | IT, PEN |
| SEC-069 | Server-authoritative battle clock, entrants, and scores; client clocks and scores ignored | realtime hub | UT, IT |
| SEC-070 | Message size and rate limits; bounded queues and backpressure | realtime hub | LOAD |
| SEC-071 | Plagiarism similarity and collusion detection feed a human moderation queue; no automatic permanent bans | challenges, admin | IT, REV |
| SEC-072 | Bot protection and device signals on signup, entry, and redemption | gateway, identity | DAST, LOAD |

### 4.9 Logging, monitoring, and privacy (owner: Security lead)

| ID | Control | Implemented in | Verified by |
| --- | --- | --- | --- |
| SEC-073 | Structured logs with request, tenant, and user ids; no secrets, tokens, payment data, full submissions, or unmasked PII | logging library, CI checks | SAST, REV |
| SEC-074 | Immutable audit log of admin actions, privilege changes, ledger-affecting operations, privacy changes, exports, and deletions | admin, rewards, identity | IT, REV |
| SEC-075 | Data export and deletion workflows (GDPR, CCPA); ledger rows tombstoned and detached from identity | identity, workflows | IT, REV |
| SEC-076 | Data minimization and classification recorded for every new field | schema docs, PR checklist | REV |
| SEC-077 | Consent records for recruiter visibility, marketing, and optional telemetry | identity | IT |
| SEC-078 | Retention enforcement per NFR-025 | jobs, partitions | IT, REV |
| SEC-079 | Security monitoring and alerting for auth anomalies, quota abuse, sandbox violations, ledger breaks, and privilege use | observability stack | REV, drills |
| SEC-080 | Production data never used in non-production without anonymization | data tooling | REV |

### 4.10 Supply chain and secure SDLC (owner: DevOps lead)

| ID | Control | Implemented in | Verified by |
| --- | --- | --- | --- |
| SEC-081 | SAST on every pull request (Semgrep, CodeQL) | CI | CI results |
| SEC-082 | Dependency and container image scanning (Trivy, Grype); block critical and high | CI | CI results |
| SEC-083 | Secret scanning in pre-commit and CI (Gitleaks) | pre-commit, CI | CI results |
| SEC-084 | Image signing (Cosign), SBOMs, admission policies rejecting unsigned or root containers | CI, Gatekeeper | REV |
| SEC-085 | Pinned dependencies with lockfiles; no latest tags or unverified installers | repos, Dockerfiles | SAST, REV |
| SEC-086 | Infrastructure as code scanning (Checkov) | CI | CI results |
| SEC-087 | Protected branches, required reviews, signed commits for sensitive repos | VCS settings | REV |
| SEC-088 | Threat model updated when a new trust boundary, data flow, or abuse case appears | PR checklist | REV |
| SEC-089 | DAST (ZAP) and API fuzzing (Schemathesis) against staging | CI, staging | DAST |
| SEC-090 | License compliance checks on dependencies | CI | CI results |

### 4.11 Client security (owner: Client lead)

| ID | Control | Implemented in | Verified by |
| --- | --- | --- | --- |
| SEC-091 | Web: no tokens in localStorage or sessionStorage; CSP; Subresource Integrity for third-party scripts | web app | DAST, SAST |
| SEC-092 | Desktop: locked-down webview, minimal command allowlist, validated IPC inputs, no remote content with privileged APIs | Tauri config | SAST, PEN |
| SEC-093 | Desktop and mobile: signed and notarized builds; update signatures verified before applying | release pipeline | REV, PEN |
| SEC-094 | Mobile: tokens in Keychain or Keystore; no secrets in the app bundle; screenshots disabled on sensitive screens where appropriate | mobile apps | SAST, PEN |
| SEC-095 | Deep links and app links validated against an allowlist; privileged actions require re-authentication | mobile, desktop | IT, PEN |
| SEC-096 | Root and jailbreak signals considered for sensitive flows | mobile apps | PEN |
| SEC-097 | Optional local code runner isolated and non-scoring; never trusted for challenges or rewards | desktop | REV, SBX |

### 4.12 Operations and assurance (owner: Security lead and SRE)

| ID | Control | Implemented in | Verified by |
| --- | --- | --- | --- |
| SEC-098 | Incident Response Plan with severity levels, playbooks, and tabletop drills before beta | IR plan | drills |
| SEC-099 | Penetration tests before beta and GA, annually after, and after major changes | Pen Testing Plan | PEN |
| SEC-100 | Vulnerability remediation SLAs: critical 7 days, high 14, medium 30 | process, tracker | REV |
| SEC-101 | Quarterly backup restore and regional failover drills | SRE runbooks | drills |
| SEC-102 | Least-privilege cloud IAM, no long-lived keys, break-glass access with alerts | cloud, Vault | REV, PEN |
| SEC-103 | Dual control for sensitive configuration (real-money flag, payout settings, key rotation) | admin, change process | REV |
| SEC-104 | Bug bounty program after GA | security program | program metrics |

## 5. Compliance Alignment

| Area | Approach |
| --- | --- |
| GDPR and CCPA | Lawful basis and consent records (SEC-077), export and deletion (SEC-075), minimization (SEC-076), breach notification within 72 hours via the IR plan |
| PCI DSS | Stripe-hosted payment fields keep CodeFull in SAQ A scope (SEC-057) |
| SOC 2 readiness | Controls in 4.9 to 4.12 map to security, availability, and confidentiality criteria; evidence collected from CI and audit logs |
| OWASP | ASVS Level 2 as the application baseline; MASVS for mobile; WSTG for testing |
| Real-money contests | Legal review per region before enabling the flag (SEC-056); store policy review for mobile |
| Children and minors | Age gate and parental-consent policy to be defined by Legal before launch (open item) |

## 6. Verification and Metrics

- Every SEC item maps to at least one test case or review record in the RTM; the security gate for release fails if any Must-level SEC item has no passing verification.
- Metrics tracked monthly: open vulnerabilities by severity and age against SLA, mean time to remediate, scan coverage, privileged action count, quota-abuse alerts, ledger reconciliation exceptions (target zero), pen test findings closed.

## 7. Exceptions and Residual Risk

- Exceptions require a written entry in the Threat Model residual-risk register with owner, justification, compensating controls, and an expiry date no more than 90 days out.
- Known residual risks for review: hypervisor-level escape against the hardened tier (mitigated by isolation layers and patch cadence), sophisticated collusion that evades similarity detection (mitigated by moderation and rate patterns), and provider-side AI behavior changes (mitigated by evals and output having no authority).

## 8. Ownership and Change Control

The Security lead owns this document. Changes go through pull request with review by the Architect and the affected area owner. cursorsecurityrules.md is updated whenever a control here changes.
