# NorthStar Finance OS — Implementation Checklist

Use this file as the quick resume point whenever you return to the project. The detailed scope and acceptance checks live in the [Monthly Update Delivery Backlog](./monthly-update-delivery-backlog.md).

## Resume here

Update this section at the end of each work session.

| Resume field | Current value |
|---|---|
| Current focus | MVP follow-up — confirm finance definitions and prototype data handling |
| Last completed ticket | MVP slice: guided topic selection and subconsultant comparison |
| Next action | Run the MVP locally, review the synthetic-only flow, then resolve finance mapping and storage decisions before extending scope |
| Blockers / decisions needed | Finance approval is needed before margin-impact calculations; durable storage and real project data remain out of scope |
| Last worked on | 2 October 2026 |

## MVP delivery snapshot

The first runnable slice is intentionally narrower than the full ticket acceptance scope: it uses one synthetic demo project, supports a guided topic list with only Subconsultants implemented, compares a manually entered actual invoice with synthetic prior-period data, and keeps the draft in the current browser session only. No margin calculation, approval workflow, or live data integration is included.

| MVP slice | Built | Verified | Notes |
|---|:---:|:---:|---|
| Guided topic picker; remaining topics marked as later work | [x] | [x] | Streamlit AppTest covers deferred-topic messaging |
| Synthetic supplier history and current invoice entry | [x] | [x] | Demo values use synthetic units; draft is session-only |
| Same-supplier prior-month amount variance | [x] | [x] | Missing prior value is not treated as zero |
| Finance-derived margin impact | [ ] | [ ] | Deliberately deferred pending Finance-approved mapping |

## Progress at a glance

Check **Ready** when the ticket's prerequisites and decisions are resolved, **Built** when the change is implemented, and **Verified** only after its acceptance checks and relevant tests pass.

| Ticket | Ready | Built | Verified | Notes |
|---|:---:|:---:|:---:|---|
| DEV-001 — Confirm finance calculation contract | [ ] | [ ] | [ ] | |
| DEV-002 — Define project update data model | [ ] | [ ] | [ ] | |
| DEV-003 — Add synthetic project fixture and repository boundary | [ ] | [x] | [ ] | Synthetic cost fixture only; full project model/repository and storage decision remain |
| DEV-004 — Add monthly update session and draft state | [x] | [x] | [ ] | MVP draft is session-only; no selectable period or approved-snapshot workflow |
| DEV-005 — Build guided topic selection | [x] | [x] | [x] | MVP scope only; remaining topics are deferred |
| DEV-006 — Capture client and scope changes | [ ] | [ ] | [ ] | |
| DEV-007 — Capture subconsultant costs | [x] | [x] | [x] | MVP scope only; synthetic supplier data and session-only draft |
| DEV-008 — Capture remaining monthly topics | [ ] | [ ] | [ ] | |
| DEV-009 — Implement comparable-period variance calculations | [x] | [x] | [ ] | Basic actual cost delta tested; full compatibility and edge-case coverage remains |
| DEV-010 — Show item-level comparison and explanation | [x] | [x] | [ ] | MVP comparison only; no Finance-derived margin explanation or category bridge |
| DEV-011 — Reconcile category bridge to project totals | [ ] | [ ] | [ ] | |
| DEV-012 — Add submission validation | [ ] | [ ] | [ ] | |
| DEV-013 — Add review status and immutable snapshots | [ ] | [ ] | [ ] | |
| DEV-014 — Add focused end-to-end UAT tests | [x] | [x] | [ ] | MVP-only UI and calculation cases pass; remaining UAT scenarios are not yet covered |

## Ticket checklist

### E1 — Trusted project data

- [ ] **DEV-001 — Confirm finance calculation contract** (parent: NS-109, NS-110, NS-112)
  - [ ] Confirm net revenue, project margin, margin %, cashflow, forecast-at-completion, and actual definitions.
  - [ ] Confirm categories/sign conventions, period comparison, rounding, and zero-denominator behavior.
  - [ ] Record the agreed mapping and unresolved items; do not invent financial rules.
- [ ] **DEV-002 — Define project update data model** (parent: NS-101, NS-110; depends on DEV-001)
  - [ ] Model project, reporting period, baseline, draft/update status, source, and change items.
  - [ ] Distinguish unknown from zero, and actual from forecast.
  - [ ] Add validation and focused unit tests.
- [ ] **DEV-003 — Add synthetic project fixture and repository boundary** (parent: NS-101, NS-112, NS-113; depends on DEV-002)
  - [ ] Decide permitted prototype storage/test data before persistence work.
  - [ ] Load synthetic data through a data-access boundary.
  - [ ] Label test data; report missing or malformed data clearly.

### E2 — Guided monthly update

- [ ] **DEV-004 — Add monthly update session and draft state** (parent: NS-102, NS-111; depends on DEV-002, DEV-003)
  - [ ] Select reporting month and start/resume a draft.
  - [ ] Keep draft separate from approved baseline.
  - [ ] Validate period and show draft status.
- [ ] **DEV-005 — Build guided topic selection** (parent: NS-102; depends on DEV-004)
  - [ ] Ask “What changed on this project this month?”
  - [ ] Offer Client / scope, Subconsultants, Salary, Expenses, Contingency, Debts, Cashflow / invoicing, Schedule, and Other.
  - [ ] Support multiple selections, skip, and topic completion state.
- [ ] **DEV-006 — Capture client and scope changes** (parent: NS-103; depends on DEV-005)
  - [ ] Capture scope description, effective month, fee/revenue movement, status, and optional note.
  - [ ] Use anonymous/synthetic client labels.
  - [ ] Validate and save as a draft item.
- [ ] **DEV-007 — Capture subconsultant costs** (parent: NS-104; depends on DEV-005)
  - [ ] Capture synthetic supplier label, amount, period, actual/forecast basis, and optional note.
  - [ ] Support add/edit in draft.
  - [ ] Represent absent prior history as missing/non-comparable, not zero.
- [ ] **DEV-008 — Capture remaining monthly topics** (parent: NS-105–NS-108; depends on DEV-005)
  - [ ] Capture salary, expenses, contingency, debts, cashflow/invoicing, and schedule as distinct topics.
  - [ ] Keep actual/forecast basis and as-of/reporting periods where relevant.
  - [ ] Do not infer margin effects from debt, cashflow, or schedule alone.

### E3 — Variance explanation

- [ ] **DEV-009 — Implement comparable-period variance calculations** (parent: NS-104–NS-106, NS-109, NS-110; depends on DEV-001, DEV-002, DEV-007, DEV-008)
  - [ ] Implement pure calculations for signed and percentage variance.
  - [ ] Compare only compatible category, period, currency, and actual/forecast basis.
  - [ ] Test increase, decrease, unchanged, new item, missing data, mismatched basis/currency, and zero prior value.
- [ ] **DEV-010 — Show item-level comparison and explanation** (parent: NS-103, NS-104, NS-109; depends on DEV-006, DEV-007, DEV-009)
  - [ ] Show prior/current value, variance, unit, period, source/status, and item details.
  - [ ] Make explanations traceable to an input and calculation.
  - [ ] Label estimates cautiously; explain unavailable comparisons.
- [ ] **DEV-011 — Reconcile category bridge to project totals** (parent: NS-101, NS-109; depends on DEV-001, DEV-009, DEV-010)
  - [ ] Roll supported category movements into totals using the approved mapping.
  - [ ] Keep actual movement separate from forecast-at-completion movement.
  - [ ] Test reconciliation within approved currency rounding; disclose exclusions.

### E4 — Validation and review

- [ ] **DEV-012 — Add submission validation** (parent: NS-110, NS-112; depends on DEV-002, DEV-004, DEV-006–DEV-008)
  - [ ] Validate required fields, periods, currencies, conflicts, and completeness.
  - [ ] Identify the exact issue and block submission when required.
  - [ ] Never guess a mapping or silently substitute zero.
- [ ] **DEV-013 — Add review status and immutable snapshots** (parent: NS-101, NS-111; depends on DEV-003, DEV-004, DEV-012)
  - [ ] Implement draft, submitted, returned, and approved states.
  - [ ] Retain reviewer reason and basic change history.
  - [ ] Preserve earlier approved snapshots when a new one is approved.
- [ ] **DEV-014 — Add focused end-to-end UAT tests** (parent: NS-101–NS-113; depends on DEV-005–DEV-013)
  - [ ] Test no change, increased supplier cost, removed scope, and new supplier/no comparison.
  - [ ] Test actual-versus-forecast mismatch, conflicting source input, and zero net revenue.
  - [ ] Test returned-draft correction and ensure test output has no real project data.

## Work session log

Add one short entry when you stop working. Record ticket IDs and file paths, but do not copy real project names, identifiers, or financial values into this log.

| Date | Tickets touched | Outcome / verification | Next action |
|---|---|---|---|
| 2026-10-02 | MVP slice; DEV-003–005, DEV-007, partial DEV-009/010/014 | Added guided Streamlit topic selection, synthetic subconsultant history, session-only invoice draft, actual cost comparison, and focused tests. Six calculation tests and three UI tests pass; browser launch smoke check succeeded. | Review the MVP; resolve finance mapping and permitted storage before adding margin or persistence |

## End-of-session reminder

- [ ] Update the **Resume here** table.
- [ ] Update the three progress checkboxes for every ticket touched.
- [ ] Add a short work-session log row.
- [ ] Leave incomplete tickets unchecked; mark **Verified** only after acceptance checks pass.
- [ ] Keep test data synthetic or explicitly approved.
