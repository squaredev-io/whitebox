import streamlit as st
import pandas as pd
import plotly.express as px


def create_line_graph(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    subtitle: str,
    height: float,
    width: float,
    markers: bool = False,
) -> None:
    """Plots a plotly chart in Streamlit"""
    fig = px.line(
        df,
        x=x,
        y=y,
        title=f"{title} <br><sup>{subtitle}</sup>",
        height=height,
        width=width,
    )
    st.plotly_chart(fig)
