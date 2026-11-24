"""Analyze synthetic site traffic, traffic sources, and conversion behavior."""

import random

from dashboard_utils import bar_panel, line_panel, make_record, save_dashboard, save_project_data


def main() -> None:
    rng = random.Random(505)
    sources = ["Search", "Direct", "Social", "Email"]
    pages = ["/home", "/pricing", "/products", "/help"]
    source_weights = [0.42, 0.27, 0.19, 0.12]
    source_sessions = [0] * len(sources)
    source_conversions = [0] * len(sources)
    page_views = [0] * len(pages)
    daily = [0] * 30
    rows = []
    for index in range(1800):
        day = rng.choices(range(30), weights=[0.8 + 0.4 * (i % 7 in (1, 2, 3)) for i in range(30)])[0]
        source_index = rng.choices(range(len(sources)), weights=source_weights)[0]
        page_index = rng.randrange(len(pages))
        converted = rng.random() < [0.035, 0.052, 0.025, 0.071][source_index]
        duration = round(rng.uniform(18, 780), 1)
        rows.append([f"S{index + 1:05d}", f"2025-06-{day + 1:02d}", sources[source_index],
                     pages[page_index], duration, int(converted)])
        source_sessions[source_index] += 1
        source_conversions[source_index] += int(converted)
        page_views[page_index] += 1
        daily[day] += 1
    save_project_data(
        "commercial_analytics.csv", "day_05_website_traffic", "website_session",
        [make_record(session_id, date=date, category="traffic_source", segment=source,
                     metrics=[("duration_seconds", duration), ("converted", converted)],
                     details=landing_page)
         for session_id, date, source, landing_page, duration, converted in rows],
    )
    conversion_rates = [100 * conversions / sessions for conversions, sessions
                        in zip(source_conversions, source_sessions)]
    save_dashboard(
        filename="day_05_traffic_dashboard.svg",
        title="Digital experience",
        subtitle="Thirty-day website session overview  |  all sessions and conversion events are synthetic",
        kpis=[
            ("SESSIONS", f"{len(rows):,}", "30-day sample"),
            ("CONVERSIONS", f"{sum(source_conversions):,}", "illustrative events"),
            ("CONVERSION RATE", f"{100 * sum(source_conversions) / len(rows):.1f}%", "sample-wide"),
            ("AVG. SESSION", f"{sum(row[4] for row in rows) / len(rows):.0f}s", "time on site"),
        ],
        panels=[
            line_panel("Daily sessions", [str(day) for day in range(1, 31)], daily, "Sessions"),
            bar_panel("Sessions by acquisition source", sources, source_sessions),
            bar_panel("Conversion rate by source (%)", sources, conversion_rates),
            bar_panel("Landing page views", pages, page_views),
        ],
    )
    print(f"Traffic analysis complete: {len(rows)} synthetic sessions, "
          f"{sum(source_conversions)} conversions.")


if __name__ == "__main__":
    main()
