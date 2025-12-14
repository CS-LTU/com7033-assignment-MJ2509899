import { Gender, WorkType, ResidenceType, SmokingStatus } from './types';

export const APP_NAME = "NeuroGuard";

export const DEFAULT_PATIENTS = [
  {
    id: "1",
    gender: Gender.Male,
    age: 67,
    hypertension: 0,
    heart_disease: 1,
    ever_married: "Yes",
    work_type: WorkType.Private,
    residence_type: ResidenceType.Urban,
    avg_glucose_level: 228.69,
    bmi: 36.6,
    smoking_status: SmokingStatus.FormerlySmoked,
    stroke: 1
  },
  {
    id: "2",
    gender: Gender.Female,
    age: 61,
    hypertension: 0,
    heart_disease: 0,
    ever_married: "Yes",
    work_type: WorkType.SelfEmployed,
    residence_type: ResidenceType.Rural,
    avg_glucose_level: 202.21,
    bmi: 28.1, // N/A handled as avg
    smoking_status: SmokingStatus.NeverSmoked,
    stroke: 1
  },
  {
    id: "3",
    gender: Gender.Male,
    age: 80,
    hypertension: 0,
    heart_disease: 1,
    ever_married: "Yes",
    work_type: WorkType.Private,
    residence_type: ResidenceType.Rural,
    avg_glucose_level: 105.92,
    bmi: 32.5,
    smoking_status: SmokingStatus.NeverSmoked,
    stroke: 1
  },
  {
    id: "4",
    gender: Gender.Female,
    age: 49,
    hypertension: 0,
    heart_disease: 0,
    ever_married: "Yes",
    work_type: WorkType.Private,
    residence_type: ResidenceType.Urban,
    avg_glucose_level: 171.23,
    bmi: 34.4,
    smoking_status: SmokingStatus.Smokes,
    stroke: 1
  },
  {
    id: "5",
    gender: Gender.Female,
    age: 79,
    hypertension: 1,
    heart_disease: 0,
    ever_married: "Yes",
    work_type: WorkType.SelfEmployed,
    residence_type: ResidenceType.Rural,
    avg_glucose_level: 174.12,
    bmi: 24.0,
    smoking_status: SmokingStatus.NeverSmoked,
    stroke: 1
  }
];