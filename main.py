import subprocess
import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow
from src.app.app_manager import AppManager

UI_FILE = 'src/designer/UI/docueditor.ui'
PY_UI_FILE = 'src/designer/PY/doceditor_ui.py'

# Convert .ui to .py if not already converted
subprocess.run(f"pyuic5 {UI_FILE} -o {PY_UI_FILE}")

from src.designer.PY.doceditor_ui import Ui_MainWindow

class DocEditor(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # self.ui = Ui_MainWindow()
        self.setupUi(self)
        self.app_manager = AppManager(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DocEditor()
    window.show()
    sys.exit(app.exec_())
