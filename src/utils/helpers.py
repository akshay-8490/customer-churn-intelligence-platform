"""
Utility Helpers

Small reusable utility functions used across the
Customer Churn Intelligence Platform.
"""


def print_section(title, width=70):
    """
    Print a formatted section header.

    Parameters
    ----------
    title : str
        Section title text.
    width : int, optional
        Width of the separator line. Default is 70.
    """
    print("=" * width)
    print(title)
    print("=" * width)


def format_percentage(value, total, decimals=2):
    """
    Format a value as a percentage of a total.

    Parameters
    ----------
    value : int or float
        The numerator.
    total : int or float
        The denominator.
    decimals : int, optional
        Number of decimal places. Default is 2.

    Returns
    -------
    str
        Formatted percentage string (e.g., '26.54%').
    """
    if total == 0:
        return "0.00%"
    return f"{(value / total) * 100:.{decimals}f}%"


def create_directory(path):
    """
    Create a directory (and parents) if it doesn't exist.

    Parameters
    ----------
    path : str or Path
        Directory path to create.
    """
    from pathlib import Path

    Path(path).mkdir(parents=True, exist_ok=True)
