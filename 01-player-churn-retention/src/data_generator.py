"""
Generate synthetic player behavior data for churn prediction.

Creates realistic player trajectories with sessions, levels, purchases, and engagement patterns.
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple
import uuid

import numpy as np
import pandas as pd
from faker import Faker

fake = Faker()
Faker.seed(42)
random.seed(42)
np.random.seed(42)


class PlayerBehaviorGenerator:
    """Generate player behavior sequences for churn modeling."""
    
    def __init__(self, num_players: int = 10000, observation_days: int = 14, prediction_window: int = 7):
        """
        Args:
            num_players: Number of players to generate
            observation_days: Days of behavior to observe
            prediction_window: Days ahead to predict churn
        """
        self.num_players = num_players
        self.observation_days = observation_days
        self.prediction_window = prediction_window
        self.start_date = datetime.now() - timedelta(days=observation_days + prediction_window)
        
    def _assign_player_segment(self) -> Dict:
        """Assign player to behavioral segment with associated parameters."""
        segment_type = random.choices(
            ["whale", "engaged", "casual", "at_risk", "dormant"],
            weights=[0.02, 0.15, 0.40, 0.23, 0.20]
        )[0]
        
        segments = {
            "whale": {
                "avg_sessions_per_day": 4.5,
                "session_duration_mean": 45,
                "session_duration_std": 15,
                "purchase_probability": 0.25,
                "avg_purchase_value": 15.0,
                "churn_probability": 0.05,
                "engagement_decay": 0.02
            },
            "engaged": {
                "avg_sessions_per_day": 2.5,
                "session_duration_mean": 30,
                "session_duration_std": 10,
                "purchase_probability": 0.08,
                "avg_purchase_value": 5.0,
                "churn_probability": 0.15,
                "engagement_decay": 0.03
            },
            "casual": {
                "avg_sessions_per_day": 0.8,
                "session_duration_mean": 15,
                "session_duration_std": 8,
                "purchase_probability": 0.02,
                "avg_purchase_value": 2.99,
                "churn_probability": 0.40,
                "engagement_decay": 0.08
            },
            "at_risk": {
                "avg_sessions_per_day": 0.4,
                "session_duration_mean": 10,
                "session_duration_std": 5,
                "purchase_probability": 0.01,
                "avg_purchase_value": 1.99,
                "churn_probability": 0.70,
                "engagement_decay": 0.15
            },
            "dormant": {
                "avg_sessions_per_day": 0.1,
                "session_duration_mean": 5,
                "session_duration_std": 3,
                "purchase_probability": 0.001,
                "avg_purchase_value": 0.99,
                "churn_probability": 0.90,
                "engagement_decay": 0.20
            }
        }
        
        profile = segments[segment_type].copy()
        profile["segment"] = segment_type
        return profile
    
    def _generate_daily_behavior(self, player: Dict, day_offset: int) -> Dict:
        """Generate behavior for a single day with realistic noise."""
        # Engagement decay over time with random variation
        decay_factor = 1.0 - (player["engagement_decay"] * day_offset)
        decay_factor = max(0.1, decay_factor)
        
        # Add daily random variation (good days/bad days)
        daily_mood = np.random.normal(1.0, 0.3)
        daily_mood = max(0.3, min(1.7, daily_mood))  # Clamp between 0.3 and 1.7
        
        # Number of sessions with engagement decay and daily variation
        expected_sessions = player["avg_sessions_per_day"] * decay_factor * daily_mood
        num_sessions = np.random.poisson(max(0.01, expected_sessions))
        
        # Stochastic churn check with noise
        base_churn_prob = player["churn_probability"] / 30
        # Add random noise to churn probability
        churn_noise = np.random.uniform(-0.15, 0.15)
        actual_churn_prob = max(0.001, min(0.99, base_churn_prob + churn_noise))
        
        if num_sessions == 0 and random.random() < actual_churn_prob:
            return None
        elif num_sessions == 0:
            # Even with 0 sessions, might still be "active" (app opened but didn't play)
            return {
                "sessions": 0,
                "playtime_seconds": 0,
                "levels_completed": 0,
                "purchases": 0,
                "revenue": 0.0
            }
        
        total_playtime = 0
        total_revenue = 0
        levels_completed = 0
        purchases = 0
        
        for _ in range(num_sessions):
            # Session duration
            duration_mean = player["session_duration_mean"] * 60 * daily_mood
            duration_std = player["session_duration_std"] * 60 * 1.5  # More variance
            duration = max(30, int(np.random.normal(duration_mean, duration_std)))
            total_playtime += duration
            
            # Levels completed (roughly 1 per 3 minutes)
            base_levels = duration / 180
            levels_completed += max(0, int(np.random.normal(base_levels, base_levels * 0.4)))
            
            # Purchase check with daily variation
            purchase_prob = player["purchase_probability"] * daily_mood
            if random.random() < purchase_prob:
                purchases += 1
                # More variance in purchase amounts
                total_revenue += np.random.exponential(player["avg_purchase_value"]) * np.random.uniform(0.5, 2.0)
        
        return {
            "sessions": num_sessions,
            "playtime_seconds": total_playtime,
            "levels_completed": levels_completed,
            "purchases": purchases,
            "revenue": round(total_revenue, 2)
        }
    
    def generate_dataset(self) -> pd.DataFrame:
        """Generate complete player behavior dataset."""
        print(f"Generating data for {self.num_players} players...")
        
        records = []
        
        for player_idx in range(self.num_players):
            player_id = str(uuid.uuid4())
            install_date = self.start_date + timedelta(days=random.randint(0, 7))
            player_profile = self._assign_player_segment()
            
            # Track if player churned with possibility of comeback
            churned = False
            inactive_days = 0
            last_activity_day = None
            
            # Generate observation period
            for day in range(self.observation_days):
                current_date = install_date + timedelta(days=day)
                
                if not churned:
                    daily_behavior = self._generate_daily_behavior(player_profile, day)
                    
                    if daily_behavior is None:
                        inactive_days += 1
                        # Consider churned after 3+ consecutive inactive days
                        if inactive_days >= 3:
                            churned = True
                    else:
                        inactive_days = 0
                        last_activity_day = day
                        record = {
                            "player_id": player_id,
                            "date": current_date.date(),
                            "days_since_install": day,
                            "segment": player_profile["segment"],
                            **daily_behavior
                        }
                        records.append(record)
                else:
                    # Small chance of comeback after churning
                    if random.random() < 0.05:  # 5% comeback chance
                        churned = False
                        inactive_days = 0
            
            # Determine if player churned in prediction window with noise
            if churned:
                # Even churned players might return
                churn_label = 1 if random.random() > 0.05 else 0
            else:
                # Check activity in prediction window
                future_active_days = 0
                for future_day in range(self.observation_days, self.observation_days + self.prediction_window):
                    future_behavior = self._generate_daily_behavior(player_profile, future_day)
                    if future_behavior is not None and future_behavior["sessions"] > 0:
                        future_active_days += 1
                
                # More nuanced churn definition
                if future_active_days == 0:
                    churn_label = 1 if random.random() > 0.1 else 0  # 10% false negative
                elif future_active_days >= 2:
                    churn_label = 0 if random.random() > 0.05 else 1  # 5% false positive
                else:
                    churn_label = 1 if random.random() > 0.5 else 0  # Ambiguous cases
            
            # Add churn label to all records for this player
            for record in records:
                if record["player_id"] == player_id:
                    record["churned"] = churn_label
        
        df = pd.DataFrame(records)
        print(f"Generated {len(df):,} daily observations")
        print(f"Churn rate: {df.groupby('player_id')['churned'].first().mean():.1%}")
        print(f"\nSegment distribution:")
        print(df.groupby('segment')['player_id'].nunique())
        
        return df
    
    def save_dataset(self, df: pd.DataFrame, output_dir: str = "data"):
        """Save dataset to CSV."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        filepath = output_path / "player_behavior.csv"
        df.to_csv(filepath, index=False)
        print(f"\nSaved dataset to: {filepath}")
        
        return filepath


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate player churn dataset")
    parser.add_argument("--players", type=int, default=10000, help="Number of players")
    parser.add_argument("--obs-days", type=int, default=14, help="Observation days")
    parser.add_argument("--pred-window", type=int, default=7, help="Prediction window days")
    args = parser.parse_args()
    
    generator = PlayerBehaviorGenerator(
        num_players=args.players,
        observation_days=args.obs_days,
        prediction_window=args.pred_window
    )
    
    df = generator.generate_dataset()
    generator.save_dataset(df)
