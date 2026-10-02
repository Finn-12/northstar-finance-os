# NorthStar Finance OS — Monthly Update Delivery Backlog

| Document field | Value |
|---|---|
| Purpose | Decompose the UAT requirements into buildable developer tickets |
| Status | Proposed; refine before starting implementation |
| Parent requirements | [UAT Business Requirements](./uat-business-requirements.md) |
| Delivery approach | Small vertical slices; each ticket should leave the app runnable |

## What this is called

This work is **backlog refinement** (also called **story decomposition**): clarify a user story, identify dependencies, and split it into testable development tickets. This document is a **delivery backlog**, not a technical design or a commitment that any ticket is complete.

Use the NS IDs in the UAT requirements as the business-story parents. The DEV IDs below are implementation tickets. A ticket is ready to start when its open business decisions are resolved, it has a testable outcome, and any prerequisite tickets are complete.

## Scope and assumptions

- The current repo is a small Streamlit prototype with a static dashboard and a sample CSV. The sample data is not a real project baseline.
- First delivery is a controlled prototype using synthetic or explicitly approved test data. No PFF connection, automatic import, production authentication, or live financial data is assumed.
- Finance must confirm the financial definitions and category mappings before margin-impact calculations are implemented.
- The persistence choice is deliberately left open pending confirmation of how the prototype will be run and what data may be stored. Keep UI and calculation logic separate from the storage implementation so this decision does not leak across the app.
- No real project name, project number, date, or financial amount is included in this backlog.

## Epics and delivery order

| Epic | Outcome | Suggested sequence |
|---|---|---|
| E1 — Trusted project data | Represent a project, reporting month, approved baseline, and update using validated, clearly labelled values | First |
| E2 — Guided monthly update | Prompt the user and capture selected month changes in a draft | After E1 |
| E3 — Variance explanation | Compare comparable values and show a traceable, cautious impact explanation | After E1; client/subconsultant update flows from E2 |
| E4 — Reviewable history | Validate, submit, review, and preserve prior snapshots | After draft and comparison flows |

## Development tickets

### E1 — Trusted project data

| Ticket | Parent story | Build | Acceptance / completion checks | Depends on |
|---|---|---|---|---|
| DEV-001 — Confirm finance calculation contract | NS-109, NS-110, NS-112 | Record Finance-approved definitions for net revenue, project margin, margin %, cashflow, forecast-at-completion, actuals, reporting period, and category sign conventions. Track unresolved items as explicit decisions. | A written mapping identifies inputs, formulas, comparison basis, rounding, and zero-denominator behavior. Margin impact work is blocked until Finance confirms the contract. | None |
| DEV-002 — Define project update data model | NS-101, NS-110 | Define typed structures for project identity, reporting period, baseline snapshot, update status, source metadata, and monthly change items. Include amount, currency, actual/forecast basis, effective/reporting period, and optional note where applicable. | Model distinguishes approved baseline, draft update, actual, and forecast. Required values are validated; unknown values remain unknown rather than defaulting to zero. Unit tests cover valid and invalid records. | DEV-001 |
| DEV-003 — Add synthetic project fixture and repository boundary | NS-101, NS-112, NS-113 | Replace dashboard-only hard-coded metrics with a synthetic, clearly labelled project fixture loaded through a small repository/data-access boundary. Select CSV or another local store only after confirming prototype run mode and data handling. | App displays the fixture as synthetic/test data, not live data. The UI does not depend directly on fixture file details. Missing or malformed fixture data surfaces a useful error. No real project data is added. | DEV-002 |

### E2 — Guided monthly update

| Ticket | Parent story | Build | Acceptance / completion checks | Depends on |
|---|---|---|---|---|
| DEV-004 — Add monthly update session and draft state | NS-102, NS-111 | Let a user select a reporting month and start/resume a draft update for the selected project. Keep draft state separate from the approved baseline. | User can start a draft, see its month and status, and return without altering the approved snapshot. Invalid or missing period is rejected with an understandable message. | DEV-002, DEV-003 |
| DEV-005 — Build guided topic selection | NS-102 | Add the “What changed on this project this month?” prompt and selectable Client / scope, Subconsultants, Salary, Expenses, Contingency, Debts, Cashflow / invoicing, Schedule, and Other topics. | Multiple topics can be selected; the user can continue, skip, and see selected/completed topics. Answers remain attached to the correct draft and reporting month. | DEV-004 |
| DEV-006 — Capture client and scope changes | NS-103 | Add a form for change description, effective month, fee/revenue movement, status, and optional note. Use anonymous/synthetic client labels in the prototype. | User can save a scope addition/removal as a draft item. Amount, period, and status are validated. The entry is clearly identified as an input, not a source-system fact. | DEV-005 |
| DEV-007 — Capture subconsultant costs | NS-104 | Add a form for supplier label, invoice amount, reporting period, actual/forecast status, and optional note/reference. Use synthetic supplier labels. | User can add and edit a supplier cost item in the draft. Missing prior supplier history is allowed and later presented as non-comparable, not as zero. | DEV-005 |
| DEV-008 — Capture remaining monthly topics | NS-105, NS-106, NS-107, NS-108 | Add topic-appropriate draft forms for salary, expenses, contingency, debts, cashflow/invoicing, and schedule. Keep financial categories and schedule fields separate. | Each item retains category, period/as-of date, actual/forecast basis where relevant, and any note. Debt/cashflow do not automatically change margin. Schedule changes do not imply a financial impact without an explicit mapped input. | DEV-005 |

### E3 — Variance explanation

| Ticket | Parent story | Build | Acceptance / completion checks | Depends on |
|---|---|---|---|---|
| DEV-009 — Implement comparable-period variance calculations | NS-104, NS-105, NS-106, NS-109, NS-110 | Add pure, unit-tested calculation functions for signed amount and percentage variance. Compare only compatible categories, periods, currencies, and actual/forecast bases. | Tests cover increase, decrease, unchanged, new item/no prior value, incompatible basis, missing data, currency mismatch, and zero prior amount. Incomparable data is identified rather than coerced. | DEV-001, DEV-002, DEV-007, DEV-008 |
| DEV-010 — Show item-level comparison and explanation | NS-103, NS-104, NS-109 | Display prior value, current value, variance, unit, period, source/status, and a drill-down to the entered item. Show “estimated impact based on entered change” where the calculation is not an approved, fully reconciled model. | Every explanation can be traced to an item and calculation. No causal claim is generated from correlation alone. Missing comparison data is explained. | DEV-006, DEV-007, DEV-009 |
| DEV-011 — Reconcile category bridge to project totals | NS-101, NS-109 | Show how available revenue and cost category movements roll into the total forecast/margin movement under the approved Finance mapping. Keep actual-period movement separate from forecast-at-completion change. | Displayed components reconcile to the displayed total within approved currency rounding. Unsupported or incomplete components are visibly excluded and described. | DEV-001, DEV-009, DEV-010 |

### E4 — Validation and review

| Ticket | Parent story | Build | Acceptance / completion checks | Depends on |
|---|---|---|---|---|
| DEV-012 — Add submission validation | NS-110, NS-112 | Validate required draft fields, period/currency consistency, unresolved conflicts, and completeness before submission. | Validation names the field/problem and blocks submission where required. It does not repair conflicts by guessing or silently substitute zero. | DEV-002, DEV-004, DEV-006, DEV-007, DEV-008 |
| DEV-013 — Add review status and immutable snapshots | NS-101, NS-111 | Add draft, submitted, returned, and approved transitions plus reviewer reason and basic change history. Preserve prior approved snapshots when a new update is approved. | User can submit; reviewer can approve or return; returned changes remain traceable. Approval does not overwrite an earlier approved month. | DEV-003, DEV-004, DEV-012 |
| DEV-014 — Add focused end-to-end UAT tests | NS-101–NS-113 | Exercise the main guided flow and the UAT edge cases using synthetic records. Add focused automated tests for calculation and validation logic. | Tests cover no change, higher subconsultant cost, removed scope, new supplier/no comparable value, actual-versus-forecast mismatch, conflicting source input, zero net revenue, and returned-draft correction. Test output contains no real project data. | DEV-005–DEV-013 |

## Suggested first implementation slice

Start with **DEV-001 through DEV-007, DEV-009, and DEV-010** to prove one end-to-end path:

1. Finance confirms the calculation contract.
2. The app loads one synthetic project and its prior-period baseline.
3. The user starts a draft, chooses Subconsultants, and records a synthetic supplier invoice.
4. NorthStar compares it with prior-period data if available, otherwise explains why it cannot compare.
5. The user sees the values, variance, and a traceable estimated impact without changing the approved baseline.

Then add the client/scope flow and other financial topics, followed by submission/review. Keep each slice runnable and tested; do not build a generic AI explanation before deterministic inputs, comparisons, and calculations are correct.

## Working agreement for a solo developer

For each DEV ticket:

1. Confirm its parent story and prerequisites.
2. Write or identify the test that proves the acceptance checks.
3. Implement the smallest complete vertical change, following existing repo patterns.
4. Run focused tests and inspect the UI with synthetic data.
5. Update the ticket status and note any unresolved decision; do not mark it done just because code was written.

## Decisions to resolve before implementation

| Decision | Needed before | Owner |
|---|---|---|
| Finance definitions and category mappings | DEV-001 completion; all margin-impact work | Finance / product owner |
| Reporting-period convention and comparison rules | DEV-001 and DEV-009 | Finance / product owner |
| Prototype storage and permitted test data | DEV-003 | Product owner / data owner |
| Review/approval roles for prototype | DEV-013 | Product owner |
| Whether any approved source integration is in the first release | Before import/integration work is added | Product owner / data owner |

