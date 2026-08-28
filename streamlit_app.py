import os

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from app.agent.agent import SalesAgent
from app.analytics.anomalies import (
    detect_revenue_anomalies,
)
from app.analytics.metrics import calculate_kpis
from app.database.queries import (
    get_revenue_by_month,
    get_sales_by_product,
    get_sales_by_region,
)


load_dotenv()


# ==================================================
# CONFIG
# ==================================================

st.set_page_config(
    page_title="Sales Analyst AI",
    page_icon="📊",
    layout="wide",
)


# ==================================================
# HEADER
# ==================================================

st.title("📊 Sales Analyst AI")

st.caption(
    "AI-powered sales analysis using Python, SQL and Gemini."
)


# ==================================================
# KPIs
# ==================================================

kpis = calculate_kpis()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Revenue",
        f"R$ {kpis['revenue']:,.2f}",
    )

with col2:
    st.metric(
        "Orders",
        f"{kpis['orders']:,}",
    )

with col3:
    st.metric(
        "Average Ticket",
        f"R$ {kpis['average_ticket']:,.2f}",
    )


st.divider()


# ==================================================
# REVENUE CHART
# ==================================================

st.subheader("📈 Revenue over time")

monthly = pd.DataFrame(
    get_revenue_by_month()
)

if not monthly.empty:

    monthly = monthly.set_index("month")

    st.line_chart(
        monthly["revenue"]
    )

else:

    st.info(
        "No monthly revenue data available."
    )


# ==================================================
# PRODUCT / REGION
# ==================================================

col1, col2 = st.columns(2)


with col1:

    st.subheader("🛒 Sales by product")

    products = pd.DataFrame(
        get_sales_by_product()
    )

    if not products.empty:

        st.dataframe(
            products,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info(
            "No product data available."
        )


with col2:

    st.subheader("🌎 Sales by region")

    regions = pd.DataFrame(
        get_sales_by_region()
    )

    if not regions.empty:

        st.dataframe(
            regions,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info(
            "No regional data available."
        )


# ==================================================
# ANOMALIES
# ==================================================

st.divider()

st.subheader("🚨 Detected anomalies")

anomalies = detect_revenue_anomalies()

if anomalies:

    for anomaly in anomalies:

        variation = anomaly["variation"]

        if variation < 0:

            st.warning(
                f"Revenue decreased "
                f"{abs(variation):.2f}% "
                f"from {anomaly['previous_month']} "
                f"to {anomaly['month']}."
            )

        else:

            st.success(
                f"Revenue increased "
                f"{variation:.2f}% "
                f"from {anomaly['previous_month']} "
                f"to {anomaly['month']}."
            )

else:

    st.success(
        "No significant revenue anomalies detected."
    )


# ==================================================
# AI ANALYST
# ==================================================

st.divider()

st.subheader("🤖 Ask Sales Analyst")

st.write(
    "Ask questions about your sales data. "
    "The AI will generate SQL, query the database "
    "and explain the results."
)


question = st.text_area(
    "Your question:",
    placeholder=(
        "Examples:\n"
        "• Which product generated the most revenue?\n"
        "• Why did revenue decrease?\n"
        "• Which region has the best sales?\n"
        "• What were the top 5 products?"
    ),
    height=120,
)


if st.button(
    "🔍 Analyze",
    type="primary",
):

    if not question.strip():

        st.warning(
            "Please enter a question."
        )

    elif not os.getenv("GEMINI_API_KEY"):

        st.error(
            "GEMINI_API_KEY is not configured. "
            "Check your .env file."
        )

    else:

        with st.spinner(
            "🤖 Analyzing sales data..."
        ):

            try:

                agent = SalesAgent()

                result = agent.analyze(
                    question
                )

                # ----------------------------------
                # AI RESPONSE
                # ----------------------------------

                st.subheader(
                    "💡 Analysis"
                )

                st.markdown(
                    result["answer"]
                )

                # ----------------------------------
                # SQL
                # ----------------------------------

                with st.expander(
                    "🔎 View generated SQL"
                ):

                    st.code(
                        result["sql"],
                        language="sql",
                    )

                # ----------------------------------
                # RAW RESULTS
                # ----------------------------------

                with st.expander(
                    "📊 View query results"
                ):

                    results = result["results"]

                    if results:

                        st.dataframe(
                            pd.DataFrame(results),
                            use_container_width=True,
                            hide_index=True,
                        )

                    else:

                        st.info(
                            "The query returned no results."
                        )

            except Exception as error:

                st.error(
                    "Error while running the agent."
                )

                st.exception(error)