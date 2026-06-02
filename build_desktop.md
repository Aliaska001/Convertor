# Construire aplicație desktop (macOS)

Acest ghid explică cum să generezi o aplicație locală pentru macOS din proiect (variantă desktop).

## Cerințe înainte de build

- Python 3.9+
- `pyinstaller` instalat: `pip install pyinstaller`
- `PyQt5` instalat în mediu (este în `requirements.txt`)
- `bin/yt-dlp` prezent în repo (sau `yt-dlp` în PATH)

## Pași pentru macOS

1. Creează și activează un mediu virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Instalează dependențele:

```bash
pip install -r requirements.txt
pip install pyinstaller
```

3. Construiește aplicația cu PyInstaller (exemplu generare `.app`):

```bash
pyinstaller --onefile --windowed \
	--add-data "bin/yt-dlp:bin" \
	--name ConvertorMP3 \
	desktop_app.py
```

După rulare, pachetul va fi în `dist/ConvertorMP3` (executabil unic). Dacă dorești un `.app` bundle pe macOS, folosește opțiunile PyInstaller pentru bundle sau creează un `.app` din executabil generat.

## Semnare și notarizare (opțional)

Pentru distribuire pe macOS, cod-signing și notarizare Apple pot fi necesare. Aceste pași sunt în afara scopului acestui ghid, dar, în esență, folosești `codesign` și `altool` / `notarytool`.

## Observații

- `converter_core.py` folosește `yt-dlp` și `ffmpeg`. Asigură-te că `bin/yt-dlp` este executabil (`chmod +x bin/yt-dlp`).
- Dacă PyInstaller nu include automat toate modulele Qt, consultă documentația PyInstaller pentru adăugarea hook-urilor PyQt5.

## Rulare locală fără build

```bash
source .venv/bin/activate
python desktop_app.py
```

