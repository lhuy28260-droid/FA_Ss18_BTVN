# main.py
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import engine, Base, get_db
from app.models.workshop import Student, Workshop, Registration
from app.schemas.workshop import (
    StudentCreateSchema, WorkshopCreateSchema, RegistrationInputSchema,
    StudentWorkshopsOutput, WorkshopStudentsOutput
)
from app.services.workshop import WorkshopService

app = FastAPI(title="Hệ thống Quản lý Đăng ký Workshop Sinh viên")

# Tự động đồng bộ tạo các bảng vật lý
Base.metadata.create_all(bind=engine)

# --- DANH SÁCH 8 API TỐI THIỂU QUY ĐỊNH ---

@app.post("/students", status_code=201)
def create_student(payload: StudentCreateSchema, db: Session = Depends(get_db)):
    # Check trùng code cổ điển
    if db.query(Student).filter(Student.student_code == payload.student_code).first():
        raise HTTPException(status_code=400, detail="Mã số sinh viên đã tồn tại!")
    new_s = Student(student_code=payload.student_code, full_name=payload.full_name, email=payload.email, status=payload.status)
    db.add(new_s)
    db.commit()
    return {"message": "Tạo mới sinh viên thành công!"}

@app.get("/students")
def get_all_students(db: Session = Depends(get_db)):
    return db.query(Student).all()

@app.post("/workshops", status_code=201)
def create_workshop(payload: WorkshopCreateSchema, db: Session = Depends(get_db)):
    new_w = Workshop(title=payload.title, description=payload.description, maximum_participants=payload.maximum_participants, status=payload.status, start_time=payload.start_time)
    db.add(new_w)
    db.commit()
    return {"message": "Tạo mới buổi workshop thành công!"}

@app.get("/workshops")
def get_all_workshops(db: Session = Depends(get_db)):
    return db.query(Workshop).all()

@app.get("/workshops/{id}")
def get_workshop_detail(id: int, db: Session = Depends(get_db)):
    w = db.query(Workshop).filter(Workshop.id == id).first()
    if not w: raise HTTPException(status_code=404, detail="Không tìm thấy workshop!")
    return w

@app.post("/registrations")
def register_workshop(payload: RegistrationInputSchema, db: Session = Depends(get_db)):
    # Gọi xuống tầng Service Layer xử lý logic chặn lỗi tập trung
    return WorkshopService.register_workshop_logic(payload=payload, db=db)

@app.get("/students/{id}/workshops", response_model=StudentWorkshopsOutput)
def get_workshops_of_student(id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == id).first()
    if not student: raise HTTPException(status_code=404, detail="Sinh viên không tồn tại!")
    return student

@app.get("/workshops/{id}/students", response_model=WorkshopStudentsOutput)
def get_students_of_workshop(id: int, db: Session = Depends(get_db)):
    workshop = db.query(Workshop).filter(Workshop.id == id).first()
    if not workshop: raise HTTPException(status_code=404, detail="Workshop không tồn tại!")
    return workshop

@app.put("/registrations/{id}/cancel")
def cancel_registration(id: int, db: Session = Depends(get_db)):
    return WorkshopService.cancel_registration_logic(reg_id=id, db=db)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)