"""Evaluate a simple, explainable transaction-risk rule on demo data."""

import random

from dashboard_utils import bar_panel, make_record, save_dashboard, save_project_data, scatter_panel


def main() -> None:
    rng = random.Random(707)
    channels = ["In-store", "Web", "Mobile", "International"]
    rows, amounts, risk_points = [], [], []
    predicted = []
    actual = []
    channel_fraud = [0] * len(channels)
    channel_counts = [0] * len(channels)
    for index in range(900):
        amount = round(rng.lognormvariate(4.2, 0.85), 2)
        channel = rng.choices(range(4), weights=[0.36, 0.30, 0.25, 0.09])[0]
        risk = int(amount > 350) + int(channel == 3) + int(rng.random() < 0.08)
        fraud_probability = 0.025 + 0.20 * int(amount > 350) + 0.22 * int(channel == 3)
        is_fraud = int(rng.random() < fraud_probability)
        flag = int(risk >= 2)
        rows.append([f"T{index + 1:05d}", amount, channels[channel], risk, is_fraud, flag])
        amounts.append(amount)
        actual.append(is_fraud)
        predicted.append(flag)
        channel_counts[channel] += 1
        channel_fraud[channel] += is_fraud
        risk_points.append((amount, risk))
    tp = sum(a == 1 and p == 1 for a, p in zip(actual, predicted))
    fp = sum(a == 0 and p == 1 for a, p in zip(actual, predicted))
    fn = sum(a == 1 and p == 0 for a, p in zip(actual, predicted))
    tn = len(rows) - tp - fp - fn
    save_project_data(
        "markets_risk_forecasts.csv", "day_07_transaction_risk", "transaction",
        [make_record(transaction_id, category="transaction", segment=channel,
                     metrics=[("amount_usd", amount), ("risk_flags", risk),
                              ("actual_fraud", is_fraud), ("rule_flag", rule_flag)])
         for transaction_id, amount, channel, risk, is_fraud, rule_flag in rows],
    )
    fraud_rates = [100 * fraud / count for fraud, count in zip(channel_fraud, channel_counts)]
    save_dashboard(
        filename="day_07_fraud_dashboard.svg",
        title="Transaction risk review",
        subtitle="Illustrative threshold rules on simulated transactions  |  not a production fraud model",
        kpis=[
            ("TRANSACTIONS", f"{len(rows):,}", "synthetic sample"),
            ("OBSERVED FRAUD", f"{sum(actual):,}", f"{100 * sum(actual) / len(rows):.1f}% base rate"),
            ("RULE PRECISION", f"{tp / max(tp + fp, 1):.1%}", "flagged cases that are fraud"),
            ("RULE RECALL", f"{tp / max(tp + fn, 1):.1%}", "fraud cases flagged"),
        ],
        panels=[
            bar_panel("Rule outcome counts", ["True positive", "False positive", "False negative", "True negative"],
                      [tp, fp, fn, tn]),
            bar_panel("Observed fraud rate by channel (%)", channels, fraud_rates),
            scatter_panel("Amount and rule risk score", risk_points[::5], "Transaction amount ($)", "Risk flags"),
            bar_panel("Flag rate by channel (%)", channels, [
                100 * sum(row[5] for row in rows if row[2] == channel) / max(channel_counts[i], 1)
                for i, channel in enumerate(channels)
            ]),
        ],
    )
    print(f"Fraud-rule demo complete: {sum(actual)} simulated fraud cases; "
          f"{tp} true positives and {fp} false positives.")


if __name__ == "__main__":
    main()

# Insight:
# This code snippet simulates a transaction fraud detection scenario using a simple rule-based approach. It generates synthetic transaction data, evaluates a risk rule based on transaction amount and channel, and calculates performance metrics such as true positives, false positives, and fraud rates by channel. The results are saved to a CSV file and visualized in a dashboard. The code is structured to provide insights into the effectiveness of the rule in identifying fraudulent transactions.