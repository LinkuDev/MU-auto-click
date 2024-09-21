import pygetwindow as gw
import pyautogui
import pydirectinput
import time

# Tìm cửa sổ có tiêu đề chứa từ khóa "Notepad"
window = gw.getWindowsWithTitle('MuBaChu.Com - Season 6')[0]  # Chọn cửa sổ đầu tiên có tiêu đề khớp

# Kích hoạt cửa sổ
window.activate()

# Đợi một chút cho cửa sổ được kích hoạt
time.sleep(1)

# Di chuyển chuột và click vào tọa độ cụ thể bên trong cửa sổ
# Chuyển tọa độ thành tương đối so với cửa sổ
window_x, window_y = window.topleft
target_x, target_y = window_x + 228, window_y + 39  # Tọa độ tương đối trong cửa sổ

# Di chuyển chuột đến tọa độ và click
# pyautogui.moveTo(target_x, target_y, duration=1)
# pyautogui.click()

# print(f"Tọa độ của cửa sổ game là: ({window_x}, {window_y})")

# # Đợi 5 giây để bạn di chuyển chuột đến nút trong game
# print("Di chuyển chuột đến nút trong 5 giây...")
# time.sleep(5)

# # Lấy tọa độ của con trỏ chuột (tọa độ màn hình)
# mouse_x, mouse_y = pyautogui.position()
# print(f"Tọa độ của chuột trên màn hình là: ({mouse_x}, {mouse_y})")

# # Tính tọa độ tương đối của nút so với cửa sổ game
# relative_x = mouse_x - window_x
# relative_y = mouse_y - window_y

# print(f"Tọa độ tương đối của nút so với cửa sổ game là: ({relative_x}, {relative_y})")

pydirectinput.moveTo(target_x, target_y) # Move the mouse to the x, y coordinates 100, 150.
pydirectinput.mouseDown()
time.sleep(0.3)
pydirectinput.mouseUp()
pydirectinput.press('home')
