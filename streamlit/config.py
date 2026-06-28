"""
Streamlit Configuration
Project: Customer Churn Intelligence Platform
Contains all Streamlit UI configuration constants.
Business logic and model settings should remain inside src/config.
"""

from src.config.settings import VERSION, MODEL_NAME


# ==========================================================
# Application Configuration
# ==========================================================

APP_TITLE = "Customer Churn Intelligence Platform"
APP_ICON = "📊"
LAYOUT = "wide"
SIDEBAR_STATE = "expanded"

# ==========================================================
# Branding
# ==========================================================

DATASET_NAME = "IBM Telco Customer Churn"
ORGANIZATION = "Customer Churn Intelligence Platform"
FOOTER_TEXT = (
    f"Customer Churn Intelligence Platform • Version {VERSION}"
)
COPYRIGHT = "© 2026"

# ==========================================================
# Model Information
# ==========================================================

MODEL_DISPLAY_NAME = MODEL_NAME.replace("_", " ").title()

# ==========================================================
# Risk Thresholds
# ==========================================================

LOW_RISK_THRESHOLD = 0.30
MEDIUM_RISK_THRESHOLD = 0.70

# ==========================================================
# Risk Labels
# ==========================================================

LOW_RISK = "🟢 Low Risk"
MEDIUM_RISK = "🟡 Medium Risk"
HIGH_RISK = "🔴 High Risk"

# ==========================================================
# Theme Colors
# ==========================================================

PRIMARY_COLOR = "#2563EB"
SUCCESS_COLOR = "#16A34A"
WARNING_COLOR = "#F59E0B"
DANGER_COLOR = "#DC2626"
BACKGROUND_COLOR = "#F8FAFC"

# ==========================================================
# Dashboard Metrics
# ==========================================================

METRIC_TOTAL_CUSTOMERS = "Total Customers"
METRIC_CHURN_RATE = "Churn Rate"
METRIC_RETENTION_RATE = "Retention Rate"
METRIC_REVENUE_AT_RISK = "Revenue at Risk"
METRIC_AVG_MONTHLY_CHARGE = "Average Monthly Charges"

# ==========================================================
# Navigation
# ==========================================================

PAGES = [
    "Dashboard",
    "Predict Churn",
    "Model Explainability",
    "Customer Insights",
    "Business Recommendations",
    "About Project",
]