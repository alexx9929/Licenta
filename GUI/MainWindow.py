from PySide6.QtWidgets import *
from ObjectBuilding.GameObject import GameObject
import DIContainer, os
from time import perf_counter


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.central_widget = QWidget()
        self.layout = QVBoxLayout()

        # Variables
        self.imageOffset = 1
        self.imagesPerRow = 10
        self.textureSize = 512
        self.imageCount = 100
        self.planeSize = GameObject.__DEFAULT__PLANE_LENGTH__()

        # Setup
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.setMinimumWidth(2560)
        self.setMinimumHeight(1336)

        self.loadImagesButton = QPushButton("Load images")
        #self.loadImagesButton.clicked.connect(lambda x: self.load_images())
        self.central_widget.layout().addWidget(self.loadImagesButton)

    # def load_images(self):
    #     image_directory = QFileDialog().getExistingDirectory()
    #     files = os.listdir(image_directory)
    #
    #     for i in range(0, self.imageCount):
    #         t1 = perf_counter()
    #         currentRow = int(i / self.imagesPerRow)
    #         currentCol = i % self.imagesPerRow
    #
    #         path = os.path.join(image_directory, files[i])
    #         e = GameObject()
    #         e.add_mesh(MeshBuilder.create_plane_mesh())
    #
    #         t11 = perf_counter()
    #         e.add_material(TextureMaterial.TextureMaterial(path, self.textureSize, self.textureSize))
    #         t12 = perf_counter()
    #         textureCreationTime.append(t12 - t11)
    #
    #         e.transform.setTranslation(
    #             QVector3D(currentCol * (self.planeSize + self.imageOffset),
    #                       -currentRow * (self.planeSize + self.imageOffset),
    #                       0))
    #         e.transform.setRotationX(90)
    #         DIContainer.scene.objects.append(e)
    #         t2 = perf_counter()
    #         objectsCreationTime.append(t2 - t1)

    def resizeEvent(self, event):
        pass

    def center_camera(self):
        plane_size = GameObject.__DEFAULT__PLANE_LENGTH__()
        x_multiplier = (self.imagesPerRow / 2) if self.imageCount >= self.imagesPerRow else self.imageCount / 2
        y_multiplier = -(self.imageCount / self.imagesPerRow) / 2
        x_pos = (plane_size + self.imageOffset) * x_multiplier
        y_pos = (plane_size + self.imageOffset) * y_multiplier
        DIContainer.scene.cameraHolder.set_position(x_pos, y_pos, 30)
