"""
database.py
------------
Quản lý kết nối tới MySQL và các thao tác tạo bảng, lưu data.
"""

import os
import logging
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()  # Đọc các biến trong file .env

logger = logging.getLogger(__name__)


def get_connection():
    """Tạo và trả về một kết nối MySQL mới."""
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", 3306)),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "api_data_db"),
        )
        return conn
    except Error as e:
        logger.error(f"Không thể kết nối MySQL: {e}")
        raise


def create_database_if_not_exists():
    """Tạo database nếu chưa tồn tại (kết nối không chỉ định database trước)."""
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", 3306)),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
        )
        cursor = conn.cursor()
        db_name = os.getenv("DB_NAME", "api_data_db")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`")
        conn.commit()
        cursor.close()
        conn.close()
        logger.info(f"Database '{db_name}' đã sẵn sàng.")
    except Error as e:
        logger.error(f"Lỗi khi tạo database: {e}")
        raise


def create_table():
    """
    Tạo bảng lưu data lấy từ API.
    Ví dụ dùng schema khớp với JSONPlaceholder /posts (userId, id, title, body).
    Bạn có thể sửa lại các cột cho khớp với API thật của mình.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS api_records (
            id INT PRIMARY KEY,
            user_id INT,
            title VARCHAR(500),
            body TEXT,
            fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    cursor.close()
    conn.close()
    logger.info("Bảng 'api_records' đã sẵn sàng.")


def save_records(records: list[dict]):
    """
    Lưu danh sách record vào bảng api_records.
    Dùng INSERT ... ON DUPLICATE KEY UPDATE để tránh lỗi khi id đã tồn tại
    (chạy lại chương trình nhiều lần sẽ không bị trùng/lỗi).
    """
    if not records:
        logger.info("Không có record nào để lưu.")
        return 0

    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        INSERT INTO api_records (id, user_id, title, body)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            user_id = VALUES(user_id),
            title = VALUES(title),
            body = VALUES(body)
    """

    data = [
        (r.get("id"), r.get("userId"), r.get("title"), r.get("body"))
        for r in records
    ]

    cursor.executemany(sql, data)
    conn.commit()
    saved_count = cursor.rowcount
    cursor.close()
    conn.close()

    logger.info(f"Đã lưu/cập nhật {len(data)} record vào database.")
    return saved_count
