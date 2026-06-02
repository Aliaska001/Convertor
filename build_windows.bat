@echo off
REM Build ConvertorMP3 for Windows (run on Windows)
python -m venv .venv
call .venv\Scripts\activate
pip install -r requirements.txt
pip install pyinstaller
pyinstaller --onefile --windowed --add-data "bin\yt-dlp;bin" --name ConvertorMP3.exe desktop_app.py
echo Build finished. Check the dist\ directory.
pause
