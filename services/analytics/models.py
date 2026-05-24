import numpy as np

# Resilient PyTorch Imports
try:
    import torch
    import torch.nn as nn
except ImportError:
    import sys
    # Fallback mock for environment-agnostic structural execution
    class MockNNModule:
        def __init__(self, *args, **kwargs):
            super().__init__()
    class MockLinear:
        def __init__(self, *args, **kwargs): pass
    class MockLSTM:
        def __init__(self, *args, **kwargs): pass
        
    mock_torch = type(sys)('torch')
    mock_nn = type(sys)('torch.nn')
    
    # Attach subclasses directly to the mock module object
    mock_nn.Module = MockNNModule
    mock_nn.Linear = MockLinear
    mock_nn.LSTM = MockLSTM
    
    sys.modules['torch'] = mock_torch
    sys.modules['torch.nn'] = mock_nn
    import torch
    import torch.nn as nn


# Resilient Scikit-Learn Imports
try:
    from sklearn.preprocessing import StandardScaler
except ImportError:
    class StandardScaler:
        def fit(self, X):
            self.mean_ = X.mean(axis=0)
            self.scale_ = X.std(axis=0)
        def transform(self, X):
            return (X - self.mean_) / (self.scale_ + 1e-9)

from typing import Dict, Any, Tuple

class TemporalCognitiveRNN(nn.Module):

    """PyTorch LSTM module to process multi-variate daily behavioral sequences (attention index, sleep, notification frequency)."""
    def __init__(self, input_dim: int = 5, hidden_dim: int = 16, num_layers: int = 1):
        super(TemporalCognitiveRNN, self).__init__()
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_dim, 2)  # Output categories: [normal, overload]

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x shape: (batch_size, sequence_length, input_dim)
        lstm_out, _ = self.lstm(x)
        # Select the output of the final time step
        last_step_out = lstm_out[:, -1, :]
        logits = self.fc(last_step_out)
        return logits


class BehavioralDriftDetector:
    """Scikit-Learn wrapper to detect long-term behavioral changes (deviations from personalized base rates)."""
    def __init__(self, deviation_threshold: float = 2.0):
        self.threshold = deviation_threshold
        self.scaler = StandardScaler()
        self.baseline_fitted = False

    def establish_user_baseline(self, historical_metrics: np.ndarray) -> None:
        """Fits standard scaling parameters to establish a user's normal baseline behavior footprint."""
        if historical_metrics.shape[0] < 10:
            raise ValueError("Insufficient baseline epochs (minimum 10 required).")
        self.scaler.fit(historical_metrics)
        self.baseline_fitted = True

    def calculate_drift_score(self, current_metrics: np.ndarray) -> Tuple[float, bool]:
        """Calculates distance from baseline center. Triggers alert if distance exceeds threshold."""
        if not self.baseline_fitted:
            return 0.0, False

        # Scale the current day's metrics
        scaled_metrics = self.scaler.transform(current_metrics.reshape(1, -1))
        
        # Calculate Mahalanobis-like Euclidean distance on scaled metrics
        distance = float(np.linalg.norm(scaled_metrics))
        drift_detected = distance > self.threshold
        
        return distance, drift_detected
