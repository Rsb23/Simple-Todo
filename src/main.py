import sys
from datetime import datetime

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QCheckBox

from database_parser import DataManagement


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setupAttributes()
        self.setupUI()

    def setupAttributes(self):
        self.setWindowTitle("ToDo App")
        self.resize(500, 400)

    def setupUI(self):
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        self.main_layout = QHBoxLayout()
        self.main_widget.setLayout(self.main_layout)

        # left sidebar setup
        self.left_sidebar_layout = QVBoxLayout()

        # left sidebar widget(s)
        self.left_sidebar_settings_btn = QPushButton()

        # left sidebar widget(s) -> left sidebar layout
        self.left_sidebar_layout.addStretch(1)
        self.left_sidebar_layout.addWidget(self.left_sidebar_settings_btn)

        # right setup
        self.right_layout = QVBoxLayout()

        # right widgets
        self.list_widget = QListWidget()

        self.main_layout.addLayout(self.left_sidebar_layout)


class TaskItem(QWidget):
    def __init__(self):
        super().__init__()

    def setupAttributes(self):
        pass

    def setupUI(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
    
