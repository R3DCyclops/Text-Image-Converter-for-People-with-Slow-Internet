import sys
import os
import zlib
import base64
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QFileDialog, QTextEdit,
    QLineEdit, QHBoxLayout, QMessageBox
)
from PySide6.QtGui import QPixmap, QImage, QIcon
from PySide6.QtCore import Qt
from PIL import Image
import numpy as np


class ImageTextConverter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Text Image Converter for People with Slow Internet")
        self.setGeometry(100, 100, 400, 600)

        self.setWindowIcon(self.get_icon("ico.ico"))

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.image_label = QLabel("Load an image:")
        self.image_label.setStyleSheet("color: white;")
        self.layout.addWidget(self.image_label)

        self.upload_button = QPushButton("Load Image")
        self.upload_button.setStyleSheet("background-color: lightgray; color: black;")
        self.upload_button.clicked.connect(self.load_image)
        self.layout.addWidget(self.upload_button)

        self.image_container = QHBoxLayout()
        self.image_container.addStretch()
        self.image_preview = QLabel()
        self.image_preview.setAlignment(Qt.AlignCenter)
        self.image_container.addWidget(self.image_preview)
        self.image_container.addStretch()
        self.layout.addLayout(self.image_container)

        self.convert_button = QPushButton("Convert to Text")
        self.convert_button.setStyleSheet("background-color: lightgray; color: black;")
        self.convert_button.clicked.connect(self.convert_to_text)
        self.layout.addWidget(self.convert_button)

        self.text_output = QTextEdit()
        self.text_output.setReadOnly(True)
        self.text_output.setStyleSheet("background-color: darkgray; color: white;")
        self.layout.addWidget(self.text_output)

        self.copy_button = QPushButton("Copy Text")
        self.copy_button.setStyleSheet("background-color: lightgray; color: black;")
        self.copy_button.clicked.connect(self.copy_text)
        self.layout.addWidget(self.copy_button)

        self.text_label = QLabel("Paste text for decoding:")
        self.text_label.setStyleSheet("color: white;")
        self.layout.addWidget(self.text_label)

        self.text_input = QLineEdit()
        self.text_input.setStyleSheet("background-color: white; color: black;")
        self.layout.addWidget(self.text_input)

        self.clear_input_button = QPushButton("Clear Input")
        self.clear_input_button.setStyleSheet("background-color: lightgray; color: black;")
        self.clear_input_button.clicked.connect(self.clear_input)
        self.layout.addWidget(self.clear_input_button)

        self.decode_button = QPushButton("Convert to Image")
        self.decode_button.setStyleSheet("background-color: lightgray; color: black;")
        self.decode_button.clicked.connect(self.decode_to_image)
        self.layout.addWidget(self.decode_button)

        self.decoded_image_container = QHBoxLayout()
        self.decoded_image_container.addStretch()
        self.decoded_image_preview = QLabel()
        self.decoded_image_preview.setAlignment(Qt.AlignCenter)
        self.decoded_image_container.addWidget(self.decoded_image_preview)
        self.decoded_image_container.addStretch()
        self.layout.addLayout(self.decoded_image_container)

        self.save_button = QPushButton("Save Image")
        self.save_button.setStyleSheet("background-color: lightgray; color: black;")
        self.save_button.clicked.connect(self.save_image)
        self.layout.addWidget(self.save_button)

        self.image = None
        self.pixels = None
        self.decoded_image = None

        self.central_widget.setStyleSheet("background-color: #2c2c2c;")

    def get_icon(self, icon_name):
        if getattr(sys, 'frozen', False):
            application_path = sys._MEIPASS
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))
        return QIcon(os.path.join(application_path, icon_name))

    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            try:
                img = Image.open(file_path).convert("L")
                img = img.resize((100, 100), Image.Resampling.LANCZOS)
                self.image = img
                self.pixels = np.array(img)

                qimage = QImage(
                    self.pixels.data, 100, 100, 100, QImage.Format_Grayscale8
                )
                pixmap = QPixmap.fromImage(qimage)
                self.image_preview.setPixmap(pixmap)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Image loading error: {e}")

    def convert_to_text(self):
        if self.pixels is None:
            return

        height, width = self.pixels.shape
        raw_text = ""
        for row in range(height):
            for col in range(width):
                pixel_value = self.pixels[row, col]
                raw_text += str(int(pixel_value / 255 * 9))
            raw_text += "-"

        raw_text = raw_text.rstrip("-")
        compressed = zlib.compress(raw_text.encode("utf-8"))
        encoded = base64.b64encode(compressed).decode("utf-8")
        self.text_output.setText(encoded)

    def copy_text(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.text_output.toPlainText())

    def decode_to_image(self):
        encoded = self.text_input.text()
        if not encoded:
            return

        try:
            compressed = base64.b64decode(encoded)
            raw_text = zlib.decompress(compressed).decode("utf-8")

            rows = raw_text.split("-")
            height = len(rows)
            width = len(rows[0])

            pixels = np.zeros((height, width), dtype=np.uint8)
            for row_idx, row in enumerate(rows):
                for col_idx, char in enumerate(row):
                    value = int(char)
                    pixels[row_idx, col_idx] = int(value / 9 * 255)

            img = Image.fromarray(pixels, mode="L")
            self.decoded_image = img

            qimage = QImage(
                pixels.data, width, height, width, QImage.Format_Grayscale8
            )
            pixmap = QPixmap.fromImage(qimage)
            self.decoded_image_preview.setPixmap(pixmap)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Decoding error: {e}")

    def save_image(self):
        if self.decoded_image is None:
            QMessageBox.warning(self, "Error", "No image to save!")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Image", "", "PNG Files (*.png);;JPEG Files (*.jpg)"
        )
        if file_path:
            try:
                self.decoded_image.save(file_path)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Image saving error: {e}")

    def clear_input(self):
        self.text_input.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageTextConverter()
    window.show()
    sys.exit(app.exec())
