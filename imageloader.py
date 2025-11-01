# image_loader.py
import os
from PyQt6.QtGui import QIcon

def load_images_for_buttons(buttons, image_files):
    """
    Assign images to given buttons.
    
    :param buttons: List of QPushButton objects
    :param image_files: List of image file paths corresponding to buttons
    """
    for i, button in enumerate(buttons):
        if i >= len(image_files):
            break  # No more images
        image_name = image_files[i]
        if button and os.path.exists(image_name):
            icon = QIcon(image_name)
            button.setIcon(icon)
            button.setIconSize(button.size())
            button.setText(f"Part {i+1}")
        elif button:
            button.setText(f"Part {i+1} (no image)")
