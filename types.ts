export enum Gender {
  Male = "Male",
  Female = "Female",
  Other = "Other"
}

export enum WorkType {
  Private = "Private",
  SelfEmployed = "Self-employed",
  GovtJob = "Govt_job",
  Children = "children",
  NeverWorked = "Never_worked"
}

export enum ResidenceType {
  Urban = "Urban",
  Rural = "Rural"
}

export enum SmokingStatus {
  FormerlySmoked = "formerly smoked",
  NeverSmoked = "never smoked",
  Smokes = "smokes",
  Unknown = "Unknown"
}

export interface Patient {
  id: string;
  gender: Gender;
  age: number;
  hypertension: 0 | 1;
  heart_disease: 0 | 1;
  ever_married: "Yes" | "No";
  work_type: WorkType;
  residence_type: ResidenceType;
  avg_glucose_level: number;
  bmi: number;
  smoking_status: SmokingStatus;
  stroke: 0 | 1;
}

export interface User {
  id: string;
  username: string;
  role: 'admin' | 'doctor';
}

export interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}