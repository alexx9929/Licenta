import imagesize, math
import numpy as np
from enum import Enum
from ObjectBuilding.GameObject import GameObject
from PySide6.QtGui import QVector3D


class Distribution(Enum):
    planar = 1
    normal = 2


class SceneManager:

    def __init__(self):
        self.image_count = 100
        self.imageOffset = 0.1
        self.imagesPerRow = 10
        self.planeSize = GameObject.__DEFAULT__PLANE_LENGTH__()

        # Gaussian distribution
        self.image_distribution = Distribution.normal
        self.normal_mean = [0, 0, 0]
        self.normal_deviation = [30, 20, 20]

        # Images ratios
        self.ratios = {}
        self.keep_aspect_ratios = False
        pass

    def calculate_normal_distribution(self, count):
        square_root = math.sqrt(count)
        self.normal_deviation[0] = square_root * 0.25
        self.normal_deviation[1] = square_root * 0.5
        self.normal_deviation[2] = square_root * 0.25

    def calculate_positions(self, count):
        positions = []
        if self.image_distribution == Distribution.normal:
            self.calculate_normal_distribution(count)
            distributions = (np.random.normal(self.normal_mean[0], self.normal_deviation[0], count),
                             np.random.normal(self.normal_mean[1], self.normal_deviation[1], count),
                             np.random.normal(self.normal_mean[2], self.normal_deviation[2], count))
            for i in range(0, count):
                positions.append(QVector3D(distributions[0][i], distributions[1][i], distributions[2][i]))

        if self.image_distribution == Distribution.planar:
            self.imagesPerRow = int(math.sqrt(count))
            for i in range(0, count):
                current_row = int(i / self.imagesPerRow)
                current_col = i % self.imagesPerRow
                x_pos = float(current_col * (self.planeSize + self.imageOffset))
                y_pos = float(-current_row * (self.planeSize + self.imageOffset))
                z_pos = 0

                positions.append(QVector3D(x_pos, y_pos, z_pos))

        return positions
