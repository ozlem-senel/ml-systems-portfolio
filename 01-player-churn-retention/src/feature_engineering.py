"""
Feature engineering for player churn prediction.

Transforms daily player behavior into time-series features for modeling.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, List


class ChurnFeatureEngineer:
    """Engineer features from player behavior sequences."""
    
    def __init__(self, lookback_days: int = 7):
        """
        Args:
            lookback_days: Number of recent days to use for features
        """
        self.lookback_days = lookback_days
    
    def create_aggregated_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create player-level aggregated features."""
        # Group by player
        player_features = df.groupby('player_id').agg({
            # Engagement features
            'sessions': ['sum', 'mean', 'std', 'max'],
            'playtime_seconds': ['sum', 'mean', 'std'],
            'levels_completed': ['sum', 'mean'],
            
            # Monetization features
            'purchases': ['sum', 'mean'],
            'revenue': ['sum', 'mean', 'max'],
            
            # Temporal features
            'days_since_install': ['max', 'count'],  # max = total days, count = active days
            
            # Target
            'churned': 'first'
        })
        
        # Flatten column names
        player_features.columns = ['_'.join(map(str, col)).strip('_') for col in player_features.columns]
        player_features = player_features.rename(columns={
            'days_since_install_max': 'total_days',
            'days_since_install_count': 'active_days',
            'churned_first': 'churned'
        })
        
        # Derived features
        player_features['activity_ratio'] = (
            player_features['active_days'] / player_features['total_days']
        ).fillna(0)
        
        player_features['avg_revenue_per_purchase'] = (
            player_features['revenue_sum'] / player_features['purchases_sum']
        ).fillna(0)
        
        player_features['is_payer'] = (player_features['purchases_sum'] > 0).astype(int)
        
        # Session engagement
        player_features['avg_playtime_per_session'] = (
            player_features['playtime_seconds_sum'] / player_features['sessions_sum']
        ).fillna(0)
        
        player_features['sessions_per_active_day'] = (
            player_features['sessions_sum'] / player_features['active_days']
        ).fillna(0)
        
        return player_features
    
    def create_recency_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create features based on recent behavior (last N days)."""
        df_sorted = df.sort_values(['player_id', 'days_since_install'])
        
        recent_features = []
        
        for player_id, group in df_sorted.groupby('player_id'):
            # Take last N days
            recent = group.tail(self.lookback_days)
            
            if len(recent) == 0:
                continue
            
            features = {
                'player_id': player_id,
                
                # Recent engagement
                'recent_sessions': recent['sessions'].sum(),
                'recent_playtime': recent['playtime_seconds'].sum(),
                'recent_active_days': len(recent),
                
                # Recent monetization
                'recent_revenue': recent['revenue'].sum(),
                'recent_purchases': recent['purchases'].sum(),
                
                # Trends
                'session_trend': self._calculate_trend(recent['sessions'].values),
                'playtime_trend': self._calculate_trend(recent['playtime_seconds'].values),
                'revenue_trend': self._calculate_trend(recent['revenue'].values),
                
                # Recency
                'days_since_last_session': group['days_since_install'].max() - recent['days_since_install'].max(),
                'days_since_last_purchase': (
                    group['days_since_install'].max() - 
                    recent[recent['purchases'] > 0]['days_since_install'].max()
                ) if recent['purchases'].sum() > 0 else 999
            }
            
            recent_features.append(features)
        
        return pd.DataFrame(recent_features)
    
    def create_sequence_features(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Create padded sequences for LSTM/GRU models.
        
        Returns:
            sequences: (n_players, max_seq_len, n_features)
            masks: (n_players, max_seq_len) - 1 for valid timesteps, 0 for padding
            labels: (n_players,)
        """
        df_sorted = df.sort_values(['player_id', 'days_since_install'])
        
        feature_cols = [
            'sessions', 'playtime_seconds', 'levels_completed',
            'purchases', 'revenue'
        ]
        
        sequences = []
        labels = []
        
        for player_id, group in df_sorted.groupby('player_id'):
            # Extract sequence
            seq = group[feature_cols].values
            sequences.append(seq)
            labels.append(group['churned'].iloc[0])
        
        # Pad sequences
        max_len = max(len(seq) for seq in sequences)
        n_features = len(feature_cols)
        
        padded_sequences = np.zeros((len(sequences), max_len, n_features))
        masks = np.zeros((len(sequences), max_len))
        
        for i, seq in enumerate(sequences):
            seq_len = len(seq)
            padded_sequences[i, :seq_len, :] = seq
            masks[i, :seq_len] = 1
        
        return padded_sequences, masks, np.array(labels)
    
    def _calculate_trend(self, values: np.ndarray) -> float:
        """Calculate linear trend slope."""
        if len(values) < 2:
            return 0.0
        
        x = np.arange(len(values))
        slope, _ = np.polyfit(x, values, 1)
        return slope
    
    def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create all features for traditional ML models."""
        print("Engineering features...")
        
        # Aggregated features
        agg_features = self.create_aggregated_features(df)
        print(f"Created {len(agg_features.columns)-1} aggregated features")
        
        # Recency features
        recency_features = self.create_recency_features(df)
        print(f"Created {len(recency_features.columns)-1} recency features")
        
        # Merge
        features = agg_features.reset_index().merge(
            recency_features, on='player_id', how='left'
        )
        
        # Replace inf and very large values
        features = features.replace([np.inf, -np.inf], np.nan)
        features = features.fillna(0)
        
        # Separate target
        y = features['churned']
        X = features.drop(columns=['churned', 'player_id'])
        
        print(f"Final feature set: {X.shape[1]} features, {X.shape[0]} players")
        print(f"Churn rate: {y.mean():.1%}")
        
        return X, y
    
    def save_features(self, X: pd.DataFrame, y: pd.Series, output_dir: str = "data"):
        """Save engineered features."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        X.to_csv(output_path / "features.csv", index=True)
        y.to_csv(output_path / "labels.csv", index=True)
        
        print(f"\nSaved features to: {output_path}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Engineer churn prediction features")
    parser.add_argument("--input", type=str, default="data/player_behavior.csv")
    parser.add_argument("--lookback", type=int, default=7)
    args = parser.parse_args()
    
    # Load data
    df = pd.read_csv(args.input)
    df['date'] = pd.to_datetime(df['date'])
    
    # Engineer features
    engineer = ChurnFeatureEngineer(lookback_days=args.lookback)
    X, y = engineer.engineer_features(df)
    engineer.save_features(X, y)
    
    print("\nFeature summary:")
    print(X.describe())
