from PySide6.QtGui import QVector3D
import DIContainer
import PySide6.Qt3DRender


class CameraHolder3D:
    def __init__(self):
        self.camera = DIContainer.view.camera()
        self.camera.lens().setPerspectiveProjection(45, 16 / 9, 0.1, 1000)
        self.camera.setPosition(QVector3D(0, 0, 40))
        self.camera.setViewCenter(QVector3D(0, 0, 0))
        pass

    def set_position(self, x: float, y: float, z: float):
        delta = QVector3D(x, y, z) - self.camera.position()
        self.camera.translateWorld(delta,
                                   option=PySide6.Qt3DRender.Qt3DRender.QCamera.CameraTranslationOption.TranslateViewCenter)

    def set_position_vector(self, position: QVector3D):
        delta = position - self.camera.position()
        self.camera.translateWorld(delta,
                                   option=PySide6.Qt3DRender.Qt3DRender.QCamera.CameraTranslationOption.TranslateViewCenter)

    def get_position(self):
        pos = self.camera.position()
        new_pos = QVector3D(pos.x(), pos.y(), pos.z())
        return new_pos

    def get_rotation(self):
        return self.camera.transform().rotation().toEulerAngles()

    def print_position(self):
        print("Position: " + str(self.camera.position().x())[:5] + ", " + str(self.camera.position().y())[
                                                                          :5] + ", " + str(
            self.camera.position().z())[:5])

    def print_rotation(self):
        rotation = self.get_rotation()
        print("Rotation: " + str(rotation.x())[:5] + ", " + str(rotation.y())[:5] + ", " + str(rotation.z())[:5])
