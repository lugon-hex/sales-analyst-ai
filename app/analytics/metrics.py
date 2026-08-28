from app.database.queries import (
    get_average_ticket,
    get_total_orders,
    get_total_revenue,
)


def calculate_kpis() -> dict:
    revenue_result = get_total_revenue()
    orders_result = get_total_orders()
    ticket_result = get_average_ticket()

    revenue = revenue_result[0]["revenue"] or 0
    orders = orders_result[0]["orders"] or 0
    average_ticket = ticket_result[0]["average_ticket"] or 0

    return {
        "revenue": revenue,
        "orders": orders,
        "average_ticket": average_ticket,
    }