from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from schemas.models import db, Prediction
from datetime import datetime
import numpy as np
import joblib
from tensorflow.keras.models import load_model

pred_bp = Blueprint('predictions', __name__)

# Load models and scalers once at startup
lstm_model = load_model('trained_models/lstm_model.h5', compile=False)
svr_lower = joblib.load('trained_models/twsvr_lower.pkl')
svr_upper = joblib.load('trained_models/twsvr_upper.pkl')
scaler_X = joblib.load('trained_models/scaler_X.pkl')
scaler_y = joblib.load('trained_models/scaler_y.pkl')

@pred_bp.route('/single', methods=['POST'])
@jwt_required()
def predict_single():
    """
    Make a single load prediction given temperature, hour, date (YYYY-MM-DD)
    Protected! Must pass JWT token.
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    temperature = data.get('temperature')
    hour = data.get('hour')
    date_str = data.get('date')  # "YYYY-MM-DD"

    # Extract month & weekday from date string
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    month = dt.month
    weekday = dt.weekday()

    # Prepare and scale input features
    X_input = np.array([[temperature, hour, month, weekday]])
    X_scaled = scaler_X.transform(X_input)
    X_lstm = X_scaled.reshape((X_scaled.shape[0], 1, X_scaled.shape[1]))

    # LSTM point prediction
    y_pred_scaled = lstm_model.predict(X_lstm)
    y_pred = scaler_y.inverse_transform(y_pred_scaled.reshape(-1, 1)).flatten()

    # SVR interval predictions
    lower_scaled = svr_lower.predict(X_scaled)
    upper_scaled = svr_upper.predict(X_scaled)
    lower = scaler_y.inverse_transform(lower_scaled.reshape(-1, 1)).flatten()
    upper = scaler_y.inverse_transform(upper_scaled.reshape(-1, 1)).flatten()

    # Save prediction in DB
    prediction = Prediction(
        user_id=user_id,
        date=dt.date(),
        hour=hour,
        temperature=temperature,
        month=month,
        weekday=weekday,
        predicted_load=float(y_pred[0]),
        lower_bound=float(lower[0]),
        upper_bound=float(upper[0]),
        model_used="LSTM+TWSVR"
    )
    db.session.add(prediction)
    db.session.commit()

    return jsonify({
        "predicted_load": float(y_pred[0]),
        "lower_bound": float(lower[0]),
        "upper_bound": float(upper[0]),
        "confidence_interval": f"{lower[0]:.2f} - {upper[0]:.2f}"
    }), 200
