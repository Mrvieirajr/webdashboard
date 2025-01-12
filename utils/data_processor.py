import pandas as pd
import streamlit as st

class DataProcessor:
    @staticmethod
    @st.cache_data
    def process_time_series(df: pd.DataFrame, date_column: str, value_column: str) -> pd.DataFrame:
        """Process time series data for charts"""
        return df.groupby(date_column)[value_column].sum().reset_index()

    @staticmethod
    @st.cache_data
    def calculate_metrics(df: pd.DataFrame) -> dict:
        """Calculate key metrics from dataframe"""
        metrics = {
            'total_count': len(df),
            'average_value': df['value'].mean() if 'value' in df.columns else 0,
            'max_value': df['value'].max() if 'value' in df.columns else 0,
            'min_value': df['value'].min() if 'value' in df.columns else 0
        }
        return metrics

    @staticmethod
    def filter_dataframe(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
        """Apply filters to dataframe"""
        filtered_df = df.copy()
        for column, value in filters.items():
            if value:
                if isinstance(value, (list, tuple)):
                    filtered_df = filtered_df[filtered_df[column].isin(value)]
                else:
                    filtered_df = filtered_df[filtered_df[column] == value]
        return filtered_df
