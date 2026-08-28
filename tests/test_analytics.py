from app.analytics.anomalies import (
    detect_revenue_anomalies,
)

from app.analytics.metrics import (
    calculate_kpis,
)


def test_kpis():
    kpis = calculate_kpis()

    assert "revenue" in kpis
    assert "orders" in kpis
    assert "average_ticket" in kpis

    assert kpis["revenue"] >= 0
    assert kpis["orders"] > 0


def test_anomalies():
    anomalies = detect_revenue_anomalies()

    assert isinstance(anomalies, list)