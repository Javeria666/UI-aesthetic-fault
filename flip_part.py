# flip_part.py
from PyQt6.QtWidgets import QWidget
from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal

class FlipInstructionScreen(QWidget):
    next_clicked = pyqtSignal()  # ✅ Signal for Next button

    def __init__(self):
        super().__init__()
        uic.loadUi("flip_part.ui", self)
        self.nextButton.clicked.connect(self.handle_next)

    def handle_next(self):
        print("Next button clicked!")
        self.next_clicked.emit()  # ✅ Let main app decide what happens next
