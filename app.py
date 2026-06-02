from __future__ import annotations

from pathlib import Path

from flask import Flask, abort, flash, redirect, render_template, request, send_from_directory, url_for
from converter_core import convert_to_mp3 as convert_url_to_mp3
from converter_core import is_youtube_url


BASE_DIR = Path(__file__).resolve().parent
DOWNLOAD_DIR = BASE_DIR / "downloads"


app = Flask(__name__)
app.config["SECRET_KEY"] = "change-this-local-secret"
DOWNLOAD_DIR.mkdir(exist_ok=True)


def convert_to_mp3(video_url: str) -> tuple[str, str]:
    final_name, title, _ = convert_url_to_mp3(video_url, DOWNLOAD_DIR)
    return final_name, title


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        video_url = request.form.get("video_url", "").strip()

        if not video_url:
            flash("Introdu un link YouTube.", "error")
            return redirect(url_for("index"))

        if not is_youtube_url(video_url):
            flash("Linkul trebuie sa fie de la YouTube.", "error")
            return redirect(url_for("index"))

        try:
            filename, title = convert_to_mp3(video_url)
        except Exception as exc:
            flash(str(exc), "error")
            return redirect(url_for("index"))

        return render_template(
            "index.html",
            converted_file=filename,
            converted_title=title,
        )

    return render_template("index.html")


@app.route("/download/<path:filename>")
def download(filename: str):
    file_path = DOWNLOAD_DIR / filename
    if not file_path.exists() or not file_path.is_file():
        abort(404)
    return send_from_directory(DOWNLOAD_DIR, filename, as_attachment=True)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
