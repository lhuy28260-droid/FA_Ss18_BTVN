# app/services/workshop.py
from sqlalchemy.orm import Session
from app.models.workshop import Student, Workshop, Registration
from app.schemas.workshop import RegistrationInputSchema
from fastapi import HTTPException, status

class WorkshopService:
    
    @staticmethod
    def register_workshop_logic(payload: RegistrationInputSchema, db: Session):
        # 1. Kiểm tra thực thể tồn tại
        student = db.query(Student).filter(Student.id == payload.student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Không tìm thấy thông tin sinh viên!")
            
        if student.status != "ACTIVE":
            raise HTTPException(status_code=400, detail="Sinh viên không còn hoạt động, từ chối đăng ký!")

        workshop = db.query(Workshop).filter(Workshop.id == payload.workshop_id).first()
        if not workshop:
            raise HTTPException(status_code=404, detail="Buổi workshop không tồn tại trên hệ thống!")

        # 2. Kiểm tra trạng thái đóng của Workshop
        if workshop.status in ["CLOSED", "CANCELLED"]:
            raise HTTPException(status_code=400, detail="Workshop đã đóng hoặc bị hủy, không thể đăng ký!")

        # 3. Chặn đăng ký trùng lặp (Cổ điển)
        is_duplicated = db.query(Registration).filter(
            Registration.student_id == payload.student_id,
            Registration.workshop_id == payload.workshop_id,
            Registration.status == "SUCCESS"
        ).first()
        if is_duplicated:
            raise HTTPException(status_code=400, detail="Sinh viên đã đăng ký tham gia workshop này trước đó!")

        # 4. Chặn số người đăng ký vượt quá giới hạn
        current_seats = db.query(Registration).filter(
            Registration.workshop_id == payload.workshop_id,
            Registration.status == "SUCCESS"
        ).count()
        if current_seats >= workshop.maximum_participants:
            raise HTTPException(status_code=400, detail="Workshop đã đủ số lượng người tham gia tối đa!")

        # 5. Thực thi ghi dữ liệu an toàn
        try:
            new_reg = Registration(student_id=payload.student_id, workshop_id=payload.workshop_id)
            db.add(new_reg)
            db.commit()
            return {"message": "Đăng ký tham gia buổi workshop thành công!"}
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Lỗi giao dịch hệ thống: {str(e)}")

    @staticmethod
    def cancel_registration_logic(reg_id: int, db: Session):
        reg = db.query(Registration).filter(Registration.id == reg_id).first()
        if not reg:
            raise HTTPException(status_code=404, detail="Không tìm thấy lượt đăng ký yêu cầu!")
        try:
            reg.status = "CANCELLED"  # Thay đổi trạng thái thay vì xóa vật lý theo quyết định thiết kế
            db.commit()
            return {"message": "Hủy đăng ký thành công!"}
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))