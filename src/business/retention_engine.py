import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def generate_recommendations(df_business):
    """
    Analyzes customer profiles to generate action-oriented retention recommendations,
    priority scores, and estimated action costs.
    """
    df_temp = df_business.copy()
    
    # Priority Score = MonthlyCharges * Churn_Probability
    df_temp["Priority_Score"] = (df_temp["MonthlyCharges"] * df_temp["Churn_Probability"]).round(2)
    
    recommendations = []
    action_costs = []
    
    for idx, row in df_temp.iterrows():
        prob = row["Churn_Probability"]
        contract = row.get("Contract")
        internet = row.get("InternetService")
        
        # Determine strategy based on churn risk and customer profile
        if prob > 0.7:
            if contract == "Month-to-month" or contract == "Month-to-Month":
                action = "Outbound Call: Offer 1-Yr Upgrade & $15/mo discount"
                cost = 15.0
            else:
                action = "Executive Call: Offer $15 loyalty credit"
                cost = 15.0
        elif prob > 0.4:
            if internet == "Fiber optic" or internet == "Fiber Optic":
                action = "Support Outreach: Offer 3-Mo Tech Support trial"
                cost = 5.0
            else:
                action = "Account Review: Offer basic plan optimization"
                cost = 0.0
        else:
            action = "Loyalty Engagement: Send thank-you summary email"
            cost = 0.0
            
        recommendations.append(action)
        action_costs.append(cost)
        
    df_temp["Retention_Action"] = recommendations
    df_temp["Estimated_Action_Cost"] = action_costs
    return df_temp

def recommendation_summary(df_business):
    """
    Groups recommendations by Retention Action and sums cost vs. priority score.
    """
    if "Retention_Action" not in df_business.columns:
        df_business = generate_recommendations(df_business)
        
    return (
        df_business
        .groupby("Retention_Action")
        .agg(
            Customers=("CustomerID", "count"),
            Avg_Churn_Probability=("Churn_Probability", "mean"),
            Total_Monthly_Charges=("MonthlyCharges", "sum"),
            Total_Priority_Score=("Priority_Score", "sum"),  # Expected MRR saved
            Total_Action_Cost=("Estimated_Action_Cost", "sum")
        )
        .round(2)
    )

def high_priority_customers(df_business, limit=10):
    """
    Returns the top N high-priority customers for outbound outreach.
    """
    if "Retention_Action" not in df_business.columns:
        df_business = generate_recommendations(df_business)
        
    high_priority = (
        df_business
        .sort_values(by="Priority_Score", ascending=False)
        .head(limit)
    )
    
    cols = [
        "CustomerID",
        "tenure",
        "MonthlyCharges",
        "Churn_Probability",
        "Risk_Segment",
        "Persona",
        "Priority_Score",
        "Retention_Action"
    ]
    return high_priority[cols]

def recommendation_dashboard(df_business, figures_dir):
    """
    Plots target volumes and expected revenue saved vs outreach cost.
    """
    if "Retention_Action" not in df_business.columns:
        df_business = generate_recommendations(df_business)
        
    summary = recommendation_summary(df_business).reset_index()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # 1. Customer Count by Action
    sns.barplot(
        data=summary,
        y="Retention_Action",
        x="Customers",
        hue="Retention_Action",
        palette="viridis",
        legend=False,
        ax=ax1
    )
    ax1.set_title("Target Customers by Campaign Action", fontsize=12, fontweight="bold")
    ax1.set_xlabel("Customer Count")
    ax1.set_ylabel("")
    
    # 2. Expected MRR Saved (Priority Score) vs Cost Comparison
    summary_melted = summary.melt(
        id_vars="Retention_Action",
        value_vars=["Total_Priority_Score", "Total_Action_Cost"],
        var_name="Financial_Metric",
        value_name="Value"
    )
    
    sns.barplot(
        data=summary_melted,
        y="Retention_Action",
        x="Value",
        hue="Financial_Metric",
        palette="crest",
        ax=ax2
    )
    ax2.set_title("Financial Impact: Expected Revenue Saved vs. Campaign Cost", fontsize=12, fontweight="bold")
    ax2.set_xlabel("Total Amount ($)")
    ax2.set_ylabel("")
    ax2.legend(title="Metric", labels=["Expected MRR Saved", "Estimated Outreach Cost"])
    
    plt.suptitle("Telco Retention Engine Strategy Dashboard", fontsize=16, fontweight="bold", y=1.02)
    plt.tight_layout()
    
    figures_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(figures_dir / "retention_engine_dashboard.png", dpi=300, facecolor="white", bbox_inches="tight")
    plt.show()
    plt.close()

def recommendation_report(df_business):
    """
    Prints a natural-language campaign ROI report.
    """
    if "Retention_Action" not in df_business.columns:
        df_business = generate_recommendations(df_business)
        
    summary = recommendation_summary(df_business)
    
    total_customers = len(df_business)
    total_saved = df_business["Priority_Score"].sum()
    total_cost = df_business["Estimated_Action_Cost"].sum()
    roi = (total_saved / total_cost) if total_cost > 0 else 0.0
    
    report = []
    report.append("=" * 75)
    report.append("RETENTION ENGINE SYSTEM CAMPAIGN STRATEGY REPORT")
    report.append("=" * 75)
    report.append(f"\nOverall Campaign Summary:")
    report.append(f"  - Total Target Customers: {total_customers} accounts")
    report.append(f"  - Expected MRR at Risk (Total Saved potential): ${total_saved:,.2f}")
    report.append(f"  - Estimated Retention Campaign Budget: ${total_cost:,.2f}")
    report.append(f"  - Estimated ROI: {roi:.2f}x (MRR Saved per Dollar Spent)")
    
    report.append("\nBreakdown by Recommended Campaign Action:")
    for action, row in summary.iterrows():
        pct = row['Customers'] / total_customers
        report.append(f"\n* Action: {action}")
        report.append(f"  - Target Accounts: {int(row['Customers'])} customers ({pct:.1%})")
        report.append(f"  - Avg Churn Risk of Group: {row['Avg_Churn_Probability']:.1%}")
        report.append(f"  - Expected MRR Saved: ${row['Total_Priority_Score']:,.2f}")
        report.append(f"  - Action Cost Budget: ${row['Total_Action_Cost']:,.2f}")
        
    report.append("\n" + "=" * 75)
    print("\n".join(report))
