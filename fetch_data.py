"""
fetch_data.py
--------------
Gọi API và trả về danh sách data (JSON).
"""

import os
import logging
import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


def fetch_from_api(url: str | None = None, params: dict | None = None) -> list[dict]:
    """
    Gọi GET request tới API và trả về data dạng list[dict].

    Args:
        url: URL của API. Nếu không truyền thì lấy từ biến môi trường API_URL.
        params: Query params tùy chọn (ví dụ phân trang, filter...).

    Returns:
        Danh sách các dict data lấy được từ API.
    """
    url = url or os.getenv("API_URL")
    if not url:
        raise ValueError("Chưa cấu hình API_URL trong file .env")

    logger.info(f"Đang gọi API: {url}")
    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()  # Ném lỗi nếu status code không phải 2xx

    data = response.json()

    # Một số API trả về dict bọc ngoài (vd: {"results": [...]})
    # thay vì trả về list trực tiếp. Xử lý linh hoạt trường hợp này.
    if isinstance(data, dict):
        for key in ("results", "data", "items"):
            if key in data:
                return data[key]
        return [data]  # trường hợp API trả về 1 object duy nhất

    return data
