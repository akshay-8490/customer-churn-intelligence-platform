import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def build_customer_personas(df_business):
    """
    Fits a K-Means model to discover natural customer groups,
    labels them dynamically, and appends the 'Persona' column to df_business.
    """
    feat_cols = ['tenure', 'MonthlyCharges', 'TotalCharges', 'Churn_Probability']
    X_cluster = df_business[feat_cols].copy()
    
    # Safe fallback for any null values
    X_cluster = X_cluster.fillna(0)
    
    # Scale features for K-Means sensitivity
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_cluster)
    
    # Fit K-Means
    km = KMeans(n_clusters=4, random_state=42, n_init=10)
    clusters = km.fit_predict(X_scaled)
    
    df_temp = df_business.copy()
    df_temp["Cluster"] = clusters
    
    # Calculate group averages to map business-friendly names dynamically
    means = df_temp.groupby("Cluster")[feat_cols].mean()
    
    cluster_mapping = {}
    
    # 1. Loyal Long-Term: Highest TotalCharges
    loyal_cluster = means["TotalCharges"].idxmax()
    cluster_mapping[loyal_cluster] = "Loyal Long-Term Customers"
    
    # 2. High-Value At-Risk: Highest Churn_Probability among remaining
    remaining = [c for c in [0, 1, 2, 3] if c != loyal_cluster]
    high_value_at_risk_cluster = means.loc[remaining, "Churn_Probability"].idxmax()
    cluster_mapping[high_value_at_risk_cluster] = "High-Value At-Risk Customers"
    
    # 3. New Price-Sensitive: Lowest MonthlyCharges among remaining
    remaining2 = [c for c in remaining if c != high_value_at_risk_cluster]
    new_price_cluster = means.loc[remaining2, "MonthlyCharges"].idxmin()
    cluster_mapping[new_price_cluster] = "New Price-Sensitive Customers"
    
    # 4. Stable Family Customers: The last remaining cluster
    last_cluster = [c for c in remaining2 if c != new_price_cluster][0]
    cluster_mapping[last_cluster] = "Stable Family Customers"
    
    df_temp["Persona"] = df_temp["Cluster"].map(cluster_mapping)
    return df_temp

def persona_distribution(df_business):
    """
    Returns counts and percentages for each customer persona.
    """
    if "Persona" not in df_business.columns:
        df_business = build_customer_personas(df_business)
        
    counts = df_business["Persona"].value_counts()
    pcts = df_business["Persona"].value_counts(normalize=True) * 100
    
    return pd.DataFrame({
        "Persona": counts.index,
        "Customer Count": counts.values,
        "Percentage (%)": pcts.values.round(2)
    })

def persona_summary(df_business):
    """
    Returns mean metrics grouped by customer persona.
    """
    if "Persona" not in df_business.columns:
        df_business = build_customer_personas(df_business)
        
    return (
        df_business
        .groupby("Persona")
        .agg(
            Customer_Count=("CustomerID", "count"),
            Avg_Tenure_Months=("tenure", "mean"),
            Avg_Monthly_Charges=("MonthlyCharges", "mean"),
            Avg_Total_Charges=("TotalCharges", "mean"),
            Avg_Churn_Probability=("Churn_Probability", "mean")
        )
        .round(2)
    )

def persona_dashboard(df_business, figures_dir):
    """
    Plots a multi-panel visual box/bar dashboard representing customer personas.
    """
    if "Persona" not in df_business.columns:
        df_business = build_customer_personas(df_business)
        
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. Persona Volume
    sns.countplot(
        data=df_business,
        y="Persona",
        hue="Persona",
        palette="viridis",
        legend=False,
        ax=ax1
    )
    ax1.set_title("Customer Volume by Persona", fontsize=12, fontweight="bold")
    ax1.set_xlabel("Customer Count")
    ax1.set_ylabel("Persona")
    
    # 2. Tenure distribution
    sns.boxplot(
        data=df_business,
        x="tenure",
        y="Persona",
        hue="Persona",
        palette="mako",
        legend=False,
        ax=ax2
    )
    ax2.set_title("Tenure Months by Persona", fontsize=12, fontweight="bold")
    ax2.set_xlabel("Tenure (Months)")
    ax2.set_ylabel("")
    
    # 3. Monthly Charges distribution
    sns.boxplot(
        data=df_business,
        x="MonthlyCharges",
        y="Persona",
        hue="Persona",
        palette="crest",
        legend=False,
        ax=ax3
    )
    ax3.set_title("Monthly Charges by Persona", fontsize=12, fontweight="bold")
    ax3.set_xlabel("Monthly Charges ($)")
    ax3.set_ylabel("Persona")
    
    # 4. Churn Risk distribution
    sns.boxplot(
        data=df_business,
        x="Churn_Probability",
        y="Persona",
        hue="Persona",
        palette="magma",
        legend=False,
        ax=ax4
    )
    ax4.set_title("Churn Risk by Persona", fontsize=12, fontweight="bold")
    ax4.set_xlabel("Churn Probability")
    ax4.set_ylabel("")
    ax4.xaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.0%}'.format(y)))
    
    plt.suptitle("Telco Customer Personas Analysis Dashboard", fontsize=16, fontweight="bold", y=1.02)
    plt.tight_layout()
    
    figures_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(figures_dir / "customer_persona_dashboard.png", dpi=300, facecolor="white", bbox_inches="tight")
    plt.show()
    plt.close()

def persona_report(df_business):
    """
    Prints a strategic business report of the segments and retention suggestions.
    """
    summary = persona_summary(df_business)
    total_cust = len(df_business)
    
    report = []
    report.append("=" * 75)
    report.append("CUSTOMER PERSONAS EXECUTIVE REPORT (DATA-DRIVEN CLUSTERING)")
    report.append("=" * 75)
    report.append("\nSummary of Natural Customer Segments Discovered:")
    
    for persona, row in summary.iterrows():
        pct = row['Customer_Count'] / total_cust
        report.append(f"\n* Persona: {persona}")
        report.append(f"  - Size: {int(row['Customer_Count'])} customers ({pct:.1%})")
        report.append(f"  - Average Tenure: {row['Avg_Tenure_Months']:.1f} months")
        report.append(f"  - Average Monthly Spending: ${row['Avg_Monthly_Charges']:.2f}")
        report.append(f"  - Average Total Charges: ${row['Avg_Total_Charges']:.2f}")
        report.append(f"  - Churn Risk Level: {row['Avg_Churn_Probability']:.1%}")
        
        # Strategic recommendations
        if "At-Risk" in persona:
            report.append("  - Strategy: Target with high-priority proactive retention, price freezes, and service guarantees.")
        elif "Long-Term" in persona:
            report.append("  - Strategy: Target with loyalty rewards, cross-sell/up-sell premium services, and long-term extensions.")
        elif "Price-Sensitive" in persona:
            report.append("  - Strategy: Offer flexible basic plans, discount bundles, or contract upgrade incentives.")
        elif "Stable" in persona:
            report.append("  - Strategy: Maintain service reliability, offer annual review checks, and ensure stable billing.")
            
    report.append("\n" + "=" * 75)
    print("\n".join(report))
