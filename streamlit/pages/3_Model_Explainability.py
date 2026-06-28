"""
Model Explainability Page

Provides an executive-friendly overview of how the churn prediction model
makes decisions using global feature importance and SHAP explainability.
"""

# ==========================================================
# Imports
# ==========================================================

import utils.path_setup  # noqa: F401  — configure sys.path

import streamlit as st

from config import APP_TITLE

from components.plots import display_figure
from components.sidebar import render_sidebar
from components.footer import render_footer
from utils.model_loader import load_model_metadata


# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title=f"{APP_TITLE} | Model Explainability",
    page_icon="🧠",
    layout="wide",
)


# ==========================================================
# Load Artifacts
# ==========================================================

try:

    metadata = load_model_metadata()

except Exception as e:

    st.error(f"Unable to load model metadata.\n\n{e}")

    st.stop()


# ==========================================================
# Sidebar
# ==========================================================

render_sidebar(metadata)


# ==========================================================
# Page Header
# ==========================================================

st.title("🧠 Model Explainability")

st.markdown(
    """
Understand how the machine learning model identifies customers at risk of
churn using feature importance and SHAP explainability. These visualizations
help explain which customer characteristics most influence the model's
predictions, improving transparency and supporting informed business
decisions.
"""
)

st.divider()


# ==========================================================
# Model Summary
# ==========================================================

st.subheader("Model Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Model",
        metadata.get("model_name", "Unknown")
    )

with col2:
    st.metric(
        "ROC-AUC",
        f"{metadata.get('roc_auc', 0):.3f}"
    )

with col3:
    st.metric(
        "Decision Threshold",
        metadata.get("threshold", "N/A")
    )

st.info(
    """
**Explainability Methods Used**

- Model Coefficients
- Permutation Feature Importance
- SHAP (SHapley Additive exPlanations)

These techniques provide both global and local insights into the model's
behavior, making predictions more transparent and easier to interpret.
"""
)

st.divider()

# ==========================================================
# Global Feature Importance
# ==========================================================

st.subheader("Global Feature Importance")

st.markdown(
    """
The chart below ranks the features that have the greatest influence on churn
prediction across the entire customer population.
"""
)

display_figure(
    "feature_importance.png",
    caption="Global Feature Importance"
)

st.success(
    """
**Business Interpretation**

The model primarily relies on customer tenure, contract type, monthly
charges, internet service, and total charges when estimating churn
probability. These variables consistently have the strongest influence on
customer retention decisions and should receive the highest business
attention.
"""
)

st.divider()


# ==========================================================
# SHAP Summary Plot
# ==========================================================

st.subheader("SHAP Summary")

st.markdown(
    """
SHAP (SHapley Additive exPlanations) quantifies how much each feature
contributes to individual predictions while also revealing overall feature
importance.
"""
)

display_figure(
    "shap_summary.png",
    caption="SHAP Summary Plot"
)

st.info(
    """
### Understanding the SHAP Summary

- Each point represents one customer.
- Features are ordered by overall importance.
- Red points indicate high feature values.
- Blue points indicate low feature values.
- Points farther to the right increase churn probability.
- Points farther to the left reduce churn probability.

This visualization provides a global understanding of how customer
characteristics influence the model's decisions.
"""
)

st.divider()


# ==========================================================
# SHAP Feature Impact Distribution
# ==========================================================

st.subheader("Feature Impact Distribution")

st.markdown(
    """
The SHAP Beeswarm plot illustrates how feature values affect churn risk
across the customer base.
"""
)

display_figure(
    "shap_beeswarm.png",
    caption="SHAP Feature Impact Distribution"
)

st.success(
    """
### Business Insights

The explainability analysis reveals several important business patterns:

- Customers with longer tenure generally exhibit lower churn risk.
- Month-to-month contracts are associated with higher churn.
- Higher monthly charges increase churn probability.
- Fiber optic internet customers tend to show elevated churn risk.
- Customers using electronic check payments are more likely to churn.

These insights help customer retention teams identify which customer
segments should receive proactive engagement strategies.
"""
)

st.divider()


# ==========================================================
# Explainability Notes
# ==========================================================

st.subheader("Explainability Notes")

with st.expander("Understanding Model Explainability", expanded=False):

    st.markdown(
        """
### Why Explainability Matters

Machine learning models often achieve high predictive performance but can
appear difficult to interpret. Explainability techniques increase
transparency by showing which customer characteristics influence model
predictions.

### Global vs Local Explainability

- **Global Explainability** identifies the features that are most important
  across the entire customer population.

- **Local Explainability** explains why the model produced a specific
  prediction for an individual customer.

### Current Implementation

This platform combines multiple explainability techniques:

- Logistic Regression coefficients
- Permutation Feature Importance
- SHAP (SHapley Additive exPlanations)

All explainability visualizations were generated during the model analysis
phase and are displayed directly within the application to ensure consistency
with the validated notebook results.
"""
    )


# ==========================================================
# Footer
# ==========================================================

render_footer("Model Explainability")