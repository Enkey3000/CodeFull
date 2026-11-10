# CodeFull Backend Plan

Backend architecture, security, frontend wiring, testing, and cross-platform / native delivery for the CodeFull platform.

## 1. Scope and Guiding Principles

The prototype exposes 26 surfaces: Dashboard, Profile, Portfolio, Learning Center, Courses, Playground, AI Tutor, Challenges, Live Battles, Tournaments, Leaderboards, Progression, Rewards, Prize Pools, Community, Mentors, Jobs, Enterprise, Analytics, Notifications, Billing, Settings, Admin. These collapse into ten backend domains:

- **Identity and Tenancy:** users, orgs (Enterprise), roles, privacy flags (anonymous leaderboard entry, recruiter visibility)
- **Learning:** tiers (Beginner to Guru), courses, lessons in four formats (video, audio, text, interactive), XP, streaks
- **Execution:** playground runs and challenge judging in sandboxes
- **Competition:** challenges, live battles, tournaments, leaderboards
- **Rewards:** points ledger, prize pools, redemptions (dual-track: points now, real-money in Phase 2, behind a flag)
- **Community:** Q&A (open and discreet), mentors, bookings
- **Careers:** recruiter marketplace, job profiles, applications
- **AI:** tutor, code assistant, recommendations (Claude-powered)
- **Billing:** plans, usage metering, invoices, entitlements
- **Platform:** notifications, analytics, moderation, admin config

Principles:

1. Multi-tenant from day one: every row carries tenant\_id and is protected by Postgres Row Level Security (RLS).
2. RLS policies live in the same migration as their table; a CI linter fails any migration that creates a table without a policy.
3. Application services never touch PostgreSQL directly. They go through a Data Access Layer (DAL) that sets tenant and user context per request.
4. The Execution Gateway is the only path to sandboxes. Nothing else talks to Firecracker or gVisor.
5. Secrets live in Vault only. No secrets in env files, images, or CI variables.
6. Identity is verified once at the API Gateway, which signs internal headers; downstream services trust only the signature.
7. Entitlement checks fail open (a billing lookup outage never blocks a paying user). Money movement (redeem, payout, prize award) always fails closed.
8. Never ask an LLM whether LLM-generated or user-submitted code is safe. Safety comes from isolation and deterministic policy, not model judgment.
9. Contract first: OpenAPI and protobuf are the source of truth; every client SDK is generated.

## 2. Tech Stack

| Layer | Choice | Why |
| --- | --- | --- |
| Edge / API Gateway | Envoy (or Kong) with an ext-authz filter | JWT validation, rate limits, signed header injection, WAF hooks |
| Domain services | Python 3.12 + FastAPI + Pydantic v2 | Fast iteration, native async, strong OpenAPI output |
| Data Access Layer | Go + gRPC (sqlc + pgx) | Typed queries, RLS context set per call, small and fast |
| Realtime hub | Go + WebSockets | Battles, live scoreboards, spectator mode at high fan-out |
| Execution Gateway | Go | Job scheduling, warm pools, sandbox lifecycle |
| Sandboxes | Kubernetes + gVisor (standard tier) and Firecracker microVMs (hardened tier) | Strong isolation for untrusted code |
| Primary database | PostgreSQL 16 (HA, PgBouncer) | Relational core, RLS, JSONB, partitioning |
| Cache / realtime state | Redis 7 (cluster) | Leaderboards (sorted sets), rate limits, presence, pub/sub |
| Event bus | NATS JetStream | Judging results, notifications, ledger events, fan-out |
| Workflows | Temporal | Tournaments, payouts, redemptions, retries with idempotency |
| Search | OpenSearch | Challenges, courses, coders, Q&A |
| Analytics | ClickHouse | Activity heatmaps, XP over time, win-rate by language |
| Object storage | S3-compatible (S3 / R2 / MinIO) | Lesson media, submissions, avatars, invoices |
| Media delivery | CDN + HLS packaging | Video and audio lessons with captions and transcripts |
| Identity | Keycloak (OIDC, OAuth2, passkeys, SAML/SCIM for Enterprise) | GitHub and Google sign-in, org SSO |
| Payments | Stripe (subscriptions, invoices), PayPal Payouts and a gift-card partner for redemptions | Billing and cash-out |
| AI | AI Gateway service wrapping the Claude API | Central prompt policy, quotas, token metering, logging |
| Secrets / PKI | HashiCorp Vault | Dynamic DB creds, signing keys, KMS-backed |
| Infra | Kubernetes, Terraform, Argo CD, Helm | GitOps delivery |
| Observability | OpenTelemetry, Prometheus, Grafana, Loki, Tempo, Sentry | Traces, metrics, logs, errors |
| Frontend (wiring target) | React + TypeScript (Vite or Next.js), TanStack Query, generated SDK | The prototype is static HTML; this is its production form |

## 3. Backend Project Structure

A single monorepo (Turborepo with per-service Makefiles):

```
codefull/
├─ apps/
│  ├─ web/                    # React + TS frontend (ported from prototype)
│  ├─ desktop-tauri/          # cross-platform desktop shell
│  ├─ mobile-rn/              # cross-platform mobile (React Native / Expo)
│  ├─ desktop-native/{windows,macos,linux}/
│  └─ mobile-native/{android,ios}/
├─ services/
│  ├─ gateway/                # Envoy config + ext-authz
│  ├─ identity/               # FastAPI: profiles, orgs, privacy flags
│  ├─ learning/               # FastAPI: courses, lessons, XP, tiers
│  ├─ challenges/             # FastAPI: challenges, submissions, verdicts
│  ├─ battles/                # Go: realtime hub, scoreboard, timers
│  ├─ tournaments/            # FastAPI + Temporal workers
│  ├─ rewards/                # FastAPI: ledger, pools, redemptions
│  ├─ community/              # FastAPI: Q&A, mentors, bookings
│  ├─ careers/                # FastAPI: jobs, recruiter marketplace
│  ├─ billing/                # FastAPI: plans, usage, Stripe webhooks
│  ├─ ai-gateway/             # FastAPI: tutor, assistant, quotas
│  ├─ notifications/          # push / email / in-app workers
│  ├─ analytics/              # ingestion + ClickHouse query API
│  ├─ admin/                  # moderation, config, feature flags
│  ├─ dal/                    # Go: Data Access Layer (gRPC)
│  └─ execution-gateway/      # Go: sole path to sandboxes
├─ sandbox/
│  ├─ images/                 # per-language runtime images
│  ├─ harness/                # test runner, resource accounting
│  └─ policies/               # seccomp, gVisor, Firecracker configs
├─ contracts/
│  ├─ openapi/                # public REST specs
│  ├─ proto/                  # internal gRPC + event schemas
│  └─ sdk/                    # generated: ts, kotlin, swift, csharp, rust
├─ db/
│  ├─ migrations/             # table + RLS policy in the same file
│  ├─ seeds/                  # tiers, achievements, plans, demo data
│  └─ lint/                   # CI check: every table has RLS + tenant_id
├─ infra/{terraform,helm,argocd}/
├─ ops/                       # runbooks, dashboards, alerts
├─ tests/                     # e2e, load, security, contract suites
└─ docs/                      # ADRs, API guides, threat models
```

Each FastAPI service follows one layout: app/api (routers), app/domain (pure business logic), app/clients (DAL, bus, other services), app/schemas, app/deps (auth context from signed headers), tests/.

## 4. Tools Required

- **Languages and runtimes:** Python 3.12, Go 1.22+, Node 20+, Rust (Tauri), Swift, Kotlin, C#/.NET 8
- **Build and quality:** uv or Poetry, ruff, mypy, pytest, golangci-lint, ESLint, Prettier, pre-commit
- **API tooling:** OpenAPI Generator or openapi-typescript, buf (protobuf), Spectral (API lint), Schemathesis (API fuzzing)
- **Database:** Atlas or Alembic (migrations), sqlc, pgTAP (RLS tests), pg\_partman, PgBouncer
- **Testing:** pytest, Testcontainers, Playwright, k6, Pact, Toxiproxy, Maestro or Detox (mobile), XCTest, Espresso
- **Security:** Semgrep, CodeQL, Trivy, Syft (SBOM), Gitleaks, OWASP ZAP, Checkov, Cosign (image signing), OPA/Gatekeeper
- **Delivery:** GitHub Actions, Docker Buildx, Argo CD, Argo Rollouts (canary), Terraform, Helm
- **Runtime ops:** kubectl, Vault CLI, Temporal CLI, nats CLI, Grafana, PagerDuty
- **Packaging and signing:** Apple notarytool, Windows signtool, Fastlane, Gradle, MSIX tooling, Flatpak builder, Sparkle, Tauri updater

## 5. Backend Architecture

### 5.1 Topology

```
Clients (web, desktop, mobile)
        │  HTTPS / WSS
        ▼
  CDN + WAF ──► API Gateway (Envoy)
                  │  verifies JWT, applies rate limits,
                  │  injects signed internal headers (tenant, user, tier, plan)
    ┌─────────────┼─────────────────────────────┐
    ▼             ▼                             ▼
Domain services     Realtime hub (Go)         AI Gateway
(FastAPI)               │ Redis pub/sub            │
    │ gRPC              ▼                          ▼
    ▼                 Redis                    Claude API
  DAL (Go) ──► PostgreSQL
    │
    ├──► NATS JetStream ──► Temporal workers, notifications, analytics sinks
    └──► Execution Gateway ──► gVisor pool / Firecracker pool
```

### 5.2 Key flows

**Run code (Playground and Challenge submit)**

1. Client posts code to the challenges or playground service, which validates size, language, entitlement, and per-user rate.
2. The service calls the Execution Gateway (gRPC). The gateway picks a tier (gVisor by default, Firecracker for hardened or competition-grade runs), takes a warm sandbox, mounts code read-only, and applies CPU, memory, wall time, process, and output limits with networking disabled.
3. The harness runs the test cases and streams results. The gateway destroys the sandbox (no reuse across users).
4. The result is published on NATS: challenges stores the verdict, rewards awards XP and points, the battles hub updates the scoreboard.

**Live battle**

- Match state is server-authoritative: the hub owns the clock, entrant list, and scoreboard in Redis sorted sets. Clients never send scores, only submissions.
- Private entries carry a visibility flag; the hub renders them as Anonymous to everyone except the owner and moderators.
- Spectators subscribe read-only; presence and fan-out use Redis pub/sub with per-room sharding.

**Points and prize pools (Rewards)**

- Double-entry immutable ledger: every movement is two rows (debit, credit) in one transaction with an idempotency key. Balances are derived, with a cached projection.
- Prize pools are accounts with a cap. Contributions debit the contributor and credit the pool. Settlement is a Temporal workflow: freeze pool, compute payouts from final standings, post ledger entries, notify winners. Retries cannot double-pay because of idempotency keys.
- Redemption (PayPal, gift card, Pro subscription, course voucher) runs as a workflow with fraud checks, holds, and manual review above thresholds. The real-money track stays behind a Phase 2 feature flag.

**AI Tutor and code assistant**

- Requests go through the AI Gateway: it attaches lesson and code context, enforces plan token quotas (the Pro 5,000 token meter), strips secrets, logs prompts and responses for abuse review, and streams tokens over SSE.
- Tutor output never executes automatically. Suggested code runs only through the Execution Gateway like any other code.

**Learning and progression**

- XP events flow through the bus. A progression worker applies tier thresholds (1,200 / 4,000 / 8,000 / 15,000 / 25,000 / 50,000 XP in the prototype), streaks, and achievements, then emits tier-up notifications.
- Lesson delivery uses signed CDN URLs per format; progress is stored per lesson with resume position.

### 5.3 Data model highlights

- Core tables: tenants, users, memberships, profiles, privacy\_settings, tiers, courses, lessons, lesson\_progress, challenges, submissions, battles, battle\_entries, tournaments, brackets, ledger\_accounts, ledger\_entries, pools, redemptions, questions, answers, mentor\_sessions, jobs, applications, subscriptions, usage\_meters, notifications, audit\_log.
- Partition high-volume tables (submissions, ledger\_entries, events, audit\_log) by month.
- Leaderboards: Redis sorted sets for live ranking, Postgres as source of truth, rebuilt nightly. Rank history for the Change column comes from daily snapshots.
- Analytics: events stream to ClickHouse; the heatmap and XP charts read materialized views.

### 5.4 Multi-tenancy

- Consumer users live in a public tenant; Enterprise orgs are separate tenants with their own leaderboards, challenges, seats, and SSO.
- The DAL sets app.tenant\_id and app.user\_id per transaction; RLS policies key off those settings. Cross-tenant reads (global leaderboard, public portfolio) go through explicit, audited views.

### 5.5 Reliability and scale targets

- Availability: 99.9% for the API, 99.5% for sandboxes. Degrade gracefully: if judging is saturated, queue with a visible ETA.
- Capacity baseline: 4,200 concurrent coders, 50 concurrent battles of up to 100 entrants, 500 sandbox runs per second at peak with warm pools.
- RPO 5 minutes, RTO 1 hour. Multi-AZ Postgres with PITR; cross-region backup copies.

## 6. Security Measures

**Identity and access**

- OIDC with PKCE for all clients; passkeys and TOTP; short-lived access tokens (10 min), rotating refresh tokens bound to device.
- RBAC (learner, mentor, recruiter, org admin, moderator, platform admin) plus ABAC for tenant and visibility rules. Admin routes require step-up MFA and are IP-restricted.
- Enterprise: SAML SSO and SCIM provisioning.

**Service-to-service**

- mTLS everywhere (service mesh). The gateway strips any inbound internal headers and signs the ones it sets; services verify the signature and reject unsigned traffic.
- The DAL is the only component with database credentials (dynamic, short-lived, from Vault).

**Data protection**

- TLS 1.3 in transit; AES-256 at rest with KMS-managed keys; field-level encryption for payout details and PII.
- Privacy controls enforced server-side: anonymous leaderboard entries, recruiter contact opt-in, private challenge history, discreet questions (visible only to the asker and assigned mentor).
- Data export and account deletion workflows (GDPR/CCPA), with retention policies and tombstoned ledger rows (financial records are kept, identity is detached).

**Code execution safety**

- No network, read-only root filesystem, seccomp allowlist, dropped capabilities, cgroup limits, and no shared kernel between untrusted runs in the Firecracker tier.
- Per-user and per-IP execution quotas; abuse detection for crypto mining and fork bombs.
- Judging is deterministic: test cases and resource limits decide the verdict. No LLM decides whether code is safe or correct.

**Application security**

- Input validation via Pydantic schemas; output encoding; strict CSP; CSRF protection for cookie flows; CORS allowlist.
- Rate limiting by user, IP, and route class (auth, run, AI, redeem). Bot protection on signup and redemption.
- Anti-cheat: plagiarism similarity checks on submissions, device signals, collusion detection in battles, moderator review queue.
- Webhook signature verification (Stripe, PayPal); replay protection on all idempotent endpoints.

**Payments and rewards integrity**

- Ledger invariants checked continuously (debits equal credits, no negative balances). Daily reconciliation against Stripe and PayPal.
- Redemption velocity limits, KYC for the real-money track, and holds on new accounts.

**Supply chain and operations**

- Signed images (Cosign), SBOMs, dependency and secret scanning in CI, admission policies blocking unsigned or root containers.
- Immutable audit log for admin actions and ledger-affecting operations. Pen test before public launch and annually after; bug bounty after GA.
- Incident response runbooks, on-call rotation, breach notification procedure.

## 7. Full Implementation Plan: Wiring Backend to Frontend

The prototype renders everything from hard-coded arrays inside template literals. Wiring means turning those arrays into API calls and the page templates into components.

### Phase 0: Foundations (weeks 1-2)

- Create the monorepo, CI, environments (dev, staging, prod), Terraform baseline, Vault, Postgres, Redis, NATS.
- Write the first OpenAPI contracts for identity, learning, challenges. Generate the TypeScript SDK.
- Implement the gateway, DAL skeleton, RLS migration linter, observability stack.

### Phase 1: Identity and shell (weeks 3-4)

- Keycloak realm, GitHub and Google login, sign-up and onboarding persisted (experience level, goal, languages, weekly hours).
- Port the app shell (header, sidebar, theme toggle, router, global search) to React. Replace navigate() with real routes and deep links.
- Settings and privacy toggles bound to privacy\_settings.

### Phase 2: Learning and progression (weeks 5-7)

- Courses, lessons, progress, XP, streaks, tier thresholds, achievements.
- Dashboard, Learning Center, Courses, Progression, Profile (heatmap from the analytics endpoint).

### Phase 3: Execution and challenges (weeks 8-11)

- Execution Gateway, gVisor pool, language images, harness.
- Playground Run button calls the real runner; output streams back.
- Challenges list, entry, submission, verdicts, solo leaderboard.

### Phase 4: Competition (weeks 12-15)

- Battles hub (WebSockets), server timer, scoreboard, private entry flag, Firecracker tier.
- Tournaments with brackets (Temporal), live bracket view, spectator mode.
- Global leaderboards with Redis, anonymous visibility, nearest rivals, rank change snapshots.

### Phase 5: Rewards and billing (weeks 16-19)

- Ledger, prize pools, contributions, settlement workflow, redemptions (points track only).
- Stripe plans, usage meters (AI tokens, executions), invoices, entitlement middleware (fail-open on lookup failure).

### Phase 6: Community, mentors, careers, AI (weeks 20-24)

- Q&A with open and discreet modes, votes, accepted answers, reputation.
- Mentor marketplace, availability, bookings, payments in points.
- Jobs, recruiter views, applications, recruiter interest feed.
- AI Gateway: tutor sessions with history, playground assistant, recommended next topic.

### Phase 7: Enterprise, analytics, admin (weeks 25-28)

- Org tenants, seats, SSO, team leaderboards, team challenges.
- Analytics dashboards (ClickHouse), moderation queue, platform config flags (AI on/off, real-money track, registrations, maintenance mode).

### Phase 8: Hardening and launch (weeks 29-32)

- Load and chaos tests, pen test, DR drill, accessibility pass, beta, staged rollout with canaries.

### Page-to-endpoint map

| Prototype page | Primary endpoints |
| --- | --- |
| Dashboard | GET /me/summary, GET /challenges?status=active, GET /learning/continue, GET /tournaments/upcoming |
| Profile / Portfolio | GET /users/{handle}, GET /users/{handle}/activity, GET /users/{handle}/solutions, PATCH /me |
| Learning / Courses | GET /courses, GET /courses/{id}, POST /lessons/{id}/progress, POST /courses/{id}/enroll |
| Playground | POST /runs, GET /runs/{id}/stream (SSE), POST /snippets |
| AI Tutor | POST /ai/sessions, POST /ai/sessions/{id}/messages (SSE), GET /ai/sessions |
| Challenges | GET /challenges, POST /challenges, POST /challenges/{id}/entries, POST /entries/{id}/submissions |
| Live Battles | WSS /battles/{id} (scoreboard, timer, chat), GET /battles/{id}/problem |
| Tournaments | GET /tournaments, POST /tournaments/{id}/register, GET /tournaments/{id}/bracket |
| Leaderboards | GET /leaderboards/{scope}, GET /me/rank, PUT /me/leaderboard-visibility |
| Progression | GET /me/progression, GET /me/achievements |
| Rewards / Prize Pools | GET /rewards/balance, GET /rewards/transactions, POST /redemptions, GET /pools, POST /pools/{id}/contributions |
| Community | GET /questions, POST /questions (mode: open or discreet), POST /questions/{id}/answers, POST /votes |
| Mentors | GET /mentors, POST /mentors/{id}/bookings |
| Jobs | GET /jobs, POST /jobs/{id}/applications, GET /me/recruiter-interest |
| Enterprise | GET /orgs/{id}/members, GET /orgs/{id}/leaderboard, POST /orgs/{id}/challenges |
| Analytics | GET /me/analytics/{metric} |
| Notifications | GET /notifications, POST /notifications/read, WSS /notifications/stream |
| Billing | GET /billing/plan, POST /billing/checkout, GET /billing/usage, GET /billing/invoices |
| Settings | GET/PATCH /me/settings, DELETE /me |
| Admin | GET /admin/flags, POST /admin/moderation/{id}/resolve, PUT /admin/config |

### Frontend wiring rules

- Generated SDK only; no hand-written fetch calls. TanStack Query for caching, optimistic updates for votes and toggles.
- Every list page gets loading, empty, and error states (the prototype has only the happy path).
- Realtime channels reconnect with backoff and resume from the last event id.
- Feature flags from /admin/flags gate Phase 2 features such as the real-money track.
- Keep the prototype's design tokens as a shared theme package so web, desktop, and mobile stay visually aligned.

## 8. Testing Plan Checklist

**Unit and component**

- Domain logic in each service (XP and tier math, streaks, scoring, prize split, entitlement rules) at 85%+ coverage.
- Frontend components and hooks with Vitest and Testing Library.

**Database**

- Every migration runs forward and backward on a copy of production-shaped data.
- pgTAP tests: for each table, user A cannot read or write tenant B rows; anonymous leaderboard rows never expose identity.
- CI linter blocks any table lacking tenant\_id and an RLS policy.

**Contract and integration**

- OpenAPI lint (Spectral) and breaking-change detection on every PR.
- Pact consumer-provider tests between SDK consumers and services.
- Testcontainers integration tests per service (Postgres, Redis, NATS).
- Webhook tests with Stripe and PayPal sandboxes: duplicate, out-of-order, and forged events.

**Rewards and money**

- Ledger invariants: debits equal credits, no negative balances, idempotent retries do not double-post.
- Prize settlement under crash and retry (kill workers mid-workflow).
- Redemption limits, holds, and fraud rules.

**Execution and sandbox**

- Escape attempts: fork bomb, memory bomb, disk fill, network egress, /proc and kernel probes, symlink tricks, timing side channels.
- Limit enforcement: CPU, memory, wall time, output size per language image.
- Determinism: the same submission yields the same verdict across 100 runs.
- No data leakage between consecutive sandbox users.

**Realtime**

- Battle clock accuracy and server authority; client clock tampering ignored.
- Reconnect and resume; scoreboard consistency under 100 entrants and 1,000 spectators.
- Anonymous entries stay anonymous in every payload, including spectator and replay.

**Security**

- SAST (Semgrep, CodeQL), dependency and container scans, secret scanning on every PR.
- DAST (ZAP) against staging; API fuzzing with Schemathesis.
- AuthZ matrix tests: each role against each endpoint (IDOR, privilege escalation, tenant hopping).
- Forged internal-header tests: direct service calls without the gateway signature are rejected.
- Pen test before launch; retest after fixes.

**AI**

- Quota enforcement and token metering accuracy.
- Prompt injection tests (lesson content and user code that try to exfiltrate prompts or tool access).
- Quality evals on a fixed question set (correctness, pedagogy, no solution dumping in challenge mode).

**Performance and resilience**

- k6 load: 4,200 concurrent users baseline, 3x spike, 8-hour soak.
- Sandbox throughput at peak, including warm-pool exhaustion behavior.
- Chaos: kill pods, partition Redis, slow Postgres, drop NATS; verify graceful degradation and entitlement fail-open.
- Backup restore and regional failover drill each quarter.

**End-to-end and UX**

- Playwright flows: sign-up, onboarding, run code, enter and win a challenge, join a battle, redeem points, upgrade plan, change privacy.
- Accessibility (WCAG 2.2 AA), keyboard navigation, dark and light themes, responsive layouts.
- Cross-browser: Chrome, Safari, Firefox, Edge.

**Release gates**

- All suites green, zero critical or high vulnerabilities, migration dry run passed, canary healthy for 30 minutes, rollback tested.

## 9. Cross-Platform Backend Plan: Desktop (Windows, macOS, Linux)

**Approach:** one codebase using Tauri 2 (Rust shell, system webview) wrapping the React app. Electron is the fallback if webview differences cause problems.

**Backend responsibilities**

- Same public REST, SSE, and WebSocket APIs as web; no desktop-only backend. Add client\_type and app\_version headers for analytics and compatibility gating.
- Auth: OIDC with PKCE using the system browser and a custom URI scheme (codefull://) or loopback redirect; refresh token in the OS keychain through the Tauri keyring plugin.
- Update service: signed update manifests per channel (stable, beta) served from the CDN; the Tauri updater verifies the signature.
- Minimum-version endpoint so the backend can force upgrades after breaking changes.
- Offline mode: local SQLite cache of enrolled lessons, drafts, and playground files; a sync queue replays writes with idempotency keys on reconnect.
- Optional local runner: the playground can run code on-device with a bundled or user-installed toolchain for offline practice. Local runs never count for challenges or rewards; only server-side judging does.

**Platform notes**

- Windows: MSIX or signed MSI, Authenticode signing, WebView2 bootstrapper.
- macOS: universal binary, Developer ID signing, notarization, hardened runtime.
- Linux: AppImage, .deb, .rpm, and Flatpak; libsecret for token storage.
- CI builds all three targets on native runners; artifacts are signed and published to the update feed.

**Delivery:** 6 to 8 weeks after the web app reaches Phase 5.

## 10. Cross-Platform Backend Plan: Mobile (Android, iOS)

**Approach:** React Native with Expo (shares TypeScript, the generated SDK, and design tokens with web). Flutter is the alternative if the team prefers a custom renderer.

**Backend responsibilities**

- Device registry: POST /devices registers platform, app version, and push token; supports multiple devices per user and revocation.
- Push: the notifications service delivers through FCM (Android) and APNs (iOS) with per-category preferences (challenge starting, rank change, answers, mentor session, recruiter interest). Quiet hours and batching are server-side.
- Auth: system-browser OIDC with PKCE and universal or app links; tokens in Keychain (iOS) and Keystore-backed secure storage (Android); optional biometric unlock.
- Attestation: App Attest (iOS) and Play Integrity (Android) verified at login and before redemptions, to block emulators and tampered builds.
- Offline: local SQLite for lessons and drafts, background sync with idempotency keys, resumable media downloads.
- Realtime: WebSockets for battles with foreground-only subscription; push for background events.
- Billing: store rules apply to digital subscriptions. Add store receipt validation endpoints (App Store Server API, Google Play Developer API) feeding the same entitlements table as Stripe. Redeeming points for cash or gift cards, and any prize competition, must be reviewed against App Store and Google Play policies for real-money and skill-based contests before the Phase 2 track ships on mobile.
- Deep links: challenge, battle, tournament, and profile URLs resolve in-app.

**Release engineering:** EAS Build or Fastlane, staged rollouts, crash reporting (Sentry), remote config for kill switches.

**Delivery:** 8 to 10 weeks after the web app reaches Phase 5.

## 11. Native Backend Plan: Desktop (Windows, macOS, Linux)

Choose native only where platform integration justifies the cost (editor performance, OS-level integrations, power users). The backend contract is identical; only the generated SDKs differ.

| Platform | Stack | Platform-specific backend integration |
| --- | --- | --- |
| Windows | C# / .NET 8, WinUI 3, generated C# SDK (Kiota or NSwag) | Windows Credential Manager for tokens, toast notifications via Windows App SDK (backed by the shared push service), MSIX auto-update, jump lists, Windows Hello for step-up auth, WebView2 for rich lesson content |
| macOS | Swift 5.10, SwiftUI + AppKit, generated Swift SDK (swift-openapi-generator) | Keychain, APNs for macOS, Sparkle updates, notarized distribution, Touch ID for step-up auth, Spotlight and menu bar integrations, native code editor view (TextKit 2 or embedded Monaco in WKWebView) |
| Linux | Rust + GTK4/libadwaita (or Qt 6), generated Rust SDK (progenitor) | libsecret / Secret Service for tokens, freedesktop notifications, Flatpak and Snap packaging with portal-based file access, systemd user service for background sync |

**Shared native-desktop backend work**

- Publish protobuf and OpenAPI specs and generate SDKs in CI for C#, Swift, and Rust; version SDKs with the API.
- Local-first data layer per platform (SQLite via EF Core, GRDB, rusqlite) with one sync protocol: change log with client-generated ids; server-side conflict rules (last write wins for drafts, server wins for scores and ledger).
- Native code editor with LSP support against a local language server for offline editing; anything scored still executes server-side.
- Per-platform update channels, crash reporting, and telemetry opt-in consistent with privacy settings.
- Cost note: three native desktop apps triple QA and release effort. Recommended sequence: ship Tauri first, then go native on the platform with the most paying users.

## 12. Native Backend Plan: Mobile (Android, iOS)

| Platform | Stack | Platform-specific backend integration |
| --- | --- | --- |
| Android | Kotlin, Jetpack Compose, Ktor/Retrofit + generated Kotlin SDK, Room, WorkManager, Hilt | FCM push, Keystore-backed tokens, Credential Manager (passkeys), Play Billing 6+ with server-side purchase verification, Play Integrity, App Links, WorkManager background sync, widgets for streak and next challenge |
| iOS | Swift 5.10, SwiftUI, URLSession with async/await + generated Swift SDK, SwiftData or GRDB | APNs (token-based auth), Keychain, passkeys via ASAuthorization, StoreKit 2 with App Store Server Notifications v2 webhook, App Attest, Universal Links, BGTaskScheduler sync, Live Activities for live battle timers, WidgetKit |

**Backend additions for native mobile**

- Store webhook handlers: Apple App Store Server Notifications and Google Real-time Developer Notifications update entitlements; reconcile daily against the store APIs.
- Push service supports rich and silent pushes, Live Activity updates (iOS), and notification channels (Android) mapped to server preference categories.
- Battle client protocol: compact messages over WebSocket with sequence numbers, resume tokens, and server time sync so native timers match the authoritative clock.
- Media: HLS with optional DRM offline downloads (FairPlay, Widevine) for lessons; signed, expiring segments.
- Code editing on phones: native editor component with syntax highlighting and a snippet keyboard; run requests go to the same Execution Gateway with a mobile rate profile.
- Release: TestFlight and Play internal tracks, staged rollouts, forced-upgrade endpoint, remote config.

**Decision guide**

- Start cross-platform (Tauri and React Native) to reach all five platforms from one TypeScript codebase.
- Go native on mobile if Live Activities, widgets, offline media DRM, or editor performance become differentiators, or if store review demands native-quality behavior.
- Keep one backend, one contract, generated SDKs, and shared design tokens regardless of client technology.

## 13. Risks and Open Decisions

- **Real-money rewards:** legal review (skill-contest and sweepstakes law by region, tax reporting, KYC) before enabling the Phase 2 track; mobile store policy review in parallel.
- **Sandbox cost:** Firecracker capacity is the largest infrastructure cost; size warm pools from load tests and reserve the hardened tier for competitions.
- **Prototype debt:** the prototype is a single HTML file with inline templates, so the port to components is real work and should be planned, not assumed.
- **Open questions:** hosting cloud (AWS, GCP, Azure), data residency requirements for Enterprise, managed or self-hosted Keycloak, and which two languages ship first in the sandbox (suggest Python and JavaScript, then Go, C++, Java, Rust).
