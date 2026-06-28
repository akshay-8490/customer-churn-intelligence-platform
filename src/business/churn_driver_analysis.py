import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def get_driver_directions(model, feature_names):
    """
    Determines whether each feature increases or decreases churn risk
    based on model coefficients.
    """
    from sklearn.pipeline import Pipeline as SkPipeline
    if isinstance(model, SkPipeline):
        model = model[-1]

    if hasattr(model, "coef_"):
        coefs = model.coef_[0]
        directions = {}
        for feat, coef in zip(feature_names, coefs):
            directions[feat] = "Positive (Increases Churn)" if coef > 0 else "Negative (Reduces Churn)"
        return directions
    else:
        # Default fallback for tree models
        return {feat: "Positive (Increases Churn)" for feat in feature_names}

def top_churn_drivers(feature_importance, model, limit=10):
    """
    Combines feature importance rankings with impact directions.
    """
    df_drivers = feature_importance.copy()
    feature_names = df_drivers["Feature"].tolist()
    directions = get_driver_directions(model, feature_names)
    df_drivers["Direction"] = df_drivers["Feature"].map(directions)
    
    return df_drivers.sort_values("Mean |SHAP Value|", ascending=False).head(limit)

def positive_driver_summary(feature_importance, model, limit=5):
    """
    Lists the top N features that increase customer churn.
    """
    df_drivers = feature_importance.copy()
    feature_names = df_drivers["Feature"].tolist()
    directions = get_driver_directions(model, feature_names)
    df_drivers["Direction"] = df_drivers["Feature"].map(directions)
    
    pos_drivers = df_drivers[df_drivers["Direction"] == "Positive (Increases Churn)"]
    return pos_drivers.sort_values("Mean |SHAP Value|", ascending=False).head(limit)

def negative_driver_summary(feature_importance, model, limit=5):
    """
    Lists the top N features that reduce customer churn.
    """
    df_drivers = feature_importance.copy()
    feature_names = df_drivers["Feature"].tolist()
    directions = get_driver_directions(model, feature_names)
    df_drivers["Direction"] = df_drivers["Feature"].map(directions)
    
    neg_drivers = df_drivers[df_drivers["Direction"] == "Negative (Reduces Churn)"]
    return neg_drivers.sort_values("Mean |SHAP Value|", ascending=False).head(limit)

def driver_category_summary(feature_importance, model):
    """
    Groups features by thematic category and averages their importances.
    """
    df_drivers = feature_importance.copy()
    
    def categorize_feature(feat):
        feat_lower = feat.lower()
        if "contract" in feat_lower:
            return "Contract Term"
        elif "charge" in feat_lower or "spend" in feat_lower:
            return "Charges & Spending"
        elif "gender" in feat_lower or "partner" in feat_lower or "dependent" in feat_lower or "citizen" in feat_lower:
            return "Demographics"
        else:
            return "Services & Add-ons"
            
    df_drivers["Category"] = df_drivers["Feature"].apply(categorize_feature)
    
    return (
        df_drivers
        .groupby("Category")
        .agg(
            Feature_Count=("Feature", "count"),
            Avg_Model_Importance=("Model Importance", "mean"),
            Avg_SHAP_Importance=("Mean |SHAP Value|", "mean"),
            Avg_Perm_Importance=("Permutation Importance", "mean")
        )
        .round(4)
    )

def driver_importance_chart(feature_importance, model, figures_dir):
    """
    Plots a dual-color feature importance chart showing impact direction.
    """
    df_drivers = feature_importance.copy().head(12)
    feature_names = df_drivers["Feature"].tolist()
    directions = get_driver_directions(model, feature_names)
    df_drivers["Direction"] = df_drivers["Feature"].map(directions)
    
    plt.figure(figsize=(10, 6))
    
    # Custom colors for positive vs negative drivers
    palette = {
        "Positive (Increases Churn)": "crimson",
        "Negative (Reduces Churn)": "teal"
    }
    
    sns.barplot(
        data=df_drivers,
        y="Feature",
        x="Mean |SHAP Value|",
        hue="Direction",
        palette=palette,
        dodge=False
    )
    
    plt.title("Top Churn Drivers & Churn Impact Directions (SHAP)", fontsize=14, fontweight="bold")
    plt.xlabel("Mean |SHAP Value| (Importance Magnitude)", fontsize=10)
    plt.ylabel("Feature", fontsize=10)
    plt.legend(title="Direction", loc="lower right")
    plt.tight_layout()
    
    figures_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(figures_dir / "driver_importance_comparison.png", dpi=300, facecolor="white", bbox_inches="tight")
    plt.show()
    plt.close()

def driver_report(feature_importance, model):
    """
    Prints a natural language report of positive and negative drivers.
    """
    pos = positive_driver_summary(feature_importance, model, limit=3)
    neg = negative_driver_summary(feature_importance, model, limit=3)
    
    report = []
    report.append("=" * 70)
    report.append("CHURN DRIVER ANALYSIS REPORT")
    report.append("=" * 70)
    report.append("\nTop 3 Drivers INCREASING Churn Risk:")
    for idx, row in pos.iterrows():
        report.append(f"  - {row['Feature']:<30} (SHAP: {row['Mean |SHAP Value|']:.4f}, Model Rank: {row['Rank_Model']})")
        
    report.append("\nTop 3 Drivers REDUCING Churn Risk (Retention Anchors):")
    for idx, row in neg.iterrows():
        report.append(f"  - {row['Feature']:<30} (SHAP: {row['Mean |SHAP Value|']:.4f}, Model Rank: {row['Rank_Model']})")
    report.append("\n" + "=" * 70)
    
    print("\n".join(report))
