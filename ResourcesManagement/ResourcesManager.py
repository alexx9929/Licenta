import os, sys
from PySide6.QtGui import *
from time import perf_counter
from Utilities import MiscFunctions


class ResourcesManager:

    def __init__(self):
        pass

    @staticmethod
    def load_images(directory: str, count: int):
        files = os.listdir(directory)
        images = []
        images_creation_times = []

        for i in range(0, count):
            path = os.path.join(directory, files[i])
            t01 = perf_counter()
            images.append(QImage(path))
            t02 = perf_counter()
            images_creation_times.append((t02 - t01) * 1000)

        print(f"Average image creation time: {sum(images_creation_times) / len(images_creation_times):0.02} ms")
        return images
