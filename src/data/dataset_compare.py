"""
Dataset Comparison Module
Project: Customer Churn Intelligence Platform
Description: Contains functions to compare structure and schemas of multiple
             datasets without side-effects (visual display/print).
"""

# Standard Library
from dataclasses import dataclass
from typing import List

# Third Party
import pandas as pd


@dataclass
class DatasetComparisonReport:
    """
    Comparison metrics for common and unique columns between two datasets.
    """
    common: List[str]
    only_df1: List[str]
    only_df2: List[str]


# ==========================================================
# Dataset Comparison
# ==========================================================

def compare_datasets(
    df1: pd.DataFrame,
    df2: pd.DataFrame
) -> DatasetComparisonReport:
    """
    Compare column structures of two datasets.

    Identifies common columns and columns unique to each dataset.

    Parameters
    ----------
    df1 : pandas.DataFrame
        First dataset.
    df2 : pandas.DataFrame
        Second dataset.

    Returns
    -------
    DatasetComparisonReport
        Dataclass containing list of common, only df1, and only df2 columns.
    """
    cols1 = set(df1.columns)
    cols2 = set(df2.columns)

    common = sorted(cols1.intersection(cols2))
    only_df1 = sorted(cols1 - cols2)
    only_df2 = sorted(cols2 - cols1)

    return DatasetComparisonReport(
        common=common,
        only_df1=only_df1,
        only_df2=only_df2
    )
