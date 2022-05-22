import os, sys
from PySide6.QtGui import *
from time import perf_counter
from Utilities import MiscFunctions
from PySide6.QtCore import QRect, QSize, Qt
from memory_profiler import profile
import numpy as np
import imagesize


class ResourcesManager:

    def __init__(self):
        pass

    @staticmethod
    def load_image(path: str, image_size=0):
        if image_size > 0:
            return QImage(path).scaled(QSize(image_size, image_size), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        else:
            return QImage(path)

    @staticmethod
    def load_images(directory: str, count: int, image_size: int):
        files = os.listdir(directory)
        images = []
        for i in range(0, count):
            path = os.path.join(directory, files[i])
            images.append(
                QImage(path).scaled(QSize(image_size, image_size), Qt.IgnoreAspectRatio, Qt.SmoothTransformation))

        return images

    @staticmethod
    def get_ratios(directory: str, files, count: int):
        """This method will return a dictionary that contains the ratios of the images
         and the count for each ratio"""

        ratios = {}

        for i in range(0, count):
            path = os.path.join(directory, files[i])
            width, height = imagesize.get(path)
            ratio = width / height
            ratio_str = str(ratio)[:3]
            if ratio_str in ratios.keys():
                ratios[ratio_str] += 1
            else:
                ratios[ratio_str] = 1

        return ratios
