import os

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QTextEdit, QLabel, QFileDialog
from pathlib import Path

from .converter_thread import ConverterThread
from .settings import JAR_PATH

class ConverterGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Minecraft Legacy World Converter")
        self.setGeometry(300, 200, 600, 400)

        layout = QVBoxLayout()

        # Input world
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        input_button = QPushButton("Browse")
        input_button.clicked.connect(self.select_input)
        input_layout.addWidget(QLabel("Input World:"))
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(input_button)
        layout.addLayout(input_layout)

        # Output world
        output_layout = QHBoxLayout()
        self.output_field = QLineEdit()
        output_button = QPushButton("Browse")
        output_button.clicked.connect(self.select_output)
        output_layout.addWidget(QLabel("Output World:"))
        output_layout.addWidget(self.output_field)
        output_layout.addWidget(output_button)
        layout.addLayout(output_layout)

        # Log window
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        layout.addWidget(self.log_box)

        # Convert button
        self.convert_button = QPushButton("Convert")
        self.convert_button.clicked.connect(self.run_conversion)
        layout.addWidget(self.convert_button)

        self.setLayout(layout)

    def select_input(self):
        path = QFileDialog.getExistingDirectory(self, "Select Input World")
        if path:
            self.input_field.setText(path)

    def select_output(self):
        path = QFileDialog.getExistingDirectory(self, "Select Output World")
        if path:
            self.output_field.setText(path)

    def run_conversion(self, ):
        legacy_path = self.input_field.text()
        renewed_path = self.output_field.text()
        if not legacy_path or not renewed_path:
            self.log_box.append("ERROR: Please select both input and output directories.")
            return

        jar_dir = os.path.dirname(os.path.abspath(JAR_PATH))
        legacy_name = os.path.basename(legacy_path.rstrip("/\\"))
        renewed_name = os.path.basename(renewed_path.rstrip("/\\"))

        self.convert_button.setEnabled(False)

        # Use these temporary relative paths
        self.thread = ConverterThread(legacy_path, renewed_path, JAR_PATH)
        self.thread.log_signal.connect(self.append_log)
        self.thread.done_signal.connect(lambda: self.conversion_done())
        self.thread.start()


    def append_log(self, text):
        self.log_box.append(text.strip())

    def conversion_done(self):
        self.log_box.append("The converter process has exited.")
        self.convert_button.setEnabled(True)
        return 0
