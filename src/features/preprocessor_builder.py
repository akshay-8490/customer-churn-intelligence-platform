"""
Preprocessor Builder Module
Project: Customer Churn Intelligence Platform
Description: Constructs and applies sklearn preprocessing pipelines
             (StandardScaler + OneHotEncoder via ColumnTransformer).
"""

import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


def identify_feature_types(X):
    """
    Splits feature columns into numerical and categorical lists.

    Returns:
        tuple: (numerical_features, categorical_features)
    """
    numerical_features = X.select_dtypes(
        include=["int64", "float64"]
    ).columns.tolist()

    categorical_features = X.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    return numerical_features, categorical_features


def build_preprocessor(numerical_features, categorical_features):
    """
    Constructs a ColumnTransformer with:
        - StandardScaler for numerical features
        - OneHotEncoder (handle_unknown='ignore') for categorical features

    Returns:
        sklearn.compose.ColumnTransformer
    """
    numeric_transformer = Pipeline(
        steps=[("scaler", StandardScaler())]
    )

    categorical_transformer = Pipeline(
        steps=[
            (
                "onehot",
                OneHotEncoder(
                    handle_unknown="ignore",
                    sparse_output=False
                )
            )
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("numerical", numeric_transformer, numerical_features),
            ("categorical", categorical_transformer, categorical_features)
        ],
        remainder="drop"
    )

    return preprocessor


def get_feature_names(preprocessor, categorical_features):
    """
    Recovers the full list of feature names after preprocessing,
    combining the numerical pass-through names with the OneHotEncoder output names.

    Must be called after fit_transform.

    Returns:
        list[str]: Ordered feature names matching the processed matrix columns.
    """
    # Numerical features keep their original names
    numerical_features = next(
        t[2] for t in preprocessor.transformers_ if t[0] == "numerical"
    )
    if isinstance(numerical_features, list):
        num_names = numerical_features
    else:
        num_names = list(numerical_features)

    # Categorical features are expanded by OneHotEncoder
    encoded_names = (
        preprocessor.named_transformers_["categorical"]
        .named_steps["onehot"]
        .get_feature_names_out(categorical_features)
        .tolist()
    )

    return num_names + encoded_names


def apply_preprocessor(df_fe, target_column, drop_columns=None):
    """
    Full pipeline: separate X/y, build preprocessor, fit_transform,
    recover feature names, and return the processed DataFrame + fitted preprocessor.

    Args:
        df_fe: DataFrame with all engineered features.
        target_column: Name of the target column to separate.
        drop_columns: Optional list of columns to drop before preprocessing
                      (e.g. binned columns that cause collinearity).

    Returns:
        tuple: (df_processed, preprocessor)
            - df_processed: pd.DataFrame with processed features + target
            - preprocessor: fitted ColumnTransformer
    """
    columns_to_drop = [target_column]
    if drop_columns:
        columns_to_drop.extend(drop_columns)

    X = df_fe.drop(columns=columns_to_drop)
    
    # Auto-drop customer ID columns if present to prevent dimension explosion
    id_cols = [c for c in ["customerID", "CustomerID"] if c in X.columns]
    if id_cols:
        X = X.drop(columns=id_cols)

    y = df_fe[target_column]

    numerical_features, categorical_features = identify_feature_types(X)

    preprocessor = build_preprocessor(numerical_features, categorical_features)

    X_processed = preprocessor.fit_transform(X)

    all_feature_names = get_feature_names(preprocessor, categorical_features)

    assert len(all_feature_names) == X_processed.shape[1], (
        f"Feature name count ({len(all_feature_names)}) does not match "
        f"processed matrix column count ({X_processed.shape[1]})!"
    )

    df_processed = pd.DataFrame(
        X_processed,
        columns=all_feature_names,
        index=df_fe.index
    )

    df_processed[target_column] = y.values

    return df_processed, preprocessor
