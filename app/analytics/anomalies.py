from app.database.queries import get_revenue_by_month


def detect_revenue_anomalies(
    threshold: float = 0.15,
) -> list[dict]:

    monthly_data = get_revenue_by_month()

    anomalies = []

    for i in range(1, len(monthly_data)):
        previous = monthly_data[i - 1]
        current = monthly_data[i]

        previous_revenue = previous["revenue"]
        current_revenue = current["revenue"]

        if previous_revenue == 0:
            continue

        variation = (
            current_revenue - previous_revenue
        ) / previous_revenue

        if abs(variation) >= threshold:
            anomalies.append(
                {
                    "month": current["month"],
                    "previous_month": previous["month"],
                    "previous_revenue": previous_revenue,
                    "current_revenue": current_revenue,
                    "variation": round(
                        variation * 100,
                        2,
                    ),
                }
            )

    return anomalies