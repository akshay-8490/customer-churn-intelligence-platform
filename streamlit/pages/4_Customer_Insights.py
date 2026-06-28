"""
Customer Insights Page

Provides interactive customer segmentation, demographic analysis,
service adoption trends, and churn insights.
"""

# ==========================================================
# Imports
# ==========================================================

import utils.path_setup  # noqa: F401  — configure sys.path

import streamlit as st

from config import APP_TITLE

from components.sidebar import render_sidebar
from components.footer import render_footer
from components.plots import (
    donut_chart,
    bar_chart,
    histogram_chart,
)
from utils.data_loader import load_dashboard_dataset
from utils.model_loader import load_model_metadata


# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title=f"{APP_TITLE} | Customer Insights",
    page_icon="👥",
    layout="wide",
)


# ==========================================================
# Load Resources
# ==========================================================

try:

    metadata = load_model_metadata()
    df = load_dashboard_dataset()

except Exception as e:

    st.error(f"Unable to load resources.\n\n{e}")

    st.stop()

render_sidebar(metadata)

# ==========================================================
# Header
# ==========================================================

st.title("👥 Customer Insights")

st.markdown(
    """
Explore customer demographics, service adoption, billing patterns,
and churn behavior through interactive business analytics.
"""
)

st.divider()

# ==========================================================
# Interactive Filters
# ==========================================================

st.subheader("Interactive Filters")

filter_col1, filter_col2, filter_col3 = st.columns(3)

with filter_col1:

    gender = st.multiselect(
        "Gender",
        sorted(df["gender"].unique()),
        default=sorted(df["gender"].unique())
    )

    contract = st.multiselect(
        "Contract",
        sorted(df["Contract"].unique()),
        default=sorted(df["Contract"].unique())
    )

with filter_col2:

    internet = st.multiselect(
        "Internet Service",
        sorted(df["InternetService"].unique()),
        default=sorted(df["InternetService"].unique())
    )

    payment = st.multiselect(
        "Payment Method",
        sorted(df["PaymentMethod"].unique()),
        default=sorted(df["PaymentMethod"].unique())
    )

with filter_col3:

    senior = st.multiselect(
        "Senior Citizen",
        sorted(df["SeniorCitizen"].unique()),
        default=sorted(df["SeniorCitizen"].unique())
    )

# ==========================================================
# Filter Dataset
# ==========================================================

filtered_df = df[
    (df["gender"].isin(gender))
    & (df["Contract"].isin(contract))
    & (df["InternetService"].isin(internet))
    & (df["PaymentMethod"].isin(payment))
    & (df["SeniorCitizen"].isin(senior))
]

st.caption(f"Showing **{len(filtered_df):,}** customers after filtering.")

st.divider()

# ==========================================================
# Customer Portfolio
# ==========================================================

st.subheader("Customer Portfolio")

total_customers = len(filtered_df)

avg_tenure = filtered_df["tenure"].mean()

avg_monthly = filtered_df["MonthlyCharges"].mean()

churn_rate = (
    filtered_df["Churn"]
    .eq("Yes")
    .mean()
    * 100
)

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric(
    "Total Customers",
    f"{total_customers:,}"
)

kpi2.metric(
    "Average Tenure",
    f"{avg_tenure:.1f} months"
)

kpi3.metric(
    "Average Monthly Charges",
    f"${avg_monthly:.2f}"
)

kpi4.metric(
    "Churn Rate",
    f"{churn_rate:.1f}%"
)

st.divider()

# ==========================================================
# Customer Demographics
# ==========================================================

st.subheader("Customer Demographics")

col1, col2 = st.columns(2)

with col1:

    gender_counts = (
        filtered_df["gender"]
        .value_counts()
        .reset_index()
    )

    gender_counts.columns = ["Gender", "Count"]

    gender_fig = donut_chart(
        gender_counts,
        names="Gender",
        values="Count",
        title="Gender Distribution"
    )

    st.plotly_chart(
        gender_fig,
        width="stretch",
        key="gender_distribution_chart"
    )

with col2:

    senior_counts = (
        filtered_df["SeniorCitizen"]
        .replace({0: "No", 1: "Yes"})
        .value_counts()
        .reset_index()
    )

    senior_counts.columns = ["Senior Citizen", "Count"]

    senior_fig = donut_chart(
        senior_counts,
        names="Senior Citizen",
        values="Count",
        title="Senior Citizen Distribution"
    )

    st.plotly_chart(
        senior_fig,
        width="stretch",
        key="senior_citizen_chart"
    )

st.divider()

# ==========================================================
# Service Adoption
# ==========================================================

st.subheader("Service Adoption")

col1, col2 = st.columns(2)

with col1:

    internet_counts = (
        filtered_df["InternetService"]
        .value_counts()
        .reset_index()
    )

    internet_counts.columns = ["Internet Service", "Customers"]

    internet_fig = bar_chart(
        internet_counts,
        x="Internet Service",
        y="Customers",
        title="Internet Service Adoption"
    )

    st.plotly_chart(
        internet_fig,
        width="stretch",
        key="internet_service_chart"
    )

with col2:

    security_counts = (
        filtered_df["OnlineSecurity"]
        .value_counts()
        .reset_index()
    )

    security_counts.columns = ["Online Security", "Customers"]

    security_fig = bar_chart(
        security_counts,
        x="Online Security",
        y="Customers",
        title="Online Security Adoption"
    )

    st.plotly_chart(
        security_fig,
        width="stretch",
        key="online_security_chart"
    )

col3, col4 = st.columns(2)

with col3:

    phone_counts = (
        filtered_df["PhoneService"]
        .value_counts()
        .reset_index()
    )

    phone_counts.columns = ["Phone Service", "Customers"]

    phone_fig = bar_chart(
        phone_counts,
        x="Phone Service",
        y="Customers",
        title="Phone Service Adoption"
    )

    st.plotly_chart(
        phone_fig,
        width="stretch",
        key="phone_service_chart"
    )

with col4:

    streaming_counts = (
        filtered_df["StreamingTV"]
        .value_counts()
        .reset_index()
    )

    streaming_counts.columns = ["Streaming TV", "Customers"]

    streaming_fig = bar_chart(
        streaming_counts,
        x="Streaming TV",
        y="Customers",
        title="Streaming TV Adoption"
    )

    st.plotly_chart(
        streaming_fig,
        width="stretch",
        key="streaming_tv_chart"
    )

st.divider()

# ==========================================================
# Contract & Billing Analysis
# ==========================================================

st.subheader("Contract & Billing")

col1, col2, col3 = st.columns(3)

with col1:

    contract_counts = (
        filtered_df["Contract"]
        .value_counts()
        .reset_index()
    )

    contract_counts.columns = ["Contract", "Customers"]

    contract_fig = bar_chart(
        contract_counts,
        x="Contract",
        y="Customers",
        title="Contract Type Distribution"
    )

    st.plotly_chart(
        contract_fig,
        width="stretch",
        key="contract_type_chart"
    )

with col2:

    payment_counts = (
        filtered_df["PaymentMethod"]
        .value_counts()
        .reset_index()
    )

    payment_counts.columns = ["Payment Method", "Customers"]

    payment_fig = bar_chart(
        payment_counts,
        x="Payment Method",
        y="Customers",
        title="Payment Method Distribution"
    )

    st.plotly_chart(
        payment_fig,
        width="stretch",
        key="payment_method_chart"
    )

with col3:

    billing_counts = (
        filtered_df["PaperlessBilling"]
        .value_counts()
        .reset_index()
    )

    billing_counts.columns = ["Paperless Billing", "Customers"]

    billing_fig = bar_chart(
        billing_counts,
        x="Paperless Billing",
        y="Customers",
        title="Paperless Billing Distribution"
    )

    st.plotly_chart(
        billing_fig,
        width="stretch",
        key="paperless_billing_chart"
    )

st.divider()

# ==========================================================
# Revenue & Tenure
# ==========================================================

st.subheader("Revenue & Tenure")

col1, col2 = st.columns(2)

with col1:

    tenure_fig = histogram_chart(
        filtered_df,
        x="tenure",
        title="Customer Tenure Distribution"
    )

    st.plotly_chart(
        tenure_fig,
        width="stretch",
        key="tenure_distribution_chart"
    )

with col2:

    monthly_fig = histogram_chart(
        filtered_df,
        x="MonthlyCharges",
        title="Monthly Charges Distribution"
    )

    st.plotly_chart(
        monthly_fig,
        width="stretch",
        key="monthly_charges_chart"
    )

revenue = (
    filtered_df
    .groupby("Contract", as_index=False)["TotalCharges"]
    .sum()
)

revenue_fig = bar_chart(
    revenue,
    x="Contract",
    y="TotalCharges",
    title="Total Revenue by Contract Type"
)

st.plotly_chart(
    revenue_fig,
    width="stretch",
    key="revenue_by_contract_chart"
)

st.divider()

# ==========================================================
# High-Risk Customer Segments
# ==========================================================

st.subheader("High-Risk Customer Segments")

segment_summary = (
    filtered_df
    .groupby(
        ["Contract", "InternetService"],
        as_index=False
    )
    .agg(
        Customers=("Churn", "count"),
        ChurnRate=("Churn", lambda x: (x == "Yes").mean() * 100)
    )
    .sort_values(
        by="ChurnRate",
        ascending=False
    )
)

segment_summary["ChurnRate"] = (
    segment_summary["ChurnRate"]
    .round(1)
)

st.dataframe(
    segment_summary,
    width="stretch"
)

st.divider()

# ==========================================================
# Download Filtered Dataset
# ==========================================================

st.subheader("Export Data")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Dataset",
    data=csv,
    file_name="customer_insights.csv",
    mime="text/csv"
)


# ==========================================================
# Footer
# ==========================================================

render_footer("Customer Insights")