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
import numpy as np
from ResourcesManagement.SceneManager import SceneManager, Distribution


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.central_widget = QWidget()
        self.grid = QGridLayout()
        self.scene_manager = DIContainer.scene_manager

        # Variables
        self.textureSize = 255
        self.imageCount = 100

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
        self.loadImagesButton.clicked.connect(
            lambda x: self.load_images_in_scene(QFileDialog.getExistingDirectory(dir=self.defaultImageDirectory),
                                                self.get_image_count()))

        self.imageCountLineEdit.setText(str(self.imageCount))
        self.imageCountLineEdit.textChanged.connect(lambda x: self.set_image_count(int(self.imageCountLineEdit.text())))
        self.grid.addWidget(self.top_buttons)
        self.grid.addWidget(DIContainer.window_container)

    def get_image_count(self):
        return self.imageCount

    def set_image_count(self, count: int):
        self.imageCount = count

    #@profile
    def load_images_in_scene(self, directory: str, count: int):
        if not directory or directory == "":
            return

        DIContainer.scene.clear_scene()
        files = os.listdir(directory)

        ratios = {}
        keep_aspect_ratios = self.scene_manager.keep_aspect_ratios
        if keep_aspect_ratios:
            ratios = ResourcesManager.get_ratios(directory, files, count)
        else:
            DIContainer.plane_mesh = MeshBuilder.create_plane_mesh(width=1, height=1)

        # print(len(self.ratios.keys()))
        # sortedRatios = sorted(self.ratios.keys())
        # for i in sortedRatios:
        #     print("Ratio: " + i + " Count: " + str(self.ratios[i]))

        self.imageCount = count
        positions = self.scene_manager.calculate_positions(count)

        for i in range(0, count):
            path = files[i]
            position = positions[i]
            rotation = QQuaternion.fromEulerAngles(90, 0, 0)
            scale = QVector3D(1, 1, 1)

            ObjectBuilder.create_textured_plane(position, rotation, scale, self.textureSize, image_path=path)
        #self.center_camera()

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

