"""Review an illustrative market-price series, returns, and drawdown."""

import random

from dashboard_utils import bar_panel, line_panel, make_record, save_dashboard, save_project_data


def main() -> None:
    rng = random.Random(303)
    months = [f"2025-{month:02d}" for month in range(1, 13)]
    prices = [100.0]
    for _ in range(1, 12):
        prices.append(prices[-1] * (1 + 0.012 + rng.uniform(-0.055, 0.055)))
    prices = [round(price, 2) for price in prices]
    returns = [0.0] + [prices[i] / prices[i - 1] - 1 for i in range(1, len(prices))]
    peak, drawdowns = prices[0], []
    for price in prices:
        peak = max(peak, price)
        drawdowns.append((price / peak - 1) * 100)
    buckets = [-0.08, -0.04, 0, 0.04, 0.08]
    labels = ["< -4%", "-4 to 0%", "0 to 4%", "4 to 8%", "> 8%"]
    distribution = [0] * len(labels)
    for change in returns:
        slot = 0 if change < buckets[0] else 1 if change < buckets[1] else 2 if change < buckets[2] else 3 if change < buckets[3] else 4
        distribution[slot] += 1
    save_project_data(
        "markets_risk_forecasts.csv", "day_03_market_trends", "monthly_market_data",
        [make_record(month, date=month, category="market_index",
                     metrics=[("close_index", price), ("monthly_return_pct", round(change * 100, 2)),
                              ("drawdown_pct", round(drawdown, 2))])
         for month, price, change, drawdown in zip(months, prices, returns, drawdowns)],
    )
    annual_return = prices[-1] / prices[0] - 1
    save_dashboard(
        filename="day_03_stock_dashboard.svg",
        title="Market trend review",
        subtitle="Simulated monthly closing prices  |  illustrative data, not an investment signal",
        kpis=[
            ("STARTING PRICE", f"${prices[0]:.2f}", "index units"),
            ("ENDING PRICE", f"${prices[-1]:.2f}", "index units"),
            ("PERIOD RETURN", f"{annual_return:.1%}", "start-to-end"),
            ("MAX DRAWDOWN", f"{min(drawdowns):.1f}%", "peak-to-trough"),
        ],
        panels=[
            line_panel("Closing price", months, prices, "Close"),
            line_panel("Peak-to-trough drawdown", months, drawdowns, "Drawdown %"),
            bar_panel("Monthly return distribution", labels, distribution),
            bar_panel("Quarter-end prices", ["Q1", "Q2", "Q3", "Q4"],
                      [prices[i] for i in (2, 5, 8, 11)]),
        ],
    )
    print(f"Stock trend review complete: simulated period return {annual_return:.1%}.")


if __name__ == "__main__":
    main()
