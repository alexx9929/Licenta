from PySide6.QtWidgets import QWidget, QGridLayout
from PySide6.QtCore import Qt
from GUI.LeftPanel.DirectoryWidget import DirectoryWidget
from GUI.LeftPanel.LoadingWidget import LoadingWidget


class LeftPanel(QWidget):

    def __init__(self):
        super().__init__()
        self.directoryWidget = DirectoryWidget(self)
        self.loadingWidget = LoadingWidget()

        # Layout setup
        self.setFixedSize(200, self.height())

        self.panelLayout = QGridLayout()
        self.panelLayout.setAlignment(Qt.AlignTop)
        self.panelLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.panelLayout)

        self.panelLayout.addWidget(self.directoryWidget)
        self.panelLayout.addWidget(self.loadingWidget)
        pass
