import os
from PySide6.QtGui import *


class ResourcesManager:

    def __init__(self):

        pass

    @staticmethod
    def load_images(directory: str, count: int):
        files = os.listdir(directory)
        images = []

        for i in range(0, count):
            path = os.path.join(directory, files[i])
            images.append(QImage(path))

        return images
