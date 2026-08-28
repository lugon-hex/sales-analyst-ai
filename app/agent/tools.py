from app.database.connection import get_connection


def get_database_schema() -> str:
    """
    Retorna o schema do banco como texto.
    """

    connection = get_connection()

    try:
        tables = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name NOT LIKE 'sqlite_%'
            ORDER BY name
            """
        ).fetchall()

        schema_parts = []

        for table in tables:
            table_name = table["name"]

            columns = connection.execute(
                f"PRAGMA table_info({table_name})"
            ).fetchall()

            schema_parts.append(
                f"TABLE {table_name}:"
            )

            for column in columns:
                schema_parts.append(
                    f"  - {column['name']} "
                    f"({column['type']})"
                )

        return "\n".join(schema_parts)

    finally:
        connection.close()