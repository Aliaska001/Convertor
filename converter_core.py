from __future__ import annotations

import re
import shutil
import subprocess
import sys
import uuid
from pathlib import Path
from urllib.parse import urlparse

from imageio_ffmpeg import get_ffmpeg_exe


def app_base_dir() -> Path:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)  # type: ignore[attr-defined]
    return Path(__file__).resolve().parent


BASE_DIR = app_base_dir()
BIN_DIR = BASE_DIR / "bin"
ALLOWED_HOSTS = {
    "youtube.com",
    "www.youtube.com",
    "m.youtube.com",
    "music.youtube.com",
    "youtu.be",
}


def is_youtube_url(url: str) -> bool:
    parsed = urlparse(url.strip())
    host = parsed.netloc.lower()
    host_without_www = host[4:] if host.startswith("www.") else host
    return parsed.scheme in {"http", "https"} and host_without_www in ALLOWED_HOSTS


def clean_filename(name: str) -> str:
    cleaned = re.sub(r"[^\w\s().,\-'&]+", "", name, flags=re.UNICODE)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned[:120] or f"audio-{uuid.uuid4().hex[:8]}"


def get_ytdlp_command() -> list[str]:
    bundled_name = "yt-dlp.exe" if sys.platform.startswith("win") else "yt-dlp"
    bundled = BIN_DIR / bundled_name
    if bundled.exists():
        return [str(bundled)]

    fallback = shutil.which("yt-dlp")
    if fallback:
        return [fallback]

    raise RuntimeError(
        f"yt-dlp nu este disponibil. Lipseste fisierul bin/{bundled_name}."
    )


def get_js_runtime_args() -> list[str]:
    deno_path = shutil.which("deno")
    if deno_path:
        return ["--js-runtimes", f"deno:{deno_path}"]

    node_path = shutil.which("node")
    if node_path:
        return ["--js-runtimes", f"node:{node_path}"]

    return []


def run_ytdlp(args: list[str], timeout: int = 300) -> subprocess.CompletedProcess[str]:
    command = get_ytdlp_command() + get_js_runtime_args() + args
    return subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
        timeout=timeout,
    )


def get_video_title(video_url: str) -> str:
    result = run_ytdlp(["--no-playlist", "--skip-download", "--print", "title", video_url], timeout=60)
    if result.returncode != 0:
        return "audio"
    title = result.stdout.strip().splitlines()[-1] if result.stdout.strip() else "audio"
    return clean_filename(title)


def format_ytdlp_error(output: str) -> str:
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    if not lines:
        return "Conversia a esuat fara un mesaj detaliat."
    return "\n".join(lines[-6:])


def get_ffmpeg_path() -> str:
    ffmpeg_path = shutil.which("ffmpeg") or get_ffmpeg_exe()
    if not ffmpeg_path:
        raise RuntimeError("FFmpeg nu este disponibil. Ruleaza din nou instalarea dependintelor.")
    return ffmpeg_path


def convert_to_mp3(video_url: str, output_dir: Path) -> tuple[str, str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)

    ffmpeg_path = get_ffmpeg_path()
    job_id = uuid.uuid4().hex
    output_template = str(output_dir / f"{job_id}.%(ext)s")
    title = get_video_title(video_url)

    result = run_ytdlp(
        [
            "--no-playlist",
            "--format",
            "bestaudio/best",
            "--extract-audio",
            "--audio-format",
            "mp3",
            "--audio-quality",
            "192K",
            "--ffmpeg-location",
            ffmpeg_path,
            "--output",
            output_template,
            video_url,
        ]
    )

    if result.returncode != 0:
        raise RuntimeError(format_ytdlp_error(result.stderr or result.stdout))

    generated_file = output_dir / f"{job_id}.mp3"
    if not generated_file.exists():
        raise RuntimeError("Conversia s-a terminat, dar fisierul MP3 nu a fost gasit.")

    final_name = f"{title}.mp3"
    final_path = output_dir / final_name
    counter = 2
    while final_path.exists():
        final_name = f"{title} ({counter}).mp3"
        final_path = output_dir / final_name
        counter += 1

    generated_file.rename(final_path)
    return final_name, title, final_path
