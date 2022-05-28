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
        #self.plotted = False

        # Setting sizes
        self.setWidth(width)
        self.setHeight(height)

        self.histogram = None
        #self.cumulative_histogram = None

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
        #self.cumulative_histogram = []

        # compute and plot the image histograms
        # if not self.plotted:
        #     plt.figure()
        #     plt.title('Color distribution ' + self.filename)

        for i, color in enumerate(colors):
            hist = cv2.calcHist([cv_img], [i], None, [256], [0, 256])
            self.histogram.append(hist)
            #flattened = hist.flatten()
            #self.cumulative_histogram.append(np.cumsum(flattened))

        #     if not self.plotted:
        #         plt.plot(hist, color=color)
        #
        # if not self.plotted:
        #     plt.figure()
        #     plt.title('Color distribution ' + self.filename)
        #     plt.plot(self.cumulative_histogram[0], color='b')
        #     plt.plot(self.cumulative_histogram[1], color='g')
        #     plt.plot(self.cumulative_histogram[2], color='r')
        #     plt.title('Intensities ' + self.filename)
        #     plt.show()
        #     self.plotted = True

        painter.drawImage(QRect(0, 0, self.width(), self.height()), image)
