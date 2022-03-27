from PySide6.Qt3DCore import Qt3DCore
from PySide6.QtGui import QVector3D, QQuaternion

import DIContainer


class GameObject:

    def __init__(self, name=""):
        # Dependencies
        self.scene = DIContainer.scene
        self.scene.objectIndex += 1

        # Object attributes
        self.entity = Qt3DCore.QEntity(self.scene)
        self.name = name if name != "" else self.DefaultGameObjectName()

        # Transform
        self.transform = Qt3DCore.QTransform()
        self.transform.setScale3D(QVector3D(1, 1, 1))
        self.transform.setRotation(QQuaternion.fromAxisAndAngle(QVector3D(0, 0, 0), 0))
        self.entity.addComponent(self.transform)

        # Visual layer
        self.mesh = None
        self.material = None
        self.texture = None
        self.textureImage = None

    def AddMesh(self, mesh):
        self.mesh = mesh
        self.entity.addComponent(self.mesh)

    def AddMaterial(self, material):
        self.material = material
        self.entity.addComponent(self.material)

    def DefaultGameObjectName(self):
        return str("GameObject(" + str(DIContainer.scene.objectIndex) + ")")
