# Sales Analyst AI

AI-powered sales analytics agent built with **Python, SQL, SQLite and OpenAI API**.

The **Sales Analyst AI** is an end-to-end application that enables users to analyze sales data using natural language. The system combines data engineering, SQL analytics, anomaly detection and an AI agent to transform business questions into actionable insights.

## AI-Assisted Development

This project was developed with the assistance of **Generative AI tools** throughout the development process.

AI was used as a development aid for tasks such as:

* Code generation and refinement
* Debugging and troubleshooting
* Documentation
* Architecture and implementation discussions
* Test development and review

The project's architecture, implementation decisions, validation, testing and final integration were reviewed and adapted as part of the development process.

## Features

* Natural-language sales analysis
* Automated business KPIs
* Revenue and sales trend analysis
* Product, category and regional analysis
* Anomaly detection
* AI-generated business insights
* AI-generated SQL queries
* Read-only SQL validation and execution
* Automated data-quality validation
* Streamlit dashboard
* Automated tests with Pytest

## Architecture

```text
CSV Dataset
     ↓
Python / Pandas
     ↓
SQLite
     ↓
Analytics Layer
     ↓
AI Agent
     ↓
SQL Validation
     ↓
Business Insights
     ↓
Streamlit Dashboard
```

## Example Questions

The agent can answer questions such as:

```text
What was our total revenue?

Which product generated the most revenue?

Which state had the highest sales?

What was the revenue in August?

Which products had the biggest decrease in sales?

Why did revenue decrease compared to the previous month?
```

Instead of manually writing SQL queries, users interact with the database through natural language.

## SQL Security

AI-generated SQL queries are validated before execution.

The system only allows read operations such as:

```sql
SELECT ...
```

```sql
WITH ...
```

Write and database-modification operations such as `INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER` and `CREATE` are blocked.

Additional validation includes:

* Multiple-statement prevention
* Query length limits
* Result limits
* Read-only execution

This provides a controlled interface between the AI agent and the database.

## Data Quality

The dataset generation pipeline includes validation rules to ensure consistency between locations and their respective states.

The project also includes automated tests covering:

* Database queries
* Revenue calculations
* Sales metrics
* Anomaly detection
* SQL validation
* Read-only query restrictions

## Project Structure

```text
sales-analyst-ai/
│
├── app/
│   ├── agent/
│   │   ├── agent.py
│   │   ├── prompts.py
│   │   └── tools.py
│   │
│   ├── analytics/
│   │   ├── anomalies.py
│   │   └── metrics.py
│   │
│   └── database/
│       ├── connection.py
│       ├── create_dataset.py
│       ├── init_db.py
│       └── queries.py
│
├── data/
│   └── sales.csv
│
├── tests/
│   ├── test_analytics.py
│   └── test_database.py
│
├── streamlit_app.py
├── requirements.txt
├── .env.example
└── README.md
```

## Technologies

| Technology    | Purpose                                |
| ------------- | -------------------------------------- |
| Python        | Application and data processing        |
| Pandas        | Data processing and dataset generation |
| SQLite        | Relational database                    |
| SQL           | Data querying and analytics            |
| OpenAI API    | AI agent and natural-language analysis |
| Streamlit     | Web dashboard                          |
| Pytest        | Automated testing                      |
| python-dotenv | Environment configuration              |

## Getting Started

### Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd sales-analyst-ai
```

### Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure the API key

Create a `.env` file:

```bash
cp .env.example .env
```

Add your OpenAI API key:

```env
OPENAI_API_KEY=your_api_key_here
```

### Generate the dataset

```bash
python -m app.database.create_dataset
```

### Initialize the database

```bash
python -m app.database.init_db
```

### Run the application

```bash
streamlit run streamlit_app.py
```

### Run tests

```bash
pytest
```

## Project Status

**MVP / Active Development**

The project demonstrates an end-to-end architecture combining:

**Data Engineering + SQL + Analytics + AI Agents + Software Engineering + Automated Testing**

The current implementation uses SQLite as a lightweight database, with PostgreSQL and a FastAPI service planned for a future production-oriented architecture.

## Author

Focused on **Python, Data Analytics, SQL, AI Agents and Software Engineering**.

## License

This project is intended for educational and portfolio purposes.
