"""
Prediction Formatter

Project: Customer Churn Intelligence Platform

Formats prediction results into UI-ready values for
Streamlit pages.
"""

from __future__ import annotations

import pandas as pd


# ==========================================================
# Prediction Formatter
# ==========================================================

def format_prediction(result: dict) -> dict:
    """
    Format prediction output for UI display.

    Parameters
    ----------
    result : dict
        Output returned by predictor.predict_customer().

    Expected Keys
    -------------
    prediction
    probability
    risk_level
    threshold

    Returns
    -------
    dict
        Formatted prediction information.
    """

    probability = result.get("probability", 0.0)
    threshold = result.get("threshold", 0.55)
    prediction = result.get("prediction", 0)
    risk_level = result.get("risk_level", "Low")

    prediction_text = (
    "Likely to Churn"
    if str(prediction).lower() == "yes"
    else "Likely to Stay"
)

    if "high" in risk_level.lower():
        icon = "🔴"
        color = "#F44336"

    elif "medium" in risk_level.lower():
        icon = "🟡"
        color = "#FFC107"

    else:
        icon = "🟢"
        color = "#4CAF50"

    return {

        "prediction": prediction,
        "prediction_text": prediction_text,
        "probability": probability,
        "probability_percent": probability * 100,
        "probability_display": f"{probability * 100:.2f}%",
        "risk_level": risk_level,
        "threshold": threshold,
        "threshold_percent": threshold * 100,
        "threshold_display": f"{threshold * 100:.0f}%",
        "icon": icon,
        "color": color,

    }

# ==========================================================
# Prediction Download Data
# ==========================================================



def create_prediction_dataframe(
    customer_input: dict,
    formatted_prediction: dict,
) -> pd.DataFrame:
    """
    Create a downloadable prediction report.

    Parameters
    ----------
    customer_input : dict
        User input collected from Streamlit form.

    formatted_prediction : dict
        Output from format_prediction().

    Returns
    -------
    pandas.DataFrame
    """

    report = {
        **customer_input,

        "Prediction":
            formatted_prediction["prediction_text"],

        "Probability":
            formatted_prediction["probability_display"],

        "Risk Level":
            formatted_prediction["risk_level"],

        "Threshold":
            formatted_prediction["threshold_display"],
    }

    return pd.DataFrame([report])

# ==========================================================
# Export
# ==========================================================

__all__ = [
    "format_prediction",
    "create_prediction_dataframe",
]