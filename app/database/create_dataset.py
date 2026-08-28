from pathlib import Path
import random

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
DATASET_PATH = DATA_DIR / "sales.csv"

NUM_ROWS = 5000

random.seed(42)


LOCATIONS = {
    "São Paulo": "SP",
    "Rio de Janeiro": "RJ",
    "Niterói": "RJ",
    "Belo Horizonte": "MG",
    "Brasília": "DF",
    "Salvador": "BA",
    "Curitiba": "PR",
    "Porto Alegre": "RS",
    "Recife": "PE",
    "Fortaleza": "CE",
}


PRODUCTS = [
    {
        "product_id": 1,
        "product_name": "Notebook Pro",
        "category": "Computers",
        "unit_price": 4500.0,
    },
    {
        "product_id": 2,
        "product_name": "Keyboard Mechanical",
        "category": "Accessories",
        "unit_price": 350.0,
    },
    {
        "product_id": 3,
        "product_name": "Monitor 27",
        "category": "Monitors",
        "unit_price": 1200.0,
    },
    {
        "product_id": 4,
        "product_name": "Mouse Wireless",
        "category": "Accessories",
        "unit_price": 180.0,
    },
    {
        "product_id": 5,
        "product_name": "Headset Pro",
        "category": "Accessories",
        "unit_price": 450.0,
    },
    {
        "product_id": 6,
        "product_name": "SSD 1TB",
        "category": "Storage",
        "unit_price": 700.0,
    },
    {
        "product_id": 7,
        "product_name": "Webcam Full HD",
        "category": "Accessories",
        "unit_price": 300.0,
    },
    {
        "product_id": 8,
        "product_name": "Tablet Pro",
        "category": "Tablets",
        "unit_price": 2800.0,
    },
    {
        "product_id": 9,
        "product_name": "External HD 2TB",
        "category": "Storage",
        "unit_price": 500.0,
    },
    {
        "product_id": 10,
        "product_name": "Laptop Stand",
        "category": "Accessories",
        "unit_price": 250.0,
    },
]


STATUSES = [
    "completed",
    "completed",
    "completed",
    "completed",
    "completed",
    "cancelled",
]


def create_dataset() -> pd.DataFrame:
    rows = []

    cities = list(LOCATIONS.keys())

    for order_id in range(1, NUM_ROWS + 1):
        customer_id = random.randint(1, 500)

        customer_name = f"Customer {customer_id}"

        city = random.choice(cities)

        state = LOCATIONS[city]

        product = random.choice(PRODUCTS)

        quantity = random.randint(1, 5)

        unit_price = product["unit_price"]

        total_amount = quantity * unit_price

        order_date = (
            pd.Timestamp("2026-01-01")
            + pd.Timedelta(
                days=random.randint(0, 239)
            )
        )

        status = random.choice(STATUSES)

        rows.append(
            {
                "order_id": order_id,
                "customer_id": customer_id,
                "customer_name": customer_name,
                "city": city,
                "state": state,
                "product_id": product["product_id"],
                "product_name": product["product_name"],
                "category": product["category"],
                "quantity": quantity,
                "unit_price": unit_price,
                "total_amount": total_amount,
                "order_date": order_date.strftime("%Y-%m-%d"),
                "status": status,
            }
        )

    return pd.DataFrame(rows)


def main():
    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    df = create_dataset()

    df.to_csv(
        DATASET_PATH,
        index=False,
    )

    print(f"Dataset created: {DATASET_PATH}")
    print(f"Rows: {len(df)}")
    print()

    print(df.head())
    print()

    print("Location validation:")

    validation = (
        df[["city", "state"]]
        .drop_duplicates()
        .sort_values(["state", "city"])
    )

    print(validation.to_string(index=False))


if __name__ == "__main__":
    main()