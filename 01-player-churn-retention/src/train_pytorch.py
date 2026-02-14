"""
PyTorch LSTM/GRU models for sequence-based churn prediction.

Uses player behavior sequences over time for temporal modeling.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import pickle

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, accuracy_score, precision_score, recall_score, f1_score

import matplotlib.pyplot as plt
import seaborn as sns


class PlayerSequenceDataset(Dataset):
    """Dataset for player behavior sequences."""
    
    def __init__(self, sequences, masks, labels):
        self.sequences = torch.FloatTensor(sequences)
        self.masks = torch.FloatTensor(masks)
        self.labels = torch.LongTensor(labels)
    
    def __len__(self):
        return len(self.labels)
    
    def __getitem__(self, idx):
        return self.sequences[idx], self.masks[idx], self.labels[idx]


class LSTMChurnModel(nn.Module):
    """LSTM-based churn prediction model."""
    
    def __init__(self, input_size, hidden_size=64, num_layers=2, dropout=0.3):
        super(LSTMChurnModel, self).__init__()
        
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        
        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0
        )
        
        self.fc = nn.Sequential(
            nn.Linear(hidden_size, 32),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(32, 2)
        )
    
    def forward(self, x, mask):
        # x: (batch, seq_len, features)
        # mask: (batch, seq_len)
        
        # LSTM forward pass
        lstm_out, _ = self.lstm(x)
        
        # Get last valid output using mask
        # Sum over sequence dimension with mask
        mask_expanded = mask.unsqueeze(-1).expand_as(lstm_out)
        masked_out = lstm_out * mask_expanded
        
        # Get last non-zero timestep
        seq_lengths = mask.sum(dim=1).long() - 1
        batch_size = x.size(0)
        
        # Gather last valid output for each sequence
        last_out = lstm_out[torch.arange(batch_size), seq_lengths]
        
        # Classification head
        logits = self.fc(last_out)
        return logits


class GRUChurnModel(nn.Module):
    """GRU-based churn prediction model."""
    
    def __init__(self, input_size, hidden_size=64, num_layers=2, dropout=0.3):
        super(GRUChurnModel, self).__init__()
        
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        
        self.gru = nn.GRU(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0
        )
        
        self.fc = nn.Sequential(
            nn.Linear(hidden_size, 32),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(32, 2)
        )
    
    def forward(self, x, mask):
        # GRU forward pass
        gru_out, _ = self.gru(x)
        
        # Get last valid output using mask
        seq_lengths = mask.sum(dim=1).long() - 1
        batch_size = x.size(0)
        
        last_out = gru_out[torch.arange(batch_size), seq_lengths]
        
        # Classification head
        logits = self.fc(last_out)
        return logits


class ChurnTrainer:
    """Trainer for sequence-based churn models."""
    
    def __init__(self, model, device='cpu'):
        self.model = model.to(device)
        self.device = device
        self.history = {'train_loss': [], 'val_loss': [], 'val_auc': []}
    
    def train_epoch(self, dataloader, optimizer, criterion):
        self.model.train()
        total_loss = 0
        
        for sequences, masks, labels in dataloader:
            sequences = sequences.to(self.device)
            masks = masks.to(self.device)
            labels = labels.to(self.device)
            
            optimizer.zero_grad()
            
            logits = self.model(sequences, masks)
            loss = criterion(logits, labels)
            
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
        
        return total_loss / len(dataloader)
    
    def evaluate(self, dataloader, criterion):
        self.model.eval()
        total_loss = 0
        all_preds = []
        all_labels = []
        
        with torch.no_grad():
            for sequences, masks, labels in dataloader:
                sequences = sequences.to(self.device)
                masks = masks.to(self.device)
                labels = labels.to(self.device)
                
                logits = self.model(sequences, masks)
                loss = criterion(logits, labels)
                
                total_loss += loss.item()
                
                probs = torch.softmax(logits, dim=1)[:, 1]
                all_preds.extend(probs.cpu().numpy())
                all_labels.extend(labels.cpu().numpy())
        
        avg_loss = total_loss / len(dataloader)
        auc = roc_auc_score(all_labels, all_preds)
        
        return avg_loss, auc, np.array(all_preds), np.array(all_labels)
    
    def train(self, train_loader, val_loader, epochs=50, lr=0.001, patience=10):
        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(self.model.parameters(), lr=lr)
        
        best_val_auc = 0
        patience_counter = 0
        
        print("Training model...")
        for epoch in range(epochs):
            train_loss = self.train_epoch(train_loader, optimizer, criterion)
            val_loss, val_auc, _, _ = self.evaluate(val_loader, criterion)
            
            self.history['train_loss'].append(train_loss)
            self.history['val_loss'].append(val_loss)
            self.history['val_auc'].append(val_auc)
            
            if (epoch + 1) % 5 == 0:
                print(f"Epoch {epoch+1}/{epochs} - Train Loss: {train_loss:.4f} - Val Loss: {val_loss:.4f} - Val AUC: {val_auc:.4f}")
            
            # Early stopping
            if val_auc > best_val_auc:
                best_val_auc = val_auc
                patience_counter = 0
                torch.save(self.model.state_dict(), 'models/best_model.pt')
            else:
                patience_counter += 1
                if patience_counter >= patience:
                    print(f"Early stopping at epoch {epoch+1}")
                    break
        
        # Load best model
        self.model.load_state_dict(torch.load('models/best_model.pt'))
        print(f"\nBest validation AUC: {best_val_auc:.4f}")
    
    def plot_training_history(self, output_dir='output'):
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Loss plot
        axes[0].plot(self.history['train_loss'], label='Train Loss')
        axes[0].plot(self.history['val_loss'], label='Val Loss')
        axes[0].set_xlabel('Epoch')
        axes[0].set_ylabel('Loss')
        axes[0].set_title('Training and Validation Loss')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # AUC plot
        axes[1].plot(self.history['val_auc'], label='Val AUC', color='green')
        axes[1].set_xlabel('Epoch')
        axes[1].set_ylabel('AUC')
        axes[1].set_title('Validation AUC')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output_path / 'training_history.png', dpi=150)
        print(f"Saved training history to: {output_path / 'training_history.png'}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Train PyTorch sequence models")
    parser.add_argument("--data", type=str, default="data/player_behavior.csv")
    parser.add_argument("--model", type=str, choices=['lstm', 'gru'], default='lstm')
    parser.add_argument("--hidden-size", type=int, default=64)
    parser.add_argument("--num-layers", type=int, default=2)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--lr", type=float, default=0.001)
    args = parser.parse_args()
    
    # Load data
    print("Loading data...")
    df = pd.read_csv(args.data)
    df['date'] = pd.to_datetime(df['date'])
    
    # Import feature engineer to create sequences
    from feature_engineering import ChurnFeatureEngineer
    
    engineer = ChurnFeatureEngineer()
    sequences, masks, labels = engineer.create_sequence_features(df)
    
    print(f"Sequences shape: {sequences.shape}")
    print(f"Churn rate: {labels.mean():.1%}")
    
    # Train/test split
    indices = np.arange(len(labels))
    train_idx, test_idx = train_test_split(indices, test_size=0.2, random_state=42, stratify=labels)
    train_idx, val_idx = train_test_split(train_idx, test_size=0.2, random_state=42, stratify=labels[train_idx])
    
    # Create datasets
    train_dataset = PlayerSequenceDataset(sequences[train_idx], masks[train_idx], labels[train_idx])
    val_dataset = PlayerSequenceDataset(sequences[val_idx], masks[val_idx], labels[val_idx])
    test_dataset = PlayerSequenceDataset(sequences[test_idx], masks[test_idx], labels[test_idx])
    
    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=args.batch_size)
    test_loader = DataLoader(test_dataset, batch_size=args.batch_size)
    
    print(f"Train: {len(train_dataset)} | Val: {len(val_dataset)} | Test: {len(test_dataset)}")
    
    # Create model
    input_size = sequences.shape[2]
    if args.model == 'lstm':
        model = LSTMChurnModel(input_size, args.hidden_size, args.num_layers)
        print(f"\nTraining LSTM model...")
    else:
        model = GRUChurnModel(input_size, args.hidden_size, args.num_layers)
        print(f"\nTraining GRU model...")
    
    print(f"Model parameters: {sum(p.numel() for p in model.parameters()):,}")
    
    # Train
    trainer = ChurnTrainer(model)
    trainer.train(train_loader, val_loader, epochs=args.epochs, lr=args.lr)
    
    # Evaluate on test set
    print("\nEvaluating on test set...")
    criterion = nn.CrossEntropyLoss()
    test_loss, test_auc, test_preds, test_labels = trainer.evaluate(test_loader, criterion)
    
    # Calculate metrics
    test_pred_labels = (test_preds >= 0.5).astype(int)
    acc = accuracy_score(test_labels, test_pred_labels)
    prec = precision_score(test_labels, test_pred_labels)
    rec = recall_score(test_labels, test_pred_labels)
    f1 = f1_score(test_labels, test_pred_labels)
    
    print(f"\nTest Set Performance:")
    print(f"AUC: {test_auc:.4f}")
    print(f"Accuracy: {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall: {rec:.4f}")
    print(f"F1 Score: {f1:.4f}")
    
    # Plot training history
    trainer.plot_training_history()
    
    # Save model
    Path('models').mkdir(exist_ok=True)
    torch.save(model.state_dict(), f'models/{args.model}_model.pt')
    print(f"\nSaved model to: models/{args.model}_model.pt")
    
    print("\n" + "="*50)
    print(f"{args.model.upper()} Model Complete")
    print(f"Test AUC: {test_auc:.4f}")
    print("="*50)
