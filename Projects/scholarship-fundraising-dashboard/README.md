# Scholarship Fundraising Dashboard

End-to-end BI project simulating a university scholarship fundraising program funded by corporate donations, inspired by real-world fundraising operations in higher education.

> **Note on data:** the donor and scholarship data in this project is **synthetic** (no real institution's data is used). The exchange rate series is **real public data** from Argentina's Central Bank (BCRA), sourced through the official [datos.gob.ar](https://datos.gob.ar) API.

## Business Problem

Universities running donor-funded scholarship programs often price scholarships in USD (to protect against local currency inflation) while receiving and reporting in local currency. This creates two recurring challenges:

1. **Tracking fundraising performance against a USD-denominated target**, when donations arrive at different stages (*committed → recognized → accrued*) and only *recognized + accrued* should count toward the goal.
2. **Understanding the real purchasing power of donations over time**, since local currency depreciation can erode the value of pledges made months earlier.

This project builds a dashboard that answers both.

## Data Sources

| Source | Type | Description |
|---|---|---|
| `donantes.csv`, `donaciones.csv`, `becas.csv` | Synthetic | Generated with realistic business logic (see `scripts/02_generate_scholarship_data.py`) |
| `tipo_cambio_oficial.csv` | Real, public | Official USD/ARS exchange rate, BCRA via datos.gob.ar (see `scripts/01_fetch_fx_rate.py`) |

## Business Logic

- **Target measure** = `recognized + accrued` donations (in USD). Committed donations are pipeline only.
- **`arancel_usd` (scholarship cost) is a divisor**, never summed across scholarships — it's used to compute averages or "how many scholarships does this donation fund," not as an additive total.
- 7 scholarship product types are tracked separately.
- Fiscal year ("Ejercicio") runs March–February, not calendar year.

## Project Structure

```
scholarship-fundraising-dashboard/
├── README.md
├── data/                          ← generated CSVs (synthetic + real FX data)
├── scripts/
│   ├── 01_fetch_fx_rate.py        ← pulls real USD/ARS data (run locally)
│   └── 02_generate_scholarship_data.py  ← generates synthetic donor/scholarship data
├── sql/
│   ├── schema.sql                 ← table definitions
│   └── analysis_queries.sql       ← KPI and analysis queries
└── powerbi/
    └── dax_measures.md            ← DAX measures + suggested visuals
```

## How to Reproduce

1. Run `scripts/01_fetch_fx_rate.py` locally to pull the real exchange rate series.
2. Run `scripts/02_generate_scholarship_data.py` to generate the synthetic donation/scholarship data.
3. Load all CSVs into a SQLite database using `sql/schema.sql`.
4. Run the queries in `sql/analysis_queries.sql` to validate the business logic.
5. Connect Power BI to the database (or the CSVs directly) and build the measures in `powerbi/dax_measures.md`.

## Key Insights *(to fill in once the dashboard is built)*

- [ ] % of annual target achieved by fiscal year
- [ ] Which scholarship product type drives the most funding
- [ ] Top donor sectors by contribution
- [ ] Impact of exchange rate volatility on the real value of committed donations

## Tools

Python (pandas, requests) · SQL (SQLite) · Power BI (DAX, Power Query)
