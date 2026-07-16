# app/schemas/workshop.py
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime

class StudentCreateSchema(BaseModel):
    student_code: str = Field(min_length=3, max_length=50)
    full_name: str = Field(min_length=1)
    email: EmailStr
    status: str = "ACTIVE"

class WorkshopCreateSchema(BaseModel):
    title: str = Field(min_length=3, max_length=150)
    description: Optional[str] = None
    maximum_participants: int = Field(gt=0)
    status: str = "OPENNING"
    start_time: datetime

class RegistrationInputSchema(BaseModel):
    student_id: int
    workshop_id: int

# --- Các lớp Output lồng nhau phục vụ hiển thị (Nested JSON) ---
class CompactWorkshopResponse(BaseModel):
    id: int
    title: str
    status: str
    class Config: from_attributes = True

class CompactStudentResponse(BaseModel):
    id: int
    student_code: str
    full_name: str
    class Config: from_attributes = True

class StudentWorkshopsOutput(BaseModel):
    id: int
    full_name: str
    workshops: List[CompactWorkshopResponse]
    class Config: from_attributes = True

class WorkshopStudentsOutput(BaseModel):
    id: int
    title: str
    maximum_participants: int
    students: List[CompactStudentResponse]
    class Config: from_attributes = True