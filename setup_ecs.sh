#!/bin/bash
# setup_ecs.sh
# Chạy script này TRÊN máy ECS (sau khi đã upload/clone folder project lên) để:
# 1. Cài Python venv + thư viện cần thiết
# 2. Tạo file .env từ mẫu (nếu chưa có)
#
# Cách dùng: cd vào thư mục gốc project rồi chạy: bash deploy/setup_ecs.sh

set -e

echo ">> Cập nhật hệ thống & cài Python..."
sudo apt update -y
sudo apt install -y python3 python3-venv python3-pip

echo ">> Tạo virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo ">> Cài thư viện từ requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

if [ ! -f .env ]; then
    echo ">> Tạo file .env từ .env.example (nhớ sửa lại thông tin thật)..."
    cp .env.example .env
    echo "   => Hãy chạy: nano .env  để điền DB_HOST, DB_USER, DB_PASSWORD, API_URL..."
else
    echo ">> File .env đã tồn tại, bỏ qua bước tạo."
fi

echo ">> Test chạy thử chương trình..."
python main.py

echo ">> Xong! Nếu muốn chạy tự động định kỳ, xem hướng dẫn trong DEPLOY.md (systemd timer)."
