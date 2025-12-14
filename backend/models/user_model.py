from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    id: Optional[int]
    username: str
    email: str
    password: str
    role: str  # 'user' or 'doctor'

    def __post_init__(self):
        if self.role not in ['user', 'doctor']:
            raise ValueError("Role must be 'user' or 'doctor'")

    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        return cls(
            id=data.get('id'),
            username=data['username'],
            email=data['email'],
            password=data['password'],
            role=data['role']
        )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'role': self.role
        }

    def to_public_dict(self) -> dict:
        """Returns user data without password for API responses"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role
        }
