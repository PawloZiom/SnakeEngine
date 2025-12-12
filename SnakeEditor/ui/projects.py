from PySide6.QtWidgets import QMainWindow, QMenuBar, QApplication
from PySide6.QtCore import QRect


class SelectProjectWindow(QMainWindow):
    def __init__(self, parent=None):
        super(SelectProjectWindow, self).__init__(parent)
        self.setWindowTitle("Snake Editor")
        self.setGeometry(QRect(0, 0, 1280, 720))

        screen = QApplication.primaryScreen()
        if screen:
            screen_geo = screen.availableGeometry()
            win_geo = self.frameGeometry()
            win_geo.moveCenter(screen_geo.center())
            self.move(win_geo.topLeft())

        menubar = QMenuBar(self)
        self.setMenuBar(menubar)

        file_menu = menubar.addMenu("File")
        edit_menu = menubar.addMenu("Edit")
        view_menu = menubar.addMenu("View")
        
        self.show()