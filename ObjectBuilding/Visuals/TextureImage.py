from PySide6.QtGui import QImage, QPainter
from PySide6.QtCore import QRect, QSize, Qt
from PySide6.Qt3DRender import Qt3DRender
import os
import numpy as np
import cv2
import DIContainer
from matplotlib import pyplot as plt
from Utilities import ImagesUtilities


class TextureImage(Qt3DRender.QPaintedTextureImage):

    def __init__(self):
        super().__init__()
        # Variables
        self.image = None
        self.filename = None

        # Computer vision
        self.histogram = None
        pass

    def paint(self, painter: QPainter):
        painter.drawImage(QRect(0, 0, self.width(), self.height()), self.image)
        self.image = None         # Once we paint the image we don't need it anymore

    def get_full_path(self):
        return os.path.join(DIContainer.main_window.defaultImageDirectory, self.filename)
