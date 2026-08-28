from typing import Any

from app.database.connection import get_connection


def execute_query(
    query: str,
    params: tuple[Any, ...] = (),
) -> list[dict]:
    connection = get_connection()

    try:
        cursor = connection.execute(
            query,
            params,
        )

        rows = cursor.fetchall()

        return [
            dict(row)
            for row in rows
        ]

    finally:
        connection.close()


def get_total_revenue() -> list[dict]:
    query = """
        SELECT
            ROUND(SUM(total_amount), 2) AS revenue
        FROM sales
        WHERE status = 'completed'
    """

    return execute_query(query)


def get_total_orders() -> list[dict]:
    query = """
        SELECT
            COUNT(*) AS orders
        FROM sales
        WHERE status = 'completed'
    """

    return execute_query(query)


def get_average_ticket() -> list[dict]:
    query = """
        SELECT
            ROUND(AVG(total_amount), 2) AS average_ticket
        FROM sales
        WHERE status = 'completed'
    """

    return execute_query(query)


def get_revenue_by_month() -> list[dict]:
    query = """
        SELECT
            strftime('%Y-%m', order_date) AS month,
            ROUND(SUM(total_amount), 2) AS revenue
        FROM sales
        WHERE status = 'completed'
        GROUP BY month
        ORDER BY month
    """

    return execute_query(query)


def get_sales_by_product() -> list[dict]:
    query = """
        SELECT
            product_name,
            SUM(quantity) AS units_sold,
            ROUND(SUM(total_amount), 2) AS revenue
        FROM sales
        WHERE status = 'completed'
        GROUP BY product_name
        ORDER BY revenue DESC
    """

    return execute_query(query)


def get_sales_by_region() -> list[dict]:
    query = """
        SELECT
            state,
            COUNT(*) AS orders,
            ROUND(SUM(total_amount), 2) AS revenue
        FROM sales
        WHERE status = 'completed'
        GROUP BY state
        ORDER BY revenue DESC
    """

    return execute_query(query)


def get_product_performance() -> list[dict]:
    query = """
        SELECT
            product_name,
            strftime('%Y-%m', order_date) AS month,
            SUM(quantity) AS units_sold,
            ROUND(SUM(total_amount), 2) AS revenue
        FROM sales
        WHERE status = 'completed'
        GROUP BY product_name, month
        ORDER BY month, revenue DESC
    """

    return execute_query(query)


def get_recent_sales(
    days: int = 30,
) -> list[dict]:

    query = """
        SELECT
            order_date,
            COUNT(*) AS orders,
            ROUND(SUM(total_amount), 2) AS revenue
        FROM sales
        WHERE
            status = 'completed'
            AND order_date >= date(
                'now',
                ?
            )
        GROUP BY order_date
        ORDER BY order_date
    """

    return execute_query(
        query,
        (f"-{days} days",),
    )


# ============================================================
# GENERIC READ-ONLY SQL
# ============================================================

def execute_read_only_query(
    query: str,
) -> list[dict]:

    query = query.strip()

    if not query:
        raise ValueError(
            "SQL query cannot be empty."
        )

    normalized = " ".join(
        query.lower().split()
    )

    # Only SELECT and WITH are allowed.
    if not (
        normalized.startswith("select ")
        or normalized.startswith("with ")
    ):
        raise ValueError(
            "Only SELECT or WITH queries are allowed."
        )

    # Dangerous SQL operations.
    forbidden_keywords = [
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "create",
        "replace",
        "truncate",
        "attach",
        "detach",
        "vacuum",
        "reindex",
        "pragma",
    ]

    for keyword in forbidden_keywords:

        if keyword in normalized:
            raise ValueError(
                f"Forbidden SQL operation: {keyword}"
            )

    # Prevent multiple SQL statements.
    #
    # A semicolon is allowed only at the end.
    if ";" in query[:-1]:
        raise ValueError(
            "Multiple SQL statements are not allowed."
        )

    # Prevent excessively large queries.
    if len(query) > 5000:
        raise ValueError(
            "SQL query is too long."
        )

    # Add a default LIMIT.
    normalized_with_spaces = f" {normalized} "

    if " limit " not in normalized_with_spaces:

        query = query.rstrip(";")

        query = (
            query
            + " LIMIT 100"
        )

    else:

        import re

        match = re.search(
            r"\blimit\s+(\d+)",
            normalized,
        )

        if match:

            limit = int(
                match.group(1)
            )

            if limit > 100:
                raise ValueError(
                    "LIMIT cannot be greater than 100."
                )

    return execute_query(query)