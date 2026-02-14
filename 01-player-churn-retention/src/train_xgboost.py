"""
XGBoost baseline model for churn prediction.

Traditional gradient boosting approach with hyperparameter tuning.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import (
    roc_auc_score, accuracy_score, precision_score, 
    recall_score, f1_score, confusion_matrix, classification_report
)
import xgboost as xgb
import matplotlib.pyplot as plt
import seaborn as sns
import pickle


class XGBoostChurnModel:
    """XGBoost model for churn prediction."""
    
    def __init__(self, params: dict = None):
        """
        Args:
            params: XGBoost parameters
        """
        self.params = params or {
            'objective': 'binary:logistic',
            'max_depth': 6,
            'learning_rate': 0.1,
            'n_estimators': 100,
            'subsample': 0.8,
            'colsample_bytree': 0.8,
            'min_child_weight': 3,
            'gamma': 0.1,
            'random_state': 42,
            'eval_metric': 'auc'
        }
        self.model = None
        self.feature_importance = None
    
    def train(self, X_train: pd.DataFrame, y_train: pd.Series,
              X_val: pd.DataFrame = None, y_val: pd.Series = None):
        """Train XGBoost model."""
        print("Training XGBoost model...")
        
        self.model = xgb.XGBClassifier(**self.params)
        
        if X_val is not None and y_val is not None:
            eval_set = [(X_train, y_train), (X_val, y_val)]
            self.model.fit(
                X_train, y_train,
                eval_set=eval_set,
                verbose=10
            )
        else:
            self.model.fit(X_train, y_train)
        
        # Store feature importance
        self.feature_importance = pd.DataFrame({
            'feature': X_train.columns,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\nTraining complete")
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Predict churn probability."""
        return self.model.predict_proba(X)[:, 1]
    
    def evaluate(self, X: pd.DataFrame, y: pd.Series, split_name: str = "Test") -> dict:
        """Evaluate model performance."""
        y_pred_proba = self.predict(X)
        y_pred = (y_pred_proba >= 0.5).astype(int)
        
        metrics = {
            'auc': roc_auc_score(y, y_pred_proba),
            'accuracy': accuracy_score(y, y_pred),
            'precision': precision_score(y, y_pred),
            'recall': recall_score(y, y_pred),
            'f1': f1_score(y, y_pred)
        }
        
        print(f"\n{split_name} Set Performance:")
        print(f"AUC: {metrics['auc']:.4f}")
        print(f"Accuracy: {metrics['accuracy']:.4f}")
        print(f"Precision: {metrics['precision']:.4f}")
        print(f"Recall: {metrics['recall']:.4f}")
        print(f"F1 Score: {metrics['f1']:.4f}")
        
        print(f"\n{split_name} Classification Report:")
        print(classification_report(y, y_pred))
        
        return metrics, y_pred_proba
    
    def plot_feature_importance(self, top_n: int = 20, output_dir: str = "output"):
        """Plot top feature importances."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        plt.figure(figsize=(10, 8))
        top_features = self.feature_importance.head(top_n)
        sns.barplot(data=top_features, x='importance', y='feature')
        plt.title(f'Top {top_n} Feature Importances')
        plt.xlabel('Importance')
        plt.tight_layout()
        plt.savefig(output_path / 'feature_importance.png', dpi=150)
        print(f"\nSaved feature importance plot to: {output_path / 'feature_importance.png'}")
    
    def plot_confusion_matrix(self, y_true, y_pred_proba, threshold=0.5, output_dir: str = "output"):
        """Plot confusion matrix."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        y_pred = (y_pred_proba >= threshold).astype(int)
        cm = confusion_matrix(y_true, y_pred)
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title('Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.tight_layout()
        plt.savefig(output_path / 'confusion_matrix.png', dpi=150)
        print(f"Saved confusion matrix to: {output_path / 'confusion_matrix.png'}")
    
    def save_model(self, filepath: str = "models/xgboost_model.pkl"):
        """Save trained model."""
        output_path = Path(filepath)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'wb') as f:
            pickle.dump(self.model, f)
        
        print(f"\nSaved model to: {output_path}")
    
    @classmethod
    def load_model(cls, filepath: str):
        """Load trained model."""
        with open(filepath, 'rb') as f:
            model = pickle.load(f)
        
        instance = cls()
        instance.model = model
        return instance


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Train XGBoost churn model")
    parser.add_argument("--features", type=str, default="data/features.csv")
    parser.add_argument("--labels", type=str, default="data/labels.csv")
    parser.add_argument("--test-size", type=float, default=0.2)
    args = parser.parse_args()
    
    # Load data
    print("Loading features...")
    X = pd.read_csv(args.features, index_col=0)
    y = pd.read_csv(args.labels, index_col=0).squeeze()
    
    print(f"Dataset: {X.shape[0]} players, {X.shape[1]} features")
    print(f"Churn rate: {y.mean():.1%}")
    
    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=args.test_size, random_state=42, stratify=y
    )
    
    # Further split train into train/val
    X_train, X_val, y_train, y_val = train_test_split(
        X_train, y_train, test_size=0.2, random_state=42, stratify=y_train
    )
    
    print(f"\nTrain: {len(X_train)} | Val: {len(X_val)} | Test: {len(X_test)}")
    
    # Train model
    model = XGBoostChurnModel()
    model.train(X_train, y_train, X_val, y_val)
    
    # Evaluate
    train_metrics, _ = model.evaluate(X_train, y_train, "Train")
    val_metrics, _ = model.evaluate(X_val, y_val, "Validation")
    test_metrics, test_proba = model.evaluate(X_test, y_test, "Test")
    
    # Visualizations
    model.plot_feature_importance(top_n=20)
    model.plot_confusion_matrix(y_test, test_proba)
    
    # Save model
    model.save_model()
    
    print("\n" + "="*50)
    print("XGBoost Baseline Complete")
    print(f"Test AUC: {test_metrics['auc']:.4f}")
    print("="*50)
