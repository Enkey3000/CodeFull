# CodeFull Release and Deployment Plan

**Doc ID:** REL-001 | **Version:** 0.1 draft | **Status:** for engineering and operations review | **Owner:** DevOps lead **Upstream:** ARCH-001, SEC-001, TP-001, UAT-001 | **Downstream:** Incident Response Plan, Execution Guide, RTM

## 1. Purpose and Scope

How CodeFull changes reach users safely and reversibly: environments, pipeline, versioning, deployment strategy per component, database migrations, feature flags, go/no-go criteria, rollback, communication, and post-release verification. Covers backend services, realtime hub, Execution Gateway and sandbox images, web app, and (after MVP) desktop and mobile clients.

## 2. Release Types and Cadence

| Type | Content | Cadence | Approval |
| --- | --- | --- | --- |
| Continuous (web and services) | Small changes behind flags | Daily to weekly trains from main | Automated gates plus code owner review |
| Beta release | MVP feature set to the beta cohort | Once, after UAT entry criteria | Go/no-go (section 9) |
| GA release | MVP to the public | After UAT exit and pen test closure | Go/no-go with executive sign-off |
| Fast-follow release | Battles, tournaments, pools, mentors, careers | Per feature, ring-based | Feature owner, QA, Security |
| Sandbox image release | New runtimes or image updates | On demand and monthly patch | Execution lead plus escape suite pass |
| Desktop and mobile releases | Client builds | Monthly, plus hotfixes | Release manager, store policies |
| Hotfix | Fix for Sev 1 or Sev 2 | As needed | Incident commander plus QA lead |

## 3. Environments and Promotion Path

```
Developer -> Pull request (preview env + CI) -> main
                                                  |
                                           Build, test, scan, sign
                                                  |
                                     Staging (full E2E, DAST, LOAD, UAT)
                                                  |
                           Production: canary 5% -> 25% -> 50% -> 100%
                                                  |
                                  Post-release verification and SLO watch
```

| Environment | Purpose | Notes |
| --- | --- | --- |
| Preview | Per-PR web and API review | Ephemeral, seeded data |
| Staging | Production-like validation | Same Helm charts and Terraform modules as production; anonymized data |
| Production | Live users | Multi-AZ; change windows avoid battle peaks and tournament start times |

## 4. Versioning and Artifacts

- **Public API:** major version in the path (v1); additive changes are non-breaking; breaking changes need a new major version with a deprecation period of at least 6 months and notices through response headers and docs.
- **Services and images:** tagged with the Git SHA and a SemVer release label; images are signed (Cosign) and carry an SBOM.
- **Contracts and SDKs:** versioned with the API; SDKs for TypeScript, Kotlin, Swift, C#, and Rust are generated and published per release.
- **Database migrations:** numbered, forward-only in production, tied to the release that needs them.
- **Sandbox images:** immutable digests per language and version, recorded in the Execution Gateway config.
- **Client apps:** web by deploy version; desktop and mobile by SemVer with build numbers.

## 5. CI/CD Pipeline and Gates

| Stage | Checks | Blocks release if |
| --- | --- | --- |
| Build | Compile, package, generate SDKs | Failure |
| Test | UT, CT, IT, DB suites; RLS linter | Any failure; coverage drop on domain code |
| Scan | SAST, dependency, secret, IaC scans | Critical or high finding |
| Contract | OpenAPI lint and breaking-change diff | Unapproved breaking change |
| Package | Image build, SBOM, Cosign signing | Unsigned or non-root violations |
| Deploy to staging | Argo CD sync | Health checks fail |
| Staging validation | E2E smoke and regression, DAST, sandbox suite when images change | P1 failure |
| Promote to production | Argo Rollouts canary with automated analysis | Error rate, latency, or business metric regression |
| Post-deploy | Smoke tests, synthetic checks, SLO dashboards | Alerts firing |

## 6. Deployment Strategy by Component

| Component | Strategy | Special handling |
| --- | --- | --- |
| API gateway (Envoy) | Canary with header-based routing; config validated before apply | Rollback by config revision; rate limit and auth policy tests run first |
| Domain services (FastAPI) | Canary 5, 25, 50, 100 percent with automated analysis | Backward-compatible API and event schemas for one release overlap |
| DAL | Canary, deployed before consumers when adding capabilities | Contract tests with all service versions in flight |
| Realtime hub | Rolling with connection draining; no deploys during live battles unless emergency | Clients reconnect and resume from the last sequence; battle state in Redis survives restarts |
| Execution Gateway | Canary with a separate pool | Rolling restart drains in-flight jobs; queue protects against short capacity dips |
| Sandbox images | Blue/green image pools by digest | Escape suite and determinism suite must pass before traffic shifts; previous digest kept for instant rollback |
| Temporal workflows | Versioned workers and workflow patching | Running settlements and redemptions finish on the version that started them |
| NATS, Redis, schemas | Additive changes first | New event versions published alongside old; consumers upgraded before producers stop the old version |
| Web app | Immutable assets on CDN, atomic switch | Feature flags for incomplete work; cache busting by hash |
| Desktop | Staged updater channels (beta, stable) with signed manifests | Minimum-version endpoint for forced upgrades |
| Mobile | TestFlight and Play internal tracks, then phased rollout (1, 5, 20, 50, 100 percent) | Remote config kill switches; forced-upgrade endpoint for breaking changes |

## 7. Database Migration Procedure

1. **Expand:** add new tables, columns, and indexes (built concurrently); new code can read and write both shapes; RLS policies in the same migration; pgTAP tests pass.
2. **Migrate data:** backfill in batches with throttling and idempotent jobs; verify row counts and checksums.
3. **Switch:** release code that uses the new shape; keep dual-write until stable.
4. **Contract:** after at least one full release cycle and a successful backup, remove the old shape in a later release.
5. **Rules:** no table rewrites or long locks on hot tables during peak hours; dry-run on a staging copy of production-sized data; ledger and audit tables never receive destructive migrations; every migration has a documented rollback or forward-fix plan.

## 8. Feature Flags and Rollout Rings

| Ring | Audience | Purpose |
| --- | --- | --- |
| 0 | Internal staff | Dogfooding |
| 1 | Beta cohort | UAT and early feedback |
| 2 | 5% of new signups | Early production signals |
| 3 | 25% | Scale validation |
| 4 | 100% | General availability |

Flag rules: every incomplete or risky feature ships behind a flag; flags have owners and expiry reviews; flag changes are audited. The `real_money_track` flag stays off in every ring and can only be enabled through dual approval with Legal, Security, and Product sign-off after KYC and limits are in place (SEC-056, SEC-103).

## 9. Go/No-Go Checklist

| Area | Criterion | Owner | Evidence |
| --- | --- | --- | --- |
| Quality | All P1 test cases pass; zero open Sev 1 or Sev 2 | QA lead | TC-001 results, defect log |
| Acceptance | UAT exit criteria met and signed | Product owner | UAT-001 report |
| Security | Pen test criticals and highs closed; SAST, dependency, and image scans clean; secrets rotated | Security lead | Scan reports, pen test retest |
| Performance | LOAD-1 to LOAD-5 met at target; capacity headroom confirmed | SRE | Load reports |
| Reliability | Backup restore and failover drill within 90 days; rollback rehearsed in staging | SRE | Drill records |
| Operations | On-call rota staffed; runbooks, dashboards, and alerts live; IR tabletop done | SRE, Security | Runbook links, drill notes |
| Data | Migrations dry-run passed; reconciliation job healthy | Backend lead | Staging logs |
| Compliance | Privacy notice, terms, consent flows approved; real-money flag confirmed off | Legal | Sign-off |
| Support | Help content, support channel, known-issues page ready | Support lead | Links |
| Business | KPI baselines and dashboards ready; communication plan approved | Product owner | Dashboard, plan |
| Dependencies | Third-party limits and quotas confirmed (Stripe, email, push, AI provider) | Engineering lead | Provider confirmations |

Decision rule: any failed Quality, Security, Reliability, or Compliance item is a no-go. Other failures need a written exception from the accountable owner.

## 10. Rollback and Recovery

| Trigger | Action |
| --- | --- |
| Canary analysis fails (error rate, latency, or key business metric) | Automatic rollback to the previous revision |
| Sev 1 or Sev 2 detected after full rollout | Incident commander decides: flag off, rollback, or forward fix |
| Ledger or reconciliation anomaly | Stop affected workflows, disable redemption and settlement flags, follow INC-2; do not roll back ledger data |
| Bad sandbox image | Shift traffic back to the previous digest |
| Bad client build | Halt rollout, pause store release, push minimum-version or kill-switch config |

Rollback principles: prefer disabling the flag over redeploying; schema changes are expand-contract so the previous version still runs; data-changing releases include a forward-fix plan; ledger and audit data are never rolled back, only corrected by compensating entries.

## 11. Release Runbook (per production release)

| When | Step | Owner |
| --- | --- | --- |
| T-7 days | Scope freeze, release notes draft, risk review | Release manager |
| T-3 days | Staging soak complete, migration dry-run, go/no-go pre-read | QA lead, Backend lead |
| T-1 day | Go/no-go meeting; communications scheduled; on-call confirmed | Release manager |
| T0 | Deploy migrations (expand), start canary, monitor dashboards | Release engineer, SRE |
| T0 + 30 min | Advance canary if analysis passes | SRE |
| T0 + 2 h | Full rollout; run smoke and synthetic checks | QA, SRE |
| T+1 day | Review SLOs, error budgets, support tickets, KPI early read | Release manager |
| T+7 days | Retrospective; schedule contract migrations and flag cleanup | Engineering lead |

Change windows: avoid scheduled tournaments, major battles, and billing cycle peaks; no deploys on Fridays after noon unless it is a hotfix.

## 12. Communication Plan

| Audience | Channel | Timing |
| --- | --- | --- |
| Engineering and support | Release channel, release notes | Before and after each release |
| Users | In-app notices, email, changelog, status page | Scheduled maintenance 48 hours ahead; incidents as they occur |
| Beta cohort | Email and community channel | Each beta build |
| Leadership | Summary after go/no-go and after T+1 | Per release |
| Partners (recruiters, Enterprise pilots) | Direct email | Before changes affecting them |

## 13. Post-Release Verification

- **Technical:** SLO dashboards (availability, latency, error rate), queue depth, sandbox warm-pool hit rate, ledger reconciliation, event lag, push delivery.
- **Product:** signup to first-run funnel (BG-01), challenge entry rate (BG-03), checkout success (BG-04), question answer time (BG-05).
- **Security:** auth anomaly alerts, quota abuse alerts, sandbox policy violations.
- **Thresholds:** automatic canary abort on error rate above 1%, p95 latency above 1.5 times baseline, or any ledger invariant alert.

## 14. Hotfix Process

1. Reproduce with a failing test; branch from the production tag.
2. Minimal fix with targeted tests; code owner and security review for sensitive areas.
3. Fast-track pipeline (full security scans retained); deploy via canary at accelerated steps.
4. Verify, communicate, and merge back to main; post-incident review within 5 business days.

## 15. Desktop and Mobile Release Notes (after MVP)

- **Desktop:** signed and notarized builds; update manifests per channel; staged rollout by percentage; forced update only for security fixes.
- **iOS and Android:** store review lead time planned (allow 3 to 7 days); privacy labels and data safety forms updated; subscription and rewards policies reviewed before each submission that changes them; phased rollout with crash-free rate gates (99.5% or higher).

## 16. Roles

| Role | Responsibility |
| --- | --- |
| Release manager | Calendar, runbook, go/no-go facilitation, communications |
| DevOps lead | Pipelines, environments, deployment tooling |
| QA lead | Quality evidence and recommendation |
| Security lead | Security gate and exceptions |
| SRE | Canary monitoring, rollback execution, drills |
| Product owner | Business readiness and acceptance |
| Incident commander (on-call) | Decision authority during incidents |

## 17. Open Items

- Choose the cloud provider and confirm nested virtualization or bare-metal support for the hardened sandbox pool.
- Define the status page tool and incident communication templates (with the Incident Response Plan).
- Decide whether the beta cohort lives in a separate tenant or a flagged cohort.
- Confirm change window policy with support and operations.
