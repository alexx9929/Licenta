import DIContainer
from PySide6.QtWidgets import *
from PySide6.QtCore import QRect, Qt
from threading import Thread
import time
from GUI.LeftPanel.LeftPanel import LeftPanel


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.central_widget = QWidget()
        self.boxLayout = QHBoxLayout()
        self.scene_manager = DIContainer.scene_manager
        self.image_searcher = DIContainer.image_searcher
        self.resources_manager = DIContainer.resources_manager

        # Setup
        self.central_widget.setLayout(self.boxLayout)
        self.setCentralWidget(self.central_widget)
        self.setGeometry(QRect(0, 0, 1266, 1336))

        # Multithreading
        self.clicked_object = None
        self.double_click_delay = 0.4
        self.events_thread = Thread(target=self.click_check)
        self.events_thread.start()

        # Widgets
        self.container = DIContainer.window_container
        self.leftPanel = LeftPanel()

        # Layout setup
        self.boxLayout.setSpacing(0)
        self.boxLayout.setContentsMargins(0, 0, 0, 0)
        self.boxLayout.addWidget(self.leftPanel)
        self.boxLayout.addWidget(self.container)
        self.boxLayout.setAlignment(self.leftPanel, Qt.AlignTop)

    # TODO: move to check to app's event filter to remove the need for a new thread
    def click_check(self):
        while True:
            if self.clicked_object:
                time.sleep(self.double_click_delay)
                self.clicked_object = None
            else:
                time.sleep(0)
