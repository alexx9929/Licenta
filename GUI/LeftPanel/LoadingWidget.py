from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLineEdit, QFileDialog, QLabel, QCheckBox, QHBoxLayout
import DIContainer, os
from PySide6.QtCore import Qt
from Utilities import MiscFunctions
from ObjectBuilding.Visuals import MeshBuilder
from PySide6.QtGui import QIntValidator


class LoadingWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.scene_manager = DIContainer.scene_manager
        self.image_searcher = DIContainer.image_searcher
        self.resources_manager = DIContainer.resources_manager

        # Elements
        self.countLabel = QLabel("Image count")
        self.imageCountLineEdit = QLineEdit()
        self.allImagesToggle = QCheckBox("All")
        self.loadImagesButton = QPushButton("Load images")
        self.searchImageButton = QPushButton("Search image")

        self.widgetLayout = QVBoxLayout()
        self.widgetLayout.addWidget(self.countLabel)

        self.countLayout = QHBoxLayout()
        self.countLayout.addWidget(self.imageCountLineEdit)
        self.countLayout.addWidget(self.allImagesToggle)

        self.widgetLayout.addLayout(self.countLayout)
        self.widgetLayout.addWidget(self.loadImagesButton)
        self.widgetLayout.addWidget(self.searchImageButton)
        self.setLayout(self.widgetLayout)

        self.validator = QIntValidator(10, DIContainer.max_dataset_length)
        self.validator.setBottom(10)
        self.imageCountLineEdit.setValidator(self.validator)

        self.setup_actions()

    def update_validator(self):
        self.validator.setTop(DIContainer.max_dataset_length)
        print(DIContainer.max_dataset_length)

    def setup_actions(self):
        self.allImagesToggle.clicked.connect(
            lambda x: self.imageCountLineEdit.setEnabled(not self.allImagesToggle.isChecked()))

        self.loadImagesButton.clicked.connect(
            lambda x: self.start_loading_images_in_scene(
                QFileDialog.getExistingDirectory(dir=DIContainer.working_directory),
                self.scene_manager.image_count))

        self.imageCountLineEdit.setText(str(self.scene_manager.image_count))
        self.searchImageButton.clicked.connect(
            lambda x: self.search_button_action(
                QFileDialog.getOpenFileName(self, dir=DIContainer.working_directory, caption='Select image',
                                            filter="JPEG (*.jpg *.jpeg)")[0]))

    def search_button_action(self, path: str):
        if not path or path == "":
            return

        self.image_searcher.search_image(path)

    def start_loading_images_in_scene(self, directory: str, count: int):
        if not directory or directory == "":
            return

        DIContainer.scene.clear_scene()
        DIContainer.default_mesh = MeshBuilder.create_plane_mesh()

        self.scene_manager.image_count = count
        positions = self.scene_manager.calculate_all_positions(count)
        files = os.listdir(directory)
        self.resources_manager.load_images_in_scene(count, directory, files, positions, DIContainer.texture_size)

        # self.image_searcher.start_classification(True)
        # self.scene_manager.group_clusters()
