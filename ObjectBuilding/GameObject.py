from PySide6.Qt3DCore import Qt3DCore
from PySide6.QtGui import QVector3D, QQuaternion

import DIContainer


class GameObject:
    __slots__ = ['name', 'entity', 'transform', 'material', 'mesh']

    def __init__(self, name=""):
        # Dependencies
        DIContainer.scene.objectIndex += 1

        # Object attributes
        self.entity = Qt3DCore.QEntity(DIContainer.scene)
        self.name = name if name != "" else GameObject.__DEFAULT_GAMEOBJECT_NAME__()

        # Transform
        self.transform = Qt3DCore.QTransform()
        self.transform.setScale3D(QVector3D(1, 1, 1))
        self.transform.setRotation(QQuaternion.fromAxisAndAngle(QVector3D(0, 0, 0), 0))
        self.entity.addComponent(self.transform)

        # Visual layer
        # self.mesh = None
        self.material = None
        pass

    def add_mesh(self, mesh):
        self.entity.addComponent(mesh)

    def add_material(self, material):
        self.material = material
        self.entity.addComponent(self.material)

    @staticmethod
    def __DEFAULT_GAMEOBJECT_NAME__():
        return str("GameObject(" + str(DIContainer.scene.objectIndex) + ")")

    # At a scale of (1, 1, 1), the plane primitive has a world length of 10
    @staticmethod
    def __DEFAULT__PLANE_LENGTH__():
        return 1
