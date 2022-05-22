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
import imagesize


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.central_widget = QWidget()
        self.grid = QGridLayout()
        self.scene_manager = DIContainer.scene_manager

        # Variables
        self.textureSize = 255

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

        self.top_layout.addWidget(self.loadImagesButton)
        self.top_layout.addWidget(self.imageCountLineEdit)
        self.top_buttons.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        # Image loading buttons
        self.defaultImageDirectory = 'C:\\Users\\serba\\Desktop\\train2017'
        self.loadImagesButton.clicked.connect(
            lambda x: self.load_images_in_scene(QFileDialog.getExistingDirectory(dir=self.defaultImageDirectory),
                                                self.scene_manager.image_count))

        self.imageCountLineEdit.setText(str(self.scene_manager.image_count))
        self.imageCountLineEdit.textChanged.connect(lambda x: self.scene_manager.set_image_count(int(self.imageCountLineEdit.text())))
        self.grid.addWidget(self.top_buttons)
        self.grid.addWidget(DIContainer.window_container)

    @profile
    def load_images_in_scene(self, directory: str, count: int):
        if not directory or directory == "":
            return

        DIContainer.scene.clear_scene()
        files = os.listdir(directory)

        DIContainer.plane_mesh = MeshBuilder.create_plane_mesh(width=1, height=1)

        self.scene_manager.image_count = count
        positions = self.scene_manager.calculate_positions(count)

        for i in range(0, count):
            path = files[i]
            ratio = 1

            if self.scene_manager.keep_aspect_ratios:
                full_path = os.path.join(directory, files[i])
                width, height = imagesize.get(full_path)
                ratio = width / height

            position = positions[i]
            rotation = QQuaternion.fromEulerAngles(90, 0, 0)
            scale = QVector3D(ratio, 1, 1)

            ObjectBuilder.create_textured_plane(position, rotation, scale, self.textureSize, image_path=path)

        DIContainer.scene.cameraController.center_camera()



