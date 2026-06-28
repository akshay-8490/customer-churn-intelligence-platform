"""
Data Visualization Module

Plotting functions for data understanding and EDA.
Reusable across notebooks and Streamlit.
"""

import matplotlib.pyplot as plt
import seaborn as sns


# ==========================================================
# Missing Value Heatmap
# ==========================================================

def plot_missing_heatmap(df, title="Missing Values Heatmap", figsize=(16, 6)):
    """
    Plot a heatmap of missing values.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset to visualize.
    title : str, optional
        Plot title.
    figsize : tuple, optional
        Figure size. Default is (16, 6).
    """
    plt.figure(figsize=figsize)

    sns.heatmap(
        df.isnull(),
        cbar=False,
        cmap="viridis"
    )

    plt.title(title, fontsize=14)

    plt.tight_layout()
    plt.show()


# ==========================================================
# Target Distribution Count Plot
# ==========================================================

def plot_target_distribution(df, target_col="Churn", palette="Set2",
                             figsize=(8, 5)):
    """
    Plot a count plot of the target variable.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset containing the target column.
    target_col : str, optional
        Name of the target column. Default is 'Churn'.
    palette : str, optional
        Seaborn color palette. Default is 'Set2'.
    figsize : tuple, optional
        Figure size. Default is (8, 5).
    """
    plt.figure(figsize=figsize)

    ax = sns.countplot(
        data=df,
        x=target_col,
        palette=palette
    )

    # Add value labels
    for container in ax.containers:
        ax.bar_label(container)

    plt.title("Customer Churn Distribution", fontsize=14)
    plt.xlabel(target_col)
    plt.ylabel("Number of Customers")

    plt.tight_layout()
    plt.show()


# ==========================================================
# Target Pie Chart
# ==========================================================

def plot_target_pie(target_counts, figsize=(6, 6)):
    """
    Plot a pie chart of target variable distribution.

    Parameters
    ----------
    target_counts : pandas.Series
        Value counts of the target variable.
    figsize : tuple, optional
        Figure size. Default is (6, 6).
    """
    plt.figure(figsize=figsize)

    plt.pie(
        target_counts,
        labels=target_counts.index,
        autopct="%1.1f%%",
        startangle=90,
        explode=[0, 0.08],
        shadow=True
    )

    plt.title("Customer Churn Percentage")

    plt.tight_layout()
    plt.show()
