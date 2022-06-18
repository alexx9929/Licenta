from PySide6.QtWidgets import QWidget, QPushButton, QGridLayout, QLineEdit, QFileDialog
import DIContainer, os
from ObjectBuilding.Visuals import MeshBuilder


class LeftPanel(QWidget):

    def __init__(self):
        super().__init__()
        self.scene_manager = DIContainer.scene_manager
        self.image_searcher = DIContainer.image_searcher
        self.resources_manager = DIContainer.resources_manager

        self.loadImagesButton = QPushButton("Load images")
        self.imageCountLineEdit = QLineEdit()
        self.searchImageButton = QPushButton("Search image")

        self.setFixedSize(200, self.height())

        self.leftPanelLayout = QGridLayout()
        self.setLayout(self.leftPanelLayout)

        self.leftPanelLayout.addWidget(self.loadImagesButton)
        self.leftPanelLayout.addWidget(self.imageCountLineEdit)
        self.leftPanelLayout.addWidget(self.searchImageButton)

        # Actions
        self.loadImagesButton.clicked.connect(
            lambda x: self.start_loading_images_in_scene(
                QFileDialog.getExistingDirectory(dir=DIContainer.defaultImageDirectory),
                self.scene_manager.image_count))

        self.imageCountLineEdit.setText(str(self.scene_manager.image_count))
        self.imageCountLineEdit.textChanged.connect(
            lambda x: self.scene_manager.set_image_count(int(self.imageCountLineEdit.text())))
        self.searchImageButton.clicked.connect(
            lambda x: self.search_button_action(
                QFileDialog.getOpenFileName(self, dir=DIContainer.defaultImageDirectory, caption='Select image',
                                            filter="JPEG (*.jpg *.jpeg)")[0]))
        pass

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

        self.resources_manager.load_images_in_scene(count, directory, files, positions, DIContainer.texture_size)

        # self.image_searcher.start_classification(True)
        # self.scene_manager.group_clusters()
