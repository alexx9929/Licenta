from PySide6.Qt3DRender import Qt3DRender
from PySide6.QtGui import QVector3D
import DIContainer


class Camera3D(Qt3DRender.QCamera):
    def __init__(self, viewCamera):
        super().__init__(viewCamera)
        self.lens().setPerspectiveProjection(45, 16 / 9, 0.1, 1000)
        self.setPosition(QVector3D(0, 0, 40))
        self.setViewCenter(QVector3D(0, 0, 0))
