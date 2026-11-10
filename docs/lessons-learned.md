# Lessons learned and design retrospective

**Status:** retrospective on the supplied prototype and planning materials, not a post-incident report. No production service or security incident is represented in the source package.

## What the prototype helped establish

- A broad information architecture can be explored quickly in one clickable interface.
- Learners benefit from seeing progression, courses, coding practice, challenges, and community as connected journeys.
- Privacy and anonymity are product decisions that affect profiles, leaderboards, recruiter tools, and community views—not merely display preferences.
- Rewards create their own integrity and policy requirements; XP, points, competitive standing, and reputation need separate meanings.

## What should not carry forward unchanged

The readiness and gap-analysis drafts report that the prototype is a single HTML file with hard-coded data, no production identity, no durable API-backed state, and simulated playground output. It includes placeholder activity/prize statistics and static content. This is appropriate for concept exploration, but it does not demonstrate backend correctness, accessibility, privacy enforcement, or safe code execution.

| Prototype shortcut or open area | Production implication |
|---|---|
| Simulated code output | Do not connect real users to execution until a separately reviewed runner is implemented and tested |
| Hard-coded page data | Define API contracts, authorization, error/loading/empty states, and a source of truth |
| Cosmetic privacy controls | Enforce visibility at every API, search, realtime, export, and analytics boundary |
| Combined XP/points/ranking values | Adopt separate domain values and make award rules versioned and auditable |
| Static competition and activity counts | Remove claims or replace only with verified, consent-aware data |
| Draft target architecture with many services | Validate the MVP boundary and operating cost before adopting the full topology |

## Security trade-offs to resolve

The planning drafts propose using gVisor for a standard execution tier and Firecracker microVMs for a more isolated tier. That is a design trade-off requiring measured performance, cost, operational expertise, and independent review. This package does not recommend that either technology alone is sufficient, and it includes no executable sandbox configuration.

Other decisions that need evidence:

- How identity context is propagated and verified between the gateway and services.
- Whether a Data Access Layer and row-level security can meet latency and team-operability goals.
- How user submissions, test cases, AI context, and logs are retained and redacted.
- How rewards and any future money-like redemption satisfy jurisdictional, provider, and store policies.
- How a broad service map can be reduced to the smallest deliverable MVP without weakening trust boundaries.

## Readiness findings recorded in supplied drafts

The CodeFull Gap Analysis rates prototype/implementation readiness as red and identifies unresolved content, legal, staffing, cost, and architecture questions. It also notes that the architecture is unproven until PoCs, while the control catalogs still need implementation and verification. These findings are source-document status, not a new audit of the repository or a claim that the findings have been closed.

## Recommended working practices

1. Turn each major assumption into a bounded proof or explicit decision before depending on it.
2. Implement vertical slices with real authorization, persistence, observability, accessibility, and failure states.
3. Keep test cases linked to requirements, privacy rules, and threat assumptions.
4. Make changes to rewards, ranking, consent, and retention versioned and auditable.
5. Treat isolation, tenant boundaries, and payment/reward integrity as release gates.
6. Publish only verified metrics and clearly distinguish prototypes, proposals, and shipped behavior.

## Items for a future measured retrospective

After an approved pilot, replace assumptions with evidence: learner completion and retention, exercise latency and cost, moderation load, accessibility findings, support burden, reward fraud indicators, and recovery-test results. Assign owners and dates to each action before describing the product as production-ready.
