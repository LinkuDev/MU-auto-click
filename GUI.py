import time
import pygetwindow as gw
import pydirectinput
import threading
from tkinter import Tk, Button, Label, Text, Entry, PhotoImage, Frame, Scrollbar, END, RIGHT, LEFT, BOTH, NW, EW, Y
from utils import read_accounts, custom_click, custom_double_click
from constants import *
from pynput import keyboard
import os

pause_flag = False
is_login_running = False
is_restart_running = False

def toggle_pause():
    global pause_flag
    pause_flag = not pause_flag
    log(f"Tạm dừng: {pause_flag}")

ctrl_pressed = False

def on_press(key):
    global ctrl_pressed
    if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        ctrl_pressed = True
    elif key == keyboard.Key.space and ctrl_pressed:
        toggle_pause()

def on_release(key):
    global ctrl_pressed
    if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        ctrl_pressed = False

# Hotkey listener
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

def get_window_titles_from_text(text_widget):
    # Lấy nội dung từ text area và tách từng dòng
    window_titles = text_widget.get("1.0", "end-1c").splitlines()
    return [title.strip() for title in window_titles if title.strip()]

def get_file_from_window_title(window_title):
    # Bỏ chữ 'Mu' và lấy phần còn lại của tên cửa sổ
    file_part = window_title.replace("Mu", "").split(".")[0].lower()  # "MuBaChu.Com - Season 6" -> "bachu"
    return f"{file_part}.txt"

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

        time.sleep(4)
        # 5. Chọn nhân vật
        log("Double click chọn nhân vật")
        custom_double_click(window, *position_choose_nhan_vat)
        custom_double_click(window, *position_choose_nhan_vat)
        
        time.sleep(4)
        # 6. Click vào auto_play
        log("Click vào auto_play")
        custom_click(window, *position_auto_play)

        time.sleep(2)
        # 6. Click vào auto_play
        log("Mở thùng đồ")
        pydirectinput.press('esc')

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
        log("Nhấn phím 'esc' để mở thùng đồ")
        pydirectinput.press('esc')
        time.sleep(2)

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
    windows = [gw.getWindowsWithTitle(title)[0] for title in window_titles if gw.getWindowsWithTitle(title)]

    log(f"Tổng cửa sổ game: {len(windows)}")
    
    for window in windows:
        if not pause_flag:
            # Lấy file tài khoản tương ứng với cửa sổ
            file_name = get_file_from_window_title(window.title)
            log(f"Lấy tài khoản từ file: {file_name}")

            if not os.path.exists(file_name):
                log(f"File {file_name} không tồn tại. Bỏ qua cửa sổ này.")
                continue

            accounts = read_accounts(file_name)

            for account in accounts:
                user_id, password = account.split('/')
                login_and_start_game(window, user_id, password, server_index)
                server_index = (server_index + 1) % len(array_position_server)

    is_login_running = False

def start_restart(window_titles, delay):
    global is_restart_running

    if is_restart_running:
        log("Quá trình khởi động lại đang chạy...")
        return

    is_restart_running = True
    windows = [gw.getWindowsWithTitle(title)[0] for title in window_titles if gw.getWindowsWithTitle(title)]

    # Chờ thời gian delay trước khi bắt đầu
    log(f"Chờ {delay * 60} giây trước khi bắt đầu khởi động lại.")
    time.sleep(delay * 60)

    while not pause_flag:
        for window in windows:
            exit_and_restart_game(window)
        log(f"Chờ {delay * 60} giây trước khi khởi động lại lần tiếp theo")
        time.sleep(delay * 60)

    is_restart_running = False

def start_login_thread(window_titles):
    threading.Thread(target=start_login, args=(window_titles,)).start()

def start_restart_thread(window_titles):
    threading.Thread(target=start_restart, args=(window_titles,)).start()

def log(message):
    global log_text_area  # Khai báo log_text_area là biến toàn cục
    print(message)  # Vẫn giữ in ra terminal
    log_text_area.config(state='normal')  # Bật chế độ chỉnh sửa
    log_text_area.insert(END, f"{message}\n")  # Thêm log vào text area
    log_text_area.yview(END)  # Cuộn xuống cuối để hiển thị log mới nhất
    log_text_area.config(state='disabled')  # Tắt chế độ chỉnh sửa

def create_gui():
    global log_text_area 
    root = Tk()
    root.title("MU login")
    
    # Thêm icon
    icon = PhotoImage(file="icon.png")  
    root.iconphoto(False, icon)
    root.resizable(False, False)

    # Cài đặt layout grid
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1) 

    img = PhotoImage(file='icon.png') 
    img_label = Label(root, image=img)
    img_label.grid(row=0, column=0, padx=10, pady=10, columnspan=2)  # Kéo dài qua hai cột

    # Text area để nhập tên các cửa sổ
    window_text_area = Text(root, height=7, width=50)
    window_text_area.grid(row=1, column=0, padx=5, pady=5, sticky='ew', columnspan=2)  # Kéo dài qua hai cột
    window_text_area.insert("1.0", "MuBaChu.Com - Season 6\nMuDangCap.Com - Season 6")

    # Label và Entry để nhập thời gian chờ
    restart_delay_label = Label(root, text="Thời gian chờ giữa các lần khởi động lại (phút):")
    restart_delay_label.grid(row=2, column=0, padx=5, pady=5, sticky='w', columnspan=2)  # Kéo dài qua hai cột

    restart_delay_entry = Entry(root)
    restart_delay_entry.grid(row=3, column=0, padx=5, pady=5, sticky='ew', columnspan=2)  # Kéo dài qua hai cột
    restart_delay_entry.insert(0, "30")  # Giá trị mặc định là 30 giây

    # Nút Start Đăng nhập hàng loạt
    start_login_button = Button(root, text="Start Đăng nhập hàng loạt", command=lambda: start_login_thread(get_window_titles_from_text(window_text_area)))
    start_login_button.grid(row=4, column=0, padx=5, pady=5, sticky='ew')

    # Nút Pause Đăng nhập hàng loạt
    pause_login_button = Button(root, text="Tạm dừng Đăng nhập hàng loạt", command=toggle_pause)
    pause_login_button.grid(row=5, column=0, padx=5, pady=5, sticky='ew')

    # Nút Start Đăng nhập lại
    start_restart_button = Button(root, text="Start Đăng nhập lại", command=lambda: start_restart_thread(get_window_titles_from_text(window_text_area), int(restart_delay_entry.get())))
    start_restart_button.grid(row=4, column=1, padx=5, pady=5, sticky='ew')  # Đặt ở cột 1

    # Nút Pause Đăng nhập lại
    pause_restart_button = Button(root, text="Tạm dừng Đăng nhập lại", command=toggle_pause)
    pause_restart_button.grid(row=5, column=1, padx=5, pady=5, sticky='ew')  # Đặt ở cột 1

    # Cửa sổ log
    log_text_area = Text(root, height=10, width=50, state='normal')
    log_text_area.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky='ew')  # Kéo dài qua hai cột
    log_text_area.config(state='disabled')  # Vô hiệu hóa để không cho chỉnh sửa

    root.mainloop()

if __name__ == '__main__':
    create_gui()
