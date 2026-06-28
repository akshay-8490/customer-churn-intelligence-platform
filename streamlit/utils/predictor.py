"""
Prediction Engine
Project: Customer Churn Intelligence Platform

Provides reusable prediction functions for the Streamlit application.
"""

from __future__ import annotations

from typing import Any

import pandas as pd

from src.features.feature_creator import create_all_features

from config import LOW_RISK_THRESHOLD, MEDIUM_RISK_THRESHOLD
from utils.model_loader import load_artifacts


# ==========================================================
# Create Input DataFrame
# ==========================================================

def create_input_dataframe(user_input: dict[str, Any]) -> pd.DataFrame:
    """
    Convert user input dictionary into a single-row DataFrame.

    Parameters
    ----------
    user_input : dict
        Raw customer information collected from Streamlit.

    Returns
    -------
    pandas.DataFrame
    """

    return pd.DataFrame([user_input])


# ==========================================================
# Feature Engineering
# ==========================================================

def engineer_features(
    input_df: pd.DataFrame,
    monthly_charge_median: float
) -> pd.DataFrame:
    """
    Create engineered features required by the ML pipeline.

    Parameters
    ----------
    input_df : pandas.DataFrame
        Raw customer data.

    monthly_charge_median : float
        Median MonthlyCharges from training data.

    Returns
    -------
    pandas.DataFrame
    """

    df = create_all_features(input_df)

    df["HighValueCustomer"] = (
        df["MonthlyCharges"] >= monthly_charge_median
    ).astype(int)

    return df

# ==========================================================
# Preprocessing
# ==========================================================

def preprocess_features(
    engineered_df: pd.DataFrame,
    preprocessor
):
    """
    Apply trained preprocessing pipeline.

    Parameters
    ----------
    engineered_df : pandas.DataFrame

    preprocessor : sklearn ColumnTransformer

    Returns
    -------
    numpy.ndarray
    """

    return preprocessor.transform(engineered_df)

# ==========================================================
# Probability Prediction
# ==========================================================

def predict_probability(
    processed_features,
    model
) -> float:
    """
    Predict churn probability.

    Returns
    -------
    float
    """

    probability = model.predict_proba(processed_features)[0][1]

    return float(probability)

# ==========================================================
# Risk Level
# ==========================================================

def get_risk_level(probability: float) -> str:
    """
    Convert probability into business-friendly risk level.
    """

    if probability < LOW_RISK_THRESHOLD:
        return "Low Risk"

    if probability < MEDIUM_RISK_THRESHOLD:
        return "Medium Risk"

    return "High Risk"

# ==========================================================
# Prediction Pipeline
# ==========================================================

def predict(user_input: dict[str, Any]) -> dict[str, Any]:
    """
    Complete inference pipeline.

    Parameters
    ----------
    user_input : dict

    Returns
    -------
    dict
    """

    artifacts = load_artifacts()

    model = artifacts["model"]

    preprocessor = artifacts["preprocessor"]

    metadata = artifacts["metadata"]

    threshold = metadata.get("threshold", 0.55)

    monthly_charge_median = metadata.get("monthly_charge_median", 70.35)

    input_df = create_input_dataframe(user_input)

    engineered_df = engineer_features(
        input_df,
        monthly_charge_median
    )

    processed = preprocess_features(
        engineered_df,
        preprocessor
    )

    probability = predict_probability(
        processed,
        model
    )

    prediction = "Yes" if probability >= threshold else "No"

    return {
        "prediction": prediction,
        "probability": probability,
        "risk_level": get_risk_level(probability),
        "threshold": threshold
    }