from PySide6.QtWidgets import QWidget, QGridLayout
from PySide6.QtCore import Qt
from GUI.LeftPanel.DirectoryWidget import DirectoryWidget
from GUI.LeftPanel.LoadingWidget import LoadingWidget
from GUI.LeftPanel.PostLoadWidget import PostLoadWidget
from GUI.LeftPanel.ImageDataWidget import ImageDataWidget
import DIContainer


class LeftPanel(QWidget):

    def __init__(self):
        super().__init__()
        self.directoryWidget = DirectoryWidget(self)
        self.loadingWidget = LoadingWidget()
        self.postLoadWidget = DIContainer.post_load_widget = PostLoadWidget()
        self.imageDataWidget = ImageDataWidget()

        # Layout setup
        self.setFixedSize(400, self.height())

        self.panelLayout = QGridLayout()
        self.panelLayout.setAlignment(Qt.AlignTop)
        self.panelLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.panelLayout)

        self.panelLayout.addWidget(self.directoryWidget)
        self.panelLayout.addWidget(self.loadingWidget)
        self.panelLayout.addWidget(self.postLoadWidget)
        self.panelLayout.addWidget(self.imageDataWidget)
        pass
