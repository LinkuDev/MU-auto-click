import time
import pydirectinput

# Đọc tài khoản từ file input.txt
def read_accounts(file_path):
    with open(file_path, 'r') as file:
        accounts = file.readlines()
    return [account.strip() for account in accounts]

# Hàm click với tọa độ tương đối so với cửa sổ
def custom_click(window, rel_x, rel_y):
    # Lấy vị trí của cửa sổ
    window_x, window_y = window.topleft

    # Tính toán tọa độ tuyệt đối
    abs_x = window_x + rel_x
    abs_y = window_y + rel_y

    # Thực hiện thao tác click
    pydirectinput.moveTo(abs_x, abs_y)
    pydirectinput.mouseDown()
    time.sleep(0.1)
    pydirectinput.mouseUp()

# Hàm double click với tọa độ tương đối so với cửa sổ
def custom_double_click(window, rel_x, rel_y):
    # Lấy vị trí của cửa sổ
    window_x, window_y = window.topleft

    # Tính toán tọa độ tuyệt đối
    abs_x = window_x + rel_x
    abs_y = window_y + rel_y

    # Thực hiện thao tác double click
    pydirectinput.moveTo(abs_x, abs_y)
    pydirectinput.mouseDown()
    time.sleep(0.05)
    pydirectinput.mouseUp()
    time.sleep(0.1)
    pydirectinput.mouseDown()
    time.sleep(0.05)
    pydirectinput.mouseUp()

# Hàm log để in ra console log
def log(message):
    print(f"[LOG] {message}")
