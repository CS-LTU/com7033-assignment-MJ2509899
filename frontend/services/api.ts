/**
 * API Service Module for NeuroGuard Healthcare System
 * 
 * This module provides all API communication functions for:
 * - User authentication (login/register)
 * - Patient data management (CRUD operations)
 * - JWT token handling
 * 
 * All requests include authentication tokens and comprehensive
 * console logging for debugging purposes.
 */

// Backend API base URL - configured for local development
const SQLITE_API_URL = "http://localhost:5000/api";

// ==================== TypeScript Interfaces ====================

/** User account data structure */
export interface User {
  id: number;
  username: string;
  email: string;
  role: 'user' | 'doctor';  // Role determines access permissions
}

/** Authentication response structure */
export interface AuthResponse {
  token: string;  // JWT access token
  user: User;     // User profile data
}

// ==================== Authentication Functions ====================

/**
 * Authenticate user with email and password
 * 
 * @param email - User's email address
 * @param password - User's password (sent as plain text over HTTPS)
 * @returns Promise containing JWT token and user data
 * @throws Error if credentials are invalid or network fails
 */
export const loginUser = async (email: string, password: string): Promise<AuthResponse> => {
  console.log('🔵 LOGIN REQUEST:', `${SQLITE_API_URL}/auth/login`);
  console.log('📧 Email:', email);

  const res = await fetch(`${SQLITE_API_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  console.log('📡 Login response status:', res.status);

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    console.error('❌ Login error:', err);
    throw new Error(err.error || "Failed to login");
  }

  const data = await res.json();
  console.log('✅ Login successful, user:', data.user);
  return data;
};

/**
 * Register a new user account
 * 
 * @param username - Unique username for the account
 * @param email - User's email address (must be unique)
 * @param password - User's password (will be hashed on server)
 * @param role - User role ('user' for read-only, 'doctor' for full access)
 * @returns Promise containing JWT token and user data
 * @throws Error if registration fails (duplicate email/username)
 */
export const registerUser = async (
  username: string,
  email: string,
  password: string,
  role: 'user' | 'doctor'
): Promise<AuthResponse> => {
  const res = await fetch(`${SQLITE_API_URL}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, email, password, role }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.error || "Failed to register");
  }

  return res.json();
};

// ----- Patient (SQLite via backend API) -----
const PATIENT_API_URL = "http://localhost:5000/api"; // backend URL

export interface Patient {
  id?: number;
  name: string;
  age: number;
  gender: 'Male' | 'Female' | 'Other';
  hypertension: 0 | 1 | boolean;
  heart_disease: 0 | 1 | boolean;
  ever_married: 'Yes' | 'No';
  work_type: string;
  residence_type: 'Urban' | 'Rural';
  avg_glucose_level: number;
  bmi: number;
  smoking_status: 'formerly smoked' | 'never smoked' | 'smokes' | 'Unknown';
  stroke_prediction?: number;
  stroke?: 0 | 1;
}

// Fetch all patients
export const fetchPatients = async (token: string): Promise<Patient[]> => {
  if (!token) throw new Error("No token provided");

  console.log('🔵 FETCHING PATIENTS:', `${PATIENT_API_URL}/patients/`);
  console.log('🔑 Token:', token.substring(0, 20) + '...');

  const res = await fetch(`${PATIENT_API_URL}/patients/`, {
    headers: { Authorization: `Bearer ${token}` },
  });

  console.log('📡 Response status:', res.status);

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    console.error('❌ Fetch patients error:', err);
    throw new Error(err.error || "Failed to fetch patients");
  }

  const data = await res.json();
  console.log('✅ Patients received:', data.length);
  return data;
};

// Add patient
export const addPatient = async (patientData: Omit<Patient, "id">, token: string): Promise<Patient> => {
  const res = await fetch(`${PATIENT_API_URL}/patients/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(patientData),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.error || "Failed to add patient");
  }

  return res.json();
};

// Update patient
export const updatePatient = async (id: number, updates: Partial<Patient>, token: string): Promise<Patient> => {
  const res = await fetch(`${PATIENT_API_URL}/patients/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(updates),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.error || "Failed to update patient");
  }

  return res.json();
};

// Delete patient
export const deletePatient = async (id: number, token: string): Promise<boolean> => {
  const res = await fetch(`${PATIENT_API_URL}/patients/${id}`, {
    method: "DELETE",
    headers: { Authorization: `Bearer ${token}` },
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.error || "Failed to delete patient");
  }

  return true;
};

// Unified API export
const api = {
  login: loginUser,
  register: registerUser,
  getPatients: fetchPatients,
  fetchPatients,
  addPatient,
  updatePatient,
  deletePatient,
};

export default api;
