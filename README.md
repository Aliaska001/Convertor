# Convertor YouTube in MP3

Varianta web locală a aplicației pentru convertirea YouTube în MP3.

## Ce conține acest proiect

- `app.py` - server web Flask
- `converter_core.py` - logică de conversie și descărcare YouTube
- `templates/index.html` - interfața web
- `static/style.css` - stilul paginii
- `bin/yt-dlp` - utilitarul yt-dlp folosit pentru descărcarea video-urilor YouTube

## Cerințe

- Python 3.9+
- `yt-dlp` instalat local sau inclus în `bin/yt-dlp`
- `ffmpeg` disponibil în sistem sau folosit prin `imageio-ffmpeg`

## Instalare

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Rulare

```bash
python app.py
```

Apoi deschide în browser:

```text
http://127.0.0.1:5000
```

Aplicația salvează automat fișierele MP3 în folderul `downloads/`.

> Folosește aplicația doar pentru conținutul tău sau materiale pe care ai dreptul să le descarci și să le convertești.
