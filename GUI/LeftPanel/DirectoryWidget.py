from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLineEdit, QFileDialog, QLabel, QCheckBox
import DIContainer, os
from PySide6.QtCore import Qt


class DirectoryWidget(QWidget):

    def __init__(self):
        super().__init__()
        # Elements
        self.datasetFolderLabel = QLabel("Dataset directory")
        self.pathLineEdit = QLineEdit(DIContainer.defaultImageDirectory)
        self.browseButton = QPushButton("Browse")

        # Styling
        self.datasetFolderLabel.setAlignment(Qt.AlignHCenter)

        # Finishing layout
        self.widgetLayout = QVBoxLayout()
        self.widgetLayout.addWidget(self.datasetFolderLabel)
        self.widgetLayout.addWidget(self.pathLineEdit)
        self.widgetLayout.addWidget(self.browseButton)
        self.setLayout(self.widgetLayout)
