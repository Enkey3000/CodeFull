# CodeFull Project Documentation Plan

The document pipeline from PRD to execution guide: what each document is for, what feeds it, what it contains, and the gate it must pass.

## 1. How the Pipeline Works

```
PRD -> SRS -> Architecture -> Security Measures -> OpenAPI
                  |                  |                |
                  v                  v                v
              Test Plan  <-----  Threat Model ----> Test Cases
                  |                                   |
                  v                                   v
   UAT Plan -> Release/Deployment Plan -> RTM <-- (traces everything)
                  |
   Incident Response Plan -> Pen Testing Plan
                  |
   PoC -> MVP Pattern -> Playbook -> Gap Analysis -> Execution Guide
```

**Rules that keep the set coherent**

1. One source of truth per fact. The PRD owns what and why, the SRS owns required behavior, the Architecture owns how, Security Measures own controls, OpenAPI owns the contract. Other documents link instead of restating.
2. Every requirement has an ID (see section 2). Tests, threats, APIs, and releases cite those IDs, and the RTM is generated from them.
3. Docs-as-code: Markdown in /docs, reviewed by pull request, versioned with the code, with front matter (id, owner, status, version, last-reviewed).
4. Each document has a gate. Nothing downstream starts a final draft until its upstream gate has passed, but drafts overlap (see section 5).
5. Run order differs from reading order. PoCs start as soon as the Architecture draft exists, because their results change the Architecture, the MVP scope, and the Threat Model. Gap Analysis runs at three checkpoints, not once at the end.
6. Changes flow downward. A PRD change triggers an impact check on SRS, OpenAPI, tests, and RTM in the same pull request.

## 2. Traceability ID Scheme

| Prefix | Meaning | Defined in | Referenced by |
| --- | --- | --- | --- |
| BG- | Business goal / KPI | PRD | SRS, RTM |
| PER- | Persona | PRD | SRS, UAT |
| FR-\<DOMAIN>-nnn | Functional requirement | SRS | OpenAPI, tests, RTM |
| NFR-nnn | Non-functional requirement | SRS | Architecture, perf tests |
| SEC-nnn | Security control requirement | Security Measures | Threat Model, tests, pen test |
| ADR-nnn | Architecture decision | Architecture | SRS, playbook |
| API-\<operationId> | API operation | OpenAPI | tests, RTM |
| TM-\<AREA>-nnn | Threat | Threat Model | SEC, tests |
| TC-nnn | Test case | Test Cases | RTM |
| UAT-nnn | Acceptance scenario | UAT Plan | RTM |
| POC-n / GAP-nnn / INC-n | Proof of concept, gap, incident playbook | respective docs | RTM, execution guide |

Example chain: BG-02 (retain learners) -> FR-LRN-014 (streak tracking) -> API-recordLessonProgress -> TM-LRN-003 (streak farming) -> SEC-021 (server-side event validation) -> TC-0412 -> UAT-009.

Domain codes: IDN, LRN, EXE, CMP, RWD, COM, CAR, AI, BIL, PLT.

## 3. Pipeline at a Glance

| # | Document | Answers | Depends on | Owner | Gate |
| --- | --- | --- | --- | --- | --- |
| 1 | PRD | What and why | Prototype, market, brand | Product | Stakeholder sign-off |
| 2 | SRS | What the system must do | PRD | Product + Tech lead | Every FR testable |
| 3 | Architecture | How it is built | SRS | Architect | Architecture review + ADRs |
| 4 | Security Measures | Which controls protect it | SRS, Architecture | Security lead | Control owners assigned |
| 5 | OpenAPI | The contract | SRS, Architecture | Backend lead | Lint + SDK generation pass |
| 6 | Test Plan | How quality is proven | SRS, Architecture | QA lead | Strategy approved |
| 7 | Threat Model | How it can be attacked | Architecture, Security | Security lead | High threats mitigated |
| 8 | Test Cases | Exact checks | SRS, OpenAPI, Threat Model | QA | Every FR and SEC covered |
| 9 | UAT Plan | Does it satisfy users | PRD, SRS | Product + QA | Scenarios approved |
| 10 | Release / Deployment Plan | How it ships | Architecture, Test Plan | DevOps | Go/no-go checklist |
| 11 | RTM | Is everything covered | All above | QA + PM | 100% of Must items traced |
| 12 | Incident Response Plan | What we do when it breaks | Architecture, Security | Security + SRE | Tabletop drill passed |
| 13 | Pen Testing Plan | How it is independently attacked | Threat Model | Security lead | Scope and RoE signed |
| 14 | PoC | Can the risky parts work | Architecture draft | Tech lead | Go / pivot / stop per PoC |
| 15 | MVP Pattern | What ships first and how it is built | PRD, PoC results | Product + Architect | Scope frozen |
| 16 | Playbook | Sequenced build steps | All specs | Tech lead | Steps verified end to end |
| 17 | Gap Analysis | What is missing vs target | RTM, prototype, PoC | PM + Architect | Backlog prioritized |
| 18 | Execution Guide | How the team runs it | Everything | Delivery lead | Team onboarded |

## 4. Document-by-Document Plan

### 4.1 PRD (Product Requirements Document)

- **Purpose:** define the product, users, and success criteria.
- **Contents:** vision; personas (learner, competitor, mentor, recruiter, org admin, moderator); problem statements; goals and KPIs (activation, weekly active coders, challenge participation, paid conversion, mentor bookings); feature epics per domain; user journeys; plans and monetization (Free, Starter, Pro, Enterprise); rewards policy (points now, real-money Phase 2); non-goals; assumptions; risks; release criteria.
- **CodeFull specifics:** six-tier progression (Beginner to Guru), four lesson formats, anonymous and public leaderboard entry, open and discreet Q&A, prize pools with caps, recruiter marketplace.
- **Gate:** every feature has a BG ID and MoSCoW priority; legal flags raised for real-money rewards.

### 4.2 SRS (Software Requirements Specification)

- **Purpose:** testable statement of system behavior.
- **Contents:** FRs per domain with Given/When/Then acceptance criteria; NFRs (4,200 concurrent coders, p95 latency targets, 99.9% API availability, RPO 5 min, RTO 1 hr); data requirements; interface requirements (web, desktop, mobile, push, store billing); state machines (battle lifecycle, redemption, prize settlement, tier progression); constraints; glossary.
- **Gate:** each FR traces to a BG; each has acceptance criteria; ambiguity log is empty.

### 4.3 Architecture

- **Purpose:** the technical blueprint. Seed it from the Backend Plan document.
- **Contents:** C4 context, container, and component views; service catalog; data model and RLS strategy; event and workflow catalog; deployment topology; capacity model; DR; ADRs (stack, DAL, sandbox tiers, ledger design, realtime hub, AI gateway); NFR coverage matrix.
- **Gate:** every NFR maps to a design element; every significant decision has an ADR.

### 4.4 Security Measures

- **Purpose:** the control catalog.
- **Contents:** identity and access model; data classification; encryption and key management; tenant isolation; sandbox policy; ledger and payments integrity; AI safety (prompt injection, quotas, no LLM judging code safety); privacy and compliance (GDPR, CCPA, PCI scope through Stripe); logging and monitoring; secure SDLC; supply chain.
- **Gate:** each SEC item has an owner, an implementation location, and a verification method.

### 4.5 OpenAPI

- **Purpose:** the contract that generates every SDK.
- **Contents:** one spec per public service; shared schemas; error model (RFC 9457 problem details); pagination; idempotency keys; rate-limit headers; auth schemes (OIDC bearer); AsyncAPI for WebSocket and SSE channels (battles, notifications, run streams); examples; versioning and deprecation policy.
- **Gate:** Spectral lint clean, breaking-change check wired into CI, SDKs for TypeScript, Kotlin, Swift, C#, and Rust generate and compile.

### 4.6 Test Plan

- **Purpose:** strategy and logistics for proving quality.
- **Contents:** test levels, environments, test data and anonymization, tools, entry and exit criteria, defect severity and SLAs, coverage targets, performance and chaos approach, device matrix, schedule, roles. Use the Backend Plan testing checklist as the base.
- **Gate:** exit criteria agreed with Product and Security.

### 4.7 Threat Model

- **Purpose:** find and rank attacks before building controls.
- **Contents:** data-flow diagrams with trust boundaries (client, gateway, services, DAL, sandbox, third parties); STRIDE per element; abuse cases (cheating and collusion, point farming, sandbox escape, prompt injection, recruiter scraping, account takeover, prize pool manipulation, tenant hopping); risk scoring; mitigation links to SEC IDs; residual risk register.
- **Gate:** no unmitigated high risks without a signed acceptance.

### 4.8 Test Cases

- **Purpose:** executable checks.
- **Contents:** per case: ID, linked FR/SEC/TM, preconditions, steps, expected result, data, automation status, priority. Suites: functional by domain, negative and boundary, authorization matrix, RLS, ledger invariants, sandbox escape, realtime, AI quota and injection, accessibility, compatibility, performance.
- **Gate:** every Must FR and every SEC has at least one case; critical paths automated.

### 4.9 UAT Plan

- **Purpose:** real users confirm the product does the job.
- **Contents:** participants per persona; scenarios derived from PRD journeys (first lesson, first challenge win, battle, redeem points, upgrade, recruiter contact); environment and data; entry criteria; feedback capture; defect triage; sign-off authority.
- **Gate:** at least 95% of scenarios pass, no open Sev 1 or Sev 2, sign-off recorded.

### 4.10 Release / Deployment Plan

- **Purpose:** ship safely and reversibly.
- **Contents:** environments and promotion path; CI/CD pipeline; versioning; database migration strategy (expand then contract); canary and blue-green rules; feature flags (including the real-money flag); rollback; go/no-go checklist; communication plan; post-release verification; desktop update feeds; App Store and Google Play submission steps.
- **Gate:** rollback rehearsed in staging.

### 4.11 RTM (Requirements Traceability Matrix)

- **Purpose:** prove nothing is untested, unbuilt, or orphaned.
- **Contents:** BG -> FR/NFR/SEC -> ADR/API -> TM -> TC -> UAT -> release. Generated by a script that reads IDs from docs, OpenAPI x-requirement tags, and test annotations.
- **Gate:** 100% of Must requirements traced; no orphan tests; report published each sprint.

### 4.12 Incident Response Plan

- **Purpose:** act fast and consistently when something goes wrong.
- **Contents:** severity levels; roles (incident commander, comms, scribe); on-call; detection sources; playbooks (INC-1 sandbox escape, INC-2 ledger mismatch or double payout, INC-3 credential or key leak, INC-4 data breach, INC-5 DDoS, INC-6 AI misuse or prompt-injection campaign, INC-7 payment provider outage, INC-8 battle clock or scoreboard failure); communications templates; regulatory notification timelines (GDPR 72 hours); post-incident review template.
- **Gate:** tabletop drill completed for INC-1, INC-2, and INC-4.

### 4.13 Penetration Testing Plan

- **Purpose:** independent verification of the controls.
- **Contents:** scope (web, API, gateway, tenant isolation, sandbox, desktop and mobile clients, AI gateway, payments flow); rules of engagement; methods (OWASP ASVS, WSTG, MASVS); schedule (pre-beta, pre-GA, annually, after major changes); sandbox escape red-team track; reporting format; remediation SLAs (critical 7 days, high 14, medium 30); retest process.
- **Gate:** scope and RoE signed by the vendor and Security.

### 4.14 PoC (Proof of Concept)

- **Purpose:** retire the riskiest assumptions in 2 to 3 weeks.
- **Candidates and success criteria:**
  - POC-1 Sandbox: gVisor and Firecracker tiers run Python and JavaScript; 500 runs per second with warm pools; escape suite fails to break out.
  - POC-2 Realtime battle: 100 entrants and 1,000 spectators, server-authoritative clock drift under 250 ms.
  - POC-3 Ledger and settlement: Temporal workflow survives crashes with zero double-posts.
  - POC-4 Tenant isolation: RLS through the DAL blocks cross-tenant reads in the pgTAP suite.
  - POC-5 AI gateway: streaming tutor with quotas and injection defenses.
  - POC-6 Client shells: Tauri and React Native with OIDC PKCE, keychain storage, and push.
- **Gate:** each PoC ends with go, pivot, or stop, and results update the ADRs.

### 4.15 MVP Pattern

- **Purpose:** define the first shippable slice and the pattern for building it.
- **Pattern:** walking skeleton first (auth, one page, one API, one deploy), then vertical slices that each cross UI, API, DAL, and tests, behind feature flags, released to rings (team, beta, public).
- **Proposed MVP slice:** identity and onboarding; one learning track (Python, Beginner to Intermediate); playground and solo challenges in two languages; global leaderboard with anonymous option; basic AI tutor; points earning (no cash redemption); Free and Pro billing.
- **Fast follow:** live battles, tournaments, prize pools, mentors, jobs, Enterprise.
- **Gate:** scope frozen, success metrics defined (activation, day-7 retention, challenge completion rate, paid conversion).

### 4.16 Playbook

- **Purpose:** the sequential build script a developer or AI coding assistant follows.
- **Format per step:** goal, input documents and IDs, prompt or task text, expected output, verification command, linked FR/SEC/TC IDs.
- **Structure:** phases mirror the Backend Plan (foundations, identity and shell, learning, execution and challenges, competition, rewards and billing, community and AI, enterprise and analytics, hardening). Target 60 or more steps, each small enough to review in one pull request.
- **Gate:** steps 1 to 10 executed from scratch on a clean machine.

### 4.17 Gap Analysis

- **Purpose:** measure the distance between current state and target.
- **Method:** compare prototype and current docs against PRD, SRS, and RTM across functional, non-functional, security, data, operations, and UX dimensions; score each gap by impact and effort.
- **Starter gaps already visible:** prototype has no authentication or persistence; all data is hard-coded; no loading, empty, or error states; accessibility not audited; static dates and copy from 2025; execution output is simulated; no server-side privacy enforcement.
- **Checkpoints:** after SRS, after PoCs, before beta. Each produces a prioritized remediation backlog (GAP-nnn).

### 4.18 Execution Guide

- **Purpose:** how the team actually runs the work.
- **Contents:** roles and RACI; sprint cadence; definition of ready and done; branching and PR rules; how docs are updated with code; environment bootstrap; how to run the playbook; gate calendar; metrics dashboard (velocity, RTM coverage, defect escape rate, DORA); escalation paths; onboarding checklist.
- **Gate:** a new engineer reaches a green local build and a merged first PR within two days.

## 5. Sequencing

| Weeks | Work | Notes |
| --- | --- | --- |
| 1-2 | PRD | Freeze Must scope |
| 2-4 | SRS | Start Test Plan outline |
| 3-5 | Architecture, Security Measures | Seed from the Backend Plan |
| 4-6 | OpenAPI v0, Threat Model | Generate first SDK |
| 5-8 | PoC 1 to 6 | Gap Analysis checkpoint 1 at week 5 |
| 6-9 | Test Plan, Test Cases | Continues through the build |
| 8-9 | MVP Pattern, Playbook | After PoC go/no-go |
| 9 | Execution Guide, cursor rule files | Team starts building |
| 10 onward | RTM (continuous), build | Gap Analysis checkpoint 2 |
| Before beta | UAT Plan, Incident Response Plan, Pen Testing Plan, Release Plan | Checkpoint 3, tabletop drills |

## 6. How the Documents Drive the Cursor Rule Files

- **PRD** supplies product guardrails: scope tiers, non-goals, feature flags, and the rule that Phase 2 real-money features stay disabled.
- **SRS** supplies behavioral contracts: acceptance criteria, NFR budgets, state machines, and the requirement-ID tagging convention for code, tests, and commits.
- **Architecture** supplies structure and layering: monorepo layout, service boundaries, DAL-only database access, Execution Gateway as the sole sandbox path, contract-first APIs.
- **Security Measures** supply the security rules: authentication, tenant isolation, secrets, input validation, sandbox policy, ledger integrity, AI safety, and forbidden patterns.

Two files are built from these: cursorrules.md (engineering conduct and conventions) and cursorsecurityrules.md (security requirements and review checklist). Regenerate or review both whenever the PRD, SRS, Architecture, or Security Measures change.
