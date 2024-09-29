@echo off
REM Kiểm tra xem Python đã được cài đặt chưa
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python chưa được cài đặt. Vui lòng cài đặt Python trước khi chạy script này.
    pause
    exit /b
)

REM Cài đặt các thư viện từ file requirements.txt
pip install -r requirements.txt

REM Thông báo hoàn thành
echo Cài đặt hoàn tất!
pause
