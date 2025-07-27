import sys
from PyQt6.QtWidgets import QApplication
from .converter_gui import ConverterGUI

def main():
    app = QApplication(sys.argv)
    window = ConverterGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()