import pygetwindow as gw
import pyautogui
import time

# Tìm cửa sổ game bằng tiêu đề (chỉnh sửa lại tiêu đề game cho phù hợp)
game_window = gw.getWindowsWithTitle('MuBaChu.Com - Season 6')[0]
game_window.activate()
# Lấy tọa độ của cửa sổ game (góc trên cùng bên trái)
window_x, window_y = game_window.topleft

# Lấy tọa độ của con trỏ chuột (tọa độ màn hình)
mouse_x, mouse_y = pyautogui.position()
print(f"Tọa độ của chuột trên màn hình là: ({mouse_x}, {mouse_y})")

# Tính tọa độ tương đối của nút so với cửa sổ game
relative_x = mouse_x - window_x
relative_y = mouse_y - window_y

print(f"Tọa độ tương đối của nút so với cửa sổ game là: ({relative_x}, {relative_y})")
