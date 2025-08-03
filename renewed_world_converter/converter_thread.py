import os
import shutil
import subprocess
from pathlib import Path
from .utils import get_temp_work_dir, extract_resources

from PyQt6.QtCore import QThread, pyqtSignal

class ConverterThread(QThread):
    log_signal = pyqtSignal(str)
    done_signal = pyqtSignal()

    def __init__(self, legacy_path, renewed_path):
        super().__init__()
        self.legacy_path = legacy_path
        self.renewed_path = renewed_path

    def run(self):
        legacy_name = os.path.basename(self.legacy_path.rstrip("/\\"))
        renewed_name = os.path.basename(self.renewed_path.rstrip("/\\"))

        temp_dir = get_temp_work_dir()
        self.log_signal.emit(f"Using temporary working directory: {temp_dir}")

        # Extract JAR + Conversions.json into it
        jar_path, conv_path = extract_resources(temp_dir)
        self.log_signal.emit("Extracted converter resources.")

        # Copy legacy world (BLOCKING)
        temp_legacy = os.path.join(temp_dir, legacy_name)
        if os.path.exists(temp_legacy):
            shutil.rmtree(temp_legacy)
        self.log_signal.emit(f"Copying input world to {temp_legacy}...")
        shutil.copytree(self.legacy_path, temp_legacy)

        # Copy renewed world (BLOCKING)
        temp_renewed = os.path.join(temp_dir, renewed_name)
        if os.path.exists(temp_renewed):
            shutil.rmtree(temp_renewed)
        self.log_signal.emit(f"Copying input world to {temp_renewed}...")
        shutil.copytree(self.renewed_path, temp_renewed)

        # Launch Java after copy completes
        self.log_signal.emit("Launching converter...")
        process = subprocess.Popen(
            ["java", "-jar", jar_path, "-s"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            cwd=temp_dir
        )
        for line in process.stdout:
            self.log_signal.emit(line)
        process.wait()

        #  Copy _Converted world back to the renewed saves folder
        output_folder = os.path.join(temp_dir, legacy_name + "_Converted")
        final_location = Path(self.renewed_path).parent.joinpath(legacy_name + "_Converted")
        self.log_signal.emit(f"Copying {legacy_name}_Converted to {final_location}...")
        if os.path.exists(final_location):
           shutil.rmtree(final_location)
        shutil.copytree(output_folder, final_location)

        self.done_signal.emit()
