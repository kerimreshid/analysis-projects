"""Score fictional customer messages with a small, explainable word lexicon."""

import random

from dashboard_utils import bar_panel, line_panel, make_record, save_dashboard, save_project_data


def main() -> None:
    rng = random.Random(404)
    positive = ["helpful", "great", "easy", "love", "fast", "excellent"]
    negative = ["slow", "broken", "confusing", "poor", "late", "difficult"]
    neutral = ["account", "order", "service", "product", "question", "update"]
    messages = []
    sentiment_counts = {"Positive": 0, "Neutral": 0, "Negative": 0}
    engagement = {"Positive": [], "Neutral": [], "Negative": []}
    monthly = [0] * 12
    for index in range(480):
        month = index % 12
        tone = rng.choices(["Positive", "Neutral", "Negative"], weights=[0.52, 0.27, 0.21])[0]
        vocabulary = positive if tone == "Positive" else negative if tone == "Negative" else neutral
        text = f"{rng.choice(vocabulary)} {rng.choice(neutral)} {rng.choice(vocabulary)}"
        score = 1 if tone == "Positive" else -1 if tone == "Negative" else 0
        likes = rng.randint(1, 85)
        messages.append([index + 1, f"2025-{month + 1:02d}", text, score, likes])
        sentiment_counts[tone] += 1
        engagement[tone].append(likes)
        monthly[month] += score
    avg_engagement = [sum(engagement[tone]) / max(len(engagement[tone]), 1)
                      for tone in sentiment_counts]
    months = [f"2025-{month:02d}" for month in range(1, 13)]
    save_project_data(
        "commercial_analytics.csv", "day_04_customer_sentiment", "customer_message",
        [make_record(str(message_id), date=month, category="customer_sentiment", segment=(
            "Positive" if score > 0 else "Negative" if score < 0 else "Neutral"
        ), metrics=[("sentiment_score", score), ("likes", likes)], details=text)
         for message_id, month, text, score, likes in messages],
    )
    positive_share = sentiment_counts["Positive"] / len(messages)
    save_dashboard(
        filename="day_04_sentiment_dashboard.svg",
        title="Customer voice",
        subtitle="Lexicon-based sentiment on fictional messages  |  sarcasm and context are not modeled",
        kpis=[
            ("MESSAGES", f"{len(messages):,}", "synthetic sample"),
            ("POSITIVE SHARE", f"{positive_share:.1%}", "rule-based classification"),
            ("NET SENTIMENT", f"{sum(monthly):+d}", "positive minus negative"),
            ("AVG. ENGAGEMENT", f"{sum(r[4] for r in messages) / len(messages):.0f}", "likes per message"),
        ],
        panels=[
            line_panel("Monthly net sentiment", months, monthly, "Net score"),
            bar_panel("Message volume by sentiment", list(sentiment_counts), list(sentiment_counts.values())),
            bar_panel("Average likes by sentiment", list(engagement), avg_engagement),
            bar_panel("Sentiment share (%)", list(sentiment_counts),
                      [100 * value / len(messages) for value in sentiment_counts.values()]),
        ],
    )
    print(f"Sentiment analysis complete: {len(messages)} fictional messages scored.")


if __name__ == "__main__":
    main()
