from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Tạo Chrome Options
chrome_options = Options()

 # Đường dẫn đến user data của Chrome (thay đổi tùy vào hệ điều hành của bạn)
chrome_user_data_dir = "C:/Users/DELL/AppData/Local/Google/Chrome/User Data"  # Windows
chrome_profile = "Default"  # Thay đổi nếu bạn dùng profile khác

chrome_options.add_argument(f"--user-data-dir={chrome_user_data_dir}")
chrome_options.add_argument(f"--profile-directory={chrome_profile}")

# Loại bỏ dấu hiệu tự động hóa
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

# Fake user-agent để giống người dùng thật
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.102 Safari/537.36")

# Tắt các tính năng mà trang web có thể phát hiện Selenium
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

# Các tùy chọn giúp tăng tính tương tự với trình duyệt thường
chrome_options.add_argument("--start-maximized")  # Mở trình duyệt toàn màn hình
chrome_options.add_argument("--disable-infobars")  # Tắt thanh thông báo "Chrome is being controlled by automated software"
chrome_options.add_argument("--disable-extensions")  # Tắt các extension để giảm rủi ro phát hiện
chrome_options.add_argument("--disable-popup-blocking")  # Tắt tính năng chặn popup
chrome_options.add_argument("--no-sandbox")  # Dùng để tăng ổn định (đặc biệt trên server Linux)
chrome_options.add_argument("--disable-dev-shm-usage")  # Dùng khi chạy trên Docker hoặc môi trường bị giới hạn bộ nhớ
chrome_options.add_argument("--disable-gpu")  # Tắt GPU để giảm lỗi đồ họa (Linux)
chrome_options.add_argument("--disable-software-rasterizer")  # Tắt rasterizer đồ họa phần mềm
chrome_options.add_argument("--disable-background-timer-throttling")  # Tắt giảm tốc độ các timer trong tab chạy nền
chrome_options.add_argument("--disable-backgrounding-occluded-windows")  # Tắt giới hạn hoạt động khi cửa sổ bị che
chrome_options.add_argument("--disable-renderer-backgrounding")  # Tắt giảm hiệu suất khi tab bị che

# Debugging
chrome_options.add_argument("--remote-debugging-port=9222")  # Để mở remote debugging, nếu cần
chrome_options.add_argument("--enable-logging")  # Kích hoạt logging
chrome_options.add_argument("--v=1")  # Đặt mức log
chrome_options.add_argument("--allow-running-insecure-content")  # Cho phép nội dung không an toàn nếu có

# Khởi động trình duyệt Chrome với các tùy chọn trên
driver = webdriver.Chrome(options=chrome_options)

# Test mở trang web
driver.get("https://www.shopee.vn")
