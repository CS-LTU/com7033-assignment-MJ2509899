# NeuroGuard - Stroke Prediction Healthcare System

A full-stack web application for healthcare professionals to manage patient data and predict stroke risk using machine learning algorithms. The system features role-based access control, real-time data visualization, and dual database architecture for scalability.

## 🎯 Features

- **User Authentication & Authorization**
  - JWT-based secure authentication
  - Role-based access control (Doctor, User, Admin)
  - Password hashing with bcrypt

- **Patient Management**
  - CRUD operations for patient records
  - Doctors: Full access to add, edit, and delete patients
  - Users: Read-only access to view patient data
  
- **Stroke Risk Prediction**
  - ML-based stroke probability calculation
  - Risk assessment based on multiple health factors
  - Real-time prediction updates

- **Data Visualization**
  - Interactive dashboards with charts and graphs
  - Patient statistics overview
  - Stroke prediction analytics using Recharts

- **Dual Database Architecture**
  - SQLite for primary operations (authentication & patient data)
  - MongoDB Atlas ready for cloud scalability
  - Seamless database switching capability

## 🛠️ Technology Stack

### Frontend
- **React 19.2.3** - UI framework
- **TypeScript** - Type-safe development
- **Vite 6.4.1** - Build tool and dev server
- **React Router 7.10.1** - Client-side routing
- **Recharts 3.5.1** - Data visualization
- **Tailwind CSS** - Utility-first styling
- **Lucide React 0.561.0** - Icon library

### Backend
- **Flask** - Python web framework
- **Flask-CORS** - Cross-origin resource sharing
- **Flask-JWT-Extended** - JWT authentication
- **Flask-Bcrypt** - Password hashing
- **Python 3.14.0** - Runtime environment

### Databases
- **SQLite** - Local relational database
- **MongoDB Atlas** - Cloud NoSQL database (configured)

## 📋 Prerequisites

- **Node.js** (v18 or higher)
- **Python 3.14** or higher
- **npm** or **yarn**
- **Git**

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd assignment
```

### 2. Backend Setup

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt

# Initialize database
cd backend
python init_db.py
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create environment file (optional)
# Add any necessary environment variables
```

### 4. Environment Configuration

Create a `.env` file in the `backend` directory:

```env
JWT_SECRET_KEY=your-secret-key-here
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/healthcare_db
```

## 🎮 Running the Application

### Start Backend Server

```bash
# From project root
cd backend
python app.py
```

The backend server will run on `http://localhost:5000`

### Start Frontend Development Server

```bash
# From project root
cd frontend
npm run dev
```

The frontend will run on `http://localhost:3000`

## 📱 Usage

### 1. Register a New Account

- Navigate to `http://localhost:3000/#/register`
- Fill in username, email, password
- Select role: `doctor` (full access) or `user` (read-only)
- Click "Register"

### 2. Login

- Navigate to `http://localhost:3000/#/login`
- Enter your credentials
- Click "Login"

### 3. Dashboard

After successful login, you'll be redirected to the dashboard where you can:

- **View Statistics**: See total patients, high-risk patients, and average risk scores
- **View Charts**: Analyze stroke predictions and risk factors distribution
- **Manage Patients** (Doctors only):
  - Click "Add New Patient" to create a record
  - Click "Edit" to modify patient information
  - Click "Delete" to remove a patient record

### 4. Patient Information Fields

When adding/editing patients, provide:
- **Personal Info**: Name, Age, Gender
- **Medical History**: Hypertension, Heart Disease
- **Lifestyle**: Marital Status, Work Type, Residence Type
- **Health Metrics**: Average Glucose Level, BMI
- **Habits**: Smoking Status

## 🔌 API Endpoints

### Authentication

```
POST /api/auth/register - Register new user
POST /api/auth/login    - User login
```

### Patients (Requires Authentication)

```
GET    /api/patients/          - Get all patients
POST   /api/patients/          - Add new patient (Doctor only)
PUT    /api/patients/<id>      - Update patient (Doctor only)
DELETE /api/patients/<id>      - Delete patient (Doctor only)
```

## 🗄️ Database Schema

### Users Table (SQLite)

| Column   | Type    | Description              |
|----------|---------|--------------------------|
| id       | INTEGER | Primary key              |
| username | TEXT    | Unique username          |
| email    | TEXT    | User email address       |
| password | TEXT    | Bcrypt hashed password   |
| role     | TEXT    | user/doctor/admin        |

### Patients Table (SQLite)

| Column              | Type      | Description                    |
|---------------------|-----------|--------------------------------|
| id                  | INTEGER   | Primary key                    |
| name                | TEXT      | Patient name                   |
| age                 | INTEGER   | Patient age                    |
| gender              | TEXT      | Male/Female/Other              |
| hypertension        | BOOLEAN   | Has hypertension (0/1)         |
| heart_disease       | BOOLEAN   | Has heart disease (0/1)        |
| ever_married        | TEXT      | Yes/No                         |
| work_type           | TEXT      | Work type category             |
| residence_type      | TEXT      | Urban/Rural                    |
| avg_glucose_level   | REAL      | Average glucose level          |
| bmi                 | REAL      | Body mass index                |
| smoking_status      | TEXT      | Smoking status category        |
| stroke_prediction   | REAL      | Predicted stroke probability   |
| created_at          | TIMESTAMP | Record creation time           |
| updated_at          | TIMESTAMP | Last update time               |

## 🧪 Testing

### Backend Tests

```bash
cd backend
python -m pytest tests/
```

### Frontend Tests

```bash
cd frontend
npm test
```

## 🔒 Security Features

- **Password Hashing**: All passwords are hashed using bcrypt
- **JWT Tokens**: Secure token-based authentication
- **Role-Based Access**: Granular permission system
- **CORS Protection**: Configured for specific origins
- **Input Validation**: Server-side validation for all inputs

## 📁 Project Structure

```
assignment/
├── backend/
│   ├── app.py                 # Flask application entry point
│   ├── init_db.py            # Database initialization script
│   ├── requirements.txt       # Python dependencies
│   ├── users.db              # SQLite database file
│   ├── db/
│   │   ├── db_mongo.py       # MongoDB operations
│   │   └── db_sql.py         # SQLite operations
│   ├── models/
│   │   ├── patient_model.py  # Patient data model
│   │   └── user_model.py     # User data model
│   └── routes/
│       ├── auth_routes.py    # Authentication endpoints
│       └── patient_routes.py # Patient CRUD endpoints
├── frontend/
│   ├── src/
│   ├── components/
│   │   ├── Layout.tsx        # Main layout wrapper
│   │   └── PatientModal.tsx  # Patient form modal
│   ├── context/
│   │   └── AuthContext.tsx   # Authentication state
│   ├── pages/
│   │   ├── Dashboard.tsx     # Main dashboard
│   │   ├── Login.tsx         # Login page
│   │   └── Register.tsx      # Registration page
│   ├── services/
│   │   └── api.ts            # API client
│   ├── App.tsx               # Root component
│   ├── types.ts              # TypeScript definitions
│   └── package.json          # Node dependencies
└── README.md                 # This file
```

## 🐛 Troubleshooting

### Backend won't start

- Ensure virtual environment is activated
- Check if port 5000 is available: `netstat -ano | findstr :5000`
- Verify all dependencies are installed: `pip list`

### Frontend won't start

- Clear node_modules and reinstall: `rm -rf node_modules && npm install`
- Check if port 3000 is available: `netstat -ano | findstr :3000`
- Verify Node.js version: `node --version`

### Database errors

- Delete `users.db` and run `python init_db.py` again
- Check database file permissions
- Ensure `backend/` directory exists

### CORS errors

- Verify backend is running on port 5000
- Check CORS configuration in `backend/app.py`
- Ensure frontend is accessing correct API URL

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## � Results & Screenshots

### Frontend Application
The React-based user interface provides an intuitive experience for healthcare professionals to manage patient data and view stroke predictions.

![Frontend Dashboard](screenshots/frontend.png)
*Interactive dashboard showing patient data visualization with charts and statistics*

### Backend API Server
Flask REST API server running on port 5000, handling authentication and patient data operations.

![Backend Server](screenshots/backend.png)
*Backend server console showing successful API initialization and MongoDB connection*

### MongoDB Atlas Database
Cloud-based NoSQL database storing 5,110 patient records with full CRUD operations.

![MongoDB Atlas](screenshots/mongo.png)
*MongoDB Atlas cluster showing the healthcare_db database with patient collection*

### SQLite Database
Local SQL database for user authentication and session management.

![SQLite Database](screenshots/sql.png)
*SQLite database structure showing user authentication tables*

---

## 📝 License

This project is part of an academic assignment.

## 👥 Authors

- Muzamil Habib - Full-stack development and database integration

## 🙏 Acknowledgments

- Medical data patterns based on healthcare research
- UI/UX inspired by modern healthcare systems
- MongoDB Atlas for cloud database hosting
- Built with ❤️ for healthcare professionals
