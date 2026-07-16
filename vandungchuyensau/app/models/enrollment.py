# app/models/enrollment.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Enrollment(Base):
    """Model đại diện cho bảng trung gian liên kết Nhiều - Nhiều (N-N)"""
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    enrolled_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class Student(Base):
    """Model đại diện cho bảng Student"""
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(100), nullable=False)
    status = Column(String(20), default="ACTIVE", nullable=False) # ACTIVE hoặc INACTIVE

    # Khai báo thuộc tính quan hệ Nhiều - Nhiều liên kết gián tiếp qua secondary
    courses = relationship("Course", secondary="enrollments", back_populates="students")


class Course(Base):
    """Model đại diện cho bảng Course"""
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    max_students = Column(Integer, nullable=False)
    status = Column(String(20), default="OPEN", nullable=False) # OPEN hoặc CLOSED

    students = relationship("Student", secondary="enrollments", back_populates="courses")