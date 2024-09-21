import time
import pygetwindow as gw
import pydirectinput
from utils import read_accounts, custom_click, custom_double_click, log
from constants import *

def login_and_start_game(window, user_id, password, server_index):
    try:
        # Kích hoạt cửa sổ game
        window.activate()
        log(f"Kích hoạt cửa sổ: {window.title}")
        time.sleep(0.5)

        # 1. Click vào nút host_name
        log("Click vào nút host_name")
        custom_click(window, *position_host_name)

        # 2. Click vào server
        log(f"Chọn server: {server_index + 1}")
        custom_click(window, *array_position_server[server_index])

        # 3. Nhập ID
        log("Click vào nút ID")
        custom_click(window, *position_button_id)
        time.sleep(0.5)
        pydirectinput.write(user_id)

        # 4. Nhập password
        log("Click vào nút Password")
        custom_click(window, *position_button_password)
        time.sleep(0.5)
        pydirectinput.write(password)
        pydirectinput.press('enter')

        time.sleep(2)
        # 5. Chọn nhân vật
        log("Double click chọn nhân vật")
        custom_double_click(window, *position_choose_nhan_vat)

        time.sleep(1)
        # 6. Click vào auto_play
        log("Click vào auto_play")
        custom_click(window, *position_auto_play)

        time.sleep(3)
        log("Hoàn thành đăng nhập và auto đánh nick: {user_id}, pass: {user_id}, vào server: {server_index}")
    except Exception as e:
        log(f"Lỗi khi xử lý cửa sổ '{window.title}': {e}")


def exit_and_restart_game(window):
    try:
        # Kích hoạt cửa sổ game
        window.activate()
        log(f"Kích hoạt cửa sổ: {window.title}")
        time.sleep(0.5)

        # 1. Nhấn phím 'esc' để thoát game
        log("Nhấn phím 'esc' để thoát game")
        pydirectinput.press('esc')

        # 2. Click vào nút exit game
        log("Click vào nút exit_game")
        custom_click(window, *position_exit_game)

        # 3. Double click chọn nhân vật
        log("Double click chọn nhân vật")
        custom_double_click(window, *position_choose_nhan_vat)

        # 4. Click vào auto_play
        log("Click vào auto_play")
        custom_click(window, *position_auto_play)

    except Exception as e:
        log(f"Lỗi khi thoát game trên cửa sổ '{window.title}': {e}")


def main():
    try:
        # Đọc danh sách tài khoản từ file
        accounts = read_accounts('input.txt')

        # Chỉ định biến server_index để lặp qua các vị trí server
        server_index = 0
        account_index = 0
        # Bước 1: Đăng nhập và bắt đầu auto_play cho tất cả cửa sổ game
        windows = gw.getWindowsWithTitle("MuBaChu.Com - Season 6")
        if not windows:
            log("Không tìm thấy cửa sổ có tiêu đề 'MuBaChu.Com - Season 6'. Đang đợi 5 giây trước khi thử lại.")
            time.sleep(5)

        for window in windows:
            user_id, password = accounts[account_index].split('/')
            login_and_start_game(window, user_id, password, server_index)
            server_index = (server_index + 1) % len(array_position_server)
            account_index
        # Đợi 30 giây
        time.sleep(30)

        # Bước 2: Sau 30 giây, thoát game và khởi động lại auto_play cho tất cả cửa sổ
        while True:
            for window in windows:
                exit_and_restart_game(window)
            # Lặp lại sau mỗi 30 giây
            time.sleep(30)

    except Exception as e:
        log(f"Lỗi toàn cục: {e}")

if __name__ == '__main__':
    main()
