from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel,QGridLayout
import DIContainer, os
from PySide6.QtCore import Qt
from GUI.LeftPanel.MapWidget import MapWidget
from Utilities import ImagesUtilities


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
        self.altitudeLabel = QLabel("Altitude: ")
        self.altitudeField = QLabel()

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
        self.dataLayout.addWidget(self.altitudeLabel, 2, 0)
        self.dataLayout.addWidget(self.altitudeField, 2, 1)
        self.dataLayout.addWidget(self.mapWidget, 3, 0, 1, 2)

        self.setLayout(self.widgetLayout)
        self.mapWidget.setMinimumHeight(400)

    def set_data(self, obj):
        info = ImagesUtilities.get_info_from_object(obj)
        self.filenameField.setText(info['Name'])
        self.load_coordinates(info)
        self.load_dateTime(info)

    def load_coordinates(self, info):
        if info.keys().__contains__('N') and info.keys().__contains__('E'):
            DIContainer.map_widget.new_map(info['N'], info['E'])
        else:
            DIContainer.map_widget.reset_map()

        if info.keys().__contains__('Altitude'):
            self.altitudeField.setText(info['Altitude'])
        else:
            self.altitudeField.setText("")

    def load_dateTime(self, info):
        if info.keys().__contains__('Date') and info.keys().__contains__('Time'):
            self.createdField.setText(info['Date'] + "  " + info['Time'])
            return

        if info.keys().__contains__('Date') and not info.keys().__contains__('Time'):
            self.createdField.setText(info['Date'])
        else:
            if not info.keys().__contains__('Date') and info.keys().__contains__('Time'):
                self.createdField.setText(info['Time'])
            else:
                self.createdField.setText("")

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

        new_string = north_string + "+" + east_string
        return new_string
