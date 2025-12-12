from PySide6.QtWidgets import QDialog
from PySide6.QtCore import Qt

class SplashScreen(QDialog):
    def __init__(self, parent=None):
        super(SplashScreen, self).__init__(parent)
        self.setWindowTitle("SnakeEditor")
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, True)
        self.show()