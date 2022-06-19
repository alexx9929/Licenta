from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLineEdit, QFileDialog, QLabel, QCheckBox, QHBoxLayout, \
    QGridLayout
import DIContainer, os
from PySide6.QtCore import Qt
from Utilities import MiscFunctions
from GUI.LeftPanel.MapWidget import MapWidget


class ImageDataWidget(QWidget):

    def __init__(self):
        super().__init__()
        DIContainer.image_data_widget = self
        self.dataLabel = QLabel("Image data")
        self.widgetLayout = QVBoxLayout()
        self.dataLayout = QGridLayout()
        self.mapWidget = MapWidget()

        self.filenameLabel = QLabel("Name: ")
        self.filenameField = QLabel()
        self.createdLabel = QLabel("Created on: ")
        self.createdField = QLabel()

        self.setup()
        pass

    def setup(self):
        self.widgetLayout.addWidget(self.dataLabel)
        self.widgetLayout.addLayout(self.dataLayout)
        self.setLayout(self.widgetLayout)

        self.dataLabel.setAlignment(Qt.AlignHCenter)

        self.dataLayout.addWidget(self.filenameLabel, 0, 0)
        self.dataLayout.addWidget(self.filenameField, 0, 1)
        self.dataLayout.addWidget(self.mapWidget, 1, 0, 1, 2)
        self.dataLayout.addWidget(self.createdLabel, 2, 0)
        self.dataLayout.addWidget(self.createdField, 2, 1)

        #self.mapWidget.setSizePolicy(Qt.PreferredSize)
      #  self.mapWidget.setFixedHeight(1000)

    def set_data(self, obj):
        texture_image = obj.get_texture_image()
        self.filenameField.setText(texture_image.filename)
