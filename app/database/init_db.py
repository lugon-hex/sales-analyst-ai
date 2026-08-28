from pathlib import Path

import pandas as pd

from app.database.connection import get_connection


ROOT_DIR = Path(__file__).resolve().parents[2]
CSV_FILE = ROOT_DIR / "data" / "sales.csv"


def initialize_database():
    if not CSV_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {CSV_FILE}"
        )

    df = pd.read_csv(CSV_FILE)

    connection = get_connection()

    try:
        df.to_sql(
            "sales",
            connection,
            if_exists="replace",
            index=False,
        )

        connection.commit()

    finally:
        connection.close()


if __name__ == "__main__":
    initialize_database()

    print("Database initialized successfully.")