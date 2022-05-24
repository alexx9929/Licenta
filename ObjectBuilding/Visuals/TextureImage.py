from PySide6.QtGui import QImage, QPainter
from PySide6.QtCore import QRect, QSize, Qt
from PySide6.Qt3DRender import Qt3DRender
import os
import numpy as np
import cv2
import DIContainer
from matplotlib import pyplot as plt


class TextureImage(Qt3DRender.QPaintedTextureImage):

    def __init__(self, width: int, height: int, filename=None):
        super().__init__()
        # Variables
        self.filename = filename

        # Setting sizes
        self.setWidth(width)
        self.setHeight(height)

        self.histogram = None
        pass

    def paint(self, painter: QPainter):
        if not self.filename:
            return

        path = os.path.join(DIContainer.main_window.defaultImageDirectory, self.filename)
        cv_img = cv2.imread(path)
        height, width, channel = cv_img.shape
        bytes_per_line = 3 * width
        image = QImage(cv_img.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped().scaled(
            QSize(self.width(), self.height()), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)

        # define colors to plot the histograms
        colors = ('b', 'g', 'r')
        self.histogram = []

        # compute and plot the image histograms
        for i, color in enumerate(colors):
            hist = cv2.calcHist([cv_img], [i], None, [256], [0, 256])
            #plt.plot(hist, color=color)
            self.histogram.append(hist)

        # plt.title('Histogram of ' + self.filename)
        # plt.show()

        painter.drawImage(QRect(0, 0, self.width(), self.height()), image)
