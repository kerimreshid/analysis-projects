"""Summarize fictional employee experience indicators without ranking people."""

import random

from dashboard_utils import bar_panel, make_record, save_dashboard, save_project_data, scatter_panel


def main() -> None:
    rng = random.Random(808)
    departments = ["Product", "Sales", "Operations", "Support"]
    rows, points = [], []
    attainment = {department: [] for department in departments}
    satisfaction = {department: [] for department in departments}
    for index in range(240):
        department = departments[index % len(departments)]
        goal = round(min(125, max(55, rng.gauss([96, 104, 98, 91][index % 4], 13))), 1)
        pulse = round(min(5, max(1, rng.gauss(3.2 + (goal - 95) / 55, 0.75))), 1)
        tenure = round(rng.uniform(0.3, 13), 1)
        rows.append([f"E{index + 1:04d}", department, tenure, goal, pulse])
        attainment[department].append(goal)
        satisfaction[department].append(pulse)
        points.append((pulse, goal))
    avg_attainment = [sum(attainment[d]) / len(attainment[d]) for d in departments]
    avg_satisfaction = [sum(satisfaction[d]) / len(satisfaction[d]) for d in departments]
    save_project_data(
        "people_health.csv", "day_08_workforce_experience", "employee_profile",
        [make_record(employee_id, category="employee", segment=department,
                     metrics=[("tenure_years", tenure), ("goal_attainment_pct", goal),
                              ("pulse_score", pulse)])
         for employee_id, department, tenure, goal, pulse in rows],
    )
    save_dashboard(
        filename="day_08_employee_dashboard.svg",
        title="Workforce experience",
        subtitle="Fictional, aggregated indicators  |  not a hiring, promotion, or performance decision tool",
        kpis=[
            ("EMPLOYEES", f"{len(rows):,}", "synthetic records"),
            ("AVG. GOAL ATTAINMENT", f"{sum(r[3] for r in rows) / len(rows):.1f}%", "illustrative"),
            ("AVG. PULSE SCORE", f"{sum(r[4] for r in rows) / len(rows):.2f}/5", "self-reported demo"),
            ("DEPARTMENTS", str(len(departments)), "represented"),
        ],
        panels=[
            bar_panel("Average goal attainment (%)", departments, avg_attainment),
            bar_panel("Average pulse score", departments, avg_satisfaction),
            scatter_panel("Satisfaction and goal attainment", points[::3], "Pulse score (1–5)", "Goal attainment (%)"),
            bar_panel("Employee records by department", departments,
                      [sum(r[1] == d for r in rows) for d in departments]),
        ],
    )
    print(f"Workforce experience analysis complete: {len(rows)} fictional employee records.")


if __name__ == "__main__":
    main()
