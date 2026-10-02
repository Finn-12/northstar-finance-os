from __future__ import annotations

import csv
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

import streamlit as st

from src.forecasting.monthly_variance import compare_amounts


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEMO_HISTORY_PATH = PROJECT_ROOT / "src" / "data" / "raw" / "mvp_subconsultant_history.csv"
REPORTING_MONTH = "2026-10"
TOPICS = (
    "Subconsultants",
    "Client / scope",
    "Salary",
    "Expenses",
    "Contingency",
    "Debts",
    "Cashflow / invoicing",
    "Schedule",
    "Other",
)


def load_demo_history(path: Path) -> dict[tuple[str, str], Decimal]:
    """Load the explicitly synthetic subconsultant comparison fixture."""
    history: dict[tuple[str, str], Decimal] = {}
    try:
        with path.open(newline="", encoding="utf-8") as csv_file:
            for row in csv.DictReader(csv_file):
                period = (row.get("period") or "").strip()
                supplier = (row.get("supplier") or "").strip()
                amount_text = (row.get("amount") or "").strip()
                if not period or not supplier or not amount_text:
                    raise ValueError("Each demo history row must include a period, supplier, and amount.")
                amount = Decimal(amount_text)
                date.fromisoformat(f"{period}-01")
                if not supplier or not amount.is_finite() or amount < 0:
                    raise ValueError("Supplier names and amounts must be valid and non-negative.")
                key = (period, supplier)
                if key in history:
                    raise ValueError(f"Duplicate demo history row for {period} / {supplier}.")
                history[key] = amount
    except (OSError, KeyError, InvalidOperation, ValueError) as error:
        raise RuntimeError(f"Could not load demo comparison data from {path}: {error}") from error
    return history


def previous_month(period: str) -> str:
    current = date.fromisoformat(f"{period}-01")
    if current.month == 1:
        return date(current.year - 1, 12, 1).strftime("%Y-%m")
    return date(current.year, current.month - 1, 1).strftime("%Y-%m")


def format_units(amount: Decimal) -> str:
    return f"CU {amount:,.2f}"


st.set_page_config(page_title="NorthStar Finance OS", layout="wide")
st.title("NorthStar Finance OS")
st.caption("MVP | Guided monthly project update")
st.warning(
    "Demo only: all displayed sample values are synthetic units, not live project data. "
    "Updates are held in this browser session and are not saved to a database. "
    "Do not enter confidential project or supplier information."
)

st.subheader("Demo project")
st.caption(f"Reporting period: {REPORTING_MONTH}")

try:
    demo_history = load_demo_history(DEMO_HISTORY_PATH)
except RuntimeError as error:
    st.error(str(error))
    st.stop()

topic = st.selectbox("What changed on this project this month?", TOPICS)
if topic != "Subconsultants":
    st.info(f"{topic} updates are planned for a later MVP iteration.")
    st.stop()

st.markdown("### Subconsultant invoice")
supplier_options = sorted({supplier for _, supplier in demo_history})
supplier_options.append("New supplier (no prior history)")
supplier = st.selectbox("Which supplier changed?", supplier_options)
basis = st.radio("What are you entering?", ("Actual invoice", "Forecast estimate"), horizontal=True)

prior_period = previous_month(REPORTING_MONTH)
prior_amount = demo_history.get((prior_period, supplier))

if basis == "Actual invoice" and prior_amount is not None:
    st.caption(f"Prior-period value ({prior_period}): {format_units(prior_amount)}")
else:
    st.caption(f"No comparable prior-period {basis.lower()} value is available.")

draft_key = (REPORTING_MONTH, supplier, basis)
default_amount = st.session_state.get(f"draft_amount:{draft_key}", Decimal("0"))
with st.form("subconsultant_update"):
    current_input = st.number_input(
        "Amount for this month (synthetic units)",
        min_value=0.0,
        value=float(default_amount),
        step=100.0,
        format="%.2f",
    )
    note = st.text_input("What changed? (optional; use non-confidential test text)")
    submitted = st.form_submit_button("Compare and save draft")

if submitted:
    current_amount = Decimal(str(current_input))
    st.session_state[f"draft_amount:{draft_key}"] = current_amount
    st.session_state[f"draft_note:{draft_key}"] = note.strip()
    st.session_state[f"draft_saved:{draft_key}"] = True

if st.session_state.get(f"draft_saved:{draft_key}"):
    current_amount = st.session_state[f"draft_amount:{draft_key}"]
    st.markdown("### Month-over-month comparison")
    if basis == "Actual invoice":
        comparison = compare_amounts(prior_amount, current_amount)
        if comparison.previous is None:
            st.info("No comparable prior-period value is available; no variance was calculated.")
        else:
            first, second, third = st.columns(3)
            first.metric("Prior period", format_units(comparison.previous))
            second.metric("This month", format_units(comparison.current))
            delta_label = (
                f"{format_units(comparison.delta)}"
                if comparison.delta is not None
                else "Unavailable"
            )
            third.metric(
                "Change in cost",
                delta_label,
                delta=(
                    f"{comparison.percentage_change:.1f}%"
                    if comparison.percentage_change is not None
                    else None
                ),
                delta_color="inverse",
            )
            if comparison.delta is not None:
                direction = "increased" if comparison.delta > 0 else "decreased"
                if comparison.delta == 0:
                    st.success("The entered cost is unchanged from the prior period.")
                else:
                    st.write(
                        f"The entered cost {direction} by "
                        f"**{format_units(abs(comparison.delta))}** versus "
                        f"{prior_period}."
                    )
                    st.info(
                        "This MVP reports the cost variance only. Any project-margin "
                        "impact depends on Finance-approved category mapping and is not "
                        "calculated here."
                    )
    else:
        st.info(
            "This MVP has no prior-period forecast baseline for comparison. "
            "The entered estimate is shown as a draft only."
        )
    st.success("Draft saved for this browser session only; it is not persisted.")
    saved_note = st.session_state.get(f"draft_note:{draft_key}", "")
    if saved_note:
        st.caption(f"Draft note: {saved_note}")

st.divider()
st.caption("MVP scope: one guided topic and an item-level subconsultant cost comparison.")
