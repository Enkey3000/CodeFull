# CodeFull Incident Response Plan

**Doc ID:** IRP-001 | **Version:** 0.1 draft | **Status:** for security and operations review | **Owner:** Security lead + SRE lead **Upstream:** SEC-001, TM-001, ARCH-001, REL-001 | **Downstream:** Pen Testing Plan, Execution Guide, RTM

## 1. Purpose and Scope

This plan defines how CodeFull detects, responds to, communicates about, and learns from incidents. It covers security incidents (sandbox escape, tenant data exposure, credential leaks, abuse), integrity incidents (ledger, scoring, battles), and availability incidents (outages, provider failures) across all platforms. It satisfies SEC-098 and is exercised in the drills in section 11.

**Principles:** protect users and their money-like points first; contain before investigating deeply; keep humans in control (no automated model decides containment); preserve evidence; communicate early and honestly; fix causes, not symptoms; run blameless reviews.

## 2. Definitions

| Term | Meaning |
| --- | --- |
| Event | Any observable occurrence (an alert, a report) |
| Incident | An event that harms or threatens confidentiality, integrity, availability, or fairness |
| Incident commander (IC) | Single decision maker for the incident |
| Containment | Actions that stop the harm from spreading, even if temporary |
| PIR | Post-incident review |

## 3. Severity Levels

| Level | Definition and examples | Acknowledge | IC assigned | Update cadence | Notify |
| --- | --- | --- | --- | --- | --- |
| SEV 1 | Active compromise or data loss, or core service down. Sandbox escape; cross-tenant data exposure; identity of private entrants exposed; ledger corruption or double payouts; credential or signing key leak; full outage over 5 minutes | 5 min | 15 min | 30 min | Executives, Legal, all responders immediately |
| SEV 2 | Major degradation or contained security issue. Judging queue saturated; battles failing; billing sync broken; abuse campaign contained by controls | 15 min | 30 min | 60 min | Engineering leadership, Support |
| SEV 3 | Minor degradation or isolated defect with workaround | 4 hours | Next business day | Daily | Owning team |
| SEV 4 | Low impact, cosmetic, or informational | Next business day | Not required | As needed | Owning team |

When unsure, declare the higher severity and downgrade later. Any suspected security or ledger incident is at least SEV 2 until proven otherwise.

## 4. Roles

| Role | Responsibilities |
| --- | --- |
| Incident commander | Owns decisions and the timeline; assigns roles; declares severity changes and resolution |
| Operations lead | Technical response: containment, recovery, runbooks |
| Security lead | Investigation, forensics, threat assessment; leads INC-1, INC-3, INC-4 |
| Communications lead | Internal updates, status page, user notices, press; keeps one voice |
| Scribe | Timestamped log of facts, decisions, and actions |
| Legal and compliance | Regulatory and contractual notification decisions, privilege |
| Support lead | User tickets, macros, escalation of user reports |
| Product owner | Business impact decisions, feature flag trade-offs |
| Executive sponsor | Resources and external escalation for SEV 1 |

One person may hold several roles in a small team, but the IC never also does the hands-on fix in a SEV 1.

## 5. On-Call and Escalation

- 24x7 primary and secondary on-call for platform, plus a security on-call; weekly rotation; handoff notes required.
- Paging through the alerting platform; acknowledgment required within the SEV 1 target or the page escalates to the secondary, then to the engineering lead.
- A dedicated incident channel and video bridge are created per SEV 1 or SEV 2; naming convention inc-YYYYMMDD-short-name.
- Anyone can declare an incident; contact method is documented in the runbook index and pinned in the support channel.

## 6. Detection Sources

Alerts on ledger invariants and reconciliation (SEC-058), sandbox policy violations and egress attempts (SEC-041, 046), auth anomalies and rate-limit saturation (SEC-007, 029), error budget burn and SLO alerts, secret scanning and CI findings (SEC-083), cloud audit anomalies, user reports and moderation flags, pen test and bug bounty reports, provider status notices (Stripe, identity, AI, cloud).

## 7. Response Lifecycle

1. **Detect and declare:** confirm the signal, open the incident channel, set severity, appoint IC and scribe.
2. **Triage (first 15 minutes):** what is affected, since when, who is impacted, is harm ongoing, is data or money involved.
3. **Contain:** use the safest reversible action first (feature flag off, route block, revoke credentials, quarantine nodes). Fail closed for money and identity.
4. **Preserve evidence:** snapshots, logs, audit records, affected rows (copy, never alter), chain-of-custody notes.
5. **Eradicate:** remove the cause (patch, rebuild from clean images, rotate secrets, remove malicious accounts).
6. **Recover:** restore service in stages; verify with smoke tests, reconciliation, and monitoring; re-enable flags progressively.
7. **Communicate:** per section 9 throughout.
8. **Close:** IC declares resolution when impact has ended and monitoring is stable for an agreed period.
9. **Review:** PIR within 5 business days; actions tracked to closure.

## 8. Playbooks

Each playbook lists the trigger, the first actions, containment, recovery, communication, and linked controls and threats. All containment steps assume the feature flags in FR-PLT-005 are available to the on-call team.

### INC-1 Sandbox escape or suspected host compromise

- **Triggers:** policy violation or kernel audit alerts; unexpected egress from sandbox pools; unexplained node behavior; pen test or external report.
- **First actions:** disable execution for the affected tier through the flag; cordon and network-quarantine affected nodes; snapshot nodes and logs for forensics; identify the submitting account and suspend it.
- **Containment and investigation:** confirm no credentials were reachable from sandboxes (they should have none); review all jobs that ran on the node in the window; check for lateral movement in the cluster and cloud audit logs.
- **Recovery:** rebuild node pools from clean images; patch and update seccomp and runtime policy; run the escape suite (TC-1201 to TC-1210) before re-enabling; reopen the hardened tier first, then the standard tier.
- **Communication:** SEV 1 internal immediately; users informed if data or results were affected; Legal assesses notification duties.
- **Links:** SEC-039 to SEC-050; TM-SBX-001, TM-SBX-003.

### INC-2 Ledger mismatch or double payout

- **Triggers:** reconciliation alert; invariant violation; complaint of wrong balance or duplicate prize.
- **First actions:** turn off redemption and prize settlement flags (fail closed); pause related workflows; snapshot ledger tables and workflow histories.
- **Containment and investigation:** determine the time range, accounts, and cause (replay, race, defect, fraud, insider); never edit or delete ledger rows; prepare compensating entries with dual approval.
- **Recovery:** post approved compensating entries; re-run reconciliation; re-enable flags progressively; monitor closely for 48 hours.
- **Communication:** affected users told what happened and what was corrected; Finance and Legal informed for monetary effects.
- **Links:** SEC-051 to SEC-059; TM-RWD-001, TM-RWD-003, TM-RWD-005.

### INC-3 Credential, key, or secret leak

- **Triggers:** secret scanning alert; external disclosure; anomalous Vault or cloud access.
- **First actions:** identify the secret type and scope; revoke and rotate immediately through Vault; invalidate sessions or signing keys if affected.
- **Containment and investigation:** search audit logs for use of the secret; scrub history where feasible; check dependent systems; assess whether data was accessed.
- **Recovery:** confirm rotation completed everywhere; add a detection rule for the leak path; update developer guidance.
- **Links:** SEC-031 to SEC-037, SEC-083; TM-INF-002, TM-INF-003.

### INC-4 Personal data breach or tenant isolation failure

- **Triggers:** cross-tenant access in logs or reports; exposure of discreet questions or private-entry identity; bulk export anomalies.
- **First actions:** contain by disabling the endpoint or feature through flags or gateway rules; preserve evidence; engage Legal immediately.
- **Investigation:** establish what data, which users or tenants, how long, and whether it was accessed by others; determine root cause (missing RLS, authorization defect, index leak).
- **Notification:** Legal decides on notices. Under GDPR the supervisory authority is notified within 72 hours of becoming aware unless harm is unlikely, and affected individuals without undue delay when risk is high; US state laws and contracts have their own timelines.
- **Recovery:** fix and add regression tests (TC-1102, 1104, 0404, 0602); purge leaked data from indexes and caches; offer support to affected users.
- **Links:** SEC-009 to SEC-020, SEC-075; TM-TEN-001 to TM-TEN-006, TM-CMP-004, TM-PRV-001.

### INC-5 DDoS, scraping, or abuse flood

- **Triggers:** traffic and latency spikes, rate-limit saturation, sandbox queue growth.
- **First actions:** enable stricter WAF and rate limit profiles; block abusive sources; shed non-essential load (search, analytics); protect the execution queue with tighter quotas; protect battles with admission control.
- **Recovery:** scale capacity if needed; keep stricter limits until traffic normalizes; review accounts involved.
- **Links:** SEC-029, SEC-046, SEC-070, SEC-072; TM-API-001, TM-SBX-009, TM-CMP-005.

### INC-6 AI misuse, injection campaign, or model provider incident

- **Triggers:** quota anomalies, reports of leaked prompts or harmful output, provider status incident, suspected key leak.
- **First actions:** tighten per-user quotas; disable AI features by flag if harm is ongoing; rotate provider keys if exposed; preserve transcripts.
- **Recovery:** update delimiting, filters, and eval sets; re-enable gradually; show a degraded-service notice during provider outages while core features continue.
- **Links:** SEC-061 to SEC-067; TM-AI-001 to TM-AI-007.

### INC-7 Payment provider outage or billing anomaly

- **Triggers:** checkout failures, webhook backlog, wrong charges or entitlements.
- **First actions:** confirm entitlement checks are failing open and being logged (FR-BIL-007); queue and retry webhooks; pause new checkout if charges are wrong.
- **Recovery:** reconcile against provider reports; correct entitlements and issue refunds; confirm no card data was logged (SEC-057).
- **Links:** SEC-055, SEC-057; TM-RWD-006.

### INC-8 Battle clock or scoreboard failure

- **Triggers:** wrong standings, clock drift reports, hub crash during a live battle.
- **First actions:** pause the battle and freeze scoring; fail over the hub shard; restore standings from Redis and verify against judged results in Postgres.
- **Recovery:** resume with an extended clock according to published rules or cancel with compensation; publish a clear notice to entrants; hold a short review before the next battle.
- **Links:** SEC-068 to SEC-070; TM-CMP-003.

### INC-0 Unclassified incident

Use the lifecycle in section 7, default to SEV 2, escalate to the Security lead, and create a new playbook after the review if the type recurs.

## 9. Communications

| Audience | Channel | Content and timing |
| --- | --- | --- |
| Responders | Incident channel and bridge | Continuous; scribe posts a summary every update interval |
| Leadership | Email or chat bulletin | SEV 1 immediately, then each update; SEV 2 hourly |
| Users | Status page, in-app banner, email | Acknowledge within 30 minutes for user-visible SEV 1 or 2; plain language, what is affected, what we are doing, next update time |
| Affected users | Direct email or in-app message | Facts about their data or points, what was done, what they should do, contact path |
| Regulators and partners | As directed by Legal | Within legal deadlines |
| Media | Communications lead only | Approved statement |

Templates (kept in the runbook repository): initial notice, update, resolution, breach notification, regulator notice, internal summary. Do not speculate on causes or promise timelines you cannot meet; do not name individuals.

## 10. Evidence and Records

- Preserve logs, snapshots, ledger and audit extracts in a restricted, write-once evidence store with access logging.
- Maintain a decision log (time, decision, who, why) in the incident document.
- Retain incident records for at least 7 years (aligned with the audit log retention in NFR-025).

## 11. Drills and Readiness

| Drill | Frequency | Scope |
| --- | --- | --- |
| Tabletop for INC-1, INC-2, INC-4 | Before beta, then quarterly rotating | Decision making, communications, Legal involvement |
| Technical game day (ledger mismatch, node quarantine, key rotation) | Twice a year | Run the real tooling in staging |
| Paging test | Monthly | Alert delivery and escalation |
| Restore and failover drill | Quarterly | SEC-101, TC-1310 |

Readiness checks before beta: on-call rota staffed, runbooks reviewed, status page live, templates approved, legal contacts confirmed, evidence store ready.

## 12. Post-Incident Review

Within 5 business days of resolution for SEV 1 and SEV 2. Blameless format covering: summary and impact, timeline, detection (how and how fast), root cause and contributing factors, what worked, what did not, action items with owners and due dates, updates required to the threat model, SEC controls, test cases, and runbooks. Action items for SEV 1 are tracked weekly by the engineering lead until closed.

## 13. Metrics

Mean time to acknowledge, to contain, and to resolve by severity; incident count by severity and category; percentage of PIRs completed on time; action item closure rate; drill findings closed; detection source mix (internal alert versus external report).

## 14. Maintenance

Review this plan after every SEV 1, after each drill, and at least every six months. Keep the contact tree, runbook links, and templates current; the Security lead approves changes.
