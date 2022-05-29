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

    def __init__(self, width: int, height: int, filename=None):
        super().__init__()
        # Variables
        self.filename = filename

        # Computer vision
        self.histograms = None
        self.channels_means = None

        # Setting sizes
        self.setSize(QSize(width, height))
        pass

    def paint(self, painter: QPainter):
        path = os.path.join(DIContainer.main_window.defaultImageDirectory, self.filename)

        # Loading image with cv2
        cv_img = cv2.imread(path)
        height, width, channel = cv_img.shape
        bytes_per_line = 3 * width

        # Creating a QImage from the cv2 image
        image = QImage(cv_img.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped().scaled(
            QSize(self.width(), self.height()), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)

        # Calculating parameters necessary for computer vision
        self.channels_means = cv2.mean(cv_img)[:3]
        self.histograms = ImagesUtilities.get_image_histograms(cv_img)

        painter.drawImage(QRect(0, 0, self.width(), self.height()), image)
