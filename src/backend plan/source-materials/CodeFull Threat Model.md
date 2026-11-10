# CodeFull Threat Model

**Doc ID:** TM-001 | **Version:** 0.1 draft | **Status:** for security review | **Owner:** Security lead **Upstream:** ARCH-001, SEC-001 | **Downstream:** Test Cases, Pen Testing Plan, Incident Response Plan, RTM

## 1. Method

- **Approach:** STRIDE applied to each element and data flow in the data-flow diagram (section 2), plus abuse cases specific to a competitive, reward-bearing coding platform.
- **Scoring:** Likelihood (L) and Impact (I) each 1 to 5. Score = L x I. Rating: High at 15 or above, Medium 8 to 14, Low below 8. Any threat with Impact 5 and Likelihood 2 or above is rated High regardless of score.
- **STRIDE codes:** S spoofing, T tampering, R repudiation, I information disclosure, D denial of service, E elevation of privilege.
- **Residual risk** is the rating after the listed controls (SEC-nnn in SEC-001) are implemented and verified.
- **Process:** the model is reviewed at each phase gate and whenever a new trust boundary, data flow, or abuse case appears (SEC-088). Each High threat has a test case in TC-001 and a pen test objective.

## 2. Data-Flow Diagram and Trust Boundaries

```
[User device]--TB1--> [CDN/WAF] --> [API Gateway] --TB2--> [Domain services]
  web/desktop/mobile                    JWT, rate limit        |   |   |
                                         signed headers        |   |   +--TB6--> [AI Gateway] --> [AI provider]
                                                               |   |
                                                       gRPC    |   +--TB5--> [Execution Gateway] --TB4--> [Sandboxes]
                                                               v
                                                       [DAL] --TB3--> [Postgres / Redis / NATS / Temporal]

Third parties (TB7): Identity provider, Stripe, PayPal, push services, app stores
Build and run plane (TB8): CI/CD, registry, Terraform, Vault, cloud IAM
```

| Boundary | Crossing | Main concern |
| --- | --- | --- |
| TB1 | Internet to edge | Abuse, injection, token theft |
| TB2 | Gateway to services | Forged identity headers |
| TB3 | DAL to data stores | Tenant isolation, privilege |
| TB4 | Platform to sandbox | Untrusted code containment |
| TB5 | Service to Execution Gateway | Job tampering, quota bypass |
| TB6 | Platform to AI | Prompt injection, data leakage |
| TB7 | Platform to third parties | Webhook forgery, secret handling |
| TB8 | Developers and pipeline to production | Supply chain, over-privilege |

## 3. Threat Register

### 3.1 Authentication and sessions (TM-AUT)

| ID | STRIDE | Threat and abuse scenario | L | I | Rating | Controls | Residual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TM-AUT-001 | S | Credential stuffing leads to account takeover and theft of points | 4 | 4 | High | SEC-001, 002, 003, 007, 008 | Low |
| TM-AUT-002 | S | Stolen refresh token replayed from another device | 3 | 4 | Medium | SEC-002, 005, 006 | Low |
| TM-AUT-003 | E | Admin or moderator account compromised, then flags or payouts abused | 2 | 5 | High | SEC-003, 004, 020, 103 | Low |
| TM-AUT-004 | R | Admin denies a moderation or config action | 2 | 4 | Medium | SEC-074 | Low |
| TM-AUT-005 | S | Account recovery flow abused to hijack accounts | 3 | 4 | Medium | SEC-004, 008 | Low |
| TM-AUT-006 | I | Tokens leak through URLs, logs, or web storage | 3 | 4 | Medium | SEC-005, 073, 091 | Low |

### 3.2 Tenancy and authorization (TM-TEN)

| ID | STRIDE | Threat and abuse scenario | L | I | Rating | Controls | Residual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TM-TEN-001 | I | A table without RLS lets one tenant read another's rows | 3 | 5 | High | SEC-013, 014, 015 | Low |
| TM-TEN-002 | I | IDOR: user changes an id in a request to read or modify another user's object | 4 | 4 | High | SEC-009, 010 | Low |
| TM-TEN-003 | S | Attacker reaches a service directly and sends forged identity headers | 3 | 5 | High | SEC-011, 012 | Low |
| TM-TEN-004 | E | A service uses a privileged database role that bypasses RLS | 2 | 5 | High | SEC-013, 032 | Low |
| TM-TEN-005 | I | Public views expose non-public columns or private entries | 3 | 3 | Medium | SEC-016, 017 | Low |
| TM-TEN-006 | E | Enterprise org admin reaches another org's data or the public tenant | 2 | 5 | High | SEC-010, 014, 015 | Low |

### 3.3 Code execution and sandbox (TM-SBX)

| ID | STRIDE | Threat and abuse scenario | L | I | Rating | Controls | Residual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TM-SBX-001 | E | Kernel or runtime vulnerability lets code escape to the host | 2 | 5 | High | SEC-042, 044, 048, 049 | Medium |
| TM-SBX-002 | D | Fork bomb, memory bomb, or disk fill starves other users | 4 | 3 | Medium | SEC-040, 046 | Low |
| TM-SBX-003 | I | Network egress or SSRF reaches metadata or internal services | 3 | 5 | High | SEC-026, 041, 049 | Low |
| TM-SBX-004 | I | Data from a previous run leaks to the next user through reused sandbox or shared filesystem | 2 | 4 | Medium | SEC-043, 045 | Low |
| TM-SBX-005 | T | Submitted code tampers with the harness or test cases to force a pass | 3 | 4 | Medium | SEC-042, 047, 050 | Low |
| TM-SBX-006 | D | Cryptocurrency mining burns compute budget | 4 | 3 | Medium | SEC-041, 046 | Low |
| TM-SBX-007 | T | Poisoned language image or toolchain compromises all runs | 2 | 5 | High | SEC-048, 084, 085 | Low |
| TM-SBX-008 | T | Sandbox output carries script content that executes in the UI | 3 | 3 | Medium | SEC-024, 050 | Low |
| TM-SBX-009 | D | Warm-pool exhaustion by bursts of cheap runs slows everyone | 3 | 3 | Medium | SEC-029, 046 | Low |

### 3.4 Rewards, ledger, and payments (TM-RWD)

| ID | STRIDE | Threat and abuse scenario | L | I | Rating | Controls | Residual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TM-RWD-001 | T | Replay or race condition double-credits points | 4 | 4 | High | SEC-052, 053, 054 | Low |
| TM-RWD-002 | T | Client-supplied amounts, scores, or balances are trusted | 3 | 4 | Medium | SEC-021, 053 | Low |
| TM-RWD-003 | T | Ledger rows altered or deleted by an insider or defect | 2 | 5 | High | SEC-051, 058, 074 | Low |
| TM-RWD-004 | R | Disputed payout with no evidence trail | 3 | 3 | Medium | SEC-052, 074 | Low |
| TM-RWD-005 | E | Redemption fraud using new accounts, bots, or stolen sessions | 4 | 4 | High | SEC-004, 056, 059, 060, 072 | Medium |
| TM-RWD-006 | S | Forged or replayed webhooks grant entitlements or mark payments paid | 3 | 4 | Medium | SEC-055 | Low |
| TM-RWD-007 | T | Prize pool manipulation through self-contribution, wash activity, or cap gaming | 3 | 3 | Medium | SEC-052, 054, 071 | Medium |
| TM-RWD-008 | D | Settlement workflow stalls or partially pays out | 3 | 4 | Medium | SEC-054, 058 | Low |
| TM-RWD-009 | E | Real-money flag enabled without KYC and limits in place | 2 | 5 | High | SEC-056, 103 | Low |

### 3.5 Competition integrity (TM-CMP)

| ID | STRIDE | Threat and abuse scenario | L | I | Rating | Controls | Residual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TM-CMP-001 | T | Plagiarism and shared solutions in challenges | 5 | 3 | High | SEC-047, 071 | Medium |
| TM-CMP-002 | T | Collusion between battle participants | 3 | 3 | Medium | SEC-069, 071 | Medium |
| TM-CMP-003 | T | Client clock or score tampering in battles | 3 | 4 | Medium | SEC-069 | Low |
| TM-CMP-004 | I | Anonymous entrants deanonymized through payloads, timing, or rank diffs | 3 | 4 | Medium | SEC-015, 017 | Low |
| TM-CMP-005 | D | Battle flooding or spectator spam degrades the hub | 3 | 3 | Medium | SEC-029, 068, 070 | Low |
| TM-CMP-006 | T | Multi-account manipulation of leaderboards | 4 | 3 | Medium | SEC-071, 072 | Medium |
| TM-CMP-007 | I | Hidden test cases inferred from detailed verdict feedback | 3 | 3 | Medium | SEC-047 (feedback limited to pass counts) | Medium |

### 3.6 Learning and progression (TM-LRN)

| ID | STRIDE | Threat and abuse scenario | L | I | Rating | Controls | Residual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TM-LRN-001 | T | Forged lesson-completion events farm XP and points | 4 | 3 | Medium | SEC-021, 029 | Low |
| TM-LRN-002 | T | Race condition promotes a tier twice or skips thresholds | 2 | 2 | Low | SEC-021, 052 | Low |
| TM-LRN-003 | T | Streak farming through clock or time zone manipulation | 4 | 2 | Medium | SEC-021 (server-side user-day rules) | Low |

### 3.7 AI gateway (TM-AI)

| ID | STRIDE | Threat and abuse scenario | L | I | Rating | Controls | Residual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TM-AI-001 | T | Prompt injection through lesson text, user code, or retrieved content redirects the tutor | 4 | 3 | Medium | SEC-063, 064, 066 | Low |
| TM-AI-002 | I | System prompt or other users' context exfiltrated | 3 | 3 | Medium | SEC-063, 065, 066 | Low |
| TM-AI-003 | E | Challenge-mode hints-only rule bypassed to obtain full solutions | 4 | 3 | Medium | SEC-067 | Medium |
| TM-AI-004 | D | Quota evasion or automated use drives provider cost | 4 | 3 | Medium | SEC-029, 062 | Low |
| TM-AI-005 | I | Secrets or PII sent to the provider or stored in logs | 3 | 4 | Medium | SEC-065, 073 | Low |
| TM-AI-006 | T | Model output executed automatically or rendered unsafely | 2 | 4 | Medium | SEC-024, 064 | Low |
| TM-AI-007 | R | Harmful or abusive content generated and attributed to the platform | 3 | 3 | Medium | SEC-064 and FR-AI-006 reporting | Medium |

### 3.8 Privacy, community, and careers (TM-PRV)

| ID | STRIDE | Threat and abuse scenario | L | I | Rating | Controls | Residual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TM-PRV-001 | I | Discreet questions appear in feeds, search, or counts | 3 | 4 | Medium | SEC-017, 018 | Low |
| TM-PRV-002 | I | Recruiters or scrapers harvest profiles without consent | 4 | 3 | Medium | SEC-019, 029, 072 | Low |
| TM-PRV-003 | I | Export feature used to obtain another person's data | 2 | 4 | Medium | SEC-004, 010 | Low |
| TM-PRV-004 | I | Deleted accounts persist in search indexes, logs, or backups | 3 | 3 | Medium | SEC-075, 078 | Low |
| TM-PRV-005 | T | Stored XSS through questions, answers, bios, or challenge text | 4 | 3 | Medium | SEC-022, 024, 027 | Low |
| TM-PRV-006 | I | Search index leaks private entries or hidden profiles | 3 | 3 | Medium | SEC-017 | Low |

### 3.9 API and edge (TM-API)

| ID | STRIDE | Threat and abuse scenario | L | I | Rating | Controls | Residual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TM-API-001 | D | Rate-limit evasion or volumetric attack | 4 | 3 | Medium | SEC-007, 029 | Low |
| TM-API-002 | T | SQL or command injection | 2 | 5 | High | SEC-022, 023 | Low |
| TM-API-003 | I | SSRF through any feature that fetches URLs | 2 | 5 | High | SEC-026 | Low |
| TM-API-004 | T | CSRF on cookie-based flows | 2 | 3 | Low | SEC-028 | Low |
| TM-API-005 | T | Mass assignment through unexpected request fields | 3 | 3 | Medium | SEC-022 | Low |
| TM-API-006 | I | Verbose errors reveal internals | 3 | 2 | Low | RFC 9457 sanitized errors, SEC-022 | Low |
| TM-API-007 | D | Malicious or oversized uploads | 3 | 3 | Medium | SEC-025 | Low |

### 3.10 Clients (TM-CLI)

| ID | STRIDE | Threat and abuse scenario | L | I | Rating | Controls | Residual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TM-CLI-001 | I | Tokens stolen from desktop or mobile storage | 3 | 4 | Medium | SEC-005, 092, 094 | Low |
| TM-CLI-002 | E | Webview or IPC abuse in the desktop shell runs OS commands | 2 | 5 | High | SEC-092 | Low |
| TM-CLI-003 | T | Malicious update delivered to desktop or mobile users | 2 | 5 | High | SEC-093 | Low |
| TM-CLI-004 | S | Deep link triggers a privileged action | 3 | 3 | Medium | SEC-095 | Low |
| TM-CLI-005 | T | Tampered app or emulator farms rewards | 4 | 3 | Medium | SEC-060, 094, 096 | Medium |
| TM-CLI-006 | I | Secrets embedded in client bundles | 3 | 4 | Medium | SEC-031, 094 | Low |

### 3.11 Infrastructure and supply chain (TM-INF)

| ID | STRIDE | Threat and abuse scenario | L | I | Rating | Controls | Residual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TM-INF-001 | T | Compromised dependency or base image enters production | 3 | 5 | High | SEC-082, 084, 085 | Low |
| TM-INF-002 | I | Secrets leaked in repositories or CI logs | 3 | 4 | Medium | SEC-031, 083 | Low |
| TM-INF-003 | E | Over-privileged cloud IAM or CI tokens abused | 3 | 5 | High | SEC-102 | Low |
| TM-INF-004 | D | Region or database loss with data loss | 2 | 5 | High | SEC-038, 101 | Low |
| TM-INF-005 | T | Malicious change merged without review | 2 | 5 | High | SEC-087 | Low |
| TM-INF-006 | I | Backups exposed or restored into insecure environments | 2 | 4 | Medium | SEC-036, 038, 080 | Low |

## 4. Risk Summary

| Rating before controls | Count | Notes |
| --- | --- | --- |
| High | 23 | All have mapped controls, test cases, and pen test objectives |
| Medium | 46 | Tracked through SEC verification and quarterly review |
| Low | 3 | Accepted with monitoring |
| Total | 72 | Across 11 threat areas |

Top risks to design and test first: TM-RWD-001 and TM-RWD-005 (reward integrity), TM-SBX-001 and TM-SBX-003 (sandbox containment), TM-TEN-001, 002, and 003 (isolation and identity), TM-CMP-001 (plagiarism), TM-INF-001 (supply chain).

## 5. Residual Risk Register

| ID | Residual risk | Owner | Decision | Review date |
| --- | --- | --- | --- | --- |
| TM-SBX-001 | Hypervisor or kernel zero-day | Execution lead | Accept with layered isolation, patch SLA, hardened tier for competitions | Quarterly |
| TM-RWD-005 | Determined fraud rings | Rewards lead | Accept with velocity limits, holds, and manual review | Monthly |
| TM-RWD-007 | Pool manipulation by coordinated accounts | Competition lead | Accept with caps and moderation | Monthly |
| TM-CMP-001, 002, 006 | Sophisticated plagiarism, collusion, and multi-accounting | Competition lead | Accept; detection assists human review | Monthly |
| TM-CMP-007 | Partial test-case inference from pass counts | Competition lead | Accept; rotate hidden tests periodically | Per challenge |
| TM-AI-003 | Model sometimes leaks too much in challenge mode | AI lead | Accept with evals and rate limits | On model change |
| TM-AI-007 | Harmful generated content | AI lead | Accept with reporting and moderation | Quarterly |
| TM-CLI-005 | Tampered clients farming rewards | Client lead | Accept with attestation and server-side validation | Quarterly |

Each acceptance needs sign-off from the Security lead and Product owner, and expires after 90 days unless renewed (SEC-001 section 7).

## 6. Review Cadence and Open Items

- Review at every phase gate, after each major incident, and before enabling the real-money track.
- Open items: confirm the age and minor-user policy with Legal, decide on managed versus self-hosted workflow and event platforms (affects TB3 and TB8), and re-score threats after POC-1 and POC-2 results.
