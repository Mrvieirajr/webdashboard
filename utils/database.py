import os
import pandas as pd
from sqlalchemy import create_engine, text
import streamlit as st

class Database:
    def __init__(self):
        self.engine = self._create_engine()

    def _create_engine(self):
        """Create SQLAlchemy engine using environment variables"""
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            st.error("Database configuration not found!")
            return None
        return create_engine(database_url)

    def query_data(self, query, params=None) -> pd.DataFrame:
        """Execute SQL query and return results as DataFrame"""
        try:
            with self.engine.connect() as conn:
                if isinstance(query, str):
                    query = text(query)
                return pd.read_sql_query(query, conn, params=params)
        except Exception as e:
            st.error(f"Query execution failed: {str(e)}")
            return pd.DataFrame()

    def get_sample_data(self, limit: int = 1000) -> pd.DataFrame:
        """Get sample data from the sales table"""
        query = """
        SELECT *
        FROM sales_data
        ORDER BY date DESC
        LIMIT :limit
        """
        return self.query_data(query, params={'limit': limit})

    def verify_user(self, email: str, password: str) -> pd.DataFrame:
        """Verify user credentials"""
        query = """
        SELECT email, name
        FROM users
        WHERE email = :email AND password = :password
        LIMIT 1
        """
        return self.query_data(query, params={'email': email, 'password': password})

    def get_financial_metrics(self, start_date: str, end_date: str) -> pd.DataFrame:
        """Get financial metrics for DRE dashboard"""
        query = """
        SELECT date, revenue, profit, taxes, expenses
        FROM financial_metrics
        WHERE date BETWEEN :start_date AND :end_date
        ORDER BY date
        """
        return self.query_data(query, params={'start_date': start_date, 'end_date': end_date})

    def get_store_performance(self, start_date: str, end_date: str) -> pd.DataFrame:
        """Get store performance metrics"""
        query = """
        SELECT date, store_name, revenue, profit, customer_count
        FROM store_performance
        WHERE date BETWEEN :start_date AND :end_date
        ORDER BY date, store_name
        """
        return self.query_data(query, params={'start_date': start_date, 'end_date': end_date})

    def get_cash_flow(self, start_date: str, end_date: str) -> pd.DataFrame:
        """Get cash flow data"""
        query = """
        SELECT date, cash_balance, inflow, outflow, category
        FROM cash_flow
        WHERE date BETWEEN :start_date AND :end_date
        ORDER BY date, category
        """
        return self.query_data(query, params={'start_date': start_date, 'end_date': end_date})