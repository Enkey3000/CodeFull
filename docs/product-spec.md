# Product specification

**Status:** consolidated overview based on the supplied PRD, SRS, points-economy specification, and content-readiness pack. These documents remain drafts or proposals; plan limits, KPIs, feature priorities, and rewards require owner review.

## Vision

Make it easier for people to learn programming through short, structured lessons, hands-on practice, and evidence of progress they choose to share. CodeFull proposes to bring learning, coding practice, challenges, community help, and career discovery into one platform.

## Target personas

| Persona | Needs | Core journeys |
|---|---|---|
| Beginner learner | A guided path, low-pressure practice, clear feedback | Onboard, start a lesson, run an exercise, ask for help |
| Competitor | Fair challenges and transparent standings | Enter a challenge, submit work, review result and rank |
| Mentor | A manageable way to help learners | Set availability, answer questions, build reputation |
| Recruiter | Relevant skills evidence from consenting candidates | Find opt-in portfolios, review work, contact a learner |
| Organization admin | Structured learning and team progress | Provision team access, assign learning, review aggregate progress |
| Moderator / platform admin | Fair, safe, accountable operation | Review flags, resolve disputes, audit administrative actions |

## Proposed product loop

1. A learner chooses a goal, current experience, preferred programming languages, and weekly study time.
2. The platform recommends a course and presents lessons in authored formats such as text, interactive exercise, video, or audio.
3. The learner practices in a playground or challenge and receives useful, bounded feedback.
4. Verified activity updates learning progress and may award XP or points under versioned rules.
5. The learner can decide whether to share a profile, challenge result, or recruiter visibility.

The proposed product distinguishes four values: **XP** (learning progress), **points** (in-app currency), **Competition Score** (challenge standing), and **reputation** (community standing). They must not be conflated in UI or API labels.

## Proposed MVP boundary

- Identity and onboarding with privacy preferences.
- One well-authored Python learning track with a usable course/lesson journey.
- Browser practice in Python and JavaScript, if a separately reviewed execution service is ready.
- Solo challenges, leaderboard privacy, basic progress view, and introductory AI assistance.
- In-app points ledger and non-cash rewards catalog, only after integrity and policy review.
- Community questions, moderation intake, notifications, and basic billing.

Live battles, cash or gift-card redemption, recruiter marketplace, paid mentoring, and broad multi-platform applications are explicitly later-phase proposals or gated features—not MVP capabilities.

## User stories

| ID | As a… | I want… | So that… |
|---|---|---|---|
| US-01 | New learner | to choose a goal and experience level | the learning path is relevant to me |
| US-02 | Learner | to resume a lesson and see my progress | I can study across sessions without losing my place |
| US-03 | Learner | to run a small exercise and understand the result | I can practice what a lesson teaches |
| US-04 | Learner | to submit to a solo challenge privately or publicly | I can demonstrate skill at my comfort level |
| US-05 | Learner | to control profile and recruiter visibility | I can decide what other people can see |
| US-06 | Learner | to ask a question and receive a moderated answer | I can get help without being exposed unexpectedly |
| US-07 | Moderator | to review flagged activity with an audit trail | disputes are handled consistently |

## Success measures proposed in source PRD

The draft proposes activation (first code run), day-7/day-30 retention, challenge participation, paid conversion, community response, and reward integrity as measures. It also names concurrency, latency, and availability goals. All numbers remain targets to test and validate; the prototype’s displayed counts and performance claims are placeholders.

## Non-goals and constraints

- No cash prizes or cash-out at MVP.
- No claim that a public leaderboard or recruiter search is appropriate for every learner; visibility is opt-in.
- No automatically executed AI-generated code.
- No production code runner until isolation, resource controls, and independent security testing are completed.
- Content ownership, third-party licensing, age policy, launch regions, terms/privacy, contest rules, and support operations need named owners before beta.
