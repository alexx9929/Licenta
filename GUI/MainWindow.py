import cmath

import DIContainer, os, sys, math
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import QRect, QSize, Qt
from ObjectBuilding.GameObject import GameObject
from ObjectBuilding.Visuals import MeshBuilder
from time import perf_counter
from ResourcesManagement.ResourcesManager import ResourcesManager
from ObjectBuilding.ObjectBuilder import ObjectBuilder
from Utilities import MiscFunctions
from memory_profiler import profile
from pympler import asizeof
import numpy as np
from enum import Enum


class Distribution(Enum):
    planar = 1
    normal = 2


class FloatingButtonWidget(QPushButton):  # 1

    def __init__(self, parent):
        super().__init__(parent)
        self.paddingLeft = 5
        self.paddingTop = 5

    def update_position(self):
        if hasattr(self.parent(), 'viewport'):
            parent_rect = self.parent().viewport().rect()
        else:
            parent_rect = self.parent().rect()

        if not parent_rect:
            return

        x = parent_rect.width() - self.width() - self.paddingLeft
        y = self.paddingTop  # 3
        self.setGeometry(x, y, self.width(), self.height())

    def resizeEvent(self, event):  # 2
        super().resizeEvent(event)
        self.update_position()

    def mousePressEvent(self, event):  # 4
        self.parent().floatingButtonClicked.emit()


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.central_widget = QWidget()
        self.grid = QGridLayout()

        # Variables
        self.imageOffset = 0.1
        self.imagesPerRow = 10
        self.textureSize = 255
        self.imageCount = 100
        self.planeSize = GameObject.__DEFAULT__PLANE_LENGTH__()

        # Setup
        self.central_widget.setLayout(self.grid)
        self.setCentralWidget(self.central_widget)

        # self.showMaximized()
        self.setMinimumWidth(2560)
        self.setMinimumHeight(1336)

        # Top buttons
        self.top_buttons = QWidget(self)
        self.top_layout = QVBoxLayout()
        self.top_buttons.setLayout(self.top_layout)

        self.loadImagesButton = QPushButton("Load images")
        self.loadSingleImageButton = QPushButton("Load single image")
        self.imageCountLineEdit = QLineEdit()

        # self.top_layout.addWidget(self.loadSingleImageButton)
        self.top_layout.addWidget(self.loadImagesButton)
        self.top_layout.addWidget(self.imageCountLineEdit)
        self.top_buttons.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        # Image loading buttons
        self.defaultImageDirectory = 'C:\\Users\\serba\\Desktop\\train2017'
        # self.defaultImageDirectory = 'C:\\Users\\serba\\Desktop\\Sample images'
        self.loadImagesButton.clicked.connect(
            lambda x: self.load_images_in_scene(QFileDialog.getExistingDirectory(dir=self.defaultImageDirectory),
                                                self.get_image_count()))
        # self.loadSingleImageButton.clicked.connect(
        #     lambda x: self.load_image_in_scene(QFileDialog.selectedFiles(dir=self.defaultImageDirectory)[0]))

        self.imageCountLineEdit.setText(str(self.imageCount))
        self.imageCountLineEdit.textChanged.connect(lambda x: self.set_image_count(int(self.imageCountLineEdit.text())))
        self.grid.addWidget(self.top_buttons)
        self.grid.addWidget(DIContainer.window_container)

        # Gaussian distribution
        self.image_distribution = Distribution.normal
        self.normal_mean = [0, 0, 0]
        self.normal_deviation = [30, 20, 20]

    def get_image_count(self):
        return self.imageCount

    def set_image_count(self, count: int):
        self.imageCount = count

    #@profile
    def load_images_in_scene(self, directory: str, count: int):
        if not directory or directory == "":
            return

        DIContainer.scene.clear_scene()
        DIContainer.plane_mesh = MeshBuilder.create_plane_mesh(width=1, height=1)
        files = os.listdir(directory)

        self.imageCount = count
        self.imagesPerRow = int(math.sqrt(count))
        positions = []

        square_root = math.sqrt(self.imageCount)
        self.normal_deviation[0] = square_root * 0.25
        self.normal_deviation[1] = square_root * 0.5
        self.normal_deviation[2] = square_root * 0.25

        if self.image_distribution == Distribution.normal:
            positions = (np.random.normal(self.normal_mean[0], self.normal_deviation[0], count),
                         np.random.normal(self.normal_mean[1], self.normal_deviation[1], count),
                         np.random.normal(self.normal_mean[2], self.normal_deviation[2], count))

        for i in range(0, count):
            path = files[i]

            current_row = int(i / self.imagesPerRow)
            current_col = i % self.imagesPerRow

            if self.image_distribution == Distribution.planar:
                x_pos = float(current_col * (self.planeSize + self.imageOffset))
                y_pos = float(-current_row * (self.planeSize + self.imageOffset))
                z_pos = 0

                position = QVector3D(x_pos, y_pos, z_pos)

            if self.image_distribution == Distribution.normal:
                position = QVector3D(positions[0][i], positions[1][i], positions[2][i])

            rotation = QQuaternion.fromEulerAngles(90, 0, 0)
            scale = QVector3D(1, 1, 1)

            ObjectBuilder.create_textured_plane(position, rotation, scale, self.textureSize, image_path=path)
        self.center_camera()

    def center_camera(self):
        if self.image_distribution == Distribution.planar:
            plane_size = GameObject.__DEFAULT__PLANE_LENGTH__()
            x_multiplier = (self.imagesPerRow / 2) if self.imageCount >= self.imagesPerRow else self.imageCount / 2
            y_multiplier = -(self.imageCount / self.imagesPerRow) / 2

            if self.imagesPerRow % 2 != 0:
                x_multiplier -= 0.5

            if (self.imagesPerRow * self.imagesPerRow) % 2 != 0:
                y_multiplier += 0.5

            x_pos = (plane_size + self.imageOffset) * x_multiplier
            y_pos = (plane_size + self.imageOffset) * y_multiplier
            DIContainer.scene.cameraHolder.set_position(x_pos, y_pos, 10)

        if self.image_distribution == Distribution.normal:
            z_pos = self.normal_deviation[2] * 2
            print("D: " + str(self.normal_deviation[2])[:3] + " Z: " + str(z_pos)[:3])
            DIContainer.scene.cameraHolder.set_position(0, 0, z_pos)

