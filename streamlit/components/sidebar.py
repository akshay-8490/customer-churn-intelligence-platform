"""
Sidebar Component
Project: Customer Churn Intelligence Platform

Reusable sidebar displayed across all Streamlit pages.
"""

import streamlit as st

from config import (
    APP_TITLE,
    DATASET_NAME,
    ORGANIZATION,
    COPYRIGHT,
)


# ==========================================================
# Sidebar
# ==========================================================

def render_sidebar(metadata: dict):
    """
    Render the common sidebar for the application.
    """

    st.sidebar.title("📊 Customer Churn")
    st.sidebar.caption(APP_TITLE)
    st.sidebar.divider()
    st.sidebar.subheader("Model Information")
    st.sidebar.write(
        f"**Model:** {metadata.get('model_name', 'Unknown')}"
    )
    st.sidebar.write(
        f"**ROC-AUC:** {metadata.get('roc_auc', 0.0):.3f}"
    )
    st.sidebar.write(
        f"**CV Score:** {metadata.get('cv_score', 0.0):.3f}"
    )
    st.sidebar.write(
        f"**Threshold:** {metadata.get('threshold', 0.0):.2f}"
    )
    st.sidebar.divider()
    st.sidebar.subheader("Dataset")
    st.sidebar.write(DATASET_NAME)
    st.sidebar.divider()
    st.sidebar.subheader("Navigation")
    st.sidebar.info(
        "Use the Pages menu above to explore different modules of the platform."
    )
    st.sidebar.divider()
    st.sidebar.subheader("About")
    st.sidebar.write(ORGANIZATION)
    st.sidebar.caption(COPYRIGHT)