import streamlit as st
import plotly.express as px


def create_line_graph(df, x, y, title, subtitle, height, width, markers=False):
    fig = px.line(
        df,
        x=x,
        y=y,
        title=f"{title} <br><sup>{subtitle}</sup>",
        height=height,
        width=width,
    )
    st.plotly_chart(fig)
