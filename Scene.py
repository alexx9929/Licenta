from PySide6.Qt3DCore import Qt3DCore
from PySide6.QtGui import QVector3D, QQuaternion
from PySide6.Qt3DExtras import Qt3DExtras
from PySide6.Qt3DRender import Qt3DRender
import DIContainer
from CameraController3D import CameraController3D
from CameraHolder3D import CameraHolder3D


class Scene(Qt3DCore.QEntity):

    def __init__(self):
        super().__init__()
        self.objectIndex = 0
        self.objects = []

        # Camera
        self.cameraHolder = None
        self.cameraController = None
        pass

    def initialize(self):
        self.initialize_camera()

    def initialize_camera(self):
        self.cameraHolder = CameraHolder3D()
        self.cameraController = CameraController3D()
