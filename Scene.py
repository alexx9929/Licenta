from PySide6.Qt3DCore import Qt3DCore
from Cameras.CameraController3D import CameraController3D
from Cameras.CameraHolder3D import CameraHolder3D
import DIContainer
from ObjectBuilding.Visuals import MeshBuilder


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
        self.cameraController = DIContainer.camera_controller = CameraController3D()

    def clear_scene(self):
        for i in self.objects:
            i.setParent(None)
        self.objects = []
        Scene.recreate_mesh()

    @staticmethod
    def recreate_mesh():
        DIContainer.default_mesh = MeshBuilder.create_plane_mesh()
