# CodeFull Penetration Testing Plan

**Doc ID:** PTP-001 | **Version:** 0.1 draft | **Status:** for security review | **Owner:** Security lead **Upstream:** TM-001, SEC-001, ARCH-001, IRP-001 | **Downstream:** Release Plan go/no-go, Test Cases (PEN items), RTM

## 1. Purpose and Objectives

Independent penetration testing verifies that the controls in SEC-001 work against a skilled attacker, and finds weaknesses that design reviews and automated scans miss. It satisfies SEC-099.

**Objectives**

1. Prove that untrusted code cannot escape sandboxes or reach internal systems (TM-SBX-001, 003).
2. Prove that tenants, roles, and privacy flags cannot be bypassed (TM-TEN-*, TM-CMP-004, TM-PRV-*).
3. Prove that points, prizes, and redemptions cannot be minted, duplicated, or diverted (TM-RWD-\*).
4. Prove that identity, session, and admin controls resist takeover (TM-AUT-\*).
5. Test AI features for injection, exfiltration, and quota abuse (TM-AI-\*).
6. Test desktop and mobile clients, update paths, and supply chain exposure (TM-CLI-*, TM-INF-*).
7. Produce actionable findings with retests, and evidence for the release gate.

## 2. Scope

| Asset | Environment | Depth | Included in |
| --- | --- | --- | --- |
| Web application and public API (all OpenAPI operations) | Staging | Gray box (accounts and API spec provided) | Pre-beta, pre-GA, annual |
| API gateway, identity (Keycloak), session handling | Staging | Gray box | All engagements |
| Tenant isolation, authorization matrix, privacy flags | Staging | White box for RLS policies and DAL; gray for the rest | All engagements |
| Execution Gateway and sandboxes (gVisor and Firecracker tiers) | Dedicated pen test sandbox pool in staging | White box (policies, images, configs) plus assumed-breach scenarios | Pre-beta, pre-GA, annual and after major isolation changes |
| Ledger, rewards, billing, webhooks, redemption workflows | Staging with provider sandboxes | Gray box | Pre-GA onward |
| Realtime hub (battles, scoreboard, spectators) | Staging | Gray box | When battles ship (FF) |
| AI Gateway | Staging with a test provider key | Gray box | Pre-GA onward |
| Cloud and Kubernetes configuration, CI/CD, secrets management | Staging and build plane | Configuration review plus targeted testing | Pre-GA and annual |
| Desktop app (Tauri) and installers, update channel | Test builds | Gray box | When desktop ships |
| Mobile apps (Android, iOS) | Test builds | Gray box with MASVS L2 | When mobile ships |
| Marketing site and docs | Production (read-only checks) | Black box | Annual |

**Out of scope:** production data stores and customer accounts; third-party systems (Stripe, identity federation, cloud provider infrastructure, app stores) except for how CodeFull configures and calls them; volumetric denial of service beyond agreed limits; physical and social engineering of staff unless explicitly added.

## 3. Schedule and Triggers

| Engagement | Timing | Duration | Gate it supports |
| --- | --- | --- | --- |
| PT-1 Pre-beta | After MVP feature complete and TP-001 beta entry gate | 2 to 3 weeks plus retest | Beta go/no-go |
| PT-2 Pre-GA | After beta fixes, before GA | 3 weeks plus retest | GA go/no-go |
| PT-3 Feature-driven | Before battles, redemption, desktop, mobile, or Enterprise SSO ship | 1 to 2 weeks each | Feature release |
| PT-4 Annual | Every 12 months | 3 to 4 weeks | SOC 2 readiness, customer assurance |
| PT-5 Event-driven | After major architecture, sandbox, or auth changes, or after a SEV 1 | As needed | Change approval |
| Continuous | After GA | Ongoing | Bug bounty program (SEC-104) |

## 4. Standards and Methodology

- **Web and API:** OWASP ASVS Level 2, OWASP WSTG, OWASP API Security Top 10.
- **Mobile:** OWASP MASVS Level 2 and MASTG.
- **Cloud and Kubernetes:** CIS benchmarks and vendor hardening guides.
- **Sandbox and container escape:** CIS container guidance plus custom red-team scenarios (section 6).
- **Reporting:** CVSS v3.1 or v4.0 base score plus business impact rating; findings mapped to SEC and TM IDs.

## 5. Vendor and Team Requirements

- Independent firm with documented experience in container and sandbox security, API and authorization testing, fintech-style logic abuse, and mobile.
- Named testers with relevant certifications or demonstrable research; no subcontracting without approval.
- Background-checked staff; signed NDA and data handling agreement; liability insurance.
- Rotation of vendors every 2 to 3 engagements, with an internal red team supplementing between engagements.

## 6. Objective-Driven Scenarios

| ID | Objective | Starting point | Success for the attacker | Linked threats | Linked cases |
| --- | --- | --- | --- | --- | --- |
| PT-S1 | Escape the sandbox | Authenticated user submitting code | Code execution on the host, access to another job, or any network path to internal ranges | TM-SBX-001, 003, 004 | TC-1203, 1204, 1205, 1208, 1210 |
| PT-S2 | Break tenant isolation | Two users in different tenants plus an org admin | Read or write another tenant's rows; bypass RLS through DAL misuse | TM-TEN-001, 004, 006 | TC-1104, 1105 |
| PT-S3 | IDOR and function-level abuse | Learner account | Access or modify another user's resources or admin functions | TM-TEN-002, TM-AUT-003 | TC-1101, 1102 |
| PT-S4 | Forge identity | Network access to internal services from a compromised pod (assumed breach) | Reach a service with forged signed headers | TM-TEN-003 | TC-1103 |
| PT-S5 | Mint or duplicate points | Learner and competitor accounts | Double credits through replay, race, or client-supplied values | TM-RWD-001, 002 | TC-0403, 0506, 0508 |
| PT-S6 | Redeem fraudulently | New account with scripted behavior | Redemption without holds, step-up, or attestation | TM-RWD-005 | TC-0507, 1115 |
| PT-S7 | Manipulate prize settlement and pools | Competitor accounts | Alter payouts, replay settlement, or game pool caps | TM-RWD-007, 008 | TC-0505, 0511 |
| PT-S8 | Deanonymize a private entrant | Spectator and learner accounts | Link an Anonymous entry to a person through payloads, timing, or rank deltas | TM-CMP-004 | TC-0404 |
| PT-S9 | Read discreet questions | Learner and non-assigned mentor | Access another user's discreet question | TM-PRV-001 | TC-0602 |
| PT-S10 | Take over an account | Credentials from breach lists, phished session, recovery flow | Access without the owner's factors | TM-AUT-001, 002, 005 | TC-0110, 0111 |
| PT-S11 | Abuse the AI Gateway | Learner account | Extract prompts or other users' context, bypass hints-only mode, evade quotas | TM-AI-001 to 004 | TC-0802 to 0805 |
| PT-S12 | Attack the battle hub | Competitor and spectator accounts | Tamper with clock or scores, flood, or hijack sessions | TM-CMP-003, 005 | TC-0407 |
| PT-S13 | Compromise the desktop shell and updates | Local user and network attacker | Command execution via IPC or webview; install a malicious update | TM-CLI-002, 003 | TC-1114 |
| PT-S14 | Tamper with mobile apps | Rooted device and emulator | Farm rewards or extract tokens and secrets | TM-CLI-001, 005, 006 | TC-1115 |
| PT-S15 | Attack the supply chain and cloud | Developer-level or CI-level foothold (assumed) | Push unsigned images, read secrets, escalate IAM | TM-INF-001, 003, 005 | TC-1110, 1117, 1118 |

### Sandbox red-team track

Provide testers with sandbox images, seccomp and runtime policies, node configuration, and network policies (white box). Scenarios: kernel and runtime exploitation attempts, side channels between co-resident jobs, resource exhaustion that evades limits, abuse of the harness and test-case files, metadata and DNS exfiltration, persistence across jobs, and microVM boundary probes on the hardened tier. Success is any breach of a SEC-039 to SEC-050 control, not only full host compromise.

## 7. Rules of Engagement

- **Environment:** staging at production parity with synthetic data. No testing against production unless explicitly agreed for read-only checks.
- **Accounts:** the team provides test accounts for each role (learner, mentor, recruiter, moderator, admin with MFA test devices) and for two tenants plus one Enterprise org; API specification and non-sensitive architecture documents are shared.
- **Allowed:** authenticated and unauthenticated testing, fuzzing within rate limits, exploit development, post-exploitation within the test environment, assumed-breach starting points agreed in advance.
- **Prohibited:** testing outside the agreed scope or time window; destruction or corruption of shared data without approval; sustained denial of service; attacks on third parties; use of real personal data; retaining customer data; publishing findings without consent.
- **Rate limits and windows:** testing windows published in advance; traffic limits agreed with SRE; a stop word and emergency contact for each side.
- **Deconfliction:** the security team knows the testers' source IPs and schedule so real attacks are not mistaken for tests; detection and response performance is observed and reported as a secondary result.
- **Critical findings:** any critical or any finding showing active risk to production is reported within 24 hours by phone and secure channel, not held for the final report.
- **Data handling:** findings, proof-of-concept code, and evidence are shared through an encrypted channel and deleted by the vendor within 90 days of final acceptance.
- **Safe harbor:** written authorization covers the named testers and scope; legal review confirms compliance with cloud provider testing policies.

## 8. Preparation Checklist (before each engagement)

- Scope, objectives, and schedule signed by Security, Engineering, and Product.
- Staging build frozen to a tagged release; seeded data and accounts prepared; feature flags set as in production candidate.
- Monitoring and alerting enabled and tested so detection can be measured.
- Dedicated sandbox pool provisioned for the sandbox track; sandbox network isolation verified (TC-1210).
- Previous findings retest list prepared; relevant SAST, DAST, and dependency results shared to avoid duplicate work.
- Escalation contacts and on-call coverage confirmed.

## 9. Reporting

Deliverables from the vendor:

1. **Executive summary** with risk posture, key themes, and release recommendation.
2. **Technical report** with each finding: title, severity (CVSS plus business impact), affected assets, SEC and TM IDs, reproduction steps, evidence, root cause, and remediation advice.
3. **Attack narratives** for chained issues (for example how a minor leak enabled a major compromise).
4. **Coverage statement** listing what was tested, what was not, and why.
5. **Retest letter** after remediation.

Severity mapping: critical and high findings follow SEC-100 SLAs (7 and 14 days); medium 30 days; low and informational triaged to the backlog.

## 10. Remediation and Retest

1. Findings are imported into the issue tracker within 2 business days with owner, due date, and linked SEC or TM IDs.
2. A fix includes a regression test (for example added to TC-11xx or TC-12xx) and a threat model update if a new abuse case was found.
3. The vendor retests all critical and high findings and a sample of medium findings; retests occur within 30 days of the final report.
4. Accepted risks require written approval by the Security lead and Product owner and are recorded in the Threat Model residual risk register with an expiry date.

## 11. Acceptance Criteria (release gates)

| Gate | Criteria |
| --- | --- |
| Beta | No open critical or high findings; all sandbox-track findings of any severity triaged; privacy and tenant isolation objectives (PT-S2, S3, S8, S9) passed |
| GA | No open critical or high findings; PT-S1, S5, S6, S10 passed with retest; medium findings have scheduled fixes; detection coverage reviewed |
| Feature release | Findings for that feature's scenarios closed or accepted |

## 12. Measuring Detection and Response

Alongside findings, record how the defenders performed: which test actions triggered alerts, time to detect, time to contain in simulated incidents, and gaps in logging. Feed the results into SEC-079, the Incident Response Plan drills (IRP-001 section 11), and alert tuning.

## 13. Roles and Budget Planning

| Role | Responsibility |
| --- | --- |
| Security lead | Owns the program, vendor relationship, risk acceptance proposals |
| Engineering lead | Provides environments, assigns fixes, tracks SLAs |
| SRE | Monitoring, rate limit agreements, environment health |
| Product owner | Participates in risk acceptance and release decisions |
| Legal | Authorization letters, data handling terms, disclosure rules |

Budget placeholders to confirm with vendors: PT-1 and PT-2 (3 weeks each, two to three testers), annual engagement, feature-driven short engagements, and a retest allowance. The sandbox track is the largest cost driver.

## 14. Risks and Open Items

- Staging parity: sandbox and cloud behavior must match production, or findings may not transfer.
- Vendor availability: book engagements at least 8 weeks ahead of the gate they support.
- Findings volume: reserve engineering capacity (about 20% of a sprint) for remediation after each engagement.
- Open: choose the vendor shortlist, decide when to launch the bug bounty (post GA), confirm cloud provider testing notification rules, and define the internal red team capacity.
