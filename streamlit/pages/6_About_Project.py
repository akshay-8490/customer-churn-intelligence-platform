"""
About Project Page

Provides an overview of the Customer Churn Intelligence Platform,
its architecture, technology stack, workflow, and future roadmap.
"""

# ==========================================================
# Imports
# ==========================================================

import utils.path_setup  # noqa: F401  — configure sys.path

import streamlit as st

from config import (
    APP_TITLE,
    DATASET_NAME,
    ORGANIZATION,
    VERSION,
)

from components.footer import render_footer
from components.sidebar import render_sidebar

from utils.model_loader import load_model_metadata


# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title=f"{APP_TITLE} | About Project",
    page_icon="ℹ️",
    layout="wide",
)


# ==========================================================
# Load Resources
# ==========================================================

try:

    metadata = load_model_metadata()

except Exception as e:

    st.error(f"Unable to load model metadata.\n\n{e}")

    st.stop()

render_sidebar(metadata)

# ==========================================================
# Header
# ==========================================================

st.title("ℹ️ About Project")

st.markdown(
    """
Learn about the Customer Churn Intelligence Platform, including its
architecture, machine learning workflow, technology stack, and business
impact.
"""
)

st.divider()

# ==========================================================
# Project Overview
# ==========================================================

st.subheader("Project Overview")

st.markdown(
    """
The **Customer Churn Intelligence Platform** is an end-to-end machine
learning and business intelligence solution designed to predict customer
churn, explain model decisions, and support proactive customer retention.

The platform combines predictive analytics, explainable AI,
interactive dashboards, and executive reporting into a unified
decision-support application that enables organizations to identify
at-risk customers and implement targeted retention strategies.
"""
)

st.divider()

# ==========================================================
# Platform Architecture
# ==========================================================

st.subheader("Platform Architecture")

st.markdown(
    """
The Customer Churn Intelligence Platform follows a complete end-to-end
machine learning pipeline, transforming raw customer data into actionable
business intelligence and executive decision support.
"""
)


def pipeline_arrow():
    """Display a centered arrow between pipeline stages."""
    st.markdown(
        "<div style='text-align:center; font-size:28px;'>⬇️</div>",
        unsafe_allow_html=True,
    )


st.success(
    """
### 📥 Raw Customer Data

Customer information is collected from the IBM Telco Customer Churn dataset
and serves as the foundation for all analytics and machine learning tasks.
"""
)

pipeline_arrow()

st.info(
    """
### 🧹 Data Cleaning

Missing values are handled, data types are corrected, and the dataset is
prepared for reliable downstream analysis.
"""
)

pipeline_arrow()

st.info(
    """
### ⚙️ Feature Engineering

Business-driven features are created and variables are transformed to
improve predictive performance and interpretability.
"""
)

pipeline_arrow()

st.warning(
    """
### 🤖 Machine Learning Model

A Logistic Regression model is trained to estimate the probability of
customer churn using engineered customer features.
"""
)

pipeline_arrow()

st.info(
    """
### 📈 Model Evaluation

Model performance is validated using ROC-AUC, Precision, Recall,
F1-Score, Confusion Matrix, and other evaluation metrics.
"""
)

pipeline_arrow()

st.success(
    """
### 🔍 Model Explainability

Feature Importance and SHAP analysis provide transparent explanations for
model predictions, improving trust and interpretability.
"""
)

pipeline_arrow()

st.warning(
    """
### 📊 Business Intelligence

Predictive insights are transformed into executive dashboards, customer
analytics, and actionable business recommendations.
"""
)

pipeline_arrow()

st.success(
    """
### 🌐 Interactive Streamlit Platform

All analytical components are integrated into a production-style web
application that enables interactive exploration, prediction, and
decision support.
"""
)

st.divider()

# ==========================================================
# Technology Stack
# ==========================================================

st.subheader("Technology Stack")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.info(
        """
### 💻 Programming

- Python
- Pandas
- NumPy
"""
    )

with col2:

    st.success(
        """
### 🤖 Machine Learning

- Scikit-learn
- Logistic Regression
- SHAP
"""
    )

with col3:

    st.warning(
        """
### 📊 Visualization

- Plotly
- Matplotlib
- Streamlit
"""
    )

with col4:

    st.info(
        """
### ⚙️ Development

- Jupyter Notebook
- Power BI
- Joblib
"""
    )

st.divider()

# ==========================================================
# Machine Learning Workflow
# ==========================================================

st.subheader("Machine Learning Workflow")

workflow = [
    "Business Understanding",
    "Dataset Exploration",
    "Data Cleaning",
    "Feature Engineering",
    "Model Training",
    "Model Evaluation",
    "Model Explainability",
    "Business Intelligence",
    "Streamlit Deployment",
]

for step in workflow:
    st.checkbox(step, value=True, disabled=True)

st.divider()

# ==========================================================
# Project Highlights
# ==========================================================

st.subheader("Project Highlights")

col1, col2 = st.columns(2)

with col1:

    st.success(
        """
### Platform Features

- Executive Dashboard
- Customer Churn Prediction
- SHAP Explainability
- Customer Insights
- Business Recommendations
"""
    )

with col2:

    st.success(
        """
### Engineering Features

- Modular Architecture
- Reusable Components
- Interactive Visualizations
- Executive Reporting
- Production-Ready Design
"""
    )

st.divider()

# ==========================================================
# Future Enhancements
# ==========================================================

st.subheader("Future Enhancements")

st.markdown(
    """
Future versions of the platform may include:

- User authentication and role-based access
- Cloud deployment
- Real-time database integration
- REST API for external applications
- Automated model retraining
- Batch prediction capability
- Model monitoring and drift detection
- Multi-model comparison dashboard
"""
)

st.divider()

# ==========================================================
# Project Information
# ==========================================================

st.subheader("Project Information")

info_col1, info_col2 = st.columns(2)

with info_col1:

    st.metric(
        "Project",
        ORGANIZATION
    )

    st.metric(
        "Version",
        VERSION
    )

with info_col2:

    st.metric(
        "Dataset",
        DATASET_NAME
    )

    st.metric(
        "Model",
        metadata.get("model_name", "Unknown")
    )

# ==========================================================
# Footer
# ==========================================================

render_footer("About Project")