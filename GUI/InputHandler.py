import PySide6
import DIContainer
from PySide6.QtCore import QEvent, QObject


class Listener(QObject):
    def __init__(self):
        super().__init__()
        pass

    def eventFilter(self, watched: PySide6.QtCore.QObject, event: PySide6.QtCore.QEvent):
        if event.type() == QEvent.MouseButtonPress or event.type() == QEvent.Wheel or event.type() == event.MouseMove:
            event.ignore()
            return True
        else:
            return QObject.eventFilter(self, watched, event)


class InputHandler:
    def __init__(self):
        self.app = DIContainer.app
        self.mouse_blocker = Listener()

    def block_mouse_input(self):
        self.app.installEventFilter(self.mouse_blocker)

    def unblock_mouse_input(self):
        self.app.removeEventFilter(self.mouse_blocker)
