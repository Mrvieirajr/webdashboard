import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from config import CHART_COLORS

class Charts:
    @staticmethod
    def create_line_chart(df: pd.DataFrame, x: str, y: str, title: str) -> go.Figure:
        """Create an interactive line chart"""
        fig = px.line(
            df, x=x, y=y,
            title=title,
            template="simple_white",
            color_discrete_sequence=CHART_COLORS
        )
        fig.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=40, b=20),
            hovermode='x unified'
        )
        return fig

    @staticmethod
    def create_bar_chart(df: pd.DataFrame, x: str, y: str, title: str) -> go.Figure:
        """Create an interactive bar chart"""
        fig = px.bar(
            df, x=x, y=y,
            title=title,
            template="simple_white",
            color_discrete_sequence=CHART_COLORS
        )
        fig.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=40, b=20),
            hovermode='x unified'
        )
        return fig

    @staticmethod
    def create_pie_chart(df: pd.DataFrame, names: str, values: str, title: str) -> go.Figure:
        """Create an interactive pie chart"""
        fig = px.pie(
            df, names=names, values=values,
            title=title,
            color_discrete_sequence=CHART_COLORS
        )
        fig.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        return fig
