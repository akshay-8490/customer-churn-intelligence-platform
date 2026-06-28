"""
Dashboard Metrics Utility

Contains reusable business calculations for the
Customer Churn Intelligence Platform dashboard.
"""

from __future__ import annotations

import pandas as pd


def get_executive_metrics(df: pd.DataFrame) -> dict:
    """
    Compute executive-level dashboard KPIs.

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    dict
    """

    if df.empty:
        return {
            "total_customers": 0,
            "churn_rate": 0.0,
            "avg_probability": 0.0,
            "high_risk_customers": 0,
        }

    total_customers = len(df)

    churn_rate = (
        (df["Churn"] == "Yes").mean() * 100
        if "Churn" in df.columns
        else 0
    )

    avg_probability = df["Churn_Probability"].mean() * 100

    high_risk_customers = (
        df["Risk_Segment"]
        .astype(str)
        .str.lower()
        .eq("high")
        .sum()
    )

    return {
        "total_customers": total_customers,
        "churn_rate": churn_rate,
        "avg_probability": avg_probability,
        "high_risk_customers": high_risk_customers,
    }


def get_business_metrics(df: pd.DataFrame) -> dict:
    """
    Compute business KPIs.

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    dict
    """

    if df.empty:
        return {
            "monthly_revenue": 0.0,
            "revenue_at_risk": 0.0,
            "average_tenure": 0.0,
            "retention_budget": 0.0,
        }

    monthly_revenue = df["MonthlyCharges"].sum()

    revenue_at_risk = (
        df["MonthlyCharges"] *
        df["Churn_Probability"]
    ).sum()

    average_tenure = df["tenure"].mean()

    retention_budget = df["Estimated_Action_Cost"].sum()

    return {
        "monthly_revenue": monthly_revenue,
        "revenue_at_risk": revenue_at_risk,
        "average_tenure": average_tenure,
        "retention_budget": retention_budget,
    }


def get_retention_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Summarize retention actions.

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    pandas.DataFrame
    """

    summary = (
        df.groupby("Retention_Action", as_index=False)
        .agg(
            Customers=("CustomerID", "count"),
            Estimated_Cost=("Estimated_Action_Cost", "sum"),
        )
        .sort_values(
            by="Customers",
            ascending=False,
        )
    )

    return summary


def get_priority_customers(
    df: pd.DataFrame,
    top_n: int = 20,
) -> pd.DataFrame:
    """
    Return highest priority customers.

    Parameters
    ----------
    df : pandas.DataFrame

    top_n : int

    Returns
    -------
    pandas.DataFrame
    """

    columns = [
        "CustomerID",
        "Risk_Segment",
        "Churn_Probability",
        "Priority_Score",
        "Persona",
        "Retention_Action",
    ]

    priority_df = (
        df[columns]
        .sort_values(
            by="Priority_Score",
            ascending=False,
        )
        .head(top_n)
        .reset_index(drop=True)
    )

    priority_df["Churn_Probability"] = (
        priority_df["Churn_Probability"] * 100
    )

    return priority_df


def get_risk_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """
    Risk segment distribution.

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    pandas.DataFrame
    """

    return (
        df["Risk_Segment"]
        .value_counts()
        .rename_axis("Risk_Segment")
        .reset_index(name="Customers")
    )


def get_persona_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """
    Persona distribution.

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    pandas.DataFrame
    """

    return (
        df["Persona"]
        .value_counts()
        .rename_axis("Persona")
        .reset_index(name="Customers")
    )


def get_revenue_by_risk(df: pd.DataFrame) -> pd.DataFrame:
    """
    Monthly revenue grouped by risk segment.

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    pandas.DataFrame
    """

    return (
        df.groupby("Risk_Segment", as_index=False)
        .agg(
            Revenue=("MonthlyCharges", "sum")
        )
    )


def get_monthly_charge_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """
    Average monthly charge by risk segment.

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    pandas.DataFrame
    """

    return (
        df.groupby("Risk_Segment", as_index=False)
        .agg(
            Average_Monthly_Charge=("MonthlyCharges", "mean")
        )
    )