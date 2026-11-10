# CodeFull Points Economy and Rewards Specification

**Doc ID:** ECO-001 | **Version:** 0.1 proposal | **Status:** decisions required from the Product owner | **Owner:** Product owner + Rewards lead **Resolves or informs:** GAP-013 (ranking metric), GAP-015 (points sink), GAP-016 (XP interpretation), GAP-017 (quota for exercises), GAP-018 (economy values), GAP-023 (plan limits) **Upstream:** PRD-001 sec 8 and 9, SRS-001 sec 3.5 and 8, SEC-001 sec 4.6, TM-001 (TM-RWD, TM-LRN) | **Downstream:** SRS v0.2, OpenAPI, DM-001, Playbook steps PB-37 to PB-42

All numbers below are proposals to be tuned with beta data. They live in configuration, never in code constants (cursorrules.md).

## 1. Decisions at a Glance

| # | Decision | Proposal | Rationale |
| --- | --- | --- | --- |
| 1 | What does the leaderboard rank? | **Competition Score (CS)**: lifetime points earned from challenges, battles, and tournaments; weekly boards use a 7-day window | Separate from spendable balance so spending never lowers rank; separate from XP so learning does not buy rank; easy to explain |
| 2 | Are XP, points, and CS the same thing? | No: four distinct values (section 2) | The prototype showed 12,480 as score, XP, and points in different places, which confuses users and breaks rules |
| 3 | XP thresholds | Per tier (XP earned inside the tier); total XP is the sum across tiers | Matches the prototype progress bars (for example 2,480 of 4,000 toward Advanced) |
| 4 | What can points buy at MVP? | A small in-app catalog: profile frames and badges, premium practice packs, streak freezes (section 8) | Gives points meaning without opening redemption workflows and cash exposure |
| 5 | Prize funding | Prizes are funded, not minted: they debit a funded account (creator, contributors, or the platform budget) | Keeps the ledger conserved and caps liability |
| 6 | Redeemable versus in-app points | Two balance buckets: learning points (in-app only) and prize points (eligible for redemption when Phase 2 opens) | Limits cash liability to points won in competition; cheap to create now, costly to retrofit |
| 7 | Do lesson exercises use the execution quota? | No: exercises run on a separate allowance that does not count toward the Free plan 100 executions | Learners should not be blocked mid-lesson; abuse is bounded by lesson rate limits |
| 8 | Points expiry | None at MVP; revisit with Legal before redemption opens | Expiry rules carry legal and trust implications |

## 2. The Four Values

| Value | Meaning | Earned by | Spendable | Affects rank | Stored |
| --- | --- | --- | --- | --- | --- |
| XP | Learning progress inside tiers | Lessons, exercises, modules, courses | No | No (drives tier only) | learning schema events and tier progress |
| Points | Currency | Lessons, answers, streaks, achievements, challenge and tournament prizes | Yes | No | Ledger (double-entry) |
| Competition Score (CS) | Competitive standing | Points earned from challenges, battles, tournaments (completion awards and prizes) | No | Yes (leaderboards) | Derived from ledger entries tagged competition; cached projection |
| Reputation | Community standing | Accepted answers and votes | No | No (affects mentor eligibility) | community schema |

UI rule: show these as four separate labeled numbers wherever they appear; never reuse the word points for XP or CS.

## 3. XP and Tiers

| Tier | XP required to complete the tier (per tier) | Cumulative total |
| --- | --- | --- |
| Beginner | 1,200 | 1,200 |
| Intermediate | 4,000 | 5,200 |
| Advanced | 8,000 | 13,200 |
| Expert | 15,000 | 28,200 |
| Master | 25,000 | 53,200 |
| Guru | 50,000 | 103,200 |

XP awards (proposed): lesson 10 to 40 XP by length (up to 5 min 10; 6 to 15 min 20; 16 to 30 min 30; over 30 min 40); interactive exercise passed 10 XP (first pass only); module completion 100 XP; course completion 250 XP; challenge completion 25 to 200 XP by tier. Promotion fires once when tier XP reaches the threshold; surplus XP carries into the next tier.

## 4. Points: Sources, Rates, and Caps

| Source | Proposed award | Streak multiplier | Daily cap | Notes |
| --- | --- | --- | --- | --- |
| Lesson completed | 10 / 20 / 35 / 50 points by length band | Yes | 500 points | First completion only; verified server-side (SEC-021) |
| Module completed | 100 points | Yes | none | Once |
| Course completed | 250 points | No | none | Once |
| Accepted answer | 10 base, plus 5 per 3 net upvotes up to +10 | Yes | 100 points | Not for self-answers or answers among linked accounts |
| Daily challenge | 25 points | Yes | 25 points | One per day |
| Weekly goal met | 50 points | No | once per week | FR-LRN-008 |
| Achievement unlocked | Common 20, Uncommon 50, Rare 100, Epic 250 | No | none | Once per achievement |
| Challenge completion | By tier: Beginner 50, Intermediate 120, Advanced 300, Expert 600 | No | none | Once per challenge; scaled by share of test cases passed; counts toward CS |
| Challenge placement prize | From the prize fund (section 6) | No | none | Counts toward CS; credited to prize points bucket |
| Battle and tournament prizes | From the prize fund | No | none | Fast-follow; counts toward CS |

**Streak multiplier:** multiplier = min(2.0, 1.0 + 0.05 x streak days), reaching 2x at 20 days. It applies only to the rows marked Yes and never to prizes. A missed day resets the streak unless a streak freeze is used.

**Placement prizes (proposed split):** with 10 or more entrants, 50% to first, 30% to second, 20% to third; with fewer, winner takes all; ties share the combined amounts equally. Rounding remainders go to the highest placement.

## 5. Competition Score and Leaderboards

- **CS** = lifetime sum of points earned from challenge completion, placement prizes, battles, and tournaments (excluding lessons, answers, streaks, and achievements). It never decreases when points are spent or redeemed.
- **Global board:** lifetime CS. **Weekly board:** CS earned in the last 7 days. **Language, region, friends, and org boards:** CS filtered by scope.
- **Display:** leaderboard rows show rank, display name (or Anonymous for private entrants), tier, CS, wins, and losses; rank change uses the daily snapshot against the prior week.
- **Anonymity** never changes CS or rank; it only hides identity (FR-CMP-005, SEC-017).
- **Ties:** equal CS is broken by earlier first-reaching of that score, then fewer attempts.
- **Alternatives considered:** Elo-style rating (fair for head-to-head, harder to explain and needs match volume); XP (rewards learning volume, not competition); lifetime points (mixes learning and competition, and lets spending distort rank). CS keeps the competitive board about competition and can later be supplemented by a rating for battles.

## 6. Funding and Conservation

Points are never created without a funding source. The ledger uses system accounts so every posting balances (FR-RWD-001, SEC-052).

| Account | Purpose |
| --- | --- |
| ISSUANCE | Platform engagement budget; source of lesson, answer, streak, achievement, and daily rewards; monthly budget with alerts |
| PRIZE\_FUND (per challenge) | Holds the prize points for one challenge; funded by the creator, contributors, or an ISSUANCE transfer approved by Product |
| POOL (per pool, fast-follow) | Community-funded prize pool with a cap |
| USER\_LEARNING and USER\_PRIZE (per user) | The two balance buckets |
| SINK | Receives points spent in the catalog |
| ADJUSTMENT | Compensating entries approved with dual control |
| FEES (Phase 2) | Platform fee on pool contributions, subject to legal review |

Example postings: lesson reward = debit ISSUANCE, credit USER\_LEARNING; challenge prize = debit PRIZE\_FUND, credit USER\_PRIZE; catalog purchase = debit USER\_LEARNING (or USER\_PRIZE if the learning bucket is short and policy allows), credit SINK. Spending order: learning points first, then prize points.

## 7. Planned Value and Liability

- Planning value: 100 points = $1 notional. This is a planning figure, not a promise, and no cash redemption exists before Phase 2 (FR-RWD-007).
- Maximum cash liability is bounded by the USER\_PRIZE bucket plus unspent PRIZE\_FUND balances, because learning points cannot be cashed out.
- When Phase 2 opens: per-user monthly redemption caps, minimum thresholds (for example PayPal 1,000 points and gift card 2,500), KYC, holds on new accounts, and manual review above limits (SEC-056, SEC-059).

## 8. Spending Catalog

| Item | Proposed price (points) | Release | Notes |
| --- | --- | --- | --- |
| Profile frame or badge cosmetic | 200 to 500 | MVP (proposed) | Cosmetic; no balance advantage |
| Premium practice pack unlock | 300 per pack | MVP (proposed) | Extra practice problems and explanations |
| Streak freeze | 150 (maximum 2 per month) | MVP (proposed) | Protects the streak for one missed day |
| Pro subscription month | 3,000 | Fast follow (FR-RWD-006) | Entitlement granted through the redemption workflow |
| Course voucher | 500 per premium course | Fast follow | Same workflow |
| Merchandise | Varies | Fast follow | Fulfilment partner needed |
| PayPal cash or gift card | 1,000 or 2,500 minimum | Phase 2 only | Behind the real\_money\_track flag |

MVP purchases are simple ledger debits through the same posting library as earning; they need a new requirement (proposed FR-RWD-010) and test cases (section 12).

## 9. Fraud, Abuse, and Integrity Controls

| Threat | Control | References |
| --- | --- | --- |
| Forged lesson or answer events | Server-side verification of timing and state; per-source daily caps | SEC-021, TM-LRN-001, TC-0207 |
| Streak farming by clock tricks | User-day computed on the server; one qualifying activity per day | TM-LRN-003, TC-0206 |
| Replay and race to double-credit | Idempotency keys per source event; single-transaction postings | SEC-052, TM-RWD-001, TC-0506 |
| Self-dealing in answers or pools | No points for self-answers or linked accounts; related-account contribution limits | TM-RWD-007, TC-0513 |
| New-account farming | Earning velocity limits and holds for the first days; device and behavior signals | SEC-059, SEC-072, TM-RWD-005, TC-0507 |
| Multi-accounting for rank | Device and pattern checks feed moderator review | TM-CMP-006, TC-0412 |
| Plagiarized solutions claiming prizes | Prize payout held until similarity review clears flagged entries | FR-CMP-013, TM-CMP-001 |

All rules, caps, and prices are versioned configuration with effective dates; changes are audited and need Product approval (FR-PLT-006).

## 10. Economy Health Metrics

| Metric | Why | Alert threshold (proposed) |
| --- | --- | --- |
| Points issued per active user per week | Inflation control | Above 120% of plan |
| Issuance to sink ratio | Balance of faucet and drain | Sustained above 3:1 |
| ISSUANCE monthly budget used | Cost control | 80% and 100% |
| Points velocity and balance distribution (Gini) | Hoarding or concentration | Review monthly |
| CS concentration in top 1% | Competitive health | Review monthly |
| Fraud rate of awards | BG-07 | Above 0.1% |
| Unspent prize fund balance | Liability | Review monthly |
| Redemption liability (Phase 2) | Financial exposure | Per Finance policy |

## 11. Configuration Model

A versioned configuration document holds: earning rates and caps per source; multiplier curve; XP awards and tier thresholds; CS inclusion list; prize split rules; catalog items and prices; redemption options and limits (Phase 2); fraud thresholds; effective dates. Services read the active version; each posting records the config version used so past awards can be explained (SEC-074).

## 12. Changes Required in Other Documents

| Document | Change |
| --- | --- |
| SRS-001 | FR-CMP-006: rank by CS (weekly window for the weekly board); FR-LRN-005: per-tier XP; section 8: replace planning ranges with this specification; new FR-RWD-010 for catalog purchases (MVP); FR-EXE-006: exercises exempt from the Free execution quota |
| OpenAPI | DashboardSummary and Leaderboard fields: separate xp, points balances (learning and prize), and competition\_score; catalog endpoints (list and purchase) with Idempotency-Key |
| DM-001 | Account kinds user\_learning and user\_prize; catalog and unlock tables |
| Test Cases | Add cases: catalog purchase idempotency and balance checks; spending order across buckets; CS unaffected by spending; per-source caps; multiplier curve; prize split and ties; ISSUANCE budget alert |
| UI copy | Four labeled values; clear Anonymous explanation; no cash promises |
| GAP-001 | Close GAP-013, 015, 016, 017 on approval; keep GAP-018 open until tuned with beta data |

## 13. Open Questions

1. Approve the CS definition and the four-value model (decisions 1 and 2).
2. Approve MVP sinks or choose to wait for fast-follow redemption (decision 4).
3. Approve the two-bucket ledger design (decision 6) and whether learning points may ever convert to prize points (proposal: never).
4. Set the ISSUANCE monthly budget with Finance.
5. Confirm with Legal how prize points and any future cash redemption are described and whether points may expire.
