import os
from PyQt5.QtWidgets import QFileDialog, QMessageBox

def create_new_project(parent=None):
    folder = QFileDialog.getExistingDirectory(parent, 'Select Project Folder')
    if folder:
        try:
            for subfolder in ['Report', 'Folder A', 'Config', 'DRL', 'Test', 'Population']:
                os.makedirs(os.path.join(folder, subfolder), exist_ok=True)
            # Example: update UI element if needed
            if hasattr(parent, 'statusbar'):
                parent.statusbar.showMessage(f'Project created at {folder}')
            QMessageBox.information(parent, 'Success', f'Project created at {folder}')
        except Exception as e:
            QMessageBox.critical(parent, 'Error', str(e))
