"""
Model Artifact Loader
Project: Customer Churn Intelligence Platform

Loads and caches machine learning artifacts used by the
Streamlit application.
"""

import json
import joblib

import streamlit as st

from src.config.paths import ARTIFACTS_DIR


# ==========================================================
# Artifact Paths
# ==========================================================

BEST_MODEL_PATH = ARTIFACTS_DIR / "best_model.pkl"
PREPROCESSOR_PATH = ARTIFACTS_DIR / "preprocessor.pkl"
SELECTED_FEATURES_PATH = ARTIFACTS_DIR / "selected_features.pkl"
MODEL_METADATA_PATH = ARTIFACTS_DIR / "model_metadata.json"


# ==========================================================
# Load Best Model
# ==========================================================

@st.cache_resource
def load_model():
    """
    Load the trained machine learning model.
    """

    with open(BEST_MODEL_PATH, "rb") as file:
        model = joblib.load(file)

    return model


# ==========================================================
# Load Preprocessor
# ==========================================================

@st.cache_resource
def load_preprocessor():
    """
    Load the preprocessing pipeline.
    """

    with open(PREPROCESSOR_PATH, "rb") as file:
        preprocessor = joblib.load(file)

    return preprocessor


# ==========================================================
# Load Selected Features
# ==========================================================

@st.cache_resource
def load_selected_features():
    """
    Load the selected feature list.
    """

    with open(SELECTED_FEATURES_PATH, "rb") as file:
        selected_features = joblib.load(file)

    return selected_features


# ==========================================================
# Load Model Metadata
# ==========================================================

@st.cache_resource
def load_model_metadata():
    """
    Load model metadata.
    """

    with open(MODEL_METADATA_PATH, "r") as file:
        metadata = json.load(file)

    return metadata


# ==========================================================
# Load All Artifacts
# ==========================================================

@st.cache_resource
def load_artifacts():
    """
    Load all required ML artifacts.

    Returns
    -------
    dict
        Dictionary containing all loaded artifacts.
    """

    return {
        "model": load_model(),
        "preprocessor": load_preprocessor(),
        "selected_features": load_selected_features(),
        "metadata": load_model_metadata(),
    }