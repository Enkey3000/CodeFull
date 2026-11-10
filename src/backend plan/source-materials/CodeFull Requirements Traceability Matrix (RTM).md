# CodeFull Requirements Traceability Matrix (RTM)

**Doc ID:** RTM-001 | **Version:** 0.1 baseline | **Status:** for QA and product review | **Owner:** QA lead + Product owner **Sources:** PRD-001, SRS-001, SEC-001, TM-001, TC-001, UAT-001, openapi.yaml | **Matrix file:** CodeFull\_RTM.xlsx

## 1. Purpose

The RTM proves that every requirement is designed, built, tested, and accepted, and that nothing is tested or built without a requirement. It is the evidence behind the release gate: 100% of Must requirements traced, no orphan tests, no unmitigated High threat without a test.

The full matrix lives in the workbook CodeFull\_RTM.xlsx (filterable, with live coverage formulas). This document explains how it is built, what it shows today, and what to fix.

## 2. Trace Chain

```
BG (goal) -> FR / NFR / SEC (requirement) -> API operation (OpenAPI x-requirement)
                                         -> TM (threat) -> TC (test case) -> UAT (acceptance) -> Release
```

Example chains from the baseline:

| Chain | Items |
| --- | --- |
| Privacy on the leaderboard | BG-07 -> FR-CMP-005 -> API-enterChallenge, API-setLeaderboardVisibility -> SEC-017 -> TM-CMP-004 -> TC-0404 -> UAT-011 |
| Safe code execution | BG-07 -> FR-EXE-003 -> API-createRun -> SEC-040, SEC-041 -> TM-SBX-002, TM-SBX-003 -> TC-0303, TC-0304, TC-1201 -> UAT-007 |
| No double payouts | BG-03, BG-07 -> FR-CMP-003, FR-RWD-005 -> API-submitSolution -> SEC-052, SEC-053 -> TM-RWD-001 -> TC-0403, TC-0505, TC-0506 -> UAT-010 |

## 3. Workbook Structure

| Sheet | Content |
| --- | --- |
| Summary | Live counts and coverage ratios computed by formulas from the other sheets; maintenance notes |
| FR Matrix | 88 functional requirements with priority, release, goal, API operations, threats, security controls, test cases, UAT, test status, UAT status |
| NFR Matrix | 26 non-functional requirements with test cases and status |
| SEC Coverage | 104 security controls with verification type, test cases, and status |
| Threat Coverage | 72 threats with rating, test cases, and status |
| UAT Scenarios | 35 scenarios with persona, release, and requirement links |
| Test Cases | 126 cases with suite, priority, and traces |

Status values: **Covered** (at least one test case), **GAP** (Must item without a test), **Planned** (lower priority item without a test yet), **Process evidence** (control verified by review, pen test, pipeline gate, or drill).

## 4. Baseline Results

| Measure | Result |
| --- | --- |
| Functional requirements | 88 (53 Must) |
| Must requirements with a test case | 53 of 53 (100%) |
| Must (MVP and FF) requirements with no UAT scenario | 8 |
| Should and Could requirements without a test case yet | 25 |
| Non-functional requirements without a test case | 5 of 26 |
| Security controls covered by a test case | 66 of 104 |
| Security controls verified by process evidence | 17 |
| Security controls with no verification yet | 21 |
| High threats with a test case | 23 of 23 |
| Medium and Low threats without a direct test tag | 15 of 49 |
| Test cases / UAT scenarios | 126 / 35 |

Coverage means a case exists and is linked. It does not mean the case has run or passed; pass and fail results are added once CI publishes them (section 6).

### Coverage by domain

| Domain | FRs | Must | Must covered | Should and Could without a test |
| --- | --- | --- | --- | --- |
| Identity (IDN) | 10 | 7 | 7 | 2 |
| Learning (LRN) | 12 | 7 | 7 | 5 |
| Execution (EXE) | 8 | 6 | 6 | 1 |
| Competition (CMP) | 14 | 8 | 8 | 6 |
| Rewards (RWD) | 9 | 6 | 6 | 1 |
| Community (COM) | 8 | 4 | 4 | 1 |
| Careers (CAR) | 5 | 2 | 2 | 2 |
| AI | 6 | 3 | 3 | 2 |
| Billing (BIL) | 7 | 5 | 5 | 1 |
| Platform (PLT) | 9 | 5 | 5 | 4 |

## 5. Gaps and Recommended Actions

These are the findings from the baseline. Close them in Test Cases v0.2 and UAT v0.2.

### 5.1 Must requirements with no UAT scenario (8)

FR-EXE-006 (plan quotas), FR-EXE-008 (hardened tier), FR-CMP-013 (plagiarism review), FR-RWD-001 (ledger), FR-RWD-005 (settlement), FR-RWD-008 (fraud controls), FR-RWD-009 (reconciliation), FR-BIL-007 (entitlement fail-open).

**Action:** add a user-visible UAT scenario for FR-EXE-006 (running out of executions) and for FR-CMP-013 (moderator reviews a flagged pair). The remaining six are internal controls with no user-facing behavior; record them as UAT not applicable, verified by test cases and operations review, and have the product owner approve that disposition.

### 5.2 Non-functional requirements with no test case (5)

| NFR | Add |
| --- | --- |
| NFR-009 search latency | LOAD case for search at baseline concurrency |
| NFR-018 privacy compliance | Privacy review case covering export, deletion, consent records, and retention evidence |
| NFR-022 observability | Check that every service emits traces, metrics, and logs and that SLO alerts fire in a drill |
| NFR-023 maintainability | CI gate evidence: coverage, lint, type checks, contract checks |
| NFR-026 localization readiness | Lint or test that user-facing strings are externalized |

### 5.3 Security controls with no verification yet (21)

SEC-001, 005, 008, 012, 016, 020, 028, 030, 033, 034, 035, 039, 048, 054, 068, 070, 077, 085, 089, 091, 095.

**Action:** add test cases or pipeline gates, for example: an OIDC with PKCE flow test (SEC-001); client token storage tests (SEC-005, 091); account recovery abuse test (SEC-008); mTLS enforcement test (SEC-012); audited view column checks (SEC-016); admin IP allowlist and step-up test (SEC-020); CSRF test (SEC-028); static rules for unsafe deserialization, weak crypto, and non-secure randomness (SEC-030, 034, 035); TLS configuration scan (SEC-033); network policy test proving only the Execution Gateway reaches sandboxes (SEC-039); escape suite as a required CI check (SEC-048); fail-closed workflow test (SEC-054; related to TC-0505); WebSocket authorization and message limit tests (SEC-068, 070); consent record test (SEC-077); lockfile and pinned image check (SEC-085); scheduled DAST (SEC-089); deep link validation test (SEC-095).

Another 17 controls rely on process evidence (reviews, pen tests, pipeline gates, drills); keep the evidence links in the RTM when they exist.

### 5.4 Medium and Low threats without a direct test tag (15)

TM-AUT-004, TM-AUT-005, TM-SBX-009, TM-RWD-004, TM-RWD-007, TM-CMP-002, TM-CMP-005, TM-PRV-006, TM-API-001, TM-API-004, TM-API-006, TM-CLI-001, TM-CLI-004, TM-CLI-006, TM-INF-006.

**Action:** most are addressed indirectly through the SEC cases that mitigate them. Tag the existing cases with the TM ID where they apply and add cases for the rest (for example account recovery abuse, warm-pool exhaustion, battle flooding, search index leakage, CSRF, and error message sanitization).

### 5.5 Should and Could requirements without a test case (25)

Add cases as features are specified, MVP-tier items first: FR-LRN-007, 008, 009; FR-EXE-007; FR-CMP-014; FR-COM-008; FR-AI-002, 005; FR-PLT-002. Fast-follow and Phase 2 items follow their release plan.

### 5.6 Data quality notes

- The goal (BG) mapping per requirement is a first pass by domain with overrides; the product owner should confirm it.
- Test case 0411 (tie-break rules) and 1405 (loading, empty, and error states) trace to business rules and PRD guidance rather than a numbered requirement; add requirement IDs for them in SRS v0.2.
- The OpenAPI file covers 53 operations; battles, notifications, and run streams need an AsyncAPI file, after which their traces move from the FR level to the operation level.

## 6. Generation and Maintenance

The workbook is generated by a script, not edited by hand. Inputs and conventions:

| Input | Convention |
| --- | --- |
| SRS, SEC, TM, UAT documents | IDs in tables; front matter lists the document ID and version |
| OpenAPI | x-requirement array on every operation (FR, NFR, SEC IDs) |
| Tests | Requirement markers in code (for example a pytest req marker, a Go comment tag, a Playwright annotation) with FR, NFR, SEC, and TM IDs |
| UAT | Results file with scenario ID, outcome, date, and tester |
| CI results | JUnit XML per suite, ingested to add pass, fail, or not run to each case |

The generator runs on every pull request that touches /docs, /contracts, or tests, and weekly for the report.

**Checks that fail the build**

1. Any Must requirement without a linked test case.
2. Any test case, API operation, or UAT scenario that references an ID that does not exist.
3. Any test case with no requirement, security, or threat trace (orphan), except those on an approved exception list.
4. Any High threat without a test case.
5. Any removed or renamed requirement still referenced elsewhere.

**Outputs:** the workbook, a CSV export for tooling, and an HTML dashboard with coverage by domain and trend over time.

## 7. Roles and Cadence

| Role | Responsibility |
| --- | --- |
| QA lead | Owns the generator, reviews weekly coverage, maintains exceptions |
| Product owner | Confirms goal mapping and UAT dispositions |
| Security lead | Owns SEC and threat links, approves process-evidence entries |
| Developers | Add requirement markers with each test and OpenAPI operation |

Cadence: updated every pull request; reviewed weekly; baselined at each release gate and attached to the go/no-go record (REL-001 section 9).

## 8. Release Gate Criteria

- 100% of Must requirements have a linked test case and a passing result in the latest run.
- Every Must (MVP) requirement with user-visible behavior has a passed UAT scenario.
- Zero High threats without a passing test.
- Every SEC item is Covered or has approved process evidence; no GAP.
- No orphan tests or dangling IDs.

## 9. Baseline v0.2 Results (supersedes sections 4 and 5)

Test Cases v0.2 (32 new cases) and UAT v0.2 (2 new scenarios, 4 approved-pending N/A dispositions) close the gaps found in the v0.1 baseline. The workbook CodeFull\_RTM.xlsx has been regenerated; its Summary sheet holds the live figures below.

| Measure | v0.1 | v0.2 |
| --- | --- | --- |
| Test cases | 126 | 158 |
| UAT scenarios | 35 | 37 |
| Must requirements with a test case | 53 of 53 | 53 of 53 |
| Must (MVP and FF) requirements with no UAT scenario | 8 | 0 |
| Must requirements with UAT marked N/A (internal control) | 0 | 4 (awaiting product owner approval) |
| Non-functional requirements without a test case | 5 | 0 |
| Security controls covered by a test case | 66 | 92 |
| Security controls verified by process evidence | 17 | 12 |
| Security controls with no verification | 21 | 0 |
| High threats with a test case | 23 of 23 | 23 of 23 |
| Medium and Low threats without a direct test tag | 15 | 0 |
| Should and Could requirements without a test case | 25 | 24 |

### What remains open

- **24 Should and Could requirements without a test case:** FR-IDN-008, 009; FR-LRN-007, 008, 009, 011, 012; FR-EXE-007; FR-CMP-004, 007, 010, 011, 012, 014; FR-RWD-006; FR-COM-008; FR-CAR-003, 004; FR-AI-002, 005; FR-BIL-006; FR-PLT-003, 007, 008. MVP-tier items (FR-LRN-007, 008, 009, FR-EXE-007, FR-CMP-014, FR-COM-008, FR-AI-002, 005) should get cases before their slices start.
- **Product owner approval** of the four UAT N/A dispositions.
- **Pass and fail results:** coverage means a case exists and is linked, not that it has run; CI results ingestion (section 6) adds pass, fail, and not-run status once tests exist.
- **Goal mapping (BG) per requirement** still needs product owner confirmation.
- **Realtime traces:** an AsyncAPI specification now exists (asyncapi.yaml); traces for battles, notifications, and streams can move from requirement level to operation level when the generator reads it.

## 10. Baseline v0.3 Results (ECO-001 approved; supersedes section 9)

The approved points economy added four requirements (FR-RWD-010 to 013), 11 test cases (TC-0514 to 0524), and two UAT scenarios (UAT-038, 039). OpenAPI moved to 0.2.0 (56 operations). The workbook CodeFull\_RTM.xlsx is regenerated; its Summary sheet holds the live figures.

| Measure | v0.2 | v0.3 |
| --- | --- | --- |
| Functional requirements / Must | 88 / 53 | 92 / 56 |
| Test cases | 158 | 169 |
| UAT scenarios | 37 | 39 |
| Must requirements with a test case | 53 of 53 | 56 of 56 |
| Must (MVP and FF) requirements with no UAT scenario | 0 | 0 |
| Must requirements with UAT marked N/A (awaiting product owner approval) | 4 | 4 |
| Security controls covered by a test case / process evidence / no verification | 92 / 12 / 0 | 92 / 12 / 0 |
| Non-functional requirements without a test case | 0 | 0 |
| High threats with a test case | 23 of 23 | 23 of 23 |
| Should and Could requirements without a test case | 24 | 24 |

What remains open is unchanged from section 9: the 24 Should and Could requirements, the four UAT N/A approvals, pass and fail results once CI publishes them, and confirmation of the goal (BG) mapping. Goal mapping for FR-RWD-010 to 013 follows the rewards domain default (BG-03 and BG-07).
