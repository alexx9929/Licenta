from PySide6.Qt3DCore import Qt3DCore
import DIContainer
from PySide6.Qt3DRender import Qt3DRender
import time, threading


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

        # Object picker
        self.object_picker = None
        pass

    def add_mesh(self, mesh):
        self.addComponent(mesh)

    def add_material(self, material):
        self.material = material
        self.addComponent(self.material)

    def add_object_picker(self):
        self.object_picker = Qt3DRender.QObjectPicker()
        self.addComponent(self.object_picker)
        self.object_picker.clicked.connect(self.object_clicked_callback)

    def object_clicked_callback(self, evt: Qt3DRender.QPickEvent):
        main_window = DIContainer.main_window
        if main_window.clicked_object == self.name:
            print("Double clicked on " + self.name)
        else:
            main_window.clicked_object = self.name

    @staticmethod
    def __DEFAULT_GAMEOBJECT_NAME__():
        return str("GameObject(" + str(DIContainer.scene.objectIndex) + ")")

    # At a scale of (1, 1, 1), the plane primitive has a world length of 10
    @staticmethod
    def __DEFAULT__PLANE_LENGTH__():
        return 1
