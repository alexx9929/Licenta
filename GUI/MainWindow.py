from PySide6.QtWidgets import *
from ObjectBuilder.GameObject import GameObject
import DIContainer


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

        # Setup
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.setMinimumWidth(2560)
        self.setMinimumHeight(1336)

    def resizeEvent(self, event):
        pass

    def center_camera(self):
        planeSize = GameObject.__DEFAULT__PLANE_LENGTH__()
        xMultiplier = (self.imagesPerRow / 2) if self.imageCount >= self.imagesPerRow else self.imageCount / 2
        yMultiplier = -(self.imageCount / self.imagesPerRow) / 2
        xPos = (planeSize + self.imageOffset) * xMultiplier
        yPos = (planeSize + self.imageOffset) * yMultiplier
        DIContainer.scene.cameraHolder.set_position(xPos, yPos, 30)
