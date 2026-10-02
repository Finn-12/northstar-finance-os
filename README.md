# NorthStar Finance OS

## MVP

The first MVP slice is a Streamlit guided monthly update for a demo project. It currently supports a subconsultant invoice update, compares the entered actual with a synthetic prior-period amount, and retains the draft only in the current browser session.

All sample amounts are synthetic units. The app is not connected to PFF or a live finance system. Do not enter confidential project or supplier information. Margin impact, durable storage, approvals, and the other monthly-update topics are not included in this MVP.

Run from the repository root:

```powershell
streamlit run src/dashboards/streamlit_app.py
```

Run the focused variance tests:

```powershell
python -m unittest tests.test_monthly_variance
```

See [the delivery backlog](docs/monthly-update-delivery-backlog.md) for follow-up scope and [the implementation checklist](docs/implementation-checklist.md) to resume work.
