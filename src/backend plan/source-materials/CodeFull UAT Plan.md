# CodeFull UAT Plan

**Doc ID:** UAT-001 | **Version:** 0.1 draft | **Status:** for product and QA approval | **Owner:** Product owner + QA lead **Upstream:** PRD-001, SRS-001, TP-001, TC-001 | **Downstream:** Release Plan, RTM

## 1. Purpose and Scope

User Acceptance Testing confirms that real users can complete the journeys that matter, that the product behaves as the PRD promises, and that it is ready for beta and then general availability. UAT does not replace automated testing; it checks value, usability, and trust (privacy, fairness, clarity of rewards).

**In scope:** all MVP journeys (UAT-001 to UAT-029), fast-follow journeys when those features reach beta (UAT-030 to UAT-034), and the Enterprise pilot (UAT-035) when it is built. **Out of scope:** load, security, and sandbox escape testing (covered by TP-001 and the Pen Testing Plan).

## 2. Objectives and Success Criteria

| Objective | Measure | Target |
| --- | --- | --- |
| Journeys work end to end | Scenario pass rate | 95% or higher of MVP scenarios pass; all P1 scenarios pass |
| No blocking defects | Open Sev 1 and Sev 2 | Zero at exit |
| Usability is acceptable | System Usability Scale (SUS) | 70 or higher |
| Users understand the product | Task completion without help | 85% or higher on core tasks |
| Early value signal | Beta cohort members who run code within 24 hours of signup (BG-01 proxy) | 60% or higher |
| Trust in privacy and rewards | Post-test survey: I understand who can see my activity; I understand how points work | 80% agree or strongly agree |
| Satisfaction | Net Promoter Score (NPS) from beta users | 30 or higher (directional) |

## 3. Participants

| Group | Persona | Size | How recruited | Focus |
| --- | --- | --- | --- | --- |
| Beginner learners | PER-01 | 30 | Waitlist, bootcamp and community partners | Onboarding, lessons, playground, AI tutor, community |
| Competitors | PER-02 | 15 | Competitive programming communities | Challenges, leaderboards, anonymity, rewards |
| Mentors | PER-03 | 5 | Invited senior developers | Answering discreet questions, reputation, bookings (FF) |
| Recruiters | PER-04 | 3 | Partner companies (FF phase) | Consent-based discovery, job board |
| Org admin | PER-05 | 1 pilot organization | Design partner | Team challenge, org dashboard (P2) |
| Moderators and admins | PER-06 | 2 internal | Operations | Moderation queue, flags, audit |

Participant rules: informed consent and a plain-language privacy notice; participants are adults only until the minor-user policy is set by Legal; no real-money rewards during UAT; incentives are in points or subscription credit only.

## 4. Environment and Data

- **Environment:** staging at production parity with the beta feature flag set; separate beta cohort tenant for analytics. Stripe in test mode for the first cycle, live mode with a small invited group for the second.
- **Data:** seeded courses, challenges, and a starter leaderboard; no production personal data; participant accounts created through the normal signup flow.
- **Support:** a triage channel with a 4-hour response during UAT hours; a known-issues page.
- **Instrumentation:** in-app feedback widget, session recording with consent (masking inputs), funnel analytics, and error tracking.

## 5. Schedule

| Week | Activity |
| --- | --- |
| T-2 | Entry criteria check, participant onboarding, scripts finalized, dry run with internal staff |
| T0 to T+1 | Cycle 1: moderated sessions (12), unmoderated scenario runs, defect triage daily |
| T+2 | Fix window; retest of Sev 1 and Sev 2; interim report |
| T+3 | Cycle 2 on release candidate: regression of failed scenarios plus new participants (10) |
| T+4 | Exit review, sign-off decision, lessons learned |

## 6. Entry Criteria

- All MVP Must features implemented behind the beta flag; TP-001 beta entry gate passed (all P1 test cases green).
- No open Sev 1 or Sev 2 defects; critical and high pen test findings closed or scheduled with approval.
- Support, feedback, and analytics tooling live; privacy notice and consent flow approved.
- UAT scripts reviewed by Product and QA.

## 7. Scenario Catalog

Pass criteria are observed outcomes; failures are logged with severity per TP-001. Each scenario traces to requirements (full mapping in RTM-001).

| ID | Persona | Scenario (Given / When / Then) | Requirements | Release | Pri |
| --- | --- | --- | --- | --- | --- |
| UAT-001 | PER-01 | Given a new visitor, when they sign up with email and verify, then they land in onboarding with a verified account | FR-IDN-001 | MVP | P1 |
| UAT-002 | PER-01 | Given a visitor, when they sign in with GitHub or Google, then they enter the app without a second account | FR-IDN-002 | MVP | P1 |
| UAT-003 | PER-01 | Given onboarding questions, when answered, then the first recommended lesson matches the level and goal | FR-IDN-003, FR-LRN-009 | MVP | P2 |
| UAT-004 | PER-01 | Given a recommended lesson, when completed, then XP, progress, and a first achievement appear | FR-LRN-001, 002, 005, 007 | MVP | P1 |
| UAT-005 | PER-01 | Given a lesson in progress, when switching format or device, then position and progress are preserved | FR-LRN-003, 004 | MVP | P2 |
| UAT-006 | PER-01 | Given daily activity, when returning on consecutive days, then streak and weekly goal update correctly | FR-LRN-006, 008 | MVP | P2 |
| UAT-007 | PER-01 | Given the playground, when running Python and JavaScript, then output appears quickly and limits are explained when hit | FR-EXE-001, 002, 003, 007, FR-LRN-010 | MVP | P1 |
| UAT-008 | PER-01 | Given working code, when saved and shared, then another person can view and fork it but not edit | FR-EXE-004 | MVP | P3 |
| UAT-009 | PER-02 | Given the challenge list, when filtering by tier, language, and status, then results are accurate and clear | FR-CMP-001 | MVP | P2 |
| UAT-010 | PER-02 | Given an open challenge, when entering and submitting, then a verdict arrives and points post once | FR-CMP-002, 003, FR-EXE-005, FR-RWD-002 | MVP | P1 |
| UAT-011 | PER-02 | Given a private entry, when others view the leaderboard, then they see Anonymous and the owner sees their rank | FR-CMP-005, 006, FR-IDN-005 | MVP | P1 |
| UAT-012 | PER-02 | Given leaderboard activity, when viewing my rank, then position, change, and nearest rivals are understandable | FR-CMP-006, 014 | MVP | P2 |
| UAT-013 | PER-02 | Given points earned, when opening balance and history, then every entry is explained and totals match | FR-RWD-003 | MVP | P1 |
| UAT-014 | PER-01 | Given a question about recursion, when chatting with the tutor, then answers use lesson context and the session can be reopened | FR-AI-001, 002 | MVP | P1 |
| UAT-015 | PER-01 | Given the plan cap, when AI usage runs out, then a clear message and upgrade path appear | FR-AI-003, FR-BIL-003 | MVP | P2 |
| UAT-016 | PER-02 | Given an active challenge, when asking the tutor for the answer, then only hints are given | FR-AI-004 | MVP | P1 |
| UAT-017 | PER-01 | Given a question posted openly, when answered and accepted, then the answerer earns points and the question shows resolved | FR-COM-001, 003, FR-RWD-002 | MVP | P1 |
| UAT-018 | PER-01 | Given a discreet question, when posted, then only I and the assigned mentor can see it; others cannot find it | FR-COM-002 | MVP | P1 |
| UAT-019 | PER-06 | Given a flagged post, when the moderator resolves it, then the outcome is applied and recorded | FR-COM-007, FR-PLT-004, FR-PLT-006 | MVP | P1 |
| UAT-020 | PER-02 | Given the Free plan, when upgrading to Pro with a card, then entitlements, usage meters, and invoice update | FR-BIL-001, 002, 004 | MVP | P1 |
| UAT-021 | PER-02 | Given a Pro subscription, when cancelling, then access continues until period end | FR-BIL-005 | MVP | P2 |
| UAT-022 | PER-02 | Given privacy settings, when changing visibility options, then profile, leaderboard, and search reflect the choice | FR-IDN-005, FR-IDN-004 | MVP | P1 |
| UAT-023 | PER-01 | Given account settings, when exporting data and deleting the account, then the export is complete and deletion is confirmed | FR-IDN-007 | MVP | P1 |
| UAT-024 | PER-06 | Given an admin account, when enabling MFA, then sign-in requires the second factor | FR-IDN-006 | MVP | P1 |
| UAT-025 | PER-01 | Given activity, when notifications fire, then they arrive in app and respect preferences | FR-PLT-001 | MVP | P2 |
| UAT-026 | PER-01 | Given a search term, when searching, then relevant challenges, courses, coders, and questions appear without private items | FR-PLT-002 | MVP | P2 |
| UAT-027 | PER-01 | Given a phone and a laptop, when using the app in dark and light themes, then layouts and contrast are usable | FR-PLT-009, NFR-021 | MVP | P2 |
| UAT-028 | PER-01 | Given assistive technology, when completing core journeys by keyboard and screen reader, then all steps are possible | NFR-019 | MVP | P1 |
| UAT-029 | PER-06 | Given the admin console, when toggling flags and reviewing the queue, then changes apply quickly and are audited | FR-PLT-004, 005, 006 | MVP | P2 |
| UAT-030 | PER-02 | Given a live battle, when joining and watching the scoreboard, then clock, standings, and spectators behave fairly | FR-CMP-008, 009, 010 | FF | P1 |
| UAT-031 | PER-02 | Given a tournament, when registering and playing a round, then bracket and results are correct | FR-CMP-011 | FF | P2 |
| UAT-032 | PER-02 | Given enough points, when redeeming for a Pro month, then points are debited once and access is granted | FR-RWD-006 | FF | P1 |
| UAT-033 | PER-04 | Given consenting talent, when a recruiter searches, then only opted-in profiles appear and the learner sees the interest | FR-CAR-002, 004 | FF | P1 |
| UAT-034 | PER-03 | Given availability, when a learner books a mentor session, then both are notified and points are escrowed | FR-COM-005, 006 | FF | P2 |
| UAT-035 | PER-05 | Given an org tenant, when the admin creates a team challenge, then members compete and the org dashboard updates | FR-PLT-007 | P2 | P2 |

## 8. Execution Procedure

1. **Briefing:** goals, consent, how to report issues, no coaching during tasks.
2. **Moderated sessions (12):** facilitator and observer; think-aloud; scenarios from the catalog; time and success recorded.
3. **Unmoderated runs:** participants follow the scenario checklist at their own pace and submit results through a form.
4. **Recording results:** per scenario: pass, pass with issues, or fail; time on task; confidence rating 1 to 5; free text; severity of any defect.
5. **Daily triage:** QA lead and product owner review new reports, assign severity and owner, update the known-issues page.
6. **Post-test survey:** SUS, NPS, trust questions on privacy and rewards, open feedback.

### Defect severity during UAT

| Severity | Examples in UAT | Action |
| --- | --- | --- |
| Sev 1 | Points wrong, identity exposed for a private entry, data loss, cannot sign in | Stop affected scenarios; fix immediately; incident process if security or ledger |
| Sev 2 | Core journey blocked without workaround, misleading reward or privacy messaging | Fix before exit |
| Sev 3 | Confusing flow with workaround | Fix or schedule with product approval |
| Sev 4 | Cosmetic | Backlog |

## 9. Exit and Acceptance Criteria

UAT passes when all of the following hold:

- At least 95% of MVP scenarios pass and every P1 scenario passes.
- Zero open Sev 1 or Sev 2 defects; every Sev 3 has an approved disposition.
- SUS at least 70; core task completion at least 85%; trust questions at least 80% agree.
- The beta cohort activation proxy (code run within 24 hours) is at or above 60%, or a corrective plan is approved by the product owner.
- Accessibility scenario UAT-028 passes with no blocking barriers.
- Results are recorded in the RTM and the sign-off table is complete.

## 10. Sign-off

| Role | Name | Decision | Date |
| --- | --- | --- | --- |
| Product owner |  |  |  |
| QA lead |  |  |  |
| Security lead |  |  |  |
| Engineering lead |  |  |  |
| Support lead |  |  |  |

## 11. Roles and Responsibilities

| Role | Responsibility |
| --- | --- |
| Product owner | Scenario ownership, acceptance decision, participant relations |
| QA lead | Scripts, facilitation, triage, reporting |
| Engineering lead | Fix capacity during UAT, release candidate builds |
| Support lead | Triage channel, known-issues page, participant communication |
| Security lead | Reviews privacy and trust findings, any security report |
| UX researcher (or designated facilitator) | Moderated sessions, survey analysis |

## 12. Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Too few participants in a persona | Over-recruit by 30%; extend the window for that persona |
| Participants drop out | Incentives in points or credit; short sessions; reminders |
| Findings overwhelm the fix window | Daily triage, strict severity rules, freeze scope during UAT |
| Privacy concerns from session recordings | Explicit consent, input masking, short retention, opt-out |
| Staging differs from production | Production parity checks at entry; smoke test after each deploy |

## 13. Deliverables

UAT scripts and checklists; results workbook per scenario; defect log; weekly status; final UAT report with metrics, quotes, open items, and recommendation; sign-off record linked from the Release Plan go/no-go checklist.

## 14. Version 0.2 Changes

These changes close the UAT gaps found in RTM-001 section 5.1 (Must requirements with no UAT scenario). The catalog grows from 35 to 37 scenarios.

| ID | Persona | Scenario (Given / When / Then) | Requirements | Release | Pri |
| --- | --- | --- | --- | --- | --- |
| UAT-036 | PER-01 | Given the Free plan limit, when the executions run out, then a clear message explains the limit, shows usage, and offers the upgrade path; interactive lesson exercises behave as the quota rules say | FR-EXE-006, FR-BIL-003 | MVP | P2 |
| UAT-037 | PER-06 | Given two near-identical submissions flagged by the system, when the moderator reviews the evidence, then they can dismiss, warn, or act, and the decision is recorded without any automatic ban | FR-CMP-013 | FF | P2 |

**Scenario updates:** UAT-030 (live battle) now also covers the hardened execution tier and prize settlement to the ledger, adding FR-EXE-008 and FR-RWD-005.

**UAT not applicable (internal controls), pending product owner approval:** FR-RWD-001 (ledger), FR-RWD-008 (fraud and velocity controls), FR-RWD-009 (reconciliation), and FR-BIL-007 (entitlement fail-open). These have no user-facing behavior; they are verified by test cases (TC-0502, 0507, 0509, 0905) and operations review. The RTM marks them N/A until the product owner signs off.

## 15. Version 0.3 Changes (ECO-001 approved)

The catalog grows from 37 to 39 scenarios.

| ID | Persona | Scenario (Given / When / Then) | Requirements | Release | Pri |
| --- | --- | --- | --- | --- | --- |
| UAT-038 | PER-02 | Given earned points, when buying a catalog item such as a streak freeze or profile frame, then the price is shown, the correct bucket is debited, the item is unlocked, and a repeat tap does not charge twice | FR-RWD-010, FR-RWD-011 | MVP | P2 |
| UAT-039 | PER-01 | Given a dashboard and a leaderboard, when reading the numbers, then XP, points, and Competition Score are clearly separate and labeled, and spending points does not change leaderboard rank | FR-RWD-003, FR-CMP-006, FR-RWD-012 | MVP | P1 |

**Scenario updates:** UAT-030 (live battle and prize settlement) also covers FR-RWD-013 (prizes are funded, not minted).

**Post-test survey addition:** ask participants to explain in their own words the difference between XP, points, and Competition Score; target at least 80% correct, because the economy only works if users understand it.
