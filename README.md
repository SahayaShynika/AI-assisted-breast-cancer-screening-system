# Breast Cancer Detection System

An AI-powered breast cancer detection system using DenseNet-121 deep learning model with a modern web interface for doctors and patients.

## Features

- **AI-Powered Detection**: Uses DenseNet-121 convolutional neural network for accurate mammogram analysis
- **User Authentication**: Separate login systems for doctors and patients
- **Modern UI**: Attractive, responsive web interface built with Bootstrap 5
- **Database Integration**: MySQL database for storing user data and prediction results
- **Image Upload**: Drag-and-drop interface for uploading mammogram images
- **Real-time Analysis**: Instant AI-powered cancer detection and staging
- **Result Management**: Comprehensive result display with confidence scores and recommendations
- **Doctor Dashboard**: Overview of all patient scans and analytics
- **Patient Dashboard**: Personal scan history and health tips

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Machine Learning**: TensorFlow, Keras, DenseNet-121
- **Database**: MySQL with SQLAlchemy ORM
- **Image Processing**: OpenCV, PIL
- **Authentication**: Flask-Login, Werkzeug security

## Project Structure

```
MyFirstProject/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── database_setup.sql     # MySQL database schema
├── enhanced_train.py      # Enhanced model training script
├── enhanced_predict.py    # Enhanced prediction module
├── README.md             # This file
├── backend/              # Original backend files
│   ├── train.py          # Basic training script
│   └── predict.py        # Basic prediction script
├── frontend/             # Original frontend files
│   └── ui.py            # Basic UI (Tkinter)
├── utils/               # Utility modules
│   └── preprocess.py    # Data preprocessing
├── models/              # Trained model storage
├── templates/           # HTML templates
│   ├── base.html        # Base template
│   ├── login.html       # Login page
│   ├── register.html    # Registration page
│   ├── patient_dashboard.html
│   ├── doctor_dashboard.html
│   ├── upload.html      # Image upload page
│   └── result.html      # Results display page
├── static/              # Static files
│   └── uploads/         # Uploaded images
└── dataset/             # Training dataset
    ├── train/          # Training images
    │   ├── normal/
    │   ├── benign/
    │   └── malignant/
    └── test/           # Testing images
        ├── normal/
        ├── benign/
        └── malignant/
```

## Installation and Setup

### 1. Prerequisites

- Python 3.8 or higher
- MySQL Server
- Git

### 2. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd MyFirstProject

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Database Setup

```bash
# Create the database and tables
mysql -u root -p < database_setup.sql

# Or execute manually:
mysql -u root -p
CREATE DATABASE breast_cancer_db;
USE breast_cancer_db;
SOURCE database_setup.sql;
```

### 4. Train the Model

```bash
# Train the DenseNet-121 model
python enhanced_train.py

# This will:
# - Load and preprocess the dataset
# - Create and train the DenseNet-121 model
# - Save the trained model to models/densenet121_model.h5
# - Generate training history and metrics
```

### 5. Run the Application

```bash
# Start the Flask web application
python app.py

# The application will be available at:
# http://localhost:5000
```

## Usage

### For Patients

1. **Register**: Create a patient account with email and password
2. **Login**: Access your personal dashboard
3. **Upload**: Upload mammogram images using the drag-and-drop interface
4. **View Results**: Get instant AI analysis with confidence scores
5. **Track History**: View all previous scans and results

### For Doctors

1. **Register**: Create a doctor account
2. **Login**: Access the doctor dashboard
3. **View All Scans**: See all patient predictions and results
4. **Analytics**: View statistics and trends
5. **Manage Cases**: Track and follow up on critical cases

## Model Performance

The DenseNet-121 model is trained to classify mammograms into three categories:

- **Normal**: No signs of cancer detected
- **Benign**: Non-cancerous abnormalities detected
- **Malignant**: Cancerous abnormalities detected

### Training Metrics

- **Accuracy**: ~95% (varies based on dataset quality)
- **Input Size**: 224x224 pixels
- **Model Size**: ~80MB
- **Inference Time**: <1 second per image

## API Endpoints

- `GET /` - Redirect to login
- `GET/POST /login` - User authentication
- `GET/POST /register` - User registration
- `GET /dashboard` - User dashboard (role-based)
- `GET/POST /upload` - Image upload and analysis
- `GET /result/<id>` - View prediction results
- `GET /logout` - User logout

## Database Schema

### Users Table
- `id` - Primary key
- `email` - User email (unique)
- `password` - Hashed password
- `user_type` - 'doctor' or 'patient'
- `name` - Full name
- `phone_number` - Contact number
- `created_at` - Registration timestamp

### Predictions Table
- `id` - Primary key
- `user_id` - Foreign key to users table
- `image_path` - Uploaded image filename
- `prediction_result` - 'normal', 'benign', or 'malignant'
- `confidence_score` - AI confidence (0-1)
- `cancer_stage` - Determined cancer stage
- `created_at` - Prediction timestamp

## Security Features

- Password hashing with bcrypt
- Session-based authentication
- Role-based access control
- File upload validation
- SQL injection prevention
- XSS protection

## Future Enhancements

- [ ] Email notifications for critical cases
- [ ] Integration with DICOM format
- [ ] Mobile app development
- [ ] Telemedicine features
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Cloud deployment options

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This system is for educational and research purposes only. The AI predictions should not replace professional medical diagnosis. Always consult with qualified healthcare professionals for medical decisions and treatment plans.

## Contact

For questions or support, please contact the development team.

---

**Note**: Ensure you have proper medical datasets and comply with healthcare data regulations (HIPAA, GDPR, etc.) when using this system with real patient data.
