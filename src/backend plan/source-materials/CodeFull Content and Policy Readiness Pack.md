# CodeFull Content and Policy Readiness Pack

**Doc ID:** CPP-001 | **Version:** 0.1 draft | **Status:** for Content, Operations, and Legal review | **Owner:** Content lead + Support and moderation lead + Legal **Closes or informs:** GAP-025 (age policy), GAP-026 (legal documents), GAP-027 (content pipeline), GAP-028 (moderation operations), GAP-029 (support tooling) **Upstream:** PRD-001, SRS-001, SEC-001, ECO-001, MVP-001 | **Downstream:** Release go/no-go (REL-001 sec 9), UAT beta recruitment

Part C lists legal and compliance documents and what each must cover. It is a checklist for qualified counsel, not legal advice, and contains no legal text.

# Part A. Content Authoring Guide

## A1. Goals and MVP Volumes (MVP-001, to confirm)

| Content | Target | Owner |
| --- | --- | --- |
| Learning track | One Python track, Beginner to Intermediate, about 40 lessons | Content lead |
| Lesson formats | Text and interactive for every lesson; video for about half; audio for about a third | Content lead |
| Challenges | About 30 solo challenges in Python and JavaScript (10 beginner, 12 intermediate, 8 advanced) with hidden tests | Challenge author team |
| Achievements | About 12 badges | Product and Content |

## A2. Lesson Specification

Every lesson is a versioned file (Markdown plus YAML front matter) imported by the content pipeline (PB-19).

```yaml
id: py-b-014-loops-for
track: python
tier: beginner
title: Repeating work with for loops
duration_minutes: 12
objectives: [Write a for loop over a list, Use range, Avoid off-by-one errors]
prerequisites: [py-b-010-lists]
formats: [text, interactive, video]
xp_award: 20
points_band: 20          # ECO-001 length bands
exercises: [ex-py-b-014-a, ex-py-b-014-b]
reviewed_by: [tech, pedagogy, accessibility]
version: 3
```

| Section | Requirement |
| --- | --- |
| Objectives | 2 to 4 measurable objectives stated at the top |
| Explanation | Short blocks, one idea each; plain language; code examples that run |
| Worked example | A complete example with the expected output |
| Practice | 1 to 3 interactive exercises with automated checks and hints |
| Check for understanding | A short quiz or reflection |
| Accessibility | Transcript for audio and video; captions; alt text; no information only in images or color |
| Length bands | Up to 5, 6 to 15, 16 to 30, over 30 minutes (drives XP and points) |

## A3. Challenge Specification

```yaml
id: ch-py-tree-balancer
title: Binary Tree Balancer
tier: intermediate
mode: solo
languages: [python, javascript]
statement: statement.md
constraints: {time_limit_ms: 2000, memory_limit_mb: 256}
tests: {sample: 3, hidden: 12}
scoring: {completion_points: 120, partial_credit: by_cases_passed}
reference_solutions: [ref.py, ref.js]
tags: [trees, recursion]
```

| Requirement | Detail |
| --- | --- |
| Statement | Unambiguous input and output formats, constraints, examples; no hidden assumptions |
| Tests | Sample tests shown to users; hidden tests cover edge cases, performance, and anti-guessing cases; at least one test that defeats hard-coded answers |
| Determinism | No randomness or time dependence in tests; fixed seeds; outputs compared exactly or with a documented checker |
| Limits | Time and memory limits calibrated so a reference solution passes with margin in every supported language |
| Reference solutions | At least two languages; both must pass all tests before publication |
| Leakage | Hidden test inputs and outputs are never shown; feedback is pass counts only (TM-CMP-007) |
| Difficulty | Rated against a rubric (concept count, algorithmic depth, implementation size) and calibrated with beta data |
| Rotation | Hidden tests refreshed periodically for challenges with prizes |

## A4. Review and Publication Workflow

1. **Draft** in the content repository by pull request.
2. **Technical review** (code and explanation correct; reference solutions run).
3. **Pedagogy review** (objectives met, level appropriate, prerequisites right).
4. **Test QA** for challenges: run all tests against reference solutions in every language, mutation checks (known wrong solutions must fail), timing checks in the real sandbox.
5. **Accessibility review** (transcripts, captions, alt text, reading level).
6. **Policy review** (licensing, no personal data, no harmful or discriminatory content).
7. **Publish** through the import pipeline behind the content flag; version recorded; rollback by prior version.

A lesson or challenge may not be published if any gate fails. Corrections after publication follow the same path with a new version.

## A5. Ownership, Licensing, and Third-Party Material

- All authored content is owned by CodeFull or licensed with written terms that allow the intended use; contractor agreements assign or license rights.
- Third-party code, text, images, and datasets need a recorded license compatible with commercial redistribution and attribution where required.
- Content generated or assisted by AI is reviewed and attributed internally; authors remain accountable for accuracy and licensing.
- User-submitted content (solutions, questions, answers) follows the terms of service licensing in Part C.

## A6. Metrics and Maintenance

Track lesson completion and drop-off points, exercise pass rates, time on task, challenge solve rates and score distributions, reports of errors, and learner ratings. Review the lowest-performing content monthly. Keep an erratum log and a content calendar.

# Part B. Community Guidelines and Moderation Policy (draft)

## B1. Community Guidelines (user-facing summary)

1. Be respectful; no harassment, hate, or threats.
2. Help, do not hand over answers to active challenges; do not share solutions to open competitions.
3. Compete fairly: no plagiarism, collusion, multiple accounts, or tampering.
4. Protect privacy: do not share other people's personal information or try to identify anonymous participants.
5. Keep content appropriate: no sexual, violent, or illegal content; no spam or advertising.
6. Respect intellectual property.
7. Report problems using the report button; do not retaliate.

## B2. Enforcement Ladder

| Level | Action | Typical triggers |
| --- | --- | --- |
| 1 | Content removed with a short explanation | First minor violation |
| 2 | Warning recorded on the account | Repeat or moderate violation |
| 3 | Temporary restriction (posting, entering challenges) | Persistent violation; confirmed plagiarism |
| 4 | Suspension | Serious harassment, collusion rings, fraud |
| 5 | Permanent ban and forfeiture of unclaimed prizes | Severe or repeated harm, confirmed fraud |

Automated systems (similarity checks, abuse signals) raise cases for human review; no permanent ban or prize forfeiture is automatic (SEC-071). Every decision records actor, reason, evidence, and is audited (SEC-074).

## B3. Operations and Service Levels (proposed)

| Item | Target |
| --- | --- |
| First response to a report | Within 24 hours (urgent safety reports within 2 hours) |
| Resolution | Within 3 business days for standard cases |
| Appeals | Accepted within 14 days; reviewed by a different moderator within 5 business days |
| Coverage | Business hours at MVP with an on-call escalation path; extend as volume grows |
| Staffing start | Two trained moderators at beta, plus a lead |
| Tools | Moderation queue (FR-PLT-004), evidence view with similarity reports, decision templates, audit trail |

Transparency: users receive the reason and the appeal path; aggregate moderation statistics are reviewed monthly.

## B4. AI Content Policy

- The tutor must refuse harmful requests, avoid personal data requests, and give hints only in challenge mode (FR-AI-004).
- Users can rate and report AI responses (FR-AI-006); reports enter the moderation queue with the transcript.
- Repeated misuse (attempts to extract solutions or bypass limits) leads to quota restrictions and, if severe, the enforcement ladder.

## B5. Support Operations

| Item | Plan |
| --- | --- |
| Channels | In-app help and email at MVP; community forum for peer help |
| Tooling | Helpdesk with macros, tags, and SLA tracking; status page; known-issues page (REL-001 sec 12) |
| Targets | First response within 1 business day at beta; security and billing issues prioritized |
| Knowledge base | Articles for sign-in and MFA, privacy settings, points and XP, plans and billing, challenge rules, data export and deletion |
| Escalation | Security reports go to the Security lead; payment and ledger issues to the Rewards lead; legal requests to Legal |

# Part C. Legal and Compliance Document Checklist (for counsel)

## C1. Age and Eligibility Policy (GAP-025)

This decision affects sign-up, rewards, competition, recruiter visibility, and data handling. Options to put before counsel:

| Option | Effect | Considerations |
| --- | --- | --- |
| Adults only (18 and over) at MVP | Simplest rules for rewards, contests, recruiter features, and consent | Excludes students and younger learners; needs an age gate and handling of under-age signups |
| Teens allowed (for example 13 or 16 and over by region) with parental consent where required | Wider audience | Parental consent flows, restrictions on rewards, recruiter contact, and public profiles; regional rules differ |
| Separate youth experience | Tailored protections | Largest scope; likely post-MVP |

Whichever is chosen: an age gate at sign-up, clear handling of users who state a younger age, restricted features for minors, and consent records (SEC-077). Until decided, beta recruitment is limited to adults (UAT-001 rules).

## C2. Required Documents

| Document | Must cover | Depends on | Needed by |
| --- | --- | --- | --- |
| Terms of Service | Eligibility, accounts, user content license, acceptable conduct, challenges and judging rules, points and rewards terms, subscriptions and refunds, termination, disclaimers, dispute resolution | PRD, ECO-001, age policy | Beta |
| Privacy Policy | Data collected and why, legal bases, retention, sharing and processors, user rights, international transfers, children policy, contact | DM-001 classification, SEC-001 sec 5 | Beta |
| Cookie and tracking notice with consent | Categories, consent management, analytics and session recording controls | Analytics vendor choice (GAP-032) | Beta |
| Contest and Rewards Rules | How points are earned, prize funding and payout, tie rules, disqualification, anonymity effects, regional restrictions, tax responsibilities, no cash value statement before Phase 2 | ECO-001, regional legal review | Beta (points); before any cash feature |
| Acceptable Use Policy and Community Guidelines | Prohibited conduct, sandbox and code execution limits, enforcement ladder, appeals | Part B | Beta |
| Data Processing Agreement and subprocessor list | Roles, security measures, subprocessors (cloud, Stripe, email, push, AI provider, analytics), breach notice terms | Vendor selection | Beta (for Enterprise pilots) |
| DSAR procedure | Intake, identity checks, export and deletion workflow, timelines, record keeping | FR-IDN-007, SEC-075, TC-0107, TC-0108 | Beta |
| Copyright and takedown policy | Reporting infringement, counter notices, repeat infringer policy | Content policy | Beta |
| Recruiter Terms | Allowed use of candidate data, consent rules, anti-scraping, verification | FR-CAR-002, 005 | Before careers launch |
| Mentor Terms | Eligibility, conduct, handling of discreet questions, payments in points | FR-COM-005 | Before mentor launch |
| Enterprise MSA, SLA, and security addendum | Service levels, support, data residency, security commitments, audit rights | ARCH-001, REL-001 | Before Enterprise pilots |
| Subscription and refund policy | Billing cycles, cancellation, refunds, store billing rules | FR-BIL-005 | Beta |
| Accessibility statement | Standard targeted, known limitations, feedback channel | NFR-019 | GA |
| Incident and breach notification procedure | Legal decision path and timelines | IRP-001 sec 8 (INC-4) | Beta |

## C3. Compliance Workstreams

| Area | Actions |
| --- | --- |
| Privacy (GDPR, CCPA and similar) | Records of processing, lawful bases, consent records, data subject request handling, retention enforcement, privacy review of new features |
| Payments | Keep card data out of scope with Stripe-hosted fields (SEC-057); tax and invoicing requirements by region |
| Rewards and contests | Regional review of skill contest and sweepstakes rules before any real-money track; tax reporting and KYC design (SEC-056) |
| App stores (after MVP) | Subscription and rewards policies, privacy labels, data safety forms |
| Security assurance | SOC 2 readiness planning; customer security questionnaires; pen test summary for customers (PTP-001) |
| Intellectual property | Content licensing records (A5), trademark checks for the CodeFull name and logo, open-source license compliance (SEC-090) |

## C4. Working Process

1. Legal assigns an owner per document and a drafting order driven by the Needed by column.
2. Product and Security review drafts for accuracy against the real system behavior; documents must match what the software does.
3. Engineering implements consent, age gate, DSAR, and policy acceptance flows with versioned policy records.
4. Final documents are published in the app and footer, and acceptance is logged with version and timestamp.
5. Any change to data handling or rewards triggers a policy review in the same release (PR checklist, cursorsecurityrules.md sec 15).

# Part D. Readiness Checklist for Beta

| Item | Owner | Done when |
| --- | --- | --- |
| Age policy decided and age gate specified | Legal, Product | Written decision; UAT recruitment rules updated |
| Terms, Privacy Policy, cookie consent, contest and rewards rules published | Legal | Versions live; acceptance logging working |
| DSAR procedure operational | Legal, Platform | TC-0107, TC-0108, TC-1314 pass |
| Content pipeline running; MVP content volumes met or scheduled | Content lead | First module live behind flag; QA checklist passed |
| Moderation policy approved; moderators trained; queue tooling live | Moderation lead | Test cases pass; tabletop done |
| Support tooling, status page, known-issues page, knowledge base | Support lead | Live and linked in the app |
| Vendor list and subprocessor register complete | Security, Legal | Register published |
