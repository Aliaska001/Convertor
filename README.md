# Convertor YouTube in MP3 — Aplicație Desktop

Această variantă este o aplicație desktop (macOS/Windows) care descarcă și convertește conținut YouTube în MP3.

## Ce conține proiectul

- `desktop_app.py` — aplicația desktop (PyQt5)
- `converter_core.py` — logică de descărcare și conversie
- `bin/yt-dlp` — utilitarul `yt-dlp` (inclus sau folosit din PATH)
- `requirements.txt` — dependențe Python

## Cerințe

- Python 3.9+
- `PyQt5` (în `requirements.txt`)
- `ffmpeg` disponibil în sistem sau `imageio-ffmpeg` instalat

## Instalare locală

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Rulare locală

```bash
python desktop_app.py
```

## Construire pentru macOS

Urmărește `build_desktop.md` pentru instrucțiuni de generare a unui executabil cu `pyinstaller`.

## Notă de utilizare

Folosește aplicația numai pentru materiale pe care ai dreptul să le descarci și să le convertești.

