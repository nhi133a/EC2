"""
main.py
--------
Chương trình chính: gọi API lấy data -> lưu vào MySQL.

Cách chạy:
    1. pip install -r requirements.txt
    2. Copy .env.example thành .env và điền thông tin thật
    3. python main.py
"""

import logging
from database import create_database_if_not_exists, create_table, save_records
from fetch_data import fetch_from_api

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    try:
        # Bước 1: đảm bảo database và bảng đã tồn tại
        create_database_if_not_exists()
        create_table()

        # Bước 2: gọi API lấy data
        records = fetch_from_api()
        logger.info(f"Lấy được {len(records)} record từ API.")

        # Bước 3: lưu data vào MySQL
        save_records(records)

        logger.info("Hoàn tất!")

    except Exception as e:
        logger.error(f"Chương trình gặp lỗi: {e}")
        raise


if __name__ == "__main__":
    main()
