"""
Dataset Loader
Project: Customer Churn Intelligence Platform

Loads datasets required by the Streamlit application.
"""

from pathlib import Path

import pandas as pd
import streamlit as st

from src.config.paths import (
    REPORTS_DASHBOARD_DIR,
    PROCESSED_DATA_DIR,
    INTERIM_DATA_DIR,
)

# ==========================================================
# Dataset Paths
# ==========================================================

DASHBOARD_DATASET_PATH = REPORTS_DASHBOARD_DIR / "dashboard_dataset.csv"

PROCESSED_DATASET_PATH = (
    PROCESSED_DATA_DIR / "ml_dataset_processed.csv"
)

BUSINESS_DATASET_PATH = (
    INTERIM_DATA_DIR / "business_dataset_interim.csv"
)


# ==========================================================
# Dashboard Dataset
# ==========================================================

@st.cache_data(show_spinner=False)
def load_dashboard_dataset() -> pd.DataFrame:
    """
    Load dashboard dataset.

    Returns
    -------
    pandas.DataFrame
    """

    return pd.read_csv(DASHBOARD_DATASET_PATH)


# ==========================================================
# Processed ML Dataset
# ==========================================================

@st.cache_data(show_spinner=False)
def load_processed_dataset() -> pd.DataFrame:
    """
    Load processed ML dataset.

    Returns
    -------
    pandas.DataFrame
    """

    return pd.read_csv(PROCESSED_DATASET_PATH)


# ==========================================================
# Business Dataset
# ==========================================================

@st.cache_data(show_spinner=False)
def load_business_dataset() -> pd.DataFrame:
    """
    Load business analytics dataset.

    Returns
    -------
    pandas.DataFrame
    """

    return pd.read_csv(BUSINESS_DATASET_PATH)