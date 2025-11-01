# main.py
import sys
from PyQt6.QtWidgets import QApplication
from part_selection import PartSelectorApp

def main():
    app = QApplication(sys.argv)
    window = PartSelectorApp()
    window.showMaximized()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
