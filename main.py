
# Python không nói chuyện trực tiếp MySQL , Python -> PyMySQL - MySQL
# Driver chỉ có nhiệm vụ gửi câu SQL xuống Database
# ORM (object relational mapping) giống 1 phiên dich viên thông minh
# Trong SQLAlchemy: 1 bảng Databasse -> 1 class Python
# Session giống như người đại diện của Python
# Py tạo obj -> User(name="Huy",age=25) => Session nhận obj -> Session.add(user) 
# SQLAlchemy phân tích object -> tablename , col , value -> SQLAlchemy tự sinh SQL 
# SQLAl tự sinh SQL -> INSERT INTO -> Driver gửi SQL xuống DB -> DB lưu data -> commit()

# Py tạo obj -> user(name="Huy",age=25) -> Session nhận obj -> db.add(user)
# SQLAlchemy lấy cái hộp(box) -> phân tách Box ( Tablename , column , value) ->
# mặt khác SQLAlchemy tự sinh SQL ( INSERT INTO ) -> Driver gửi SQL xuống DB -> DB lưu data -> commit()

#Py -> obj(user(name="Huy",age=26)) -> Session nhận obj -> db.add(user) -> SQLAlchemy get box(user) -> tách (tablename , col , value) -> SQLAlchemy sinh SQL (INSERT INTO user) -> Driver lấy SQL đưa cho DB -> DB lưu data -> commit()
# Python làm việc với object / SQLAlchemy ORM -> convert object into câu lệnh SQL phù hợp -> DB chỉ nhận và thực thi SQL
# SQLAlchemy ko phải tồn tại để viết code SQL ngắn hơn , mà để giải quyết sự khác biệt giữa OOP và Database.
# Python(obj) -> SQLAlchemy ORM(Create Table , Sinh SQL) -> Driver(pymysql) chuyển SQL xuống DB -> Database nhận và xử lý data.

