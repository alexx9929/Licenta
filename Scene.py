from PySide6.Qt3DCore import Qt3DCore


class Scene(Qt3DCore.QEntity):

    def __init__(self):
        super().__init__()
        self.objectIndex = 0
        self.objects = []
        pass
