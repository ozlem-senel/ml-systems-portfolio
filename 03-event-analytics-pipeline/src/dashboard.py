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
import importlib.util


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
    st.markdown("Explore player behavior and level performance")

    if "dashboard_view" not in st.session_state:
        st.session_state.dashboard_view = "player"
    player_nav, level_nav = st.columns(2)
    with player_nav:
        st.button("Player Analytics", use_container_width=True,
                  type="primary" if st.session_state.dashboard_view == "player" else "secondary",
                  on_click=lambda: st.session_state.update(dashboard_view="player"))
    with level_nav:
        st.button("Level Analytics", use_container_width=True,
                  type="primary" if st.session_state.dashboard_view == "level" else "secondary",
                  on_click=lambda: st.session_state.update(dashboard_view="level"))
    
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
    
    if st.session_state.dashboard_view == "player":
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
        st.caption("All cohorts; the date filter applies to the daily charts above, not this retention summary.")
    
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
    
        # Data Table
        with st.expander("View Raw Metrics Data"):
            st.dataframe(
                daily_metrics_filtered.sort_values('event_date', ascending=False),
                use_container_width=True
            )
    else:
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
    
        # Level analysis is owned by project 04; the dashboard only presents it.
        st.header("Level Difficulty Analysis")
        st.caption("Synthetic data · Players are grouped by when they first started each level. "
                   "Outcomes are observed through the selected end date.")
        analysis_path = Path(__file__).resolve().parents[2] / "04-level-progression-analysis" / "src" / "analysis.py"
        try:
            spec = importlib.util.spec_from_file_location("level_analysis", analysis_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            events_path = Path(__file__).resolve().parents[1] / "data" / "processed" / "events_cleaned.parquet"
            if len(date_range) != 2:
                st.info("Select both a start and an end date to view level analysis.")
            else:
                events = pd.read_parquet(events_path)
                metrics = module.level_metrics(events, start_date=date_range[0], end_date=date_range[1])
                max_level = int(metrics.level.max())
                if max_level > 1:
                    selected_levels = st.slider("Level range", 1, max_level, (1, min(50, max_level)))
                else:
                    selected_levels = (1, 1)
                min_players = st.number_input("Minimum players per level", min_value=1, value=30, step=5,
                                              help="Hide levels with too few players for a useful comparison.")
                subset = metrics[metrics.level.between(*selected_levels)]
                visible = subset[subset.players_started >= min_players].copy()
                st.caption(f"Showing {len(visible)} of {len(subset)} levels in range with at least {min_players} players. "
                           "Change the controls to explore other levels.")
                if visible.empty:
                    st.info("No levels meet these filters. Try a wider level range or a lower minimum player count.")
                else:
                    first, second = st.columns(2)
                    with first:
                        fig = go.Figure()
                        fig.add_trace(go.Scatter(
                            x=visible.level, y=visible.first_attempt_win_rate, mode="lines+markers",
                            name="First-attempt win rate", line=dict(color="#62b5ff", width=2),
                            customdata=visible[["players_started", "first_win_ci_low", "first_win_ci_high"]],
                            hovertemplate="Level %{x}<br>First-attempt wins: %{y:.1%}<br>Players: %{customdata[0]}<br>95% interval: %{customdata[1]:.1%}–%{customdata[2]:.1%}<extra></extra>"))
                        fig.update_layout(title="First-attempt win rate", xaxis_title="Level", yaxis_title="Players",
                                          yaxis=dict(tickformat=".0%", range=[0, 1]), hovermode="closest")
                        st.plotly_chart(fig, use_container_width=True)
                    with second:
                        fig = px.bar(visible, x="level", y="mean_attempts", hover_data=["players_started"],
                                     title="Average attempts per player", labels={"level": "Level", "mean_attempts": "Attempts"},
                                     color_discrete_sequence=["#a58bfa"])
                        st.plotly_chart(fig, use_container_width=True)
                    st.subheader("Progression funnel")
                    st.caption("Follow the same players from their first start of the selected starting level through consecutive level starts.")
                    if max_level > 1:
                        funnel_range = st.slider("Funnel level range", 1, max_level, (1, min(10, max_level)))
                    else:
                        funnel_range = (1, 1)
                    if funnel_range[1] - funnel_range[0] >= 30:
                        st.info("Choose up to 30 levels to keep the funnel readable.")
                    else:
                        funnel = module.progression_funnel(events, *funnel_range,
                                                           start_date=date_range[0], end_date=date_range[1])
                        if funnel.players.iloc[0] == 0:
                            st.info("No players first started this level in the selected dates.")
                        else:
                            funnel['stage'] = funnel.level.map(lambda n: f"Level {n}")
                            fig = px.funnel(funnel, x="players", y="stage", color_discrete_sequence=["#62b5ff"])
                            fig.update_traces(texttemplate="%{value:,} players · %{customdata:.1%} of starting cohort",
                                              customdata=funnel['share'])
                            fig.update_layout(height=max(350, 48 * len(funnel) + 100), xaxis_title="Players", yaxis_title="")
                            st.plotly_chart(fig, use_container_width=True)
                    st.caption("The cohort consists of players whose first recorded start of the starting level was in the selected dates. Later starts are observed through the end date; recent starters have less time to progress.")
                    st.subheader("Retry after a failed attempt")
                    fig = px.bar(visible, x="level", y="retry_rate_7d", hover_data=["retry_eligible", "retried_7d"],
                                 title="Returned within 7 days after first failure", labels={"level": "Level", "retry_rate_7d": "Players"})
                    fig.update_yaxes(tickformat=".0%", range=[0, 1])
                    st.plotly_chart(fig, use_container_width=True)
                    st.caption("Only players with a full 7-day observation window after their first failure are included.")
                    with st.expander("Level non-completion details"):
                        st.caption("Players who had not completed the level by the cutoff and whose last attempt was at least 7 days before it. This is not game churn.")
                        detail = visible[['level', 'mature_players', 'abandoned', 'abandonment_rate']].copy()
                        detail['abandonment_rate'] = detail['abandonment_rate'] * 100
                        detail.columns = ['Level', 'Eligible players', 'Not completed', 'Not completed rate (%)']
                        st.dataframe(detail, use_container_width=True,
                                     column_config={'Not completed rate (%)': st.column_config.NumberColumn(format="%.2f%%")})
                    st.subheader("Levels to investigate")
                    ranked = module.prioritize_levels(metrics, min_players=int(min_players))
                    ranked = ranked[ranked.level.between(*selected_levels) & (ranked.gap > 0)].head(10)
                    if ranked.empty:
                        st.info("No eligible level has a lower first-attempt win rate than its neighboring levels.")
                    else:
                        st.dataframe(ranked, use_container_width=True)
                    st.caption("Ranks use the first-win gap against adjacent eligible levels multiplied by starters. This is a descriptive prioritization, not an estimated causal effect.")
                    with st.expander("Level metrics and definitions"):
                        st.dataframe(visible, use_container_width=True)
                        st.caption("Completion and attempts include activity through the selected end date; recent starters may not yet have completed. "
                                   "Seven-day abandonment excludes players without a complete observation window.")
        except (FileNotFoundError, ValueError) as exc:
            st.info(f"Level analysis unavailable: {exc}")



if __name__ == "__main__":
    main()
