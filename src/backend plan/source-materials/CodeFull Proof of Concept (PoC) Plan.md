# CodeFull Proof of Concept (PoC) Plan

**Doc ID:** POC-001 | **Version:** 0.1 draft | **Status:** for architecture review | **Owner:** Tech lead **Upstream:** ARCH-001, SEC-001, TM-001, SRS-001 (NFRs) | **Downstream:** ARCH-001 updates (ADRs), MVP Pattern, Playbook, Gap Analysis

## 1. Purpose and Principles

The PoCs retire the riskiest assumptions in the architecture before the team commits to the build. Each PoC answers a specific question with measured evidence and ends with a decision: **Go**, **Pivot**, or **Stop**.

1. **Question first:** every PoC states a hypothesis and numeric success criteria before any code is written.
2. **Timeboxed:** 2 to 3 weeks each, run in parallel by small teams; no scope growth.
3. **Throwaway code, kept learnings:** prototypes are not production code; results, configs, scripts, and measurements are kept.
4. **Measure, do not guess:** capacity, latency, and cost numbers come from the PoC and replace assumptions in ARCH-001 and SRS-001.
5. **Security counts:** PoCs that touch untrusted code, tenancy, or money include abuse tests, not only happy paths.
6. **Kill criteria are agreed up front** so a failed PoC changes the plan instead of being rationalized.

## 2. PoC Portfolio

| ID | Question | Why it matters | Priority | Duration |
| --- | --- | --- | --- | --- |
| POC-1 | Can sandboxes run Python and JavaScript fast, safely, and cheaply at scale? | Core product, largest cost and risk (TM-SBX-001, NFR-003, NFR-013) | Highest | 3 weeks |
| POC-2 | Can the realtime hub keep fair clocks and scoreboards for 100 entrants and 1,000 spectators per battle? | Competition fairness and experience (NFR-006, NFR-012) | High | 2 weeks |
| POC-3 | Can the ledger and settlement workflows be exactly-once in practice under failure? | Money-like integrity (TM-RWD-001, 003, 008) | Highest | 2 weeks |
| POC-4 | Does RLS through the DAL isolate tenants with acceptable overhead? | Trust promise and performance (TM-TEN-001, NFR-001) | Highest | 2 weeks |
| POC-5 | Can the AI Gateway stream fast, enforce quotas, and resist injection at acceptable cost? | Cost and abuse exposure (TM-AI-\*, NFR-008) | Medium | 2 weeks |
| POC-6 | Do the cross-platform shells (Tauri and React Native) support the required auth, storage, push, and offline needs? | Platform reach (FR-LRN-012, SEC-005, SEC-093) | Medium | 3 weeks |

Order: start POC-1, POC-3, and POC-4 first (they gate the architecture); POC-2 and POC-5 start in the second week; POC-6 can begin once the web app skeleton exists.

## 3. PoC Definitions

### POC-1 Sandbox execution at scale

- **Hypothesis:** a gVisor-based standard tier and a Firecracker microVM hardened tier can meet latency and throughput targets within an acceptable cost per run, with no escapes in the escape suite.
- **Scope:** Execution Gateway skeleton in Go; warm pools for Python 3.12 and Node; harness with test-case judging; resource limits (SEC-040); no-network policy; sandbox node pool isolation; both tiers.
- **Method:** build, then run (a) latency tests for cold and warm starts, (b) sustained load of 500 runs per second for 10 minutes, (c) the escape suite from TC-1201 to TC-1210, (d) cross-user leakage tests, (e) cost measurement per 1,000 runs on target instance types.
- **Success criteria:** warm-pool time to first output p95 under 2 s (NFR-003); verdict for a 10-test challenge p95 under 10 s (NFR-004); 500 runs per second sustained (NFR-013); hardened tier start under 1.5 s with pooling; zero escapes or cross-user leakage; documented cost per 1,000 runs.
- **Kill or pivot:** if the hardened tier needs bare metal beyond budget or cannot meet start times, pivot to gVisor-only for MVP and defer the hardened tier (battles launch later); if gVisor overhead breaks latency targets, evaluate alternative isolation (for example Kata or a hybrid) before proceeding.
- **Outputs:** measured capacity and cost model, node pool sizing, sandbox policy baseline, updated ADR-004 and NFR-013 assumptions, test harness reused for the sandbox suite.

### POC-2 Realtime battle hub

- **Hypothesis:** a Go WebSocket hub with Redis sorted sets and pub/sub can sustain 100 entrants and 1,000 spectators per battle with accurate server clocks.
- **Scope:** hub, room sharding, sequence numbers and resume, server clock, scoreboard updates fed by simulated judged events, private-entry anonymization in payloads.
- **Method:** load generators simulate 10 battles then scale toward 50; inject disconnects, slow clients, and clock skew; measure propagation latency, memory, CPU, Redis load; run anonymity payload scans.
- **Success criteria:** scoreboard propagation p95 under 1 s and clock drift under 250 ms (NFR-006); resume with no missed or duplicate events after disconnect; 50 concurrent battles within the planned node count (NFR-012); no identity field for private entrants in any payload (TC-0404).
- **Kill or pivot:** if Redis pub/sub fan-out limits spectators, move to sharded fan-out services or a managed realtime option; if drift cannot meet the target, redesign time sync in the client protocol.
- **Outputs:** protocol spec (AsyncAPI), capacity per node, updated ADR-008 and ADR-009.

### POC-3 Ledger and settlement workflows

- **Hypothesis:** a Postgres append-only double-entry ledger with idempotency keys and Temporal workflows produces exactly-once effects under crashes, retries, and concurrency.
- **Scope:** ledger schema and roles without UPDATE or DELETE (SEC-051), posting API through the DAL, prize settlement and redemption workflows, reconciliation job.
- **Method:** property-based tests over random operation sequences (millions of operations); 50 parallel identical requests with one idempotency key; kill workers and databases mid-workflow; inject duplicate and out-of-order events; run reconciliation against injected mismatches.
- **Success criteria:** invariants hold (debits equal credits, no negative balances); one posting per idempotency key; zero double payouts across crash tests; reconciliation detects 100% of injected mismatches; sustained posting rate meets planned load with p95 under 100 ms.
- **Kill or pivot:** if Temporal operational overhead is too high for the team, fall back to a Postgres-based workflow library with an outbox for MVP; if throughput is short, partition ledger tables and batch projections.
- **Outputs:** ledger schema and migration templates, workflow patterns, updated ADR-005 and ADR-006, test suites reused as TC-0501 to TC-0511.

### POC-4 Tenant isolation through the DAL

- **Hypothesis:** RLS policies with per-transaction context set by a Go DAL isolate tenants and privacy flags with under 10% overhead.
- **Scope:** DAL with gRPC and sqlc; 30 representative tables with RLS in the same migration; CI linter; audited public views for the global leaderboard and portfolio; pgTAP suites.
- **Method:** benchmark read and write paths with and without RLS and SET LOCAL at 4,200 concurrent connections using PgBouncer in transaction mode; attempt cross-tenant access with all verbs; test leaderboard views for anonymity; test migration linter on bad migrations.
- **Success criteria:** zero cross-tenant reads or writes; linter blocks every table lacking RLS; overhead under 10% at baseline load; API read p95 meets NFR-001 for tested queries.
- **Kill or pivot:** if overhead or pooling constraints break targets, consider schema-per-tenant for Enterprise orgs while keeping RLS for the public tenant, or move hot read paths to read models.
- **Outputs:** DAL conventions, migration templates, linter, updated ADR-002 and ADR-003.

### POC-5 AI Gateway

- **Hypothesis:** a gateway can stream tutor responses with under 2 s first token, enforce exact quotas, redact secrets, and hold up against prompt injection at an acceptable cost per active learner.
- **Scope:** FastAPI gateway, SSE streaming, quota and metering, redaction, delimiting of untrusted content, challenge-mode policy, logging with retention, evaluation harness with injection and solution-leak prompts.
- **Method:** run 500 concurrent streams; compare metered tokens to provider reports; run the injection set (TC-0804) and challenge-mode set (TC-0803); estimate monthly cost per active learner from realistic usage.
- **Success criteria:** first token p95 under 2 s (NFR-008); metering equals provider totals; zero instruction-following from untrusted content in the fixed set above the agreed pass threshold; cost per active learner within the unit economics from the PRD plans.
- **Kill or pivot:** if cost exceeds plan margins, tighten quotas, add caching and smaller models for easy turns, or shift limits between plans.
- **Outputs:** prompt and policy templates, eval harness, cost model, updated ADR-011.

### POC-6 Client shells

- **Hypothesis:** Tauri (desktop) and React Native (mobile) can deliver secure sign-in, secure storage, push, deep links, offline cache with sync, and signed updates with the same TypeScript SDK.
- **Scope:** minimal shells for Windows, macOS, Linux, Android, and iOS consuming the generated SDK; OIDC with PKCE via the system browser; keychain and Keystore storage; push registration; offline lesson cache and a sync queue with idempotency keys; update channel (desktop); attestation call (mobile).
- **Method:** scripted scenarios on real devices and CI runners; startup time and bundle size measurements; basic security checks (IPC allowlist, webview restrictions, no tokens in plain storage).
- **Success criteria:** sign-in and token refresh work on all five platforms; tokens only in secure storage (SEC-005); offline progress merges without loss; signed update applies and an unsigned one is refused (SEC-093); cold start under 3 s on a mid-range device.
- **Kill or pivot:** if a platform fails a security or capability requirement, move that platform to a native shell earlier or ship web-only there first.
- **Outputs:** shell templates, auth and sync libraries, platform risk list, updated ADR-013.

## 4. Environments, Team, and Dependencies

| Item | Plan |
| --- | --- |
| Environment | Isolated PoC cloud account or project with budget alarms; separate network from staging |
| Team | One lead per PoC with 1 to 2 engineers; security engineer part-time on POC-1, 3, 4; QA support for test design |
| Tooling | k6, Testcontainers, pgTAP, property-based testing libraries, Toxiproxy, device cloud for POC-6 |
| Dependencies | Cloud provider decision (nested virtualization or bare metal for POC-1), Keycloak instance, provider test keys (Stripe, AI), Temporal and Redis clusters |
| Budget | Cap per PoC, tracked weekly; cost data is itself a PoC result |

## 5. Decision Framework

Each PoC ends with a one-page report and a review with the architect, security lead, and product owner.

| Decision | When | Consequence |
| --- | --- | --- |
| Go | All success criteria met, no unresolved high risk | Proceed as in ARCH-001; adopt patterns into the Playbook |
| Pivot | Some criteria missed but a defined alternative meets them | Update ARCH-001, SRS-001 targets, and MVP Pattern scope; schedule a short follow-up PoC if needed |
| Stop | Core hypothesis false and no acceptable alternative | Escalate to leadership; change scope, timeline, or approach |

### Report template

Question and hypothesis; what was built; measurements versus criteria (table); security findings; cost and operational observations; decision and rationale; ADR, NFR, and capacity changes required; follow-ups.

## 6. Schedule

| Week | Activity |
| --- | --- |
| 5 | Kickoff, environments, POC-1, POC-3, POC-4 start |
| 6 | POC-2 and POC-5 start; first measurements |
| 7 | POC-1 load and escape testing; POC-3 chaos testing; POC-4 benchmarks |
| 8 | POC-6 shells in progress; reports for POC-3 and POC-4 |
| 9 | Reports for POC-1, POC-2, POC-5; decision review; Gap Analysis checkpoint 2 |
| 10 | POC-6 report; ARCH-001, SRS-001, MVP Pattern, and Playbook updated with results |

## 7. Effect on Other Documents

| Document | Likely changes |
| --- | --- |
| ARCH-001 | ADR confirmations or amendments (ADR-002, 003, 004, 005, 006, 008, 009, 011, 013); capacity table; deployment topology for sandbox pools |
| SRS-001 | NFR targets adjusted to measured reality (NFR-003, 004, 006, 013) |
| SEC-001 and TM-001 | New or changed controls and re-scored threats from PoC findings |
| MVP Pattern | Scope cuts or deferrals (for example hardened tier and battles) |
| Test Cases and RTM | Reuse PoC suites as the first automated cases; update traces |
| Playbook | Proven setup steps and templates become the first build steps |

## 8. Risks

| Risk | Mitigation |
| --- | --- |
| PoC scope creep into a half-built product | Timebox and success criteria fixed in advance; weekly review |
| Results do not transfer to production-scale environments | Use production-like instance types and data shapes; record limitations |
| Security shortcuts in prototype code leak into the product | Label prototype code, restrict to the PoC account, rewrite for production |
| Team capacity conflicts with documentation work | Dedicated PoC leads and a published schedule |
| Cost overruns from load tests | Budget alarms, scheduled test windows, automatic teardown |

## 9. Exit Criteria for the PoC Phase

- A decision is recorded for each PoC (Go, Pivot, or Stop) and approved by the architect, security lead, and product owner.
- ARCH-001, SRS-001, SEC-001, TM-001, and the MVP Pattern reflect the measured results.
- Reusable assets are in the repository: harnesses, schemas, workflows, linters, shell templates, and eval sets.
- Open risks from PoCs are in the risk register with owners.
