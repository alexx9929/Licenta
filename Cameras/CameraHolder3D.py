from PySide6.QtGui import QVector3D
import DIContainer


class CameraHolder3D:
    def __init__(self):
        self.camera = DIContainer.view.camera()
        self.camera.lens().setPerspectiveProjection(45, 16 / 9, 0.1, 1000)
        self.camera.setPosition(QVector3D(0, 0, 0))
        #self.camera.setViewCenter(QVector3D(0, 0, 0))
        pass

    def set_position(self, x: float, y: float, z: float):
        self.camera.setPosition(QVector3D(x, y, z))
        #self.camera.setViewCenter(QVector3D(0, 0, 0))
        #self.camera.translateWorld(QVector3D(x, y, z))
        print(self.camera.position())
