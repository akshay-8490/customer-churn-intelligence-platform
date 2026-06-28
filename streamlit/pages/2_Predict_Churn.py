"""
Predict Customer Churn

Project: Customer Churn Intelligence Platform

Interactive interface for predicting customer churn
using the trained machine learning model.
"""

# ==========================================================
# Imports
# ==========================================================

import utils.path_setup  # noqa: F401  — configure sys.path

import streamlit as st
import pandas as pd

from components.plots import (
    gauge_chart,
)
from components.cards import (
    render_prediction_card,
)
from components.sidebar import render_sidebar
from utils.model_loader import load_model_metadata
from utils.predictor import predict
from utils.prediction_formatter import (
    format_prediction,
    create_prediction_dataframe,
)
from components.footer import render_footer

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Predict Churn",
    page_icon="🎯",
    layout="wide",
)


# ==========================================================
# Load Artifacts
# ==========================================================

try:

    metadata = load_model_metadata()

except Exception as e:

    st.error(
        f"Unable to load model artifacts.\n\n{e}"
    )

    st.stop()


# ==========================================================
# Sidebar
# ==========================================================

render_sidebar(metadata)


# ==========================================================
# Session State
# ==========================================================

if "prediction_result" not in st.session_state:

    st.session_state.prediction_result = None


if "formatted_prediction" not in st.session_state:

    st.session_state.formatted_prediction = None


if "download_dataframe" not in st.session_state:

    st.session_state.download_dataframe = None


# ==========================================================
# Page Header
# ==========================================================

st.title("🎯 Predict Customer Churn")

st.caption(
    "Predict the likelihood of customer churn using the "
    "trained machine learning model."
)

st.divider()


# ==========================================================
# Instructions
# ==========================================================

st.info(
    """
    Fill in the customer information below and click
    **'🚀 Predict Customer Churn'** to generate
    a prediction and business recommendations.
    """
)

# ==========================================================
# Customer Information Form
# ==========================================================

with st.form("prediction_form"):

    # ------------------------------------------------------
    # Personal Information
    # ------------------------------------------------------

    with st.expander(
        "👤 Personal Information",
        expanded=True
    ):

        col1, col2 = st.columns(2)

        with col1:

            gender = st.selectbox(
                "Gender",
                ["Male", "Female"]
            )

            senior_citizen = st.selectbox(
                "Senior Citizen",
                [0, 1],
                format_func=lambda x: "Yes" if x else "No"
            )

        with col2:

            partner = st.selectbox(
                "Partner",
                ["Yes", "No"]
            )

            dependents = st.selectbox(
                "Dependents",
                ["Yes", "No"]
            )

    # ------------------------------------------------------
    # Service Information
    # ------------------------------------------------------

    with st.expander(
        "🌐 Service Information",
        expanded=True
    ):

        col1, col2 = st.columns(2)

        with col1:

            phone_service = st.selectbox(
                "Phone Service",
                ["Yes", "No"]
            )

            multiple_lines = st.selectbox(
                "Multiple Lines",
                ["No phone service", "No", "Yes"]
            )

            internet_service = st.selectbox(
                "Internet Service",
                ["DSL", "Fiber optic", "No"]
            )

            online_security = st.selectbox(
                "Online Security",
                ["No internet service", "No", "Yes"]
            )

            online_backup = st.selectbox(
                "Online Backup",
                ["No internet service", "No", "Yes"]
            )

        with col2:

            device_protection = st.selectbox(
                "Device Protection",
                ["No internet service", "No", "Yes"]
            )

            tech_support = st.selectbox(
                "Tech Support",
                ["No internet service", "No", "Yes"]
            )

            streaming_tv = st.selectbox(
                "Streaming TV",
                ["No internet service", "No", "Yes"]
            )

            streaming_movies = st.selectbox(
                "Streaming Movies",
                ["No internet service", "No", "Yes"]
            )

    # ------------------------------------------------------
    # Billing Information
    # ------------------------------------------------------

    with st.expander(
        "💳 Billing Information",
        expanded=True
    ):

        col1, col2 = st.columns(2)

        with col1:

            contract = st.selectbox(
                "Contract",
                [
                    "Month-to-month",
                    "One year",
                    "Two year"
                ]
            )

            paperless_billing = st.selectbox(
                "Paperless Billing",
                ["Yes", "No"]
            )

            payment_method = st.selectbox(
                "Payment Method",
                [
                    "Electronic check",
                    "Mailed check",
                    "Bank transfer (automatic)",
                    "Credit card (automatic)",
                ]
            )

        with col2:

            tenure = st.slider(
                "Tenure (Months)",
                min_value=0,
                max_value=72,
                value=12,
            )

            monthly_charges = st.number_input(
                "Monthly Charges",
                min_value=0.0,
                max_value=200.0,
                value=70.0,
                step=0.5,
            )

            auto_total_charges = st.checkbox(
                "Automatically calculate Total Charges",
                value=True,
            )

            if auto_total_charges:

                total_charges = round(tenure * monthly_charges, 2,)
                st.number_input("Total Charges", value=total_charges, disabled=True,)

            else: 
                total_charges = st.number_input("Total Charges", min_value=0.0, value=850.0, step=1.0,)

    # ------------------------------------------------------
    # Predict Button
    # ------------------------------------------------------

    submitted = st.form_submit_button(
        "🚀 Predict Customer Churn",
        width="stretch",
    )

# ==========================================================
# Prediction Pipeline
# ==========================================================

if submitted:

    customer_input = {

        "gender": gender,
        "SeniorCitizen": senior_citizen,
        "Partner": partner,
        "Dependents": dependents,
        "PhoneService": phone_service,
        "MultipleLines": multiple_lines,
        "InternetService": internet_service,
        "OnlineSecurity": online_security,
        "OnlineBackup": online_backup,
        "DeviceProtection": device_protection,
        "TechSupport": tech_support,
        "StreamingTV": streaming_tv,
        "StreamingMovies": streaming_movies,
        "Contract": contract,
        "PaperlessBilling": paperless_billing,
        "PaymentMethod": payment_method,
        "tenure": tenure,
        "MonthlyCharges": monthly_charges,
        "TotalCharges": total_charges,
    }

    try:

        prediction_result = predict(customer_input)

        formatted_prediction = format_prediction(
            prediction_result
        )

        download_dataframe = create_prediction_dataframe(
            customer_input,
            formatted_prediction,
        )

        st.session_state.prediction_result = prediction_result

        st.session_state.formatted_prediction = (
            formatted_prediction
        )

        st.session_state.download_dataframe = (
            download_dataframe
        )

        st.success(
            "Prediction completed successfully."
        )

    except Exception as e:

        st.error(
            f"Prediction failed.\n\n{e}"
        )

# ==========================================================
# Prediction Results
# ==========================================================

if st.session_state.formatted_prediction is not None:

    formatted_prediction = st.session_state.formatted_prediction
    prediction_result = st.session_state.prediction_result

    st.divider()

    st.subheader("Prediction Summary")

    # ------------------------------------------------------
    # Business Recommendation
    # ------------------------------------------------------

    probability = formatted_prediction["probability_percent"]

    if probability >= 80:

        recommended_action = (
            "Immediate outbound call and premium retention offer."
        )

    elif probability >= 60:

        recommended_action = (
            "Provide personalized discount and service review."
        )

    elif probability >= 40:

        recommended_action = (
            "Send loyalty campaign and monitor customer activity."
        )

    else:

        recommended_action = (
            "No immediate action required."
        )

    # ------------------------------------------------------
    # Summary Cards
    # ------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        render_prediction_card(
            title="Prediction",
            value=formatted_prediction["prediction_text"],
            icon=formatted_prediction["icon"],
            color=formatted_prediction["color"],
        )

    with col2:

        render_prediction_card(
            title="Risk Level",
            value=formatted_prediction["risk_level"],
            icon="⚠️",
            color=formatted_prediction["color"],
        )

    col3, col4 = st.columns(2)

    with col3:

        render_prediction_card(
            title="Churn Probability",
            value=formatted_prediction["probability_display"],
            icon="📈",
            color="#2563EB",
        )

    with col4:

        render_prediction_card(
            title="Recommended Action",
            value=recommended_action,
            icon="💡",
            color="#10B981",
        )

    st.divider()

    # ------------------------------------------------------
    # Churn Probability Gauge
    # ------------------------------------------------------

    st.subheader("Churn Probability")

    gauge = gauge_chart(
        value=formatted_prediction["probability_percent"],
        title="Predicted Churn Probability",
        threshold=formatted_prediction["threshold_percent"],
    )

    st.plotly_chart(
        gauge,
        width="stretch",
        key="prediction_gauge",
    )

    st.divider()

    # ------------------------------------------------------
    # Prediction Details
    # ------------------------------------------------------

    st.subheader("Prediction Details")

    details = {
        "Metric": [
            "Prediction",
            "Risk Level",
            "Probability",
            "Threshold",
            "Model",
        ],
        "Value": [
            formatted_prediction["prediction_text"],
            formatted_prediction["risk_level"],
            formatted_prediction["probability_display"],
            formatted_prediction["threshold_display"],
            metadata.get("model_name", "N/A"),
        ],
    }

    details_df = pd.DataFrame(details)

    st.dataframe(
        details_df,
        width="stretch",
        hide_index=True,
    )

    # ==========================================================
# Download Prediction Report
# ==========================================================

if st.session_state.download_dataframe is not None:

    st.divider()

    st.subheader("Download Prediction Report")

    csv = (
        st.session_state.download_dataframe
        .to_csv(index=False)
        .encode("utf-8")
    )

    st.download_button(
        label="📥 Download Prediction Report",
        data=csv,
        file_name="customer_prediction_report.csv",
        mime="text/csv",
        width="stretch",
    )


# ==========================================================
# Reset Prediction
# ==========================================================

st.divider()

if st.button(
    "🔄 Reset Prediction",
    width="stretch",
):

    st.session_state.prediction_result = None
    st.session_state.formatted_prediction = None
    st.session_state.download_dataframe = None

    st.rerun()


# ==========================================================
# Footer
# ==========================================================

render_footer("Predict Churn")