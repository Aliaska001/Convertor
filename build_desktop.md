# Construire aplicație desktop (macOS)

Acest ghid explică cum să generezi o aplicație locală pentru macOS din proiect (variantă desktop).

## Cerințe înainte de build

- Python 3.9+
- `pyinstaller` instalat: `pip install pyinstaller`
- `PyQt5` instalat în mediu (este în `requirements.txt`)
- `yt-dlp` instalat: `pip install yt-dlp` (sau descărcat automat la build)

## Pași pentru macOS

1. Creează și activează un mediu virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Instalează dependențele:

```bash
pip install -r requirements.txt
pip install pyinstaller yt-dlp
```

3. Construiește aplicația cu PyInstaller (exemplu generare executabil):

```bash
pyinstaller --onefile --windowed --name ConvertorMP3 desktop_app.py
```

După rulare, pachetul va fi în `dist/ConvertorMP3` (executabil unic). Dacă dorești un `.app` bundle pe macOS, folosește opțiunile PyInstaller pentru bundle sau creează un `.app` din executabil generat.

## Semnare și notarizare (opțional)

Pentru distribuire pe macOS, cod-signing și notarizare Apple pot fi necesare. Aceste pași sunt în afara scopului acestui ghid, dar, în esență, folosești `codesign` și `altool` / `notarytool`.

## Observații

- `converter_core.py` folosește `yt-dlp` (instalat via pip) și `ffmpeg` (din `imageio-ffmpeg`).
- Dacă PyInstaller nu include automat toate modulele Qt, consultă documentația PyInstaller pentru adăugarea hook-urilor PyQt5.

## Rulare locală fără build

```bash
source .venv/bin/activate
python desktop_app.py

## Construire pentru Windows

Este recomandat să rulezi pașii de build pe un sistem Windows (PyInstaller generează binare specifice OS).

1. Pe Windows, creează și activează mediul virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Instalează dependențele și PyInstaller:

```powershell
pip install -r requirements.txt
pip install pyinstaller yt-dlp
```

3. Construiește executabilul Windows (.exe):

```powershell
pyinstaller --onefile --windowed --name ConvertorMP3 desktop_app.py
```

Fișierul rezultat va fi în `dist\ConvertorMP3.exe`. Pentru distribuire poți crea un installer (`Inno Setup`, `NSIS`) sau împacheta `.exe` într-un `.zip`.

Notă: Dacă vrei ca build-ul Windows să fie generat de pe macOS, poți folosi CI (GitHub Actions) sau mașini virtuale Windows; cross-compilarea locală nu este recomandată.
```

