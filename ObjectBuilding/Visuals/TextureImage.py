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
        self.histogram = None
        self.histograms = None
        self.channels_means = None

        # Setting sizes
        self.setSize(QSize(width, height))
        pass

    def paint(self, painter: QPainter):
        path = self.get_full_path()

        # Loading image with cv2
        cv_img = cv2.imread(path)
        height, width, channel = cv_img.shape
        bytes_per_line = 3 * width

        # Creating a QImage from the cv2 image
        image = QImage(cv_img.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped().scaled(
            QSize(self.width(), self.height()), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)

        # Calculating parameters necessary for computer vision
        self.channels_means = cv2.mean(cv_img)[:3]
        # self.histograms = ImagesUtilities.get_image_histograms(cv_img)
        self.histogram = self.image_histogram(cv_img, 'HSV', 256)
        painter.drawImage(QRect(0, 0, self.width(), self.height()), image)

    def image_histogram(self, img, color_space, bins):
        if color_space == 'HSV':
            code = cv2.COLOR_BGR2HSV
            max_val = [360, 1, 256]
        else:
            if color_space == 'RGB':
                code = cv2.COLOR_BGR2RGB
                max_val = [256, 256, 256]
            else:
                print('Invalid colorspace')
                return

        img = cv2.cvtColor(img, code=code)
        concat_hist = []

        for i in range(3):
            channel = img[:, :, i]
            hist = cv2.calcHist([channel], [0], None, [bins], [0, max_val[i]])
            concat_hist.append(hist)

        return np.array(concat_hist).flatten()

    def get_full_path(self):
        return os.path.join(DIContainer.main_window.defaultImageDirectory, self.filename)
