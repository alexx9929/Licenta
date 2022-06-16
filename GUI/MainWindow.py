import DIContainer, os, sys, math, ImageSearcher
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import QRect, QSize, Qt, QObject
from ObjectBuilding.Visuals import MeshBuilder
from ResourcesManagement.ResourcesManager import ResourcesManager
from threading import Thread
import time
from time import perf_counter
import queue


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.central_widget = QWidget()
        self.grid = QGridLayout()
        self.scene_manager = DIContainer.scene_manager
        self.image_searcher = DIContainer.image_searcher
        self.resources_manager = DIContainer.resources_manager

        self.texture_size = 255

        # Setup
        self.central_widget.setLayout(self.grid)
        self.setCentralWidget(self.central_widget)
        self.setGeometry(QRect(0, 0, 2533, 1336))

        # Multithreading
        self.clicked_object = None
        self.double_click_delay = 0.4
        self.events_thread = Thread(target=self.click_check)
        self.events_thread.start()

        # Top buttons
        self.top_buttons = QWidget(self)
        self.top_layout = QVBoxLayout()
        self.top_buttons.setLayout(self.top_layout)

        self.loadImagesButton = QPushButton("Load images")
        self.loadSingleImageButton = QPushButton("Load single image")
        self.imageCountLineEdit = QLineEdit()
        self.searchImageButton = QPushButton("Search image")

        # Adding buttons to layout
        self.top_layout.addWidget(self.loadImagesButton)
        self.top_layout.addWidget(self.imageCountLineEdit)
        self.top_layout.addWidget(self.searchImageButton)
        self.top_buttons.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        # Buttons actions
        #self.defaultImageDirectory = 'C:\\Users\\serba\\Desktop\\train2017'
        self.defaultImageDirectory = 'C:\\Users\\serba\\Desktop\\Thermal'
        self.loadImagesButton.clicked.connect(
            lambda x: self.start_loading_images_in_scene(
                QFileDialog.getExistingDirectory(dir=self.defaultImageDirectory),
                self.scene_manager.image_count))

        self.imageCountLineEdit.setText(str(self.scene_manager.image_count))
        self.imageCountLineEdit.textChanged.connect(
            lambda x: self.scene_manager.set_image_count(int(self.imageCountLineEdit.text())))
        self.searchImageButton.clicked.connect(
            lambda x: self.search_button_action(
                QFileDialog.getOpenFileName(self, dir=self.defaultImageDirectory, caption='Select image',
                                            filter="JPEG (*.jpg *.jpeg)")[0]))

        self.grid.addWidget(self.top_buttons)
        self.grid.addWidget(DIContainer.window_container)

    # TODO: move to check to app's event filter to remove the need for a new thread
    def click_check(self):
        while True:
            if self.clicked_object:
                time.sleep(self.double_click_delay)
                self.clicked_object = None
            else:
                time.sleep(0)

    def search_button_action(self, path: str):
        if not path or path == "":
            return

        self.image_searcher.search_image(path)

    def start_loading_images_in_scene(self, directory: str, count: int):
        if not directory or directory == "":
            return

        DIContainer.scene.clear_scene()
        files = os.listdir(directory)

        DIContainer.default_mesh = MeshBuilder.create_plane_mesh()

        self.scene_manager.image_count = count
        positions = self.scene_manager.calculate_all_positions(count)

        self.resources_manager.load_images_in_scene(count, directory, files, positions, self.texture_size)

        # self.image_searcher.start_classification(True)
        # self.scene_manager.group_clusters()

        # Centering camera
        # DIContainer.scene.cameraController.center_camera()
