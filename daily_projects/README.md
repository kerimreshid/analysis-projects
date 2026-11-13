# Daily Analysis Portfolio

A 10-project analytics portfolio. Each Python script creates a small, reproducible
synthetic dataset and a **rendered SVG dashboard**. The dashboards are pictures,
not notebook code; all project and chart-generation code lives here in
`daily_projects/`.

## View the dashboards

Open [`../dashbords/index.html`](../dashbords/index.html) in a browser to browse
the portfolio, or open an individual SVG from
[`../dashbords/visualizations/`](../dashbords/visualizations/).

## Run a project

From the repository root, run any day:

```bash
python daily_projects/day_01_sales_analysis.py
```

Each script updates its rows in one of the three shared tables in
`daily_projects/data/` and refreshes its dashboard in
`dashbords/visualizations/`. Running a script again replaces only that
project's matching record type; outputs from the other projects are preserved.
Run all projects with:

```bash
for project in daily_projects/day_*.py; do python "$project"; done
```

The projects use only the Python standard library; no package installation is
required. Output is deterministic and synthetic, so it is suitable for
demonstration and practice, not for operational decisions.

## Shared data tables

The portfolio keeps its outputs in three CSV files:

| File | Included projects |
|---|---|
| [commercial_analytics.csv](data/commercial_analytics.csv) | Sales, customer segments, customer sentiment, website traffic, and product recommendations |
| [markets_risk_forecasts.csv](data/markets_risk_forecasts.csv) | Market trends, transaction risk, and revenue forecasting |
| [people_health.csv](data/people_health.csv) | Workforce experience and healthcare admissions |

All tables use the same columns: `project`, `record_type`, `record_id`,
`date`, `category`, `segment`, four `metric_N` / `value_N` pairs, `status`,
and `details`. Metric names explain each numeric value, so different project
types can share a table without losing their meaning. Blank fields mean that
the field does not apply to that record. `record_type` distinguishes multiple
outputs from one project, such as ratings and recommendations.

## Project index

| Day | Project | Analysis script | Dashboard |
|---|---|---|---|
| 01 | Sales performance | [day_01_sales_analysis.py](day_01_sales_analysis.py) | [View](../dashbords/visualizations/day_01_sales_dashboard.svg) |
| 02 | Customer segments | [day_02_customer_segmentation.py](day_02_customer_segmentation.py) | [View](../dashbords/visualizations/day_02_customer_segmentation_dashboard.svg) |
| 03 | Market trends | [day_03_stock_trends.py](day_03_stock_trends.py) | [View](../dashbords/visualizations/day_03_stock_dashboard.svg) |
| 04 | Customer sentiment | [day_04_sentiment_analysis.py](day_04_sentiment_analysis.py) | [View](../dashbords/visualizations/day_04_sentiment_dashboard.svg) |
| 05 | Website traffic | [day_05_website_traffic.py](day_05_website_traffic.py) | [View](../dashbords/visualizations/day_05_traffic_dashboard.svg) |
| 06 | Product recommendations | [day_06_recommendations.py](day_06_recommendations.py) | [View](../dashbords/visualizations/day_06_recommendations_dashboard.svg) |
| 07 | Transaction risk | [day_07_fraud_detection.py](day_07_fraud_detection.py) | [View](../dashbords/visualizations/day_07_fraud_dashboard.svg) |
| 08 | Workforce experience | [day_08_employee_performance.py](day_08_employee_performance.py) | [View](../dashbords/visualizations/day_08_employee_dashboard.svg) |
| 09 | Admission patterns | [day_09_healthcare_analysis.py](day_09_healthcare_analysis.py) | [View](../dashbords/visualizations/day_09_healthcare_dashboard.svg) |
| 10 | Forecast backtest | [day_10_financial_forecast.py](day_10_financial_forecast.py) | [View](../dashbords/visualizations/day_10_forecast_dashboard.svg) |
