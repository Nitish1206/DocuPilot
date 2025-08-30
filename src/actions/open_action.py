from PyQt5.QtWidgets import QFileDialog, QMessageBox

def open_existing_project(parent=None):
    folder = QFileDialog.getExistingDirectory(parent, 'Select Existing Project Folder')
    if folder:
        # Example: update UI element if needed
        if hasattr(parent, 'statusbar'):
            parent.statusbar.showMessage(f'Opened project at {folder}')
        QMessageBox.information(parent, 'Open Project', f'Opened project at {folder}')
