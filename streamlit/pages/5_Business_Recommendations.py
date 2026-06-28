"""
Business Recommendations Page

Provides executive-level business recommendations based on customer churn
patterns, customer segmentation, and model insights.
"""

# ==========================================================
# Imports
# ==========================================================

import utils.path_setup  # noqa: F401  — configure sys.path

import streamlit as st

from config import APP_TITLE

from components.sidebar import render_sidebar
from components.footer import render_footer
from utils.data_loader import load_dashboard_dataset
from utils.model_loader import load_model_metadata


# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title=f"{APP_TITLE} | Business Recommendations",
    page_icon="💼",
    layout="wide",
)


# ==========================================================
# Load Resources
# ==========================================================

metadata = load_model_metadata()
df = load_dashboard_dataset()

render_sidebar(metadata)

# ==========================================================
# Header
# ==========================================================

st.title("💼 Business Recommendations")

st.markdown(
    """
Transform customer churn insights into actionable business strategies.
This page provides executive recommendations, identifies priority customer
segments, and estimates the potential business impact of retention efforts.
"""
)

st.divider()

# ==========================================================
# Executive Summary
# ==========================================================

st.subheader("Executive Summary")

total_customers = len(df)

churn_customers = df["Churn"].eq("Yes").sum()

churn_rate = churn_customers / total_customers * 100

high_risk_customers = len(
    df[
        (df["Contract"] == "Month-to-month")
        & (df["Churn"] == "Yes")
    ]
)

revenue_at_risk = (
    df.loc[
        df["Churn"] == "Yes",
        "MonthlyCharges"
    ].sum()
)

if churn_rate < 15:
    business_health = "Healthy 🟢"
elif churn_rate < 30:
    business_health = "Moderate 🟡"
else:
    business_health = "Critical 🔴"

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Overall Churn Rate",
    f"{churn_rate:.1f}%"
)

c2.metric(
    "High-Risk Customers",
    f"{high_risk_customers:,}"
)

c3.metric(
    "Revenue at Risk",
    f"${revenue_at_risk:,.0f}"
)

c4.metric(
    "Business Health",
    business_health
)

st.divider()

# ==========================================================
# Strategic Recommendations
# ==========================================================

st.subheader("Strategic Recommendations")

col1, col2 = st.columns(2)

with col1:

    st.success(
        """
### 🎯 Retention Strategy

- Prioritize month-to-month customers.
- Launch targeted retention campaigns.
- Contact customers approaching contract renewal.
- Focus on customers with short tenure.
"""
    )

    st.info(
        """
### 💰 Pricing Strategy

- Review pricing for high monthly charge customers.
- Introduce loyalty discounts.
- Bundle premium services to improve value.
"""
    )

with col2:

    st.warning(
        """
### 📄 Contract Strategy

- Encourage migration to annual contracts.
- Offer renewal incentives.
- Reward long-term customer loyalty.
"""
    )

    st.success(
        """
### 🤝 Customer Experience

- Improve onboarding experience.
- Promote online security services.
- Strengthen proactive customer support.
"""
    )

st.divider()

# ==========================================================
# High-Risk Customer Segments
# ==========================================================

st.subheader("High-Risk Customer Segments")

segment_summary = (
    df.groupby(
        ["Contract", "InternetService"],
        as_index=False
    )
    .agg(
        Customers=("Churn", "count"),
        ChurnRate=("Churn", lambda x: (x == "Yes").mean() * 100),
        AverageMonthlyCharges=("MonthlyCharges", "mean")
    )
)

segment_summary["ChurnRate"] = (
    segment_summary["ChurnRate"]
    .round(1)
)

segment_summary["AverageMonthlyCharges"] = (
    segment_summary["AverageMonthlyCharges"]
    .round(2)
)

segment_summary = segment_summary.sort_values(
    by="ChurnRate",
    ascending=False
)

st.dataframe(
    segment_summary,
    width="stretch",
    hide_index=True
)

st.divider()

# ==========================================================
# Priority Matrix
# ==========================================================

st.subheader("Business Priority Matrix")


def assign_priority(rate):
    if rate >= 50:
        return "🔴 High"
    elif rate >= 25:
        return "🟡 Medium"
    return "🟢 Low"


priority_df = segment_summary.copy()

priority_df["Priority"] = (
    priority_df["ChurnRate"]
    .apply(assign_priority)
)

priority_df["Recommended Action"] = priority_df["Priority"].map({
    "🔴 High": "Immediate retention campaign",
    "🟡 Medium": "Targeted engagement",
    "🟢 Low": "Monitor customer satisfaction"
})

st.dataframe(
    priority_df[
        [
            "Priority",
            "Contract",
            "InternetService",
            "Customers",
            "ChurnRate",
            "Recommended Action"
        ]
    ],
    width="stretch",
    hide_index=True
)

st.divider()

# ==========================================================
# Estimated Business Impact
# ==========================================================

st.subheader("Estimated Business Impact")

potential_saved = int(high_risk_customers * 0.30)

revenue_protected = revenue_at_risk * 0.30

expected_reduction = "5–10%"

col1, col2, col3 = st.columns(3)

col1.metric(
    "Potential Customers Saved",
    f"{potential_saved:,}"
)

col2.metric(
    "Estimated Revenue Protected",
    f"${revenue_protected:,.0f}"
)

col3.metric(
    "Expected Churn Reduction",
    expected_reduction
)

st.caption(
    "These estimates assume a 30% improvement in retention among high-risk customers and are intended for business planning purposes."
)

st.divider()

# ==========================================================
# Implementation Roadmap
# ==========================================================

st.subheader("Implementation Roadmap")

col1, col2, col3 = st.columns(3)

with col1:

    st.info(
        """
### 🚀 Immediate (0–3 Months)

- Contact high-risk customers
- Launch retention campaigns
- Offer loyalty incentives
- Monitor churn weekly
"""
    )

with col2:

    st.warning(
        """
### 📈 Short-Term (3–6 Months)

- Improve onboarding
- Promote annual contracts
- Enhance customer support
- Optimize pricing strategy
"""
    )

with col3:

    st.success(
        """
### 🌟 Long-Term (6–12 Months)

- Personalize customer engagement
- Expand loyalty programs
- Continuously retrain ML models
- Monitor customer lifetime value
"""
    )

st.divider()

# ==========================================================
# Executive Report
# ==========================================================

st.subheader("Executive Summary Report")

report = f"""
CUSTOMER CHURN INTELLIGENCE PLATFORM

Executive Business Summary

--------------------------------------------

Overall Churn Rate : {churn_rate:.2f}%

High-Risk Customers : {high_risk_customers}

Estimated Revenue at Risk : ${revenue_at_risk:,.2f}

Business Health : {business_health}

Recommended Actions

• Prioritize month-to-month customers.
• Encourage long-term contracts.
• Improve customer onboarding.
• Launch personalized retention campaigns.
• Strengthen customer support.

Estimated Business Impact

Potential Customers Saved:
{potential_saved}

Estimated Revenue Protected:
${revenue_protected:,.2f}

Expected Churn Reduction:
{expected_reduction}
"""

st.download_button(
    label="📄 Download Executive Report",
    data=report,
    file_name="business_recommendations_report.txt",
    mime="text/plain"
)


# ==========================================================
# Footer
# ==========================================================

render_footer("Business Recommendations")