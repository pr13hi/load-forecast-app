import pandas as pd
import numpy as np
from datetime import datetime

def preprocess_data(df):
    """
    Clean and preprocess raw data
    
    Args:
        df: Raw dataframe
    
    Returns:
        Processed dataframe
    """
    # Make a copy to avoid modifying original
    df = df.copy()
    
    # Convert date column
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    
    # Convert numeric columns
    df['Load'] = pd.to_numeric(df['Load'], errors='coerce')
    df['Temperature'] = pd.to_numeric(df['Temperature'], errors='coerce')
    
    # Remove rows with missing values
    df = df.dropna()
    
    # Extract time-based features
    df['Month'] = df['Date'].dt.month
    df['Weekday'] = df['Date'].dt.weekday
    df['Hour'] = df['Hour'].astype(int)
    
    return df

def prepare_features(data):
    """
    Prepare features and target for model training
    
    Args:
        data: Processed dataframe
    
    Returns:
        Tuple of (X, y) where X is features and y is target
    """
    # Features: Temperature, Hour, Month, Weekday
    X = data[['Temperature', 'Hour', 'Month', 'Weekday']].values
    
    # Target: Load
    y = data['Load'].values
    
    return X, y

def create_single_prediction_input(temperature, hour, date):
    """
    Create input array for single prediction
    
    Args:
        temperature: Temperature value
        hour: Hour (0-23)
        date: Date string (YYYY-MM-DD format)
    
    Returns:
        2D numpy array with [temperature, hour, month, weekday]
    """
    date_obj = pd.to_datetime(date)
    month = date_obj.month
    weekday = date_obj.weekday()
    
    # Return as 2D array for model input
    return np.array([[temperature, hour, month, weekday]])

def validate_prediction_input(temperature, hour, date):
    """
    Validate prediction input parameters
    
    Args:
        temperature: Temperature value
        hour: Hour (0-23)
        date: Date string
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    errors = []
    
    # Validate temperature
    if not isinstance(temperature, (int, float)):
        errors.append("Temperature must be a number")
    elif temperature < -50 or temperature > 60:
        errors.append("Temperature must be between -50°C and 60°C")
    
    # Validate hour
    if not isinstance(hour, int):
        errors.append("Hour must be an integer")
    elif hour < 0 or hour > 23:
        errors.append("Hour must be between 0 and 23")
    
    # Validate date
    try:
        date_obj = pd.to_datetime(date)
        if date_obj < datetime.now():
            errors.append("Date cannot be in the past")
    except:
        errors.append("Invalid date format (use YYYY-MM-DD)")
    
    is_valid = len(errors) == 0
    error_message = " | ".join(errors) if errors else None
    
    return is_valid, error_message
