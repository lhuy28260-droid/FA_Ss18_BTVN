# app/services/enrollment.py
from sqlalchemy.orm import Session
from app.models.enrollment import Student, Course, Enrollment
from app.schemas.enrollment import EnrollmentInputSchema
from fastapi import HTTPException, status

class EnrollmentService:

    @staticmethod
    def process_enrollment(payload: EnrollmentInputSchema, db: Session) -> Enrollment:
        """Thực thi đầy đủ 6 quy tắc nghiệp vụ cốt lõi trước khi tạo bản ghi mới"""
        
        # Quy tắc 1: Kiểm tra sinh viên phải tồn tại
        student = db.query(Student).filter(Student.id == payload.student_id).first()
        if student is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Thao tác thất bại: Mã số sinh viên không tồn tại trên hệ thống!"
            )

        # Quy tắc 2: Kiểm tra khóa học phải tồn tại
        course = db.query(Course).filter(Course.id == payload.course_id).first()
        if course is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Thao tác thất bại: Mã số khóa học không tồn tại trên hệ thống!"
            )

        # Quy tắc 3: Sinh viên phải có trạng thái ACTIVE
        if student.status != "ACTIVE":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Từ chối xử lý: Sinh viên hiện tại đã ngừng học (INACTIVE)!"
            )

        # Quy tắc 4: Khóa học phải có trạng thái OPEN
        if course.status != "OPEN":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Từ chối xử lý: Khóa học hiện tại đang ở trạng thái đóng (CLOSED)!"
            )

        # Quy tắc 5: Sinh viên không được đăng ký trùng một khóa học (Duyệt mảng/Dò tìm bản ghi)
        is_already_enrolled = db.query(Enrollment).filter(
            Enrollment.student_id == payload.student_id,
            Enrollment.course_id == payload.course_id
        ).first()
        
        if is_already_enrolled is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Vi phạm ràng buộc: Sinh viên đã đăng ký tham gia khóa học này trước đó!"
            )

        # Quy tắc 6: Số lượng đăng ký hiện tại phải nhỏ hơn max_students
        current_enrollment_count = db.query(Enrollment).filter(
            Enrollment.course_id == payload.course_id
        ).count()
        
        if current_enrollment_count >= course.max_students:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Sự cố quá tải: Khóa học đã đủ số lượng học viên tối đa đăng ký!"
            )

        # HỢP LỆ TOÀN VẸN: Tiến hành mở khối try...except lưu trữ vĩnh viễn vào MySQL
        try:
            new_enrollment = Enrollment(
                student_id=payload.student_id,
                course_id=payload.course_id
            )
            db.add(new_enrollment)
            db.commit()          # Lưu thật và chốt giao dịch xuống MySQL
            db.refresh(new_enrollment)
            return new_enrollment
        except Exception as err:
            db.rollback()        # Hoàn tác ngay lập tức để bảo vệ dữ liệu nếu có lỗi mạng
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Lỗi xung đột hệ thống cơ sở dữ liệu: {str(err)}"
            )