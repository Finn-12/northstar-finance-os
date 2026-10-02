# NorthStar Finance OS — UAT Business Requirements

| Document field | Value |
|---|---|
| Status | Draft for business review |
| Product | NorthStar Finance OS |
| Business capability | Guided monthly project updates and financial variance explanations |
| Currency in supplied example | [REDACTED] |
| Reference snapshot date | [REDACTED] |
| Primary users | Project Manager, Project Accountant, Finance Reviewer |

## 1. Purpose

Replace the prototype's static project-health display with a project-finance workspace that guides a user through monthly changes, drills into the underlying client and cost items, compares the update with the previous approved month, and explains the resulting forecast and margin movement.

The user should be able to start with a short prompt such as **“What changed on this project this month?”**, choose a topic, answer focused follow-up questions, and review a traceable explanation before saving or submitting the update.

This document defines requirements and UAT tickets; it does not assert that the prototype is already connected to PFF or to live finance systems.

## 2. Business outcomes and success measures

1. A project user can complete a guided monthly update without editing a spreadsheet.
2. Every displayed month-over-month movement can be traced to an entered or imported item and a stated calculation.
3. Revenue, cost, project margin, margin percentage, cashflow, and schedule changes are shown with consistent units and period definitions.
4. A reviewer can distinguish actuals, forecast values, and approved baseline values.
5. Missing or conflicting source values are visible and are never silently treated as zero or as verified.

## 3. Users and permissions

| User | Need | Minimum permissions |
|---|---|---|
| Project Manager | Record scope, client, schedule, and delivery changes; review their forecast impact | View project; draft and edit monthly update |
| Project Accountant | Record invoice, salary, expense, contingency, debt, and cashflow movements | View project; draft and edit financial update |
| Finance Reviewer | Validate explanations and figures before approval | View project and audit trail; review, return, or approve update |

Authentication, project-level access rules, and approval authority must follow the host organization's approved identity and finance controls. UAT must use synthetic or explicitly approved test data.

## 4. Proposed user journey

1. User opens a project and chooses the reporting month.
2. NorthStar shows the current approved figures and the previous-month comparison.
3. NorthStar asks: **“What changed on this project this month?”**
4. User chooses one or more topics: **Client / scope**, **Subconsultants**, **Salary**, **Expenses**, **Contingency**, **Debts**, **Cashflow / invoicing**, **Schedule**, or **Other**.
5. NorthStar asks a topic-specific follow-up and captures the item, amount, period, status, and optional explanation/evidence.
6. NorthStar compares the entered data with the prior month and calculates a transparent, provisional impact on revenue, cost, margin, and cashflow where supported.
7. User reviews the explanation and corrects or confirms it; unsupported or incomplete comparisons are labelled as such.
8. User saves a draft or submits it for finance review. Approval creates a new approved monthly snapshot; prior snapshots remain unchanged.

## 5. Measures and calculation rules

These rules are the initial UAT contract and require confirmation by Finance before production use.

| Measure | Proposed definition | UAT presentation |
|---|---|---|
| Net revenue | Gross revenue less subconsultant costs, if that matches the organization's PFF definition | Amount and currency; show component inputs |
| Project margin | Net revenue less applicable project costs, using the approved chart/category mapping | Amount; show the calculation bridge |
| Project margin % | Project margin divided by net revenue; undefined when net revenue is zero | Percentage; never divide by zero |
| Month-over-month variance | Current reporting-month value less the comparable prior-month value | Signed amount, direction, period, and source |
| Forecast impact | Difference between the new forecast-at-completion and the previous approved forecast-at-completion | Separate from actual-period movement |
| Cashflow | Cash received/paid or the approved PFF cashflow measure, not interchangeable with margin | Label the chosen basis and period |

Positive and negative signs must be consistent throughout the UI. A cost increase should be shown as an increase in cost and, where the approved margin formula applies, a decrease in margin. The product must not describe a correlation as a confirmed cause: explanations should say **“estimated impact based on the entered change”** unless the calculation is directly supported by the underlying values.

## 6. Anonymized reference scenario for UAT design

The source project name, project number, reporting dates, currency, and all project-specific financial values have been masked. This anonymized scenario is for requirements context only; it is not a verified fixture, a source-system import, or permission to use the original project data in testing.

| Field | Masked value |
|---|---|
| Project number | [REDACTED] |
| Project name | [REDACTED] |
| Scope / status | [REDACTED] |
| Start / current end date | [REDACTED] |
| Original end date | [REDACTED] |
| Completion percentage | [REDACTED] |
| Currency | [REDACTED] |
| Forecast-at-completion values | [REDACTED] |
| Forecast margin percentage | [REDACTED] |
| Actual profitability and margin | [REDACTED] |
| Cumulative margin cashflow | [REDACTED] |
| Debts and debtor timing | [REDACTED] |

### Source-data reconciliation required

- The supplied dashboard text contained conflicting completion percentages. The actual values and their report context have been masked; Finance must resolve the conflict using an authorized source before any real baseline is used.
- The flattened report text did not preserve all row/column boundaries. Do not infer field mappings or totals from text order.
- Summary, forecast-at-completion, actual-profitability, and cashflow sections are different measures. Do not merge or substitute them.
- No comparable monthly details for named clients or subconsultants are included here. Use synthetic test values for those scenarios.
- The repository's sample forecast CSV contains generic prototype data and does not represent the anonymized reference project. It must not be presented as actual project history.
- PFF access and a live integration have not been established by this brief. Any initial implementation should identify figures as manually entered or synthetic fixture data until an approved integration is available.

## 7. Ticket backlog and UAT acceptance criteria

Priority: **P0** = required for the first usable release; **P1** = important follow-up; **P2** = later enhancement.

| Ticket | Priority | User story | Acceptance criteria / UAT |
|---|---|---|---|
| NS-101 — Project baseline and monthly snapshots | P0 | As a Project Manager, I want to open a project with its approved and current monthly figures so that I know what I am updating. | Given a project with an approved snapshot, when I open it, then I see project number/name, reporting period, currency, approved forecast, actuals, margin, margin %, cashflow, and source/status labels. Given an unverified or incomplete field, then it is visibly marked as such and is not silently shown as zero. Given a new month, then saving a new snapshot does not overwrite the previous approved snapshot. |
| NS-102 — Guided monthly-update entry point | P0 | As a project user, I want NorthStar to ask what changed this month so that I can provide updates without navigating a dense financial report. | Given a project and reporting month, when I start an update, then NorthStar asks “What changed on this project this month?” and presents selectable topics: Client / scope, Subconsultants, Salary, Expenses, Contingency, Debts, Cashflow / invoicing, Schedule, and Other. I can select multiple topics, skip a topic, save a draft, and see which topics remain unanswered. |
| NS-103 — Client and scope changes | P0 | As a Project Manager, I want to record a client scope or fee change so that its forecast impact is visible. | Given the Client / scope topic, when I select it, then I can record the client, scope change, effective month, fee/revenue amount or estimate, status, and note. When a removed scope reduces forecast revenue, the comparison shows the entered revenue delta and its estimated effect on margin, using the approved calculation rules. If amount or prior baseline is missing, the impact is labelled incomplete rather than guessed. |
| NS-104 — Subconsultant invoice drill-down | P0 | As a Project Accountant, I want to enter this month's subconsultant invoice by supplier so that I can explain cost movement. | Given the Subconsultants topic, when I open it, then I can choose or add a supplier and enter invoice amount, invoice/reporting period, actual-versus-forecast status, and optional note/reference. The view compares the amount with the same supplier and comparable period last month when that data exists. If the amount is higher, it shows the absolute and percentage increase and an estimated margin impact equal to the mapped cost change, subject to the Finance-approved margin treatment. Missing prior supplier data is explicitly shown as “no comparable prior-month value.” |
| NS-105 — Salary and resourcing changes | P0 | As a Project Accountant, I want to explain salary or resourcing changes so that project-cost movement is not hidden in a single total. | Given the Salary topic, when I enter current-month actual or forecast salary cost and an optional reason (hours, rate, staffing, or adjustment), then NorthStar compares it with the comparable prior value and reports the amount and estimated margin effect. The screen identifies actual versus forecast and prevents an actual from being compared with a forecast without a clear label. |
| NS-106 — Expenses and contingency | P0 | As a Project Accountant, I want to record expense and contingency changes separately so that I can see which category moved. | Given either topic, when I enter an amount and period/status, then NorthStar retains the categories separately, compares against the prior month where available, and displays the signed variance and estimated effect on margin. A contingency release/use is not silently reclassified as an expense; any accounting treatment follows the configured Finance mapping. |
| NS-107 — Debts, invoicing, and cashflow | P1 | As a Project Accountant, I want to update debt and cash collection information so that margin and cash timing are not confused. | Given the Debts or Cashflow / invoicing topic, when I record the value and as-of date, then NorthStar labels debts outstanding separately from revenue, margin, and cash received. Debts exclude tax only when the source says they do. Cash delay is displayed with its basis (for example, manual assumption). The dashboard does not imply that a debt movement directly changes project margin unless a mapped adjustment is explicitly recorded. |
| NS-108 — Schedule and completion changes | P1 | As a Project Manager, I want to record end-date and completion changes so that the forecast reflects schedule risk. | Given the Schedule topic, when I change current end date, original end date, or completion percentage, then NorthStar preserves the original baseline, shows prior/current values, and labels the movement. It does not calculate a financial impact from schedule movement unless there is an explicit, reviewable financial input or approved model. |
| NS-109 — Variance comparison and explanation | P0 | As a project user, I want to see what changed versus last month and why the total moved so that I can review the forecast drivers. | Given comparable current and previous values, when the update is calculated, then NorthStar shows previous value, current value, signed variance, unit, period, source, and a category/item-level bridge. For every impact statement, I can open the underlying item and calculation. The displayed category deltas reconcile to the displayed total within currency rounding. If data is insufficient, NorthStar explains what is missing and does not fabricate a cause. |
| NS-110 — Forecast, actual, and approved status controls | P0 | As a Finance Reviewer, I want actuals, forecasts, drafts, and approved figures clearly separated so that I can avoid comparing unlike values. | Given financial values with different bases or statuses, when they are displayed or compared, then each is labelled actual, forecast, or approved and includes a reporting/as-of period. A month-on-month actual comparison uses comparable actual periods; forecast-at-completion change is shown separately. Rejected/returned drafts do not appear as approved. |
| NS-111 — Review, approval, and audit history | P1 | As a Finance Reviewer, I want to review and approve a monthly update with a change history so that the result is auditable. | Given a submitted update, when I review it, then I can approve or return it with a reason. The system records who created/edited/submitted/reviewed it and when, plus before/after values and source references. Approval locks that snapshot from ordinary editing; a subsequent correction creates a traceable revision rather than erasing history. |
| NS-112 — Source-data validation and import reconciliation | P0 | As a Project Accountant, I want imported or entered values validated against their source structure so that malformed data does not corrupt the forecast. | Given a source file or entered baseline, when required identifiers, periods, currency, units, or row/column mapping are missing or contradictory, then NorthStar reports the exact validation issue and prevents approval until it is resolved or explicitly waived by an authorized reviewer. Imported values retain source and import timestamp. Ambiguous flattened report text is not mapped by positional guesswork. |
| NS-113 — Project access and protected test data | P0 | As a project user, I want to see only authorized project data so that financial information remains appropriately controlled. | Given a user without project access, when they try to open a project or its update endpoint, then no project financial data is returned. Given a UAT environment, then test execution uses synthetic or explicitly authorized records, and test records are clearly distinguishable from live/approved records. |
| NS-114 — UAT dashboard and portfolio navigation | P2 | As a finance lead, I want to find projects with pending updates or material changes so that I can focus review effort. | Given multiple authorized projects, when I open the portfolio view, then I can identify each project's reporting month, update status, and material forecast/margin movement. Filtering does not expose projects outside the user's access. A project with no approved baseline is labelled “baseline required,” not ranked as healthy by default. |

## 8. Core UAT scenarios

| Scenario | Given | When | Expected result |
|---|---|---|---|
| No change this month | A project has a complete prior-month baseline | User records no changes and confirms all applicable topics | No artificial variance is created; unchanged values remain unchanged; the month is still clearly identified as reviewed. |
| Higher subconsultant invoice | Supplier A has a comparable prior-month amount and a higher current-month amount | User enters the current invoice as actual | Supplier-level increase, current/prior values, and the estimated margin decrease are shown; the item-level bridge reconciles to the total. |
| Client removes scope | A fee/revenue baseline exists | User enters a scope removal and its fee decrease | Forecast revenue decreases by the entered amount; estimated margin effect follows the configured calculation; note/status is retained. |
| No supplier comparison exists | A new supplier is entered this month | User records the invoice | The item is shown as new/no comparable prior value; no fictitious month-over-month percentage is produced. |
| Actual compared to forecast | Prior value is forecast; current value is actual | User views variance | NorthStar labels the basis mismatch and does not present it as a like-for-like actual variance. |
| Ambiguous source totals | Imported source contains conflicting FPC or unresolved row totals | User attempts to submit/approve | Validation identifies the conflict and blocks approval pending reconciliation or authorized waiver. |
| Zero net revenue | A project's net revenue is zero | Margin percentage is calculated | Margin amount may display if inputs support it; margin percentage displays as unavailable/not meaningful, with no divide-by-zero error. |
| Draft correction | A submitted update is returned for correction | User changes an entered amount and resubmits | Change history retains the returned and corrected values, editor, timestamps, and reviewer reason. |

## 9. Definition of Ready for first build

- Finance confirms the authoritative definitions and category mappings for net revenue, project margin, margin percentage, cashflow, FPC, actuals, and forecast-at-completion.
- Finance resolves the conflicting/ambiguous values in the supplied PFF snapshot before it is used as a numeric baseline.
- Product owner confirms the reporting month convention, whether updates are actual-to-date or full-month values, and who may approve a submission.
- Product owner confirms whether project and supplier names/amounts may be stored in this prototype and what test dataset is authorized.
- The team agrees which approved source systems, if any, will provide project, invoice, payroll, debt, and forecast data. Until then, data-entry and import states must be labelled accurately.

## 10. Open decisions

1. Which finance definition and cost categories should drive project margin and net revenue?
2. Is the workflow limited to monthly actuals, or must users also revise forecast-at-completion in the same update?
3. What constitutes a comparable month for invoices, especially accruals, late invoices, and partial periods?
4. Should approval be required for every monthly update, or only forecast changes above a Finance-defined threshold?
5. Which fields may contain free text or supporting evidence, and what retention/access policy applies?
6. Which source-system integration is in scope for the first release? No connection to the PFF URLs is assumed by this requirements document.
