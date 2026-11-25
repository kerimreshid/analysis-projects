"""Build a transparent popularity-based recommendation example."""

import random

from dashboard_utils import bar_panel, make_record, save_dashboard, save_project_data, scatter_panel


def main() -> None:
    rng = random.Random(606)
    products = [f"Product {letter}" for letter in "ABCDEFGHIJ"]
    categories = ["Outdoors", "Home", "Technology", "Style", "Kitchen"]
    ratings = {product: [] for product in products}
    rows = []
    user_preferences = {}
    for user in range(1, 181):
        preferred = rng.randrange(len(categories))
        user_preferences[user] = preferred
        for product_index, product in enumerate(products):
            category = product_index % len(categories)
            if rng.random() < (0.78 if category == preferred else 0.34):
                rating = round(min(5, max(1, rng.gauss(4.3 if category == preferred else 3.4, 0.65))), 1)
                ratings[product].append(rating)
                rows.append([f"U{user:03d}", product, categories[category], rating])
    product_means = {product: sum(scores) / len(scores) for product, scores in ratings.items()}
    coverage = {product: len(scores) for product, scores in ratings.items()}
    selected_user = 17
    preferred_category = user_preferences[selected_user]
    recommendations = sorted(
        [product for product in products if product not in {
            row[1] for row in rows if row[0] == f"U{selected_user:03d}"}],
        key=lambda product: (product_means[product] if product_means[product] else 0, coverage[product]),
        reverse=True,
    )[:5]
    save_project_data(
        "commercial_analytics.csv", "day_06_product_recommendations", "product_rating",
        [make_record(f"{user_id}:{product}", category="product", segment=category,
                     metrics=[("rating", rating)], details=user_id)
         for user_id, product, category, rating in rows],
    )
    save_project_data(
        "commercial_analytics.csv", "day_06_product_recommendations", "recommendation",
        [make_record(f"U{selected_user:03d}:{product}", category="product",
                     segment=categories[products.index(product) % len(categories)],
                     metrics=[("mean_rating", round(product_means[product], 2))],
                     status=f"rank_{rank}", details=f"sample_user=U{selected_user:03d}")
         for rank, product in enumerate(recommendations, 1)],
    )
    save_dashboard(
        filename="day_06_recommendations_dashboard.svg",
        title="Product discovery",
        subtitle="Offline recommendation demo  |  ranked by product rating and coverage, not personalized AI",
        kpis=[
            ("RATINGS", f"{len(rows):,}", "synthetic interactions"),
            ("CUSTOMERS", "180", "illustrative users"),
            ("CATALOG", str(len(products)), "demo products"),
            ("SUGGESTIONS", str(len(recommendations)), f"sample user U{selected_user:03d}"),
        ],
        panels=[
            bar_panel("Top recommendations for sample user", recommendations,
                      [product_means[product] for product in recommendations]),
            bar_panel("Average product rating", products, [product_means[p] for p in products]),
            bar_panel("Rating coverage by product", products, [coverage[p] for p in products]),
            scatter_panel("Ratings and coverage", [(coverage[p], product_means[p]) for p in products],
                          "Rating count", "Average rating"),
        ],
    )
    print(f"Recommendation demo complete: {len(recommendations)} suggestions for U{selected_user:03d} "
          f"(preferred category: {categories[preferred_category]}).")


if __name__ == "__main__":
    main()
