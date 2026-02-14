"""
Enhanced ETL Pipeline with logging, error handling, and data quality checks.

Production-ready version with monitoring and validation.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import sys

import polars as pl
import yaml


# Setup logging after creating logs directory
def setup_logging():
    """Configure logging with proper directory creation."""
    Path('logs').mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/etl_pipeline.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )

setup_logging()
logger = logging.getLogger(__name__)


class DataQualityError(Exception):
    """Raised when data quality checks fail."""
    pass


class EventETLPipeline:
    """Production ETL pipeline for game events."""
    
    def __init__(self, input_file: str, config_path: Optional[str] = None):
        self.input_file = Path(input_file)
        self.config = self._load_config(config_path)
        self.metrics = {
            'events_loaded': 0,
            'events_cleaned': 0,
            'events_failed': 0,
            'processing_time_seconds': 0
        }
        
        logger.info(f"Initialized ETL pipeline for {self.input_file}")
    
    def _load_config(self, config_path: Optional[str]) -> Dict:
        """Load configuration from YAML file."""
        if config_path and Path(config_path).exists():
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        
        # Default configuration
        return {
            'quality_checks': {
                'min_events': 1000,
                'max_null_percentage': 0.1,
                'required_event_types': ['session_start', 'session_end'],
                'max_future_days': 1
            },
            'aggregation': {
                'min_dau': 1,
                'max_revenue_per_event': 1000
            }
        }
    
    def validate_input_file(self) -> bool:
        """Validate input file exists and is readable."""
        try:
            if not self.input_file.exists():
                raise FileNotFoundError(f"Input file not found: {self.input_file}")
            
            if self.input_file.stat().st_size == 0:
                raise ValueError(f"Input file is empty: {self.input_file}")
            
            logger.info(f"Input file validated: {self.input_file.stat().st_size / 1024 / 1024:.2f} MB")
            return True
            
        except Exception as e:
            logger.error(f"Input validation failed: {str(e)}")
            raise
    
    def load_events(self) -> pl.DataFrame:
        """Load events from JSON lines with error handling."""
        logger.info(f"Loading events from {self.input_file}...")
        start_time = datetime.now()
        
        try:
            # Read JSON lines with error handling
            events = []
            failed_lines = 0
            
            with open(self.input_file, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    try:
                        events.append(json.loads(line))
                    except json.JSONDecodeError as e:
                        failed_lines += 1
                        logger.warning(f"Failed to parse line {line_num}: {str(e)}")
                        if failed_lines > 100:
                            raise DataQualityError(f"Too many failed lines: {failed_lines}")
            
            if not events:
                raise DataQualityError("No valid events found in input file")
            
            self.metrics['events_loaded'] = len(events)
            self.metrics['events_failed'] = failed_lines
            
            logger.info(f"Loaded {len(events):,} events ({failed_lines} failed)")
            
            # Flatten properties
            flattened = []
            for event in events:
                try:
                    flat_event = {
                        "event_id": event["event_id"],
                        "player_id": event["player_id"],
                        "session_id": event.get("session_id"),
                        "event_type": event["event_type"],
                        "timestamp": event["timestamp"]
                    }
                    
                    if "properties" in event:
                        for key, value in event["properties"].items():
                            flat_event[f"prop_{key}"] = value
                    
                    flattened.append(flat_event)
                except KeyError as e:
                    logger.warning(f"Event missing required field {e}: {event.get('event_id', 'unknown')}")
                    self.metrics['events_failed'] += 1
            
            df = pl.DataFrame(flattened, infer_schema_length=10000)
            
            # Convert timestamp
            df = df.with_columns([
                pl.col("timestamp").str.to_datetime().alias("timestamp")
            ])
            
            elapsed = (datetime.now() - start_time).total_seconds()
            logger.info(f"Load completed in {elapsed:.2f}s")
            
            return df
            
        except Exception as e:
            logger.error(f"Failed to load events: {str(e)}")
            raise
    
    def run_quality_checks(self, df: pl.DataFrame) -> Tuple[bool, List[str]]:
        """Run data quality validations."""
        logger.info("Running data quality checks...")
        issues = []
        
        try:
            config = self.config['quality_checks']
            
            # Check minimum event count
            if len(df) < config['min_events']:
                issues.append(f"Too few events: {len(df)} < {config['min_events']}")
            
            # Check for required event types
            event_types = df['event_type'].unique().to_list()
            missing_types = set(config['required_event_types']) - set(event_types)
            if missing_types:
                issues.append(f"Missing required event types: {missing_types}")
            
            # Check null percentages
            for col in df.columns:
                null_pct = df[col].is_null().mean()
                if null_pct > config['max_null_percentage']:
                    issues.append(f"Column {col} has {null_pct:.1%} nulls (threshold: {config['max_null_percentage']:.1%})")
            
            # Check timestamp validity
            now = datetime.now()
            future_events = df.filter(
                pl.col("timestamp") > now
            )
            if len(future_events) > 0:
                issues.append(f"Found {len(future_events)} events with future timestamps")
            
            # Check for duplicates
            duplicate_count = len(df) - df['event_id'].n_unique()
            if duplicate_count > 0:
                issues.append(f"Found {duplicate_count} duplicate event IDs")
            
            if issues:
                logger.warning(f"Quality check found {len(issues)} issues:")
                for issue in issues:
                    logger.warning(f"  - {issue}")
                return False, issues
            else:
                logger.info("All quality checks passed")
                return True, []
                
        except Exception as e:
            logger.error(f"Quality checks failed: {str(e)}")
            return False, [f"Quality check error: {str(e)}"]
    
    def clean_and_enrich(self, df: pl.DataFrame) -> pl.DataFrame:
        """Clean and enrich data with monitoring."""
        logger.info("Cleaning and enriching data...")
        
        try:
            # Extract date components
            df = df.with_columns([
                pl.col("timestamp").dt.date().alias("event_date"),
                pl.col("timestamp").dt.hour().alias("event_hour"),
                pl.col("timestamp").dt.weekday().alias("day_of_week")
            ])
            
            # Remove duplicates
            before_count = len(df)
            df = df.unique(subset=["event_id"])
            removed = before_count - len(df)
            
            if removed > 0:
                logger.warning(f"Removed {removed} duplicate events")
            
            self.metrics['events_cleaned'] = len(df)
            
            logger.info(f"After cleaning: {len(df):,} events")
            return df
            
        except Exception as e:
            logger.error(f"Cleaning failed: {str(e)}")
            raise
    
    def aggregate_daily_metrics(self, df: pl.DataFrame) -> pl.DataFrame:
        """Calculate daily metrics with validation."""
        logger.info("Calculating daily metrics...")
        
        try:
            # DAU
            dau = (
                df.filter(pl.col("event_type") == "session_start")
                .group_by("event_date")
                .agg([pl.col("player_id").n_unique().alias("dau")])
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
                logger.warning("No purchase events found")
                purchase_metrics = pl.DataFrame({
                    "event_date": [],
                    "total_purchases": [],
                    "total_revenue": [],
                    "paying_users": []
                })
            
            # Merge all metrics
            daily_metrics = dau.join(session_metrics, on="event_date", how="left")
            daily_metrics = daily_metrics.join(purchase_metrics, on="event_date", how="left")
            
            # Fill nulls
            daily_metrics = daily_metrics.fill_null(0)
            
            # Calculate derived metrics
            daily_metrics = daily_metrics.with_columns([
                (pl.col("total_revenue") / pl.col("dau")).alias("arpu"),
                (pl.col("paying_users") / pl.col("dau") * 100).alias("conversion_rate"),
                (pl.col("total_sessions") / pl.col("dau")).alias("sessions_per_user")
            ])
            
            logger.info(f"Generated metrics for {len(daily_metrics)} days")
            return daily_metrics
            
        except Exception as e:
            logger.error(f"Aggregation failed: {str(e)}")
            raise
    
    def calculate_retention(self, df: pl.DataFrame) -> pl.DataFrame:
        """Calculate retention cohorts with error handling."""
        logger.info("Calculating retention metrics...")
        
        try:
            # Implementation from original etl_pipeline.py
            # (keeping the same logic but with logging)
            session_starts = df.filter(pl.col("event_type") == "session_start")
            
            player_install_dates = (
                session_starts
                .group_by("player_id")
                .agg([
                    pl.col("event_date").min().alias("install_date")
                ])
            )
            
            player_activity = (
                session_starts
                .join(player_install_dates, on="player_id")
                .with_columns([
                    (pl.col("event_date") - pl.col("install_date")).dt.total_days().alias("days_since_install")
                ])
            )
            
            retention = (
                player_activity
                .group_by("install_date")
                .agg([
                    pl.col("player_id").n_unique().alias("cohort_size"),
                    pl.col("player_id").filter(pl.col("days_since_install") >= 1).n_unique().alias("d1_active"),
                    pl.col("player_id").filter(pl.col("days_since_install") >= 7).n_unique().alias("d7_active"),
                    pl.col("player_id").filter(pl.col("days_since_install") >= 30).n_unique().alias("d30_active")
                ])
                .with_columns([
                    (pl.col("d1_active") / pl.col("cohort_size") * 100).alias("d1_retention"),
                    (pl.col("d7_active") / pl.col("cohort_size") * 100).alias("d7_retention"),
                    (pl.col("d30_active") / pl.col("cohort_size") * 100).alias("d30_retention")
                ])
                .sort("install_date")
            )
            
            logger.info(f"Calculated retention for {len(retention)} cohorts")
            return retention
            
        except Exception as e:
            logger.error(f"Retention calculation failed: {str(e)}")
            raise
    
    def run(self, output_dir: str = "data/processed"):
        """Execute full ETL pipeline with monitoring."""
        logger.info("="*70)
        logger.info("Starting ETL Pipeline")
        logger.info("="*70)
        
        start_time = datetime.now()
        
        try:
            # Validate input
            self.validate_input_file()
            
            # Load
            df = self.load_events()
            
            # Quality checks
            passed, issues = self.run_quality_checks(df)
            if not passed and self.config.get('strict_mode', False):
                raise DataQualityError(f"Quality checks failed: {issues}")
            
            # Clean
            df = self.clean_and_enrich(df)
            
            # Save cleaned events
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            df.write_parquet(output_path / "events_cleaned.parquet")
            logger.info(f"Saved cleaned events to {output_path / 'events_cleaned.parquet'}")
            
            # Aggregate
            daily_metrics = self.aggregate_daily_metrics(df)
            daily_metrics.write_parquet(output_path / "daily_metrics.parquet")
            logger.info(f"Saved daily metrics to {output_path / 'daily_metrics.parquet'}")
            
            # Retention
            retention = self.calculate_retention(df)
            retention.write_parquet(output_path / "retention_cohorts.parquet")
            logger.info(f"Saved retention data to {output_path / 'retention_cohorts.parquet'}")
            
            # Calculate total time
            elapsed = (datetime.now() - start_time).total_seconds()
            self.metrics['processing_time_seconds'] = elapsed
            
            # Log summary
            logger.info("="*70)
            logger.info("ETL Pipeline Completed Successfully")
            logger.info("="*70)
            logger.info(f"Events loaded: {self.metrics['events_loaded']:,}")
            logger.info(f"Events cleaned: {self.metrics['events_cleaned']:,}")
            logger.info(f"Events failed: {self.metrics['events_failed']}")
            logger.info(f"Processing time: {elapsed:.2f}s")
            logger.info(f"Throughput: {self.metrics['events_loaded']/elapsed:.0f} events/sec")
            logger.info("="*70)
            
            return True
            
        except Exception as e:
            logger.error(f"Pipeline failed: {str(e)}")
            logger.error("="*70)
            raise


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Production ETL Pipeline")
    parser.add_argument("--input", type=str, required=True, help="Input JSONL file")
    parser.add_argument("--output", type=str, default="data/processed", help="Output directory")
    parser.add_argument("--config", type=str, help="Config YAML file")
    args = parser.parse_args()
    
    try:
        pipeline = EventETLPipeline(args.input, args.config)
        pipeline.run(output_dir=args.output)
    except Exception as e:
        logger.error(f"Pipeline execution failed: {str(e)}")
        sys.exit(1)
