import time
import pygetwindow as gw
import pydirectinput
import threading
from tkinter import Tk, Button, Label, Text
from utils import read_accounts, custom_click, custom_double_click, log
from constants import *
from pynput import keyboard

pause_flag = False
is_login_running = False
is_restart_running = False

def toggle_pause():
    global pause_flag
    pause_flag = not pause_flag
    log(f"Tạm dừng: {pause_flag}")

def on_press(key):
    if key == keyboard.Key.space:
        toggle_pause()

# Hotkey listener
listener = keyboard.Listener(on_press=on_press)
listener.start()

def get_window_titles_from_text(text_widget):
    # Lấy nội dung từ text area và tách từng dòng
    window_titles = text_widget.get("1.0", "end-1c").splitlines()
    return [title.strip() for title in window_titles if title.strip()]

def login_and_start_game(window, user_id, password, server_index):
    if pause_flag:
        log("Tạm dừng đăng nhập")
        return

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
        time.sleep(1)

        # 3. Nhập ID
        log("Click vào nút ID")
        custom_click(window, *position_button_id)
        time.sleep(0.5)
        pydirectinput.write(user_id)
        time.sleep(1)

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
        log(f"Hoàn thành đăng nhập và auto đánh nick: {user_id}, pass: {password}, vào server: {server_index}")
        time.sleep(3)
    except Exception as e:
        log(f"Lỗi khi xử lý cửa sổ '{window.title}': {e}")

def exit_and_restart_game(window):
    if pause_flag:
        log("Tạm dừng thoát và khởi động lại")
        return

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
        time.sleep(2)

        # 4. Click vào auto_play
        log("Click vào auto_play")
        custom_click(window, *position_auto_play)

    except Exception as e:
        log(f"Lỗi khi thoát game trên cửa sổ '{window.title}': {e}")

def start_login(window_titles):
    global is_login_running, server_index

    if is_login_running:
        log("Quá trình đăng nhập đang chạy...")
        return

    is_login_running = True
    server_index = 0
    accounts = read_accounts('input.txt')
    windows = [gw.getWindowsWithTitle(title)[0] for title in window_titles if gw.getWindowsWithTitle(title)]

    if len(accounts) < len(windows):
        log("Số lượng tài khoản ít hơn số lượng cửa sổ, một số cửa sổ sẽ không được xử lý.")
        windows = windows[:len(accounts)]

    for i, window in enumerate(windows):
        if not pause_flag:
            account = accounts[i]
            user_id, password = account.split('/')
            login_and_start_game(window, user_id, password, server_index)
            server_index = (server_index + 1) % len(array_position_server)

    is_login_running = False

def start_restart(window_titles):
    global is_restart_running

    if is_restart_running:
        log("Quá trình khởi động lại đang chạy...")
        return

    is_restart_running = True
    windows = [gw.getWindowsWithTitle(title)[0] for title in window_titles if gw.getWindowsWithTitle(title)]

    while not pause_flag:
        for window in windows:
            exit_and_restart_game(window)
        time.sleep(30)

    is_restart_running = False

def start_login_thread(window_titles):
    threading.Thread(target=start_login, args=(window_titles,)).start()

def start_restart_thread(window_titles):
    threading.Thread(target=start_restart, args=(window_titles,)).start()

def create_gui():
    root = Tk()
    root.title("MU login")

    Label(root, text="MU login", font=("Arial", 14)).pack(pady=10)

    # Text area để nhập tên các cửa sổ
    window_text_area = Text(root, height=10, width=50)
    window_text_area.pack(pady=10)

    # Nút Start Đăng nhập hàng loạt
    start_login_button = Button(root, text="Start Đăng nhập hàng loạt", command=lambda: start_login_thread(get_window_titles_from_text(window_text_area)))
    start_login_button.pack(pady=10)

    # Nút Pause Đăng nhập hàng loạt
    pause_login_button = Button(root, text="Tạm dừng Đăng nhập hàng loạt", command=toggle_pause)
    pause_login_button.pack(pady=10)

    # Nút Start Đăng nhập lại
    start_restart_button = Button(root, text="Start Đăng nhập lại", command=lambda: start_restart_thread(get_window_titles_from_text(window_text_area)))
    start_restart_button.pack(pady=10)

    # Nút Pause Đăng nhập lại
    pause_restart_button = Button(root, text="Tạm dừng Đăng nhập lại", command=toggle_pause)
    pause_restart_button.pack(pady=10)

    root.mainloop()

if __name__ == '__main__':
    create_gui()
