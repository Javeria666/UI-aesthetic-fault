# top_scan.py
from PyQt6.QtWidgets import QWidget
from PyQt6 import uic
from PyQt6.QtCore import QTimer, pyqtSignal

class TopScanWindow(QWidget):
    finished = pyqtSignal(str)  # ✅ Signal emits part_name

    def __init__(self, part_name=None, parent=None):
        super().__init__(parent)
        uic.loadUi("top_scan.ui", self)

        self.part_name = part_name or "Selected Part"
        self.setWindowTitle(f"Top Scan: {self.part_name}")

        if hasattr(self, "scanLabel"):
            self.scanLabel.setText(f"Scanning Top of {self.part_name}...")

        self.progress_value = 0
        self.scanProgressBar.setValue(0)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(50)

    def update_progress(self):
        if self.progress_value < 100:
            self.progress_value += 1
            self.scanProgressBar.setValue(self.progress_value)
        else:
            self.timer.stop()
            self.finish_scan()

    def finish_scan(self):
        print(f"✅ Top scan for {self.part_name} completed.")
        self.finished.emit(self.part_name)  # ✅ Emit when done
        self.close()
