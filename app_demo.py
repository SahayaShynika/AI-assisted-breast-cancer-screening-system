from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import cv2
import numpy as np
import tensorflow as tf
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
# Use SQLite for demo instead of MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///breast_cancer_demo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Load the trained model
try:
    model = tf.keras.models.load_model('models/densenet121_model.h5')
    classes = ["normal", "benign", "malignant"]
    print("Model loaded successfully!")
except Exception as e:
    print(f"Model loading error: {e}")
    model = None
    classes = ["normal", "benign", "malignant"]

# Database Models
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)  # 'doctor' or 'patient'
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with predictions
    predictions = db.relationship('Prediction', backref='user', lazy=True)

class Prediction(db.Model):
    __tablename__ = 'predictions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    image_path = db.Column(db.String(200), nullable=False)
    prediction_result = db.Column(db.String(50), nullable=False)
    confidence_score = db.Column(db.Float, nullable=False)
    cancer_stage = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Helper function for role-based access
def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.user_type != role:
                flash('Access denied. You do not have permission to view this page.', 'danger')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Prediction function
def predict_image(image_path):
    if model is None:
        return "Model not loaded", 0.0, "Unknown"
    
    try:
        img = cv2.imread(image_path)
        if img is None:
            return "Invalid image", 0.0, "Unknown"
        
        img = cv2.resize(img, (224, 224))
        img = img / 255.0
        img = np.reshape(img, (1, 224, 224, 3))
        
        prediction = model.predict(img)[0]
        predicted_class = classes[np.argmax(prediction)]
        confidence = float(np.max(prediction))
        
        # Determine cancer stage based on prediction
        if predicted_class == "normal":
            stage = "No Cancer"
        elif predicted_class == "benign":
            stage = "Early Stage (Benign)"
        else:
            stage = "Advanced Stage (Malignant)"
        
        return predicted_class, confidence, stage
    except Exception as e:
        return f"Error: {str(e)}", 0.0, "Unknown"

# Routes
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user_type = request.form.get('user_type')
        
        user = User.query.filter_by(email=email, user_type=user_type).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash(f'Welcome back, {user.name}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        user_type = request.form.get('user_type')
        phone_number = request.form.get('phone_number')
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('register.html')
        
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered', 'danger')
            return render_template('register.html')
        
        hashed_password = generate_password_hash(password)
        new_user = User(
            name=name,
            email=email,
            password=hashed_password,
            user_type=user_type,
            phone_number=phone_number
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.user_type == 'doctor':
        # Get all patient predictions for doctor
        predictions = Prediction.query.order_by(Prediction.created_at.desc()).all()
        return render_template('doctor_dashboard.html', predictions=predictions)
    else:
        # Get patient's own predictions
        predictions = Prediction.query.filter_by(user_id=current_user.id).order_by(Prediction.created_at.desc()).all()
        return render_template('patient_dashboard.html', predictions=predictions)

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected', 'danger')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'danger')
            return redirect(request.url)
        
        if file:
            filename = secure_filename(f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}")
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Make prediction
            prediction_result, confidence, cancer_stage = predict_image(filepath)
            
            # Save to database
            new_prediction = Prediction(
                user_id=current_user.id,
                image_path=filename,
                prediction_result=prediction_result,
                confidence_score=confidence,
                cancer_stage=cancer_stage
            )
            
            db.session.add(new_prediction)
            db.session.commit()
            
            flash('Image uploaded and analyzed successfully!', 'success')
            return redirect(url_for('result', prediction_id=new_prediction.id))
    
    return render_template('upload.html')

@app.route('/result/<int:prediction_id>')
@login_required
def result(prediction_id):
    prediction = Prediction.query.get_or_404(prediction_id)
    
    # Check if user has permission to view this result
    if current_user.user_type == 'patient' and prediction.user_id != current_user.id:
        flash('Access denied', 'danger')
        return redirect(url_for('dashboard'))
    
    return render_template('result.html', prediction=prediction)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/train_model')
def train_model():
    # This route can be used to trigger model training
    # For now, we'll just show a message
    flash('Model training should be done separately. Please run train_model.py from the backend directory.', 'info')
    return redirect(url_for('dashboard'))

# Create sample users for demo
@app.route('/create_demo_users')
def create_demo_users():
    """Create demo users for testing"""
    
    # Check if users already exist
    if User.query.filter_by(email='doctor@demo.com').first():
        flash('Demo users already exist', 'info')
        return redirect(url_for('login'))
    
    # Create demo doctor
    doctor = User(
        name='Dr. Sarah Johnson',
        email='doctor@demo.com',
        password=generate_password_hash('doctor123'),
        user_type='doctor',
        phone_number='+1234567890'
    )
    
    # Create demo patient
    patient = User(
        name='Emily Smith',
        email='patient@demo.com',
        password=generate_password_hash('patient123'),
        user_type='patient',
        phone_number='+0987654321'
    )
    
    db.session.add(doctor)
    db.session.add(patient)
    db.session.commit()
    
    flash('Demo users created! Login as doctor@demo.com/doctor123 or patient@demo.com/patient123', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
