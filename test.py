import pydirectinput
import pygetwindow as gw
import time

# Lấy cửa sổ đầu tiên có tên cụ thể
windows = gw.getWindowsWithTitle("MuBaChu.Com - Season 6")
if windows:
    window = windows[0]
    window.activate()  # Kích hoạt cửa sổ
    time.sleep(1)  # Chờ cửa sổ được kích hoạt
    pydirectinput.click(window.left + 100, window.top + 100)  # Click vào vị trí bất kỳ trong cửa sổ
