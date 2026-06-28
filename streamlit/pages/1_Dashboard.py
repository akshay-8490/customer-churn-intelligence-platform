"""
Executive Dashboard

Project: Customer Churn Intelligence Platform

Provides an executive overview of customer churn,
revenue risk, customer portfolio, and retention strategy.
"""

# ==========================================================
# Imports
# ==========================================================

import utils.path_setup  # noqa: F401  — configure sys.path

import streamlit as st

from components.sidebar import render_sidebar
from components.cards import render_info_card
from components.plots import (
    donut_chart,
    bar_chart,
    horizontal_bar_chart,
)

from utils.data_loader import load_dashboard_dataset
from utils.model_loader import load_model_metadata
from utils.dashboard_metrics import (
    get_executive_metrics,
    get_business_metrics,
    get_risk_distribution,
    get_persona_distribution,
    get_revenue_by_risk,
    get_monthly_charge_distribution,
    get_retention_summary,
    get_priority_customers,
)
from components.footer import render_footer

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Executive Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Executive Dashboard")
st.caption(
    "Real-time executive overview of customer churn, "
    "revenue risk, and customer portfolio."
)

st.divider()


# ==========================================================
# Load Data
# ==========================================================

try:

    dashboard_df = load_dashboard_dataset()

    metadata = load_model_metadata()

except Exception as e:

    st.error(f"Unable to load dashboard resources.\n\n{e}")

    st.stop()


# ==========================================================
# Sidebar
# ==========================================================

render_sidebar(metadata)


# ==========================================================
# Dashboard Filters
# ==========================================================

st.subheader("Dashboard Filters")

filter_col1, filter_col2, filter_col3 = st.columns(3)

with filter_col1:

    risk_options = [
        "All"
    ] + sorted(
        dashboard_df["Risk_Segment"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_risk = st.selectbox(
        "Risk Segment",
        risk_options,
    )


with filter_col2:

    contract_options = [
        "All"
    ] + sorted(
        dashboard_df["Contract"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_contract = st.selectbox(
        "Contract",
        contract_options,
    )


with filter_col3:

    internet_options = [
        "All"
    ] + sorted(
        dashboard_df["InternetService"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_internet = st.selectbox(
        "Internet Service",
        internet_options,
    )


# ==========================================================
# Apply Filters
# ==========================================================

filtered_df = dashboard_df.copy()

if selected_risk != "All":

    filtered_df = filtered_df[
        filtered_df["Risk_Segment"] == selected_risk
    ]


if selected_contract != "All":

    filtered_df = filtered_df[
        filtered_df["Contract"] == selected_contract
    ]


if selected_internet != "All":

    filtered_df = filtered_df[
        filtered_df["InternetService"] == selected_internet
    ]


st.divider()

# ==========================================================
# Dashboard Metrics
# ==========================================================

executive_metrics = get_executive_metrics(filtered_df)

business_metrics = get_business_metrics(filtered_df)


# ==========================================================
# Executive KPIs
# ==========================================================

st.subheader("Executive Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    render_info_card(
        title="Total Customers",
        value=f"{executive_metrics['total_customers']:,}"
    )

with col2:
    render_info_card(
        title="Churn Rate",
        value=f"{executive_metrics['churn_rate']:.2f}%"
    )

with col3:
    render_info_card(
        title="Avg Churn Probability",
        value=f"{executive_metrics['avg_probability']:.2f}%"
    )

with col4:
    render_info_card(
        title="High Risk Customers",
        value=f"{executive_metrics['high_risk_customers']:,}"
    )


st.markdown("<br>", unsafe_allow_html=True)


# ==========================================================
# Business KPIs
# ==========================================================

st.subheader("Business Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    render_info_card(
        title="Monthly Revenue",
        value=f"${business_metrics['monthly_revenue']:,.2f}"
    )

with col2:
    render_info_card(
        title="Revenue at Risk",
        value=f"${business_metrics['revenue_at_risk']:,.2f}"
    )

with col3:
    render_info_card(
        title="Average Tenure",
        value=f"{business_metrics['average_tenure']:.1f} Months"
    )

with col4:
    render_info_card(
        title="Retention Budget",
        value=f"${business_metrics['retention_budget']:,.2f}"
    )


st.divider()

# ==========================================================
# Portfolio Overview
# ==========================================================

st.subheader("Customer Portfolio")

risk_df = get_risk_distribution(filtered_df)

persona_df = get_persona_distribution(filtered_df)

left_col, right_col = st.columns(2)

with left_col:

    risk_fig = donut_chart(
        df=risk_df,
        names="Risk_Segment",
        values="Customers",
        title="Risk Segment Distribution"
    )

    st.plotly_chart(
        risk_fig,
        width="stretch",
        key="risk_distribution_chart"
    )

with right_col:

    persona_fig = bar_chart(
        df=persona_df,
        x="Persona",
        y="Customers",
        title="Customer Personas"
    )

    st.plotly_chart(
        persona_fig,
        width="stretch",
        key="persona_distribution_chart"
    )


st.divider()


# ==========================================================
# Revenue Insights
# ==========================================================

st.subheader("Revenue Insights")

revenue_df = get_revenue_by_risk(filtered_df)

monthly_charge_df = get_monthly_charge_distribution(filtered_df)

left_col, right_col = st.columns(2)

with left_col:

    revenue_fig = bar_chart(
        df=revenue_df,
        x="Risk_Segment",
        y="Revenue",
        title="Revenue by Risk Segment"
    )

    st.plotly_chart(
        revenue_fig,
        width="stretch",
        key="revenue_by_risk_chart"
    )

with right_col:

    monthly_charge_fig = bar_chart(
        df=monthly_charge_df,
        x="Risk_Segment",
        y="Average_Monthly_Charge",
        title="Average Monthly Charges"
    )

    st.plotly_chart(
        monthly_charge_fig,
        width="stretch",
        key="monthly_charge_chart"
    )


st.divider()


# ==========================================================
# Customer Portfolio Summary
# ==========================================================

summary_col1, summary_col2, summary_col3 = st.columns(3)

with summary_col1:

    st.metric(
        label="Highest Risk Segment",
        value=risk_df.iloc[
            risk_df["Customers"].idxmax()
        ]["Risk_Segment"]
    )

with summary_col2:

    st.metric(
        label="Largest Customer Persona",
        value=persona_df.iloc[
            persona_df["Customers"].idxmax()
        ]["Persona"]
    )

with summary_col3:

    highest_revenue_segment = revenue_df.loc[
        revenue_df["Revenue"].idxmax(),
        "Risk_Segment"
    ]

    st.metric(
        label="Highest Revenue Segment",
        value=highest_revenue_segment
    )


st.divider()

# ==========================================================
# Retention Strategy
# ==========================================================

st.subheader("Retention Strategy")

retention_df = get_retention_summary(filtered_df)

# Interactive Chart
retention_fig = horizontal_bar_chart(
    df=retention_df,
    x="Customers",
    y="Retention_Action",
    title="Retention Actions by Customer Count"
)

st.plotly_chart(
    retention_fig,
    width="stretch",
    key="retention_action_chart"
)

# Detailed Table
st.dataframe(
    retention_df,
    width="stretch",
    hide_index=True,
    column_config={

        "Retention_Action": st.column_config.TextColumn(
            "Retention Strategy",
            width="large",
        ),

        "Customers": st.column_config.NumberColumn(
            "Customers",
            format="%d",
        ),

        "Estimated_Cost": st.column_config.NumberColumn(
            "Estimated Cost ($)",
            format="$%.2f",
        ),
    },
)

st.divider()


# ==========================================================
# High Priority Customers
# ==========================================================

st.subheader("High Priority Customers")

priority_df = get_priority_customers(
    filtered_df,
    top_n=20,
)

st.dataframe(
    priority_df,
    width="stretch",
    hide_index=True,
    column_config={

        "CustomerID": st.column_config.TextColumn(
            "Customer ID",
            width="medium",
        ),

        "Risk_Segment": st.column_config.TextColumn(
            "Risk Segment",
            width="small",
        ),

        "Churn_Probability": st.column_config.ProgressColumn(
            "Churn Probability",
            format="%.2f%%",
            min_value=0.0,
            max_value=100.0,
        ),

        "Priority_Score": st.column_config.NumberColumn(
            "Priority Score",
            format="%.2f",
        ),

        "Persona": st.column_config.TextColumn(
            "Customer Persona",
            width="medium",
        ),

        "Retention_Action": st.column_config.TextColumn(
            "Recommended Action",
            width="large",
        ),
    },
)


st.divider()


# ==========================================================
# Download Filtered Dataset
# ==========================================================

st.subheader("Export")

csv = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Dataset",
    data=csv,
    file_name="filtered_dashboard_dataset.csv",
    mime="text/csv",
)


st.divider()


# ==========================================================
# Dashboard Footer
# ==========================================================

render_footer("Executive Dashboard")