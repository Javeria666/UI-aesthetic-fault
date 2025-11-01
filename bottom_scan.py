from PyQt6.QtWidgets import QWidget
from PyQt6 import uic
from PyQt6.QtCore import QTimer, pyqtSignal

class BottomScanWindow(QWidget):
    scan_complete = pyqtSignal(str)
    def __init__(self, part_name, parent=None):
        super().__init__(parent)
        uic.loadUi("bottom_scan.ui", self)
        self.part_name = part_name
        self.setWindowTitle(f"Bottom Scan - {part_name}")

        if hasattr(self, "scanLabel"):
            self.scanLabel.setText(f"Scanning bottom of {part_name}...")

        if hasattr(self, "scanProgressBar"):
            self.scanProgressBar.setValue(0)
            self.progress_value = 0
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
            print(f"✅ Bottom scan for {self.part_name} completed.")
    def finish_scan(self):
        print(f"✅ Bottom scan for {self.part_name} completed.")
        self.scan_complete.emit(self.part_name)  # ✅ Emit signal when finished
        self.close()