import numpy as np
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.preprocessing import MinMaxScaler
import joblib
import os

class LSTMForecaster:
    """
    LSTM-based load forecasting model
    Predicts electricity load based on historical data
    """
    
    def __init__(self):
        self.model = None
        self.scaler_X = MinMaxScaler(feature_range=(0, 1))
        self.scaler_y = MinMaxScaler(feature_range=(0, 1))
    
    def build_model(self, input_shape, lstm_units=64, dropout_rate=0.2):
        """
        Build LSTM model architecture
        
        Args:
            input_shape: Number of input features
            lstm_units: Number of LSTM units
            dropout_rate: Dropout rate for regularization
        
        Returns:
            Compiled Keras model
        """
        self.model = Sequential([
            LSTM(lstm_units, input_shape=(1, input_shape), return_sequences=True),
            Dropout(dropout_rate),
            LSTM(lstm_units // 2, return_sequences=False),
            Dropout(dropout_rate),
            Dense(32, activation='relu'),
            Dense(1)  # Output layer for continuous prediction
        ])
        
        optimizer = Adam(learning_rate=0.001)
        self.model.compile(optimizer=optimizer, loss='mse', metrics=['mae'])
        
        return self.model
    
    def train(self, X_train, y_train, epochs=50, batch_size=32, validation_split=0.2):
        """
        Train the LSTM model
        
        Args:
            X_train: Training features
            y_train: Training targets
            epochs: Number of training epochs
            batch_size: Batch size for training
            validation_split: Validation split ratio
        
        Returns:
            Training history
        """
        # Scale data
        X_scaled = self.scaler_X.fit_transform(X_train)
        y_scaled = self.scaler_y.fit_transform(y_train.reshape(-1, 1))
        
        # Reshape for LSTM [samples, timesteps, features]
        X_scaled = X_scaled.reshape((X_scaled.shape, 1, X_scaled.shape))
        
        # Train model
        history = self.model.fit(
            X_scaled, y_scaled,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=validation_split,
            verbose=1
        )
        
        return history
    
    def predict(self, X_test):
        """
        Make predictions on test data
        
        Args:
            X_test: Test features
        
        Returns:
            Predictions (unscaled)
        """
        X_scaled = self.scaler_X.transform(X_test)
        X_scaled = X_scaled.reshape((X_scaled.shape, 1, X_scaled.shape))
        
        predictions_scaled = self.model.predict(X_scaled, verbose=0)
        predictions = self.scaler_y.inverse_transform(predictions_scaled)
        
        return predictions.flatten()
    
    def save_model(self, filepath):
        """
        Save trained model and scalers
        
        Args:
            filepath: Path to save model
        """
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Save Keras model
        self.model.save(filepath)
        
        # Save scalers
        scaler_X_path = filepath.replace('.h5', '_scaler_X.pkl')
        scaler_y_path = filepath.replace('.h5', '_scaler_y.pkl')
        
        joblib.dump(self.scaler_X, scaler_X_path)
        joblib.dump(self.scaler_y, scaler_y_path)
        
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath):
        """
        Load pre-trained model and scalers
        
        Args:
            filepath: Path to load model
        """
        self.model = load_model(filepath)
        
        scaler_X_path = filepath.replace('.h5', '_scaler_X.pkl')
        scaler_y_path = filepath.replace('.h5', '_scaler_y.pkl')
        
        self.scaler_X = joblib.load(scaler_X_path)
        self.scaler_y = joblib.load(scaler_y_path)
        
        print(f"Model loaded from {filepath}")
