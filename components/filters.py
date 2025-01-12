import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from config import DEFAULT_DAYS

class Filters:
    @staticmethod
    def create_date_filter(key: str = "date_filter"):
        """Create a date range filter"""
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input(
                "Start Date",
                datetime.now() - timedelta(days=DEFAULT_DAYS),
                key=f"{key}_start"
            )
        with col2:
            end_date = st.date_input(
                "End Date",
                datetime.now(),
                key=f"{key}_end"
            )
        return start_date, end_date

    @staticmethod
    def create_category_filter(df: pd.DataFrame, column: str, label: str):
        """Create a multi-select filter for categories"""
        options = sorted(df[column].unique().tolist())
        return st.multiselect(
            label,
            options=options,
            default=None,
            key=f"filter_{column}"
        )

    @staticmethod
    def create_numeric_filter(df: pd.DataFrame, column: str, label: str):
        """Create a numeric range filter"""
        min_val = float(df[column].min())
        max_val = float(df[column].max())
        return st.slider(
            label,
            min_value=min_val,
            max_value=max_val,
            value=(min_val, max_val),
            key=f"filter_{column}"
        )
