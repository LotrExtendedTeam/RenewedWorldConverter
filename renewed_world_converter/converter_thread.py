import os
import shutil
import subprocess
#from pathlib import Path

from PyQt6.QtCore import QThread, pyqtSignal

class ConverterThread(QThread):
    log_signal = pyqtSignal(str)
    done_signal = pyqtSignal()

    def __init__(self, legacy_path, renewed_path, jar_path):
        super().__init__()
        self.legacy_path = legacy_path
        self.renewed_path = renewed_path
        self.jar_path = jar_path

    def run(self):
        jar_dir = os.path.dirname(os.path.abspath(self.jar_path))
        legacy_name = os.path.basename(self.legacy_path.rstrip("/\\"))
        renewed_name = os.path.basename(self.renewed_path.rstrip("/\\"))

        # Copy legacy world (BLOCKING)
        temp_legacy = os.path.join(jar_dir, legacy_name)
        if os.path.exists(temp_legacy):
            shutil.rmtree(temp_legacy)
        self.log_signal.emit(f"Copying input world to {temp_legacy}...")
        shutil.copytree(self.legacy_path, temp_legacy)

        # Copy renewed world (BLOCKING)
        temp_renewed = os.path.join(jar_dir, renewed_name)
        if os.path.exists(temp_renewed):
            shutil.rmtree(temp_renewed)
        self.log_signal.emit(f"Copying input world to {temp_renewed}...")
        shutil.copytree(self.renewed_path, temp_renewed)

        # Launch Java after copy completes
        process = subprocess.Popen(
            ["java", "-jar", self.jar_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            cwd=jar_dir
        )
        for line in process.stdout:
            self.log_signal.emit(line)
        process.wait()

        # TODO: Update to Copy _Converted world back to renewed saves folder
        #output_folder = os.path.join(jar_dir, renewed_name + "_Converted")
        #final_location = Path(self.renewed_path).parent.joinpath(legacy_name + "_Converted")
        # if os.path.exists(self.output_path):
        #   shutil.rmtree(self.output_path)
        #shutil.copytree(temp_output, self.output_path)

        self.done_signal.emit()
