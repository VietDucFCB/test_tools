
# Birthday Reminder Tool

Công cụ này được thiết kế để **tự động** kiểm tra ngày sinh nhật của bạn bè/người thân trong cơ sở dữ liệu MySQL và **gửi email nhắc nhở**. Trong trường hợp không có ai sinh nhật hôm nay, hệ thống sẽ gửi email thông báo “No Birthdays Today”.

---

## 1. Giới Thiệu

1. **Kết nối MySQL**: Truy vấn bảng `friends` để tìm người có ngày sinh trùng với hôm nay.  
2. **Gửi Email**: Dùng SMTP (mặc định là Outlook) để gửi.  
3. **Ghi Log**: Tất cả hoạt động (kết nối DB, lỗi, kết quả truy vấn,…) được lưu tại `birthday_reminder.log`.

---

## 2. Cấu Trúc Dự Án
├── birthday_mail_tool.py # File code chính ├── birthday_reminder.log # File log (tự tạo sau khi chạy) ├── README.md # Hướng dẫn (file này)


- **birthday_mail_tool.py**: Chứa logic  
  - Kết nối DB  
  - Truy vấn ngày sinh  
  - Gửi mail  
  - Ghi log  
- **birthday_reminder.log**: File lưu kết quả chạy, bao gồm thời điểm gửi mail, lỗi, v.v.

---

## 3. Yêu Cầu Hệ Thống

1. **Python 3.x**  
2. **Thư viện cần thiết** (cài qua `pip install`):
   - `mysql-connector-python`
   - `smtplib` (mặc định trong Python)
   - `email` (mặc định trong Python)
   - `logging` (mặc định trong Python)
3. **MySQL** Server hoạt động, trong đó:
   - Database tên `dateofbirth`
   - Bảng `friends` có cột `name (VARCHAR)` và `birthdate (DATE)`

---

## 4. Thiết Lập Cơ Sở Dữ Liệu

```sql
CREATE DATABASE dateofbirth;
USE dateofbirth;

CREATE TABLE friends (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255),
  birthdate DATE
);

INSERT INTO friends (name, birthdate) VALUES
  ('Alice', '1995-09-01'),
  ('Bob', '1996-09-01');
```
## 5. Cách Dùng:
1.  Chỉnh sửa thông tin kết nối DB trong birthday_mail_tool.py:
```
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YOUR_DB_PASSWORD",
    database="dateofbirth"
)
```
2. Chỉnh sửa thông tin email:
```
sender_email = "22280012@student.hcmus.edu.vn"
sender_password = "YOUR_MAIL_PASSWORD"
receiver_email = "kkagiuma1@gmail.com"
```
3. Đổi sang SMTP khác (vd: Gmail) nếu cần:
```
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
```
4. Chạy tool:
```bash
python birthday_mail_tool.py
```
Tool sẽ kiểm tra ngày hiện tại, truy vấn DB, gửi mail thông báo.
Log được lưu trong file birthday_reminder.log.

## 6. Tự Động Hóa (Automation)
- Cron Job trên Linux/Mac:
```bash
crontab -e
# Thêm dòng:
0 8 * * * /usr/bin/python /path/to/birthday_mail_tool.py
```
  - Mỗi ngày 08:00, mail sẽ được gửi tự động.
- Task Scheduler trên Windows:
  - Tạo tác vụ mới, chọn thời điểm lặp (Daily), trỏ đến file .py.

## 7. Logging & Giải Quyết Sự Cố
- File birthday_reminder.log ghi lại:
  - Thời điểm kết nối DB
  - Lỗi (nếu có)
  - Kết quả truy vấn
  - Kết quả gửi mail
-Nếu gặp lỗi:
- Kiểm tra đúng thông tin DB & email.
  - Kiểm tra log để biết lỗi chi tiết.
## 8. Mở Rộng
- Thêm trường (phone, email) trong DB để gửi tin nhắn / gọi API khác.
- Định dạng email HTML thay vì plain text.
- Thông báo qua Slack/Telegram bằng webhook.

