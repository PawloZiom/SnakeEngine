import sys
from ui.splash import SplashScreen
from ui.projects import SelectProjectWindow
from PySide6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    splash = SplashScreen()
    projects = SelectProjectWindow()
    sys.exit(app.exec())