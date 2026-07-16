# app/models/workshop.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Registration(Base):
    __tablename__ = "registrations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    workshop_id = Column(Integer, ForeignKey("workshops.id", ondelete="CASCADE"), nullable=False)
    registered_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    status = Column(String(30), default="SUCCESS", nullable=False) # SUCCESS, CANCELLED


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_code = Column(String(50), unique=True, nullable=False, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    status = Column(String(30), default="ACTIVE", nullable=False) # ACTIVE, INACTIVE

    # Thiết lập mối quan hệ Nhiều-Nhiều thông qua bảng trung gian registrations
    workshops = relationship("Workshop", secondary="registrations", back_populates="students")


class Workshop(Base):
    __tablename__ = "workshops"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(150), nullable=False)
    description = Column(String(255), nullable=True)
    maximum_participants = Column(Integer, nullable=False)
    status = Column(String(30), default="OPENNING", nullable=False) # OPENNING, CLOSED, CANCELLED
    start_time = Column(DateTime, nullable=False)

    students = relationship("Student", secondary="registrations", back_populates="workshops")