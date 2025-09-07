from pydantic import BaseModel
from typing import Optional

class Employee(BaseModel):
    emp_id: int
    name: str
    department: str
    status: str
    training_hours: float
    completed_courses: int
    assigned_courses: int
    lat: Optional[float] = None
    lon: Optional[float] = None
    city: Optional[str] = None