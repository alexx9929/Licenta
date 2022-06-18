from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLineEdit, QFileDialog, QLabel, QCheckBox, QHBoxLayout, \
    QGridLayout
import DIContainer, os
from PySide6.QtCore import Qt
from Utilities import MiscFunctions


class ImageDataWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.dataLabel = QLabel("Image data")
        self.widgetLayout = QVBoxLayout()
        self.dataLayout = QGridLayout()

        self.filenameLabel = QLabel("Name: ")
        self.filenameField = QLabel("Filename")

        self.setup()
        pass

    def setup(self):
        self.widgetLayout.addWidget(self.dataLabel)
        self.widgetLayout.addLayout(self.dataLayout)
        self.setLayout(self.widgetLayout)

        self.dataLabel.setAlignment(Qt.AlignHCenter)

        self.dataLayout.addWidget(self.filenameLabel, 0, 0)
        self.dataLayout.addWidget(self.filenameField, 0, 1)
