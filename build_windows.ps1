# Build ConvertorMP3 for Windows (PowerShell)
# Run this on Windows PowerShell as Administrator if you need to install globally
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install pyinstaller
pyinstaller --onefile --windowed --add-data "bin\yt-dlp;bin" --name ConvertorMP3.exe desktop_app.py
Write-Host "Build finished. Check the dist\ directory."
Pause
