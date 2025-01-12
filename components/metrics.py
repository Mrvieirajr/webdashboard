import streamlit as st

class Metrics:
    @staticmethod
    def display_metric_card(label: str, value: any, delta: any = None):
        """Display a metric in a card format"""
        st.metric(
            label=label,
            value=value,
            delta=delta
        )

    @staticmethod
    def display_metrics_row(metrics: dict):
        """Display a row of metric cards"""
        cols = st.columns(len(metrics))
        for col, (label, value) in zip(cols, metrics.items()):
            with col:
                st.metric(label=label, value=value)
