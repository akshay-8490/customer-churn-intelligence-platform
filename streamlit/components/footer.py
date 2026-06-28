"""
Reusable Footer Component

Provides a consistent footer across all pages of the
Customer Churn Intelligence Platform.
"""

# ==========================================================
# Imports
# ==========================================================

import streamlit as st

from config import (
    COPYRIGHT,
    DATASET_NAME,
    ORGANIZATION,
)


# ==========================================================
# Footer
# ==========================================================

def render_footer(
    page_name: str,
    show_divider: bool = True,
):
    """
    Render a standardized footer.

    Parameters
    ----------
    page_name : str
        Name of the current Streamlit page.

    show_divider : bool, optional
        Whether to display a divider above the footer.
        Default is True.
    """

    if show_divider:
        st.divider()

    st.caption(
        f"{DATASET_NAME} • {page_name}"
    )

    st.caption(
        f"{ORGANIZATION} | {COPYRIGHT}"
    )