from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np

def calculate_rmse(y_true, y_pred):
    """Calculate Root Mean Squared Error"""
    return np.sqrt(mean_squared_error(y_true, y_pred))

def calculate_mae(y_true, y_pred):
    """Calculate Mean Absolute Error"""
    return mean_absolute_error(y_true, y_pred)

def calculate_r2(y_true, y_pred):
    """Calculate R² Score"""
    return r2_score(y_true, y_pred)

def calculate_mape(y_true, y_pred):
    """Calculate Mean Absolute Percentage Error"""
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

def calculate_all_metrics(y_true, y_pred):
    """
    Calculate all performance metrics
    
    Args:
        y_true: Ground truth values
        y_pred: Predicted values
    
    Returns:
        Dictionary with all metrics
    """
    metrics = {
        'rmse': float(calculate_rmse(y_true, y_pred)),
        'mae': float(calculate_mae(y_true, y_pred)),
        'r2': float(calculate_r2(y_true, y_pred)),
        'mape': float(calculate_mape(y_true, y_pred))
    }
    
    return metrics

def calculate_interval_coverage(y_true, y_lower, y_upper):
    """
    Calculate prediction interval coverage
    Percentage of actual values within predicted bounds
    
    Args:
        y_true: Ground truth values
        y_lower: Lower bounds
        y_upper: Upper bounds
    
    Returns:
        Coverage percentage (0-1)
    """
    coverage = np.sum((y_true >= y_lower) & (y_true <= y_upper)) / len(y_true)
    return float(coverage)

def calculate_interval_width(y_lower, y_upper):
    """
    Calculate average prediction interval width
    
    Args:
        y_lower: Lower bounds
        y_upper: Upper bounds
    
    Returns:
        Average interval width
    """
    width = np.mean(y_upper - y_lower)
    return float(width)

def create_metrics_report(y_true, y_pred, y_lower=None, y_upper=None):
    """
    Create comprehensive metrics report
    
    Args:
        y_true: Ground truth values
        y_pred: Point predictions
        y_lower: Lower bounds (optional)
        y_upper: Upper bounds (optional)
    
    Returns:
        Dictionary with all metrics and analysis
    """
    report = calculate_all_metrics(y_true, y_pred)
    
    if y_lower is not None and y_upper is not None:
        report['interval_coverage'] = float(calculate_interval_coverage(y_true, y_lower, y_upper))
        report['interval_width'] = float(calculate_interval_width(y_lower, y_upper))
    
    return report
