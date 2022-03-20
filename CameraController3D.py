from PySide6.Qt3DExtras import Qt3DExtras
import DIContainer


class CameraController3D(Qt3DExtras.QOrbitCameraController):
    def __init__(self):
        super().__init__(DIContainer.scene)
        self.setLinearSpeed(50)
        self.setLookSpeed(180)
        self.setCamera(DIContainer.scene.camera)
