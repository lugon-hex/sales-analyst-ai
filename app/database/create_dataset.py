from pathlib import Path

import numpy as np
import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = DATA_DIR / "sales.csv"

SEED = 42
N_ORDERS = 5000

rng = np.random.default_rng(SEED)


def generate_dataset() -> pd.DataFrame:
    customers = pd.DataFrame(
        {
            "customer_id": np.arange(1, 501),
            "customer_name": [
                f"Customer {i}" for i in range(1, 501)
            ],
            "city": rng.choice(
                [
                    "Rio de Janeiro",
                    "São Paulo",
                    "Niterói",
                    "Belo Horizonte",
                    "Curitiba",
                    "Porto Alegre",
                    "Salvador",
                    "Brasília",
                ],
                500,
            ),
            "state": rng.choice(
                [
                    "RJ",
                    "SP",
                    "MG",
                    "PR",
                    "RS",
                    "BA",
                    "DF",
                ],
                500,
            ),
        }
    )

    products = pd.DataFrame(
        {
            "product_id": range(1, 11),
            "product_name": [
                "Notebook Pro",
                "Notebook Air",
                "Monitor 24",
                "Monitor 27",
                "Keyboard Mechanical",
                "Mouse Wireless",
                "Headset Pro",
                "Webcam HD",
                "SSD 1TB",
                "USB Hub",
            ],
            "category": [
                "Computers",
                "Computers",
                "Monitors",
                "Monitors",
                "Accessories",
                "Accessories",
                "Accessories",
                "Accessories",
                "Storage",
                "Accessories",
            ],
            "price": [
                5500,
                3800,
                1200,
                1800,
                450,
                180,
                650,
                350,
                700,
                150,
            ],
        }
    )

    dates = pd.date_range(
        start="2026-01-01",
        end="2026-08-27",
        freq="D",
    )

    rows = []

    for order_id in range(1, N_ORDERS + 1):
        date = rng.choice(dates)

        customer = customers.iloc[
            rng.integers(0, len(customers))
        ]

        product = products.iloc[
            rng.integers(0, len(products))
        ]

        quantity = int(
            rng.choice(
                [1, 1, 1, 2, 2, 3, 4],
            )
        )

        # Criamos uma queda artificial nas vendas
        # do Notebook Pro durante agosto.
        if (
            product["product_name"] == "Notebook Pro"
            and pd.Timestamp(date).month == 8
        ):
            if rng.random() < 0.65:
                continue

        status = rng.choice(
            ["completed", "completed", "completed", "cancelled"],
        )

        total_amount = float(
            product["price"] * quantity
        )

        rows.append(
            {
                "order_id": order_id,
                "customer_id": int(customer["customer_id"]),
                "customer_name": customer["customer_name"],
                "city": customer["city"],
                "state": customer["state"],
                "product_id": int(product["product_id"]),
                "product_name": product["product_name"],
                "category": product["category"],
                "quantity": quantity,
                "unit_price": float(product["price"]),
                "total_amount": total_amount,
                "order_date": pd.Timestamp(date).strftime(
                    "%Y-%m-%d"
                ),
                "status": status,
            }
        )

    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = generate_dataset()

    df.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    print(f"Dataset created: {OUTPUT_FILE}")
    print(f"Rows: {len(df)}")
    print()
    print(df.head())
