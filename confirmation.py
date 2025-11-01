# confirmation.py
from PyQt6.QtWidgets import QWidget
from PyQt6 import uic
from PyQt6.QtCore import Qt
from top_scan import TopScanWindow
from flip_part import FlipInstructionScreen
from bottom_scan import BottomScanWindow
from scan_complete import ScanCompletedWindow 
from app_state import AppState


class ConfirmationWindow(QWidget):
    def __init__(self, part_name, parent=None):
        super().__init__()
        uic.loadUi("confirmation.ui", self)

        self.part_name = part_name
        self.parent_window = parent  # ✅ Store parent (PartSelectorApp)
        self.setWindowTitle("Part Confirmation")

        # Update UI labels
        if hasattr(self, "selectedPartButton"):
            self.selectedPartButton.setText(part_name)


        # Connect buttons
        self.nextButton.clicked.connect(self.go_next)
        self.backButton.clicked.connect(self.go_back)

    # -----------------------------
    # NEXT BUTTON → Go to Top Scan
    # -----------------------------
    def go_next(self):
        print(f"➡️ Next pressed for {self.part_name}")
        self.hide()
        self.top_scan_window = TopScanWindow(self.part_name)

        # ✅ Connect to signal when top scan finishes
        if hasattr(self.top_scan_window, "finished"):
            self.top_scan_window.finished.connect(self.show_flip_screen)

        self.top_scan_window.showMaximized()

    # -----------------------------
    # After Top Scan → Flip Screen
    # -----------------------------
    def show_flip_screen(self, part_name):
        print(f"Opening Flip Screen for {part_name}")
        self.top_scan_window.close()
        self.flip_screen = FlipInstructionScreen()

        self.flip_screen.next_clicked.connect(self.next_stage)
        self.flip_screen.showMaximized()

    # -----------------------------
    # Proceed to Bottom Scan
    # -----------------------------
    def next_stage(self):
        print("Proceeding to Bottom Scan...")
        self.flip_screen.close()
        self.bottom_scan = BottomScanWindow(self.part_name)
        if hasattr(self.bottom_scan, "scan_complete"):
            self.bottom_scan.scan_complete.connect(self.show_scan_completed)

        self.bottom_scan.showMaximized()
     # -----------------------------
    # Show Scan Completed Screen
    # -----------------------------
    def show_scan_completed(self, part_name):
        print(f"✅ Scan Completed for {part_name}")
        if self.bottom_scan:
          self.bottom_scan.close()
        self.scan_completed_window = ScanCompletedWindow(part_name)
        self.scan_completed_window.showMaximized()
    # -----------------------------
    # BACK BUTTON → Return to Selection
    # confirmation.py (Inside ConfirmationWindow class)

    # -----------------------------
    # BACK BUTTON → Return to Selection
    # confirmation.py

# ... (imports) ...
    # BACK BUTTON → Return to Selection
    def go_back(self):
        print("⬅️ Going back to part selection.")
        self.close()

        if not self.parent_window:
            return

        # ✅ Restore parent visibility
        self.parent_window.show()
        self.parent_window.showMaximized()
        self.parent_window.raise_()
        self.parent_window.activateWindow()

        # ✅ Determine login state correctly
        if hasattr(self.parent_window, 'login_dialog') and self.parent_window.login_dialog.is_logged_in:
            print("Restoring logged-in state...")
            self.parent_window.set_state(AppState.LOGIN_SUCCESS)
        else:
            print("Restoring guest state...")
            self.parent_window.set_state(AppState.PART_SELECTION_SCREEN)
