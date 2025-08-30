from src.actions.create_action import create_new_project
from src.actions.open_action import open_existing_project
from PyQt5.QtWidgets import (
    QTreeView, QFileSystemModel, QSizePolicy, QTextEdit, QLabel, QVBoxLayout, QWidget, QTabWidget,
    QTextBrowser, QTableWidget, QTableWidgetItem, QFileDialog, QMessageBox
)
from PyQt5.QtGui import QPixmap
import os

class AppManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.setup_connections()
        self._setup_buttons()

    def setup_connections(self):
        # Connect using the actual QAction objects from the UI
        if hasattr(self.main_window, 'actionNew_Project'):
            self.main_window.actionNew_Project.triggered.connect(self.handle_create_project)
        if hasattr(self.main_window, 'actionOpen'):
            self.main_window.actionOpen.triggered.connect(self.handle_open_project)

    def _setup_buttons(self):
        # Connect ExplorerButtonVMenu to toggle MenuContext
        if hasattr(self.main_window, 'ExplorerButtonVMenu'):
            self.main_window.ExplorerButtonVMenu.clicked.connect(self._toggle_menu_context)

    def handle_create_project(self):
        folder = self._get_folder_from_create()
        if folder:
            self._show_folder_tree(folder)

    def _get_folder_from_create(self):
        # Patch create_new_project to return the folder path
        from PyQt5.QtWidgets import QFileDialog, QMessageBox
        folder = QFileDialog.getExistingDirectory(self.main_window, 'Select Project Folder')
        if folder:
            import os
            for subfolder in ['Report', 'Folder A', 'Config', 'DRL', 'Test', 'Population']:
                os.makedirs(os.path.join(folder, subfolder), exist_ok=True)
            if hasattr(self.main_window, 'statusbar'):
                self.main_window.statusbar.showMessage(f'Project created at {folder}')
            QMessageBox.information(self.main_window, 'Success', f'Project created at {folder}')
            return folder
        return None

    def _show_folder_tree(self, folder):
        # Remove previous tree if exists
        if hasattr(self, 'tree_view') and self.tree_view:
            self.tree_view.setParent(None)
        from PyQt5.QtWidgets import QSizePolicy, QTextEdit, QLabel, QVBoxLayout, QWidget, QTabWidget
        self.tree_view = QTreeView(self.main_window)
        self.tree_model = QFileSystemModel()
        self.tree_model.setRootPath(folder)
        self.tree_view.setModel(self.tree_model)
        self.tree_view.setRootIndex(self.tree_model.index(folder))
        self.tree_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tree_view.setMinimumHeight(300)
        import os
        max_len = max((len(f) for f in os.listdir(folder)), default=20)
        self.tree_view.setColumnWidth(0, max(150, max_len * 10))
        # Hide all columns except file name
        for col in range(1, self.tree_model.columnCount()):
            self.tree_view.hideColumn(col)
        if hasattr(self.main_window, 'ContextlLabel'):
            self.main_window.ContextlLabel.setText('Explorer')
        self.main_window.MenuContext.addWidget(self.tree_view)

        # Add tab widget above editor area if not already added
        if not hasattr(self.main_window, 'editorTabWidget'):
            self.main_window.editorTabWidget = QTabWidget(self.main_window.centralwidget)
            self.main_window.editorTabWidget.setObjectName('editorTabWidget')
            self.main_window.editorTabWidget.setTabsClosable(True)
            self.main_window.editorTabWidget.tabCloseRequested.connect(self._close_tab)
            self.main_window.editorTabWidget.setMinimumHeight(400)
            self.main_window.centralwidget.layout().addWidget(self.main_window.editorTabWidget)

        # Connect tree view selection to editor
        self.tree_view.selectionModel().selectionChanged.connect(self._on_tree_selection)

    def _close_tab(self, index):
        self.main_window.editorTabWidget.removeTab(index)

    def _on_tree_selection(self, selected, deselected):
        from PyQt5.QtWidgets import QTextEdit, QLabel, QTextBrowser, QTableWidget, QTableWidgetItem
        import os
        indexes = selected.indexes()
        if not indexes:
            return
        index = indexes[0]
        file_path = self.tree_model.filePath(index)
        if os.path.isdir(file_path):
            return
        ext = os.path.splitext(file_path)[1].lower()
        # Check if file is already open in a tab
        tab_widget = self.main_window.editorTabWidget
        for i in range(tab_widget.count()):
            if tab_widget.tabText(i) == os.path.basename(file_path):
                tab_widget.setCurrentIndex(i)
                return
        if ext in ['.txt', '.py', '.md', '.csv', '.log']:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                # If .md or .html, use QTextBrowser for formatting
                if ext in ['.md', '.html']:
                    browser = QTextBrowser()
                    browser.setHtml(text)
                    tab_widget.addTab(browser, os.path.basename(file_path))
                    tab_widget.setCurrentWidget(browser)
                else:
                    editor = QTextEdit()
                    editor.setText(text)
                    editor.setReadOnly(True)
                    tab_widget.addTab(editor, os.path.basename(file_path))
                    tab_widget.setCurrentWidget(editor)
            except Exception as e:
                error_label = QLabel(f'Error loading file: {e}')
                tab_widget.addTab(error_label, os.path.basename(file_path))
                tab_widget.setCurrentWidget(error_label)
        elif ext in ['.png', '.jpg', '.jpeg', '.bmp', '.gif']:
            from PyQt5.QtGui import QPixmap
            image_label = QLabel()
            pixmap = QPixmap(file_path)
            image_label.setPixmap(pixmap.scaled(500, 400))
            tab_widget.addTab(image_label, os.path.basename(file_path))
            tab_widget.setCurrentWidget(image_label)
        elif ext in ['.xlsx', '.xls']:
            try:
                import pandas as pd
                df = pd.read_excel(file_path)
                table = QTableWidget()
                table.setRowCount(len(df.index))
                table.setColumnCount(len(df.columns))
                table.setHorizontalHeaderLabels([str(col) for col in df.columns])
                for i, row in enumerate(df.values):
                    for j, val in enumerate(row):
                        table.setItem(i, j, QTableWidgetItem(str(val)))
                tab_widget.addTab(table, os.path.basename(file_path))
                tab_widget.setCurrentWidget(table)
            except Exception as e:
                error_label = QLabel(f'Error loading Excel file: {e}')
                tab_widget.addTab(error_label, os.path.basename(file_path))
                tab_widget.setCurrentWidget(error_label)
        elif ext in ['.doc', '.docx']:
            try:
                import docx
                doc = docx.Document(file_path)
                html = ''
                for para in doc.paragraphs:
                    html += f'<p>{para.text}</p>'
                browser = QTextBrowser()
                browser.setHtml(html)
                tab_widget.addTab(browser, os.path.basename(file_path))
                tab_widget.setCurrentWidget(browser)
            except Exception as e:
                error_label = QLabel(f'Error loading Word file: {e}')
                tab_widget.addTab(error_label, os.path.basename(file_path))
                tab_widget.setCurrentWidget(error_label)
        else:
            info_label = QLabel('File type not supported for preview.')
            tab_widget.addTab(info_label, os.path.basename(file_path))
            tab_widget.setCurrentWidget(info_label)

    def _toggle_menu_context(self):
        # Toggle MenuContext layout visibility
        if hasattr(self.main_window, 'MenuContext'):
            any_hidden = False
            for i in range(self.main_window.MenuContext.count()):
                widget = self.main_window.MenuContext.itemAt(i).widget()
                if widget and not widget.isVisible():
                    any_hidden = True
            for i in range(self.main_window.MenuContext.count()):
                widget = self.main_window.MenuContext.itemAt(i).widget()
                if widget:
                    widget.setVisible(any_hidden)

    def handle_open_project(self):
        folder = self._get_folder_from_open()
        if folder:
            self._show_folder_tree(folder)

    def _get_folder_from_open(self):
        from PyQt5.QtWidgets import QFileDialog, QMessageBox
        folder = QFileDialog.getExistingDirectory(self.main_window, 'Select Existing Project Folder')
        if folder:
            if hasattr(self.main_window, 'statusbar'):
                self.main_window.statusbar.showMessage(f'Opened project at {folder}')
            QMessageBox.information(self.main_window, 'Open Project', f'Opened project at {folder}')
            return folder
        return None
