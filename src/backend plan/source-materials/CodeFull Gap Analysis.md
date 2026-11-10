# CodeFull Gap Analysis

**Doc ID:** GAP-001 | **Version:** 0.1 (Checkpoint 1) | **Status:** for product and engineering review | **Owner:** Product owner + Architect **Inputs:** interactive prototype (codefull.html), PRD-001, SRS-001, ARCH-001, SEC-001, TM-001, TP-001, TC-001, UAT-001, REL-001, RTM-001, POC-001, MVP-001, PB-001 **Downstream:** Playbook updates, Execution Guide backlog, Release go/no-go

## 1. Purpose and Method

The Gap Analysis measures the distance between where the project is and where the MVP needs to be, and turns that distance into a prioritized backlog. It runs at three checkpoints:

| Checkpoint | Timing | Focus |
| --- | --- | --- |
| 1 (this document) | After SRS, Architecture, and Security baselines | Prototype versus target; specification gaps and inconsistencies; readiness gaps |
| 2 | After PoC decisions | PoC results versus assumptions; architecture and scope changes; cost model |
| 3 | Before beta | Build versus RTM; test, security, operations, and legal readiness |

**Dimensions:** functional, non-functional, security and privacy, data and content, operations and support, legal and compliance, team and tooling, specification quality.

**Scoring:** Impact 1 to 5 (5 = blocks launch or creates serious trust, legal, or security risk); Effort S (days), M (weeks), L (months); Needed by: the latest milestone at which the gap must be closed. Priority follows impact and the needed-by date.

## 2. Readiness Scorecard (Checkpoint 1)

| Dimension | Status | Summary |
| --- | --- | --- |
| Product definition | Green | PRD, SRS, MVP scope baselined; some product decisions open (section 4.2) |
| Architecture | Amber | Complete on paper; capacity, cost, and sandbox feasibility unproven until PoCs |
| Security design | Green | 104 controls, 72 threats, pen test and incident plans written; verification gaps listed in RTM-001 |
| Test and quality design | Amber | 126 cases and 35 UAT scenarios; 21 security controls, 5 NFRs, and 8 Must items need cases or dispositions |
| Prototype and implementation | Red | Prototype is a clickable design reference only; no backend, persistence, or real execution |
| Content | Red | Learning track and challenges not yet authored; no pipeline or reviewers named |
| Legal and compliance | Red | Age policy, terms, privacy policy, contest rules, and consent flows not yet drafted |
| Operations and support | Amber | IR and release plans written; staffing, tooling, and moderation operations not set |
| Team and tooling | Amber | Skills and capacity for Go, Python, Kubernetes, and sandboxing to be confirmed |

## 3. Findings: Prototype versus Target

The prototype (a single HTML file) is valuable as a design and flow reference. These items describe what must change to reach the MVP.

| ID | Area | Gap | Impact | Effort | Needed by | Action | Traces |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GAP-001 | Functional | No authentication, sessions, or identity; every page is open with a hard-coded user | 5 | L | S1 | Build identity slice (Keycloak, gateway, identity service) | FR-IDN-001 to 006; SEC-001 |
| GAP-002 | Functional | All data is hard-coded in script templates; no API or persistence | 5 | L | S1 to S9 | Contract-first port to React with the generated SDK | OpenAPI; ADR-012 |
| GAP-003 | Functional | Playground output is simulated; the editor is a plain editable block without highlighting or language services | 5 | L | S3 | Real runner via the Execution Gateway; adopt a code editor component | FR-EXE-001; SEC-039 |
| GAP-004 | Quality | Only happy paths exist; no loading, empty, or error states | 3 | M | S10 | Add the three states to every data view; TC-1405 | PRD sec 11 |
| GAP-005 | Accessibility | Clickable elements without keyboard support or roles, controls without labels, and secondary text colors likely below the 4.5:1 contrast ratio on dark surfaces (verify) | 4 | M | S10 | Accessible components and token contrast checks; TC-1401, 1402, 1406 | NFR-019 |
| GAP-006 | Structure | One file using document.write, inline event handlers, and script-driven navigation; no routes or deep links | 4 | L | S1 | Componentize with a router and URL-addressable pages | ARCH-001 sec 11 |
| GAP-007 | Privacy | Visibility toggles are cosmetic; nothing is enforced on a server | 4 | M | S1, S4 | Shared privacy library and server-side enforcement; TC-0105, TC-0404 | FR-IDN-005; SEC-017 |
| GAP-008 | Security | Inline handlers and string-built HTML make a strict CSP impossible and invite XSS once user content is shown | 4 | M | S1 | Framework escaping, no inline handlers, strict CSP; TC-0604 | SEC-024, 027 |
| GAP-009 | Content | Placeholder claims and dates (128K coders, $2.4M prizes, live counts, 2025 dates, Prototype build label) | 3 | S | Beta | Remove or replace with real data; never publish placeholders as facts | PRD sec 16 |
| GAP-010 | Design system | Tokens retuned to the logo, but not packaged; no component library or documented states; no decision on an AI accent color | 3 | M | S1 | Create the shared theme package and component set; confirm palette rules | cursorrules sec 8 |
| GAP-011 | Responsive | Mobile drawer exists, but tool pages use fixed heights and wide tables that need verification at 320 px | 2 | S | S10 | Responsive pass; TC-1404 | NFR-021 |
| GAP-012 | Realtime | Battle and live scoreboard pages are static | 3 | L | F1 (fast follow) | Realtime hub after POC-2 | FR-CMP-008, 009 |

## 4. Findings: Specification and Product Decisions

### 4.1 Inconsistencies found while reconciling the prototype with the SRS

| ID | Area | Gap | Impact | Effort | Needed by | Action | Traces |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GAP-013 | Ranking metric | The prototype shows 12,480 as the leaderboard score, total XP, and points on different pages, while the points balance is 2,140 and lifetime earned is 8,920. XP, spendable points, and rank score are conflated | 5 | S | Before S5 | Decide the ranking metric (for example competition rating or lifetime points) and update FR-CMP-006, FR-RWD-002, and the UI copy | FR-CMP-006; FR-RWD-002 |
| GAP-014 | Discreet questions | FR-COM-002 needs an assigned mentor, but the mentor marketplace is fast-follow | 4 | S | Before S8 | Define an MVP rule: a small invited mentor pool with queue assignment, or limit visibility to the asker and moderators until mentors launch | FR-COM-002; SEC-018 |
| GAP-015 | Rewards | Points have no way to be spent at MVP (redemption is fast-follow), which may weaken motivation and BG-03 | 3 | M | Before S5 | Add a small sink (for example course vouchers or Pro days) or state the plan and show value clearly | PRD sec 5, 9; FR-RWD-006 |
| GAP-016 | Learning | XP thresholds could be per tier or cumulative | 3 | S | Before S2 | Confirm in SRS section 8 | FR-LRN-005 |
| GAP-017 | Quotas | Unclear whether interactive lesson exercises consume the Free plan execution quota | 3 | S | Before S6 | Decide and document; exercises should likely be exempt | FR-EXE-006; FR-LRN-010 |
| GAP-018 | Economy | Earning rates, redemption values, and plan limits are planning values only | 4 | M | Before S5 | Model the economy and fraud exposure; set values in a configuration spec | SRS sec 8 |
| GAP-019 | Realtime and notifications | No AsyncAPI specification for battles, notifications, or run streams | 3 | S | F1 and S3 | Write AsyncAPI; move traces to operation level | RTM-001 sec 5.6 |
| GAP-020 | Traceability | 21 security controls, 5 NFRs, 8 Must items without UAT, and 15 threats lack direct cases | 4 | M | S10 | Close per RTM-001 sections 5.1 to 5.4 | RTM-001 |

### 4.2 Decisions still open

| ID | Decision | Owner | Needed by |
| --- | --- | --- | --- |
| GAP-021 | Cloud provider and region; nested virtualization or bare metal for the hardened tier; managed versus self-hosted Keycloak, Temporal, NATS, OpenSearch | Architect | Before PoC start |
| GAP-022 | Approve ADR-015 (MVP simplifications) | Architect, Product | After PoC review |
| GAP-023 | Final pricing and Free versus Pro limits; whether Starter waits for fast-follow | Product | Before S6 |
| GAP-024 | First two languages and the content authoring owner | Product, Content lead | Before S2 |

## 5. Findings: Readiness (Legal, Content, Operations, Team)

| ID | Area | Gap | Impact | Effort | Needed by | Action |
| --- | --- | --- | --- | --- | --- | --- |
| GAP-025 | Legal | No minor-user and age policy; affects sign-up, rewards, recruiter visibility, and data handling | 5 | M | Before beta recruitment | Legal sets policy; add age gate and parental consent if needed |
| GAP-026 | Legal | Terms of service, privacy policy, cookie and analytics consent, contest and rewards rules, data processing terms, and a DSAR procedure not drafted | 5 | M | Before beta | Legal drafts; wire consent records (SEC-077) |
| GAP-027 | Content | No authoring pipeline, review process, licensing and ownership terms; hidden test quality assurance for challenges | 5 | L | S2 start | Name a content lead; build import and review workflow; plan QA of challenges |
| GAP-028 | Operations | Moderation staffing, SLAs, content policy, appeals, and tooling undefined | 4 | M | Before beta | Define policy and rota; set response targets |
| GAP-029 | Operations | Support tooling, status page, known-issues page, and help content not chosen | 3 | S | Before beta | Select tools; draft templates |
| GAP-030 | Cost | Sandbox, AI, and hosting unit costs unvalidated | 5 | M | PoC review | Use POC-1 and POC-5 measurements; build the cost model and margin check per plan |
| GAP-031 | Team | Skills and capacity for Go, Python, Kubernetes, sandbox security, and on-call rota not confirmed | 4 | M | Before S0 | Confirm roster, hire or contract, set on-call |
| GAP-032 | Vendors | Email, push, analytics, and error tracking vendors not selected | 2 | S | S1 | Choose and configure; respect consent |
| GAP-033 | Security program | Pen test vendor shortlist and booking lead time (about 8 weeks) | 3 | S | Before S9 | Shortlist and book PT-1 |

## 6. Prioritized Remediation Backlog

**P0: resolve before the first build sprint (S0 and S1 start)** GAP-021 cloud and platform decisions; GAP-031 team and on-call; GAP-001, 002, 006 and 008 are addressed by the plan itself (S0 and S1); GAP-010 design system package.

**P1: resolve before the slice that depends on them** GAP-016 XP interpretation (before S2); GAP-024 languages and content owner and GAP-027 content pipeline (before S2); GAP-013 ranking metric, GAP-015 points sink, GAP-018 economy (before S5); GAP-017 quota rules and GAP-023 pricing (before S6); GAP-014 mentor rule (before S8); GAP-019 AsyncAPI (before S3 and F1).

**P2: resolve before beta** GAP-025 age policy, GAP-026 legal documents, GAP-028 moderation operations, GAP-029 support tooling, GAP-033 pen test booking, GAP-020 RTM gaps, GAP-004, 005, 007, 009, 011 delivered through the slices and hardening.

**Decision points from PoCs:** GAP-022 (ADR-015) and GAP-030 (cost model) close at the PoC review.

## 7. Updating This Analysis

- Checkpoint 2 re-scores each gap against PoC results and adds new gaps from measured limits (for example sandbox cost or hardened tier viability).
- Checkpoint 3 compares build status with the RTM and re-runs the readiness scorecard; any Red item blocks the go/no-go unless an approved exception exists.
- Each gap has an owner, due milestone, and status (open, in progress, closed, accepted) tracked in the Execution Guide backlog; closed gaps link to the pull request, decision record, or document version that resolved them.

## 8. Follow-up After Checkpoint 1

Supporting documents added since this analysis, and what they do to the gap list:

| Document | Gaps affected | Status |
| --- | --- | --- |
| ECO-001 Points Economy Specification | GAP-013 ranking metric (proposal: Competition Score), GAP-015 points sink (proposal: MVP catalog), GAP-016 XP interpretation (proposal: per tier), GAP-017 quota for exercises (proposal: exempt), GAP-018 economy values (proposed values) | Proposals written; each needs a Product owner decision; GAP-018 stays open until tuned with beta data |
| DM-001 Data Model Specification | Supports GAP-002, GAP-007, and the S1 to S9 slices | Draft; update after POC-3 and POC-4 |
| DS-001 Design System Specification | GAP-005 (contrast confirmed with computed ratios and replacement tokens), GAP-010 (tokens, components, and states defined), GAP-006 and GAP-008 (component and handler rules) | Draft; logo master SVGs and AI accent decision outstanding |
| CPP-001 Content and Policy Readiness Pack | GAP-025 age policy options, GAP-026 legal document checklist, GAP-027 content authoring guide and pipeline, GAP-028 moderation policy, GAP-029 support plan | Drafted for Legal, Content, and Operations to own; no legal text; decisions and owners still required |
| asyncapi.yaml | GAP-019 | Closed (specification written; validation with an AsyncAPI tool pending) |
| Test Cases v0.2, UAT v0.2, RTM v0.2 | GAP-020 | Closed for the items listed in RTM-001 section 9; 24 Should and Could requirements still need cases |

Still open and not solvable by documentation alone: GAP-021 cloud and platform decisions, GAP-030 cost model (needs PoC measurements), GAP-031 team and on-call readiness, GAP-023 pricing, GAP-024 first languages and content owner, and the legal drafting itself (GAP-025, GAP-026).
