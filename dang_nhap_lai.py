import time
import pygetwindow as gw
import pydirectinput
from utils import read_accounts, custom_click, custom_double_click, log
from constants import *

def exit_and_restart_game(window):
    try:
        # Kích hoạt cửa sổ game
        window.activate()
        log(f"Kích hoạt cửa sổ: {window.title}")
        time.sleep(0.5)

        # 1. Nhấn phím 'esc' để thoát game
        log("Nhấn phím 'esc' để thoát game")
        pydirectinput.press('esc')
        time.sleep(2)
        # 2. Click vào nút exit game
        log("Click vào nút exit_game")
        custom_click(window, *position_exit_game)
        time.sleep(10)
        # 3. Double click chọn nhân vật
        log("Double click chọn nhân vật")
        custom_double_click(window, *position_choose_nhan_vat)
        time.sleep(3)
        # 4. Click vào auto_play
        log("Click vào auto_play")
        custom_click(window, *position_auto_play)

    except Exception as e:
        log(f"Lỗi khi thoát game trên cửa sổ '{window.title}': {e}")


def main():
    try:
        # Bước 1: Đăng nhập và bắt đầu auto_play cho tất cả cửa sổ game
        windows = gw.getWindowsWithTitle("MuBaChu.Com - Season 6")
        if not windows:
            log("Không tìm thấy cửa sổ có tiêu đề 'MuBaChu.Com - Season 6'. Đang đợi 5 giây trước khi thử lại.")
            time.sleep(5)

        while True:
            for window in windows:
                exit_and_restart_game(window)
            # Lặp lại sau mỗi 30 giây
            time.sleep(30)

    except Exception as e:
        log(f"Lỗi toàn cục: {e}")

if __name__ == '__main__': 
    main()
