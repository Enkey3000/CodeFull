# CodeFull MVP Pattern

**Doc ID:** MVP-001 | **Version:** 0.1 draft | **Status:** for product and engineering approval | **Owner:** Product owner + Architect **Upstream:** PRD-001, SRS-001, ARCH-001, POC-001 | **Downstream:** Playbook, Execution Guide, Release Plan, Gap Analysis

## 1. MVP Hypothesis and Goals

**Hypothesis:** learners who can learn Python step by step, run code instantly, compete in solo challenges with privacy control, and earn visible points will activate, return weekly, and a meaningful share will pay for Pro.

| Goal | Measure | Target (from PRD-001) |
| --- | --- | --- |
| BG-01 Activation | Signups who run code within 24 hours | 60% |
| BG-02 Retention | Day-7 and Day-30 retention | 35% and 20% |
| BG-03 Competition | Monthly actives entering a challenge | 30% |
| BG-04 Monetization | Free to paid conversion (6 months after GA) | 4% |
| BG-05 Community | Questions answered within 24 hours | 50% |
| BG-07 Trust | Fraudulent point awards; cross-tenant incidents | under 0.1%; zero |

**North-star metric (proposed):** weekly active coders who run code and complete a lesson or challenge.

## 2. MVP Scope

All items below are MVP-tier requirements in SRS-001. Fast-follow (battles, tournaments, prize pools, mentors, careers, desktop and mobile apps) and Phase 2 items are out of scope, except that their flags and extension points exist.

| Domain | MVP requirements |
| --- | --- |
| Identity | FR-IDN-001 to 007 |
| Learning | FR-LRN-001 to 010 |
| Execution | FR-EXE-001 to 007 (standard isolation tier) |
| Competition | FR-CMP-001, 002, 003, 005, 006, 014 (solo challenges, global and weekly rankings) |
| Rewards | FR-RWD-001, 002, 003, 008, 009 (earn and view points; no redemption) |
| Community | FR-COM-001, 002, 003, 004, 007, 008 |
| AI | FR-AI-001 to 006 |
| Billing | FR-BIL-001 to 005, 007 (Free and Pro; Starter is FF) |
| Platform | FR-PLT-001, 002, 004, 005, 006, 009 |

### Content scope (proposed, to confirm)

| Content | Target |
| --- | --- |
| Learning track | One deep Python track, Beginner to Intermediate, about 40 lessons |
| Lesson formats | Text and interactive for every lesson; video for about half; audio for about a third (FR-LRN-003 allows formats where authored) |
| Challenges | About 30 solo challenges in Python and JavaScript (10 beginner, 12 intermediate, 8 advanced), each with hidden tests |
| Achievements | About 12 badges |
| Languages in the playground | Python 3.12 and JavaScript |

## 3. The Pattern: Walking Skeleton, Then Vertical Slices

1. **Walking skeleton first (S0).** One screen, one API call, authenticated, through the gateway, DAL, database with RLS, deployed to staging by the pipeline with observability. It proves the architecture end to end before features pile on.
2. **Vertical slices.** Each slice delivers a user-visible capability through every layer: UI, API (OpenAPI first), service, DAL and migration with RLS, tests, docs, analytics events, and a feature flag.
3. **Release to rings continuously.** Every slice reaches ring 0 (internal) when done and ring 1 (beta cohort) after S10, using the rollout rings in REL-001.
4. **Contract-first and test-first for risky areas.** Ledger, privacy, sandbox, and authorization slices start from tests derived from TC-001 and TM-001.
5. **Instrument from day one.** Each slice ships its analytics events so KPIs are measurable at beta.
6. **Definition of done per slice:** requirements traced in the RTM; unit, contract, integration, and security cases passing; flag and rollback verified; accessibility checks on new screens; documentation and runbook updates; demo to Product.

## 4. Slice Plan

Weeks are indicative for a team of about 6 to 8 engineers plus design, QA, and content; they overlap and assume PoC results (POC-001) arrive by week 9 for the areas they affect.

| Slice | Name | Weeks | Requirements | Demo outcome |
| --- | --- | --- | --- | --- |
| S0 | Walking skeleton | 1-2 | Foundations: SEC-009, 011, 013, 014; NFR-022 | Signed-in stub page served through gateway and DAL, deployed by pipeline, traces visible |
| S1 | Identity and shell | 3-4 | FR-IDN-001 to 006, FR-PLT-006, FR-PLT-009 | Sign up, sign in with GitHub or Google, onboarding, profile, privacy settings, MFA, theme toggle, audit log |
| S2 | Learning core | 5-7 | FR-LRN-001 to 008 | Browse the Python track, finish a lesson in any format, resume, see XP, tier, streak, achievements, weekly goal |
| S3 | Playground and execution | 6-9 | FR-EXE-001 to 004, 007; FR-LRN-010 | Run Python and JavaScript with streamed output, limits explained, snippets saved and shared, run history |
| S4 | Challenges and judging | 8-11 | FR-CMP-001, 002, 003, 005; FR-EXE-005 | Browse, enter publicly or privately, submit, get a deterministic verdict |
| S5 | Points and leaderboards | 10-13 | FR-RWD-001, 002, 003, 008, 009; FR-CMP-006, 014 | Points post once per event, balance and history, global and weekly leaderboards with anonymity, reconciliation running |
| S6 | Billing and plans | 12-14 | FR-BIL-001 to 005, 007; FR-EXE-006 | Upgrade to Pro in test mode, usage meters, quotas enforced, fail-open entitlements |
| S7 | AI tutor | 13-16 | FR-AI-001 to 006; FR-LRN-009 | Tutor sessions with history, playground assistant, caps, hints-only in challenge mode, recommendations |
| S8 | Community | 14-17 | FR-COM-001 to 004, 007, 008 | Open and discreet questions, answers, votes, accepted answers, reputation, flagging |
| S9 | Platform and compliance | 15-18 | FR-PLT-001, 002, 004, 005; FR-IDN-007 | Notifications, search, admin moderation and flags, export and deletion workflows |
| S10 | Hardening and beta | 19-22 | Cross-cutting: NFRs, SEC verification, UAT | Load, escape, authorization, and privacy suites green; pen test PT-1 closed; UAT passed; beta launch |

After beta: GA gate per PRD-001 section 14, then fast-follow slices (battles, tournaments, pools, redemption, mentors, careers, Starter plan, desktop and mobile).

## 5. Proposed MVP Simplifications to ARCH-001

The full architecture is the destination; these deferrals shrink MVP operations without closing doors. They need an ADR (proposed ADR-015) and should be confirmed after POC-1 and POC-3.

| Full architecture | MVP approach | When to adopt the full version |
| --- | --- | --- |
| OpenSearch for search | Postgres full-text search behind the same search API | When search latency or relevance misses NFR-009, or at fast-follow scale |
| ClickHouse analytics | Postgres rollups and materialized views; product analytics from the event stream | When personal analytics (FR-PLT-003) and org analytics ship |
| Temporal workflows | Outbox pattern plus a durable job queue for earning postings and notifications | At fast-follow when settlement and redemption arrive (POC-3 outcome) |
| Firecracker hardened tier | gVisor standard tier only (competition-grade runs are not in MVP) | With live battles and tournaments (FR-EXE-008, SEC-044) |
| Desktop and mobile clients | Responsive web only | After MVP per Backend Plan sections 9 and 10 |

Non-negotiable in MVP, regardless of simplification: RLS and DAL access only, signed gateway headers, Vault secrets, append-only ledger with idempotency, server-side privacy enforcement, deterministic judging, no network in sandboxes, AI Gateway as the only model caller, audit logging, and the CI security gates.

## 6. Scope Management and Cut Lines

If the schedule slips, cut in this order, with Product approval, and record each cut in the RTM:

1. AI-generated recommendations become rule-based suggestions (FR-LRN-009, FR-AI-005).
2. Achievements and weekly goals (FR-LRN-007, 008) shrink to a minimum set.
3. Snippet sharing and run history polish (FR-EXE-004, 007).
4. Reputation scoring (FR-COM-004).
5. Weekly leaderboard scope beyond global (FR-CMP-014 detail).
6. JavaScript runtime moves to fast-follow, leaving Python only.

**Never cut:** tenant isolation, privacy enforcement, ledger integrity and reconciliation, sandbox isolation and limits, authorization, MFA for admins, security gates, the pen test, and UAT.

## 7. Instrumentation and KPI Plan

| Event group | Events (examples) | KPI served |
| --- | --- | --- |
| Acquisition and activation | signup\_completed, onboarding\_completed, first\_run, first\_lesson\_completed | BG-01 |
| Engagement and retention | lesson\_completed, streak\_incremented, session\_started, weekly\_goal\_met | BG-02 |
| Competition | challenge\_viewed, challenge\_entered, submission\_judged, leaderboard\_viewed | BG-03 |
| Monetization | checkout\_started, checkout\_completed, quota\_reached, upgrade\_prompt\_shown | BG-04 |
| Community | question\_posted, answer\_posted, answer\_accepted, time\_to\_first\_answer | BG-05 |
| Trust and quality | privacy\_setting\_changed, reconciliation\_exception, flag\_created, sandbox\_policy\_violation | BG-07 |
| AI | tutor\_session\_started, tokens\_used, hint\_requested, report\_submitted | BG-02, cost control |

Dashboards are ready before beta: activation funnel, weekly cohorts, challenge funnel, conversion, and system health. Event schemas follow the privacy rules (no code content or PII in analytics events).

## 8. Team and Working Agreements

| Area | Agreement |
| --- | --- |
| Cadence | Two-week sprints; each slice is one to three sprints; weekly demo to Product |
| Branching | Trunk-based with short-lived branches; flags for unfinished work |
| Quality | PR checks per TP-001; slice done only when its test cases and RTM links pass |
| Content | Content team works one slice ahead; lessons and challenges reviewed for correctness before release |
| Security | Security review at the start of S4, S5, S6, S7 and before beta; threat model updates in the same PRs |
| Design | Design tokens and components from the logo-derived design system; every screen has loading, empty, and error states |

## 9. Launch Plan

1. **Internal ring (S0 onward):** staff use each slice as it lands.
2. **Closed beta (after S10):** about 60 participants across personas (UAT-001), Stripe test mode first then a small live cohort; points have no cash value.
3. **Public GA:** after UAT exit, pen test closure, load targets, and go/no-go (REL-001 section 9); ring rollout from 5% of signups to 100%.
4. **Eight-week KPI review** after GA with a corrective plan if BG-01, BG-02, or BG-03 fall short.

## 10. Risks

| Risk | Mitigation |
| --- | --- |
| Content production lags engineering | Start content in week 1; keep one track; staged release by module |
| Sandbox cost or latency misses targets | POC-1 results drive pool sizing; fall back to Python-only if needed |
| Scope creep from fast-follow features | Frozen MVP list; cut lines in section 6; backlog for FF |
| Slice dependencies (ledger before billing, judging before points) | Slice order above; contract tests between slices |
| Beta recruitment shortfall | Waitlist from week 8; partner communities; incentives in points or credit |
| Simplifications create rework | Keep interfaces stable (search, analytics, workflow ports) so engines can be swapped |

## 11. Open Decisions

- Confirm the content plan sizes and who authors lessons and challenges.
- Approve ADR-015 (MVP simplifications) after POC results.
- Confirm Free versus Pro limits and whether Starter waits for FF.
- Choose the cloud provider and region (affects S0 and POC-1).
- Confirm minor-user policy with Legal before the beta cohort is recruited.
