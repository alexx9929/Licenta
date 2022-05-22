import DIContainer
from PySide6.QtGui import *
from PySide6.Qt3DExtras import Qt3DExtras
from PySide6.QtCore import *
from ObjectBuilding.GameObject import GameObject
from ObjectBuilding.Visuals import MeshBuilder, TextureMaterial
from memory_profiler import profile


class ObjectBuilder:

    def __init__(self):
        pass

    @staticmethod
    def create_textured_plane(translation: QVector3D, rotation: QQuaternion, scale: QVector3D, texture_size: int,
                              image_path=None):
        obj = GameObject(DIContainer.scene)
        obj.add_mesh(DIContainer.default_mesh)
        obj.add_material(
            TextureMaterial.TextureMaterial(texture_size, texture_size, filename=image_path))
        obj.transform.setTranslation(translation)
        obj.transform.setRotation(rotation)
        obj.transform.setScale3D(scale)
        DIContainer.scene.objects.append(obj)
        return
