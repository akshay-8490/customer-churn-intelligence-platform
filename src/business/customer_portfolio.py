import pandas as pd

def portfolio_summary(df_business):
    """
    Computes high-level statistics and churn probabilities for the customer base.
    """
    return pd.DataFrame({
        "Metric": [
            "Total Customers",
            "High Risk Customers",
            "Critical Customers",
            "Average Customer Tenure",
            "Average Monthly Charges",
            "Average Churn Probability"
        ],
        "Value": [
            len(df_business),
            df_business["Risk_Segment"].isin(["At Risk", "Critical"]).sum(),
            (df_business["Risk_Segment"] == "Critical").sum(),
            round(df_business["tenure"].mean(), 2),
            round(df_business["MonthlyCharges"].mean(), 2),
            round(df_business["Churn_Probability"].mean(), 3)
        ]
    })

def contract_portfolio(df_business):
    """
    Analyzes customer volume and average churn risk per contract type.
    """
    return (
        pd.crosstab(
            df_business["Contract"],
            df_business["Risk_Segment"],
            normalize="index"
        )
        * 100
    ).round(2)

def internet_portfolio(df_business):
    """
    Analyzes customer distribution and risk by internet service type.
    """
    return (
        pd.crosstab(
            df_business["InternetService"],
            df_business["Risk_Segment"],
            normalize="index"
        )
        * 100
    ).round(2)

def payment_portfolio(df_business):
    """
    Analyzes customer counts and churn risk by payment method.
    """
    return (
        pd.crosstab(
            df_business["PaymentMethod"],
            df_business["Risk_Segment"],
            normalize="index"
        )
        * 100
    ).round(2)

def demographic_profile(df_business):
    """
    Groups customer counts and churn risk by demographics profile attributes.
    """
    return (
        df_business
        .groupby("Risk_Segment")
        .agg(
            Customers=("CustomerID", "count"),
            Avg_Tenure=("tenure", "mean"),
            Avg_Monthly_Charges=("MonthlyCharges", "mean"),
            Avg_Churn_Probability=("Churn_Probability", "mean")
        )
        .round(2)
    )

def high_risk_customers(df_business, limit=20):
    """
    Filters and returns the top N highest-risk customers.
    """
    high_risk = (
        df_business[
            df_business["Risk_Segment"].isin(["At Risk", "Critical"])
        ]
        .sort_values("Churn_Probability", ascending=False)
    )
    cols = [
        "CustomerID",
        "Contract",
        "InternetService",
        "PaymentMethod",
        "tenure",
        "MonthlyCharges",
        "Churn_Probability",
        "Risk_Segment"
    ]
    return high_risk[cols].head(limit)
