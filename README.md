# Convertor YouTube in MP3

Aplicație locală pentru Windows/macOS care descarcă și convertește conținut YouTube în MP3.

## Ce conține acest proiect

- `desktop_app.py` - aplicația desktop Tkinter
- `converter_core.py` - logică de conversie și descărcare YouTube
- `bin/yt-dlp` - utilitar yt-dlp folosit pentru descărcarea video-urilor YouTube
- `requirements.txt` - dependențe Python

## Cerințe

- Python 3.9+
- `yt-dlp` inclus în `bin/yt-dlp`
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

Introdu un link YouTube, alege folderul de salvare și apasă `Converteste in MP3`.

## Construire aplicație desktop

Vezi `build_desktop.md` pentru pașii de generare a unui executabil Windows/macOS.

> Folosește aplicația doar pentru conținutul tău sau materiale pe care ai dreptul să le descarci și să le convertești.
