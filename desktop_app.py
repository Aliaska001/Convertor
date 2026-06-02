from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QFileDialog,
    QMessageBox,
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QColor

from converter_core import convert_to_mp3, is_youtube_url


APP_TITLE = "Convertor YouTube in MP3"


def default_download_dir() -> Path:
    downloads = Path.home() / "Downloads"
    return downloads if downloads.exists() else Path.home()


class ConversionThread(QThread):
    finished = pyqtSignal(str, Path)
    error = pyqtSignal(str)

    def __init__(self, url: str, output_dir: Path) -> None:
        super().__init__()
        self.url = url
        self.output_dir = output_dir

    def run(self) -> None:
        try:
            filename, _title, path = convert_to_mp3(self.url, self.output_dir)
            self.finished.emit(filename, path)
        except Exception as exc:
            self.error.emit(str(exc))


class ConverterApp(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(APP_TITLE)
        self.setGeometry(100, 100, 700, 550)
        self.last_file: Path | None = None
        self.conversion_thread: ConversionThread | None = None

        self.init_ui()
        self.apply_styles()

    def init_ui(self) -> None:
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)

        # Title
        title = QLabel(APP_TITLE)
        title_font = QFont("Arial", 20, QFont.Bold)
        title.setFont(title_font)
        main_layout.addWidget(title)

        # Subtitle
        subtitle = QLabel("Introdu un link YouTube si converteste audio in MP3")
        subtitle.setStyleSheet("color: #5f6b61; font-size: 12px;")
        main_layout.addWidget(subtitle)

        # Spacing
        main_layout.addSpacing(10)

        # URL Input
        url_label = QLabel("Link YouTube")
        url_label.setStyleSheet("font-weight: bold; color: #17201a;")
        main_layout.addWidget(url_label)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://www.youtube.com/watch?v=...")
        main_layout.addWidget(self.url_input)

        # Folder Selection
        folder_label = QLabel("Folder salvare")
        folder_label.setStyleSheet("font-weight: bold; color: #17201a;")
        main_layout.addWidget(folder_label)

        folder_layout = QHBoxLayout()
        self.folder_input = QLineEdit()
        self.folder_input.setText(str(default_download_dir()))
        folder_layout.addWidget(self.folder_input)

        self.folder_button = QPushButton("Alege folder")
        self.folder_button.clicked.connect(self.choose_folder)
        self.folder_button.setStyleSheet(
            "background-color: #eef4f0; color: #17201a; border: none; padding: 5px 15px; border-radius: 4px;"
        )
        folder_layout.addWidget(self.folder_button)
        main_layout.addLayout(folder_layout)

        # Spacing
        main_layout.addSpacing(10)

        # Buttons
        button_layout = QHBoxLayout()

        self.convert_button = QPushButton("Converteste in MP3")
        self.convert_button.clicked.connect(self.start_conversion)
        self.convert_button.setStyleSheet(
            "background-color: #1f7a5f; color: white; border: none; padding: 10px 20px; border-radius: 4px; font-weight: bold;"
        )
        button_layout.addWidget(self.convert_button)

        self.open_button = QPushButton("Deschide folderul")
        self.open_button.clicked.connect(self.open_output_folder)
        self.open_button.setEnabled(False)
        self.open_button.setStyleSheet(
            "background-color: #eef4f0; color: #17201a; border: none; padding: 10px 20px; border-radius: 4px;"
        )
        button_layout.addWidget(self.open_button)

        main_layout.addLayout(button_layout)

        # Spacing
        main_layout.addSpacing(10)

        # Status
        self.status_label = QLabel("Introdu un link YouTube si alege folderul pentru MP3.")
        self.status_label.setStyleSheet("color: #17201a; font-size: 11px;")
        main_layout.addWidget(self.status_label)

        # Messages
        self.messages = QTextEdit()
        self.messages.setReadOnly(True)
        self.messages.setMaximumHeight(80)
        self.messages.setStyleSheet(
            "background-color: #ffffff; color: #17201a; border: 1px solid #dbe3d8; border-radius: 4px;"
        )
        main_layout.addWidget(self.messages)

        main_layout.addStretch()

        central_widget.setLayout(main_layout)

    def apply_styles(self) -> None:
        stylesheet = """
        QMainWindow, QWidget {
            background-color: #ffffff;
            color: #17201a;
        }
        QLineEdit {
            background-color: #ffffff;
            color: #17201a;
            border: 1px solid #dbe3d8;
            border-radius: 4px;
            padding: 5px;
            font-size: 11px;
        }
        QLineEdit:focus {
            border: 2px solid #1f7a5f;
        }
        QLabel {
            color: #17201a;
        }
        """
        self.setStyleSheet(stylesheet)

    def choose_folder(self) -> None:
        folder = QFileDialog.getExistingDirectory(
            self,
            "Alege folder",
            self.folder_input.text(),
        )
        if folder:
            self.folder_input.setText(folder)

    def start_conversion(self) -> None:
        url = self.url_input.text().strip()
        output_dir = Path(self.folder_input.text()).expanduser()

        if not url:
            self.show_message("❌ Introdu un link YouTube.", error=True)
            return

        if not is_youtube_url(url):
            self.show_message("❌ Linkul trebuie sa fie de la YouTube.", error=True)
            return

        self.convert_button.setEnabled(False)
        self.open_button.setEnabled(False)
        self.status_label.setText("Se converteste. Poate dura cateva minute...")
        self.messages.clear()

        self.conversion_thread = ConversionThread(url, output_dir)
        self.conversion_thread.finished.connect(self.on_conversion_success)
        self.conversion_thread.error.connect(self.on_conversion_error)
        self.conversion_thread.start()

    def on_conversion_success(self, filename: str, path: Path) -> None:
        self.last_file = path
        self.status_label.setText(f"✓ Conversie finalizata: {filename}")
        self.show_message(f"✓ MP3 salvat cu succes!\n{path}", error=False)
        self.open_button.setEnabled(True)
        self.convert_button.setEnabled(True)

        QMessageBox.information(
            self,
            APP_TITLE,
            f"Fisierul MP3 a fost salvat:\n{path}",
        )

    def on_conversion_error(self, error: str) -> None:
        self.status_label.setText("❌ Conversia a esuat.")
        self.show_message(f"❌ {error}", error=True)
        self.convert_button.setEnabled(True)

        QMessageBox.critical(
            self,
            APP_TITLE,
            error,
        )

    def show_message(self, text: str, error: bool = False) -> None:
        if error:
            self.messages.setStyleSheet(
                "background-color: #fff1f0; color: #b42318; border: 1px solid #ffd1cc; border-radius: 4px; padding: 8px;"
            )
        else:
            self.messages.setStyleSheet(
                "background-color: #e7f6ef; color: #1f7a5f; border: 1px solid #c4e7d7; border-radius: 4px; padding: 8px;"
            )
        self.messages.setText(text)

    def open_output_folder(self) -> None:
        if not self.last_file:
            return

        folder = self.last_file.parent
        if sys.platform.startswith("win"):
            os.startfile(folder)  # type: ignore[attr-defined]
        elif sys.platform == "darwin":
            subprocess.run(["open", str(folder)], check=False)
        else:
            subprocess.run(["xdg-open", str(folder)], check=False)


def main() -> None:
    app = QApplication(sys.argv)
    window = ConverterApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
