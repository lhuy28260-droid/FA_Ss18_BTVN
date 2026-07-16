# app/schemas/enrollment.py
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

# Schema nhận dữ liệu đăng ký đầu vào từ Request Body
class EnrollmentInputSchema(BaseModel):
    student_id: int
    course_id: int

# Schema ánh xạ dữ liệu đầu ra khi đăng ký thành công
class EnrollmentSuccessResponse(BaseModel):
    id: int
    student_id: int
    course_id: int
    enrolled_at: datetime

    class Config:
        from_attributes = True

# --- Các lớp Schema DTO lồng nhau phục vụ API xem khóa học của sinh viên ---
class CompactCourseDTO(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True

class StudentCoursesOutputSchema(BaseModel):
    student_id: int
    full_name: str
    courses: List[CompactCourseDTO]

    class Config:
        from_attributes = True