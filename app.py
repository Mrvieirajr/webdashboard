import streamlit as st
from utils.database import Database
from utils.data_processor import DataProcessor
from utils.auth import Auth
from components.charts import Charts
from components.metrics import Metrics
from components.filters import Filters
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Interactive Dashboard",
    page_icon="📊",
    layout="wide"
)

# Initialize components
auth = Auth()
db = Database()
charts = Charts()
metrics = Metrics()
filters = Filters()

def login_page():
    st.title("🔐 Login")

    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            if auth.login(email, password):
                st.session_state['current_page'] = 'dashboard_selection'
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid email or password")

def dashboard_selection_page():
    st.title("📊 Dashboard Selection")

    # Sidebar with logout button
    with st.sidebar:
        if st.button("Logout"):
            auth.logout()
            st.rerun()
        st.write(f"Welcome, {st.session_state['user']['name']}!")

    # Style for dashboard cards
    st.markdown("""
        <style>
        .dashboard-card {
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #e6e6e6;
            margin: 10px;
            transition: transform 0.2s;
        }
        .dashboard-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
            <div class="dashboard-card">
                <h3>📈 Analytics Dashboard</h3>
                <p>Comprehensive data analysis and visualization dashboard with interactive charts and filters.</p>
            </div>
        """, unsafe_allow_html=True)

        if st.button("Open Dashboard", key="main_dashboard"):
            st.session_state['current_page'] = 'main_dashboard'
            st.rerun()

    with col2:
        st.markdown("""
            <div class="dashboard-card">
                <h3>💰 DRE Empresarial</h3>
                <p>Financial metrics, revenue by store, and cash flow analysis with detailed reports.</p>
            </div>
        """, unsafe_allow_html=True)

        if st.button("Open Dashboard", key="dre_dashboard"):
            st.session_state['current_page'] = 'dre_dashboard'
            st.rerun()

def dre_dashboard():
    st.title("💰 DRE Empresarial")

    # Sidebar
    with st.sidebar:
        if st.button("← Back to Dashboard Selection"):
            st.session_state['current_page'] = 'dashboard_selection'
            st.rerun()

        if st.button("Logout"):
            auth.logout()
            st.rerun()

        st.write(f"Welcome, {st.session_state['user']['name']}!")
        st.markdown("---")

        # Date filter
        st.markdown("### Date Range")
        start_date, end_date = filters.create_date_filter()

        # Store filter
        st.markdown("### Store Filter")
        store_data_temp = db.get_store_performance(start_date, end_date)
        selected_stores = filters.create_category_filter(
            store_data_temp, 'store_name', 'Select Stores'
        )

    # Load financial data
    store_data = db.get_store_performance(start_date, end_date)
    if selected_stores:
        store_data = store_data[store_data['store_name'].isin(selected_stores)]

    # Aggregate financial data based on selected stores
    if not store_data.empty:
        financial_data = pd.DataFrame({
            'date': store_data['date'].unique()
        }).sort_values('date')

        financial_metrics = store_data.groupby('date').agg({
            'revenue': 'sum',
            'profit': 'sum'
        }).reset_index()

        financial_data = financial_data.merge(financial_metrics, on='date', how='left')
        financial_data['taxes'] = financial_data['revenue'] * 0.15  # Example tax calculation
        financial_data['expenses'] = financial_data['revenue'] - financial_data['profit'] - financial_data['taxes']
    else:
        financial_data = pd.DataFrame()

    cash_flow_data = db.get_cash_flow(start_date, end_date)
    if selected_stores and not cash_flow_data.empty:
        # Filter cash flow data if it has store information
        if 'store_name' in cash_flow_data.columns:
            cash_flow_data = cash_flow_data[cash_flow_data['store_name'].isin(selected_stores)]

    # Big Numbers Section
    st.markdown("### Key Financial Metrics")
    if not financial_data.empty:
        total_revenue = financial_data['revenue'].sum()
        total_profit = financial_data['profit'].sum()
        total_taxes = financial_data['taxes'].sum()
        profit_margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            metrics.display_metric_card("Faturamento", f"R$ {total_revenue:,.2f}")
        with col2:
            metrics.display_metric_card("Lucro", f"R$ {total_profit:,.2f}")
        with col3:
            metrics.display_metric_card("Impostos", f"R$ {total_taxes:,.2f}")
        with col4:
            metrics.display_metric_card("Margem de Lucro", f"{profit_margin:.1f}%")

    # Charts Section
    st.markdown("### Performance Analysis")
    col1, col2 = st.columns(2)

    with col1:
        if not financial_data.empty:
            # Revenue and Profit Trend
            fig = charts.create_line_chart(
                financial_data,
                'date',
                'revenue',
                'Evolução do Faturamento'
            )
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        if not store_data.empty:
            # Store Performance
            store_summary = store_data.groupby('store_name')['revenue'].sum().reset_index()
            fig = charts.create_pie_chart(
                store_summary,
                'store_name',
                'revenue',
                'Faturamento por Loja'
            )
            st.plotly_chart(fig, use_container_width=True)

    # Cash Flow Analysis
    st.markdown("### Cash Flow Analysis")
    if not cash_flow_data.empty:
        col1, col2 = st.columns(2)

        with col1:
            # Cash Balance Trend
            fig = charts.create_line_chart(
                cash_flow_data,
                'date',
                'cash_balance',
                'Evolução do Saldo de Caixa'
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Inflow vs Outflow by Category
            cash_summary = cash_flow_data.groupby('category')[['inflow', 'outflow']].sum().reset_index()
            fig = charts.create_bar_chart(
                cash_summary,
                'category',
                'inflow',
                'Entradas vs Saídas por Categoria'
            )
            st.plotly_chart(fig, use_container_width=True)

    # Detailed Data Tables
    st.markdown("### Detailed Reports")
    tab1, tab2, tab3 = st.tabs(["Financial Metrics", "Store Performance", "Cash Flow"])

    with tab1:
        if not financial_data.empty:
            st.dataframe(financial_data, use_container_width=True)

    with tab2:
        if not store_data.empty:
            st.dataframe(store_data, use_container_width=True)

    with tab3:
        if not cash_flow_data.empty:
            st.dataframe(cash_flow_data, use_container_width=True)


def main_dashboard():
    # Initialize df as empty DataFrame
    df = pd.DataFrame()

    # Load and cache data
    @st.cache_data(ttl=3600)
    def load_data():
        return db.get_sample_data()

    # Load data only if authenticated
    df = load_data()
    if df.empty:
        st.error("No data available")
        return

    # Apply date formatting
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])

    # Sidebar
    with st.sidebar:
        # Navigation buttons
        if st.button("← Back to Dashboard Selection"):
            st.session_state['current_page'] = 'dashboard_selection'
            st.rerun()

        if st.button("Logout"):
            auth.logout()
            st.rerun()

        st.write(f"Welcome, {st.session_state['user']['name']}!")
        st.markdown("---")

        # Filters section in sidebar
        st.title("📊 Filters")

        # Date filter
        st.markdown("### Date Range")
        start_date, end_date = filters.create_date_filter()

        # Apply date filters
        if 'date' in df.columns:
            df = df[(df['date'].dt.date >= start_date) & 
                    (df['date'].dt.date <= end_date)]

        # Additional filters in sidebar
        selected_categories = None
        selected_regions = None

        if 'category' in df.columns:
            st.markdown("### Category Filter")
            selected_categories = filters.create_category_filter(
                df, 'category', 'Select Categories'
            )

            if 'region' in df.columns:
                st.markdown("### Region Filter")
                selected_regions = filters.create_category_filter(
                    df, 'region', 'Select Regions'
                )
                if selected_regions:
                    df = df[df['region'].isin(selected_regions)]

        if selected_categories:
            df = df[df['category'].isin(selected_categories)]

    # Header
    st.title("📊 Interactive Dashboard")

    # Main content area
    # Calculate and display metrics
    st.markdown("### Key Metrics")
    metrics_data = DataProcessor.calculate_metrics(df)
    metrics.display_metrics_row(metrics_data)
    st.markdown("---")

    # Charts section
    st.markdown("### Data Visualization")
    col1, col2 = st.columns(2)

    with col1:
        if 'date' in df.columns and 'value' in df.columns:
            time_series = DataProcessor.process_time_series(
                df, 'date', 'value'
            )
            st.plotly_chart(
                charts.create_line_chart(
                    time_series, 'date', 'value',
                    'Time Series Analysis'
                ),
                use_container_width=True
            )

    with col2:
        if 'category' in df.columns and 'value' in df.columns:
            category_data = df.groupby('category')['value'].sum().reset_index()
            st.plotly_chart(
                charts.create_pie_chart(
                    category_data, 'category', 'value',
                    'Distribution by Category'
                ),
                use_container_width=True
            )

    # Data table section
    st.markdown("### Detailed Data")

    # Download button for filtered data
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "Download filtered data as CSV",
        csv,
        "filtered_data.csv",
        "text/csv",
        key='download-csv'
    )

    # Display interactive table
    st.dataframe(
        df,
        use_container_width=True,
        height=400
    )

def main():
    # Initialize current_page in session state if not exists
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = 'login'

    # Check authentication
    if not auth.is_authenticated():
        st.session_state['current_page'] = 'login'
        login_page()
        return

    # Route to appropriate page based on current_page
    if st.session_state['current_page'] == 'login':
        login_page()
    elif st.session_state['current_page'] == 'dashboard_selection':
        dashboard_selection_page()
    elif st.session_state['current_page'] == 'main_dashboard':
        main_dashboard()
    elif st.session_state['current_page'] == 'dre_dashboard':
        dre_dashboard()

if __name__ == "__main__":
    main()