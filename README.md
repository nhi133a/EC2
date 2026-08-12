# Chương trình lấy data từ API và lưu vào MySQL

## Cấu trúc project

```
api_to_mysql/
├── main.py             # File chạy chính
├── fetch_data.py       # Gọi API lấy data
├── database.py         # Kết nối MySQL, tạo bảng, lưu data
├── requirements.txt    # Danh sách thư viện
├── .env.example        # Mẫu file cấu hình
└── README.md
```

## Cách chạy

### 1. Cài thư viện
```bash
pip install -r requirements.txt
```

### 2. Cấu hình kết nối
Copy file `.env.example` thành `.env`:
```bash
cp .env.example .env
```
Sau đó mở `.env` và điền thông tin MySQL thật của bạn (host, user, password, tên database) và URL của API bạn muốn lấy data.

### 3. Chạy chương trình
```bash
python main.py
```

Chương trình sẽ tự động:
1. Tạo database nếu chưa có
2. Tạo bảng `api_records` nếu chưa có
3. Gọi API lấy data (mặc định demo dùng API JSONPlaceholder)
4. Lưu data vào MySQL (nếu chạy lại nhiều lần, data trùng `id` sẽ được **cập nhật** thay vì lỗi trùng khóa)

## Tùy chỉnh cho API/data thật của bạn

Đây là bản khung (template) dùng data mẫu từ `https://jsonplaceholder.typicode.com/posts` (có các trường `id`, `userId`, `title`, `body`). Để dùng với API thật của bạn, cần sửa 2 chỗ:

1. **`database.py` → hàm `create_table()`**: đổi tên bảng và các cột cho khớp với cấu trúc data thật.
2. **`database.py` → hàm `save_records()`**: đổi câu lệnh `INSERT` và cách map field cho khớp với các cột đã tạo ở bước 1.

Nếu API của bạn cần gửi API key hoặc header xác thực, có thể thêm vào hàm `fetch_from_api()` trong `fetch_data.py`, ví dụ:
```python
headers = {"Authorization": f"Bearer {os.getenv('API_KEY')}"}
response = requests.get(url, headers=headers, params=params, timeout=15)
```

## Lưu ý
- Cần cài MySQL Server và đang chạy sẵn trên máy (hoặc dùng MySQL từ xa/cloud).
- Nếu muốn tự động chạy định kỳ (vd: mỗi giờ), có thể dùng `cron` (Linux/Mac) hoặc Task Scheduler (Windows) để gọi `python main.py`.
