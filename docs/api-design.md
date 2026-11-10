# API design

**Status:** overview of the supplied OpenAPI 3.1 draft (`openapi.yaml`) and the backend plan. The contract is a proposal and has not been deployed or verified against a running service.

## Contract conventions

The supplied draft declares `/v1` servers, OIDC bearer authentication by default, operation IDs, requirement tags, and RFC 9457-style problem details. Realtime channels are described separately in the supplied AsyncAPI draft. A release must publish accurate server addresses; the `codefull.dev` URLs in the draft are examples, not confirmation of live environments.

Recommended contract rules:

- Validate all request bodies against explicit schemas and enforce bounded request sizes.
- Scope private operations to authenticated user/workspace context and document authorization per operation.
- Use idempotency keys for submissions and reward-affecting actions; reject stale state with explicit conflict responses.
- Use opaque cursors for large collections and avoid returning hidden judging material.
- Version asynchronous events and keep them minimal; resolve the authorized resource through the API.
- Document limits, stable error codes, retry behavior, privacy effects, and deprecation policy.

## Proposed REST resources

| Domain | Example operations | Privacy / integrity notes |
|---|---|---|
| Identity | `GET/PATCH /me`, `DELETE /me`, session and privacy settings | Export/deletion and visibility changes need auditable workflows |
| Learning | `GET /courses`, `GET /courses/{id}`, enrollment, lesson progress | Award progress from verified server-side events |
| Execution | `POST /runs`, read run status/output, create/list snippets | Submit only to the execution service; apply limits and plan allowances |
| Challenges | list/detail challenges, create entry, submit solution | Private entry identity must be omitted from public responses |
| Rewards | balance, transactions, catalog, purchase | Client never chooses a balance or award; idempotent ledger post |
| Community | questions, answers, votes, accepted answer, moderation flag | “Discreet” questions need strict owner/assigned-helper visibility |
| Billing | plan, checkout, usage, invoices | Payment card handling stays with hosted provider UI |
| Platform | notifications, search, analytics, admin configuration | Admin operations need least privilege and audit |

The source `openapi.yaml` contains the proposed operation-level contract and requirement references. The full original is preserved under `src/backend plan/source-materials/`.

## Code execution request (conceptual)

A future run operation should accept a language identifier, bounded source payload, and optional challenge/run context, and return a run identifier with queued/running/completed state. Output includes bounded stdout/stderr and resource summary where appropriate. Challenge verdict responses should disclose only approved feedback and must not return hidden tests or implementation details.

The interface shown here is a high-level contract description, not a production runner API. The supplied HTML has simulated output, and this package does not provide an execution service. Do not send sensitive or confidential code to an unverified endpoint.

## Realtime interfaces

The supplied AsyncAPI file describes proposed realtime event channels for battle state, notifications, and run streams. A future implementation should authenticate at connection and reconnection, authorize each topic, use sequence IDs for resume, enforce message-size/rate bounds, and treat client messages as requests—not authoritative scores or clocks.

## Contract validation and release gates

The OpenAPI and AsyncAPI documents should be linted, checked for breaking changes, and compared to generated SDKs. Contract tests must cover authorization, tenant scope, anonymous/private response shape, idempotent retries, error schemas, rate limits, and event resumption. None of those implementation tests is present in this documentation package; CI validates package structure and builds the docs only.
