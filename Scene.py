from PySide6.Qt3DCore import Qt3DCore
from PySide6.QtGui import QVector3D, QQuaternion
from PySide6.Qt3DExtras import Qt3DExtras
from PySide6.Qt3DRender import Qt3DRender
import DIContainer
from CameraController3D import CameraController3D


class Scene(Qt3DCore.QEntity):

    def __init__(self):
        super().__init__()
        self.objectIndex = 0
        self.objects = []

        # Camera
        self.camera = None
        self.cameraController = None
        pass

    def initialize(self):
        self.initialize_camera()

    def initialize_camera(self):
        self.camera = DIContainer.view.camera()
        self.camera.lens().setPerspectiveProjection(45, 16 / 9, 0.1, 1000)
        self.camera.setPosition(QVector3D(0, 0, 40))
        self.camera.setViewCenter(QVector3D(0, 0, 0))

        self.cameraController = CameraController3D()
