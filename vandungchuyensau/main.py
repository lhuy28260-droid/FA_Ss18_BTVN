import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

# Import các phân lớp thành phần nội bộ
from app.database import engine, Base, get_db
from app.models.enrollment import Student, Course, Enrollment
from app.schemas.enrollment import (
    EnrollmentInputSchema, EnrollmentSuccessResponse, StudentCoursesOutputSchema
)
from app.services.enrollment import EnrollmentService

app = FastAPI(title="Hệ thống API Đăng ký Khóa học Sinh viên")

# Tự động tạo cấu trúc bảng vật lý khi khởi chạy
Base.metadata.create_all(bind=engine)

# --- DỮ LIỆU SEED MẪU ĐỂ SINH VIÊN NGHIỆM THU DỄ DÀNG ---
@app.on_event("startup")
def seed_initial_data():
    db = SessionLocal()
    try:
        if db.query(Student).count() == 0:
            # Sinh viên ACTIVE & INACTIVE
            s1 = Student(full_name="Nguyễn Văn An", status="ACTIVE")
            s2 = Student(full_name="Trần Thị Bình", status="INACTIVE")
            # Khóa học OPEN & CLOSED kèm max_students giới hạn
            c1 = Course(name="FastAPI Basic", max_students=2, status="OPEN")
            c2 = Course(name="NextJS Advanced", max_students=30, status="CLOSED")
            
            db.add_all([s1, s2, c1, c2])
            db.commit()
    finally:
        db.close()


# =================================================================
# 5. DANH SÁCH CÁC API CẦN XÂY DỰNG
# =================================================================

# --- 1. API ĐĂNG KÝ KHÓA HỌC: POST /enrollments ---
@app.post("/enrollments", response_model=EnrollmentSuccessResponse, status_code=status.HTTP_201_CREATED)
def create_enrollment(payload: EnrollmentInputSchema, db: Session = Depends(get_db)):
    """API tiếp nhận thông tin và kiểm tra đầy đủ các điều kiện nghiệp vụ trước khi lưu"""
    return EnrollmentService.process_enrollment(payload=payload, db=db)


# --- 2. API XEM CÁC KHÓA HỌC CỦA SINH VIÊN: GET /students/{student_id}/courses ---
@app.get("/students/{student_id}/courses", response_model=StudentCoursesOutputSchema)
def get_student_courses_detail(student_id: int, db: Session = Depends(get_db)):
    """Tìm kiếm và trả về danh sách các khóa học đã đăng ký dạng lồng nhau (Nested Structure)"""
    student = db.query(Student).filter(Student.id == student_id).first()
    
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Thao tác thất bại: Sinh viên yêu cầu tra cứu không tồn tại!"
        )

    # Sử dụng kỹ thuật chuyển đổi dữ liệu thông qua Pydantic DTO mapping
    # Khớp chính xác mẫu Output mong đợi của đề bài ở mục 5
    return {
        "student_id": student.id,
        "full_name": student.full_name,
        "courses": student.courses
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)