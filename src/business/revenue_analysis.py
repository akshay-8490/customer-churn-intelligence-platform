import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def _get_monthly_charges_scale(preprocessor):
    """
    Dynamically retrieves the mean and scale of the MonthlyCharges column
    from the fitted scaler within the preprocessor.
    """
    scaler = preprocessor.named_transformers_['numerical'].named_steps['scaler']
    numerical_cols = next(
        t[2] for t in preprocessor.transformers_ if t[0] == "numerical"
    )
    m_idx = list(numerical_cols).index("MonthlyCharges")
    return scaler.mean_[m_idx], scaler.scale_[m_idx]

def calculate_revenue_kpis(df, model, preprocessor):
    """
    Calculates high-level Monthly Recurring Revenue (MRR) KPIs and churn rates.
    """
    m_mean, m_scale = _get_monthly_charges_scale(preprocessor)
    
    X = df.drop(columns="Churn")
    proba = model.predict_proba(X)[:, 1]
    
    df_temp = df.copy()
    df_temp["Churn_Probability"] = proba
    df_temp["MonthlyCharges_unscaled"] = df["MonthlyCharges"] * m_scale + m_mean
    
    total_mrr = df_temp["MonthlyCharges_unscaled"].sum()
    expected_mrr_loss = (df_temp["MonthlyCharges_unscaled"] * df_temp["Churn_Probability"]).sum()
    high_risk_mrr_loss = df_temp[df_temp["Churn_Probability"] > 0.5]["MonthlyCharges_unscaled"].sum()
    
    expected_churn_rate = df_temp["Churn_Probability"].mean()
    if df_temp["Churn"].dtype == object:
        actual_churn_rate = (df_temp["Churn"] == "Yes").mean()
    else:
        actual_churn_rate = df_temp["Churn"].mean()
    
    return {
        "Total Customers": int(len(df_temp)),
        "Total Monthly Revenue (MRR)": float(total_mrr),
        "Expected Monthly Revenue Loss": float(expected_mrr_loss),
        "High Risk Monthly Revenue Loss": float(high_risk_mrr_loss),
        "Expected Churn Rate": float(expected_churn_rate),
        "Actual Churn Rate": float(actual_churn_rate)
    }

def revenue_by_segment(df, model, preprocessor):
    """
    Analyzes MRR and churn probability by demographics segments.
    """
    m_mean, m_scale = _get_monthly_charges_scale(preprocessor)
    
    X = df.drop(columns="Churn")
    proba = model.predict_proba(X)[:, 1]
    
    df_temp = df.copy()
    df_temp["Churn_Probability"] = proba
    df_temp["MonthlyCharges_unscaled"] = df["MonthlyCharges"] * m_scale + m_mean
    
    segments = {}
    if "SeniorCitizen" in df_temp.columns:
        segments["Senior Citizens"] = df_temp[df_temp["SeniorCitizen"] > 0]
        segments["Non-Senior Citizens"] = df_temp[df_temp["SeniorCitizen"] <= 0]
    if "Partner_Yes" in df_temp.columns:
        segments["Has Partner"] = df_temp[df_temp["Partner_Yes"] > 0.5]
    if "Partner_No" in df_temp.columns:
        segments["No Partner"] = df_temp[df_temp["Partner_No"] > 0.5]
    if "Dependents_Yes" in df_temp.columns:
        segments["Has Dependents"] = df_temp[df_temp["Dependents_Yes"] > 0.5]
    if "Dependents_No" in df_temp.columns:
        segments["No Dependents"] = df_temp[df_temp["Dependents_No"] > 0.5]
    
    report = []
    for name, sub_df in segments.items():
        if len(sub_df) == 0:
            continue
        total_mrr = sub_df["MonthlyCharges_unscaled"].sum()
        expected_mrr_loss = (sub_df["MonthlyCharges_unscaled"] * sub_df["Churn_Probability"]).sum()
        avg_probability = sub_df["Churn_Probability"].mean()
        
        report.append({
            "Segment": name,
            "Customer Count": int(len(sub_df)),
            "Total MRR": float(total_mrr),
            "Expected MRR Loss": float(expected_mrr_loss),
            "Avg Churn Probability": float(avg_probability)
        })
        
    return pd.DataFrame(report)

def revenue_by_contract(df, model, preprocessor):
    """
    Analyzes MRR risk and count of customers per contract type.
    """
    m_mean, m_scale = _get_monthly_charges_scale(preprocessor)
    
    X = df.drop(columns="Churn")
    proba = model.predict_proba(X)[:, 1]
    
    df_temp = df.copy()
    df_temp["Churn_Probability"] = proba
    df_temp["MonthlyCharges_unscaled"] = df["MonthlyCharges"] * m_scale + m_mean
    
    contracts = {
        "Month-to-Month": "Contract_Month-to-month",
        "One Year": "Contract_One year",
        "Two Year": "Contract_Two year"
    }
    
    report = []
    for display_name, col in contracts.items():
        if col in df_temp.columns:
            sub_df = df_temp[df_temp[col] > 0.5]
            total_mrr = sub_df["MonthlyCharges_unscaled"].sum()
            expected_mrr_loss = (sub_df["MonthlyCharges_unscaled"] * sub_df["Churn_Probability"]).sum()
            avg_probability = sub_df["Churn_Probability"].mean()
            
            report.append({
                "Contract Type": display_name,
                "Customer Count": int(len(sub_df)),
                "Total MRR": float(total_mrr),
                "Expected MRR Loss": float(expected_mrr_loss),
                "Avg Churn Probability": float(avg_probability)
            })
            
    return pd.DataFrame(report)

def revenue_by_service(df, model, preprocessor):
    """
    Analyzes MRR exposure by customer add-ons and core services.
    """
    m_mean, m_scale = _get_monthly_charges_scale(preprocessor)
    
    X = df.drop(columns="Churn")
    proba = model.predict_proba(X)[:, 1]
    
    df_temp = df.copy()
    df_temp["Churn_Probability"] = proba
    df_temp["MonthlyCharges_unscaled"] = df["MonthlyCharges"] * m_scale + m_mean
    
    services = {
        "Fiber Optic Internet": "InternetService_Fiber optic",
        "DSL Internet": "InternetService_DSL",
        "Online Security Add-on": "OnlineSecurity_Yes",
        "Online Backup Add-on": "OnlineBackup_Yes",
        "Device Protection Add-on": "DeviceProtection_Yes",
        "Tech Support Add-on": "TechSupport_Yes"
    }
    
    report = []
    for display_name, col in services.items():
        if col in df_temp.columns:
            sub_df = df_temp[df_temp[col] > 0.5]
            total_mrr = sub_df["MonthlyCharges_unscaled"].sum()
            expected_mrr_loss = (sub_df["MonthlyCharges_unscaled"] * sub_df["Churn_Probability"]).sum()
            avg_probability = sub_df["Churn_Probability"].mean()
            
            report.append({
                "Service": display_name,
                "Customer Count": int(len(sub_df)),
                "Total MRR": float(total_mrr),
                "Expected MRR Loss": float(expected_mrr_loss),
                "Avg Churn Probability": float(avg_probability)
            })
            
    return pd.DataFrame(report)

def create_revenue_dashboard(df, model, preprocessor, figures_dir):
    """
    Generates and saves a business-facing revenue risk visual dashboard.
    """
    # Load analysis DataFrames
    df_contract = revenue_by_contract(df, model, preprocessor)
    df_segment = revenue_by_segment(df, model, preprocessor)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # 1. Contract-Level expected loss
    sns.barplot(
        data=df_contract,
        x="Contract Type",
        y="Expected MRR Loss",
        hue="Contract Type",
        palette="crest",
        legend=False,
        ax=ax1
    )
    ax1.set_title("Expected MRR Loss by Contract Type", fontsize=12, fontweight="bold")
    ax1.set_xlabel("Contract Type", fontsize=10)
    ax1.set_ylabel("Expected Monthly Revenue Loss ($)", fontsize=10)
    
    # Add values on top of bars
    for p in ax1.patches:
        val = p.get_height()
        ax1.annotate(f"${val:,.0f}", (p.get_x() + p.get_width() / 2., val),
                    ha='center', va='center', xytext=(0, 8), textcoords='offset points', fontsize=9)
                    
    # 2. Segment-Level average churn probability
    sns.barplot(
        data=df_segment.sort_values("Avg Churn Probability", ascending=False).head(5),
        y="Segment",
        x="Avg Churn Probability",
        hue="Segment",
        palette="magma",
        legend=False,
        ax=ax2
    )
    ax2.set_title("Top Churn Risk Customer Segments", fontsize=12, fontweight="bold")
    ax2.set_xlabel("Average Churn Probability", fontsize=10)
    ax2.set_ylabel("Demographic Segment", fontsize=10)
    
    # Format x-axis as percentage
    ax2.xaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.0%}'.format(y)))
    
    plt.suptitle("Telco Churn Revenue Risk Analysis Dashboard", fontsize=16, fontweight="bold", y=1.02)
    plt.tight_layout()
    
    # Save the dashboard figure
    figures_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(figures_dir / "revenue_risk_dashboard.png", dpi=300, facecolor="white", bbox_inches="tight")
    plt.show()
    plt.close()
