"""
Streamlit dashboard for game analytics.

Visualizes key metrics: DAU, retention, revenue, engagement.
"""

import streamlit as st
import polars as pl
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime


st.set_page_config(
    page_title="Game Analytics Dashboard",
    page_icon=" ",
    layout="wide"
)


@st.cache_data
def load_data():
    """Load processed metrics data."""
    # Get the project root directory (parent of src/)
    project_root = Path(__file__).parent.parent
    data_dir = project_root / "data" / "processed"
    
    daily_metrics = pl.read_parquet(data_dir / "daily_metrics.parquet")
    retention = pl.read_parquet(data_dir / "retention_cohorts.parquet")
    
    return daily_metrics.to_pandas(), retention.to_pandas()


def main():
    st.title("Game Analytics Dashboard")
    st.markdown("Player behavior, engagement and monetization")
    
    try:
        daily_metrics, retention = load_data()
    except FileNotFoundError:
        st.error("No data found. Please run the ETL pipeline first.")
        st.code("python src/event_generator.py --players 5000 --days 30")
        st.code("python src/etl_pipeline.py --input data/raw_events/events_*.jsonl")
        return
    
    # Sidebar filters
    st.sidebar.header("Filters")
    
    # Convert event_date to datetime for compatibility
    daily_metrics['event_date'] = pd.to_datetime(daily_metrics['event_date'])
    
    date_range = st.sidebar.date_input(
        "Date Range",
        value=(daily_metrics['event_date'].min().date(), daily_metrics['event_date'].max().date()),
        min_value=daily_metrics['event_date'].min().date(),
        max_value=daily_metrics['event_date'].max().date()
    )
    
    # Filter data by date range
    if len(date_range) == 2:
        # Convert date objects to datetime for comparison
        start_date = pd.to_datetime(date_range[0])
        end_date = pd.to_datetime(date_range[1])
        mask = (daily_metrics['event_date'] >= start_date) & (daily_metrics['event_date'] <= end_date)
        daily_metrics_filtered = daily_metrics[mask]
    else:
        daily_metrics_filtered = daily_metrics
    
    # KPI Row
    st.header("Overview")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        avg_dau = int(daily_metrics_filtered['dau'].mean())
        st.metric("Avg DAU", f"{avg_dau:,}")
    
    with col2:
        total_revenue = daily_metrics_filtered['total_revenue'].sum()
        st.metric("Total Revenue", f"${total_revenue:,.2f}")
    
    with col3:
        avg_arpu = daily_metrics_filtered['arpu'].mean()
        st.metric("ARPU (Avg Rev Per User)", f"${avg_arpu:.3f}")
    
    with col4:
        avg_conversion = daily_metrics_filtered['conversion_rate'].mean()
        st.metric("Conversion Rate", f"{avg_conversion:.2f}%")
    
    with col5:
        avg_session_duration = daily_metrics_filtered['avg_session_duration'].mean()
        st.metric("Avg Session", f"{int(avg_session_duration/60)}m")
    
    # Charts Row 1
    st.header("Engagement Metrics")
    col1, col2 = st.columns(2)
    
    with col1:
        # DAU over time
        fig_dau = px.line(
            daily_metrics_filtered,
            x='event_date',
            y='dau',
            title='Daily Active Users',
            labels={'event_date': 'Date', 'dau': 'DAU'}
        )
        fig_dau.update_traces(line_color='#1f77b4', line_width=2)
        fig_dau.update_layout(hovermode='x unified')
        st.plotly_chart(fig_dau, use_container_width=True)
    
    with col2:
        # Sessions per user
        fig_sessions = px.line(
            daily_metrics_filtered,
            x='event_date',
            y='sessions_per_user',
            title='Sessions per User',
            labels={'event_date': 'Date', 'sessions_per_user': 'Sessions'}
        )
        fig_sessions.update_traces(line_color='#ff7f0e', line_width=2)
        fig_sessions.update_layout(hovermode='x unified')
        st.plotly_chart(fig_sessions, use_container_width=True)
    
    # Charts Row 2
    st.header("Monetization Metrics")
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue over time
        fig_revenue = go.Figure()
        fig_revenue.add_trace(go.Bar(
            x=daily_metrics_filtered['event_date'],
            y=daily_metrics_filtered['total_revenue'],
            name='Revenue',
            marker_color='#2ca02c'
        ))
        fig_revenue.update_layout(
            title='Daily Revenue',
            xaxis_title='Date',
            yaxis_title='Revenue ($)',
            hovermode='x unified'
        )
        st.plotly_chart(fig_revenue, use_container_width=True)
    
    with col2:
        # ARPU over time
        fig_arpu = px.line(
            daily_metrics_filtered,
            x='event_date',
            y='arpu',
            title='ARPU',
            labels={'event_date': 'Date', 'arpu': 'ARPU ($)'}
        )
        fig_arpu.update_traces(line_color='#d62728', line_width=2)
        fig_arpu.update_layout(hovermode='x unified')
        st.plotly_chart(fig_arpu, use_container_width=True)
    
    # Retention Section
    st.header("Retention")
    
    # Retention cohort table
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Retention curve
        avg_retention = retention[['d1_retention', 'd7_retention', 'd30_retention']].mean()
        
        fig_retention = go.Figure()
        fig_retention.add_trace(go.Scatter(
            x=['D1', 'D7', 'D30'],
            y=avg_retention.values,
            mode='lines+markers',
            marker=dict(size=12, color='#9467bd'),
            line=dict(width=3, color='#9467bd')
        ))
        fig_retention.update_layout(
            title='Retention Curve',
            xaxis_title='Days Since Install',
            yaxis_title='Retention Rate (%)',
            yaxis=dict(range=[0, 100])
        )
        st.plotly_chart(fig_retention, use_container_width=True)
    
    with col2:
        st.subheader("Stats")
        st.metric("D1 Retention", f"{avg_retention['d1_retention']:.1f}%")
        st.metric("D7 Retention", f"{avg_retention['d7_retention']:.1f}%")
        st.metric("D30 Retention", f"{avg_retention['d30_retention']:.1f}%")
        
        st.markdown("---")
        st.markdown(f"**Total Cohorts:** {len(retention)}")
        st.markdown(f"**Avg Cohort Size:** {int(retention['cohort_size'].mean()):,}")
    
    # Level Performance
    st.header("Player Progression")
    col1, col2 = st.columns(2)
    
    with col1:
        # Level success rate
        fig_success = px.line(
            daily_metrics_filtered,
            x='event_date',
            y='level_success_rate',
            title='Level Success Rate',
            labels={'event_date': 'Date', 'level_success_rate': 'Success Rate (%)'}
        )
        fig_success.update_traces(line_color='#8c564b', line_width=2)
        fig_success.update_layout(
            hovermode='x unified',
            yaxis=dict(range=[0, 100])
        )
        st.plotly_chart(fig_success, use_container_width=True)
    
    with col2:
        # Total level attempts
        fig_levels = go.Figure()
        fig_levels.add_trace(go.Bar(
            x=daily_metrics_filtered['event_date'],
            y=daily_metrics_filtered['total_level_attempts'],
            name='Level Attempts',
            marker_color='#e377c2'
        ))
        fig_levels.update_layout(
            title='Daily Level Attempts',
            xaxis_title='Date',
            yaxis_title='Attempts',
            hovermode='x unified'
        )
        st.plotly_chart(fig_levels, use_container_width=True)
    
    # Data Table
    with st.expander("View Raw Metrics Data"):
        st.dataframe(
            daily_metrics_filtered.sort_values('event_date', ascending=False),
            use_container_width=True
        )


if __name__ == "__main__":
    main()
