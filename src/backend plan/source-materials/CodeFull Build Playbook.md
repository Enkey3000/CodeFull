# CodeFull Build Playbook

**Doc ID:** PB-001 | **Version:** 0.1 draft | **Status:** for tech lead review | **Owner:** Tech lead **Upstream:** MVP-001, ARCH-001, SRS-001, SEC-001, TC-001, POC-001 | **Downstream:** Execution Guide, RTM

## 1. Purpose and How to Use It

The Playbook is the sequential build script for the MVP. Each step is small enough to review in one pull request, names its inputs, what to build, how to verify it, and which requirement, security, and test IDs it satisfies. A developer or an AI coding assistant works through the steps in order within each slice (S0 to S10 from MVP-001).

**Rules**

1. Do steps in order inside a slice; do not start a step whose inputs are not met.
2. Load the standing context for every step: cursorrules.md, cursorsecurityrules.md, the cited SRS and SEC items, and openapi.yaml.
3. Tests first for risky areas (marked T-first): write the cited test cases before the implementation.
4. A step is done only when its verification passes, its IDs are tagged in code, tests, and OpenAPI, and the RTM generator is green.
5. PoC results (POC-001) override assumptions here; where a step references a PoC, adopt its measured settings and ADR decisions.

### Standard step wrapper (paste with each step)

```
Context: load cursorrules.md, cursorsecurityrules.md, docs for <IDs>, contracts/openapi.
Task: <step task>
Process: 1) restate the requirement and acceptance criteria; 2) list files you will change;
3) write or update tests (cite TC IDs); 4) implement the smallest change that passes;
5) run lint, type checks, tests, and security scans; 6) update OpenAPI x-requirement tags and
requirement markers; 7) summarize what changed, what you ran, results, and open questions.
Stop and ask if: the step touches auth, tenancy, RLS, ledger, sandbox limits, or encryption in an
unplanned way, or a requirement is missing or ambiguous.
```

## 2. Slice S0: Walking Skeleton (weeks 1 to 2)

| Step | Task | Inputs | Verify | Traces |
| --- | --- | --- | --- | --- |
| PB-01 | Create the monorepo layout, tooling, pre-commit hooks (format, lint, Gitleaks), CODEOWNERS, and Conventional Commit checks | ARCH-001 sec 3; Backend Plan sec 3; cursorrules sec 2 | make lint and make test run on an empty repo | NFR-023, SEC-083 |
| PB-02 | Build the CI pipeline: build, test, SAST, dependency and image scans, IaC scan, image signing, SBOM | REL-001 sec 5 | Sample PR passes; a seeded fake secret and a vulnerable dependency are blocked | SEC-081 to 086; TC-1109, TC-1110 |
| PB-03 | Contract tooling: OpenAPI repo layout, Spectral lint, breaking-change diff, SDK generation (TypeScript first) | openapi.yaml | CI fails on a lint error and on a breaking change; SDK compiles | NFR-023; CT suite |
| PB-04 | Infrastructure baseline with Terraform and Helm: dev and staging clusters, Vault, PostgreSQL, Redis, NATS, ingress; GitOps with Argo CD | ARCH-001 sec 7 | A hello-world service deploys through Argo CD to staging | SEC-031, SEC-102 |
| PB-05 | Database baseline: migration tool, base tenant tables, roles without superuser or BYPASSRLS, RLS migration linter in db/lint, pgTAP harness (T-first) | ARCH-001 sec 5.3 | Linter rejects a table without RLS; pgTAP proves tenant A cannot read tenant B | SEC-013, 014, 015; TC-1104, TC-1105 |
| PB-06 | DAL service in Go: gRPC, sqlc, SET LOCAL of app.tenant\_id and app.user\_id per transaction, health checks | ARCH-001 sec 4.1; POC-4 results | Contract tests pass; queries without context return no rows | SEC-013; ADR-002 |
| PB-07 | API gateway (Envoy and ext-authz): JWT validation, inbound internal header stripping, signed internal headers, rate limits | ARCH-001 sec 4.1 | Direct calls with forged headers are rejected; rate limit trips | SEC-009, 011, 029; TC-1103 |
| PB-08 | FastAPI service template: layout, signature-verifying auth dependency, problem+json errors, structured logging, DAL client | cursorrules sec 4 | Template service passes unit and contract tests; logs contain no secrets | SEC-073; TC-1111 |
| PB-09 | Observability: OpenTelemetry, metrics, logs, dashboards, SLO and error-budget alerts | ARCH-001 sec 10 | A trace spans gateway, service, DAL; an induced error fires an alert | NFR-022 |
| PB-10 | Web shell: React and TypeScript, design tokens (logo-derived palette), routing, generated SDK, OIDC PKCE sign-in; end-to-end call to a /me stub through gateway, service, DAL with RLS | PRD sec 11; cursorrules sec 8 | Signed-in user sees data scoped by RLS; demo recorded | SEC-001; FR-PLT-009 (tokens) |

## 3. Slice S1: Identity and Shell (weeks 3 to 4)

| Step | Task | Inputs | Verify | Traces |
| --- | --- | --- | --- | --- |
| PB-11 | Configure Keycloak realm: email and password, GitHub and Google federation, TOTP and passkeys, token lifetimes, refresh rotation with reuse detection | SEC-001 sec 4.1 | Token tests pass; reused refresh token revokes the family | SEC-001, 002, 003; TC-0110 |
| PB-12 | Identity service: profile get and update, unique display names, migrations with RLS (T-first) | OpenAPI getMe, updateMe | TC-0104 passes; RLS tests pass | FR-IDN-004; SEC-022 |
| PB-13 | Registration, sign-in, and verification UI and flows | SRS 3.1 | TC-0101 and TC-0102 pass in E2E | FR-IDN-001, 002 |
| PB-14 | Onboarding capture and persistence | OpenAPI saveOnboarding | TC-0103 passes; skip path works | FR-IDN-003 |
| PB-15 | Shared privacy library: privacy settings model and enforcement helpers used by every read path; settings API and UI (T-first) | SEC-017; TM-CMP-004 | TC-0105 passes; payload scan finds no identity for hidden users | FR-IDN-005; SEC-017 |
| PB-16 | MFA enrollment UI and admin MFA enforcement | SEC-003 | TC-0106 passes; admin without MFA is blocked | FR-IDN-006; SEC-003, 020 |
| PB-17 | Immutable audit log: table, write API, database permissions blocking UPDATE and DELETE | SEC-074 | TC-1003 passes | FR-PLT-006; SEC-074 |
| PB-18 | Theme system: dark and light tokens, system preference, persistence; app shell navigation and responsive drawer | PRD sec 11 | TC-1004 and TC-1404 pass; contrast check on tokens | FR-PLT-009; NFR-021 |

## 4. Slice S2: Learning Core (weeks 5 to 7)

| Step | Task | Inputs | Verify | Traces |
| --- | --- | --- | --- | --- |
| PB-19 | Learning schema (courses, modules, lessons, formats) and a content import pipeline from versioned Markdown and YAML | SRS 3.2; MVP-001 content scope | Sample course imports and validates; schema checks run in CI | FR-LRN-002, 003 |
| PB-20 | Catalog and enrollment API and UI | OpenAPI listCourses, getCourse, enrollCourse | TC-0202 passes | FR-LRN-002 |
| PB-21 | Lesson delivery: text, interactive, audio with transcript, video with captions via signed CDN URLs; format switcher | SRS FR-LRN-003 | TC-0203 passes; URLs expire | FR-LRN-003; SEC-036 (private storage) |
| PB-22 | Progress and resume with idempotency and server-side validation of events (T-first) | OpenAPI recordLessonProgress | TC-0204 and TC-0207 pass | FR-LRN-004; SEC-021; TM-LRN-001 |
| PB-23 | XP, tier thresholds, promotion events through the outbox; tier display | ECO-001 sec 3 (per-tier thresholds, approved) | TC-0201, 0205, 0209 pass | FR-LRN-001, 005 |
| PB-24 | Streaks with user-day rules and multiplier cap; weekly goals | SRS FR-LRN-006, 008 | TC-0206 passes across DST and time zone cases | FR-LRN-006, 008; TM-LRN-003 |
| PB-25 | Achievements with rarity and profile display | SRS FR-LRN-007 | Badge awarded once; UAT-004 dry run | FR-LRN-007 |

## 5. Slice S3: Playground and Execution (weeks 6 to 9)

| Step | Task | Inputs | Verify | Traces |
| --- | --- | --- | --- | --- |
| PB-26 | Execution Gateway skeleton in Go: job API, mandatory limit validation, tier selection, sole entry to sandboxes (T-first); apply POC-1 settings | POC-001 POC-1; SEC-039, 040 | UT rejects any job missing a limit; only the gateway can reach sandbox pools | SEC-039, 040; ADR-004 |
| PB-27 | Sandbox images for Python 3.12 and Node, harness for test-case judging, seccomp and capability policies, no-network and metadata blocks | SEC-041 to 045 | TC-0304, TC-1203, TC-1204 pass | SEC-041 to 045; FR-EXE-003 |
| PB-28 | Warm pools and scheduling; per-user and per-IP quotas and abuse detection | NFR-003, 013 | LOAD-4 meets targets at the POC-1 sizing | NFR-003, 013; SEC-046 |
| PB-29 | Escape and leakage suite wired into CI as a required check for image or policy changes | TC-1201 to 1210 | A deliberately weakened policy fails CI | SEC-048; TM-SBX-001, 004 |
| PB-30 | Playground API: createRun, getRun, streamRun (SSE), listRuns, snippets | OpenAPI Execution tag | TC-0301, TC-0302, TC-0308 pass | FR-EXE-001, 002, 004, 007 |
| PB-31 | Playground UI with a proper code editor component, output pane, limits messaging, snippet share; interactive lesson exercises use the same runner | PRD sec 11; SRS FR-LRN-010 | TC-0208 passes; UAT-007 dry run | FR-EXE-001, FR-LRN-010 |

## 6. Slice S4: Challenges and Judging (weeks 8 to 11)

| Step | Task | Inputs | Verify | Traces |
| --- | --- | --- | --- | --- |
| PB-32 | Challenge schema, catalog API with filters, and a seed import of the first challenges with hidden tests | SRS 3.4; MVP-001 content scope | TC-0401 passes; hidden tests are never returned by any API | FR-CMP-001 |
| PB-33 | Entries with public or private visibility; privacy-safe response models for every challenge payload (T-first) | PB-15 library | TC-0404 passes: no identity for private entries in any payload | FR-CMP-005; SEC-017; TM-CMP-004 |
| PB-34 | Submission pipeline: submit, queue, judge through the Execution Gateway, verdict API with pass counts only, per-case limits | OpenAPI submitSolution, getSubmission | TC-0305 (100 identical runs) and TC-0409 pass | FR-CMP-002, 003; FR-EXE-005; SEC-047 |
| PB-35 | Event contract judged.v1 and idempotent consumers (outbox publish, deduplicated consumers) | ARCH-001 sec 6 | Replaying an event three times has no extra effect (TC-0403 precondition) | SEC-052; ADR-007 |
| PB-36 | Challenge list, detail, entry, and submission UI with verdict display | PRD sec 7 journey 3 | UAT-009 and UAT-010 dry runs; TC-0402 passes | FR-CMP-001, 002 |

## 7. Slice S5: Points and Leaderboards (weeks 10 to 13)

| Step | Task | Inputs | Verify | Traces |
| --- | --- | --- | --- | --- |
| PB-37 | Ledger schema and roles: append-only, double-entry, idempotency keys; posting library through the DAL (T-first, adopt POC-3 results) | ARCH-001 sec 5.4; POC-001 POC-3 | TC-0501, TC-0502, TC-0506 pass | FR-RWD-001; SEC-051, 052; ADR-005 |
| PB-38 | Earning rules engine consuming events (lesson, challenge, accepted answer, daily challenge) into postings | ECO-001 sec 4 earning tables (approved; values in configuration) | TC-0503 and TC-0403 pass | FR-RWD-002 |
| PB-39 | Balance and transaction history API and UI | OpenAPI getBalance, listTransactions | TC-0504 passes; UAT-013 dry run | FR-RWD-003 |
| PB-40 | Fraud and velocity rules for earning, with holds and review flags | SEC-059; TM-RWD-005 | Abnormal-rate test is held for review | FR-RWD-008; SEC-059 |
| PB-41 | Daily reconciliation job and alerts | SEC-058 | TC-0509 injected mismatch pages on-call | FR-RWD-009; SEC-058 |
| PB-42 | Leaderboards: Redis sorted sets with Postgres source of truth, anonymity handling, daily rank snapshots, nearest rivals (rank by Competition Score, ECO-001 sec 5) | SRS FR-CMP-006, 014; FR-RWD-012; ECO-001 sec 5 | TC-0404, TC-0405 pass; Redis rebuild from Postgres works | FR-CMP-006, 014; SEC-017 |

## 8. Slice S6: Billing and Plans (weeks 12 to 14)

| Step | Task | Inputs | Verify | Traces |
| --- | --- | --- | --- | --- |
| PB-43 | Plans and entitlements model with a shared entitlement check library that fails open on lookup errors and logs | SRS FR-BIL-001, 007; ADR-014 | TC-0306 and TC-0905 pass | FR-BIL-001, 007; FR-EXE-006 |
| PB-44 | Stripe Checkout and webhooks: signature verification, replay protection, idempotent handlers (T-first) | SEC-055 | TC-0901 and TC-0904 pass with Stripe test mode | FR-BIL-002; SEC-055, 057 |
| PB-45 | Usage meters (AI tokens, executions, challenge entries) and quota enforcement | SRS FR-BIL-003 | TC-0902 passes; counters match event totals | FR-BIL-003 |
| PB-46 | Invoices, plan change, and cancel at period end | SRS FR-BIL-004, 005 | TC-0903 passes; UAT-020 and UAT-021 dry runs | FR-BIL-004, 005 |
| PB-47 | Chaos check of fail-open entitlements versus fail-closed money paths | ADR-014 | TC-0905 passes with billing taken down | FR-BIL-007 |

## 9. Slice S7: AI Tutor (weeks 13 to 16)

| Step | Task | Inputs | Verify | Traces |
| --- | --- | --- | --- | --- |
| PB-48 | AI Gateway skeleton: auth, plan quota check before calls, SSE streaming, provider client with keys from Vault (adopt POC-5 settings) | POC-001 POC-5; SEC-061, 062 | TC-0802 passes; first token within NFR-008 in LOAD-7 | FR-AI-003; SEC-061, 062 |
| PB-49 | Prompt policy: delimiting of untrusted content, secret and PII redaction, challenge-mode hints-only policy (T-first) | SEC-063, 065, 067 | TC-0803, TC-0804, TC-0805 pass | FR-AI-004; SEC-063 to 067 |
| PB-50 | Tutor sessions API and UI with history | OpenAPI AI tag | TC-0801 passes; UAT-014 dry run | FR-AI-001 |
| PB-51 | Playground assistant and recommendations (rules first, model-assisted second) | SRS FR-AI-002, 005; FR-LRN-009 | Suggestions never auto-run (TC-0806) | FR-AI-002, 005; FR-LRN-009 |
| PB-52 | Evaluation harness in CI for injection and solution-leak sets; rate and report responses | TM-AI-001 to 003 | Eval thresholds enforced on prompt or model changes; TC-0807 passes | FR-AI-006; SEC-066 |

## 10. Slice S8: Community (weeks 14 to 17)

| Step | Task | Inputs | Verify | Traces |
| --- | --- | --- | --- | --- |
| PB-53 | Community schema, open and discreet questions, access control for discreet items including the MVP mentor assignment rule (confirm GAP-014) | SRS FR-COM-001, 002 | TC-0601 and TC-0602 pass | FR-COM-001, 002; SEC-018 |
| PB-54 | Answers, votes, accepted answers (points through the ledger), reputation | SRS FR-COM-003, 004 | TC-0603 and TC-0606 pass | FR-COM-003, 004 |
| PB-55 | Flagging and moderation intake | SRS FR-COM-007 | TC-0605 passes | FR-COM-007; SEC-074 |
| PB-56 | Sanitization of user content and stored-XSS tests; notification hooks for answers | SEC-024, 027 | TC-0604 passes; UAT-017 and UAT-018 dry runs | SEC-024, 027; FR-COM-008 |

## 11. Slice S9: Platform and Compliance (weeks 15 to 18)

| Step | Task | Inputs | Verify | Traces |
| --- | --- | --- | --- | --- |
| PB-57 | Notifications service: in-app and email, preferences | SRS FR-PLT-001 | TC-1001 passes | FR-PLT-001; NFR-010 |
| PB-58 | Search on Postgres full-text behind a search port, indexing that honors privacy flags (MVP simplification, ADR-015 proposed) | MVP-001 sec 5; SEC-017 | Hidden users and discreet items never appear; search latency within NFR-009 | FR-PLT-002; SEC-017, 018 |
| PB-59 | Admin console: moderation queue, flags with dual control for sensitive flags, audit trail | SRS FR-PLT-004, 005 | TC-1002 and TC-1005 pass; UAT-029 dry run | FR-PLT-004, 005; SEC-020, 103 |
| PB-60 | Data export and account deletion workflows | SEC-075 | TC-0107 and TC-0108 pass | FR-IDN-007; SEC-075 |
| PB-61 | Automated authorization matrix and IDOR suites generated from OpenAPI roles | SEC-009, 010 | TC-1101 and TC-1102 run in CI | SEC-009, 010; TM-TEN-002 |

## 12. Slice S10: Hardening and Beta (weeks 19 to 22)

| Step | Task | Inputs | Verify | Traces |
| --- | --- | --- | --- | --- |
| PB-62 | Run LOAD-1 to LOAD-5 and tune; chaos tests for Redis, Postgres, and NATS | TP-001 sec 5 | TC-1301 to 1309 meet targets | NFR-001 to 016 |
| PB-63 | Security hardening pass: headers and CSP, CORS, dependency and image gates, TLS settings, log scans | SEC-001 sec 4.3 | TC-1108, 1110, 1111 pass | SEC-027, 033, 073 |
| PB-64 | Pen test PT-1, remediation, and retest | PTP-001 | No open critical or high findings | SEC-099; TM-001 |
| PB-65 | Accessibility and compatibility passes including empty and error states | TP-001 sec 6 | TC-1401 to 1406 pass | NFR-019, 020, 021 |
| PB-66 | Backup restore drill, failover drill, incident tabletops for INC-1, INC-2, INC-4 | IRP-001 sec 11 | TC-1310 passes; tabletop notes filed | SEC-098, 101; NFR-015 |
| PB-67 | UAT cycles, fix window, RTM gate, go/no-go, beta launch | UAT-001; REL-001 sec 9 | UAT exit criteria met; RTM gate green | All Must requirements |

## 13. After the MVP: Fast-Follow Outline

Each item becomes its own slice with its own steps, written when scheduled and informed by PoC results.

| Slice | Content | Key requirements | Adopt |
| --- | --- | --- | --- |
| F1 | Hardened tier and live battles with spectators | FR-EXE-008, FR-CMP-008, 009, 010; SEC-044, 068 to 070 | Firecracker pool (POC-1), realtime hub (POC-2) |
| F2 | Plagiarism and collusion review | FR-CMP-013; SEC-071 | Moderation tooling |
| F3 | Prize pools, settlement, redemption of points | FR-RWD-004, 005, 006; SEC-054, 056 | Temporal workflows (POC-3, ADR-006) |
| F4 | Tournaments and team events | FR-CMP-011, 012 | Workflows |
| F5 | Mentors, bookings, escrow | FR-COM-005, 006 | Ledger holds |
| F6 | Careers and recruiter marketplace | FR-CAR-001 to 004 | Consent and rate controls |
| F7 | Starter plan, store billing, push, desktop and mobile shells | FR-BIL-006, FR-LRN-012; SEC-060, 092 to 097 | POC-6 shells |
| F8 | OpenSearch and ClickHouse if scale or features require them | FR-PLT-002, 003 | ADR-015 follow-up |

## 14. Maintaining the Playbook

- Update it when a PoC decision, ADR, or SRS change affects a step; version the file with the code.
- When a step is completed, record the PR link and date in the Execution Guide tracker; do not rewrite history.
- If a step proves too large for one PR, split it and keep the traces on each part.
- New steps must name inputs, verification, and trace IDs before they are scheduled.

## 15. Version 0.2 Step Additions (ECO-001 approved)

The approved points economy adds these steps. Placement shows where each runs inside the existing slices.

| Step | Task | Placement | Inputs | Verify | Traces |
| --- | --- | --- | --- | --- | --- |
| PB-68 | Versioned economy configuration: earning rates and caps, multiplier curve, XP awards, catalog prices, fraud thresholds, effective dates; services read the active version; every ledger transaction records its config version (T-first) | Before PB-38 in S5 | ECO-001 sec 11; DM-001 sec 8 | TC-0523 passes; a config change is audited | FR-RWD-002; SEC-074 |
| PB-69 | Ledger buckets and funding accounts: account kinds (user\_learning, user\_prize, prize\_fund, pool, issuance, sink, adjustment), seeded system accounts, spending order learning first then prize (T-first) | After PB-37 in S5 | ECO-001 sec 6; DM-001 sec 8 | TC-0515 and TC-0519 pass | FR-RWD-011, 013; SEC-052, 054 |
| PB-70 | Competition Score: ledger entries flagged competition, derived projection, nightly rebuild, leaderboard seeding, weekly window | With PB-42 in S5 | ECO-001 sec 5 | TC-0516 and TC-0524 pass | FR-RWD-012; FR-CMP-006 |
| PB-71 | Catalog and purchases: catalog from configuration, purchase API with Idempotency-Key, unlock rows, streak freeze effect, UI | After PB-39 in S5 | OpenAPI listCatalog, purchaseCatalogItem, listUnlocks | TC-0514 and TC-0515 pass; UAT-038 dry run | FR-RWD-010, 011; SEC-052, 053 |
| PB-72 | Lesson exercise allowance: run context field, separate exercise rate limit, exemption from the Free execution quota | After PB-30 in S3; verified in S6 | OpenAPI createRun context | TC-0521 passes | FR-EXE-006; FR-LRN-010 |
| PB-73 | Earning caps and streak multiplier engine, issuance budget tracking and alerts | Within PB-38 in S5 | ECO-001 sec 4, 10 | TC-0517 and TC-0520 pass | FR-RWD-002; SEC-079 |

Also note for PB-23: XP thresholds are per tier with surplus carry (TC-0522). In the fast-follow slice F3 (prize pools, settlement, redemption), funded prizes (FR-RWD-013) and the prize split rules (TC-0518) apply.
