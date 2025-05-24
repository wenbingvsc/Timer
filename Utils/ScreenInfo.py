from PySide6.QtGui import QScreen
from PySide6.QtWidgets import QApplication


class Screen:
    """屏幕信息类"""

    def __init__(self):
        self.screens: list[QScreen] = []
        self.primeryScreen: QScreen = None

    def getScreenInfo(self, app: QApplication):
        """获取屏幕信息"""
        self.screens.clear()
        for screen in app.screens():
            self.screens.append(screen)
        self.primeryScreen = app.primaryScreen()
