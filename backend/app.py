from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from schemas.models import db
import os

def create_app(config_class=Config):
    """Create and configure Flask application"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Initialize Flask extensions
    db.init_app(app)
    
    # Enable CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": app.config.get('CORS_ORIGINS', 'http://localhost:3000'),
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Initialize JWT
    jwt = JWTManager(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # ===== BASIC ROUTES =====
    
    @app.route('/api/health', methods=['GET'])
    def health():
        """Health check endpoint"""
        return jsonify({
            'status': 'OK',
            'message': 'Load Forecasting API is running'
        }), 200
    
    @app.route('/api/status', methods=['GET'])
    def status():
        """Detailed status endpoint"""
        return jsonify({
            'status': 'running',
            'version': '1.0.0',
            'database': 'connected',
            'environment': app.config.get('FLASK_ENV', 'unknown')
        }), 200
    
    # ===== ERROR HANDLERS =====
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(500)
    def server_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({'error': 'Access forbidden'}), 403
    
    # ===== BLUEPRINT REGISTRATION =====
    
    
    from routes.auth import auth_bp
    from routes.predictions import pred_bp
    # from routes.admin import admin_bp
    # from routes.feedback import feedback_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(pred_bp, url_prefix='/api/predict')
    # app.register_blueprint(admin_bp, url_prefix='/api/admin')
    # app.register_blueprint(feedback_bp, url_prefix='/api/feedback')
    print(app.url_map)

    return app

if __name__ == '__main__':
    app = create_app()
    print("Starting Load Forecasting API...")
    print("Server running on http://localhost:5000")
    print("Health check: http://localhost:5000/api/health")
    app.run(debug=True, port=5000)
