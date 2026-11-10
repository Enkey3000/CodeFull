# CodeFull Execution Guide

**Doc ID:** EXG-001 | **Version:** 0.1 draft | **Status:** for team onboarding | **Owner:** Delivery lead **Upstream:** all CodeFull documents (PRD, SRS, ARCH, SEC, OpenAPI, TP, TM, TC, UAT, REL, RTM, IRP, PTP, POC, MVP, PB, GAP) | **Companion files:** cursorrules.md, cursorsecurityrules.md

## 1. Purpose

This guide explains how the team runs the work: who does what, how a task moves from idea to production, what "done" means, which documents govern which decisions, and how the first 30 days unfold. It is the entry point for a new engineer and the operating manual for the delivery lead.

## 2. The Document Map (what governs what)

| Question | Governing document |
| --- | --- |
| What are we building and why? | PRD-001 |
| What must it do, exactly? | SRS-001 (FR, NFR) |
| How is it built? | ARCH-001 (ADRs), POC-001 results |
| How is it protected? | SEC-001, TM-001, cursorsecurityrules.md |
| What does the API look like? | openapi.yaml (and AsyncAPI when written) |
| In what order do we build? | MVP-001 slices, PB-001 steps |
| How do we prove quality? | TP-001, TC-001, RTM-001, UAT-001 |
| How do we ship and recover? | REL-001, IRP-001 |
| How do we attack ourselves? | PTP-001 |
| What is still missing? | GAP-001 |
| How should AI assistants behave in the repo? | cursorrules.md, cursorsecurityrules.md |

When documents disagree, the order of authority is: signed-off PRD, SRS, ARCH (with approved ADRs), SEC, then everything else. Raise the conflict and fix it in the document in the same pull request that exposes it.

## 3. Roles and RACI

| Role | Responsibility |
| --- | --- |
| Product owner | Scope, priorities, acceptance, UAT, economy and pricing decisions |
| Delivery lead | Plan, cadence, risks, tracker, gates, working agreements |
| Architect | ADRs, PoC decisions, cross-service design, technical risk |
| Tech leads (backend, frontend, execution, platform) | Slice delivery, code quality, reviews in their area |
| Security lead | Controls, threat model, security reviews, pen tests, exceptions |
| QA lead | Test strategy, RTM, release evidence, defect process |
| SRE and DevOps | Environments, pipelines, observability, on-call, drills |
| Content lead | Lessons, challenges, hidden tests, review pipeline |
| Legal and compliance | Policies, consent, contest rules, regulatory notices |
| Support and moderation lead | Support tooling, moderation policy and queue |

| Activity | Product | Delivery | Architect | Security | QA | SRE | Legal |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Scope change | A | R | C | C | C | I | C |
| Architecture decision (ADR) | C | I | A/R | C | I | C | I |
| Security exception | C | I | C | A/R | I | I | C |
| Slice acceptance | A | R | C | C | R | I | I |
| Release go/no-go | A | R | C | R | R | R | C |
| Incident command | I | I | C | R | I | A/R | C |
| Policy and legal documents | C | I | I | C | I | I | A/R |

(R responsible, A accountable, C consulted, I informed.)

## 4. Cadence

| Ritual | Frequency | Purpose |
| --- | --- | --- |
| Sprint planning and review | Every 2 weeks | Commit to playbook steps; demo working slices to Product |
| Daily standup | Daily, 15 minutes | Blockers and coordination |
| Architecture and security review | Weekly, 45 minutes | ADRs, threat model changes, PoC and design questions |
| RTM and quality review | Weekly | Coverage, defects, flaky tests |
| Risk and gap review | Weekly | GAP backlog, risk register, decisions due |
| Release readiness | At each gate | Go/no-go with evidence |
| Retrospective | Every sprint | Process improvement |
| Stakeholder update | Every 2 weeks | Progress, risks, KPIs |

## 5. How Work Flows

1. **Pick a step.** Take the next playbook step (PB-nn) for the active slice; if none fits, write a new step with inputs, verification, and traces before starting.
2. **Definition of ready:** governing requirement IDs identified; acceptance criteria clear; dependencies available; security impact assessed; test cases identified (TC IDs); designs available for UI work.
3. **Branch and build:** branch name feat/PB-nn-slug; tests first for risky areas; contract first for API changes; small commits (Conventional Commits with IDs).
4. **Pull request:** description covers what changed, IDs, how it was tested, flag and rollout notes, security considerations, screenshots for UI; automated checks must pass (TP-001 section 4).
5. **Review:** one code owner approval, plus Security review for sensitive areas (auth, tenancy, ledger, sandbox, crypto, AI gateway); no self-merge.
6. **Merge and deploy:** trunk-based; unfinished work stays behind flags; deploy to staging automatically; production by the release process.
7. **Verify and close:** slice demo, test evidence, RTM green, tracker updated.

### Definition of done (per step and slice)

- Acceptance criteria met and demonstrated.
- Unit, contract, integration, and relevant security cases written and passing (cited by TC ID).
- OpenAPI x-requirement and test requirement markers updated; RTM generator green.
- No new critical or high findings from SAST, dependency, secret, or image scans.
- Observability in place (traces, metrics, logs without sensitive data) and runbook notes updated.
- Accessibility checked for new UI; loading, empty, and error states present.
- Documentation updated: SRS or ADR if behavior or design changed; playbook if the process changed.
- Flag and rollback path verified.

## 6. Working With the Cursor Rule Files

- Place cursorrules.md and cursorsecurityrules.md in the repository root (or map them to the editor's project rules folder) so every AI-assisted session loads them.
- Start each AI session with the playbook step and the standard step wrapper from PB-001 section 1; ask the assistant to restate the requirement and list files before changing code.
- Review AI-written code as you would any contribution: tests, security rules, and traces apply equally; the assistant never approves its own work.
- When a rule needs to change, change the governing document first (SRS, ARCH, or SEC), then update the rule files in the same pull request.

## 7. Environments and Bootstrap

| Step | Action |
| --- | --- |
| 1 | Get repository and cloud access through the onboarding request; MFA is mandatory |
| 2 | Install the toolchain (Python 3.12, Go, Node 20, Docker, Terraform, kubectl, Helm, Vault CLI, pre-commit) with the repository bootstrap script |
| 3 | Run make bootstrap to start local Postgres, Redis, NATS, and Keycloak in containers with seeded synthetic data |
| 4 | Run make test and make lint; both must pass before you start |
| 5 | Open a preview environment from a test pull request to confirm the pipeline works for you |
| 6 | Read the documents in the order: PRD, SRS (your domain), ARCH sections 1 to 5, SEC sections 1 to 4, cursorrules.md, cursorsecurityrules.md, your slice in PB-001 |

Secrets are never copied locally; development uses synthetic credentials and Vault dev mode. Production access is limited to on-call roles and is time-bound.

## 8. Tracking and Metrics

**Tracker:** one board with columns Backlog, Ready, In progress, In review, Verify, Done; each card carries PB-nn, requirement IDs, and test IDs. A separate GAP and decision log lists owner, due milestone, status, and resolution link.

| Metric | Target or use |
| --- | --- |
| Slice progress against MVP-001 plan | Weekly burn-up |
| RTM coverage and Must requirements passing | 100% by beta gate |
| Lead time and deployment frequency | DORA trend |
| Change failure rate and time to restore | Improve release safety |
| Defect escape rate and open Sev 1 or Sev 2 | Zero open at gates |
| Security findings by severity and age | Within SEC-100 SLAs |
| Flaky test rate | under 1% |
| PoC and ADR decisions made on time | Track against POC schedule |
| Gap backlog burn-down | P0 closed before S0, P1 before dependent slices, P2 before beta |

## 9. Gate Calendar

| Gate | Timing (indicative) | Evidence |
| --- | --- | --- |
| G0 Kickoff ready | Before week 1 | GAP P0 items closed (cloud decision, team, on-call); environments requested |
| G1 Skeleton complete | End of week 2 | S0 demo; CI security gates; RLS linter; observability |
| G2 PoC decisions | Weeks 9 to 10 | POC-1 to POC-6 reports; ADR updates; ADR-015 decision; GAP checkpoint 2 |
| G3 Feature complete | End of S9 | MVP requirements implemented behind flags; RTM status |
| G4 Beta readiness | End of S10 | TP-001 beta gate, pen test PT-1 closed, UAT entry criteria, legal documents, IR tabletop |
| G5 GA readiness | After UAT and KPI check | UAT exit, load targets, restore and failover drill, go/no-go |

## 10. Decisions and Change Control

- **Product scope changes** go through the Product owner; update PRD or SRS and the RTM, and record the reason.
- **Architecture changes** need an ADR with options, decision, and consequences; the Architect and Security lead review it.
- **Security exceptions** need a written entry in the Threat Model residual-risk register with owner, compensating controls, and an expiry of 90 days or less.
- **Decision log:** every decision with date, owner, options considered, outcome, and linked documents. Open questions from the PRD and the GAP list live here until closed.

## 11. Escalation Paths

| Situation | First contact | Escalate to |
| --- | --- | --- |
| Blocked by another team or unclear requirement | Tech lead or Product owner | Delivery lead within 1 business day |
| Security concern or suspected vulnerability | Security lead | Executive sponsor if critical |
| Production incident | On-call (see IRP-001) | Incident commander, per severity |
| Schedule or scope risk | Delivery lead | Product owner and executive sponsor |
| Legal or compliance question | Legal and compliance | Executive sponsor |

## 12. The First 30 Days

| Days | Focus | Outputs |
| --- | --- | --- |
| 1 to 5 | Close GAP P0 items: cloud and platform choices, team roster, on-call plan; stand up repository, CI, and environments (PB-01 to PB-04) | Decisions logged; repository and pipeline running |
| 6 to 10 | Database, DAL, gateway, service template, observability (PB-05 to PB-09); kick off POC-1, POC-3, POC-4 | Walking skeleton plan on track; PoC environments ready |
| 11 to 15 | Web shell and first end-to-end call (PB-10); finalize contract tooling; start content pipeline and challenge authoring | G1 skeleton demo |
| 16 to 20 | Identity slice begins (PB-11 to PB-14); POC-2 and POC-5 start; legal drafting for policies and age rules | Sign-up and onboarding working in staging |
| 21 to 25 | Privacy library, MFA, audit log (PB-15 to PB-17); Gap Analysis refresh; RTM weekly report running | S1 near complete |
| 26 to 30 | Learning slice starts (PB-19 onward); PoC interim findings; hiring or vendor gaps closed | S1 demo; first PoC readouts |

## 13. Onboarding Checklist (new engineer, first two days)

- Access: repository, cloud console (read-only), chat, tracker, documents; MFA enabled.
- Environment: bootstrap script run; make test and make lint pass.
- Reading: documents in the order in section 7, step 6; security rules acknowledged.
- First task: a small playbook step or a documentation fix, merged through the full pull request flow.
- Meet: tech lead, Security lead, QA lead; understand on-call expectations.

## 14. Risk Management

Keep a living risk register (PRD section 13 and POC risks as the starting point) with probability, impact, owner, mitigation, and trigger. Review weekly. Escalate any risk that threatens a gate date, the privacy promise, ledger integrity, or sandbox safety.

## 15. Maintenance of the Document Set

- Each document has an owner and lives in /docs with version history; changes by pull request.
- Run the RTM generator on every change to documents, contracts, or tests.
- Re-baseline the set at each gate and archive the baseline with the release evidence.
- Review this guide every quarter and after each major process change.
