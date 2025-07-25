import os
import sys

def resource_path(relative_path):
    """Trả về đường dẫn tuyệt đối tới file tài nguyên, tương thích PyInstaller"""
    try:
        base_path = sys._MEIPASS  # Khi chạy từ exe
    except AttributeError:
        base_path = os.path.abspath(".")  # Khi chạy bằng Python thông thường
    return os.path.join(base_path, relative_path)