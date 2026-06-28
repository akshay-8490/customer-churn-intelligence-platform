"""
Customer Churn Intelligence Platform
Main Streamlit Application
"""

import utils.path_setup  # noqa: F401  — configure sys.path

import streamlit as st

from config import (
    APP_TITLE,
    APP_ICON,
    LAYOUT,
    SIDEBAR_STATE,
    FOOTER_TEXT,
    MODEL_DISPLAY_NAME,
)

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout=LAYOUT,
    initial_sidebar_state=SIDEBAR_STATE,
)

# ==========================================================
# Session State Initialization
# ==========================================================

if "app_initialized" not in st.session_state:
    st.session_state.app_initialized = True

# ==========================================================
# Header
# ==========================================================

st.title("📊 Customer Churn Intelligence Platform")

st.markdown(
    """
An end-to-end Machine Learning and Business Intelligence platform
for customer churn prediction, explainability, revenue analysis,
and retention strategy.

Use the navigation menu on the left to explore the application.
"""
)

# ==========================================================
# Project Overview
# ==========================================================

st.subheader("Project Modules")

col1, col2 = st.columns(2)

with col1:

    st.success("✅ Customer Churn Prediction")
    st.success("✅ Executive Dashboard")
    st.success("✅ Explainable AI (SHAP)")

with col2:

    st.success("✅ Customer Insights")
    st.success("✅ Business Recommendations")
    st.success("✅ Revenue Risk Analysis")

# ==========================================================
# Model Information
# ==========================================================

st.info(f"Current Prediction Model : **{MODEL_DISPLAY_NAME}**")

# ==========================================================
# Instructions
# ==========================================================

st.subheader("Getting Started")

st.markdown(
    """
1. Open **Dashboard** to view business KPIs.
2. Use **Predict Churn** to estimate churn probability.
3. Explore **Model Explainability** to understand model decisions.
4. Review **Customer Insights** for portfolio analysis.
5. Visit **Business Recommendations** for actionable strategies.
"""
)

# ==========================================================
# Footer
# ==========================================================

st.divider()
st.caption(FOOTER_TEXT)