import time
import pygetwindow as gw
import pydirectinput
import threading
from tkinter import Tk, Button, Label, Text, Entry, PhotoImage, Frame, Scrollbar, END, RIGHT, LEFT, BOTH, NW, EW, Y
from utils import read_accounts, custom_click, custom_double_click, long_press
from constants import *
from pynput import keyboard
import os

pause_flag = False
is_login_running = False
is_restart_running = False
remaining_time_label = Label

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
        time.sleep(2)

        # 1. Click vào nút host_name
        log("Click vào nút host_name")
        custom_click(window, *position_host_name)
        time.sleep(1)
        custom_click(window, *position_host_name)

        # 2. Click vào server
        log(f"Chọn server: {server_index + 1}")
        custom_click(window, *array_position_server[server_index])
        time.sleep(1)
        custom_click(window, *array_position_server[server_index])
        time.sleep(2)

        # 3. Nhập ID
        log("Click vào nút ID")
        custom_click(window, *position_button_id)
        time.sleep(1)
        pydirectinput.write(user_id)
        time.sleep(1)

        # 4. Nhập password
        log("Click vào nút Password")
        custom_click(window, *position_button_password)
        time.sleep(1)
        pydirectinput.write(password)
        long_press('enter')

        time.sleep(4)
        # 5. Chọn nhân vật
        log("click vào nhân vật giữa")
        custom_click(window, *position_choose_nhan_vat)
        time.sleep(1)
        custom_click(window, *position_choose_nhan_vat)
        time.sleep(1)
        custom_click(window, *position_choose_nhan_vat)
        time.sleep(1)
        custom_click(window, *position_choose_nhan_vat)
        time.sleep(3)
        long_press('enter')
        log("Đã nhấn enter")

        time.sleep(4)
        # 6. Click vào auto_play
        log("Click vào auto_play")
        custom_click(window, *position_auto_play)

        time.sleep(2)
        log("Mở thùng đồ")
        long_press('v')

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
        time.sleep(2)
        # Kích hoạt cửa sổ game
        if window is None:
            log(f"Cửa sổ '{window}' không tồn tại hoặc không tìm thấy.")
            return
        
        window.activate()
        log(f"Kích hoạt cửa sổ: {window.title}")
        time.sleep(3)

        # 1. Nhấn phím 'esc' để thoát game
        log("Nhấn phím 'esc' để tắt thùng đồ")
        long_press('esc')
        time.sleep(2)

        log("Nhấn phím 'esc' để thoát game")
        long_press('esc')
        time.sleep(2)

        # 2. Click vào nút exit game
        log("Click vào nút chọn server lần 1")
        custom_click(window, *position_exit_game)
        time.sleep(2)
        log("Click vào nút chọn server lần 2")
        custom_click(window, *position_exit_game)
        time.sleep(10)

        # 3. Chọn nhân vật
        log("Click chọn nhân vật")
        custom_click(window, *position_choose_nhan_vat)
        time.sleep(1)
        custom_click(window, *position_choose_nhan_vat)
        time.sleep(1)
        custom_click(window, *position_choose_nhan_vat)
        time.sleep(1)
        custom_click(window, *position_choose_nhan_vat)
        time.sleep(2)
        long_press('enter')

        # 4. Click vào auto_play
        log("Click vào auto_play")
        custom_click(window, *position_auto_play)

        time.sleep(2)
        log("Mở lại thùng đồ")
        long_press('v')
    
    except Exception as e:
        log(f"Lỗi khi thoát game trên cửa sổ '{window.title}' (nếu có): {e}")


def start_login(window_titles, delay):
    global is_login_running, is_restart_running

    if is_login_running:
        log("Quá trình đăng nhập đang chạy...")
        return

    is_login_running = True
    windows = []
    for title in window_titles:
        matched_windows = gw.getWindowsWithTitle(title)
        if matched_windows:
            windows.extend(matched_windows)  # Thêm toàn bộ cửa sổ vào danh sách windows

    log(f"Tổng số cửa sổ tìm thấy: {len(windows)}")
    
    # Tạo từ điển để theo dõi biến đếm của từng file tài khoản
    account_indices = {}
    for window in windows:
        window.activate()
        time.sleep(1)

    for window in windows:
        if not pause_flag:
            # Lấy file tài khoản tương ứng với cửa sổ
            file_name = get_file_from_window_title(window.title)
            log(f"Lấy tài khoản từ file: {file_name}")

            if not os.path.exists(file_name):
                log(f"File {file_name} không tồn tại. Bỏ qua cửa sổ này.")
                continue

            # Đọc tất cả các tài khoản từ file
            accounts = read_accounts(file_name)

            # Khởi tạo biến đếm cho tài khoản nếu chưa có trong từ điển
            if file_name not in account_indices:
                account_indices[file_name] = 0

            # Lấy vị trí index cho file tài khoản từ từ điển
            account_index = account_indices[file_name]

            # Kiểm tra xem index tài khoản có hợp lệ không
            if account_index < len(accounts):
                # Lấy tài khoản tương ứng với account_index
                account_data = accounts[account_index].strip()
                user_id, password, server_index = account_data.split('/')

                # Chuyển server_index về dạng số
                server_index = int(server_index) - 1  # Trừ đi 1 để index đúng với mảng

                # Đăng nhập vào game
                login_and_start_game(window, user_id, password, server_index)
                log(f"Đã đăng nhập vào cửa sổ: {window.title} với tài khoản: {user_id} và server: {server_index + 1}")

                # Tăng biến đếm cho file tương ứng
                account_indices[file_name] += 1
                time.sleep(2)

            else:
                log(f"Không có đủ tài khoản trong file {file_name} cho cửa sổ: {window.title}")

    is_login_running = False
    log("Đã hoàn thành đăng nhập hàng loạt")
    is_restart_running = False

def start_restart(window_titles, delay):
    global is_restart_running, pause_flag

    if is_restart_running:
        log("Quá trình khởi động lại đang chạy...")
        return

    try:
        # Lấy tất cả các cửa sổ ngay từ đầu
        windows = []
        for title in window_titles:
            matched_windows = gw.getWindowsWithTitle(title)
            log(f"Tiêu đề: {title} - Số lượng cửa sổ tìm thấy: {len(matched_windows)}")
            if matched_windows:
                windows.extend(matched_windows)  # Thêm toàn bộ cửa sổ vào danh sách windows

        log(f"Tổng số cửa sổ tìm thấy: {len(windows)}")
        if len(windows) == 0:
            log("Không tìm thấy cửa sổ nào, dừng quá trình.")
            is_restart_running = False
            return

        log("Mở toàn bộ tab để tránh bị lag")
        for window in windows:
            window.activate()
            time.sleep(1)

        # Không còn delay, thực hiện action ngay lập tức
        log(f"Đang khởi động lại {len(windows)} cửa sổ...")

        for window in windows:
            if pause_flag:  # Nếu quá trình bị dừng, thoát khỏi vòng lặp
                log("Tạm dừng quá trình khởi động lại.")
                break
            exit_and_restart_game(window)  # Hàm đăng nhập lại từng cửa sổ

        log("Đã hoàn thành đăng nhập lại hàng loạt.")
    
    except Exception as e:
        log(f"Lỗi xảy ra trong quá trình khởi động lại: {e}")

    finally:
        is_restart_running = False  # Đảm bảo flag được reset sau khi hoàn thành

def start_delay(window_titles, delay):
    global pause_flag

    while True:
        if pause_flag:  # Kiểm tra nếu có yêu cầu tạm dừng
            log("Tạm dừng quá trình khởi động lại với delay.")
            break

        # Chờ thời gian delay trước khi thực hiện lại quá trình khởi động
        log(f"Chờ {delay} phút trước khi khởi động lại.")
        for i in range(delay):  # Đếm ngược thời gian
            if pause_flag:  # Kiểm tra nếu có yêu cầu tạm dừng trong khi chờ
                log("Tạm dừng trong khi chờ delay.")
                break
            time.sleep(60)  # Chờ 1 phút
            log(f'Còn {delay - (i + 1)} phút trước khi đăng nhập lại.')

        # Nếu không bị tạm dừng thì kích hoạt lại giao diện chính và thực hiện click
        if not pause_flag:
            try:
                windows = []
                for title in window_titles:
                    matched_windows = gw.getWindowsWithTitle(title)
                    if matched_windows:
                        windows.extend(matched_windows)  # Thêm toàn bộ cửa sổ vào danh sách windows
                time.sleep((2 + 30)*(len(windows)))
                gui_tool = gw.getWindowsWithTitle("MU login")[0]
                gui_tool.activate()
                time.sleep(1)
                log('Click vào nút đăng nhập lại')
                custom_click(gui_tool, 328, 421)
                # start_restart(window_titles, delay)
            except IndexError:
                # log("Không tìm thấy cửa sổ 'Mu login'. Sẽ thử lại sau.")
                continue  # Không dừng vòng lặp mà tiếp tục sau thời gian delay


def countdown(remaining):
    if remaining > 0:
        remaining_time_label.config(text=f"Thời gian còn lại: {remaining} giây")
        remaining_time_label.after(1000, countdown, remaining - 1)  # Gọi lại sau 1 giây
    else:
        remaining_time_label.config(text="Thời gian chờ đã hết!")

def start_login_thread(window_titles, time):
    threading.Thread(target=start_login, args=(window_titles, time)).start()

def start_restart_thread(window_titles):
    threading.Thread(target=start_restart, args=(window_titles, 0)).start()

def start_delay_restart_thread(window_titles, time):
    threading.Thread(target=start_delay, args=(window_titles, time)).start()

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

    img = PhotoImage(file="icon.png")
    img_label = Label(root, image=img)
    img_label.grid(row=0, column=0, padx=10, pady=10, columnspan=2)  # Kéo dài qua hai cột

    # Text area để nhập tên các cửa sổ
    window_text_area = Text(root, height=7, width=50)
    window_text_area.grid(row=1, column=0, padx=5, pady=5, sticky='ew', columnspan=2)  # Kéo dài qua hai cột
    window_text_area.insert("1.0", "MuBaChu.Com - Season 6\nMuDangCap.Com - Season 6\nMuBaoChau.Com - Season 6")

    # Label và Entry để nhập thời gian chờ
    restart_delay_label = Label(root, text="Thời gian chờ giữa các lần khởi động lại (phút):")
    restart_delay_label.grid(row=3, column=0, padx=5, pady=5, sticky='w', columnspan=2)  # Kéo dài qua hai cột

    restart_delay_entry = Entry(root)
    restart_delay_entry.grid(row=4, column=0, padx=5, pady=5, sticky='ew', columnspan=2)  # Kéo dài qua hai cột
    restart_delay_entry.insert(0, "30")  # Giá trị mặc định là 30 phút

    # Nút Start Đăng nhập hàng loạt
    start_login_button = Button(root, text="Start Đăng nhập hàng loạt", command=lambda: start_login_thread(get_window_titles_from_text(window_text_area), int(restart_delay_entry.get())))
    start_login_button.grid(row=5, column=0, padx=5, pady=5, sticky='ew')

    # Nút Pause Đăng nhập hàng loạt
    pause_login_button = Button(root, text="Tạm dừng Đăng nhập hàng loạt", command=toggle_pause)
    pause_login_button.grid(row=6, column=0, padx=5, pady=5, sticky='ew')

    # Nút Start Đăng nhập lại
    start_restart_button = Button(root, text="Đăng nhập lại", command=lambda: start_restart_thread(get_window_titles_from_text(window_text_area)))
    start_restart_button.grid(row=5, column=1, padx=5, pady=5, sticky='ew')  # Đặt ở cột 1

    # Nút Pause Đăng nhập lại
    pause_restart_button = Button(root, text="Tạm dừng Đăng nhập lại", command=toggle_pause)
    pause_restart_button.grid(row=6, column=1, padx=5, pady=5, sticky='ew')  # Đặt ở cột 1

    # Cửa sổ log
    log_text_area = Text(root, height=10, width=50, state='normal')
    log_text_area.grid(row=8, column=0, columnspan=2, padx=5, pady=5, sticky='ew')  # Kéo dài qua hai cột
    log_text_area.config(state='disabled')  # Vô hiệu hóa để không cho chỉnh sửa
        
    # Nút Delay Đăng nhập lại (full width)
    delay_restart_button = Button(root, text="Delay đăng nhập lại", command=lambda: start_delay_restart_thread(get_window_titles_from_text(window_text_area), int(restart_delay_entry.get())))
    delay_restart_button.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky='ew')  # Kéo dài qua hai cột

    root.mainloop()

if __name__ == '__main__':
    create_gui()
