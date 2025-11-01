#part_selection.py
import sys
from PyQt6.QtWidgets import QWidget, QDialog, QMessageBox
from PyQt6 import uic
from PyQt6.QtCore import Qt
from imageloader import load_images_for_buttons
from app_state import AppState  # ✅ shared enum, no circular import


# ==========================================================
# LOGIN DIALOG CLASS
# ==========================================================
class LoginDialog(QDialog):
    """Dialog window for Supervisor/Quality Team login."""

    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("login_dialog.ui", self)
        self._logged_in = False
        self.loginButton.clicked.connect(self.check_credentials)
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)
        print("LoginDialog initialized.")

    def reset_fields(self):
        self.usernameEdit.clear()
        self.passwordEdit.clear()
        print("LoginDialog fields reset.")

    @property
    def is_logged_in(self):
        return self._logged_in

    def check_credentials(self):
        username = self.usernameEdit.text().strip()
        password = self.passwordEdit.text().strip()

        DUMMY_CREDENTIALS = {"supervisor": "pass123", "quality": "secure456"}

        if username in DUMMY_CREDENTIALS and password == DUMMY_CREDENTIALS[username]:
            QMessageBox.information(self, "Login Success", f"Welcome, {username.title()}!")
            self._logged_in = True
            self.accept()
        else:
            QMessageBox.critical(self, "Login Failed", "Invalid Username or Password.")
            self.passwordEdit.clear()
            self._logged_in = False


# ==========================================================
# MAIN APPLICATION CLASS
# ==========================================================
class PartSelectorApp(QWidget):
    """Main application window for part selection and login handling."""

    def __init__(self):
        super().__init__()
        uic.loadUi("part_selection.ui", self)

        self.current_state = None
        self.selected_part = None
        self.login_dialog = LoginDialog(self)

        # Window flags
        self.setWindowFlags(
            Qt.WindowType.Window |
            Qt.WindowType.WindowMinimizeButtonHint |
            Qt.WindowType.WindowMaximizeButtonHint |
            Qt.WindowType.WindowCloseButtonHint
        )
        self.showMaximized()

        # Connect buttons
        self.selectButton.clicked.connect(self.confirm_selection)
        self.loginButton.clicked.connect(self.login_action)

        # Load part images
        self.image_files = [
            "image1.jpeg", "image2.jpeg",
            "meow.jpeg", "meow.jpeg", "meow.jpeg", "meow.jpeg",
            "meow.jpeg", "meow.jpeg", "meow.jpeg", "meow.jpeg",
            "meow.jpeg", "meow.jpeg"
        ]

        # Load part buttons dynamically
        self.part_buttons = [
            getattr(self, f"partButton{i}") for i in range(1, 21)
            if hasattr(self, f"partButton{i}")
        ]

        load_images_for_buttons(self.part_buttons, self.image_files)
        self.set_state(AppState.PART_SELECTION_SCREEN)
         # ✅ Hide welcome label initially (if exists)
        if hasattr(self, "welcomeLabel"):
            self.welcomeLabel.hide()
    # ---------------- STATE MANAGEMENT ----------------
    def set_state(self, new_state):
        if self.current_state != new_state:
            old_state = self.current_state.name if self.current_state else "None"
            self.current_state = new_state
            print(f"--- State changed from {old_state} to {self.current_state.name} ---")

            try:
                self.loginButton.clicked.disconnect()
            except TypeError:
                pass

            if self.current_state == AppState.LOGIN_SUCCESS:
                self.loginButton.setText("Log Out")
                self.loginButton.setStyleSheet(
                    "background-color: #F44336; color: white; font-size: 12pt; "
                    "font-weight: bold; padding: 10px 20px; border-radius: 8px; border: none;"
                )
                self.loginButton.clicked.connect(self.logout_action)
            else:
                self.loginButton.setText("Login")
                self.loginButton.setStyleSheet("")
                self.loginButton.clicked.connect(self.login_action)

    # ---------------- ACTIONS ----------------
    def confirm_selection(self):
        self.set_state(AppState.SELECT_PRESSED)
        selected_button = self.partButtonGroup.checkedButton()

        if selected_button:
            part_name = selected_button.text()
            self.selected_part = part_name
            print(f"Confirmed Selection: '{part_name}'")
            self.open_confirmation_screen(part_name)
        else:
            print("No part selected.")

    def open_confirmation_screen(self, part_name):
        from confirmation import ConfirmationWindow
        self.set_state(AppState.PART_CONFIRMATION_SCREEN)

        print("Creating ConfirmationWindow...")
        self.hide()

        self.confirmation_window = ConfirmationWindow(part_name, parent=self)
        print("ConfirmationWindow object created.")
        self.confirmation_window.showMaximized()
        print("ConfirmationWindow shown.")

    def login_action(self):
        self.set_state(AppState.LOGIN_SCREEN_OPEN)
        result = self.login_dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            username = self.login_dialog.usernameEdit.text().strip()
            self.set_username(username)
            self.set_state(AppState.LOGIN_SUCCESS)
            print(f"Login successful for user: {username}")

        else:
            self.set_state(AppState.PART_SELECTION_SCREEN)
            print("Login failed or cancelled.")

        # ---------------- UI HELPERS ----------------
    def set_username(self, username):
        """Display 'Welcome (username)!' at the top of the screen."""
        if hasattr(self, "welcomeLabel"):
            self.welcomeLabel.setText(f"Welcome, {username}!")
            self.welcomeLabel.setStyleSheet(
                "font-size: 16pt; font-weight: bold; color: #2E8B57; padding: 8px;"
            )
            self.welcomeLabel.show()
        else:
            print("⚠️ No welcomeLabel found in UI to display message.")

    def hide_welcome_message(self):
        """Hide the welcome message when user logs out."""
        if hasattr(self, "welcomeLabel"):
            self.welcomeLabel.clear()
            self.welcomeLabel.hide()

    def logout_action(self):
        """Handle user logout and reset login UI."""
        self.login_dialog.reset_fields()
        self.hide_welcome_message()  # ✅ hide welcome message on logout
        self.set_state(AppState.PART_SELECTION_SCREEN)
        print("User logged out.")
