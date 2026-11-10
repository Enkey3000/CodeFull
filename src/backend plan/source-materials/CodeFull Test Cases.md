# CodeFull Test Cases

**Doc ID:** TC-001 | **Version:** 0.1 draft | **Status:** for QA review | **Owner:** QA lead **Upstream:** SRS-001, SEC-001, TM-001, TP-001, OpenAPI | **Downstream:** UAT Plan, RTM

## 1. Conventions

- **ID ranges:** 01xx Identity, 02xx Learning, 03xx Execution, 04xx Competition, 05xx Rewards, 06xx Community, 07xx Careers, 08xx AI, 09xx Billing, 10xx Platform, 11xx Security, 12xx Sandbox, 13xx Non-functional, 14xx Accessibility and compatibility.
- **Suite codes** follow TP-001 (UT, CT, IT, DB, SBX, E2E, SAST, DAST, LOAD, CHAOS, AI, A11Y, COMPAT, PEN).
- **Priority:** P1 blocks release, P2 blocks beta or GA for the area, P3 normal.
- **Auto:** A = automated in CI, M = manual or exploratory (with a plan to automate).
- **Format:** each case lists scenario and steps, expected result, traced IDs (FR, NFR, SEC, TM), priority, and automation. Full step scripts live in the test repository next to the code and carry the same ID and trace tags.
- Every Must requirement in SRS-001 and every High threat in TM-001 has at least one case here (coverage summary in section 5).

## 2. Functional Test Cases

### 2.1 Identity and privacy

| ID | Suite | Scenario | Expected result | Traces | Pri | Auto |
| --- | --- | --- | --- | --- | --- | --- |
| TC-0101 | E2E | Register with a new valid email and password; repeat with the same email | Account created and verification email sent; duplicate returns a 409 problem response | FR-IDN-001 | P1 | A |
| TC-0102 | E2E | Sign in with GitHub and with Google, as new and returning users | Signed in or account created; no duplicate accounts | FR-IDN-002 | P1 | A |
| TC-0103 | E2E | Complete onboarding; separately skip it | Answers stored; first recommendation reflects them; skipping still reaches the dashboard | FR-IDN-003 | P2 | A |
| TC-0104 | IT | Edit profile with a 3-character name, a 2-character name, and a taken name | Valid saved within 5 s; short name 422; taken name 409 | FR-IDN-004, SEC-022 | P2 | A |
| TC-0105 | IT | User A turns off leaderboard visibility; user B views leaderboard, profile, search, and exports | A's identity appears in none; A still ranks as Anonymous | FR-IDN-005, SEC-017, TM-TEN-005 | P1 | A |
| TC-0106 | E2E | Enroll TOTP MFA, sign out, sign in; try an admin account without MFA | Second factor required; admin without MFA denied admin routes | FR-IDN-006, SEC-003, TM-AUT-003 | P1 | A |
| TC-0107 | IT | Request data export; try with another user's id | Archive contains only the caller's data; foreign id returns 403 or 404 | FR-IDN-007, TM-PRV-003 | P1 | A |
| TC-0108 | IT | Delete an account | Personal data removed or detached within 30 days; ledger rows kept without identity; user absent from search and leaderboards | FR-IDN-007, SEC-075, TM-PRV-004 | P1 | A |
| TC-0109 | IT | Revoke a session from the device list | Revoked token rejected within 60 s | FR-IDN-010, SEC-006 | P2 | A |
| TC-0110 | IT | Replay a used refresh token | Whole token family revoked; user must sign in again | SEC-002, TM-AUT-002 | P1 | A |
| TC-0111 | DAST | Credential-stuffing run against login from one IP and from many IPs | Rate limits and bot protection trigger; no account lockout bypass | SEC-007, TM-AUT-001 | P1 | A |

### 2.2 Learning and progression

| ID | Suite | Scenario | Expected result | Traces | Pri | Auto |
| --- | --- | --- | --- | --- | --- | --- |
| TC-0201 | IT | Open the dashboard and progression pages for a user mid-tier | Current tier, XP in tier, and XP to next are correct | FR-LRN-001 | P2 | A |
| TC-0202 | E2E | Enroll in a course | Course appears in Continue Learning | FR-LRN-002 | P2 | A |
| TC-0203 | E2E | Switch a lesson between video, audio, text, and interactive | Format changes; progress position preserved | FR-LRN-003 | P2 | A |
| TC-0204 | IT | Leave mid-lesson on one device; open on another | Resumes within 10 s of the last position | FR-LRN-004 | P2 | A |
| TC-0205 | UT | Award XP twice with the same idempotency key; push XP across a tier threshold | One award; tier promotes exactly once; one notification | FR-LRN-005, TM-LRN-002 | P1 | A |
| TC-0206 | UT | Streaks across consecutive days, a missed day, DST changes, and a time zone change; multiplier at cap | Streak increments per user-day; reset on miss; multiplier never above 2x | FR-LRN-006, TM-LRN-003 | P2 | A |
| TC-0207 | IT | Client sends completion for a lesson never started, and for a video finished faster than its duration | Rejected; no XP; event logged for abuse review | SEC-021, TM-LRN-001 | P1 | A |
| TC-0208 | E2E | Run an interactive exercise from a lesson | Output and pass state shown via the execution service | FR-LRN-010 | P2 | A |
| TC-0209 | UT | Property test: random sequences of XP events | XP never decreases; tier is monotonic | FR-LRN-005 | P3 | A |

### 2.3 Code execution

| ID | Suite | Scenario | Expected result | Traces | Pri | Auto |
| --- | --- | --- | --- | --- | --- | --- |
| TC-0301 | E2E | Run Python and JavaScript hello-world from a warm pool | First output within the NFR-003 target; run recorded in history | FR-EXE-001, NFR-003 | P1 | A |
| TC-0302 | IT | Request an unsupported language | 422 problem response; UI does not offer it | FR-EXE-002 | P3 | A |
| TC-0303 | SBX | Infinite loop; memory bomb; large output | Terminated at limits with clear messages; node unaffected | FR-EXE-003, SEC-040, TM-SBX-002 | P1 | A |
| TC-0304 | SBX | Open a socket, resolve DNS, call the cloud metadata address | All fail; no route to internal services | SEC-041, TM-SBX-003 | P1 | A |
| TC-0305 | IT | Judge the same submission 100 times | Identical verdict and test results every time | FR-EXE-005, SEC-047 | P1 | A |
| TC-0306 | IT | Free user performs the 101st execution; repeat with the entitlement service down | First case refused with upgrade message; second case allowed and logged (fail open) | FR-EXE-006, FR-BIL-007 | P2 | A |
| TC-0307 | SBX | Submit in a battle | Job runs in the hardened tier | FR-EXE-008, SEC-044 | P1 | A |
| TC-0308 | IT | Share a snippet; open as another user; try to edit | Viewer can read and fork; edit denied | FR-EXE-004 | P3 | A |

### 2.4 Competition

| ID | Suite | Scenario | Expected result | Traces | Pri | Auto |
| --- | --- | --- | --- | --- | --- | --- |
| TC-0401 | E2E | Filter challenges by mode, language, tier, and status | Results match every selected filter | FR-CMP-001 | P2 | A |
| TC-0402 | IT | Enter an open challenge within quota; submit after the close time | Entry created; late submission rejected | FR-CMP-002 | P1 | A |
| TC-0403 | IT | Win a challenge; replay the verdict event three times | Exactly one points posting; dashboard reflects it | FR-CMP-003, TM-RWD-001 | P1 | A |
| TC-0404 | IT | Enter privately; inspect leaderboard, search, spectator, replay, and API payloads as another user | Only Anonymous with lock shown; no identity field anywhere | FR-CMP-005, SEC-017, TM-CMP-004 | P1 | A |
| TC-0405 | IT | Change a score; poll the global leaderboard | Updated within 5 s | FR-CMP-006 | P2 | A |
| TC-0406 | IT | Join a battle until capacity, then one more | Extra join refused with alternative offered | FR-CMP-008 | P2 | A |
| TC-0407 | IT | Join with client clock skewed by plus and minus 10 minutes; submit after cutoff | Cutoffs and scores unaffected; late submission rejected | FR-CMP-009, SEC-069, TM-CMP-003 | P1 | A |
| TC-0408 | IT | Two near-identical submissions from different users | Both flagged in moderation queue; no automatic ban; moderator action audited | FR-CMP-013, SEC-071, TM-CMP-001 | P1 | A |
| TC-0409 | IT | Inspect verdict responses and errors | Only pass counts shown; hidden inputs and expected outputs never exposed | TM-CMP-007, SEC-047 | P2 | A |
| TC-0410 | LOAD | 100 entrants and 1,000 spectators in one battle | Scoreboard propagation p95 under 1 s; drift under 250 ms | NFR-006, NFR-012 | P1 | A |
| TC-0411 | UT | Equal scores with different submission times and attempts | Earlier accepted submission wins; then fewer attempts | SRS section 8 | P3 | A |
| TC-0412 | IT | Same person creates many accounts to climb leaderboards | Device and behavior signals raise flags; velocity limits apply | SEC-072, TM-CMP-006 | P2 | A |

### 2.5 Rewards

| ID | Suite | Scenario | Expected result | Traces | Pri | Auto |
| --- | --- | --- | --- | --- | --- | --- |
| TC-0501 | DB | Attempt UPDATE and DELETE on ledger tables with the application role | Both fail with permission errors | SEC-051, TM-RWD-003 | P1 | A |
| TC-0502 | UT | Property test over random posting sequences | Debits equal credits; no negative balances | FR-RWD-001, SEC-052 | P1 | A |
| TC-0503 | IT | Trigger each earning source (lesson, answer, streak, challenge, tournament, daily) | One posting per event with source reference | FR-RWD-002 | P1 | A |
| TC-0504 | IT | Post an entry; open balance and history | Appears within 5 s; lifetime earned correct | FR-RWD-003 | P2 | A |
| TC-0505 | IT | Kill the settlement worker mid-run; restart | Workflow resumes; exactly one payout per winner | FR-RWD-005, TM-RWD-008 | P1 | A |
| TC-0506 | IT | 50 parallel awards with one idempotency key | One posting | TM-RWD-001, SEC-052 | P1 | A |
| TC-0507 | IT | New account redeems a large amount; amount above the step-up threshold | Held for review; step-up MFA required | FR-RWD-008, SEC-004, SEC-059, TM-RWD-005 | P1 | A |
| TC-0508 | IT | Send a request body containing points or score fields | Ignored or rejected; values computed server-side | SEC-053, TM-RWD-002 | P1 | A |
| TC-0509 | IT | Inject a mismatch between ledger and projection | Reconciliation detects it and pages on-call | FR-RWD-009, SEC-058 | P1 | A |
| TC-0510 | IT | With the real-money flag off, call cash redemption; then try to enable the flag as a single admin | Route unreachable; enabling requires dual approval and is audited | FR-RWD-007, SEC-056, SEC-103, TM-RWD-009 | P1 | A |
| TC-0511 | IT | Contribute to a pool beyond its cap | Further contributions refused | FR-RWD-004 | P2 | A |

### 2.6 Community and mentors

| ID | Suite | Scenario | Expected result | Traces | Pri | Auto |
| --- | --- | --- | --- | --- | --- | --- |
| TC-0601 | E2E | Post an open question with tags | Appears in the feed and in search | FR-COM-001 | P2 | A |
| TC-0602 | IT | Post a discreet question; view as another learner, a non-assigned mentor, in feed, search, counts, and by direct id | Never visible; direct id returns 404; only asker and assigned mentor see it | FR-COM-002, SEC-018, TM-PRV-001 | P1 | A |
| TC-0603 | IT | Answer, vote, accept; re-accept the same answer | Points awarded once to the answerer; second accept has no effect | FR-COM-003 | P1 | A |
| TC-0604 | DAST | Submit script and HTML payloads in titles, bodies, bios, and challenge text | Rendered inert; CSP blocks inline execution | SEC-024, SEC-027, TM-PRV-005 | P1 | A |
| TC-0605 | IT | Flag content; moderator resolves | Audit record has actor, action, and reason | FR-COM-007, SEC-074 | P1 | A |
| TC-0606 | IT | Accepted answers and votes change reputation | Reputation and ranking update | FR-COM-004 | P3 | A |
| TC-0607 | IT | Book a mentor slot; cancel | Slot held; points escrowed; returned per policy on cancel | FR-COM-005, FR-COM-006 | P2 | A |

### 2.7 Careers

| ID | Suite | Scenario | Expected result | Traces | Pri | Auto |
| --- | --- | --- | --- | --- | --- | --- |
| TC-0701 | IT | Recruiter searches talent; some profiles have recruiter visibility off | Hidden profiles never appear; views are logged | FR-CAR-002, SEC-019, TM-PRV-002 | P1 | A |
| TC-0702 | IT | Unverified recruiter tries to access talent views | Denied until verified | FR-CAR-005 | P1 | A |
| TC-0703 | IT | View a job requiring Expert as an Intermediate user | Shown as locked or informational | FR-CAR-001 | P3 | A |
| TC-0704 | DAST | Script 1,000 profile fetches as one recruiter | Rate limits apply; alert raised | SEC-029, TM-PRV-002 | P2 | A |

### 2.8 AI assistance

| ID | Suite | Scenario | Expected result | Traces | Pri | Auto |
| --- | --- | --- | --- | --- | --- | --- |
| TC-0801 | E2E | Hold a multi-turn tutor session; reopen it later | Messages and context preserved | FR-AI-001 | P2 | A |
| TC-0802 | IT | Use tokens up to the plan cap, then one more request | Request refused with usage shown; metered total equals provider-reported total | FR-AI-003, SEC-062, TM-AI-004 | P1 | A |
| TC-0803 | AI | Run the fixed set of challenge-mode prompts that try to extract full solutions | Hints only; pass rate at or above the agreed threshold; failures reviewed | FR-AI-004, SEC-067, TM-AI-003 | P1 | A |
| TC-0804 | AI | Lesson text and code comments containing instruction-override and tool-escalation attempts | Instructions not followed; system prompt not disclosed; no permission change | SEC-063, SEC-064, SEC-066, TM-AI-001, TM-AI-002 | P1 | A |
| TC-0805 | IT | Include API keys and emails in code sent to the tutor | Masked before the provider call and absent from logs | SEC-065, TM-AI-005 | P1 | A |
| TC-0806 | E2E | Model output containing HTML, script, and runnable code | Rendered inert; code never runs unless the user chooses Run | SEC-064, SEC-024, TM-AI-006 | P1 | A |
| TC-0807 | IT | Report an AI response | Enters moderation queue with transcript | FR-AI-006, TM-AI-007 | P3 | A |

### 2.9 Billing

| ID | Suite | Scenario | Expected result | Traces | Pri | Auto |
| --- | --- | --- | --- | --- | --- | --- |
| TC-0901 | E2E | Subscribe to Pro with a Stripe test card | Entitlements update within 30 s; invoice appears | FR-BIL-002, FR-BIL-004 | P1 | A |
| TC-0902 | IT | View plans and usage meters on Free, Starter, and Pro | Limits and meters match SRS section 8 | FR-BIL-001, FR-BIL-003 | P2 | A |
| TC-0903 | IT | Cancel a subscription mid-period | Access continues to period end | FR-BIL-005 | P2 | A |
| TC-0904 | IT | Send forged, replayed, duplicate, and out-of-order Stripe webhooks | Forged rejected; duplicates ignored; order tolerated; entitlements correct | SEC-055, TM-RWD-006 | P1 | A |
| TC-0905 | CHAOS | Take billing down; then exercise a redemption | Normal requests allowed and logged (fail open); redemption denied and alerted (fail closed) | FR-BIL-007, ADR-014 | P1 | A |
| TC-0906 | IT | Scan logs, databases, and traces after a purchase | No card data present | SEC-057, NFR-024 | P1 | A |

### 2.10 Platform

| ID | Suite | Scenario | Expected result | Traces | Pri | Auto |
| --- | --- | --- | --- | --- | --- | --- |
| TC-1001 | IT | Trigger notifications with preferences on and off | In-app within 5 s; disabled categories suppressed | FR-PLT-001, NFR-010 | P2 | A |
| TC-1002 | IT | Admin changes feature flags; enables maintenance mode | Effective within 60 s; audited; writes blocked with a clear message | FR-PLT-005, FR-PLT-006 | P1 | A |
| TC-1003 | DB | Attempt UPDATE and DELETE on audit log tables | Both fail | FR-PLT-006, SEC-074 | P1 | A |
| TC-1004 | E2E | Toggle theme; reload; change system preference | Choice persisted; system preference respected when unset | FR-PLT-009 | P3 | A |
| TC-1005 | IT | Learner, moderator, and admin call moderation endpoints | Learner denied; moderator and admin allowed | FR-PLT-004, SEC-009 | P1 | A |

## 3. Security Test Cases

| ID | Suite | Scenario | Expected result | Traces | Pri | Auto |
| --- | --- | --- | --- | --- | --- | --- |
| TC-1101 | IT | Authorization matrix generated from OpenAPI roles: every role against every endpoint | Unauthorized calls return 401 or 403 | SEC-009 | P1 | A |
| TC-1102 | IT | For every route with an id, use another user's resource id | 403 or 404; no data returned | SEC-010, TM-TEN-002 | P1 | A |
| TC-1103 | IT | Call each service directly with missing, altered, and forged identity headers | Rejected | SEC-011, TM-TEN-003 | P1 | A |
| TC-1104 | DB | For every tenant-scoped table, tenant A session attempts all verbs on tenant B rows; list tables lacking RLS | All blocked; zero tables without RLS | SEC-014, SEC-015, TM-TEN-001, TM-TEN-006 | P1 | A |
| TC-1105 | DB | Audit database roles used by services | No superuser, BYPASSRLS, or direct service access outside the DAL | SEC-013, TM-TEN-004 | P1 | A |
| TC-1106 | DAST | SQL and command injection fuzzing across all inputs | No injection; errors sanitized | SEC-022, SEC-023, TM-API-002 | P1 | A |
| TC-1107 | IT | Supply private, link-local, and metadata addresses to any feature that fetches URLs | Blocked by egress policy | SEC-026, TM-API-003 | P1 | A |
| TC-1108 | DAST | Inspect response headers and CORS behavior | CSP, HSTS, content-type, and frame headers present; no wildcard CORS with credentials | SEC-027 | P2 | A |
| TC-1109 | SAST | Commit a seeded fake secret in a pull request | Blocked by pre-commit and CI | SEC-083, TM-INF-002 | P1 | A |
| TC-1110 | SAST | Introduce a critical dependency vulnerability; deploy an unsigned image | Build blocked; admission controller rejects the image | SEC-082, SEC-084, TM-INF-001, TM-SBX-007 | P1 | A |
| TC-1111 | IT | Run the full E2E suite, then scan all logs | No tokens, passwords, payment data, full submissions, or unmasked PII | SEC-073, TM-AUT-006 | P1 | A |
| TC-1112 | IT | Send requests with unexpected extra fields | 422; fields not persisted | SEC-022, TM-API-005 | P2 | A |
| TC-1113 | IT | Upload oversized files, wrong magic bytes, and an EICAR sample | All rejected | SEC-025, TM-API-007 | P2 | A |
| TC-1114 | PEN | Desktop shell: webview and IPC abuse; tampered update package | No command execution; unsigned update refused | SEC-092, SEC-093, TM-CLI-002, TM-CLI-003 | P1 | M |
| TC-1115 | PEN | Mobile: tampered build and emulator attempt a redemption | Blocked without valid attestation | SEC-060, SEC-096, TM-CLI-005 | P2 | M |
| TC-1116 | IT | Scan repos and images for secrets; let dynamic database credentials expire | None found; expired credentials rejected and renewed | SEC-031, SEC-032 | P1 | A |
| TC-1117 | REV | Review cloud IAM, CI tokens, and break-glass access | Least privilege; no long-lived keys; break-glass alerts fire | SEC-102, TM-INF-003 | P1 | M |
| TC-1118 | REV | Attempt to merge to a protected branch without review | Blocked | SEC-087, TM-INF-005 | P1 | A |

## 4. Sandbox Test Cases

| ID | Suite | Scenario | Expected result | Traces | Pri | Auto |
| --- | --- | --- | --- | --- | --- | --- |
| TC-1201 | SBX | Fork bomb | Process limit stops it; neighbors unaffected | SEC-040, TM-SBX-002 | P1 | A |
| TC-1202 | SBX | Fill disk and temp storage | Quota stops writes; sandbox destroyed | SEC-040 | P1 | A |
| TC-1203 | SBX | ptrace, mount, unshare, module load, and privileged syscall attempts | Blocked by seccomp and dropped capabilities | SEC-042, TM-SBX-001 | P1 | A |
| TC-1204 | SBX | Look for the container runtime socket and host paths | Not present | SEC-045 | P1 | A |
| TC-1205 | SBX | Write a marker in run 1; run again from the same account and a different account | Marker never visible | SEC-043, TM-SBX-004 | P1 | A |
| TC-1206 | SBX | Attempt to modify or read hidden test files and expected outputs | Denied; verdict unaffected | SEC-047, SEC-050, TM-SBX-005 | P1 | A |
| TC-1207 | SBX | Run a mining-style workload | Detected, killed, user flagged | SEC-046, TM-SBX-006 | P2 | A |
| TC-1208 | PEN | MicroVM escape and side-channel probes against the hardened tier | No escape; findings tracked | SEC-044, TM-SBX-001 | P1 | M |
| TC-1209 | E2E | Output containing script tags and terminal escape sequences | Rendered inert in the UI | SEC-050, TM-SBX-008 | P2 | A |
| TC-1210 | SBX | From a sandbox node, reach internal service ranges and instance credentials | Unreachable | SEC-049, TM-SBX-003 | P1 | A |

## 5. Non-Functional and UX Test Cases

| ID | Suite | Scenario | Expected result | Traces | Pri | Auto |
| --- | --- | --- | --- | --- | --- | --- |
| TC-1301 | LOAD | LOAD-1 baseline, 4,200 concurrent users | NFR-001 and NFR-002 met; error rate under 0.5% | NFR-001, NFR-002, NFR-011 | P1 | A |
| TC-1302 | LOAD | LOAD-2 spike at 3x for 15 minutes | No data loss; autoscaling within 3 minutes | NFR-011 | P1 | A |
| TC-1303 | LOAD | LOAD-3 soak for 8 hours | No leaks or degradation trend | NFR-014 | P2 | A |
| TC-1304 | LOAD | LOAD-4 sandbox at 500 runs per second | Latency targets met; no cross-user leakage | NFR-003, NFR-004, NFR-013 | P1 | A |
| TC-1305 | LOAD | LOAD-6 leaderboard updates at scale | Leaderboard read p95 under 200 ms | NFR-007 | P2 | A |
| TC-1306 | LOAD | LOAD-7 AI streams with quotas | First token p95 under 2 s; quotas exact | NFR-008 | P2 | A |
| TC-1307 | CHAOS | Take Redis offline | Leaderboards served from snapshots; core flows continue | NFR-016 | P1 | A |
| TC-1308 | CHAOS | Fail over Postgres | RTO met; no lost committed writes | NFR-014, NFR-015 | P1 | M |
| TC-1309 | CHAOS | Take NATS offline during traffic | Outbox retries; no event loss after recovery | NFR-016 | P1 | A |
| TC-1310 | REV | Restore from backup into a clean environment | Meets RPO 5 minutes and RTO 1 hour | NFR-015, SEC-101, TM-INF-004 | P1 | M |
| TC-1311 | IT | Run retention jobs on aged data | Logs, submissions, and deleted-account data handled per NFR-025 | NFR-025, SEC-078 | P2 | A |
| TC-1312 | E2E | Measure largest contentful paint on key pages | p75 under 2.5 s | NFR-005 | P2 | A |
| TC-1401 | A11Y | Automated and screen reader checks on all MVP screens | WCAG 2.2 AA with no critical violations | NFR-019 | P1 | A |
| TC-1402 | A11Y | Complete core journeys using only the keyboard | All flows reachable; visible focus | NFR-019 | P2 | M |
| TC-1403 | COMPAT | Run smoke suite across the browser matrix | Passes on all supported browsers | NFR-020 | P2 | A |
| TC-1404 | COMPAT | Check layouts from 320 to 1440 px; open the drawer under 860 px | No clipped content; drawer works | NFR-021 | P2 | A |
| TC-1405 | E2E | Force empty, slow, and failing API responses for every list and data view | Loading, empty, and error states appear and recover | PRD section 11 | P2 | A |
| TC-1406 | A11Y | Check contrast in dark and light themes against the logo-derived palette | Ratios meet AA | NFR-019, FR-PLT-009 | P2 | A |

## 6. Coverage Summary

| Measure | Result |
| --- | --- |
| Total cases in this baseline | 126 |
| Must functional requirements (53) with at least one case | 53 of 53 |
| High threats (23) with at least one case | 23 of 23 |
| Suites represented | E2E, UT, IT, DB, SBX, DAST, SAST, LOAD, CHAOS, AI, A11Y, COMPAT, PEN, REV |

Not yet covered by cases (to add as features are specified): Should and Could requirements not listed above (for example FR-LRN-007, 008, 011, 012; FR-CMP-004, 007, 010 to 012; FR-IDN-008, 009; FR-PLT-002, 003, 007, 008), P2 items, and native desktop and mobile client suites.

## 7. Execution Notes

- P1 cases run on every release candidate; P2 on beta and GA candidates; P3 weekly.
- Cases marked M are scripted in the test repository with a plan to automate; PEN and REV cases are executed by the security lead or the external vendor.
- Each failed P1 case opens a Sev 1 or Sev 2 defect per TP-001 section 8 and blocks promotion.
- Results are published to the RTM report each sprint.

## 8. Version 0.2 Additions

These 32 cases close the gaps found in RTM-001 sections 5.2 to 5.4: 21 security controls, 5 non-functional requirements, and 15 threats without a direct test tag. They raise the baseline from 126 to 158 cases.

| ID | Suite | Scenario | Expected result | Traces | Pri | Auto |
| --- | --- | --- | --- | --- | --- | --- |
| TC-0413 | IT | Several accounts submit with correlated timing, shared device or network signals, and near-identical solutions in a battle or challenge | Pattern flagged for moderator review; no automatic ban | SEC-071, TM-CMP-002 | P2 | A |
| TC-0512 | IT | Pick a posted prize or earning entry and reconstruct it from ledger, source reference, and audit records | Full trail available without editing data; supports dispute handling | SEC-052, SEC-074, TM-RWD-004 | P2 | A |
| TC-0513 | IT | Contribute to a pool from related accounts and in wash patterns; exceed the cap | Patterns flagged; cap enforced; contributions from related accounts limited | FR-RWD-004, SEC-052, TM-RWD-007 | P2 | A |
| TC-1119 | IT | Start an authorization request without a PKCE verifier; try implicit and password grant flows from each client type | Rejected; only code flow with PKCE is enabled | SEC-001 | P1 | A |
| TC-1120 | IT | After sign-in, inspect web storage, cookies, desktop and mobile secure storage, and logs | No tokens in localStorage or sessionStorage; cookies HttpOnly and SameSite; native clients use keychain or Keystore | SEC-005, SEC-091, TM-CLI-001, TM-AUT-006 | P1 | A |
| TC-1121 | IT | Abuse account recovery: reuse and expire recovery tokens, brute-force codes, request recovery repeatedly | Tokens single-use and short-lived; cooldowns and notifications apply; step-up required | SEC-008, TM-AUT-005 | P1 | A |
| TC-1122 | IT | Open plaintext and unauthenticated connections between services; present an expired client certificate | All refused | SEC-012 | P1 | A |
| TC-1123 | DB | Query audited public views and base tables as the public role | Only allowlisted public columns appear; no direct base-table access | SEC-016, TM-TEN-005 | P1 | A |
| TC-1124 | IT | Call admin routes from a non-allowlisted IP, and from an allowlisted IP without step-up MFA | Both denied | SEC-020, TM-AUT-003 | P1 | A |
| TC-1125 | DAST | Send cookie-authenticated mutating requests from another origin without a CSRF token | Rejected | SEC-028, TM-API-004 | P2 | A |
| TC-1126 | SAST | Introduce unsafe deserialization, MD5 or SHA-1 for security, ECB mode, and non-CSPRNG token generation in a test branch | Each seeded violation fails CI | SEC-030, SEC-034, SEC-035 | P1 | A |
| TC-1127 | DAST | Scan external endpoints for TLS versions and ciphers; search code for disabled verification | TLS 1.3 only externally; no disabled verification | SEC-033 | P2 | A |
| TC-1128 | IT | From each service identity, attempt to reach sandbox pools | Only the Execution Gateway identity succeeds | SEC-039, TM-SBX-003 | P1 | A |
| TC-1129 | SAST | Open a pull request that weakens a sandbox policy or image | The escape suite runs as a required check and blocks the merge | SEC-048, TM-SBX-001 | P1 | A |
| TC-1130 | CHAOS | Take a dependency of settlement or redemption offline, or leave a workflow in an ambiguous state | Money actions are denied or held and an alert fires; nothing is credited or paid | SEC-054, FR-RWD-005 | P1 | A |
| TC-1131 | IT | Connect to the hub without a token, with a token for another room, with a stale resume token, and from a disallowed origin | All rejected | SEC-068, FR-CMP-009 | P1 | A |
| TC-1132 | LOAD | Send oversized messages and floods from one client and many | Oversize dropped and client disconnected; flood isolated; queues bounded; other rooms unaffected | SEC-070, TM-CMP-005 | P2 | A |
| TC-1133 | IT | Grant, change, and withdraw recruiter visibility, marketing, and telemetry consent | Consent stored with time and version; withdrawal honored everywhere | SEC-077 | P2 | A |
| TC-1134 | SAST | Add an unpinned dependency, a latest tag, and an unverified installer | Each fails CI | SEC-085, TM-INF-001 | P2 | A |
| TC-1135 | DAST | Run the scheduled ZAP and API fuzzing job on staging | Report produced; new high findings fail the job | SEC-089 | P2 | A |
| TC-1136 | IT | Open deep and app links to non-allowlisted hosts and to privileged actions | Non-allowlisted ignored; privileged actions require re-authentication | SEC-095, TM-CLI-004 | P2 | A |
| TC-1313 | LOAD | Run search at baseline concurrency | p95 under 400 ms | NFR-009 | P2 | A |
| TC-1314 | REV | Review privacy evidence: export, deletion, consent records, retention; run a data subject request drill | Requests completed within policy; evidence filed | NFR-018, SEC-075, SEC-077 | P1 | M |
| TC-1315 | IT | Check every service emits traces, metrics, and logs; induce a fault | Dashboards show the service; the SLO alert fires within target | NFR-022, SEC-079 | P1 | A |
| TC-1316 | SAST | Verify required CI checks: coverage on domain code, lint, type checks, contract diff | Checks configured as required; a violation blocks merge | NFR-023 | P2 | A |
| TC-1317 | IT | Run a lint for hard-coded user-facing strings; render a pseudo-locale | No hard-coded strings; layouts survive longer text | NFR-026 | P3 | A |
| TC-1318 | LOAD | Burst cheap runs from one user while others run normally | Quotas and fair scheduling keep other users within twice their normal p95 | SEC-029, SEC-046, TM-SBX-009 | P2 | A |
| TC-1319 | IT | Query search and suggestions for hidden users, private entries, discreet questions, and deleted accounts | None retrievable by any query | SEC-017, SEC-018, TM-PRV-006, FR-PLT-002 | P1 | A |
| TC-1320 | DAST | Try to evade rate limits with spoofed forwarding headers, many IPs, and token rotation | Limits hold on the verified identity and source | SEC-029, SEC-007, TM-API-001 | P2 | A |
| TC-1321 | DAST | Trigger errors across routes | Responses are sanitized problem details; no stack traces, SQL, or internal hosts | SEC-022, TM-API-006 | P2 | A |
| TC-1322 | SAST | Scan built web, desktop, and mobile bundles for secrets | None found | SEC-031, SEC-094, TM-CLI-006 | P1 | A |
| TC-1323 | REV | Review backup access, encryption, and restore targets | Least-privilege access; restores only to approved environments with anonymization for non-production | SEC-036, SEC-038, SEC-080, TM-INF-006 | P2 | M |

Traces were also added to existing cases: TC-1003 now covers TM-AUT-004 (audit records protect against repudiation).

### Updated coverage summary (v0.2)

| Measure | Result |
| --- | --- |
| Total cases | 158 |
| Must functional requirements with a case | 53 of 53 |
| High threats with a case | 23 of 23 |
| Medium and Low threats with a direct case | 49 of 49 |
| Security controls covered by a case | 92 of 104 (the other 12 rely on process evidence: review, pen test, pipeline gate, drill, or program) |
| Non-functional requirements with a case | 26 of 26 |
| Should and Could requirements still without a case | 24 (added as those features are specified) |

## 9. Version 0.3 Additions (ECO-001 approved)

These 11 cases cover the approved points economy: the four-value model, Competition Score, two balance buckets, the MVP catalog, funded prizes, and the exercise quota exemption. Total cases: 169.

| ID | Suite | Scenario | Expected result | Traces | Pri | Auto |
| --- | --- | --- | --- | --- | --- | --- |
| TC-0514 | IT | Buy a catalog item with 50 parallel requests sharing one idempotency key | One debit and one unlock; others return the same result | FR-RWD-010, SEC-052, TM-RWD-001 | P1 | A |
| TC-0515 | IT | Buy an item larger than the learning bucket with enough prize points; then try with insufficient total points | Learning points debited first, remainder from prize points; insufficient total debits nothing | FR-RWD-011, SEC-053 | P1 | A |
| TC-0516 | IT | Spend points and redeem, then read the leaderboard; separately complete a challenge | Competition Score and rank unchanged by spending; increases only from competition entries | FR-RWD-012, FR-CMP-006 | P1 | A |
| TC-0517 | UT | Apply per-source daily caps; compute the streak multiplier for days 1, 10, 20, and 40; apply to lesson, daily, answer, prize, and course completion sources | Caps enforced; multiplier equals min(2.0, 1.0 + 0.05 x days); applied only to eligible sources, never to prizes | FR-RWD-002, TM-LRN-001 | P1 | A |
| TC-0518 | UT | Split prizes with 12 entrants, with 6 entrants, and with ties | 50, 30, 20 percent for 10 or more entrants; winner takes all below 10; ties share combined amounts; remainder to the highest placement | FR-RWD-005 | P2 | A |
| TC-0519 | IT | Attempt a payout from an unfunded prize fund; attempt to mint points for a prize | Rejected with an alert; only funded accounts can pay | FR-RWD-013, SEC-052, SEC-054 | P1 | A |
| TC-0520 | IT | Drive issuance to 80 and 100 percent of the monthly ISSUANCE budget | Alerts fire at each threshold; behavior at 100 percent follows the configured policy | FR-RWD-002, SEC-079 | P2 | A |
| TC-0521 | IT | A Free user at 100 playground executions runs lesson exercises and a playground run | Exercises still run within their own rate limit; the playground run is refused with the upgrade message | FR-EXE-006, FR-LRN-010 | P1 | A |
| TC-0522 | UT | Award XP that crosses a tier threshold; read total XP | Tier promotes once; surplus carries to the next tier; total XP equals the sum across tiers | FR-LRN-005, FR-LRN-001 | P2 | A |
| TC-0523 | IT | Change an earning rate in configuration, then post earnings before and after the effective date | Each ledger transaction records its configuration version; only new postings use the new rate; the change is audited | FR-RWD-002, SEC-074 | P2 | A |
| TC-0524 | CT | Contract test over OpenAPI 0.2.0 responses for dashboard, balance, leaderboard, and progression | Separate fields xp\_total, learning\_points, prize\_points, competition\_score; no field named points carries XP or score | FR-CMP-006, FR-RWD-003, FR-RWD-012 | P1 | A |

### Updated coverage summary (v0.3)

| Measure | Result |
| --- | --- |
| Total cases | 169 |
| Functional requirements / Must | 92 / 56 (all 56 Must have a case) |
| High threats with a case | 23 of 23 |
| Security controls covered by a case | 92 of 104 (12 rely on process evidence) |
| Non-functional requirements with a case | 26 of 26 |
| Should and Could requirements without a case | 24 |
