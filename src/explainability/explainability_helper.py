"""
Explainability Helper Module
Project: Customer Churn Intelligence Platform
Description: Helper functions for global feature importance extraction,
             Tree vs Linear SHAP explainer wrappers, local explanation builders,
             and permutation importance.
"""

import numpy as np
import pandas as pd
import shap
from sklearn.inspection import permutation_importance


def calculate_model_importance(model, feature_names):
    """
    Computes or extracts global model feature importances.
    Falls back to absolute value of coefficients if model is a linear classifier.
    """
    from sklearn.pipeline import Pipeline as SkPipeline
    if isinstance(model, SkPipeline):
        model = model[-1]

    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
    elif hasattr(model, "coef_"):
        importances = np.abs(model.coef_[0])
    else:
        importances = np.zeros(len(feature_names))

    importance_df = pd.DataFrame({
        "Feature": feature_names,
        "Importance": importances
    }).sort_values("Importance", ascending=False)
    
    return importance_df


def compute_shap_explanations(model, X_processed):
    """
    Initializes the appropriate SHAP explainer (Linear vs Tree)
    and computes modern Explanation objects.
    """
    from sklearn.pipeline import Pipeline as SkPipeline
    if isinstance(model, SkPipeline):
        model = model[-1]

    if hasattr(model, "coef_"):
        explainer = shap.LinearExplainer(model, X_processed)
    else:
        explainer = shap.TreeExplainer(model)

    explanation = explainer(X_processed)
    return explainer, explanation


def extract_shap_importance(explanation, feature_names):
    """
    Extracts mean absolute SHAP values across all customers and returns
    a sorted DataFrame.
    """
    if len(explanation.shape) == 3:
        values = explanation.values[:, :, 1]
    else:
        values = explanation.values

    mean_abs_shap = np.mean(np.abs(values), axis=0)
    
    shap_df = pd.DataFrame({
        "Feature": feature_names,
        "Mean |SHAP Value|": mean_abs_shap
    }).sort_values("Mean |SHAP Value|", ascending=False)
    
    return shap_df


def compute_permutation_importance(model, X_processed, y, random_state=42):
    """
    Computes permutation feature importance on the processed dataset.
    """
    result = permutation_importance(
        model, X_processed, y,
        n_repeats=10,
        random_state=random_state,
        n_jobs=-1
    )
    
    perm_df = pd.DataFrame({
        "Feature": X_processed.columns,
        "Importance Mean": result.importances_mean,
        "Importance Std": result.importances_std
    }).sort_values("Importance Mean", ascending=False)
    
    return perm_df


def generate_comparative_summary(model_importance, shap_importance, permutation_importance=None):
    """
    Merges model, SHAP, and permutation importances and ranks them.
    """
    summary = model_importance.copy()
    summary = summary.rename(columns={"Importance": "Model Importance"})
    summary["Rank_Model"] = summary["Model Importance"].rank(ascending=False, method="min").astype(int)

    shap_copy = shap_importance.copy()
    summary = summary.merge(shap_copy, on="Feature", how="left")
    summary["Rank_SHAP"] = summary["Mean |SHAP Value|"].rank(ascending=False, method="min").astype(int)

    if permutation_importance is not None:
        perm_copy = permutation_importance.copy().rename(columns={"Importance Mean": "Permutation Importance"})
        # Drop Std column if present
        if "Importance Std" in perm_copy.columns:
            perm_copy = perm_copy.drop(columns=["Importance Std"])
        summary = summary.merge(perm_copy, on="Feature", how="left")
        summary["Rank_Permutation"] = summary["Permutation Importance"].rank(ascending=False, method="min").astype(int)

    return summary


def generate_local_explanation(sample_index, model, X_processed, explanation):
    """
    Generates a natural-language profile description detailing positive
    and negative contributors to churn risk for a specific customer.
    """
    sample_row = X_processed.iloc[sample_index]
    pred_prob = model.predict_proba(X_processed.iloc[[sample_index]])[0, 1]

    if len(explanation.shape) == 3:
        shap_values = explanation.values[sample_index, :, 1]
    else:
        shap_values = explanation.values[sample_index]

    contrib = pd.DataFrame({
        "Feature": X_processed.columns,
        "Value": sample_row.values,
        "SHAP_Value": shap_values
    })

    # Top drivers increasing vs decreasing risk
    positive = contrib[contrib["SHAP_Value"] > 0].sort_values("SHAP_Value", ascending=False).head(4)
    negative = contrib[contrib["SHAP_Value"] < 0].sort_values("SHAP_Value", ascending=True).head(4)

    lines = []
    lines.append(f"Customer Index: {sample_index}")
    lines.append(f"Predicted Churn Probability: {pred_prob:.1%}")
    lines.append("\nStrongest Churn Risk Drivers (Increase Risk):")
    for _, row in positive.iterrows():
        # Check if float to format nicely
        val_str = f"{row['Value']:.4f}" if isinstance(row["Value"], (float, np.floating)) else str(row["Value"])
        lines.append(f"  - {row['Feature']:<25}: {val_str:<10} (SHAP impact: +{row['SHAP_Value']:.4f})")

    lines.append("\nStrongest Retention Anchors (Decrease Risk):")
    for _, row in negative.iterrows():
        val_str = f"{row['Value']:.4f}" if isinstance(row["Value"], (float, np.floating)) else str(row["Value"])
        lines.append(f"  - {row['Feature']:<25}: {val_str:<10} (SHAP impact: {row['SHAP_Value']:.4f})")

    return "\n".join(lines)
