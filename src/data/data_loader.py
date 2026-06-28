"""
Data Loader Module

Responsible for loading all datasets used in the
Customer Churn Intelligence Platform.
"""

import pandas as pd


def load_ml_dataset(path):
    """
    Load Machine Learning dataset.

    Parameters
    ----------
    path : str or Path
        Path to CSV dataset.

    Returns
    -------
    pandas.DataFrame
    """
    return pd.read_csv(path)


def load_business_dataset(path):
    """
    Load Business Analytics dataset.

    Parameters
    ----------
    path : str or Path
        Path to Excel dataset.

    Returns
    -------
    pandas.DataFrame
    """
    return pd.read_excel(path)


def load_all_datasets(ml_path, business_path):
    """
    Load both datasets.

    Parameters
    ----------
    ml_path : Path
    business_path : Path

    Returns
    -------
    tuple
        (df_ml, df_business)
    """

    df_ml = load_ml_dataset(ml_path)

    df_business = load_business_dataset(business_path)

    return df_ml, df_business


def save_dataset(df, path, file_format="csv"):
    """
    Save a DataFrame to disk.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame to save.
    path : str or Path
        Output file path.
    file_format : str, optional
        Format to save in ('csv' or 'excel'). Default is 'csv'.

    Returns
    -------
    Path
        The path where the file was saved.
    """
    from pathlib import Path

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if file_format == "csv":
        df.to_csv(path, index=False)
    elif file_format == "excel":
        df.to_excel(path, index=False)
    else:
        raise ValueError(f"Unsupported format: {file_format}. Use 'csv' or 'excel'.")

    return path