from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLineEdit, QFileDialog, QLabel, QCheckBox, QHBoxLayout
import DIContainer, os
from PySide6.QtCore import Qt
from Utilities import MiscFunctions


class PostLoadWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.image_searcher = DIContainer.image_searcher

        self.widgetLayout = QVBoxLayout()

        self.postLoadLabel = QLabel("Post-loading")
        self.startClassificationButton = QPushButton("Start classification")
        self.groupClustersButton = QPushButton("Group clusters")
        self.searchImageButton = QPushButton("Search image")
        self.setup()

    def setup(self):
        self.setLayout(self.widgetLayout)
        self.widgetLayout.addWidget(self.postLoadLabel)
        self.widgetLayout.addWidget(self.startClassificationButton)
        self.widgetLayout.addWidget(self.groupClustersButton)
        self.widgetLayout.addWidget(self.searchImageButton)

        self.postLoadLabel.setAlignment(Qt.AlignHCenter)
        self.startClassificationButton.setEnabled(False)
        self.groupClustersButton.setEnabled(False)
        self.searchImageButton.setEnabled(False)

        self.startClassificationButton.clicked.connect(
            lambda x: DIContainer.resources_manager.thread_start_classification(0))
        self.groupClustersButton.clicked.connect(lambda x: self.group_clustesr())
        self.searchImageButton.clicked.connect(
            lambda x: self.search_button_action(
                QFileDialog.getOpenFileName(self, dir=DIContainer.working_directory, caption='Select image',
                                            filter="JPEG (*.jpg *.jpeg)")[0]))

    def group_clustesr(self):
        DIContainer.scene_manager.group_clusters()
        self.enable_search_button(True)

    def search_button_action(self, path: str):
        if not path or path == "":
            return

        self.image_searcher.search_image(path)

    def enable_classification_button(self, value):
        self.startClassificationButton.setEnabled(value)

    def enable_group_clusters_button(self, value):
        self.groupClustersButton.setEnabled(value)

    def enable_search_button(self, value):
        self.searchImageButton.setEnabled(value)
