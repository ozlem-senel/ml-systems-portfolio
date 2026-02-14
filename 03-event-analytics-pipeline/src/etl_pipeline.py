"""
ETL Pipeline for processing game events.

Reads raw event data, cleans, enriches, and aggregates into metrics.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import polars as pl


class EventETLPipeline:
    """Process raw game events into analytics-ready metrics."""
    
    def __init__(self, input_file: str):
        self.input_file = Path(input_file)
        
    def load_events(self) -> pl.DataFrame:
        """Load events from JSON lines file into Polars DataFrame."""
        print(f"Loading events from {self.input_file}...")
        
        # Read JSON lines
        with open(self.input_file, 'r') as f:
            events = [json.loads(line) for line in f]
        
        # Flatten properties into columns
        flattened = []
        for event in events:
            flat_event = {
                "event_id": event["event_id"],
                "player_id": event["player_id"],
                "session_id": event.get("session_id"),
                "event_type": event["event_type"],
                "timestamp": event["timestamp"]
            }
            
            # Add properties as separate columns
            if "properties" in event:
                for key, value in event["properties"].items():
                    flat_event[f"prop_{key}"] = value
            
            flattened.append(flat_event)
        
        df = pl.DataFrame(flattened, infer_schema_length=10000)
        
        # Convert timestamp to datetime
        df = df.with_columns([
            pl.col("timestamp").str.to_datetime().alias("timestamp")
        ])
        
        print(f"Loaded {len(df):,} events")
        return df
    
    def clean_and_enrich(self, df: pl.DataFrame) -> pl.DataFrame:
        """Clean data and add derived columns."""
        print("Cleaning and enriching data...")
        
        # Add date and hour columns
        df = df.with_columns([
            pl.col("timestamp").dt.date().alias("event_date"),
            pl.col("timestamp").dt.hour().alias("event_hour"),
            pl.col("timestamp").dt.weekday().alias("day_of_week")
        ])
        
        # Remove duplicates by event_id
        df = df.unique(subset=["event_id"])
        
        # Sort by timestamp
        df = df.sort("timestamp")
        
        print(f"After cleaning: {len(df):,} events")
        return df
    
    def aggregate_daily_metrics(self, df: pl.DataFrame) -> pl.DataFrame:
        """Aggregate events into daily metrics."""
        print("Calculating daily metrics...")
        
        # Get unique players per day (DAU)
        dau = (
            df.filter(pl.col("event_type") == "session_start")
            .group_by("event_date")
            .agg([
                pl.col("player_id").n_unique().alias("dau")
            ])
        )
        
        # Session metrics
        session_metrics = (
            df.filter(pl.col("event_type") == "session_end")
            .group_by("event_date")
            .agg([
                pl.col("session_id").n_unique().alias("total_sessions"),
                pl.col("prop_session_duration").mean().alias("avg_session_duration"),
                pl.col("prop_levels_played").sum().alias("total_levels_played")
            ])
        )
        
        # Purchase metrics
        purchase_df = df.filter(pl.col("event_type") == "purchase")
        if len(purchase_df) > 0:
            # Ensure prop_price_usd column exists, even if it's all null
            if "prop_price_usd" not in purchase_df.columns:
                purchase_df = purchase_df.with_columns([
                    pl.lit(None).alias("prop_price_usd")
                ])
            
            purchase_metrics = (
                purchase_df
                .group_by("event_date")
                .agg([
                    pl.col("event_id").count().alias("total_purchases"),
                    pl.col("prop_price_usd").sum().fill_null(0).alias("total_revenue"),
                    pl.col("player_id").n_unique().alias("paying_users")
                ])
            )
        else:
            # Create empty dataframe with correct schema
            purchase_metrics = pl.DataFrame({
                "event_date": [],
                "total_purchases": [],
                "total_revenue": [],
                "paying_users": []
            })
        
        # Ad metrics
        ad_df = df.filter(pl.col("event_type") == "ad_watched")
        if len(ad_df) > 0:
            ad_metrics = (
                ad_df
                .group_by("event_date")
                .agg([
                    pl.col("event_id").count().alias("total_ads_watched")
                ])
            )
        else:
            ad_metrics = pl.DataFrame({
                "event_date": [],
                "total_ads_watched": []
            })
        
        # Level completion metrics
        level_metrics = (
            df.filter(pl.col("event_type").is_in(["level_complete", "level_fail"]))
            .group_by("event_date")
            .agg([
                pl.col("event_id").count().alias("total_level_attempts"),
                (pl.col("event_type") == "level_complete").sum().alias("successful_completions"),
            ])
        )
        
        # Merge all metrics
        daily_metrics = dau
        for metrics_df in [session_metrics, purchase_metrics, ad_metrics, level_metrics]:
            daily_metrics = daily_metrics.join(metrics_df, on="event_date", how="left")
        
        # Fill nulls with 0 for metrics
        daily_metrics = daily_metrics.fill_null(0)
        
        # Calculate derived metrics
        daily_metrics = daily_metrics.with_columns([
            (pl.col("total_revenue") / pl.col("dau")).alias("arpu"),
            (pl.col("paying_users") / pl.col("dau") * 100).alias("conversion_rate"),
            (pl.col("successful_completions") / pl.col("total_level_attempts") * 100).alias("level_success_rate"),
            (pl.col("total_sessions") / pl.col("dau")).alias("sessions_per_user")
        ])
        
        return daily_metrics.sort("event_date")
    
    def calculate_retention(self, df: pl.DataFrame) -> pl.DataFrame:
        """Calculate D1, D7, D30 retention by install cohort."""
        print("Calculating retention metrics...")
        
        # Get first session per player (install date)
        installs = (
            df.filter(pl.col("event_type") == "session_start")
            .group_by("player_id")
            .agg([
                pl.col("event_date").min().alias("install_date")
            ])
        )
        
        # Get all active days per player
        active_days = (
            df.filter(pl.col("event_type") == "session_start")
            .select(["player_id", "event_date"])
            .unique()
        )
        
        # Join to get days since install
        activity = active_days.join(installs, on="player_id")
        activity = activity.with_columns([
            (pl.col("event_date") - pl.col("install_date")).dt.total_days().alias("days_since_install")
        ])
        
        # Calculate retention for each cohort
        retention = (
            installs.group_by("install_date")
            .agg([
                pl.col("player_id").count().alias("cohort_size")
            ])
        )
        
        # D1 retention
        d1_active = (
            activity.filter(pl.col("days_since_install") == 1)
            .group_by("install_date")
            .agg([
                pl.col("player_id").n_unique().alias("d1_active")
            ])
        )
        
        # D7 retention
        d7_active = (
            activity.filter(pl.col("days_since_install") == 7)
            .group_by("install_date")
            .agg([
                pl.col("player_id").n_unique().alias("d7_active")
            ])
        )
        
        # D30 retention
        d30_active = (
            activity.filter(pl.col("days_since_install") == 30)
            .group_by("install_date")
            .agg([
                pl.col("player_id").n_unique().alias("d30_active")
            ])
        )
        
        # Merge retention data
        retention = retention.join(d1_active, on="install_date", how="left")
        retention = retention.join(d7_active, on="install_date", how="left")
        retention = retention.join(d30_active, on="install_date", how="left")
        
        retention = retention.fill_null(0)
        
        # Calculate retention percentages
        retention = retention.with_columns([
            (pl.col("d1_active") / pl.col("cohort_size") * 100).alias("d1_retention"),
            (pl.col("d7_active") / pl.col("cohort_size") * 100).alias("d7_retention"),
            (pl.col("d30_active") / pl.col("cohort_size") * 100).alias("d30_retention")
        ])
        
        return retention.sort("install_date")
    
    def run(self, output_dir: str = "data/processed"):
        """Run full ETL pipeline."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Load and clean events
        df = self.load_events()
        df = self.clean_and_enrich(df)
        
        # Save cleaned events
        cleaned_file = output_path / "events_cleaned.parquet"
        df.write_parquet(cleaned_file)
        print(f"Saved cleaned events to {cleaned_file}")
        
        # Calculate metrics
        daily_metrics = self.aggregate_daily_metrics(df)
        metrics_file = output_path / "daily_metrics.parquet"
        daily_metrics.write_parquet(metrics_file)
        print(f"Saved daily metrics to {metrics_file}")
        print(f"\nDaily Metrics Preview:")
        print(daily_metrics.head())
        
        # Calculate retention
        retention = self.calculate_retention(df)
        retention_file = output_path / "retention_cohorts.parquet"
        retention.write_parquet(retention_file)
        print(f"\nSaved retention data to {retention_file}")
        print(f"\nRetention Preview:")
        print(retention.head())
        
        return {
            "events": df,
            "daily_metrics": daily_metrics,
            "retention": retention
        }


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run ETL pipeline on game events")
    parser.add_argument("--input", type=str, required=True, help="Input JSONL file")
    parser.add_argument("--output", type=str, default="data/processed", help="Output directory")
    
    args = parser.parse_args()
    
    pipeline = EventETLPipeline(args.input)
    pipeline.run(output_dir=args.output)
