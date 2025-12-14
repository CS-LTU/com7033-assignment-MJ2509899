# NeuroGuard - Stroke Prediction Data Management System

This project contains a secure web application with a React frontend and a Python Flask backend.

## Folder Structure

*   `frontend/`: React application source code.
*   `backend/`: Python Flask API, SQLite (Users), and MongoDB (Patients) logic.

## 1. Setup & Run Backend (Python)

**Prerequisites:** Python 3.8+, MongoDB installed and running locally.

1.  Navigate to the backend folder:
    ```bash
    cd backend
    ```
2.  Create a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Initialize the SQLite database (for users):
    ```bash
    python init_db.py
    ```
5.  Run the server:
    ```bash
    flask run
    ```
    The API will run at `http://localhost:5000`.

## 2. Setup & Run Frontend (React)

**Prerequisites:** Node.js and npm.

1.  Navigate to the project root.
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Run the development server:
    ```bash
    npm start
    ```

**Note:** By default, the frontend in this demo uses a `mockBackend` service to function without the Python server running. To connect to the real Flask API:
1.  Open `frontend/services/mockBackend.ts`.
2.  Replace the mock functions with actual `fetch` calls to `http://localhost:5000/api/...`.

## Security Features

*   **Authentication**: Passwords hashed using Bcrypt.
*   **Session**: Secure HttpOnly cookies (Flask Session).
*   **Database**: 
    *   SQLite for relational user data (SQL injection protected via parameterized queries).
    *   MongoDB for flexible patient health records.
*   **Sanitization**: Input validation on both client and server.
