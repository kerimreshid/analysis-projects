"""Explore sales trends, category mix, and regional performance."""

import random

from dashboard_utils import bar_panel, line_panel, make_record, save_dashboard, save_project_data


def main() -> None:
    rng = random.Random(101)
    months = [f"2025-{month:02d}" for month in range(1, 13)]
    categories = ["Technology", "Home", "Outdoor", "Accessories"]
    regions = ["North", "South", "East", "West"]
    monthly_revenue = [round(21000 + i * 780 + 3200 * ((i % 4) - 1.5) + rng.randrange(-1600, 1600), 2)
                       for i in range(12)]
    category_revenue = [round(sum(monthly_revenue) * share, 2)
                        for share in (0.36, 0.27, 0.21, 0.16)]
    region_revenue = [round(sum(monthly_revenue) * share, 2)
                      for share in (0.31, 0.25, 0.24, 0.20)]
    orders = 1840
    revenue = sum(monthly_revenue)
    save_project_data(
        "commercial_analytics.csv", "day_01_sales", "monthly_revenue",
        [make_record(month, date=month, category="monthly_revenue",
                     metrics=[("revenue_usd", amount)])
         for month, amount in zip(months, monthly_revenue)],
    )
    save_dashboard(
        filename="day_01_sales_dashboard.svg",
        title="Sales performance",
        subtitle="Twelve-month commercial overview  |  deterministic synthetic transactions",
        kpis=[
            ("GROSS REVENUE", f"${revenue:,.0f}", "12-month total"),
            ("ORDERS", f"{orders:,}", "illustrative order volume"),
            ("AVERAGE ORDER", f"${revenue / orders:,.2f}", "revenue per order"),
            ("REVENUE GROWTH", f"{(monthly_revenue[-1] / monthly_revenue[0] - 1):.1%}", "first to final month"),
        ],
        panels=[
            line_panel("Monthly revenue", months, monthly_revenue, "Revenue"),
            bar_panel("Revenue by category", categories, category_revenue),
            bar_panel("Revenue by region", regions, region_revenue),
            bar_panel("Quarterly revenue", ["Q1", "Q2", "Q3", "Q4"],
                      [sum(monthly_revenue[i:i + 3]) for i in range(0, 12, 3)]),
        ],
    )
    print(f"Sales analysis complete: ${revenue:,.0f} revenue across {orders:,} demo orders.")


if __name__ == "__main__":
    main()
