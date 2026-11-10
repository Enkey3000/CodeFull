# CodeFull Software Requirements Specification (SRS)

**Doc ID:** SRS-001 | **Version:** 0.1 draft | **Status:** for review | **Owner:** Product + Tech lead **Upstream:** PRD-001 | **Downstream:** ARCH-001, SEC-001, OpenAPI, Test Plan, Test Cases, RTM

## 1. Introduction

### 1.1 Purpose and scope

This SRS states what CodeFull must do, in testable terms. It covers the web application and the backend services; desktop and mobile clients consume the same behavior and add only the client-specific items in section 6.

### 1.2 Conventions

- **Requirement IDs:** FR-\<DOMAIN>-nnn for functional, NFR-nnn for non-functional, SEC-nnn for security (defined in SEC-001). Domains: IDN, LRN, EXE, CMP, RWD, COM, CAR, AI, BIL, PLT.
- **Priority:** M = Must, S = Should, C = Could.
- **Release:** MVP, FF (fast follow), P2 (Phase 2, flagged off by default).
- **Acceptance (AC):** written as Given / When / Then in short form. Every Must requirement has at least one test case.
- **Keywords:** shall = mandatory; should = recommended; may = optional.

### 1.3 References

PRD-001, Backend Plan, Documentation Plan, interactive prototype, cursorrules.md, cursorsecurityrules.md.

## 2. System Context and Actors

| Actor | Description |
| --- | --- |
| Learner, Competitor (PER-01, PER-02) | End users on web, desktop, or mobile |
| Mentor (PER-03) | User with Advanced tier or above who opts in |
| Recruiter (PER-04) | Verified account with consent-based access to profiles |
| Org admin (PER-05) | Manages an Enterprise tenant |
| Moderator / admin (PER-06) | Operates moderation, flags, configuration |
| Identity provider | OIDC provider with GitHub and Google federation |
| Payment providers | Stripe (subscriptions), PayPal (payouts, P2), app stores |
| AI provider | Language model accessed only through the AI Gateway |
| Push and email services | FCM, APNs, transactional email |

## 3. Functional Requirements

### 3.1 Identity and privacy (IDN)

| ID | Requirement and acceptance | Pri | Rel |
| --- | --- | --- | --- |
| FR-IDN-001 | The system shall let a user register with email and password. AC: Given a new valid email, when the user submits, then an account is created and a verification email is sent; duplicate emails are rejected. | M | MVP |
| FR-IDN-002 | The system shall support GitHub and Google sign-in. AC: Given a linked provider account, when the user chooses it, then they are signed in or an account is created. | M | MVP |
| FR-IDN-003 | The system shall run onboarding capturing experience level, primary goal, known languages, and weekly hours. AC: Given a new user, when onboarding is completed or skipped, then answers are stored and the first recommendation reflects them. | M | MVP |
| FR-IDN-004 | The system shall provide a profile with display name, bio, location, skills, and tier. AC: Given the owner edits and saves, then changes show on the profile within 5 s; display names are unique and 3 to 30 characters. | M | MVP |
| FR-IDN-005 | The system shall provide privacy controls: show on leaderboard, allow recruiter contact, public challenge history, show points balance. AC: Given a control is off, then the corresponding data is absent from every API response and UI for other users. | M | MVP |
| FR-IDN-006 | The system shall support TOTP and passkey MFA; MFA shall be required for admins. AC: Given MFA is enrolled, when signing in, then a second factor is required. | M | MVP |
| FR-IDN-007 | The system shall let a user export their data and delete their account. AC: Given a delete request is confirmed, then personal data is removed or detached within 30 days; ledger rows are retained without identity. | M | MVP |
| FR-IDN-008 | The system shall publish an opt-in public portfolio at a stable URL. AC: Given the portfolio is public, then featured solutions, stats, and skills are visible without sign-in; turning it off returns 404. | S | FF |
| FR-IDN-009 | The system shall support Enterprise tenants with SAML SSO and SCIM provisioning. AC: Given a configured IdP, when a user is added in SCIM, then they can sign in via SSO into the org tenant. | S | P2 |
| FR-IDN-010 | The system shall list active sessions and devices and allow revocation. AC: Given a revoked session, then its tokens are rejected within 60 s. | S | FF |

### 3.2 Learning and progression (LRN)

| ID | Requirement and acceptance | Pri | Rel |
| --- | --- | --- | --- |
| FR-LRN-001 | The system shall organize learning in six tiers: Beginner, Intermediate, Advanced, Expert, Master, Guru. AC: Given a user, then their current tier and progress toward the next are visible. | M | MVP |
| FR-LRN-002 | The system shall provide a course catalog with enrollment. AC: Given a course, when the user enrolls, then it appears in their Continue Learning list. | M | MVP |
| FR-LRN-003 | Each lesson shall be available as video (captioned), audio (with transcript), interactive, and text where authored. AC: Given a lesson with multiple formats, then the user can switch format and keep progress. | M | MVP |
| FR-LRN-004 | The system shall store lesson progress and resume position. AC: Given a user leaves mid-lesson, when they return on any device, then they resume within 10 s of the last position. | M | MVP |
| FR-LRN-005 | The system shall award XP for verified learning events and promote tiers when the per-tier XP threshold is met (surplus XP carries into the next tier). AC: Given XP reaches the tier threshold, then the tier advances once, a notification is created, and the event is idempotent. | M | MVP |
| FR-LRN-006 | The system shall track daily streaks and apply a points multiplier up to 2x. AC: Given a qualifying activity each UTC-adjusted user day, then the streak increments; a missed day resets it. | M | MVP |
| FR-LRN-007 | The system shall grant achievements with rarity levels. AC: Given criteria are met, then the badge is awarded once and shown on the profile. | S | MVP |
| FR-LRN-008 | The system shall support weekly lesson goals. AC: Given a goal of N lessons, then progress shows X of N and resets weekly. | S | MVP |
| FR-LRN-009 | The system shall recommend next topics using progress and skills (see FR-AI-005). | S | MVP |
| FR-LRN-010 | Interactive exercises shall run in the browser through the execution service. AC: Given an exercise, when the user runs it, then results display per FR-EXE-001. | M | MVP |
| FR-LRN-011 | The system shall issue course completion certificates. AC: Given 100% completion, then a verifiable certificate URL is issued. | C | FF |
| FR-LRN-012 | Desktop and mobile clients shall cache enrolled lessons for offline use and sync progress on reconnect. AC: Given offline progress, when online, then it merges without loss using idempotency keys. | S | FF |

### 3.3 Code execution (EXE)

| ID | Requirement and acceptance | Pri | Rel |
| --- | --- | --- | --- |
| FR-EXE-001 | The playground shall run user code and stream stdout, stderr, runtime, and memory. AC: Given valid Python code, when Run is pressed, then first output appears within the NFR-003 target and the run is recorded. | M | MVP |
| FR-EXE-002 | MVP languages shall be Python 3.12 and JavaScript; later Go, Java, C++, Rust. AC: Given an unsupported language, then the UI hides it or marks it unavailable. | M | MVP |
| FR-EXE-003 | Every run shall execute in an isolated sandbox with CPU, memory, process, wall-time, and output limits and no network. AC: Given code that opens a socket, then it fails; given an infinite loop, then it terminates at the time limit with a clear message. | M | MVP |
| FR-EXE-004 | Users shall save, name, and share snippets. AC: Given a share link, then viewers can read and fork but not edit. | S | MVP |
| FR-EXE-005 | Challenge submissions shall be judged against hidden test cases with per-case verdicts and aggregate score. AC: Given the same submission, then the verdict is identical across repeated runs. | M | MVP |
| FR-EXE-006 | Execution and challenge quotas shall follow the user's plan. AC: Given the Free limit of 100 playground and challenge executions is reached (interactive lesson exercises do not count toward this limit), then further runs are refused with an upgrade message (see FR-BIL-007 for fail-open on lookup errors). | M | MVP |
| FR-EXE-007 | Users shall see run history. AC: Given past runs, then the last 50 show time, language, status, and duration. | S | MVP |
| FR-EXE-008 | Competition-grade runs shall use the hardened isolation tier. AC: Given a battle submission, then it runs in the hardened tier. | M | FF |

### 3.4 Competition (CMP)

| ID | Requirement and acceptance | Pri | Rel |
| --- | --- | --- | --- |
| FR-CMP-001 | The system shall list challenges with filters for mode, language, tier, and status, plus search. AC: Given filters, then results match all selected filters and show prize, entrants, and time left. | M | MVP |
| FR-CMP-002 | A user shall enter a solo challenge and submit solutions within the allowed window. AC: Given an open challenge within quota, when entering, then an entry exists; submitting after the close is rejected. | M | MVP |
| FR-CMP-003 | On verdict the system shall award points according to the challenge rules and publish the result. AC: Given a win, then exactly one ledger posting is made (idempotent) and the dashboard reflects it. | M | MVP |
| FR-CMP-004 | Eligible users and org admins shall create challenges, subject to moderation before publication. AC: Given a draft, then it is not public until approved. | S | FF |
| FR-CMP-005 | Entrants shall choose public or private entry. AC: Given a private entry, then other users, spectators, and recruiters see Anonymous with a lock indicator. | M | MVP |
| FR-CMP-006 | The system shall maintain a global leaderboard ranked by Competition Score (lifetime points earned from challenges, battles, and tournaments; never reduced by spending), showing rank, tier, competition score, win-loss, and rank change. AC: Given a score change, then the leaderboard reflects it within 5 s. | M | MVP |
| FR-CMP-007 | Leaderboards shall also exist by week, language, region, and friends. AC: Given a scope tab, then only matching users appear. | S | FF |
| FR-CMP-008 | Users shall join live battles through a lobby with capacity limits. AC: Given a full battle, then joining is refused and a waitlist or alternative is offered. | M | FF |
| FR-CMP-009 | Battles shall use a server-authoritative clock and live scoreboard. AC: Given a client with a wrong clock, then scoring and cutoffs are unaffected; scoreboard updates propagate within NFR-006. | M | FF |
| FR-CMP-010 | Spectators shall watch battles read-only. AC: Given a spectator, then they receive scoreboard and activity events but cannot submit. | S | FF |
| FR-CMP-011 | The system shall run bracket tournaments with registration, seeding, rounds, and results. AC: Given a full bracket, then matches are scheduled and winners advance automatically. | S | FF |
| FR-CMP-012 | The system shall support team events with team scoring. AC: Given a team entry, then member contributions aggregate under the team rules. | C | FF |
| FR-CMP-013 | The system shall flag suspected plagiarism and collusion for moderator review. AC: Given similarity above threshold, then the submission enters the review queue; no permanent ban occurs without a moderator decision. | M | FF |
| FR-CMP-014 | The system shall keep daily rank snapshots to show rank change. AC: Given a snapshot history, then the Change column shows the delta against the prior week. | S | MVP |

### 3.5 Rewards (RWD)

| ID | Requirement and acceptance | Pri | Rel |
| --- | --- | --- | --- |
| FR-RWD-001 | The system shall maintain an append-only double-entry points ledger. AC: Given any posting, then debits equal credits and no row is updated or deleted. | M | MVP |
| FR-RWD-002 | Points shall be earned per the rules in section 8 (lessons, answers, streaks, challenges, tournaments, daily challenge). AC: Given a qualifying event, then points post once with a source reference. | M | MVP |
| FR-RWD-003 | Users shall see balance, lifetime earned, and transaction history. AC: Given a posting, then it appears in history within 5 s. | M | MVP |
| FR-RWD-004 | The system shall support prize pools with caps and contributions. AC: Given contributions reaching the cap, then further contributions are refused. | S | FF |
| FR-RWD-005 | The system shall settle prize pools to winners automatically from final standings. AC: Given a repeated settlement attempt, then no double payout occurs. | M | FF |
| FR-RWD-006 | Users shall redeem points for a Pro subscription month or a course voucher. AC: Given sufficient balance, then points are debited and entitlement is granted atomically. | S | FF |
| FR-RWD-007 | Cash and gift-card redemption shall exist only behind the real-money flag, with KYC, limits, and review. AC: Given the flag is off, then no cash redemption route is reachable. | S | P2 |
| FR-RWD-008 | The system shall apply fraud and velocity controls to earning and redemption. AC: Given abnormal earn or redeem rates, then the action is held for review. | M | MVP |
| FR-RWD-009 | The system shall reconcile ledger totals daily and alert on any invariant violation. AC: Given a mismatch, then on-call is paged. | M | MVP |

### 3.6 Community and mentors (COM)

| ID | Requirement and acceptance | Pri | Rel |
| --- | --- | --- | --- |
| FR-COM-001 | Users shall post open questions with tags and topic. AC: Given a posted question, then it appears in the feed and is searchable. | M | MVP |
| FR-COM-002 | Users shall post discreet questions visible only to the asker and an assigned mentor. AC: Given a discreet question, then it never appears in feeds, search, or counts for other users. | M | MVP |
| FR-COM-003 | Users shall answer, vote, and the asker shall accept an answer. AC: Given acceptance, then the answerer receives points once. | M | MVP |
| FR-COM-004 | The system shall compute reputation from accepted answers and votes. AC: Given events, then reputation updates and rankings reflect it. | S | MVP |
| FR-COM-005 | Mentors shall list availability and rates; learners shall book sessions. AC: Given an available slot, when booked, then both parties are notified and the slot is held. | S | FF |
| FR-COM-006 | Session payments shall use points held in escrow and released on completion. AC: Given a cancelled session, then points are returned per policy. | S | FF |
| FR-COM-007 | Users shall flag content; moderators shall resolve flags with audited actions. AC: Given a resolved flag, then an audit record exists with actor and reason. | M | MVP |
| FR-COM-008 | Users shall be notified of answers, acceptances, and bookings. | S | MVP |

### 3.7 Careers (CAR)

| ID | Requirement and acceptance | Pri | Rel |
| --- | --- | --- | --- |
| FR-CAR-001 | The system shall list jobs with filters and required tier. AC: Given a job requiring Expert, then lower-tier users see it as locked or informational. | S | FF |
| FR-CAR-002 | Recruiters shall see only profiles whose owners enabled recruiter visibility. AC: Given visibility off, then the profile never appears in recruiter views. | M | FF |
| FR-CAR-003 | Users shall apply to jobs and track status. | S | FF |
| FR-CAR-004 | Users with recruiter visibility shall see a feed of recruiter interest (views, shortlists, messages). AC: Given a recruiter action, then it appears within 1 minute. | S | FF |
| FR-CAR-005 | Recruiter accounts shall be verified before access. | M | P2 |

### 3.8 AI assistance (AI)

| ID | Requirement and acceptance | Pri | Rel |
| --- | --- | --- | --- |
| FR-AI-001 | The tutor shall hold multi-turn sessions with history and lesson context. AC: Given a prior session, then it can be reopened with its messages. | M | MVP |
| FR-AI-002 | The playground assistant shall explain and suggest improvements for the current code. AC: Given code, then suggestions appear without running them. | S | MVP |
| FR-AI-003 | AI usage shall be metered and capped per plan. AC: Given the cap is reached, then requests are refused with the usage shown. | M | MVP |
| FR-AI-004 | In challenge mode the AI shall not provide full solutions. AC: Given an active challenge, then tutor responses are hints only (verified by eval suite). | M | MVP |
| FR-AI-005 | The system shall recommend next topics and challenges. | S | MVP |
| FR-AI-006 | Users shall rate and report AI responses. AC: Given a report, then it enters the moderation queue with the transcript. | S | MVP |

### 3.9 Billing (BIL)

| ID | Requirement and acceptance | Pri | Rel |
| --- | --- | --- | --- |
| FR-BIL-001 | The system shall offer Free, Starter, Pro, and Enterprise plans with defined limits. | M | MVP |
| FR-BIL-002 | Users shall subscribe through Stripe Checkout. AC: Given a successful payment, then entitlements update within 30 s. | M | MVP |
| FR-BIL-003 | The system shall show usage meters (AI tokens, executions, challenge entries). | M | MVP |
| FR-BIL-004 | The system shall provide invoice history with downloadable PDFs. | S | MVP |
| FR-BIL-005 | Users shall change or cancel plans. AC: Given cancel, then access continues to period end. | M | MVP |
| FR-BIL-006 | Mobile apps shall validate store receipts and map them to the same entitlements. | S | FF |
| FR-BIL-007 | If the entitlement or subscription lookup fails, the system shall allow the request and log it (fail open). AC: Given a billing outage, then paying users are not blocked; this never applies to points or money movement. | M | MVP |

### 3.10 Platform (PLT)

| ID | Requirement and acceptance | Pri | Rel |
| --- | --- | --- | --- |
| FR-PLT-001 | The system shall deliver in-app and email notifications with per-category preferences; push in FF. | M | MVP |
| FR-PLT-002 | The system shall provide global search across challenges, courses, coders, and Q&A. AC: Given a query, then results return per NFR-009. | S | MVP |
| FR-PLT-003 | Users shall see personal analytics (XP over time, language performance, challenge history). | S | FF |
| FR-PLT-004 | Admins shall moderate flagged content, disputes, and pending content. | M | MVP |
| FR-PLT-005 | Admins shall control platform flags: AI features, real-money track, registrations, maintenance mode. AC: Given a flag change, then it takes effect within 60 s and is audited. | M | MVP |
| FR-PLT-006 | The system shall write an immutable audit log of privileged and ledger-affecting actions. | M | MVP |
| FR-PLT-007 | Org admins shall see team leaderboards, team challenges, and org analytics. | S | P2 |
| FR-PLT-008 | The system shall offer a public API with keys and rate limits. | C | P2 |
| FR-PLT-009 | The UI shall support dark and light themes and respect system preference. | M | MVP |

## 4. Non-Functional Requirements

| ID | Category | Requirement | Measure |
| --- | --- | --- | --- |
| NFR-001 | Performance | API read latency | p95 under 300 ms at 4,200 concurrent users |
| NFR-002 | Performance | API write latency | p95 under 500 ms at 4,200 concurrent users |
| NFR-003 | Performance | Playground time to first output (warm pool, Python or JavaScript) | p95 under 2 s |
| NFR-004 | Performance | Typical challenge verdict (up to 10 test cases) | p95 under 10 s |
| NFR-005 | Performance | Web largest contentful paint | p75 under 2.5 s on a mid-range laptop over broadband |
| NFR-006 | Performance | Battle scoreboard propagation; client clock drift | p95 under 1 s; drift under 250 ms |
| NFR-007 | Performance | Leaderboard read | p95 under 200 ms |
| NFR-008 | Performance | AI tutor time to first token | p95 under 2 s |
| NFR-009 | Performance | Global search | p95 under 400 ms |
| NFR-010 | Performance | Notification delivery | In-app under 5 s; push under 30 s |
| NFR-011 | Scalability | Concurrent users | 4,200 baseline; 3x spike for 15 minutes |
| NFR-012 | Scalability | Live battles | 50 concurrent battles of up to 100 entrants and 1,000 spectators each |
| NFR-013 | Scalability | Sandbox throughput | 500 runs per second at peak with warm pools |
| NFR-014 | Availability | Uptime | API 99.9%, sandboxes 99.5% per month |
| NFR-015 | Recoverability | Disaster recovery | RPO 5 minutes, RTO 1 hour |
| NFR-016 | Reliability | Retries and degradation | Idempotent writes; if judging saturates, queue with visible ETA rather than fail |
| NFR-017 | Security | Controls and verification | As defined in SEC-001; every SEC item traced to a test |
| NFR-018 | Privacy | Compliance | GDPR and CCPA: export, deletion, consent, minimization |
| NFR-019 | Accessibility | Standard | WCAG 2.2 AA on all MVP screens |
| NFR-020 | Compatibility | Supported clients | Last 2 versions of Chrome, Safari, Firefox, Edge; Windows 10+, macOS 12+, Ubuntu 22.04+; Android 9+; iOS 16+ |
| NFR-021 | Usability | Responsive layout | Functional from 320 px width; drawer navigation under 860 px |
| NFR-022 | Observability | Telemetry | Traces, metrics, structured logs for every service; SLO dashboards and alerts |
| NFR-023 | Maintainability | Engineering quality | 85% coverage on domain logic; contract-first APIs; no critical lint or type errors |
| NFR-024 | Compliance | Payments | Card data never touches CodeFull systems (Stripe-hosted fields; PCI SAQ A scope) |
| NFR-025 | Data retention | Retention periods | Logs 90 days; audit log 7 years; submissions 12 months unless featured; deleted-account data within 30 days |
| NFR-026 | Localization | Languages | English at MVP; all strings externalized for later locales |

## 5. Data Requirements

| Entity | Key attributes | Classification | Notes |
| --- | --- | --- | --- |
| User, profile | handle, display name, bio, location, skills, tier, XP | Confidential | Handle unique and immutable after 30 days |
| Privacy settings | leaderboard visibility, recruiter contact, public history, show points | Confidential | Enforced in every read path |
| Lesson progress | lesson, format, position, completion | Internal | Syncs across devices |
| Challenge, entry, submission | mode, language, tier, prize, visibility, code, verdict, runtime | Confidential | Code retained per NFR-025 |
| Battle, scoreboard | entrants, clock, standings | Internal | Private entrants rendered anonymous |
| Ledger account, entry | account, amount, direction, source, idempotency key | Restricted | Append-only, partitioned monthly |
| Prize pool, redemption | pool, cap, contributors; option, amount, status, KYC state | Restricted | Payout details field-encrypted |
| Question, answer, vote | mode (open or discreet), tags, author, mentor assignment | Confidential | Discreet items access-restricted |
| Subscription, usage meter | plan, period, AI tokens, executions | Confidential | Provider ids stored, not card data |
| Audit log | actor, action, target, time, reason | Restricted | Immutable |

Every tenant-scoped record carries tenant\_id. Timestamps are stored in UTC.

## 6. Interface Requirements

**User interface.** Responsive web app following the CodeFull design tokens (logo-derived blue, navy, near-black, and white; dark and light themes); every data view has loading, empty, and error states; keyboard navigation and visible focus; no information conveyed by color alone.

**API.** Public REST (OpenAPI 3.1) plus SSE for run and AI streams and WebSocket for battles and notifications (AsyncAPI). Errors use RFC 9457 problem details. Mutating calls that could double an effect accept an Idempotency-Key. Lists use cursor pagination. All traffic over TLS 1.3.

**External systems.** Identity provider (OIDC), Stripe (checkout, webhooks, invoices), PayPal (P2 payouts), FCM and APNs, transactional email, AI provider (via AI Gateway only), app store server APIs.

**Desktop client additions.** Custom URI scheme codefull:// for sign-in redirect; OS keychain for refresh tokens; signed auto-update; offline cache with sync queue.

**Mobile client additions.** Push registration and preferences; universal and app links; secure storage; platform attestation before redemptions; store receipt validation; offline lessons and sync.

## 7. State Machines

**Submission:** draft -> queued -> running -> judged (passed, failed, partial) | error | timeout. A judged state is final; re-judging creates a new record.

**Battle:** scheduled -> lobby\_open -> live -> closing -> settled | cancelled. Clock and cutoffs are set by the server at live; late submissions are rejected in closing.

**Prize settlement:** open -> frozen -> computed -> posted -> notified. Each transition is idempotent; a failure retries from the last completed step; posted is final.

**Redemption:** requested -> held -> (approved | rejected | review) -> fulfilled | refunded. Funds move only on fulfilled or refunded; held reserves points.

**Tier progression:** the tier advances when XP in the current tier reaches its threshold; the transition fires once and emits a notification.

**Subscription:** trialing | active -> past\_due -> canceled | expired; entitlements follow the state with a grace period.

## 8. Business Rules

**Tier XP thresholds (XP to complete each tier; per tier, not cumulative, as decided in ECO-001):** Beginner 1,200; Intermediate 4,000; Advanced 8,000; Expert 15,000; Master 25,000; Guru 50,000.

**Points earning (governed by ECO-001; the ranges below are superseded by its tables):** lessons 10 to 50; accepted answer 5 to 20; daily challenge 25 guaranteed; challenge win 50 to 25,000 depending on prize; tournament win 100 to 10,000; streak multiplier up to 2x on eligible earnings.

**Redemption (planning values):** 100 points = $1 notional. Pro month 3,000 points; course voucher 500 points per premium course; gift card minimum 2,500 points; PayPal minimum 1,000 points (both P2).

**Plan limits:** Free 5 challenges per month and 100 executions; Starter 20 challenges per month, unlimited executions, 500 AI tokens; Pro unlimited challenges, 5,000 AI tokens, multiplayer; Enterprise by contract.

**Anonymity:** a private entry hides identity from all other users, spectators, and recruiters; moderators and the owner can see it; the choice can be changed for future entries and, where the rules allow, past ones.

**Ties:** equal scores are broken by earliest accepted submission time, then fewest attempts.

## 9. Constraints and Assumptions

- Code is executed only in managed sandboxes; no user-hosted runners.
- MVP languages are Python and JavaScript.
- Real-money features stay disabled until legal approval.
- Content volumes assumed: one deep track at MVP.
- Initial hosting region and data residency to be decided (open question in PRD-001).

## 10. Glossary

| Term | Meaning |
| --- | --- |
| Tier | One of six skill levels from Beginner to Guru |
| XP | Experience points that drive tier progression |
| Points | Redeemable currency earned through activity and prizes |
| Battle | Live multiplayer challenge on a shared server clock |
| Discreet question | Question visible only to the asker and an assigned mentor |
| Private entry | Competitive entry shown to others as Anonymous |
| DAL | Data Access Layer, the only component with database access |
| Execution Gateway | The only path to code sandboxes |
| Hardened tier | MicroVM-based isolation for competition-grade runs |

## 11. Traceability and Change Control

- Each FR cites its PRD goal (BG-nn) in the RTM; each Must FR needs a test case, and each SEC item a verification.
- Changes follow pull-request review with an impact note on OpenAPI, tests, and RTM.
- Open items: confirm XP threshold interpretation, final points economy, and plan limits before the SRS is baselined at v1.0.

## 12. Version 0.2 Changes (ECO-001 decisions approved)

The Product owner approved the decisions in ECO-001 (points economy). The earning, XP, catalog, funding, and ranking rules in ECO-001 govern wherever this document gives planning ranges.

### 12.1 Requirement changes

| ID | Change |
| --- | --- |
| FR-CMP-006 | Leaderboards rank by Competition Score (CS); the weekly board uses a 7-day window; CS is never reduced by spending or redemption; anonymity does not change CS or rank |
| FR-LRN-005 | XP thresholds are per tier; surplus XP carries into the next tier; total XP is the sum across tiers |
| FR-EXE-006 | Interactive lesson exercises do not count toward the Free plan execution quota; exercises have their own rate limit |
| FR-RWD-002 | Earning follows the ECO-001 tables (rates, daily caps, streak multiplier min(2.0, 1.0 + 0.05 x streak days) applied only to eligible sources) |
| Section 8 | Tier XP thresholds, points earning, redemption planning values, and prize splits are defined in ECO-001 |

### 12.2 New requirements

| ID | Requirement and acceptance | Pri | Rel |
| --- | --- | --- | --- |
| FR-RWD-010 | The system shall offer an in-app points catalog (profile frames and badges, premium practice packs, streak freezes) with prices from configuration. AC: Given sufficient points, when a user buys an item, then points are debited and the item unlocked in one transaction; repeating the request with the same idempotency key changes nothing. | S | MVP |
| FR-RWD-011 | Each user shall have two balance buckets, learning points (in-app use only) and prize points (eligible for redemption when Phase 2 opens); spending debits learning points first, then prize points. AC: Given a purchase larger than the learning bucket, then the remainder comes from prize points; if the total is insufficient, nothing is debited. | M | MVP |
| FR-RWD-012 | The system shall derive Competition Score from ledger entries flagged as competition (challenge completion, placement prizes, battles, tournaments). AC: Given spending or redemption, then CS does not change; given a challenge prize, then CS increases by the prize. | M | MVP |
| FR-RWD-013 | Prizes shall be funded, not minted: payouts debit a funded prize fund or pool account. AC: Given an unfunded prize fund, then the payout is rejected and an alert is raised. | M | FF |

### 12.3 UAT and API implications

- New UAT scenarios: UAT-038 (buy a catalog item and see balances) and UAT-039 (understand XP, points, and Competition Score on the dashboard and leaderboard).
- OpenAPI 0.2.0 separates xp\_total, learning and prize points, competition\_score, and reputation, adds catalog operations, and marks run context so lesson exercises are exempt from the execution quota.
- Test Cases v0.3 adds TC-0514 to TC-0524 covering these rules.
