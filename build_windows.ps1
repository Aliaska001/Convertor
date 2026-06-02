# Build ConvertorMP3 for Windows (PowerShell)
# Run this on Windows PowerShell as Administrator if you need to install globally
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install pyinstaller

# Download yt-dlp
if (-not (Test-Path "bin")) { mkdir bin }
Invoke-WebRequest -Uri "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe" -OutFile "bin\yt-dlp.exe"

# Build executable
pyinstaller --onefile --windowed --add-data "bin\yt-dlp.exe;bin" --icon dj.png --name ConvertorMP3 desktop_app.py
Write-Host "Build finished. Check the dist\ directory."
Pause
