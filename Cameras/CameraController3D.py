from PySide6.Qt3DExtras import Qt3DExtras
import DIContainer
from ResourcesManagement.SceneManager import SceneManager, Distribution
from ObjectBuilding.GameObject import GameObject


class CameraController3D(Qt3DExtras.QOrbitCameraController):
    def __init__(self):
        super().__init__(DIContainer.scene)
        self.scene_manager = DIContainer.scene_manager

        self.setLinearSpeed(50)
        self.setLookSpeed(180)
        self.setCamera(DIContainer.scene.cameraHolder.camera)

    def center_camera(self):
        if self.scene_manager.image_distribution == Distribution.planar:
            count = self.scene_manager.image_count
            imagesPerRow = self.scene_manager.imagesPerRow
            offset = self.scene_manager.imageOffset

            plane_size = GameObject.__DEFAULT__PLANE_LENGTH__()
            x_multiplier = (imagesPerRow / 2) if count >= imagesPerRow else count / 2
            y_multiplier = -(count / imagesPerRow) / 2

            if imagesPerRow % 2 != 0:
                x_multiplier -= 0.5

            if (imagesPerRow * imagesPerRow) % 2 != 0:
                y_multiplier += 0.5

            x_pos = (plane_size + offset) * x_multiplier
            y_pos = (plane_size + offset) * y_multiplier
            DIContainer.scene.cameraHolder.set_position(x_pos, y_pos, 10)

        if self.scene_manager.image_distribution == Distribution.normal:
            z_pos = self.scene_manager.normal_deviation[2] * 2
            #print("D: " + str(self.scene_manager.normal_deviation[2])[:3] + " Z: " + str(z_pos)[:3])
            DIContainer.scene.cameraHolder.set_position(0, 0, z_pos)