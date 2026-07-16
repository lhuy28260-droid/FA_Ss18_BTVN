# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

# Cấu hình chuỗi kết nối MySQL thực tế
DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/center_db"

# Mặc định sử dụng SQLite in-memory để sinh viên chạy file độc lập không bị crash lỗi kết nối:
DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Quản lý tốt vòng đời giải phóng Session kết nối (db_session)
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()