import PIL.Image
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLineEdit, QFileDialog, QLabel, QCheckBox, QHBoxLayout, \
    QGridLayout
import DIContainer, os
from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QPen, QPainter, QColor
from Utilities import MiscFunctions
from GUI.LeftPanel.MapWidget import MapWidget
from PIL import Image
import PIL.ExifTags


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

        self.dataLabel.setAlignment(Qt.AlignHCenter)

        self.dataLayout.addWidget(self.filenameLabel, 0, 0)
        self.dataLayout.addWidget(self.filenameField, 0, 1)
        self.dataLayout.addWidget(self.createdLabel, 1, 0)
        self.dataLayout.addWidget(self.createdField, 1, 1)
        self.dataLayout.addWidget(self.mapWidget, 2, 0, 1, 2)

        self.setLayout(self.widgetLayout)
        self.mapWidget.setMinimumHeight(400)

    def set_data(self, obj):
        texture_image = obj.get_texture_image()
        img = PIL.Image.open(texture_image.get_full_path())

        exif_data = {
            PIL.ExifTags.TAGS[key]: value
            for key, value in img._getexif().items()
            if key in PIL.ExifTags.TAGS
        }

        print(self.format_gps_coordinates(str(exif_data['GPSInfo'][2]), str(exif_data['GPSInfo'][4])))
        self.filenameField.setText(texture_image.filename)

    def format_gps_coordinates(self, north: str, east: str):
        split = north[1:-1].split(",")
        degrees = split[0].split(".")[0]
        minutes = split[1].split(".")[0]
        seconds = split[2].split(".")[0]

        north_string = degrees + "°" + minutes + "\'" + seconds + "\"" + "N"
        north_string = north_string.replace(" ", "")

        split = east[1:-1].split(",")
        degrees = split[0].split(".")[0]
        minutes = split[1].split(".")[0]
        seconds = split[2].split(".")[0]
        east_string = degrees + "°" + minutes + "\'" + seconds + "\"" + "E"
        east_string = east_string.replace(" ", "")

        new_string = north_string + " " + east_string
        return new_string
