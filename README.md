Claro. Fiz um README com uma pegada **profissional, mas sem exagerar**, adequado para colocar diretamente no GitHub. Ele apresenta o projeto, arquitetura, funcionalidades, instalação, testes e roadmap.

# 🤖 Sales Analyst AI

> AI-powered sales analytics agent built with Python, SQL, SQLite and the OpenAI API.

**Sales Analyst AI** is an application that allows users to analyze sales data using natural language. The system combines traditional data analytics with an AI agent capable of querying a relational database, identifying patterns and anomalies, and generating business-oriented insights.

The project was designed as an MVP with a focus on **Python, SQL, data quality, automated testing and agentic AI**.

---

## 🎯 Project Goal

The goal is to build an AI assistant capable of answering questions such as:

* "What was our total revenue?"
* "Which product generated the most revenue?"
* "Which state had the highest sales?"
* "Which products had the biggest drop in sales?"
* "Why did revenue decrease this month?"
* "What anomalies can be found in the sales data?"

Instead of manually writing SQL queries, users can interact with the system using natural language.

---

## 🏗️ Architecture

```text
                    ┌──────────────────┐
                    │   Sales Dataset  │
                    │      CSV         │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   Python ETL     │
                    │     Pandas       │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │      SQLite      │
                    │   Sales Database │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   Analytics      │
                    │                  │
                    │ KPIs / Anomalies │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │    AI Agent      │
                    │   OpenAI API     │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │    Streamlit     │
                    │    Dashboard     │
                    └──────────────────┘
```

---

## ✨ Features

### 📊 Sales Analytics

The application calculates important business metrics:

* Total revenue
* Number of orders
* Average ticket
* Revenue over time
* Sales by product
* Sales by category
* Sales by region

### 🚨 Anomaly Detection

The analytics layer automatically searches for unusual behavior in sales data.

Examples:

* Significant revenue changes
* Unusual product performance
* Regional sales variations

### 🤖 AI Sales Agent

Users can ask questions using natural language.

Example:

```text
Why did sales decrease in August?
```

The agent can:

1. Understand the question
2. Determine which data is necessary
3. Query the database
4. Analyze the results
5. Generate a business-oriented response

### 🔒 Read-Only SQL

The AI-generated SQL is validated before execution.

Only read operations are allowed.

Allowed:

```sql
SELECT ...
```

```sql
WITH ...
```

Blocked operations include:

```sql
INSERT
UPDATE
DELETE
DROP
ALTER
CREATE
TRUNCATE
```

Queries are also protected with a maximum result limit.

---

## 🗂️ Project Structure

```text
sales-analyst-ai/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   ├── prompts.py
│   │   └── tools.py
│   │
│   ├── analytics/
│   │   ├── __init__.py
│   │   ├── anomalies.py
│   │   └── metrics.py
│   │
│   └── database/
│       ├── __init__.py
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
├── .env.example
├── .gitignore
├── pytest.ini
├── requirements.txt
├── streamlit_app.py
└── README.md
```

---

## 🛠️ Technologies

| Technology    | Purpose                        |
| ------------- | ------------------------------ |
| Python        | Main programming language      |
| Pandas        | Data generation and processing |
| SQLite        | Relational database            |
| SQL           | Data querying and analytics    |
| OpenAI API    | AI agent                       |
| Streamlit     | Web interface                  |
| Pytest        | Automated testing              |
| python-dotenv | Environment configuration      |

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd sales-analyst-ai
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file:

```bash
cp .env.example .env
```

Add your OpenAI API key:

```env
OPENAI_API_KEY=your_api_key_here
```

Do not commit `.env` to Git.

The repository includes `.env.example` as a template.

---

## 🗄️ Create the Dataset

Generate the sales dataset:

```bash
python -m app.database.create_dataset
```

This creates:

```text
data/sales.csv
```

The current dataset contains approximately **5,000 sales records**.

The generated data includes:

* Customers
* Cities
* States
* Products
* Categories
* Quantities
* Prices
* Order dates
* Order status

The dataset generator also validates the relationship between cities and states.

---

## 💾 Initialize the Database

After generating the dataset:

```bash
python -m app.database.init_db
```

This creates the SQLite database used by the application.

---

## ▶️ Run the Application

### CLI

Run the basic analytics:

```bash
python -m app.main
```

Example:

```text
Sales Analyst AI
================
Revenue: R$ 10,296,120.00
Orders: 3,724
Average ticket: R$ 2,764.80

Anomalies detected: 1
```

### Streamlit

Start the dashboard:

```bash
streamlit run streamlit_app.py
```

Then open the URL provided by Streamlit in your browser.

---

## 🧪 Running Tests

The project uses `pytest`.

Run:

```bash
pytest
```

Current test suite:

```text
14 passed
```

The tests cover:

* Database queries
* Revenue calculations
* Sales metrics
* Anomaly detection
* SQL validation
* Read-only query restrictions

---

## 🔒 SQL Security

Because the AI agent can generate SQL queries, the project does not execute arbitrary SQL directly.

Queries pass through a validation layer before reaching SQLite.

The validation checks:

* Query type
* Forbidden SQL operations
* Multiple statements
* Query length
* Result limits

For example:

```sql
SELECT *
FROM sales
LIMIT 10;
```

is allowed.

But:

```sql
DELETE FROM sales;
```

is rejected.

This creates a controlled interface between the LLM and the database.

---

## 📈 Example Questions

The agent is designed to answer questions such as:

```text
What is our total revenue?
```

```text
Which product generated the most revenue?
```

```text
Which state has the highest number of orders?
```

```text
What was the revenue in August?
```

```text
Which products had the biggest decrease in sales?
```

```text
Why did revenue decrease compared to the previous month?
```

The objective is not only to return raw numbers, but to transform them into useful business insights.

---

## 🧠 Agent Workflow

A typical question follows this flow:

```text
User question
      │
      ▼
   AI Agent
      │
      ▼
Determine required data
      │
      ▼
Generate SQL
      │
      ▼
SQL validation
      │
      ▼
SQLite
      │
      ▼
Query results
      │
      ▼
AI analysis
      │
      ▼
Business insight
```

This architecture separates the responsibilities of:

* Data storage
* SQL querying
* Data analytics
* Security
* AI reasoning
* User interface

---

## 🧪 Data Quality

The dataset generator enforces basic consistency rules.

For example:

```text
São Paulo       → SP
Rio de Janeiro  → RJ
Niterói         → RJ
Curitiba        → PR
Salvador        → BA
Recife          → PE
Fortaleza       → CE
Brasília        → DF
```

This prevents inconsistent location data from entering the analytics layer.

Future versions will expand automated data-quality validation.


## 🎯 Future Architecture

The MVP currently uses SQLite for simplicity:

```text
CSV
 ↓
Python
 ↓
SQLite
 ↓
AI Agent
 ↓
Streamlit
```

The planned production-oriented architecture is:

```text
CSV / External Data
        ↓
      ETL
        ↓
   PostgreSQL
        ↓
   Analytics Layer
        ↓
     AI Agent
        ↓
     FastAPI
        ↓
    Streamlit
        ↓
      Users
```

---

## 📌 Project Status

**Status:** MVP / Active Development

The current version demonstrates an end-to-end pipeline combining:

**Data Engineering + SQL + Analytics + AI Agent + Automated Testing**

The project is intentionally being developed incrementally, adding complexity only when it provides a clear technical or business benefit.

---

## 👨‍💻 Author

Developed as a portfolio project focused on:

* Python
* Data Analytics
* SQL
* AI Agents
* Software Engineering
* Automated Testing

---

## 📄 License

This project is intended for educational and portfolio purposes.
