# scan_completed.py
from PyQt6.QtWidgets import QWidget
from PyQt6 import uic

class ScanCompletedWindow(QWidget):
    def __init__(self, part_name, parent=None):
        super().__init__(parent)
        uic.loadUi("scan_complete.ui", self)
        self.part_name = part_name
        self.setWindowTitle("Scan Completed")

        if hasattr(self, "completedLabel"):
            self.completedLabel.setText(f"✅ Part '{part_name}' scanning completed!\nYou can now go to the Results screen.")
