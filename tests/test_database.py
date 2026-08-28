from app.database.queries import (
    get_sales_by_product,
    get_sales_by_region,
    get_total_orders,
    get_total_revenue,
)


def test_total_revenue():
    result = get_total_revenue()

    assert len(result) == 1
    assert result[0]["revenue"] >= 0


def test_total_orders():
    result = get_total_orders()

    assert len(result) == 1
    assert result[0]["orders"] > 0


def test_products():
    result = get_sales_by_product()

    assert len(result) > 0
    assert "product_name" in result[0]


def test_regions():
    result = get_sales_by_region()

    assert len(result) > 0
    assert "state" in result[0]
import pytest

from app.database.queries import (
    execute_read_only_query,
)


def test_read_only_select():

    result = execute_read_only_query(
        """
        SELECT
            product_name,
            SUM(quantity) AS units
        FROM sales
        WHERE status = 'completed'
        GROUP BY product_name
        ORDER BY units DESC
        """
    )

    assert len(result) > 0
    assert "product_name" in result[0]


def test_read_only_with():

    result = execute_read_only_query(
        """
        WITH revenue AS (
            SELECT
                SUM(total_amount) AS total
            FROM sales
            WHERE status = 'completed'
        )
        SELECT *
        FROM revenue
        """
    )

    assert len(result) == 1


def test_insert_is_blocked():

    with pytest.raises(ValueError):

        execute_read_only_query(
            """
            INSERT INTO sales
            VALUES (99999)
            """
        )


def test_delete_is_blocked():

    with pytest.raises(ValueError):

        execute_read_only_query(
            """
            DELETE FROM sales
            """
        )


def test_drop_is_blocked():

    with pytest.raises(ValueError):

        execute_read_only_query(
            """
            DROP TABLE sales
            """
        )


def test_update_is_blocked():

    with pytest.raises(ValueError):

        execute_read_only_query(
            """
            UPDATE sales
            SET quantity = 0
            """
        )


def test_multiple_statements_are_blocked():

    with pytest.raises(ValueError):

        execute_read_only_query(
            """
            SELECT *
            FROM sales;

            SELECT *
            FROM sales;
            """
        )


def test_limit_is_restricted():

    with pytest.raises(ValueError):

        execute_read_only_query(
            """
            SELECT *
            FROM sales
            LIMIT 1000
            """
        )
