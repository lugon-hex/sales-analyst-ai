from app.analytics.anomalies import (
    detect_revenue_anomalies,
)

from app.analytics.metrics import (
    calculate_kpis,
)


def main():
    print("Sales Analyst AI")
    print("================")

    kpis = calculate_kpis()

    print(
        f"Revenue: R$ {kpis['revenue']:,.2f}"
    )

    print(
        f"Orders: {kpis['orders']:,}"
    )

    print(
        f"Average ticket: "
        f"R$ {kpis['average_ticket']:,.2f}"
    )

    print()

    anomalies = detect_revenue_anomalies()

    print(
        f"Anomalies detected: {len(anomalies)}"
    )


if __name__ == "__main__":
    main()