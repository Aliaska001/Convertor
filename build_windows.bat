@echo off
REM Build ConvertorMP3 for Windows (run on Windows)
python -m venv .venv
call .venv\Scripts\activate
pip install -r requirements.txt
pip install pyinstaller

REM Download yt-dlp
if not exist bin mkdir bin
powershell -Command "Invoke-WebRequest -Uri 'https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe' -OutFile 'bin\yt-dlp.exe'"

REM Build executable
pyinstaller --onefile --windowed --add-data "bin\yt-dlp.exe;bin" --icon dj.png --name ConvertorMP3 desktop_app.py
echo Build finished. Check the dist\ directory.
pause
