# CodeFull Data Model Specification

**Doc ID:** DM-001 | **Version:** 0.1 draft | **Status:** for architecture and security review | **Owner:** Backend lead + Architect **Upstream:** SRS-001 sec 5, ARCH-001 sec 5, SEC-001, ECO-001 | **Downstream:** migrations in db/migrations, DAL queries, pgTAP suites, Playbook steps PB-05, PB-37

## 1. Conventions

| Topic | Rule |
| --- | --- |
| Engine | PostgreSQL 16; one schema per domain (identity, learning, execution, challenges, battles, rewards, community, careers, billing, ai, notifications, admin, platform) |
| Identifiers | UUID version 7 primary keys (time-ordered); external references use ids, never joins across service boundaries |
| Tenancy | Every tenant-scoped table has tenant\_id NOT NULL, RLS enabled and forced, policies in the same migration (SEC-014) |
| Timestamps | timestamptz in UTC; created\_at and updated\_at on mutable tables; created\_at only on append-only tables |
| Points | bigint, whole points; never floating point (money-like values) |
| Text and enums | text with CHECK constraints; case-insensitive handles use citext |
| JSONB | Only for configuration or provider payloads with a documented shape; never for fields queried by joins |
| Deletion | Hard delete or detachment per retention rules; soft delete flags only where the product needs undo; ledger and audit rows are never deleted |
| Naming | snake\_case; plural table names; foreign keys named table\_id; indexes named ix\_table\_columns |
| Privacy | Each column is classified (public, internal, confidential, restricted) in a comment; sensitive columns are encrypted at field level where SEC-036 requires |

## 2. Roles and Grants

| Role | Purpose | Rules |
| --- | --- | --- |
| migrator | Applies migrations | Owns schemas; not used at runtime; no BYPASSRLS in runtime paths |
| app\_rw | Used by the DAL for normal reads and writes | RLS applies (FORCE ROW LEVEL SECURITY); no superuser; no BYPASSRLS; no UPDATE or DELETE on ledger and audit tables |
| app\_ledger | DAL role used for posting entries | INSERT and SELECT only on ledger\_entries and ledger\_transactions |
| app\_ro | Read replicas and reporting | SELECT only; RLS applies |
| analytics\_export | Event export to analytics | SELECT on approved views only |

Credentials are dynamic and short-lived from Vault; only the DAL holds them (SEC-013, SEC-032).

## 3. Standard RLS Pattern

```sql
-- Context functions (set per transaction by the DAL using SET LOCAL)
CREATE SCHEMA IF NOT EXISTS app;
CREATE FUNCTION app.current_tenant() RETURNS uuid LANGUAGE sql STABLE AS
$$ SELECT NULLIF(current_setting('app.tenant_id', true), '')::uuid $$;
CREATE FUNCTION app.current_user_id() RETURNS uuid LANGUAGE sql STABLE AS
$$ SELECT NULLIF(current_setting('app.user_id', true), '')::uuid $$;

-- Per table, in the same migration as the CREATE TABLE
ALTER TABLE learning.lesson_progress ENABLE ROW LEVEL SECURITY;
ALTER TABLE learning.lesson_progress FORCE ROW LEVEL SECURITY;

-- Restrictive guard: every statement must match the tenant
CREATE POLICY tenant_guard ON learning.lesson_progress AS RESTRICTIVE
  USING (tenant_id = app.current_tenant())
  WITH CHECK (tenant_id = app.current_tenant());

-- Permissive owner rule: a learner sees and writes only their own rows
CREATE POLICY owner_rw ON learning.lesson_progress
  USING (user_id = app.current_user_id())
  WITH CHECK (user_id = app.current_user_id());
```

If app.tenant\_id is not set, the policies return no rows. The db/lint check fails any migration that creates a table without tenant\_id, ENABLE and FORCE ROW LEVEL SECURITY, and at least one tenant guard (SEC-014). Each policy has a pgTAP test (SEC-015, TC-1104).

## 4. Platform Tables (cross-cutting)

| Table | Key columns | Notes |
| --- | --- | --- |
| platform.outbox\_events | id, tenant\_id, aggregate\_type, aggregate\_id, event\_type, event\_version, payload jsonb, created\_at, published\_at | Written in the same transaction as state changes; relay publishes to NATS (ARCH-001 sec 9) |
| platform.processed\_events | consumer, event\_id, processed\_at; PK (consumer, event\_id) | Consumer-side deduplication |
| platform.idempotency\_keys | tenant\_id, key, scope, request\_hash, response\_ref, created\_at; unique (tenant\_id, scope, key) | Backs the Idempotency-Key header; TTL cleanup |
| platform.jobs | id, tenant\_id, queue, payload, run\_at, attempts, status, locked\_by, locked\_at | MVP durable job queue behind WorkflowPort (ADR-015 proposed) |
| admin.audit\_log | id, tenant\_id, actor\_id, action, target\_type, target\_id, reason, before\_hash, after\_hash, ip, created\_at; partitioned monthly | Append-only; role has no UPDATE or DELETE (SEC-074, TC-1003) |

## 5. Identity Schema

| Table | Key columns | Notes |
| --- | --- | --- |
| identity.tenants | id, kind (public, org), name, status | The public tenant plus one row per Enterprise org (P2) |
| identity.users | id, tenant\_id, handle citext unique, email citext unique, display\_name, status, created\_at | Email is confidential; verified flag from Keycloak; handle immutable after 30 days |
| identity.oidc\_identities | user\_id, provider, subject; unique (provider, subject) | Links GitHub and Google accounts |
| identity.user\_profiles | user\_id PK, bio, location, skills text\[\], avatar\_key | Public fields exposed only through views |
| identity.privacy\_settings | user\_id PK, show\_on\_leaderboard, allow\_recruiter\_contact, public\_challenge\_history, show\_points\_balance, updated\_at | Read by the shared privacy library in every read path (SEC-017) |
| identity.onboarding\_answers | user\_id PK, experience\_level, primary\_goal, known\_languages text\[\], weekly\_hours | FR-IDN-003 |
| identity.devices | id, user\_id, platform, app\_version, push\_token (encrypted), last\_seen\_at, revoked\_at | Device registry (FR-IDN-010) |
| identity.consent\_records | id, user\_id, purpose, granted, policy\_version, created\_at | Append-only; recruiter visibility, marketing, telemetry (SEC-077) |
| identity.data\_requests | id, user\_id, kind (export, deletion), status, requested\_at, completed\_at | Drives the export and deletion workflows (SEC-075) |
| identity.memberships | user\_id, tenant\_id, role | P2 Enterprise roles |

## 6. Learning Schema

| Table | Key columns | Notes |
| --- | --- | --- |
| learning.courses | id, slug, title, description, tier\_min, tier\_max, status, version | Content imported from versioned Markdown and YAML |
| learning.modules | id, course\_id, position, title |  |
| learning.lessons | id, module\_id, position, title, duration\_minutes, xp\_award, points\_band | points\_band maps to ECO-001 length bands |
| learning.lesson\_formats | lesson\_id, format (video, audio, text, interactive), asset\_key, duration\_s, transcript\_key, captions\_key | Assets in private storage; signed URLs (FR-LRN-003) |
| learning.enrollments | tenant\_id, user\_id, course\_id, enrolled\_at; PK (user\_id, course\_id) |  |
| learning.lesson\_progress | tenant\_id, user\_id, lesson\_id, format, position\_s, completed\_at; PK (user\_id, lesson\_id) | Server-validated updates only (SEC-021) |
| learning.xp\_events | id, tenant\_id, user\_id, source\_type, source\_id, xp, created\_at; unique (user\_id, source\_type, source\_id) | Idempotent XP awards |
| learning.tier\_progress | user\_id, tier, xp\_in\_tier, completed\_at; PK (user\_id, tier) | Per-tier XP (ECO-001 sec 3) |
| learning.streaks | user\_id PK, current\_days, best\_days, last\_activity\_user\_day, freezes\_used\_month | User-day computed on the server (TM-LRN-003) |
| learning.weekly\_goals | user\_id, week\_start, target, done; PK (user\_id, week\_start) |  |
| learning.achievements | id, code, name, rarity, criteria jsonb | Seeded catalog |
| learning.user\_achievements | user\_id, achievement\_id, earned\_at; PK (user\_id, achievement\_id) | Awarded once |

## 7. Execution and Challenges Schemas

| Table | Key columns | Notes |
| --- | --- | --- |
| execution.runs | id, tenant\_id, user\_id, language, source\_ref, status, duration\_ms, memory\_kb, created\_at | Source stored in object storage or truncated copy per retention; no payment or token data |
| execution.snippets | id, tenant\_id, user\_id, title, language, source\_ref, share\_token, created\_at | Share links are read and fork only (FR-EXE-004) |
| execution.usage\_counters | tenant\_id, user\_id, period\_start, kind (executions, exercises), count | Feeds quotas and meters (exercises tracked separately, ECO-001 decision 7) |
| challenges.challenges | id, tenant\_id, slug, title, description, mode, language\_hint, tier, status, opens\_at, closes\_at, time\_limit\_ms, memory\_limit\_mb, prize\_fund\_account\_id |  |
| challenges.challenge\_tests | id, challenge\_id, position, visibility (sample, hidden), input\_ref, expected\_ref | Hidden rows restricted to the judging role; never returned by APIs (TM-CMP-007) |
| challenges.entries | id, tenant\_id, challenge\_id, user\_id, visibility (public, private), created\_at; unique (challenge\_id, user\_id) | Visibility drives anonymity everywhere (SEC-017) |
| challenges.submissions | id, tenant\_id, entry\_id, language, source\_ref, status, verdict, passed\_cases, total\_cases, runtime\_ms, created\_at; partitioned monthly | Judged state is final; re-judging creates a new row |
| challenges.scores | entry\_id PK, best\_submission\_id, completion\_points, placement, cs\_awarded | Basis for CS and prizes (ECO-001) |
| challenges.leaderboard\_snapshots | scope, snapshot\_date, entry\_key, rank, cs; PK (scope, snapshot\_date, entry\_key) | entry\_key is an opaque id; identity joined only in owner and moderator views |
| challenges.similarity\_flags | id, submission\_a, submission\_b, score, status, reviewed\_by, decision | Feeds moderation (FR-CMP-013) |

## 8. Rewards Schema and Ledger Design

```sql
CREATE TABLE rewards.ledger_accounts (
  id            uuid PRIMARY KEY,
  tenant_id     uuid NOT NULL,
  kind          text NOT NULL CHECK (kind IN
                ('user_learning','user_prize','prize_fund','pool','issuance','sink','fee','adjustment')),
  owner_user_id uuid,            -- set for user_* accounts
  ref_id        uuid,            -- challenge or pool id for prize_fund and pool
  currency      text NOT NULL DEFAULT 'PTS',
  created_at    timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE rewards.ledger_transactions (
  id              uuid PRIMARY KEY,
  tenant_id       uuid NOT NULL,
  idempotency_key text NOT NULL,
  source_type     text NOT NULL,   -- lesson, challenge, answer, purchase, adjustment...
  source_id       uuid,
  config_version  text NOT NULL,   -- economy configuration used (ECO-001 sec 11)
  created_at      timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, idempotency_key)
);

CREATE TABLE rewards.ledger_entries (
  id         bigint GENERATED ALWAYS AS IDENTITY,
  tx_id      uuid NOT NULL,
  account_id uuid NOT NULL,
  direction  text NOT NULL CHECK (direction IN ('debit','credit')),
  amount     bigint NOT NULL CHECK (amount > 0),
  competition boolean NOT NULL DEFAULT false,  -- counts toward Competition Score
  created_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (id, created_at)
) PARTITION BY RANGE (created_at);

-- Append-only enforcement
REVOKE UPDATE, DELETE, TRUNCATE ON rewards.ledger_entries FROM app_rw, app_ledger;
REVOKE UPDATE, DELETE, TRUNCATE ON rewards.ledger_transactions FROM app_rw, app_ledger;
GRANT SELECT, INSERT ON rewards.ledger_entries, rewards.ledger_transactions TO app_ledger;

-- Balance invariant: debits equal credits per transaction (deferred constraint trigger,
-- checked at commit; rejects unbalanced sets)
```

| Table | Key columns | Notes |
| --- | --- | --- |
| rewards.account\_balances | account\_id PK, balance bigint, last\_entry\_id, updated\_at | Projection refreshed from entries; CHECK (balance >= 0) for user accounts; verified nightly against entries (SEC-058) |
| rewards.competition\_scores | user\_id, scope (global, weekly), cs bigint, updated\_at | Derived from entries where competition is true; rebuilt nightly; source of leaderboard seeding |
| rewards.catalog\_items | id, code, kind (cosmetic, pack, streak\_freeze), price\_points, status, config\_version | MVP catalog (ECO-001 sec 8) |
| rewards.user\_unlocks | user\_id, item\_id, ledger\_tx\_id, unlocked\_at | A purchase is a ledger debit plus an unlock row in one transaction |
| rewards.earning\_events | id, tenant\_id, user\_id, source\_type, source\_id, status (posted, held, rejected), reason | Fraud and velocity decisions (SEC-059); links to the ledger transaction |
| rewards.redemptions | id, user\_id, option, points, status, held\_reason, created\_at | Fast follow; written by the redemption workflow |
| rewards.pools and pool\_contributions | pool id, challenge id, cap, balance; contribution rows with contributor and ledger tx | Fast follow |

Rules: one transaction per posting set; every set balances; postings are idempotent by key; spending debits USER\_LEARNING first, then USER\_PRIZE; compensating entries use the ADJUSTMENT account with dual approval; reconciliation compares projections with entries and with provider reports (SEC-051, SEC-052, SEC-058, TC-0501, TC-0502, TC-0506, TC-0509).

## 9. Community Schema

| Table | Key columns | Notes |
| --- | --- | --- |
| community.questions | id, tenant\_id, author\_id, mode (open, discreet), title, body, tags text\[\], status, accepted\_answer\_id, created\_at | Discreet rows are excluded from feeds, search, and counts by policy and index rules (SEC-018) |
| community.answers | id, question\_id, author\_id, body, created\_at |  |
| community.votes | user\_id, target\_type, target\_id, value, created\_at; PK (user\_id, target\_type, target\_id) | One vote per target |
| community.mentor\_pool | user\_id, tier\_required, topics text\[\], capacity, active | MVP rule for assigned mentors (GAP-014 to be decided) |
| community.discreet\_assignments | question\_id PK, mentor\_id, assigned\_at | Only the asker and this mentor (and moderators) can read the question |
| community.reputation\_events | id, user\_id, source\_type, source\_id, delta | Idempotent by source |
| community.flags | id, target\_type, target\_id, reporter\_id, reason, status, created\_at | Intake for moderation (FR-COM-007) |
| community.mentor\_slots and bookings | Slot and booking rows with escrow ledger tx | Fast follow |

## 10. Careers, Billing, AI, Notifications, Admin

| Table | Key columns | Notes |
| --- | --- | --- |
| careers.jobs, applications, recruiter\_accounts, recruiter\_views | Job and applicant records; recruiter view log (user, recruiter, time) | Fast follow; views are logged and visible to the learner (SEC-019) |
| billing.plans | code (free, starter, pro, enterprise), limits jsonb, price\_cents | Limits as configuration |
| billing.subscriptions | id, tenant\_id, user\_id, plan\_code, provider, provider\_ref, status, current\_period\_end | Provider ids only; no card data (SEC-057) |
| billing.usage\_meters | user\_id, period\_start, ai\_tokens, executions, challenge\_entries | Feeds FR-BIL-003 and quotas |
| billing.webhook\_events | provider, event\_id, received\_at, processed\_at, status; unique (provider, event\_id) | Replay and duplicate protection (SEC-055) |
| billing.invoices | id, user\_id, provider\_ref, date, amount\_cents, status, pdf\_ref | Cached from the provider |
| ai.sessions and ai.messages | Session per user and topic; messages with role, redacted text, token counts | Retention-limited; PII and secrets redacted before storage (SEC-065) |
| ai.usage\_events | id, user\_id, tokens\_in, tokens\_out, model, created\_at | Meter source |
| notifications.notifications | id, user\_id, category, title, body, read\_at, created\_at |  |
| notifications.preferences | user\_id, category, in\_app, email, push |  |
| admin.feature\_flags | key, enabled, scope, updated\_by, updated\_at | real\_money\_track, ai\_features, registrations\_open, maintenance\_mode |
| admin.flag\_changes | id, key, requested\_by, approved\_by, new\_value, status | Dual control for sensitive flags (SEC-103) |
| admin.moderation\_items and actions | Item queue and recorded decisions with reasons | Every action also written to the audit log |

## 11. Public Views and Privacy Enforcement

- **Rule:** applications read other users' data only through audited views or privacy-aware repository functions, never by selecting base tables across users (SEC-016, SEC-017).
- **Views:** v\_public\_profiles (handle, display name, tier, skills, only where privacy allows); v\_leaderboard\_public (rank, display name or Anonymous, tier, cs, wins, losses); v\_challenge\_catalog (no hidden tests); v\_public\_portfolio (opt-in).
- **Anonymity design:** leaderboard rows are keyed by an opaque entry\_key. The identity join exists only in owner and moderator views; public views output the literal Anonymous for private entries and never include user\_id (TC-0404, TC-1123).
- **Search index:** built from the public views only; discreet questions, hidden users, and deleted accounts are excluded at index time (TC-1319).

## 12. Partitioning, Retention, and Deletion

| Data | Partitioning | Retention |
| --- | --- | --- |
| admin.audit\_log | Monthly | 7 years |
| rewards.ledger\_entries | Monthly | Kept; identity detached on account deletion (tombstoned account owner) |
| challenges.submissions | Monthly | 12 months unless featured in a portfolio |
| platform.outbox\_events and processed\_events | Weekly | 14 days after publish |
| ai.messages | Monthly | Per policy (proposed 90 days) |
| Application logs (outside Postgres) | n/a | 90 days |

Account deletion (SEC-075): the workflow removes or detaches personal data in every domain, removes the user from search and caches, replaces ledger owner references with a tombstone id, and records completion in identity.data\_requests. Partitions older than retention are detached and dropped by scheduled jobs after a backup check (TC-1311).

## 13. Indexing and Performance Notes

- Index foreign keys used in joins; add partial indexes for hot filters (for example open challenges, unread notifications).
- Leaderboards read from Redis; Postgres keeps source of truth and snapshots; rebuild jobs run off-peak.
- RLS predicates must be index-friendly: lead composite indexes with tenant\_id where policies filter on it.
- Measure overhead of SET LOCAL and RLS in POC-4 (budget under 10%); adjust pooling and indexes from the results.
- Large reads (exports, analytics) run on replicas through approved views.

## 14. Migration Standards

1. Forward-only in production; expand, migrate, contract across releases (REL-001 sec 7).
2. The table, its constraints, its indexes, and its RLS policies ship in one migration file.
3. Concurrent index builds; no long locks on hot tables; batch backfills with throttling.
4. Every migration has a rollback or forward-fix note and a staging dry run on production-sized data.
5. Ledger and audit tables receive no destructive migrations.
6. CI runs the RLS linter, pgTAP suites, and a schema diff against the expected contract.

## 15. Entity Relationship Overview

```
tenants 1---* users 1---1 privacy_settings
                 | 1---* devices            1---* consent_records
                 | 1---* enrollments *---1 courses 1---* modules 1---* lessons 1---* lesson_formats
                 | 1---* lesson_progress *---1 lessons
                 | 1---1 streaks    1---* tier_progress    1---* user_achievements *---1 achievements
                 | 1---* entries *---1 challenges 1---* challenge_tests
                 |         1---* submissions 1---1 scores
                 | 1---* questions 1---* answers ; votes ; discreet_assignments *---1 mentor_pool
                 | 1---* subscriptions ; usage_meters ; ai.sessions 1---* ai.messages
                 | 1---2 ledger_accounts (user_learning, user_prize)
ledger_transactions 1---* ledger_entries *---1 ledger_accounts
ledger_accounts (prize_fund) *---1 challenges
```

## 16. Seed Data

| Seed | Content |
| --- | --- |
| Tiers | Six tiers with per-tier XP thresholds (ECO-001 sec 3) |
| Achievements | About 12 badges with rarity and criteria |
| Plans | Free, Starter, Pro, Enterprise limits as configuration |
| System ledger accounts | ISSUANCE, SINK, ADJUSTMENT, FEES per tenant |
| Feature flags | Defaults: real\_money\_track off, ai\_features on, registrations\_open on, maintenance\_mode off |
| Economy configuration | Version 1 of the earning, XP, catalog, and fraud rules |
| Demo content | Sample course and challenges for non-production environments only |

## 17. Data Classification and Encryption Map

| Class | Fields |
| --- | --- |
| Public (through views, with consent) | handle, display name, tier, skills, CS, public portfolio items |
| Internal | lesson progress, XP, streaks, battle standings, analytics events |
| Confidential | email, bio, location, submissions, questions, discreet items, subscription state, AI messages |
| Restricted | ledger entries and balances, payout details, KYC data, device push tokens, secrets and keys, audit log |

Field-level encryption: payout details, KYC data, push tokens, and any future sensitive identifiers (SEC-036). Keys in KMS; rotation tested annually (SEC-037).

## 18. Open Items

- Confirm the two-bucket ledger design and CS derivation with the Product owner (ECO-001 decisions 1 and 6).
- Decide the MVP rule for the assigned mentor on discreet questions (GAP-014).
- Confirm retention periods for submissions and AI messages with Legal.
- Update after POC-3 and POC-4 results (ledger throughput and RLS overhead).
- Generate the schema reference and ERD from migrations in CI so this document stays aligned.
