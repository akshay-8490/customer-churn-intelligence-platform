import pandas as pd
import numpy as np
from pathlib import Path


def prepare_dashboard_dataset(df_business):
    """
    Consolidates all enriched business columns into a single clean dashboard-ready
    DataFrame. Selects and reorders columns for downstream consumption by Streamlit,
    Power BI, or any other BI tool.

    Expects df_business to already contain columns appended by:
      - artifact_loader   (Churn_Probability, Risk_Segment)
      - customer_personas (Persona, Cluster)
      - retention_engine  (Priority_Score, Retention_Action, Estimated_Action_Cost)

    Returns:
        pd.DataFrame: Dashboard-ready dataset with standardised column order.
    """
    df = df_business.copy()

    # Standardise ID column
    if "customerID" in df.columns:
        df = df.rename(columns={"customerID": "CustomerID"})

    # Define the preferred column order (present columns only)
    preferred_order = [
        # Identity
        "CustomerID",
        # Demographics
        "gender", "SeniorCitizen", "Partner", "Dependents",
        # Account
        "tenure", "Contract", "PaperlessBilling", "PaymentMethod",
        # Services
        "PhoneService", "MultipleLines", "InternetService",
        "OnlineSecurity", "OnlineBackup", "DeviceProtection",
        "TechSupport", "StreamingTV", "StreamingMovies",
        # Financials
        "MonthlyCharges", "TotalCharges",
        # Target
        "Churn",
        # ML Enrichments
        "Churn_Probability", "Risk_Segment",
        # Clustering
        "Persona",
        # Retention Engine
        "Priority_Score", "Retention_Action", "Estimated_Action_Cost",
    ]

    # Keep only columns that actually exist in the dataframe
    ordered_cols = [c for c in preferred_order if c in df.columns]

    # Append any remaining columns not in the preferred list
    remaining = [c for c in df.columns if c not in ordered_cols]
    ordered_cols.extend(remaining)

    df = df[ordered_cols]

    # Round numeric enrichment columns for cleanliness
    for col in ["Churn_Probability", "Priority_Score", "Estimated_Action_Cost"]:
        if col in df.columns:
            df[col] = df[col].round(4)

    return df


def dashboard_summary(df_dashboard):
    """
    Prints a concise statistical overview of the dashboard dataset,
    including row/column counts, enrichment coverage, and risk distributions.
    """
    rows, cols = df_dashboard.shape

    report = []
    report.append("=" * 70)
    report.append("DASHBOARD DATASET EXPORT SUMMARY")
    report.append("=" * 70)
    report.append(f"\n  Total Records        : {rows:,}")
    report.append(f"  Total Columns        : {cols}")

    # Enrichment coverage checks
    enrichments = {
        "Churn_Probability": "ML Churn Probability",
        "Risk_Segment":      "Risk Segment",
        "Persona":           "Customer Persona",
        "Retention_Action":  "Retention Action",
        "Priority_Score":    "Priority Score",
    }
    report.append("\n  Enrichment Coverage:")
    for col, label in enrichments.items():
        if col in df_dashboard.columns:
            non_null = df_dashboard[col].notna().sum()
            pct = non_null / rows
            report.append(f"    - {label:<25}: {non_null:,} / {rows:,} ({pct:.1%})")
        else:
            report.append(f"    - {label:<25}: NOT PRESENT")

    # Risk segment distribution
    if "Risk_Segment" in df_dashboard.columns:
        report.append("\n  Risk Segment Distribution:")
        for seg in ["Critical", "At Risk", "Stable", "Safe"]:
            count = (df_dashboard["Risk_Segment"] == seg).sum()
            pct = count / rows
            report.append(f"    - {seg:<12}: {count:>5,} customers ({pct:.1%})")

    # Persona distribution
    if "Persona" in df_dashboard.columns:
        report.append("\n  Persona Distribution:")
        for persona, count in df_dashboard["Persona"].value_counts().items():
            pct = count / rows
            report.append(f"    - {persona:<35}: {count:>5,} ({pct:.1%})")

    report.append("\n" + "=" * 70)
    print("\n".join(report))


def export_dashboard_dataset(df_dashboard, export_dir, filename="dashboard_dataset.csv"):
    """
    Exports the dashboard-ready DataFrame to CSV in the specified directory.

    Args:
        df_dashboard: The prepared dashboard DataFrame.
        export_dir: Path (or str) to the export directory.
        filename: Output CSV filename (default: dashboard_dataset.csv).

    Returns:
        Path: The absolute path of the exported file.
    """
    export_dir = Path(export_dir)
    export_dir.mkdir(parents=True, exist_ok=True)

    export_path = export_dir / filename
    df_dashboard.to_csv(export_path, index=False)

    print(f"✅ Dashboard dataset exported successfully.")
    print(f"   Path     : {export_path}")
    print(f"   Records  : {len(df_dashboard):,}")
    print(f"   Columns  : {df_dashboard.shape[1]}")
    print(f"   File Size: {export_path.stat().st_size / 1024:.1f} KB")

    return export_path
