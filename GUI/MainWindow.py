import DIContainer, os, sys, math
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from ObjectBuilding.GameObject import GameObject
from time import perf_counter
from ResourcesManagement.ResourcesManager import ResourcesManager
from ObjectBuilding.ObjectBuilder import ObjectBuilder
from Utilities import MiscFunctions
from memory_profiler import profile


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
        self.imageOffset = 1
        self.imagesPerRow = 10
        self.textureSize = 255
        self.imageCount = 100
        self.planeSize = GameObject.__DEFAULT__PLANE_LENGTH__()

        # Setup
        self.central_widget.setLayout(self.grid)
        self.setCentralWidget(self.central_widget)

        self.showMaximized()
        # self.setMinimumWidth(2560)
        # self.setMinimumHeight(1336)

        # Top buttons
        self.top_buttons = QWidget(self)
        self.top_layout = QVBoxLayout()
        self.top_buttons.setLayout(self.top_layout)

        self.loadImagesButton = QPushButton("Load images")
        self.loadSingleImageButton = QPushButton("Load single image")
        self.imageCountLineEdit = QLineEdit()

        #self.top_layout.addWidget(self.loadSingleImageButton)
        self.top_layout.addWidget(self.loadImagesButton)
        self.top_layout.addWidget(self.imageCountLineEdit)
        self.top_buttons.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        # Image loading buttons
        self.defaultImageDirectory = 'C:\\Users\\serba\\Desktop\\Comedy gold 2'
        #self.defaultImageDirectory = 'C:\\Users\\serba\\Desktop\\Sample images'
        self.loadImagesButton.clicked.connect(
            lambda x: self.load_images_in_scene(QFileDialog.getExistingDirectory(dir=self.defaultImageDirectory),
                                                self.get_image_count()))
        # self.loadSingleImageButton.clicked.connect(
        #     lambda x: self.load_image_in_scene(QFileDialog.selectedFiles(dir=self.defaultImageDirectory)[0]))

        self.imageCountLineEdit.setText(str(self.imageCount))
        self.imageCountLineEdit.textChanged.connect(lambda x: self.set_image_count(int(self.imageCountLineEdit.text())))
        self.grid.addWidget(self.top_buttons)
        self.grid.addWidget(DIContainer.window_container)

    def get_image_count(self):
        return self.imageCount

    def set_image_count(self, count: int):
        self.imageCount = count

    @profile
    def load_image_in_scene(self, path: str, imageSize: int, clear = True):
        if not path or path == "":
            return

        if clear:
            DIContainer.scene.clear_scene()

        position = QVector3D(0, 0, 0)
        rotation = QQuaternion.fromEulerAngles(90, 0, 0)
        scale = QVector3D(1, 1, 1)

        plane = ObjectBuilder.create_textured_plane(position, rotation, scale, self.textureSize, image=ResourcesManager.load_image(path, imageSize))
        self.center_camera()

    @profile
    def load_images_in_scene(self, directory: str, count: int):
        if not directory or directory == "":
            return

        DIContainer.scene.clear_scene()
        objects_creation_times = []

        t01 = perf_counter()
        images = ResourcesManager.load_images(directory, count, self.textureSize)
        t02 = perf_counter()

        self.imagesPerRow = int(math.sqrt(self.imageCount))

        for i in range(0, len(images)):
            current_row = int(i / self.imagesPerRow)
            current_col = i % self.imagesPerRow

            x_pos = float(current_col * (self.planeSize + self.imageOffset))
            y_pos = float(-current_row * (self.planeSize + self.imageOffset))
            z_pos = 0

            position = QVector3D(x_pos, y_pos, z_pos)
            rotation = QQuaternion.fromEulerAngles(90, 0, 0)
            scale = QVector3D(1, 1, 1)

            t11 = perf_counter()
            plane = ObjectBuilder.create_textured_plane(position, rotation, scale, self.textureSize, image=images[i])
            t12 = perf_counter()
            objects_creation_times.append(t12 - t11)

        self.center_camera()
        average_object_creation_time = (sum(objects_creation_times) / len(objects_creation_times)) * 1000
        print(f"Average object creation time (without image creation): {average_object_creation_time:0.6f} ms")
        print(f"{len(images)} images created in {t02 - t01:0.2f} seconds")
        t03 = perf_counter()
        print(f"{len(images)} objects created in {t03 - t01:0.2f} seconds")
        print("\n")

    def center_camera(self):
        plane_size = GameObject.__DEFAULT__PLANE_LENGTH__()
        x_multiplier = (self.imagesPerRow / 2) if self.imageCount >= self.imagesPerRow else self.imageCount / 2
        y_multiplier = -(self.imageCount / self.imagesPerRow) / 2

        if self.imagesPerRow % 2 != 0:
            x_multiplier -= 0.5

        if (self.imagesPerRow * self.imagesPerRow) % 2 != 0:
            y_multiplier += 0.5

        x_pos = (plane_size + self.imageOffset) * x_multiplier
        y_pos = (plane_size + self.imageOffset) * y_multiplier
        DIContainer.scene.cameraHolder.set_position(x_pos, y_pos, 40)
