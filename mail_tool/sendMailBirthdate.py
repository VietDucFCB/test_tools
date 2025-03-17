import mysql.connector
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import os

current_directory = os.path.dirname(os.path.abspath(__file__))

log_file_path = os.path.join(current_directory, 'birthday_reminder.log')

logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="*******",
        database="dateofbirth"
    )
    cursor = conn.cursor()
    logging.info('Connected to MySQL database successfully.')
except mysql.connector.Error as err:
    logging.error(f'Error connecting to MySQL: {err}')
    raise

# Lấy ngày hiện tại

today = datetime.now().strftime('%m-%d')

# Truy vấn các bạn có sinh nhật hôm nay
try:
    query = "SELECT name FROM friends WHERE DATE_FORMAT(birthdate, '%m-%d') = %s"
    cursor.execute(query, (today,))
    friends = cursor.fetchall()
    logging.info('Query executed successfully.')
except mysql.connector.Error as err:
    logging.error(f'Error executing query: {err}')
finally:
    cursor.close()
    conn.close()
    logging.info('Connection closed.')

# Cấu hình thông tin Outlook
sender_email = "22280012@student.hcmus.edu.vn"
sender_password = "********"
receiver_email = "kkagiuma1@gmail.com"  # Bạn có thể thay đổi email người nhận nếu cần

# Xác định nội dung email
if friends:
    subject = "Birthday Reminder"
    body = "Today's birthdays:\n" + "\n".join([friend[0] for friend in friends])
    logging.info('Birthdays found: ' + ', '.join([friend[0] for friend in friends]))
else:
    subject = "Birthday Reminder - No Birthdays Today"
    body = "There are no birthdays today."
    logging.info('No birthdays today.')

# Tạo email
message = MIMEMultipart()
message['From'] = sender_email
message['To'] = receiver_email
message['Subject'] = subject
message.attach(MIMEText(body, 'plain'))

# Gửi email
try:
    server = smtplib.SMTP('smtp-mail.outlook.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    server.close()
    logging.info('Email sent successfully!')
except Exception as e:
    logging.error(f'Failed to send email: {e}')
