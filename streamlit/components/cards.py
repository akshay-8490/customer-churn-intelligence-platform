"""
Reusable Card Components
Project: Customer Churn Intelligence Platform

Contains reusable card components shared across multiple
Streamlit pages.
"""

from __future__ import annotations

import streamlit as st


# ==========================================================
# Information Card
# ==========================================================

def render_info_card(
    title: str,
    value: str,
    icon: str = "ℹ️"
) -> None:
    """
    Display an information card.

    Parameters
    ----------
    title : str
        Card title.

    value : str
        Card body.

    icon : str, default="ℹ️"
        Emoji displayed before the title.
    """

    with st.container(border=True):

        st.subheader(f"{icon} {title}")

        st.write(value)


# ==========================================================
# Prediction Result Card
# ==========================================================

def render_prediction_card(
    title: str,
    value: str,
    icon: str = "",
    color: str = "#2563EB",
) -> None:
    """
    Render a styled prediction result card.

    Parameters
    ----------
    title : str
        Card title.

    value : str
        Main value displayed.

    icon : str, optional
        Emoji or icon shown before title.

    color : str, optional
        Left border color.
    """

    st.markdown(
        f"""
        <div style="
            background-color:#FFFFFF;
            border-left:6px solid {color};
            border-radius:10px;
            padding:18px;
            margin-bottom:10px;
            box-shadow:0 2px 8px rgba(0,0,0,0.08);
        ">

        <div style="
            font-size:15px;
            color:#666666;
            font-weight:600;
        ">
            {icon} {title}
        </div>

        <div style="
            font-size:28px;
            font-weight:bold;
            color:#111111;
            margin-top:8px;
        ">
            {value}
        </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

# ==========================================================
# Risk Badge
# ==========================================================

def render_risk_badge(
    risk_level: str,
) -> None:
    """
    Display a colored risk badge.

    Parameters
    ----------
    risk_level : str
    """

    risk = risk_level.lower()

    if risk == "high":

        color = "#F44336"

        icon = "🔴"

    elif risk == "medium":

        color = "#FFC107"

        icon = "🟡"

    else:

        color = "#4CAF50"

        icon = "🟢"

    st.markdown(
        f"""
        <div style="
            display:inline-block;
            padding:8px 18px;
            border-radius:25px;
            background:{color};
            color:white;
            font-weight:bold;
            font-size:15px;
        ">
            {icon} {risk_level}
        </div>
        """,
        unsafe_allow_html=True,
    )

__all__ = [

    "render_info_card",

    "render_prediction_card",

    "render_risk_badge",

]