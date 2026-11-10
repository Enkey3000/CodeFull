# CodeFull Product Requirements Document (PRD)

**Doc ID:** PRD-001 | **Version:** 0.1 draft | **Status:** for stakeholder sign-off | **Owner:** Product **Sources:** interactive prototype (26 surfaces), brand logo and palette, Backend Plan, Documentation Plan **Downstream:** SRS-001, ARCH-001, SEC-001, MVP Pattern, UAT Plan

## 1. Vision and Summary

CodeFull is the arena where coders become champions: a platform to learn programming from zero to expert, compete in solo and live multiplayer challenges, earn points and prizes, get help from mentors and an AI tutor, and be discovered by employers. Learning, competition, rewards, community, and careers reinforce each other in one loop:

```
Learn -> Practice (playground) -> Compete (challenges, battles) -> Earn (points, prizes)
   ^                                                                     |
   +---- Mentors, AI tutor, community <---- Rank and portfolio ----> Jobs
```

**Positioning:** comprehensive learning plus real competition plus real rewards, with privacy controls the learner owns (public or anonymous, open or discreet).

**Tagline:** Learn. Compete. Earn. Beginner to Guru, at your pace.

## 2. Problem Statement

| Problem | Who feels it | Today |
| --- | --- | --- |
| Learning platforms teach but do not motivate sustained practice | Beginners | Drop off after the first weeks |
| Competitive platforms assume prior skill and give little guidance | Intermediate coders | Frustration, quitting |
| Skill is hard to prove without credentials | Job seekers, career changers | Resumes without evidence |
| Learners fear public failure and judgment | Beginners | Do not ask questions or enter contests |
| Hiring on merit is hard to scale | Recruiters | Noisy applicant pools |
| Teams lack an engaging way to upskill | Enterprise managers | Low-engagement training |

## 3. Goals and KPIs

Targets are proposed starting points to validate with the first cohort; they are not commitments.

| ID | Goal | Metric | Proposed target |
| --- | --- | --- | --- |
| BG-01 | Activation | Share of signups who run code within 24 hours | 60% |
| BG-02 | Retention | Day-7 / Day-30 retention | 35% / 20% |
| BG-03 | Competitive engagement | Monthly active users entering at least one challenge | 30% |
| BG-04 | Monetization | Free-to-paid conversion of monthly actives (6 months after GA) | 4% |
| BG-05 | Community health | Questions receiving an answer within 24 hours | 50% |
| BG-06 | Career outcomes | Recruiter-learner connections per month (Phase 2) | tracked from launch |
| BG-07 | Trust and integrity | Fraudulent point awards; cross-tenant data incidents | under 0.1%; zero |
| BG-08 | Reach | Platforms live: web, desktop, mobile | web at MVP; desktop and mobile after |
| BG-09 | Enterprise | Paying organizations | 5 pilots within 6 months of Enterprise launch |

## 4. Personas

| ID | Persona | Needs | Key journeys |
| --- | --- | --- | --- |
| PER-01 | Learner (beginner) | Guided path, low pressure, quick wins, help when stuck | Onboard, first lesson, first run, ask AI or community |
| PER-02 | Competitor (intermediate to expert) | Fair challenges, live battles, rankings, prizes, privacy choice | Enter challenge, join battle, check rank, redeem points |
| PER-03 | Mentor (advanced and above) | Reach learners, earn points, manage availability | Set availability, accept bookings, answer questions |
| PER-04 | Recruiter | Find verified skill signals, contact consenting talent | Search talent, view portfolios, message, post jobs |
| PER-05 | Org admin (Enterprise) | Team upskilling, team challenges, analytics, SSO | Provision seats, run team challenge, view reports |
| PER-06 | Moderator / platform admin | Keep the platform fair and safe | Review flags, resolve disputes, manage flags and config |

## 5. Scope and Release Tiers

| Tier | Meaning |
| --- | --- |
| MVP | First public release; minimum to validate the learn-compete-earn loop |
| FF (fast follow) | Weeks to a few months after MVP; flagged until ready |
| P2 (Phase 2) | Requires legal, compliance, or major new capability; off by default |

| Domain | MVP | FF | P2 |
| --- | --- | --- | --- |
| Identity | Sign up, GitHub/Google login, onboarding, profile, privacy settings, export and delete | Public portfolio, MFA enrolment prompts, session management | Enterprise SSO and SCIM |
| Learning | One full track (Python, Beginner to Intermediate), four lesson formats, XP, tiers, streaks, achievements | More tracks and languages, certificates, offline cache | Guru-tier content, creator tools |
| Execution | Playground and judging for Python and JavaScript, saved snippets | Go, Java, C++, Rust; hardened tier | Local offline runner (non-scoring) |
| Competition | Solo challenges, global and weekly leaderboards, anonymous entries | Live battles, spectators, tournaments, team events | Seasonal leagues |
| Rewards | Points earning and ledger, balance and history, in-app points catalog (profile frames, practice packs, streak freezes) | Prize pools, redeem points for Pro or course vouchers | Cash and gift-card redemption (real-money track) |
| Community | Open and discreet Q&A, votes, reputation | Mentor marketplace and bookings | Paid mentoring in currency |
| Careers | None | Job board, recruiter interest feed | Recruiter marketplace with verified recruiters |
| AI | Tutor chat, playground assistant, next-topic recommendation | Code review mode, personalized plans | Voice and agentic study plans |
| Billing | Free and Pro via Stripe, usage meters, invoices | Starter plan, store billing in apps | Enterprise invoicing |
| Platform | In-app and email notifications, search, admin moderation, feature flags | Push, analytics dashboards | Public API, white-label |

## 6. Product Capabilities by Epic

**EP-IDN Identity and privacy.** Accounts, social login, onboarding (experience level, goal, languages, weekly hours), profile and skills, privacy controls (show on leaderboard, recruiter contact, public challenge history, show points balance), data export and deletion.

**EP-LRN Learning.** Six tiers (Beginner, Intermediate, Advanced, Expert, Master, Guru) with XP thresholds; courses and topics; lessons as video, audio, interactive, and text; progress and resume; streaks with multiplier up to 2x; achievements; weekly goals; AI-suggested next topic.

**EP-EXE Execution.** Browser playground with run output, limits shown to users, saved and shared snippets; judging against hidden test cases; quotas by plan.

**EP-CMP Competition.** Challenge catalog with filters (mode, language, tier, status); solo entries; public or private entry; live battles with server clock, live scoreboard, and spectators; tournaments with brackets; leaderboards (global, weekly, language, region, friends) with anonymous option and rank history; anti-cheat review.

**EP-RWD Rewards.** Points earned from lessons, answers, streaks, challenges, tournaments; balance and history; prize pools that grow through contributions up to a cap; redemption options; fraud controls.

**EP-COM Community.** Ask openly or discreetly (discreet is visible only to the asker and an assigned mentor); answers, votes, accepted answer, reputation; mentor marketplace with availability and booking; moderation.

**EP-CAR Careers.** Public developer portfolio; job listings with tier requirements; recruiter interest feed; applications; recruiter access only with learner consent.

**EP-AI AI assistance.** Tutor with session history and context awareness; code assistant in the playground; recommendations; plan-based token quotas; challenge mode withholds full solutions.

**EP-BIL Billing.** Plans, checkout, usage meters, invoices, upgrade, downgrade, cancel; mobile store billing mapped to the same entitlements.

**EP-PLT Platform.** Notifications with preferences, global search, personal analytics, Enterprise team dashboards, admin moderation and configuration, feature flags, audit trail.

## 7. Key User Journeys

1. **First win (PER-01):** sign up -> onboarding -> recommended first lesson -> runs code in the playground -> earns XP and first achievement -> sees streak start.
2. **Stuck and helped (PER-01):** fails an exercise -> asks the AI tutor -> still confused -> posts a discreet question -> mentor answers -> accepted answer earns points for the answerer.
3. **First challenge (PER-02):** browses challenges by tier -> enters publicly or privately -> submits -> gets a verdict and points -> sees leaderboard movement.
4. **Live battle (PER-02):** joins a battle lobby -> solves under a shared clock -> watches the scoreboard -> prize settles to the ledger.
5. **Redeem and upgrade (PER-02):** checks balance -> redeems points for a Pro month or course voucher -> sees updated entitlements and transaction history.
6. **Get discovered (PER-02, PER-04):** opts in to recruiter visibility -> a recruiter views the portfolio -> messages -> learner replies or declines.
7. **Team upskill (PER-05):** org admin provisions seats with SSO -> launches a team challenge -> reviews team leaderboard and analytics.
8. **Keep it fair (PER-06):** receives a flag -> reviews evidence (similarity report, activity) -> resolves, with an audit record.

## 8. Plans and Monetization

| Plan | Price (proposed) | Includes |
| --- | --- | --- |
| Free | $0 | 5 challenges per month, 100 executions, community access, basic AI quota |
| Starter | $9 per month | 20 challenges per month, unlimited executions, 500 AI tokens |
| Pro | $29 per month | Unlimited challenges, 5,000 AI tokens, multiplayer, priority support |
| Enterprise | Custom | Seats, team management, SSO, team challenges and analytics, priority support |

Other revenue: prize pool contributions (platform fee, subject to legal review), recruiter subscriptions and job postings, mentor marketplace commission, merchandise. Pricing and limits are hypotheses to test.

## 9. Rewards and Competition Policy

- **Points** are the live currency. Working conversion for planning: 100 points = $1 notional value; actual redemption values are set per option and may change.
- **Real-money track is Phase 2** and stays disabled (feature flag) until legal review per region (skill-contest rules, tax reporting, KYC, store policy) is complete. Nothing in the MVP may imply or promise cash prizes.
- **Fairness:** judging is deterministic and automated; ties and disputes follow a published rule; moderators can review but every action is audited.
- **Privacy as a feature:** anonymous entries never reveal identity to other users, spectators, or recruiters; the user can switch visibility at any time.
- **Prize pools** have caps and published contribution rules; payouts are computed from final standings by an automated, replay-safe process.
- **Integrity:** plagiarism and collusion detection assist moderators; no automatic permanent bans without review.

## 10. Channels and Platforms

| Channel | Phase | Notes |
| --- | --- | --- |
| Web app (responsive) | MVP | Primary; dark and light themes |
| Desktop (Windows, macOS, Linux) | After MVP | Cross-platform shell first; native only where justified |
| Mobile (Android, iOS) | After MVP | Cross-platform first; push, offline lessons, store billing |

## 11. Product-Level Quality Expectations

Detailed targets live in the SRS. Headlines: responsive and fast for 4,200 concurrent coders; 99.9% API availability; accessible (WCAG 2.2 AA); secure by design with tenant isolation; every list or data view has loading, empty, and error states; the brand uses the logo-derived white, blue, and black palette.

## 12. Assumptions, Dependencies, Constraints

- Learners will accept browser-based coding for MVP languages (Python, JavaScript).
- Content (lessons, challenges) can be produced at the pace the release plan needs; content ownership and licensing are resolved.
- External dependencies: identity provider, Stripe, PayPal (Phase 2), push services, AI provider, cloud hosting, app stores.
- Real-money features depend on legal and compliance approval and on store policy.
- Sandbox capacity cost scales with competition activity and must be budgeted.

## 13. Risks

| ID | Risk | Impact | Mitigation |
| --- | --- | --- | --- |
| RISK-01 | Legal exposure from real-money contests | High | Phase 2 gating, regional legal review, KYC |
| RISK-02 | Sandbox escape or abuse | Critical | Layered isolation, quotas, escape testing, pen test |
| RISK-03 | Cheating and collusion erode trust | High | Plagiarism checks, moderation, server-authoritative judging |
| RISK-04 | Point farming and fraud | High | Server-side event validation, velocity limits, ledger reconciliation |
| RISK-05 | Content shortage slows learning growth | Medium | Prioritize one deep track, partner and creator program later |
| RISK-06 | Infrastructure cost of sandboxes | Medium | Warm pools sized by load tests, tiered isolation |
| RISK-07 | Store policy conflicts on rewards and subscriptions | Medium | Early policy review, store billing path, flag mobile redemption |
| RISK-08 | Low retention after initial novelty | High | Streaks, goals, community, AI nudges, measured A/B tests |
| RISK-09 | Prototype shortcuts carried into production | Medium | Gap Analysis, definition of done, RTM gate |

## 14. MVP Success and Release Criteria

- All MVP-tier Must requirements implemented and traced in the RTM.
- UAT passed (at least 95% scenarios, no open Sev 1 or Sev 2).
- Security gate: pen test critical and high findings closed; tenant isolation and sandbox escape suites green.
- Performance gate: sustained load at 4,200 concurrent users within SRS latency targets.
- KPI review after 8 weeks: BG-01, BG-02, BG-03 meet or approach targets, or a corrective plan is approved.

## 15. Non-Goals

- Not a general social network or video platform.
- No cash prizes or cash-out at MVP.
- No user-hosted code execution outside the managed sandbox.
- No AI model that judges code correctness, safety, or cheating.
- No native desktop or mobile apps at MVP.

## 16. Prototype Notes

The interactive prototype is a design reference, not a product baseline. Carry over: information architecture, flows, visual language, copy intent. Replace: hard-coded data, simulated code output, and static dates. The landing page figures (128K+ active coders, $2.4M prizes awarded, 4,200 competing now) are placeholders and must not be published as facts until real numbers exist.

## 17. Open Questions

1. Final pricing, free-tier limits, and points economy (earn rates versus redemption values).
2. Legal strategy and launch regions for the real-money track.
3. First two content tracks and who authors them.
4. Hosting cloud and data-residency commitments for Enterprise.
5. Whether recruiter marketplace launches with verified recruiters only.
6. Final brand palette extensions (for example whether an AI accent color is allowed).

## 18. Approval

| Role | Name | Decision | Date |
| --- | --- | --- | --- |
| Product owner |  |  |  |
| Engineering lead |  |  |  |
| Security lead |  |  |  |
| Legal / compliance |  |  |  |

## 19. Version 0.2 Update (ECO-001 approved)

The Product owner approved the Points Economy Specification (ECO-001). Effects on this PRD:

- **Four distinct values:** XP (learning progress), points (spendable currency), Competition Score (competitive standing), and reputation (community standing). The product must label them separately everywhere.
- **Leaderboards rank by Competition Score**, which is lifetime points earned from challenges, battles, and tournaments and is never reduced by spending.
- **MVP rewards scope** now includes a small in-app catalog (profile frames and badges, premium practice packs, streak freezes) so points have meaning before redemption of Pro months or vouchers arrives in fast follow.
- **Two balance buckets:** learning points (in-app use only) and prize points (eligible for redemption when the Phase 2 real-money track opens). Prizes are funded, not minted.
- **Planning value** of 100 points = $1 remains a planning figure; there is no cash redemption before Phase 2 and legal approval.
- **Open questions** 1 (points economy) in section 17 is resolved for structure; values stay in configuration and are tuned with beta data. The ISSUANCE monthly budget and legal treatment of points remain open.
