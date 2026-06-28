"""
Feature Creator Module
Project: Customer Churn Intelligence Platform
Description: Reusable derived feature engineering functions.
             Each function accepts a DataFrame and returns a modified copy
             with new feature columns appended.
"""

import numpy as np
import pandas as pd


def create_tenure_groups(df):
    """
    Bins tenure into business-friendly lifecycle groups using fixed thresholds.

    Groups:
        New (0–12), Emerging (13–24), Established (25–48),
        Loyal (49–60), Long-Term (61+)
    """
    df = df.copy()
    tenure_bins = [0, 12, 24, 48, 60, np.inf]
    tenure_labels = ["New", "Emerging", "Established", "Loyal", "Long-Term"]

    df["TenureGroup"] = pd.cut(
        df["tenure"],
        bins=tenure_bins,
        labels=tenure_labels,
        include_lowest=True
    )
    return df


def create_charge_groups(df):
    """
    Bins MonthlyCharges into quartile-based spending tiers.

    Groups: Low, Medium, High, Premium
    """
    df = df.copy()
    
    # qcut requires at least 4 unique values. For single-row inference or small datasets,
    # we fall back to fixed training dataset quartiles (25%: 35.50, 50%: 70.35, 75%: 89.85)
    if df["MonthlyCharges"].nunique() < 4:
        bins = [-np.inf, 35.50, 70.35, 89.85, np.inf]
        df["MonthlyChargeGroup"] = pd.cut(
            df["MonthlyCharges"],
            bins=bins,
            labels=["Low", "Medium", "High", "Premium"]
        )
    else:
        df["MonthlyChargeGroup"] = pd.qcut(
            df["MonthlyCharges"],
            q=4,
            labels=["Low", "Medium", "High", "Premium"]
        )
    return df


def create_total_services(df):
    """
    Counts the total number of active services each customer subscribes to.
    """
    df = df.copy()
    service_columns = [
        "PhoneService",
        "MultipleLines",
        "InternetService",
        "OnlineSecurity",
        "OnlineBackup",
        "DeviceProtection",
        "TechSupport",
        "StreamingTV",
        "StreamingMovies"
    ]

    df["TotalServices"] = (
        df[service_columns]
        .replace({
            "Yes": 1,
            "Fiber optic": 1,
            "DSL": 1,
            "No": 0,
            "No internet service": 0,
            "No phone service": 0
        })
        .sum(axis=1)
    )
    return df


def create_avg_monthly_spend(df):
    """
    Calculates average monthly spend as TotalCharges / tenure.
    Falls back to MonthlyCharges when tenure is zero.
    """
    df = df.copy()
    df["AvgMonthlySpend"] = np.where(
        df["tenure"] > 0,
        df["TotalCharges"] / df["tenure"],
        df["MonthlyCharges"]
    )
    return df


def create_high_value_flag(df):
    """
    Flags customers whose MonthlyCharges exceed the dataset median.
    """
    df = df.copy()
    median_charge = df["MonthlyCharges"].median()
    df["HighValueCustomer"] = (df["MonthlyCharges"] >= median_charge).astype(int)
    return df


def create_security_risk_flag(df):
    """
    Flags customers who have neither OnlineSecurity nor TechSupport.
    """
    df = df.copy()
    df["SecurityRisk"] = (
        (df["OnlineSecurity"] == "No") &
        (df["TechSupport"] == "No")
    ).astype(int)
    return df


def create_streaming_user_flag(df):
    """
    Flags customers who subscribe to StreamingTV or StreamingMovies.
    """
    df = df.copy()
    df["StreamingUser"] = (
        (df["StreamingTV"] == "Yes") |
        (df["StreamingMovies"] == "Yes")
    ).astype(int)
    return df


def create_all_features(df):
    """
    Orchestrates all derived feature engineering steps in sequence.

    Returns a DataFrame with all new columns appended:
        TenureGroup, MonthlyChargeGroup, TotalServices,
        AvgMonthlySpend, HighValueCustomer, SecurityRisk, StreamingUser
    """
    df = create_tenure_groups(df)
    df = create_charge_groups(df)
    df = create_total_services(df)
    df = create_avg_monthly_spend(df)
    df = create_high_value_flag(df)
    df = create_security_risk_flag(df)
    df = create_streaming_user_flag(df)
    return df
