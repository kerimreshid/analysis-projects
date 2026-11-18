"""Profile customer groups using transparent, rule-based spending bands."""

import random

from dashboard_utils import bar_panel, make_record, save_dashboard, save_project_data, scatter_panel


def main() -> None:
    rng = random.Random(202)
    personas = [
        ("Occasional", 65, 2.4, 38),
        ("Regular", 90, 6.2, 54),
        ("Premium", 45, 5.1, 145),
        ("Loyal", 100, 10.3, 72),
    ]
    counts, spend, orders, rows, points = [], [], [], [], []
    for segment, (name, size, mean_orders, average_order) in enumerate(personas):
        segment_spend = []
        segment_orders = []
        for customer in range(size):
            visits = max(1, round(rng.gauss(mean_orders, max(1, mean_orders * 0.22))))
            total = round(max(20, rng.gauss(average_order * visits, average_order * visits * 0.18)), 2)
            segment_orders.append(visits)
            segment_spend.append(total)
            rows.append([f"C{segment * 1000 + customer + 1:04d}", name, visits, total])
            points.append((visits, total))
        counts.append(size)
        spend.append(sum(segment_spend) / size)
        orders.append(sum(segment_orders) / size)
    save_project_data(
        "commercial_analytics.csv", "day_02_customer_segments", "customer_profile",
        [make_record(customer_id, category="customer", segment=segment,
                     metrics=[("orders", customer_orders), ("annual_spend_usd", annual_spend)])
         for customer_id, segment, customer_orders, annual_spend in rows],
    )
    save_dashboard(
        filename="day_02_customer_segmentation_dashboard.svg",
        title="Customer segments",
        subtitle="RFM-style customer profiles  |  rule-based synthetic personas, not learned clusters",
        kpis=[
            ("CUSTOMERS", f"{sum(counts):,}", "profiled customers"),
            ("SEGMENTS", str(len(personas)), "illustrative spending bands"),
            ("AVG. ANNUAL SPEND", f"${sum(r[3] for r in rows) / len(rows):,.0f}", "per customer"),
            ("TOP SEGMENT", personas[spend.index(max(spend))][0], "highest average spend"),
        ],
        panels=[
            bar_panel("Customers by segment", [p[0] for p in personas], counts),
            bar_panel("Average spend by segment", [p[0] for p in personas], spend),
            bar_panel("Average annual orders", [p[0] for p in personas], orders),
            scatter_panel("Spend and purchase frequency", points, "Orders / year", "Annual spend ($)"),
        ],
    )
    print(f"Customer segmentation complete: {sum(counts)} demo customers in {len(personas)} profiles.")


if __name__ == "__main__":
    main()
