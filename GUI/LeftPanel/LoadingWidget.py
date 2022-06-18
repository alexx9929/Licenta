from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLineEdit, QFileDialog, QLabel, QCheckBox, QHBoxLayout
import DIContainer, os
from PySide6.QtCore import Qt
from Utilities import MiscFunctions
from ObjectBuilding.Visuals import MeshBuilder
from PySide6.QtGui import QIntValidator, QPalette


class LoadingWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.scene_manager = DIContainer.scene_manager
        self.resources_manager = DIContainer.resources_manager

        # Elements
        self.countLabel = QLabel("Image count")
        self.imageCountLineEdit = QLineEdit()
        self.allImagesToggle = QCheckBox("All")
        self.loadImagesButton = QPushButton("Load images")
        self.errorLabel = QLabel("Invalid image count")

        self.errorPallete = QPalette()

        self.widgetLayout = QVBoxLayout()
        self.countLayout = QHBoxLayout()
        self.validator = QIntValidator(10, DIContainer.max_dataset_length)

        self.setup()

    def setup(self):
        self.widgetLayout.addWidget(self.countLabel)
        self.countLayout.addWidget(self.imageCountLineEdit)
        self.countLayout.addWidget(self.allImagesToggle)

        self.widgetLayout.addLayout(self.countLayout)
        self.widgetLayout.addWidget(self.loadImagesButton)
        self.widgetLayout.addWidget(self.errorLabel)

        self.errorPallete.setColor(QPalette.WindowText, Qt.red)

        self.errorLabel.setPalette(self.errorPallete)
        self.errorLabel.hide()
        self.setLayout(self.widgetLayout)

        self.validator.setBottom(10)
        self.imageCountLineEdit.setValidator(self.validator)

        #self.countLabel.setAlignment(Qt.AlignHCenter)
        self.setup_actions()

    def update_validator(self):
        self.validator.setTop(DIContainer.max_dataset_length)

    def setup_actions(self):
        self.allImagesToggle.clicked.connect(
            lambda x: self.imageCountLineEdit.setEnabled(not self.allImagesToggle.isChecked()))

        self.loadImagesButton.clicked.connect(lambda x: self.start_loading_images_in_scene())
        self.imageCountLineEdit.setText(str(10))

    def start_loading_images_in_scene(self):
        count = DIContainer.max_dataset_length if self.allImagesToggle.isChecked() else int(
            self.imageCountLineEdit.text())

        if count > DIContainer.max_dataset_length:
            self.errorLabel.show()
            return
        else:
            self.errorLabel.hide()

        directory = DIContainer.working_directory
        DIContainer.scene.clear_scene()
        DIContainer.default_mesh = MeshBuilder.create_plane_mesh()

        self.scene_manager.image_count = count
        positions = self.scene_manager.calculate_all_positions(count)
        files = os.listdir(directory)
        self.resources_manager.load_images_in_scene(count, directory, files, positions, DIContainer.texture_size)

        # self.image_searcher.start_classification(True)
        # self.scene_manager.group_clusters()
