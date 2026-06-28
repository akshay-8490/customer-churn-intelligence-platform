"""
Visualization Components
Project: Customer Churn Intelligence Platform

Reusable visualization helpers for displaying
pre-generated project figures and interactive
Plotly charts across the Streamlit application.
"""

from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.config.paths import REPORTS_FIGURES_DIR


# ==========================================================
# Display Figure
# ==========================================================

def display_figure(
    filename: str,
    caption: str | None = None,
    width: str = "stretch"
) -> None:
    """
    Display a pre-generated figure.

    Parameters
    ----------
    filename : str
        Image filename inside reports/figures.

    caption : str, optional
        Caption displayed below the image.

    width : str, default="stretch"
        Whether the image expands to container width.
    """

    image_path = REPORTS_FIGURES_DIR / filename

    if not image_path.exists():
        st.warning(
            f"Figure not found: {filename}"
        )
        return

    st.image(
        str(image_path),
        caption=caption,
        width=width
    )


# ==========================================================
# Display Two Figures
# ==========================================================

def display_two_figures(
    left_filename: str,
    right_filename: str,
    left_caption: str | None = None,
    right_caption: str | None = None,
) -> None:
    """
    Display two figures side-by-side.
    """

    col1, col2 = st.columns(2)

    with col1:
        display_figure(
            left_filename,
            left_caption
        )

    with col2:
        display_figure(
            right_filename,
            right_caption
        )


# ==========================================================
# Display Three Figures
# ==========================================================

def display_three_figures(
    first_filename: str,
    second_filename: str,
    third_filename: str,
    first_caption: str | None = None,
    second_caption: str | None = None,
    third_caption: str | None = None,
) -> None:
    """
    Display three figures in a single row.
    """

    col1, col2, col3 = st.columns(3)

    with col1:
        display_figure(
            first_filename,
            first_caption
        )

    with col2:
        display_figure(
            second_filename,
            second_caption
        )

    with col3:
        display_figure(
            third_filename,
            third_caption
        )


# ==========================================================
# Dashboard Theme
# ==========================================================

def apply_dashboard_theme(
    fig: go.Figure
) -> go.Figure:
    """
    Apply a consistent theme to Plotly figures.
    """

    fig.update_layout(
        template="plotly_white",
        height=380,
        margin=dict(
            l=20,
            r=20,
            t=55,
            b=20
        ),
        title_x=0.02,
        legend_title_text="",
        font=dict(
            size=13
        )
    )

    return fig


# ==========================================================
# Generic Vertical Bar Chart
# ==========================================================

def bar_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    color: str | None = None,
    text_auto: bool = True
) -> go.Figure:
    """
    Create a reusable vertical bar chart.
    """

    fig = px.bar(
        df,
        x=x,
        y=y,
        color=color,
        text_auto=".2s" if text_auto else False,
        title=title
    )

    fig.update_layout(
        xaxis_title="",
        yaxis_title=""
    )

    return apply_dashboard_theme(fig)


# ==========================================================
# Generic Horizontal Bar Chart
# ==========================================================

def horizontal_bar_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    color: str | None = None,
    text_auto: bool = True
) -> go.Figure:
    """
    Create a reusable horizontal bar chart.
    """

    fig = px.bar(
        df,
        x=x,
        y=y,
        orientation="h",
        color=color,
        text_auto=".2s" if text_auto else False,
        title=title
    )

    fig.update_layout(
        xaxis_title="",
        yaxis_title=""
    )

    return apply_dashboard_theme(fig)


# ==========================================================
# Generic Donut Chart
# ==========================================================

def donut_chart(
    df: pd.DataFrame,
    names: str,
    values: str,
    title: str
) -> go.Figure:
    """
    Create a reusable donut chart.
    """

    fig = px.pie(
        df,
        names=names,
        values=values,
        hole=0.55,
        title=title
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    return apply_dashboard_theme(fig)


# ==========================================================
# Generic Pie Chart
# ==========================================================

def pie_chart(
    df: pd.DataFrame,
    names: str,
    values: str,
    title: str
) -> go.Figure:
    """
    Create a reusable pie chart.
    """

    fig = px.pie(
        df,
        names=names,
        values=values,
        title=title
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    return apply_dashboard_theme(fig)

# ==========================================================
# Generic Line Chart
# ==========================================================

def line_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    color: str | None = None,
    markers: bool = True
) -> go.Figure:
    """
    Create a reusable line chart.

    Parameters
    ----------
    df : pandas.DataFrame

    x : str
        X-axis column.

    y : str
        Y-axis column.

    title : str
        Chart title.

    color : str, optional
        Column used for color grouping.

    markers : bool, default=True
        Whether to display markers.

    Returns
    -------
    plotly.graph_objects.Figure
    """

    fig = px.line(
        df,
        x=x,
        y=y,
        color=color,
        markers=markers,
        title=title
    )

    fig.update_layout(
        xaxis_title="",
        yaxis_title=""
    )

    return apply_dashboard_theme(fig)


# ==========================================================
# Generic Histogram
# ==========================================================

def histogram_chart(
    df: pd.DataFrame,
    x: str,
    title: str,
    color: str | None = None,
    nbins: int = 20
) -> go.Figure:
    """
    Create a reusable histogram.

    Parameters
    ----------
    df : pandas.DataFrame

    x : str
        Numeric column.

    title : str

    color : str, optional

    nbins : int, default=20

    Returns
    -------
    plotly.graph_objects.Figure
    """

    fig = px.histogram(
        df,
        x=x,
        color=color,
        nbins=nbins,
        title=title
    )

    fig.update_layout(
        xaxis_title="",
        yaxis_title="Count"
    )

    return apply_dashboard_theme(fig)


# ==========================================================
# Generic Box Plot
# ==========================================================

def box_plot(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    color: str | None = None
) -> go.Figure:
    """
    Create a reusable box plot.

    Parameters
    ----------
    df : pandas.DataFrame

    x : str

    y : str

    title : str

    color : str, optional

    Returns
    -------
    plotly.graph_objects.Figure
    """

    fig = px.box(
        df,
        x=x,
        y=y,
        color=color,
        title=title
    )

    fig.update_layout(
        xaxis_title="",
        yaxis_title=""
    )

    return apply_dashboard_theme(fig)


# ==========================================================
# Generic Scatter Plot
# ==========================================================

def scatter_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    color: str | None = None,
    size: str | None = None
) -> go.Figure:
    """
    Create a reusable scatter plot.

    Parameters
    ----------
    df : pandas.DataFrame

    x : str

    y : str

    title : str

    color : str, optional

    size : str, optional

    Returns
    -------
    plotly.graph_objects.Figure
    """

    fig = px.scatter(
        df,
        x=x,
        y=y,
        color=color,
        size=size,
        title=title
    )

    fig.update_layout(
        xaxis_title="",
        yaxis_title=""
    )

    return apply_dashboard_theme(fig)


# ==========================================================
# Generic Gauge Chart
# ==========================================================

def gauge_chart(
    value: float,
    title: str,
    threshold: float = 55.0,
    min_value: float = 0.0,
    max_value: float = 100.0,
) -> go.Figure:
    """
    Create a reusable gauge chart for displaying
    churn probability or other percentage metrics.

    Parameters
    ----------
    value : float
        Value to display (0–100).

    title : str
        Chart title.

    threshold : float, default=55.0
        Model prediction threshold (percentage).

    min_value : float, default=0

    max_value : float, default=100

    Returns
    -------
    plotly.graph_objects.Figure
    """

    medium_limit = min(threshold + 20, max_value)

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",

            value=value,

            number={
                "suffix": "%"
            },

            title={
                "text": title
            },

            gauge={

                "axis": {
                    "range": [min_value, max_value]
                },

                "bar": {
                    "thickness": 0.30
                },

                "threshold": {
                    "line": {
                        "color": "black",
                        "width": 4
                    },
                    "thickness": 0.8,
                    "value": threshold
                },

                "steps": [

                    {
                        "range": [0, threshold],
                        "color": "#4CAF50"
                    },

                    {
                        "range": [threshold, medium_limit],
                        "color": "#FFC107"
                    },

                    {
                        "range": [medium_limit, max_value],
                        "color": "#F44336"
                    },
                ],
            },
        )
    )

    fig.update_layout(
        template="plotly_white",
        height=320,
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20,
        ),
    )

    return fig

# ==========================================================
# Exports
# ==========================================================

__all__ = [

    # Static Figures
    "display_figure",
    "display_two_figures",
    "display_three_figures",

    # Theme
    "apply_dashboard_theme",

    # Interactive Charts
    "bar_chart",
    "horizontal_bar_chart",
    "donut_chart",
    "pie_chart",
    "line_chart",
    "histogram_chart",
    "box_plot",
    "scatter_chart",
    "gauge_chart",
]