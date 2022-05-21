from PySide6.Qt3DCore import Qt3DCore
import DIContainer


class GameObject(Qt3DCore.QEntity):

    def __init__(self, parent, name=""):
        super().__init__(parent)
        # Dependencies
        DIContainer.scene.objectIndex += 1

        # Object attributes
        self.name = name if name != "" else GameObject.__DEFAULT_GAMEOBJECT_NAME__()

        # Transform
        self.transform = Qt3DCore.QTransform()
        self.addComponent(self.transform)

        # Visual layer
        self.material = None
        pass

    def add_mesh(self, mesh):
        self.addComponent(mesh)

    def add_material(self, material):
        self.material = material
        self.addComponent(self.material)

    @staticmethod
    def __DEFAULT_GAMEOBJECT_NAME__():
        return str("GameObject(" + str(DIContainer.scene.objectIndex) + ")")

    # At a scale of (1, 1, 1), the plane primitive has a world length of 10
    @staticmethod
    def __DEFAULT__PLANE_LENGTH__():
        return 1
