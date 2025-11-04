from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from schemas.models import db, User
from datetime import datetime
import re

# Create blueprint for auth routes
auth_bp = Blueprint('auth', __name__)

# ===== HELPER FUNCTIONS =====

def is_valid_email(email):
    """Validate email format"""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def is_valid_password(password):
    """
    Validate password strength
    At least 6 characters
    """
    return len(password) >= 6

# ===== AUTH ROUTES =====

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    
    Request JSON:
    {
        "username": "john_doe",
        "email": "john@example.com",
        "password": "securepassword123"
    }
    
    Response:
    {
        "message": "User registered successfully",
        "user_id": 1,
        "email": "john@example.com"
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({'error': 'Request body is empty'}), 400
        
        username = data.get('username', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        # Validation
        if not username:
            return jsonify({'error': 'Username is required'}), 400
        
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        
        if not password:
            return jsonify({'error': 'Password is required'}), 400
        
        if len(username) < 3:
            return jsonify({'error': 'Username must be at least 3 characters'}), 400
        
        if not is_valid_email(email):
            return jsonify({'error': 'Invalid email format'}), 400
        
        if not is_valid_password(password):
            return jsonify({'error': 'Password must be at least 6 characters'}), 400
        
        # Check if user already exists
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already registered'}), 409
        
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already taken'}), 409
        
        # Create new user
        new_user = User(
            username=username,
            email=email,
            role='user',  # Default role
            is_verified=True  # Auto-verify for development
        )
        
        # Hash password
        new_user.set_password(password)
        
        # Save to database
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            'message': 'User registered successfully',
            'user_id': new_user.user_id,
            'email': new_user.email,
            'username': new_user.username
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Registration failed: {str(e)}'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login user and return JWT token
    
    Request JSON:
    {
        "email": "john@example.com",
        "password": "securepassword123"
    }
    
    Response:
    {
        "access_token": "eyJhbGciOiJIUzI1NiIs...",
        "user_id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "role": "user"
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({'error': 'Request body is empty'}), 400
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        
        if not password:
            return jsonify({'error': 'Password is required'}), 400
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
        
        # Check if user exists and password is correct
        if not user:
            return jsonify({'error': 'Invalid email or password'}), 401
        
        if not user.check_password(password):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Check if user is active
        if not user.is_active:
            return jsonify({'error': 'User account is inactive'}), 403
        
        # Generate JWT token
        access_token = create_access_token(identity=str(user.user_id))
        
        return jsonify({
            'access_token': access_token,
            'user_id': user.user_id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'message': 'Login successful'
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Login failed: {str(e)}'}), 500


@auth_bp.route('/verify-token', methods=['GET'])
def verify_token():
    """
    Verify if a token is valid (protected endpoint)
    Headers required:
    Authorization: Bearer <token>
    
    Response:
    {
        "valid": true,
        "user_id": 1
    }
    """
    from flask_jwt_extended import jwt_required, get_jwt_identity
    
    @jwt_required()
    def check():
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'valid': True,
            'user_id': user_id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        }), 200
    
    return check()


@auth_bp.route('/user-info', methods=['GET'])
def get_user_info():
    """
    Get current logged-in user info (protected endpoint)
    Headers required:
    Authorization: Bearer <token>
    
    Response:
    {
        "user_id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "role": "user",
        "is_verified": true
    }
    """
    from flask_jwt_extended import jwt_required, get_jwt_identity
    
    @jwt_required()
    def info():
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify(user.to_dict()), 200
    
    return info()


@auth_bp.route('/change-password', methods=['POST'])
def change_password():
    """
    Change user password (protected endpoint)
    Headers required:
    Authorization: Bearer <token>
    
    Request JSON:
    {
        "old_password": "oldpass123",
        "new_password": "newpass456"
    }
    
    Response:
    {
        "message": "Password changed successfully"
    }
    """
    from flask_jwt_extended import jwt_required, get_jwt_identity
    
    @jwt_required()
    def change():
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Request body is empty'}), 400
        
        old_password = data.get('old_password', '')
        new_password = data.get('new_password', '')
        
        if not old_password:
            return jsonify({'error': 'Old password is required'}), 400
        
        if not new_password:
            return jsonify({'error': 'New password is required'}), 400
        
        # Verify old password
        if not user.check_password(old_password):
            return jsonify({'error': 'Old password is incorrect'}), 401
        
        # Validate new password
        if not is_valid_password(new_password):
            return jsonify({'error': 'New password must be at least 6 characters'}), 400
        
        # Set new password
        user.set_password(new_password)
        db.session.commit()
        
        return jsonify({'message': 'Password changed successfully'}), 200
    
    return change()


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """
    Logout user (frontend should delete token)
    
    Response:
    {
        "message": "Logout successful"
    }
    """
    return jsonify({'message': 'Logout successful. Please delete token from client'}), 200
