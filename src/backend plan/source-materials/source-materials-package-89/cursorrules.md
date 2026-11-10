# CodeFull — Cursor Rules (v2)

Engineering rules for AI-assisted development on CodeFull. Derived from PRD-001, SRS-001, ARCH-001, and SEC-001, and aligned with POC-001, MVP-001, and PB-001. Security rules live in `cursorsecurityrules.md`; follow both. If a rule here conflicts with a signed-off document, the document wins: say so and ask.

---

## 0. How to Work

1. **Read before writing.** Find the governing requirement (`FR-*`, `NFR-*`, `SEC-*`) and the playbook step (`PB-nn`) before changing code. If none exists, stop and ask; never invent scope.
2. **Cite IDs everywhere.** Branches, commits, PR text, tests, and OpenAPI operations carry the IDs they implement (see section 1). The RTM generator fails the build on missing or dangling IDs.
3. **Work in vertical slices (S0 to S10, MVP-001).** One playbook step per PR; each step names inputs, verification, and traces. Do not start a step whose inputs are unmet.
4. **Contract first.** Change `contracts/openapi` (or `contracts/proto`) first, regenerate SDKs, then implement.
5. **Tests ship with code, and come first for risky areas** (T-first steps in PB-001: privacy, ledger, sandbox, authorization, webhooks, AI policy).
6. **Small diffs.** One concern per change; no drive-by refactors.
7. **Ask when ambiguous.** One precise question beats a guess that touches money, tenancy, auth, privacy, or the sandbox. Open decisions are listed in section 3.4: do not guess them.
8. **Do not hand-edit** generated code (`contracts/sdk/**`), applied migrations, or lockfiles.
9. **Never claim verification you did not run.** State the commands you ran and their results.

## 1. Document Authority and ID Scheme

Order of authority: PRD-001, SRS-001, ARCH-001 (with approved ADRs), SEC-001, then everything else.

| Prefix | Meaning | Source |
|---|---|---|
| BG-nn | Business goal | PRD-001 |
| FR-DOM-nnn, NFR-nnn | Functional and non-functional requirements | SRS-001 |
| SEC-nnn | Security control (001 to 104) | SEC-001 |
| TM-AREA-nnn | Threat | TM-001 |
| ADR-nnn | Architecture decision (ADR-015 proposed) | ARCH-001 |
| API-operationId | API operation | openapi.yaml |
| TC-nnnn, UAT-nnn | Test case, acceptance scenario | TC-001, UAT-001 |
| POC-n, PB-nn, S0 to S10, GAP-nnn | PoC, playbook step, slice, gap | POC-001, PB-001, MVP-001, GAP-001 |

Domain codes: IDN, LRN, EXE, CMP, RWD, COM, CAR, AI, BIL, PLT. Example: commit `feat(rewards): post earning entries [FR-RWD-002, SEC-052, PB-38]`.

## 2. Product Guardrails (PRD-001, SRS-001)

- Product: learn, compete, earn. Six tiers (Beginner, Intermediate, Advanced, Expert, Master, Guru); four lesson formats; Free, Starter, Pro, Enterprise plans.
- **MVP scope (build now):** FR-IDN-001..007; FR-LRN-001..010; FR-EXE-001..007; FR-CMP-001, 002, 003, 005, 006, 014; FR-RWD-001, 002, 003, 008, 009; FR-COM-001, 002, 003, 004, 007, 008; FR-AI-001..006; FR-BIL-001..005, 007; FR-PLT-001, 002, 004, 005, 006, 009.
- **Fast follow (flagged, not built until scheduled):** FR-EXE-008, FR-CMP-004, 007..013, FR-RWD-004..006, FR-COM-005, 006, FR-CAR-001..004, FR-BIL-006, FR-LRN-011, 012, FR-IDN-008, 010, FR-PLT-003, and the Starter plan.
- **Phase 2 (off by default):** FR-RWD-007 cash and gift-card redemption, FR-CAR-005, FR-IDN-009, FR-PLT-007, FR-PLT-008. The `real_money_track` flag stays off in every environment; never build or expose a cash path outside it (SEC-056, SEC-103).
- **Privacy is a product promise enforced server-side:** FR-IDN-005 (privacy controls), FR-CMP-005 (private entries show as Anonymous everywhere), FR-COM-002 (discreet questions), FR-CAR-002 (recruiter consent). Never rely on the UI alone (SEC-017, 018, 019).
- Non-goals: no cash prizes at MVP, no native desktop or mobile apps at MVP, no AI that judges code correctness, safety, or cheating, no user-hosted runners.
- Do not publish placeholder marketing figures from the prototype (128K coders, $2.4M prizes). Use real data or omit.

## 3. MVP Build Pattern and Proposed Simplifications (MVP-001, PB-001)

### 3.1 Slices
S0 skeleton, S1 identity, S2 learning, S3 playground and execution, S4 challenges, S5 points and leaderboards, S6 billing, S7 AI tutor, S8 community, S9 platform and compliance, S10 hardening and beta. Walking skeleton first; every slice crosses UI, API, service, DAL and migration (with RLS), tests, docs, analytics events, and a feature flag.

### 3.2 Cut lines and never-cut list
If behind, cut in this order with Product approval: AI recommendations to rule-based, achievements and weekly goals, snippet sharing polish, reputation, weekly leaderboard detail, JavaScript runtime. **Never cut:** tenant isolation and RLS, privacy enforcement, ledger integrity and reconciliation, sandbox isolation and limits, authorization, admin MFA, CI security gates, pen test, UAT.

### 3.3 Proposed MVP simplifications (ADR-015, pending approval)
Build to ports so engines can be swapped later; do not hard-wire a simplification and do not build the deferred engines early.

| Deferred (full architecture) | MVP approach | Port to code against |
|---|---|---|
| OpenSearch | Postgres full-text search (FR-PLT-002), still honoring privacy flags (SEC-017) | `SearchPort` |
| ClickHouse | Postgres rollups and materialized views; events still emitted | `AnalyticsPort` |
| Temporal | Outbox plus durable job queue for earning postings and notifications | `WorkflowPort` |
| Firecracker hardened tier | gVisor standard tier only; no competition-grade runs until F1 (FR-EXE-008, SEC-044) | `SandboxTier` |
| Desktop and mobile apps | Responsive web only | n/a |

Until ADR-015 is approved, treat it as the plan, not as permission to delete the full-architecture interfaces.

### 3.4 Open decisions: ask, do not guess (GAP-001)
Ranking metric for leaderboards (GAP-013); XP threshold interpretation, per tier or cumulative (GAP-016); MVP mentor assignment rule for discreet questions (GAP-014); whether interactive exercises consume execution quota (GAP-017); points earn rates, redemption values, and plan limits (GAP-018, GAP-023); minor-user policy (GAP-025). Put economy and limits in configuration, never hard-coded constants.

## 4. Proofs of Concept (POC-001)

- **PoC code lives apart.** Under `/poc` in a separate cloud project, using synthetic data and no real secrets. Production code never imports PoC code; rewrite for production.
- **Decide before depending.** POC-1 sandbox, POC-2 realtime hub, POC-3 ledger and workflows, POC-4 RLS through the DAL, POC-5 AI gateway, POC-6 client shells each end in Go, Pivot, or Stop. If the decision is not recorded, build only behind interfaces and flags and say so in the PR.
- **Measured numbers win.** Capacity, latency, and cost values (NFR-003, 004, 006, 013, NFR-008, pool sizes, per-run cost) come from PoC reports and replace assumptions; update ARCH-001 and SRS-001 in the same change.
- **Adopt through ADRs.** A PoC result that changes design needs an ADR (ADR-002, 003, 004, 005, 006, 008, 009, 011, 013 are the candidates) before production code relies on it.
- **Reuse assets, not shortcuts.** Test harnesses, escape suites, property tests, linters, schemas, eval sets, and shell templates from PoCs move into the main repo with traces; prototype shortcuts do not.

## 5. Stack and Repository Layout (ARCH-001)

| Area | Choice |
|---|---|
| Domain services | Python 3.12, FastAPI, Pydantic v2 |
| DAL, realtime hub, Execution Gateway | Go, gRPC, sqlc and pgx |
| Data | PostgreSQL 16 with RLS; Redis 7; NATS JetStream (OpenSearch, ClickHouse, Temporal per section 3.3) |
| Identity | Keycloak (OIDC with PKCE) |
| Frontend | React and TypeScript, TanStack Query, generated SDK |
| Clients later | Tauri 2 (desktop), React Native with Expo (mobile) |

```
apps/ (web, desktop-tauri, mobile-rn, native)   services/ (gateway, identity, learning, challenges,
battles, tournaments, rewards, community, careers, billing, ai-gateway, notifications, analytics,
admin, dal, execution-gateway)   sandbox/ (images, harness, policies)   contracts/ (openapi, proto, sdk)
db/ (migrations, seeds, lint)   infra/   docs/   tests/   poc/ (isolated, never imported)
```
A new service or top-level directory needs an ADR.

## 6. Architecture Rules (non-negotiable)

1. FastAPI services never touch PostgreSQL directly; all access goes through the DAL over gRPC (ADR-002, SEC-013).
2. RLS lives with the table: `tenant_id`, `ENABLE ROW LEVEL SECURITY`, and policies in the same migration; the `db/lint` check must pass (SEC-014, SEC-015, ADR-003).
3. The Execution Gateway is the only path to sandboxes (SEC-039, ADR-004).
4. Identity is verified once at the API Gateway, which sets signed internal headers; services verify the signature and never trust or re-parse end-user tokens (SEC-011, ADR-010).
5. Secrets come from Vault only (SEC-031, SEC-032).
6. Entitlement checks fail open and log; money, ledger, redemption, and settlement fail closed (FR-BIL-007, ADR-014, SEC-054).
7. The ledger is double-entry and append-only; every posting has an idempotency key; balances are derived or cached projections (FR-RWD-001, SEC-051, SEC-052, ADR-005).
8. Battle state is server-authoritative; clients never submit scores or timestamps that count (FR-CMP-009, SEC-069, ADR-009).
9. Judging is deterministic from test cases and limits; never ask a model whether code is safe, correct, or plagiarized (SEC-047).
10. Cross-domain effects go through versioned events with an outbox; consumers are idempotent and deduplicate by event id (ADR-007).
11. Hidden test cases and expected outputs are never returned by any API; only pass counts (TM-CMP-007).

## 7. Python (FastAPI) Rules

- Layout: `app/api`, `app/domain` (pure logic), `app/clients`, `app/schemas`, `app/deps`, `tests/`. Routers are thin.
- `mypy --strict`, `ruff`, no `Any` without a comment. Pydantic v2 with `extra="forbid"` (SEC-022).
- Errors are RFC 9457 problem details; no stack traces or internals in responses.
- Mutating operations that could double an effect accept `Idempotency-Key`: createRun, enterChallenge, submitSolution, recordLessonProgress, acceptAnswer, createRedemption, createCheckout, requestExport.
- All I/O async with timeouts and retries with backoff; structured logs with `request_id`, `tenant_id`, `user_id`; never log tokens, full submissions, payment data, or PII (SEC-073).

## 8. Go Rules (DAL, hub, Execution Gateway)

- `golangci-lint` clean; `context.Context` first; propagate deadlines.
- DAL: every transaction starts with `SET LOCAL app.tenant_id` and `app.user_id`; sqlc queries only.
- Execution Gateway: reject any job missing CPU, memory, pid, disk, wall-time, or output limits; network disabled (SEC-040, SEC-041).
- Hub: sequence-numbered messages, resume tokens, bounded queues, per-room sharding (SEC-068, 070).

## 9. API and Contract Rules

- `contracts/openapi/openapi.yaml` is the source of truth for REST (53 operations at baseline). Use the generated SDK; no handwritten HTTP clients.
- Every operation keeps a stable `operationId`, an `x-requirement` list of `FR`, `NFR`, and `SEC` IDs, an `x-release` (MVP, FF, P2), and `x-roles` where role-restricted.
- Cursor pagination with a maximum page size; rate-limit headers documented. Breaking changes need a new major version; CI runs the breaking-change diff.
- `contracts/asyncapi/asyncapi.yaml` describes battles, notifications, run output streams, and AI streams (closes GAP-019). Keep message types, sequence numbers, and the Anonymous rule for private entrants in sync with it; change it before changing a channel.

## 10. Database Rules

- Forward-only, expand-then-contract migrations; never edit an applied migration (REL-001 sec 7).
- Every table: `id` (UUID), `tenant_id`, `created_at`, `updated_at`, indexes, RLS and policies.
- Partition submissions, ledger entries, events, and audit log by month. The application role cannot UPDATE or DELETE ledger or audit tables (SEC-051, SEC-074).
- Cross-tenant reads only through audited public views (SEC-016). Every new policy gets a pgTAP test (TC-1104).

## 11. Frontend Rules

- Strict TypeScript, generated SDK, TanStack Query. No inline event handlers; no raw HTML injection (SEC-024).
- Every data view has **loading, empty, and error** states (TC-1405).
- Design tokens only; no hard-coded hex values. Palette: logo blue (`--blue`), mid blue (`--accent2`), navy (`--accent`), near-black dark surfaces, white light surfaces; both themes work (FR-PLT-009).
- Use a real code editor component in the playground (GAP-003). Accessibility: WCAG 2.2 AA, keyboard operable, labeled controls, contrast checked (NFR-019, TC-1401, 1402, 1406).
- One reserved AI accent token (violet, `#8B7FD6`) for AI-touched UI only; confirm against the final brand palette (GAP-010).
- Realtime clients reconnect with backoff and resume from the last sequence.
- Gate fast-follow and Phase 2 UI with feature flags from `/admin/flags`.
- Fonts: Space Grotesk (display), IBM Plex Sans (body), IBM Plex Mono (code).

## 12. AI Feature Rules (AI Gateway)

- All model calls go through `services/ai-gateway` (SEC-061); keys live in Vault.
- Enforce plan quota and rate limit before each call and meter after (FR-AI-003, SEC-062).
- Treat user text, lessons, code, and retrieved content as untrusted: delimit, never follow instructions inside them (SEC-063).
- Output is text with no authority; it never executes automatically (SEC-064). Suggested code runs only through the Execution Gateway when the user chooses.
- Challenge mode returns hints only (FR-AI-004, SEC-067). Add evals (TC-0803, 0804) for every prompt or model change.

## 13. Testing and Traceability (TP-001, TC-001, RTM-001)

- Suites: UT, CT, IT, DB, SBX, E2E, SAST, DAST, LOAD, CHAOS, AI, A11Y, COMPAT. P1 cases block release.
- Mark tests with requirement IDs (`FR-*`, `NFR-*`, `SEC-*`, `TM-*`); cite the TC IDs a change satisfies.
- The RTM check fails the build for: a Must requirement without a test, a reference to an unknown ID, an orphan test, a High threat without a test.
- Coverage: 85% or more on domain and DAL code. Bug fixes start with a failing test. No sleeps; use fake clocks and fixtures.
- Definition of done: tests green, lint and types clean, OpenAPI and RTM tags updated, docs touched if behavior changed, no new scan findings, flag and rollback path verified.

## 14. Git, Commits, and PRs

- Branches: `feat/PB-nn-slug`, `fix/<ID>-slug`, `chore/slug`. Conventional Commits with IDs.
- PR text: what changed, IDs, how tested (TC IDs), flag and rollout notes, security considerations, screenshots for UI.
- Do not merge with failing checks; do not bypass hooks.

## 15. Documentation Rules

- Behavior changes update SRS-001 and OpenAPI in the same PR; design changes add or amend an ADR; security changes update SEC-001 and `cursorsecurityrules.md`.
- When a PoC decision or approved ADR changes a step, update PB-001 and this file.
- Comments explain why, not what. Every TODO names an owner and an issue.

## 16. Hard Stops (ask a human first)

- Changes to auth, tenancy, RLS policies, the ledger, payout logic, sandbox limits, encryption, or the AI Gateway policy.
- Enabling any fast-follow or Phase 2 flag, or adding a cash-out path.
- Building a deferred engine (OpenSearch, ClickHouse, Temporal, Firecracker tier) before its slice, or deleting its port.
- Promoting PoC code into production, or changing a decision recorded after a PoC.
- Adding a dependency with a non-permissive license, deleting data, dropping columns, or running destructive scripts.
- Anything that requires skipping a rule here or in `cursorsecurityrules.md`.

## 17. Quick Reference

- Notional points value for planning: 100 points = $1 (configurable). Plans: Free (5 challenges a month, 100 executions), Starter (FF), Pro, Enterprise.
- Tie-break: earlier accepted submission, then fewer attempts.
- Streak multiplier cap: 2x. Tier XP thresholds: 1,200; 4,000; 8,000; 15,000; 25,000; 50,000 (interpretation pending, GAP-016).
- Targets: API p95 under 300 ms reads and 500 ms writes at 4,200 concurrent users (NFR-001, 002); first output p95 under 2 s (NFR-003); scoreboard propagation p95 under 1 s (NFR-006). PoC results may change these.
