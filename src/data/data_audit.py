"""
Data Audit Module
Project: Customer Churn Intelligence Platform
Description: Contains clean, testable data audit analysis functions. None of
             these functions print output or render visualizations directly.
             All presentational display is delegated to notebooks or UI applications.
"""

# Standard Library
from dataclasses import dataclass
from typing import List

# Third Party
import numpy as np
import pandas as pd

# Local
from src.config.settings import TARGET_COLUMN


@dataclass
class DatasetOverviewReport:
    """
    Summary metrics of a dataset's basic dimensions, column list, and types.
    """
    metrics_df: pd.DataFrame
    columns: List[str]
    dtypes: pd.Series


@dataclass
class DuplicateReport:
    """
    Summary count and percentage of duplicate rows.
    """
    count: int
    percentage: float


@dataclass
class FeatureSummaryReport:
    """
    Categorical and numerical features breakdown.
    """
    summary_df: pd.DataFrame
    categorical_cols: List[str]
    numerical_cols: List[str]


@dataclass
class TargetSummary:
    """
    Target variable counts, percentages, class imbalance ratio, and imbalance status.
    """
    counts: pd.Series
    percentages: pd.Series
    imbalance_ratio: float
    status: str


@dataclass
class StatisticalSummaryReport:
    """
    Statistical describe matrices for numerical and categorical variables.
    """
    numerical: pd.DataFrame
    categorical: pd.DataFrame


# ==========================================================
# Dataset Overview
# ==========================================================

def dataset_overview(df: pd.DataFrame) -> DatasetOverviewReport:
    """
    Generate basic shapes and summary stats for a dataset.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset to analyze.

    Returns
    -------
    DatasetOverviewReport
        Object containing the summary dataframe, column list, and types.
    """
    memory_kb = df.memory_usage(deep=True).sum() / 1024

    metrics_df = pd.DataFrame({
        "Metric": [
            "Rows",
            "Columns",
            "Categorical Features",
            "Numerical Features",
            "Memory Usage (KB)"
        ],
        "Value": [
            df.shape[0],
            df.shape[1],
            df.select_dtypes(include="object").shape[1],
            df.select_dtypes(include=np.number).shape[1],
            f"{memory_kb:.2f}"
        ]
    })

    return DatasetOverviewReport(
        metrics_df=metrics_df,
        columns=df.columns.tolist(),
        dtypes=df.dtypes
    )


# ==========================================================
# Missing Value Analysis
# ==========================================================

def missing_value_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze missing values in a dataset.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset to analyze.

    Returns
    -------
    pandas.DataFrame
        DataFrame with missing value counts and percentages
        (only columns with missing values, sorted descending).
    """
    missing = df.isnull().sum()
    missing_percent = (missing / len(df)) * 100

    missing_df = pd.DataFrame({
        "Missing Values": missing,
        "Percentage (%)": missing_percent
    })

    missing_df = missing_df[missing_df["Missing Values"] > 0]
    missing_df = missing_df.sort_values(by="Missing Values", ascending=False)

    return missing_df


# ==========================================================
# Duplicate Analysis
# ==========================================================

def duplicate_analysis(df: pd.DataFrame) -> DuplicateReport:
    """
    Analyze duplicate records in a dataset.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset to analyze.

    Returns
    -------
    DuplicateReport
        Dataclass containing duplicate count and percentage.
    """
    count = int(df.duplicated().sum())
    percentage = (count / len(df)) * 100 if len(df) > 0 else 0.0

    return DuplicateReport(count=count, percentage=percentage)


# ==========================================================
# Feature Summary
# ==========================================================

def feature_summary(df: pd.DataFrame) -> FeatureSummaryReport:
    """
    Summarize feature types in a dataset.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset to analyze.

    Returns
    -------
    FeatureSummaryReport
        Dataclass containing lists of features and metrics.
    """
    categorical = df.select_dtypes(include="object").columns.tolist()
    numerical = df.select_dtypes(include=np.number).columns.tolist()

    summary_df = pd.DataFrame({
        "Metric": ["Total Features", "Categorical", "Numerical"],
        "Value": [df.shape[1], len(categorical), len(numerical)]
    })

    return FeatureSummaryReport(
        summary_df=summary_df,
        categorical_cols=categorical,
        numerical_cols=numerical
    )


# ==========================================================
# Target Variable Summary
# ==========================================================

def target_summary(df: pd.DataFrame, target_col: str = TARGET_COLUMN) -> TargetSummary:
    """
    Analyze the target variable distribution and class imbalance.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset containing the target column.
    target_col : str, optional
        Name of the target column. Default is imported TARGET_COLUMN.

    Returns
    -------
    TargetSummary
        Dataclass containing targets counts, percentages, ratio, and status.
    """
    target_counts = df[target_col].value_counts()
    target_percent = df[target_col].value_counts(normalize=True).mul(100).round(2)

    majority = target_counts.max()
    minority = target_counts.min()
    imbalance_ratio = round(float(majority / minority), 2) if minority > 0 else 0.0

    if imbalance_ratio < 1.5:
        status = "Balanced"
    elif imbalance_ratio < 3.0:
        status = "Moderately Imbalanced"
    else:
        status = "Highly Imbalanced"

    return TargetSummary(
        counts=target_counts,
        percentages=target_percent,
        imbalance_ratio=imbalance_ratio,
        status=status
    )


# ==========================================================
# Statistical Summary
# ==========================================================

def statistical_summary(df: pd.DataFrame) -> StatisticalSummaryReport:
    """
    Generate numerical and categorical descriptive statistics.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset to summarize.

    Returns
    -------
    StatisticalSummaryReport
        Dataclass with separate numerical and categorical summary matrices.
    """
    numerical_stats = df.describe()
    
    if df.select_dtypes(include="object").shape[1] > 0:
        categorical_stats = df.describe(include="object")
    else:
        categorical_stats = pd.DataFrame()

    return StatisticalSummaryReport(
        numerical=numerical_stats,
        categorical=categorical_stats
    )


# ==========================================================
# Unique Value Summary
# ==========================================================

def unique_value_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Show data types, unique value counts, and missing values per column.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset to analyze.

    Returns
    -------
    pandas.DataFrame
        Summary with Data Type, Unique Values, and Missing Values.
    """
    summary = pd.DataFrame({
        "Data Type": df.dtypes,
        "Unique Values": df.nunique(),
        "Missing Values": df.isnull().sum()
    })

    return summary


# ==========================================================
# Data Quality Report
# ==========================================================

def data_quality_report(df_ml: pd.DataFrame, df_business: pd.DataFrame) -> pd.DataFrame:
    """
    Generate a consolidated data quality report for both datasets.

    Parameters
    ----------
    df_ml : pandas.DataFrame
        Machine learning dataset.
    df_business : pandas.DataFrame
        Business analytics dataset.

    Returns
    -------
    pandas.DataFrame
        Quality metrics for both datasets.
    """
    report = pd.DataFrame({
        "Metric": [
            "ML Dataset Rows",
            "ML Dataset Columns",
            "Business Dataset Rows",
            "Business Dataset Columns",
            "Duplicate Rows (ML)",
            "Duplicate Rows (Business)",
            "Missing Values (ML)",
            "Missing Values (Business)"
        ],
        "Value": [
            df_ml.shape[0],
            df_ml.shape[1],
            df_business.shape[0],
            df_business.shape[1],
            int(df_ml.duplicated().sum()),
            int(df_business.duplicated().sum()),
            int(df_ml.isnull().sum().sum()),
            int(df_business.isnull().sum().sum())
        ]
    })

    return report
