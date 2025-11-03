from sklearn.svm import SVR
import numpy as np
import joblib
import os

class TWVSRPredictor:
    """
    Twin Support Vector Regression for prediction intervals
    Creates upper and lower bounds for confidence intervals
    """
    
    def __init__(self, epsilon=0.1, C=100, kernel='rbf'):
        """
        Initialize TWSVR
        
        Args:
            epsilon: Epsilon parameter for SVR
            C: Regularization parameter
            kernel: Kernel type (rbf, linear, poly)
        """
        self.epsilon = epsilon
        self.C = C
        self.kernel = kernel
        
        # Two SVR models for upper and lower bounds
        self.svr_upper = SVR(kernel=kernel, C=C, epsilon=epsilon)
        self.svr_lower = SVR(kernel=kernel, C=C, epsilon=epsilon)
    
    def train(self, X_residuals, y_residuals):
        """
        Train TWSVR on LSTM residuals
        
        Args:
            X_residuals: Feature data (prediction inputs)
            y_residuals: Residuals from LSTM predictions
        """
        # Upper boundary: residuals + epsilon
        y_upper = y_residuals + self.epsilon
        self.svr_upper.fit(X_residuals, y_upper)
        
        # Lower boundary: residuals - epsilon
        y_lower = y_residuals - self.epsilon
        self.svr_lower.fit(X_residuals, y_lower)
        
        print("TWSVR models trained successfully")
    
    def predict_intervals(self, X_test, point_predictions):
        """
        Generate prediction intervals
        
        Args:
            X_test: Test features
            point_predictions: Point predictions from LSTM
        
        Returns:
            Tuple of (lower_bounds, upper_bounds)
        """
        lower_offsets = self.svr_lower.predict(X_test)
        upper_offsets = self.svr_upper.predict(X_test)
        
        lower_bounds = point_predictions + lower_offsets
        upper_bounds = point_predictions + upper_offsets
        
        return lower_bounds, upper_bounds
    
    def calculate_interval_width(self, X_test):
        """
        Calculate average prediction interval width
        
        Args:
            X_test: Test features
        
        Returns:
            Average interval width
        """
        dummy_predictions = np.zeros(len(X_test))
        lower, upper = self.predict_intervals(X_test, dummy_predictions)
        
        width = np.mean(upper - lower)
        return width
    
    def save_model(self, filepath):
        """
        Save trained TWSVR models
        
        Args:
            filepath: Path to save model
        """
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        models_dict = {
            'svr_upper': self.svr_upper,
            'svr_lower': self.svr_lower
        }
        
        joblib.dump(models_dict, filepath)
        print(f"TWSVR model saved to {filepath}")
    
    def load_model(self, filepath):
        """
        Load pre-trained TWSVR models
        
        Args:
            filepath: Path to load model
        """
        models_dict = joblib.load(filepath)
        self.svr_upper = models_dict['svr_upper']
        self.svr_lower = models_dict['svr_lower']
        
        print(f"TWSVR model loaded from {filepath}")
