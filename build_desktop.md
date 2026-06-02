# Construire aplicație desktop

Acest ghid explică cum să generezi o aplicație locală pentru Windows și macOS din proiect.

## Pași generali

1. Creează un mediu virtual Python:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Instalează dependențele:

```bash
pip install -r requirements.txt
pip install pyinstaller
```

3. Construiește aplicația desktop:

### Windows

```bash
pyinstaller --onefile --windowed --add-data "bin/yt-dlp;bin" desktop_app.py
```

### macOS

```bash
pyinstaller --onefile --windowed --add-data "bin/yt-dlp:bin" desktop_app.py
```

4. Executabilul va fi generat în directorul `dist/`.

## Observații

- `desktop_app.py` folosește `converter_core.py` pentru descărcare și conversie.
- `bin/yt-dlp` trebuie inclus în pachet pentru ca aplicația să funcționeze fără instalare separată.
- Dacă `ffmpeg` nu este găsit în sistem, `imageio-ffmpeg` va furniza un executabil compatibil.

## Rulare locală fără build

Poți porni aplicația local direct din cod:

```bash
python desktop_app.py
```

Apoi introdu linkul YouTube și folderul în care vrei să salvezi MP3-ul.
