# CodeFull Architecture Document

**Doc ID:** ARCH-001 | **Version:** 0.1 draft | **Status:** for architecture review | **Owner:** Architect **Upstream:** PRD-001, SRS-001, Backend Plan | **Downstream:** SEC-001, OpenAPI, Test Plan, Release Plan, Playbook

## 1. Purpose, Drivers, and Constraints

### 1.1 Architectural drivers (from SRS)

| Driver | Source | Consequence |
| --- | --- | --- |
| Untrusted code execution at scale | FR-EXE-001..008, NFR-003, NFR-013 | Dedicated Execution Gateway with tiered isolation and warm pools |
| Live competition with fair clocks | FR-CMP-008..010, NFR-006, NFR-012 | Server-authoritative realtime hub, Redis state |
| Money-like points with auditability | FR-RWD-001..009 | Append-only double-entry ledger, workflow-based settlement |
| Privacy as a product promise | FR-IDN-005, FR-CMP-005, FR-COM-002 | Server-side enforcement in every read path, RLS |
| Multi-tenant including Enterprise | FR-IDN-009, FR-PLT-007 | tenant\_id everywhere, RLS, per-tenant leaderboards |
| Many clients, one behavior | PRD channels | Contract-first APIs, generated SDKs |
| AI features with cost and abuse risk | FR-AI-001..006 | AI Gateway with quotas, injection defenses |
| Reliability and recovery | NFR-014..016 | Multi-AZ, PITR, queues, idempotency |

### 1.2 Architectural principles

1. Multi-tenant from day one; Row Level Security (RLS) policies are created in the same migration as their tables, and a CI linter enforces it.
2. Application services never touch PostgreSQL directly; they use the Data Access Layer (DAL).
3. The Execution Gateway is the sole path to sandboxes.
4. Identity is verified once at the API Gateway, which sets signed internal headers; services trust only the signature.
5. Secrets exist only in Vault.
6. Entitlement lookups fail open; money and ledger operations fail closed.
7. Judging and safety decisions are deterministic; no model decides whether code is safe or correct.
8. Contract first: OpenAPI, AsyncAPI, and protobuf are the source of truth; SDKs are generated.
9. Prefer asynchronous events across domains; keep synchronous chains short.
10. Reuse proven isolation architecture (Kubernetes with gVisor and Firecracker tiers) rather than redesign it.

### 1.3 Constraints

Python and Go for services; Kubernetes hosting; PostgreSQL as system of record; English at MVP; real-money track disabled at launch; web first, desktop and mobile later.

## 2. System Context (C4 Level 1)

```
                    Learners / Competitors / Mentors / Recruiters / Admins
                                      |
                      Web | Desktop (Tauri) | Mobile (React Native)
                                      |
                                  [ CodeFull ]
            +---------+------+--------+--------+---------+----------+
            |         |      |        |        |         |          |
        Identity   Stripe  PayPal   FCM/APNs  Email    AI model   App stores
        (OIDC)            (P2)                         provider   (receipts)
```

## 3. Container View (C4 Level 2)

```
Clients -> CDN + WAF -> API Gateway (Envoy + ext-authz)
                              |  JWT check, rate limits, signed headers
   +-------------+------------+------------+--------------+-------------+
   |             |            |            |              |             |
 Identity   Learning     Challenges    Rewards       Community     AI Gateway ---> model provider
 Careers    Tournaments  Billing       Notifications Analytics     Admin
   (FastAPI domain services)             |
   |             |            |          | gRPC                      
   +-------------+------------+----------+
                              |
                          DAL (Go) ----> PostgreSQL (HA, PgBouncer)
                              
 Realtime Hub (Go) <-> Redis (sorted sets, pub/sub, rate limits)
 Execution Gateway (Go) -> gVisor pool | Firecracker pool
 NATS JetStream (events) <-> Temporal (workflows) <-> workers
 OpenSearch (search)   ClickHouse (analytics)   Object storage + CDN (media)
 Vault (secrets/PKI)   Observability stack (OTel, Prometheus, Grafana, Loki, Tempo)
```

### 3.1 Service catalog

| Service | Tech | Responsibility | Owns data | Key requirements |
| --- | --- | --- | --- | --- |
| gateway | Envoy + ext-authz | TLS, JWT validation, rate limits, signed internal headers, WAF hooks | none | SEC auth items, NFR-001 |
| identity | FastAPI | Profiles, privacy settings, orgs, sessions, export and deletion | users, profiles, privacy | FR-IDN-\* |
| learning | FastAPI | Courses, lessons, progress, XP, tiers, streaks, achievements | learning schema | FR-LRN-\* |
| challenges | FastAPI | Challenge catalog, entries, submissions, verdicts, leaderboards | challenges schema | FR-CMP-001..007, FR-EXE-005 |
| battles | Go | Lobby, server clock, live scoreboard, spectators | Redis state, battles tables via DAL | FR-CMP-008..010 |
| tournaments | FastAPI + Temporal | Brackets, scheduling, advancement | tournaments schema | FR-CMP-011..012 |
| rewards | FastAPI + Temporal | Ledger, pools, settlement, redemption, fraud rules | ledger schema | FR-RWD-\* |
| community | FastAPI | Q&A, votes, reputation, mentors, bookings, moderation intake | community schema | FR-COM-\* |
| careers | FastAPI | Jobs, applications, recruiter visibility and feed | careers schema | FR-CAR-\* |
| billing | FastAPI | Plans, Stripe, store receipts, usage meters, entitlements | billing schema | FR-BIL-\* |
| ai-gateway | FastAPI | Tutor, assistant, quotas, redaction, streaming, logging | AI sessions | FR-AI-\* |
| notifications | FastAPI + workers | In-app, email, push, preferences | notification schema | FR-PLT-001 |
| analytics | FastAPI + ingest | Event ingestion, ClickHouse queries, personal and org dashboards | ClickHouse | FR-PLT-003, FR-PLT-007 |
| admin | FastAPI | Moderation, flags, configuration, audit queries | flags, moderation | FR-PLT-004..006 |
| dal | Go (gRPC) | Typed data access, RLS context, transaction control | none (proxy) | Principle 2 |
| execution-gateway | Go | Job scheduling, sandbox pools, limit enforcement, result streaming | job records | FR-EXE-\* |

## 4. Key Runtime Views

### 4.1 Authenticated request

1. Client calls the gateway with an OIDC access token.
2. Gateway validates signature, expiry, audience; applies rate limits; strips any inbound internal headers; sets signed headers (tenant, user, roles, tier, plan).
3. Domain service verifies the header signature, authorizes the action, and calls the DAL via gRPC with the context.
4. DAL opens a transaction, sets app.tenant\_id and app.user\_id with SET LOCAL, runs typed queries; RLS applies.
5. Response returns through the gateway with request id and rate-limit headers.

### 4.2 Run code and judge a challenge

```
Client -> challenges/playground -> validate + quota (billing entitlement, fail open)
       -> Execution Gateway -> pick tier (gVisor default | Firecracker hardened)
       -> warm sandbox: code mounted read-only, limits applied, no network
       -> harness runs tests, streams output (SSE) -> sandbox destroyed
       -> event judged.v1 on NATS
            |-> challenges: store verdict
            |-> rewards: post XP and points (idempotent)
            |-> battles hub: update scoreboard
            |-> analytics: record
```

### 4.3 Live battle

- The hub creates the match, sets start and end times from its own clock, and keeps standings in a Redis sorted set.
- Clients subscribe over WebSocket with sequence numbers; on reconnect they resume from the last sequence.
- Submissions go to the Execution Gateway (hardened tier); verdict events update scores; the hub never accepts scores from clients.
- Private entrants are rendered as Anonymous in every payload except to the owner and moderators.
- At close, a settlement workflow runs (see 4.4).

### 4.4 Prize settlement and redemption

- Settlement is a Temporal workflow: freeze pool -> compute payouts from final standings -> post ledger entries -> notify. Each step has an idempotency key; retries cannot double-post.
- Redemption is a workflow: hold points -> fraud and velocity checks -> approve or review -> fulfill (grant entitlement or payout) -> release or refund. Anything uncertain fails closed.

### 4.5 AI request

Client -> gateway -> ai-gateway: check plan quota, redact secrets, attach lesson or code context in delimited blocks, call provider, stream tokens (SSE), meter usage, log for abuse review. Output is text only; any suggested code runs only through the Execution Gateway when the user chooses.

## 5. Data Architecture

### 5.1 Stores and roles

| Store | Role | Notes |
| --- | --- | --- |
| PostgreSQL 16 | System of record | HA with multi-AZ and PITR; PgBouncer; monthly partitions on high-volume tables |
| Redis 7 cluster | Leaderboards, battle state, rate limits, presence, pub/sub | Rebuildable from Postgres; not a source of truth |
| NATS JetStream | Domain events | At-least-once; consumers are idempotent |
| Temporal | Long-running workflows | Settlement, redemption, tournaments, retries |
| OpenSearch | Search index | Fed by events; respects privacy flags at index time |
| ClickHouse | Analytics | Materialized views for heatmaps, XP over time, win rate |
| Object storage + CDN | Media, submissions, avatars, invoices | Signed URLs; private by default |

### 5.2 Schema layout

One Postgres schema per domain (identity, learning, challenges, battles, tournaments, rewards, community, careers, billing, notifications, admin). Cross-schema references use ids, not joins across service boundaries; read models are built from events.

### 5.3 Tenancy and RLS

- Every tenant-scoped table has tenant\_id, RLS enabled, and policies in the same migration; db/lint fails CI otherwise.
- Consumer users belong to the public tenant; each Enterprise org is its own tenant.
- Cross-tenant reads (global leaderboard, public portfolio, public challenge catalog) use audited views that expose only public columns and honor privacy flags.
- pgTAP tests prove tenant A cannot read or write tenant B and that anonymous entries expose no identity.

### 5.4 Ledger design

- Tables: accounts (user, pool, system), entries (account, amount, direction, transaction id, source, idempotency key, created\_at).
- Rules: one transaction per posting set; debits equal credits; no update or delete (revoked at database role level); balances are derived with a cached projection refreshed by events and verified nightly.
- Daily reconciliation compares projections and provider reports; violations page on-call.

### 5.5 Leaderboards and rank history

Redis sorted sets hold live scores per scope (global, weekly, language, region, friends, org). Postgres stores the source of truth; a nightly job rebuilds the sets and writes daily snapshots used for rank change. Anonymous entrants appear with a placeholder identity while still ranking.

## 6. Event and Workflow Catalog

| Event / workflow | Producer | Consumers | Notes |
| --- | --- | --- | --- |
| user.registered.v1 | identity | learning, notifications, analytics | Creates progress record, welcome flow |
| lesson.completed.v1 | learning | learning (XP), rewards, analytics | Idempotent by lesson and user |
| xp.awarded.v1, tier.promoted.v1 | learning | notifications, analytics, search | Tier change fires once |
| run.requested.v1, judged.v1 | challenges, execution-gateway | challenges, rewards, battles, analytics | Verdict is final |
| leaderboard.updated.v1 | challenges, battles | Redis updater, analytics | Honors visibility flags |
| ledger.posted.v1 | rewards | notifications, analytics, reconciliation | Source of balance projection |
| answer.accepted.v1 | community | rewards, notifications | One award per acceptance |
| subscription.changed.v1 | billing | entitlement cache, notifications | Drives plan limits |
| privacy.changed.v1 | identity | search indexer, leaderboards, analytics | Triggers re-index and cache purge |
| ai.usage.v1 | ai-gateway | billing meters, analytics | Token counts per user |
| Workflow: PrizeSettlement | rewards (Temporal) | rewards, notifications | Freeze, compute, post, notify |
| Workflow: Redemption | rewards (Temporal) | billing, notifications | Hold, check, fulfill or refund |
| Workflow: TournamentRound | tournaments (Temporal) | battles, notifications | Schedules and advances matches |
| Workflow: AccountDeletion | identity (Temporal) | all domains | Detaches identity, keeps tombstoned ledger rows |

Event rules: versioned schemas in contracts/proto; at-least-once delivery; consumers dedupe by event id; poison messages go to a dead-letter stream with alerting.

## 7. Deployment Architecture

```
Region A (primary)                                   Region B (DR)
+------------------------------------------+        +-------------------------+
| CDN/WAF -> Envoy gateway (HPA)           |        | Standby: backups,       |
| Kubernetes: services node pool           |        | infra as code, warm     |
| Kubernetes: sandbox node pool (gVisor)   |        | restore targets         |
| Bare-metal or nested-virt pool           |        +-------------------------+
|   (Firecracker microVMs)                 |
| Postgres HA (3 AZ) + PITR | Redis cluster |
| NATS cluster | Temporal | OpenSearch      |
| ClickHouse | Vault (HA) | Observability   |
+------------------------------------------+
```

- **Environments:** dev, staging (production-like, anonymized data), prod. Preview environments per pull request for web.
- **Delivery:** GitHub Actions builds and signs images; Argo CD syncs Helm charts; Argo Rollouts performs canary with automated analysis and rollback.
- **Network:** private subnets; egress proxy with allowlist; sandbox node pools have no route to internal services or metadata endpoints; mTLS inside the mesh.
- **Infrastructure as code:** Terraform for cloud resources, Helm for workloads, policy as code (OPA/Gatekeeper) for admission.

## 8. Scalability and Capacity

| Area | Baseline sizing assumption | Scaling mechanism |
| --- | --- | --- |
| API services | 4,200 concurrent users, 3x spike | Horizontal pod autoscaling on CPU and request rate |
| Realtime hub | 50 battles x (100 entrants + 1,000 spectators) | Shard rooms by battle id; Redis pub/sub per shard |
| Sandboxes | 500 runs per second peak | Warm pools per language image, autoscale pool size on queue depth |
| Postgres | Read-heavy with partitioned write-heavy tables | Read replicas, PgBouncer, monthly partitions, archive old partitions |
| Leaderboards | Millions of members | Redis sorted sets sharded by scope |
| Media | Video and audio lessons | CDN with HLS, signed URLs |

Capacity numbers are starting hypotheses to validate in POC-1 and POC-2 and the load tests.

## 9. Resilience and Recovery

- **Failure modes and responses:** billing lookup fails -> fail open and log; judging saturated -> queue with ETA; Redis unavailable -> serve leaderboards from Postgres snapshots at reduced freshness; NATS unavailable -> outbox pattern in services retries delivery; AI provider down -> tutor shows degraded notice, core app unaffected.
- **Outbox pattern:** services write events to an outbox table in the same transaction as state changes and a relay publishes to NATS.
- **Backups and DR:** continuous WAL archiving with PITR, daily snapshots copied cross-region, quarterly restore drill; RPO 5 minutes and RTO 1 hour per NFR-015.
- **Backpressure:** per-user and per-IP quotas at the gateway; bounded queues in the hub and execution gateway; circuit breakers on outbound calls.

## 10. Observability

OpenTelemetry traces across gateway, services, DAL, and gateway-to-sandbox calls; Prometheus metrics with SLO dashboards (availability, latency, queue depth, sandbox warm-pool hit rate, ledger invariant checks); structured logs in Loki with request, tenant, and user ids and no secrets or full submissions; Sentry for client and service errors; alerting on error budget burn, ledger mismatches, sandbox policy violations, and auth anomalies.

## 11. Client Architecture

| Client | Stack | Notes |
| --- | --- | --- |
| Web | React + TypeScript, TanStack Query, generated SDK | Design tokens as a shared theme package; routes replace the prototype navigate() function |
| Desktop | Tauri 2 wrapping the web app | OS keychain, signed updater, SQLite cache and sync queue, optional non-scoring local runner |
| Mobile | React Native with Expo | Secure storage, push, deep links, attestation, store billing, offline lessons |
| Native (later) | WinUI 3, SwiftUI/AppKit, GTK4 or Qt; Jetpack Compose; SwiftUI | Same contract; generated SDKs for C#, Swift, Kotlin, Rust |

All clients use OIDC with PKCE, the same error model, and the same realtime protocols.

## 12. Architecture Decision Records (summary)

| ADR | Decision | Rationale | Trade-off |
| --- | --- | --- | --- |
| ADR-001 | Python (FastAPI) for domain services, Go for DAL, hub, and Execution Gateway | Fast product iteration plus performance where concurrency matters | Two languages to maintain |
| ADR-002 | DAL is the only database client | Central RLS context, one place to audit queries, no ad hoc connections | Extra hop and a service to run |
| ADR-003 | PostgreSQL with RLS for multi-tenancy | Strong isolation enforced in the database | Policy complexity and testing cost |
| ADR-004 | Execution Gateway is the sole sandbox path; gVisor default, Firecracker hardened | Defense in depth for untrusted code | Higher infra cost and ops complexity |
| ADR-005 | Append-only double-entry ledger with idempotency keys | Auditability and safe retries | Derived balances need projection |
| ADR-006 | Temporal for settlement, redemption, tournaments | Durable, retryable workflows | New platform to operate |
| ADR-007 | NATS JetStream for events with outbox pattern | Simple, fast, at-least-once | Consumers must be idempotent |
| ADR-008 | Redis for realtime state; Postgres remains truth | Low-latency leaderboards and battles | Rebuild path required |
| ADR-009 | Server-authoritative battle clock | Prevents client-side cheating | Needs time sync UX |
| ADR-010 | Envoy gateway verifies identity once and signs internal headers | Single trust point, simple services | Gateway becomes critical path |
| ADR-011 | AI Gateway is the only model caller | Quotas, redaction, logging in one place | Added latency |
| ADR-012 | Contract-first with generated SDKs | Consistency across five client platforms | Spec discipline required |
| ADR-013 | Cross-platform clients first (Tauri, React Native), native later | Reach with one TypeScript codebase | Platform-specific polish deferred |
| ADR-014 | Entitlements fail open; money fails closed | Do not block paying users; never risk money | Possible short-term over-allowance, logged |

Full ADRs live in docs/adr with context, options, decision, and consequences.

## 13. NFR Coverage Matrix

| NFR | Addressed by |
| --- | --- |
| NFR-001, 002 | Gateway rate limits, DAL pooling, read replicas, caching, autoscaling |
| NFR-003, 004, 013 | Warm sandbox pools, Execution Gateway scheduling, result streaming |
| NFR-005 | CDN, code splitting, image and media optimization |
| NFR-006, 012 | Realtime hub sharding, Redis, server clock and time sync |
| NFR-007 | Redis sorted sets |
| NFR-008 | AI Gateway streaming, regional provider endpoint |
| NFR-009 | OpenSearch with event-driven indexing |
| NFR-010 | Notification workers, push providers |
| NFR-011 | Horizontal scaling, load tests with 3x spike |
| NFR-014, 015, 016 | Multi-AZ, PITR, cross-region backups, queues, outbox, circuit breakers |
| NFR-017, 018 | SEC-001 controls, privacy by design, deletion workflow |
| NFR-019, 020, 021 | Design system with accessibility checks, supported-client matrix in CI |
| NFR-022 | OpenTelemetry stack and SLO alerts |
| NFR-023 | Monorepo standards, contract-first CI, coverage gates |
| NFR-024 | Stripe-hosted fields, no card data in CodeFull systems |
| NFR-025 | Retention jobs, partition archival, audit log immutability |
| NFR-026 | Externalized strings in clients |

## 14. Risks and Open Decisions

- Cloud provider and region, and whether Firecracker needs bare metal or nested virtualization instances (decide after POC-1).
- Managed versus self-hosted Keycloak, Temporal, NATS, and OpenSearch.
- Data residency commitments for Enterprise customers.
- Final list of launch languages beyond Python and JavaScript.
- Capacity assumptions pending POC-1, POC-2, and load tests.
