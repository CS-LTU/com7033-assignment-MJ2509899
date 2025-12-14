from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime

@dataclass
class Patient:
    id: Optional[int]
    name: str
    age: int
    gender: str  # 'Male', 'Female', 'Other'
    hypertension: bool
    heart_disease: bool
    ever_married: str  # "Yes" or "No"
    work_type: str  # 'Private', 'Self-employed', 'Govt_job', 'children', 'Never_worked'
    residence_type: str  # 'Urban', 'Rural'
    avg_glucose_level: float
    bmi: float
    smoking_status: str  # 'formerly smoked', 'never smoked', 'smokes', 'Unknown'
    stroke_prediction: Optional[float] = None  # Probability or binary
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if self.age < 0:
            raise ValueError("Age cannot be negative")
        if self.gender not in ['Male', 'Female', 'Other']:
            raise ValueError("Invalid gender")
        if self.work_type not in ['Private', 'Self-employed', 'Govt_job', 'children', 'Never_worked']:
            raise ValueError("Invalid work type")
        if self.residence_type not in ['Urban', 'Rural']:
            raise ValueError("Invalid residence type")
        if self.smoking_status not in ['formerly smoked', 'never smoked', 'smokes', 'Unknown']:
            raise ValueError("Invalid smoking status")
        if self.avg_glucose_level < 0:
            raise ValueError("Glucose level cannot be negative")
        if self.bmi < 0:
            raise ValueError("BMI cannot be negative")

    @classmethod
    def from_dict(cls, data: dict) -> 'Patient':
        return cls(
            id=data.get('id'),
            name=data['name'],
            age=data['age'],
            gender=data['gender'],
            hypertension=data['hypertension'],
            heart_disease=data['heart_disease'],
            ever_married=data['ever_married'],
            work_type=data['work_type'],
            residence_type=data['residence_type'],
            avg_glucose_level=data['avg_glucose_level'],
            bmi=data['bmi'],
            smoking_status=data['smoking_status'],
            stroke_prediction=data.get('stroke_prediction'),
            created_at=data.get('created_at', datetime.now()),
            updated_at=data.get('updated_at', datetime.now())
        )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'hypertension': self.hypertension,
            'heart_disease': self.heart_disease,
            'ever_married': self.ever_married,
            'work_type': self.work_type,
            'residence_type': self.residence_type,
            'avg_glucose_level': self.avg_glucose_level,
            'bmi': self.bmi,
            'smoking_status': self.smoking_status,
            'stroke_prediction': self.stroke_prediction,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def update_prediction(self, prediction: float):
        self.stroke_prediction = prediction
        self.updated_at = datetime.now()
