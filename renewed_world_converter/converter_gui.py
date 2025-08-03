from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QTextEdit, QLabel, QFileDialog
from renewed_world_converter.converter_thread import ConverterThread

class ConverterGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Minecraft Legacy World Converter")
        self.setGeometry(300, 200, 600, 400)

        layout = QVBoxLayout()

        # Legacy world
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        input_button = QPushButton("Browse")
        input_button.clicked.connect(self.select_input)
        input_layout.addWidget(QLabel("Legacy World:"))
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(input_button)
        layout.addLayout(input_layout)

        # Renewed world
        output_layout = QHBoxLayout()
        self.output_field = QLineEdit()
        output_button = QPushButton("Browse")
        output_button.clicked.connect(self.select_output)
        output_layout.addWidget(QLabel("Renewed World:"))
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
        path = QFileDialog.getExistingDirectory(self, "Select Legacy World")
        if path:
            self.input_field.setText(path)

    def select_output(self):
        path = QFileDialog.getExistingDirectory(self, "Select Renewed World")
        if path:
            self.output_field.setText(path)

    def run_conversion(self, ):
        legacy_path = self.input_field.text()
        renewed_path = self.output_field.text()
        if not legacy_path or not renewed_path:
            self.log_box.append("ERROR: Please select both Legacy and Renewed world directories.")
            return

        self.convert_button.setEnabled(False)

        # Use these temporary relative paths
        self.thread = ConverterThread(legacy_path, renewed_path)
        self.thread.log_signal.connect(self.append_log)
        self.thread.done_signal.connect(lambda: self.conversion_done())
        self.thread.start()


    def append_log(self, text):
        self.log_box.append(text.strip())

    def conversion_done(self):
        self.log_box.append("The converter process has exited.")
        self.convert_button.setEnabled(True)
        return 0
