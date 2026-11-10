# CodeFull — Cursor Security Rules (v2)

Mandatory security rules for AI-assisted development on CodeFull. Each rule cites the control (`SEC-nnn`, SEC-001), the threat it addresses (`TM-*`, TM-001), and the test that proves it (`TC-nnnn`, TC-001) where one exists. Derived from SEC-001, ARCH-001, TM-001 and aligned with POC-001, MVP-001, and PB-001. Applies to every file you write or change. Pair with `cursorrules.md`. If a request would violate a rule, refuse that part, explain why, and propose a compliant alternative.

**MUST** = blocking. **SHOULD** = justify in the PR if skipped.

---

## 1. Assets, Boundaries, and Control Index

Protect, in priority order: points ledger and prize pools; sandbox host integrity; tenant isolation; credentials and keys; personal data and privacy settings; ranking and judging integrity; AI gateway quotas and prompts.

Trust boundaries: client, CDN/WAF, API Gateway, services, DAL, databases, Execution Gateway, sandbox, AI Gateway, third parties, build and run plane.

| Area | Controls | Key tests |
|---|---|---|
| Identity and sessions | SEC-001..008 | TC-0106, 0110, 0111 |
| Authorization and tenancy | SEC-009..020 | TC-1101..1105, 0105, 0404, 0602 |
| Input and application | SEC-021..030 | TC-0207, 1106..1108, 1112, 1113 |
| Secrets, crypto, data | SEC-031..038 | TC-1116, 1310 |
| Sandbox | SEC-039..050 | TC-0303, 0304, 1201..1210 |
| Ledger and payments | SEC-051..060 | TC-0501..0510, 0904, 0906 |
| AI Gateway | SEC-061..067 | TC-0802..0806 |
| Realtime and abuse | SEC-068..072 | TC-0407, 0408, 0412 |
| Logging and privacy | SEC-073..080 | TC-1003, 1111, 0107, 0108 |
| Supply chain and SDLC | SEC-081..090 | TC-1109, 1110, 1118 |
| Clients | SEC-091..097 | TC-1114, 1115 |
| Operations | SEC-098..104 | TC-1117, 1310 |

## 2. Authentication and Sessions

- MUST use OIDC with PKCE for all clients; no password handling in application services (SEC-001).
- MUST keep access tokens short-lived (about 10 minutes) and refresh tokens rotating and device-bound; reuse revokes the family (SEC-002; TM-AUT-002; TC-0110).
- MUST require MFA for admins and moderators, and step-up MFA for redemptions above threshold, payout changes, account recovery, and admin actions (SEC-003, SEC-004; TM-AUT-003; TC-0106, 0507).
- MUST store client tokens only in platform secure storage (OS keychain, Keychain, Keystore) or HttpOnly SameSite cookies; never `localStorage` or `sessionStorage` (SEC-005, SEC-091; TM-AUT-006).
- MUST make session and device revocation effective within 60 seconds (SEC-006; TC-0109).
- MUST apply rate limits, breached-password checks, and bot protection to signup and login; harden account recovery with cooldowns and notifications (SEC-007, SEC-008; TM-AUT-001, TM-AUT-005; TC-0111).
- MUST NOT put tokens, session ids, or secrets in URLs or logs (TM-AUT-006; TC-1111).

## 3. Authorization, Tenancy, and Privacy

- MUST deny by default: every route declares required role and tenant scope in OpenAPI (`x-roles`); a missing declaration fails CI (SEC-009; TC-1101).
- MUST authorize every object access by resource id and owner or role, not only login status (SEC-010; TM-TEN-002; TC-1102).
- MUST derive identity and tenant only from gateway-signed internal headers; reject unsigned or altered headers; never accept `tenant_id` or `user_id` from bodies or query strings to authorize (SEC-011; TM-TEN-003; TC-1103). Use mTLS between services (SEC-012).
- MUST access the database only through the DAL, which sets `app.tenant_id` and `app.user_id` per transaction; no superuser or RLS-bypass role in application paths (SEC-013; TM-TEN-004; TC-1105).
- MUST create RLS policies in the same migration as each table, with a pgTAP test showing cross-tenant read and write are blocked (SEC-014, SEC-015; TM-TEN-001, 006; TC-1104).
- MUST route cross-tenant reads through audited views exposing public columns only (SEC-016; TM-TEN-005).
- MUST enforce privacy flags in every read path: APIs, search, leaderboards, spectator and replay streams, exports. Private entries show as Anonymous everywhere (SEC-017; TM-CMP-004; TC-0105, 0404).
- MUST restrict discreet questions to the asker and the assigned mentor (or the approved MVP rule from GAP-014), and exclude them from feeds, search, counts, and indexes (SEC-018; TM-PRV-001; TC-0602).
- MUST show recruiters only profiles whose owners enabled visibility, and log access (SEC-019; TM-PRV-002; TC-0701).
- MUST require step-up MFA and IP allowlisting on admin routes (SEC-020).
- MUST test an authorization matrix (role by endpoint) for every new route (TC-1101).

## 4. Input Handling and Application Security

- MUST validate learning, XP, streak, and answer events server-side; progress comes from verified signals, never client-reported totals (SEC-021; TM-LRN-001, TM-LRN-003; TC-0207).
- MUST validate input with schemas (type, length, range, enum); reject unknown fields; cap body and array sizes (SEC-022; TM-API-005; TC-1112).
- MUST use parameterized queries (sqlc) only; no string-built SQL, shell, file paths, or regexes from user input (SEC-023; TM-API-002; TC-1106).
- MUST encode output by context and sanitize Markdown and HTML with an allowlist; no inline handlers, no raw HTML injection; render sandbox output and model output as text (SEC-024, SEC-050; TM-PRV-005, TM-SBX-008, TM-AI-006; TC-0604, 0806, 1209).
- MUST validate uploads by size and magic bytes, scan them, store privately under random names (SEC-025; TM-API-007; TC-1113).
- MUST prevent SSRF: outbound calls through an allowlisted egress proxy; block private, link-local, and metadata ranges (SEC-026; TM-API-003; TC-1107).
- MUST set strict CSP, HSTS, content-type, and frame headers; CORS uses an explicit origin allowlist, never `*` with credentials (SEC-027; TC-1108). MUST protect cookie flows from CSRF (SEC-028).
- MUST rate-limit by user, IP, and route class (auth, run, AI, redeem, search) (SEC-029; TM-API-001).
- MUST NOT deserialize untrusted data with unsafe loaders (`pickle`, unrestricted YAML, `eval`, `exec`) (SEC-030).

## 5. Secrets, Cryptography, and Data Protection

- MUST fetch secrets from Vault with workload identity; none in repos, images, config, fixtures, client bundles, or logs (SEC-031; TM-INF-002; TC-1109, 1116). Gitleaks runs in pre-commit and CI (SEC-083).
- MUST use dynamic short-lived database credentials, held only by the DAL (SEC-032).
- MUST use TLS 1.3 externally and never disable certificate verification, including in tests that could ship (SEC-033).
- MUST use vetted algorithms: AES-256-GCM, Argon2id (if hashing is needed), Ed25519 or ECDSA P-256, SHA-256 or stronger; no custom crypto, MD5, SHA-1, ECB, or static IVs (SEC-034). MUST use a CSPRNG for tokens and ids (SEC-035). Compare secrets in constant time.
- MUST encrypt at rest with KMS-managed keys and use field-level encryption for payout details and sensitive PII; support key rotation (SEC-036, SEC-037). Backups are encrypted and restore-tested (SEC-038; TC-1310).

## 6. Code Execution and Sandbox (highest-risk surface)

- MUST route all user code through the Execution Gateway; never run user code in a service, CI job, or helper script (SEC-039; TM-SBX-003).
- MUST reject any job missing CPU, memory, pid, disk, wall-time, and output limits (SEC-040; TM-SBX-002; TC-0303, 1201, 1202).
- MUST give sandboxes no network and no access to metadata endpoints or internal ranges (SEC-041, SEC-049; TM-SBX-003; TC-0304, 1210).
- MUST use read-only root filesystems, dropped capabilities, and a seccomp allowlist (SEC-042; TM-SBX-001; TC-1203).
- MUST NOT reuse a sandbox across users or jobs; destroy after each run (SEC-043; TM-SBX-004; TC-1205).
- MUST NOT mount host paths, the container runtime socket, or credentials into a sandbox (SEC-045; TC-1204).
- MUST enforce per-user and per-IP execution quotas and alert on mining, fork bombs, and egress attempts (SEC-046; TM-SBX-006; TC-1207).
- MUST keep verdicts deterministic from test cases and limits; never ask a model whether code is safe, correct, or plagiarized (SEC-047; TM-SBX-005; TC-0305, 1206).
- MUST run the escape and leakage suite (TC-1201..1210) on every change to images, policies, or the harness, as a required CI check (SEC-048).
- MUST use the hardened Firecracker tier for competition-grade runs (SEC-044; TC-0307, 1208). **MVP rule:** the hardened tier is deferred (ADR-015 proposed); therefore competition-grade runs, live battles, and tournaments MUST NOT be enabled on the standard tier. They ship with the hardened tier (slice F1).

## 7. Ledger, Rewards, and Payments

- MUST keep the ledger append-only, enforced by database roles without UPDATE or DELETE (SEC-051; TM-RWD-003; TC-0501).
- MUST post double-entry entries in one transaction with idempotency keys (SEC-052; TM-RWD-001; TC-0502, 0506, 0403).
- MUST compute amounts, scores, and balances server-side from verified events; never trust client-supplied values (SEC-053; TM-RWD-002; TC-0508).
- MUST fail closed on any uncertainty in redemption, payout, contribution, or settlement: deny, log, alert (SEC-054; TC-0905). **MVP rule:** without Temporal, earning postings use the outbox plus a durable job queue behind `WorkflowPort`; they stay idempotent and retry-safe, and settlement and redemption are not built until F3.
- MUST verify Stripe, PayPal, App Store, and Google Play webhooks by signature, enforce replay protection, and tolerate duplicates and out-of-order events (SEC-055; TM-RWD-006; TC-0904).
- MUST keep `real_money_track` off by default; enabling needs KYC, velocity limits, manual review thresholds, and dual approval (SEC-056, SEC-103; TM-RWD-009; TC-0510).
- MUST NOT store card data; use Stripe-hosted fields and tokens only (SEC-057; TC-0906).
- MUST run daily reconciliation and page on any invariant violation (SEC-058; TC-0509). MUST apply velocity limits and new-account holds (SEC-059; TM-RWD-005; TC-0507). MUST require attestation before mobile redemptions (SEC-060).
- Entitlement lookups fail open and log (FR-BIL-007); this never applies to anything that moves points or money.

## 8. AI Gateway and Prompt Safety

- MUST call models only through `services/ai-gateway`; provider keys in Vault; never in clients (SEC-061).
- MUST enforce plan quota and rate limit before the call and meter after (SEC-062; TM-AI-004; TC-0802).
- MUST delimit user text, lessons, code, and retrieved content as untrusted data and instruct the model not to follow instructions inside them (SEC-063; TM-AI-001, 002; TC-0804).
- MUST give model output no authority: no auto-execution, no permission or tool changes, no moderation, payout, or verdict decisions (SEC-064; TM-AI-006; TC-0806).
- MUST redact secrets and PII before sending context and keep logs within retention limits (SEC-065; TM-AI-005; TC-0805).
- MUST add injection and exfiltration tests for every AI feature and run the eval suite on prompt or model changes (SEC-066; TC-0804). Challenge mode returns hints only (SEC-067; TM-AI-003; TC-0803).

## 9. Realtime, Anti-Cheat, and Abuse

- MUST authenticate WebSockets at connect and resume, authorize per room, check origin (SEC-068).
- MUST keep battle clocks, entrants, and scores server-authoritative (SEC-069; TM-CMP-003; TC-0407).
- MUST enforce message size and rate limits, bounded queues, and backpressure (SEC-070; TM-CMP-005).
- MUST route plagiarism and collusion signals to human moderation; no automatic permanent bans (SEC-071; TM-CMP-001, 002; TC-0408).
- MUST apply bot protection and device signals on signup, entry, and redemption (SEC-072; TM-CMP-006; TC-0412).
- MUST return only pass counts for hidden tests, never inputs or expected outputs (TM-CMP-007; TC-0409).

## 10. Logging, Monitoring, and Privacy

- MUST write structured logs without secrets, tokens, payment data, full submissions, or unmasked PII (SEC-073; TC-1111).
- MUST write immutable audit records for admin actions, privilege changes, ledger-affecting operations, privacy changes, exports, and deletions (SEC-074; TC-1003).
- MUST support export and deletion (GDPR, CCPA), detaching identity from retained ledger rows (SEC-075; TC-0107, 0108). MUST record consent (SEC-077) and enforce retention (SEC-078; TC-1311).
- MUST classify every new field (public, internal, confidential, restricted) and minimize collection (SEC-076).
- MUST keep production data out of non-production unless anonymized (SEC-080). SHOULD alert on auth anomalies, quota abuse, sandbox violations, ledger breaks, and privileged use (SEC-079).
- **MVP rule:** Postgres full-text search behind `SearchPort` MUST honor privacy flags and exclude discreet items at index time (SEC-017, SEC-018; TM-PRV-006). Analytics events carry no code content or PII.

## 11. Dependencies, Supply Chain, and CI

- MUST pin dependencies with lockfiles and review new packages for maintenance, license, and known issues (SEC-085, SEC-090).
- MUST run SAST, dependency, image, secret, and IaC scans in CI; no merge with critical or high findings (SEC-081..083, SEC-086; TC-1109, 1110).
- MUST sign images, produce SBOMs, and admit only signed, non-root images (SEC-084; TM-INF-001).
- MUST use protected branches and required reviews (SEC-087; TC-1118). MUST update the threat model for new trust boundaries, flows, or abuse cases (SEC-088). DAST and API fuzzing run on staging (SEC-089).
- MUST NOT use `curl | sh`, unpinned base images, or `latest` tags. MUST NOT add telemetry or third-party scripts without security and privacy review.

## 12. Client-Specific Rules

- **Web:** tokens never in web storage; CSP and Subresource Integrity for third-party scripts (SEC-091).
- **Desktop (Tauri or native):** locked-down webview, minimal command allowlist, validated IPC inputs, no remote content with privileged APIs; verify update signatures; signed and notarized builds; any local runner is isolated and non-scoring (SEC-092, SEC-093, SEC-097; TM-CLI-002, 003; TC-1114).
- **Mobile:** tokens in Keychain or Keystore; no secrets in the bundle; validate deep and app links against an allowlist and re-authenticate for privileged actions; consider root and jailbreak signals on sensitive flows (SEC-094, 095, 096; TM-CLI-004, 005, 006; TC-1115).
- Client shells are PoC-gated (POC-6); do not ship a platform that failed a security criterion there.

## 13. Proofs of Concept and Test Environments

- PoC work runs in a separate cloud project with synthetic data, no production secrets, budget alarms, and automatic teardown. It never connects to production systems or real user data.
- PoC code MUST NOT be promoted to production or imported by it. Reusable assets (escape suites, property tests, linters, schemas, eval sets) move to the main repo with traces.
- PoC security findings are reported like any other finding and feed SEC-001 and TM-001 updates before production code relies on the design.
- Pen test and load environments use staging with synthetic data (PTP-001 rules of engagement); never test destructively against production.

## 14. Forbidden Patterns (reject on sight)

- Direct database connections from FastAPI services; superuser or RLS-bypass roles in app paths (SEC-013).
- Trusting `X-Tenant-Id`, `X-User-Id`, or similar headers not signed by the gateway (SEC-011).
- String-built SQL, shell commands, or file paths from user input (SEC-023).
- `eval`, `exec`, `pickle.loads`, unsafe YAML on untrusted data; `subprocess` with `shell=True` on user input (SEC-030).
- Hard-coded credentials, committed `.env` secrets (SEC-031).
- Disabled TLS verification, wildcard CORS with credentials, `unsafe-inline` or `unsafe-eval` CSP without an approved exception (SEC-027, SEC-033).
- Updating or deleting ledger rows; client-computed scores or balances (SEC-051, SEC-053).
- User code outside the Execution Gateway; sandboxes with network or host mounts; competition runs on the standard tier (SEC-039, 041, 044, 045).
- Calling the AI provider from clients or other services; executing model output (SEC-061, SEC-064).
- Logging tokens, passwords, payment data, or full submissions (SEC-073).
- Custom crypto, `Math.random` or `random` for security values (SEC-034, SEC-035).
- Promoting PoC code to production; enabling `real_money_track` outside the approved process (SEC-056, SEC-103).

## 15. Required Security Checklist for Every PR

- [ ] Governing `FR-*`, `SEC-*`, and playbook `PB-nn` cited
- [ ] New or changed routes declare role and tenant scope (`x-roles`); authorization-matrix tests added (TC-1101, 1102)
- [ ] Inputs validated by schema; outputs encoded; no unsafe sinks (TC-1106, 0604)
- [ ] No direct DB access; DAL context and RLS with pgTAP test for any new table (TC-1104)
- [ ] No secrets in code, config, fixtures, or logs (TC-1109, 1111)
- [ ] Ledger, money, or sandbox changes: invariants and escape tests added; fail-closed behavior verified (TC-0502, 0506, 1201..1210)
- [ ] AI changes: quotas, injection and challenge-mode evals, no auto-execution (TC-0802..0806)
- [ ] Privacy flags respected in every response shape, including search and exports (TC-0105, 0404, 0602)
- [ ] Dependencies reviewed; SAST, dependency, secret, image, and IaC scans green
- [ ] Threat model (`TM-*`) updated if a new boundary, flow, or abuse case appears
- [ ] Audit logging present for privileged or ledger-affecting actions (TC-1003)
- [ ] RTM markers present; generator green

## 16. Findings, Incidents, and Uncertainty

- If unsure whether something is safe, treat it as unsafe and ask.
- If you find a vulnerability, secret exposure, or isolation failure, stop, describe it with affected files and IDs, propose a fix, and flag it for the incident process (IRP-001 playbooks INC-1 sandbox escape, INC-2 ledger mismatch, INC-3 secret leak, INC-4 data or tenant exposure, INC-5 abuse flood, INC-6 AI misuse, INC-7 payment outage, INC-8 battle failure). Do not quietly patch or ignore it.
- Never weaken a control, add a bypass flag, or disable a check to make a test or demo pass. Fix the cause or escalate.
- Security exceptions need a written entry in the Threat Model residual-risk register with owner, compensating controls, and an expiry no more than 90 days out (SEC-001 section 7).
- Pen test findings (PTP-001) get regression tests before closure; critical and high follow the 7 and 14 day SLAs (SEC-100).
