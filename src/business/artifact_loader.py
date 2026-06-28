import joblib
import pandas as pd
from src.config.paths import ARTIFACTS_DIR, REPORTS_EXPLAINABILITY_DIR, PROCESSED_DATA_DIR, INTERIM_DATA_DIR

def load_business_artifacts():
    """
    Loads all necessary business and model explainability artifacts, and
    dynamically constructs the unscaled business-level portfolio dataset.
    
    Returns:
        dict: Dictionary containing:
            - 'model': Trained classifier model
            - 'preprocessor': Fit preprocessor pipeline
            - 'feature_importance': Comparative explainability summary DataFrame
            - 'shap_values': Array of SHAP values
            - 'df': Preprocessed dataset DataFrame
            - 'df_business': Unscaled business-level dataset with Churn_Probability and Risk_Segment
    """
    model_path = ARTIFACTS_DIR / "best_model.pkl"
    preprocessor_path = ARTIFACTS_DIR / "preprocessor.pkl"
    explainability_summary_path = REPORTS_EXPLAINABILITY_DIR / "explainability_summary.csv"
    shap_values_path = ARTIFACTS_DIR / "shap_values.pkl"
    processed_dataset_path = PROCESSED_DATA_DIR / "ml_dataset_processed.csv"
    
    model = joblib.load(model_path)
    preprocessor = joblib.load(preprocessor_path)
    feature_importance = pd.read_csv(explainability_summary_path)
    shap_values = joblib.load(shap_values_path)
    df = pd.read_csv(processed_dataset_path)
    
    # Dynamically build df_business from unscaled interim dataset
    df_interim = pd.read_csv(INTERIM_DATA_DIR / "ml_dataset_interim.csv")
    
    # Predict churn probabilities on the processed dataset
    X_processed = df.drop(columns="Churn")
    df_interim["Churn_Probability"] = model.predict_proba(X_processed)[:, 1]
    
    # Assign Risk Segment based on probability thresholds
    def assign_risk_segment(prob):
        if prob > 0.7:
            return "Critical"
        elif prob > 0.4:
            return "At Risk"
        elif prob > 0.2:
            return "Stable"
        else:
            return "Safe"
            
    df_interim["Risk_Segment"] = df_interim["Churn_Probability"].apply(assign_risk_segment)
    
    # Normalize ID column name
    if "customerID" in df_interim.columns:
        df_interim = df_interim.rename(columns={"customerID": "CustomerID"})
        
    df_business = df_interim
    
    return {
        "model": model,
        "preprocessor": preprocessor,
        "feature_importance": feature_importance,
        "shap_values": shap_values,
        "df": df,
        "df_business": df_business
    }
