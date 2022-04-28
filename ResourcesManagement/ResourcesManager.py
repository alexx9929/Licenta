import os, sys
from PySide6.QtGui import *
from time import perf_counter
from Utilities import MiscFunctions
from PySide6.QtCore import QRect, QSize, Qt
from memory_profiler import profile
import numpy as np


class ResourcesManager:

    def __init__(self):
        pass

    @staticmethod
    def load_image(path: str, imageSize=0):
        if imageSize > 0:
            return QImage(path).scaled(QSize(imageSize, imageSize), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        else:
            return QImage(path)

    @staticmethod
    def load_images(directory: str, count: int, imageSize: int):
        files = os.listdir(directory)
        images = []
        for i in range(0, count):
            path = os.path.join(directory, files[i])
            images.append(QImage(path).scaled(QSize(imageSize, imageSize), Qt.IgnoreAspectRatio, Qt.SmoothTransformation))

        return images
