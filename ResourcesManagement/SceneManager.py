import imagesize, math
import numpy as np
from enum import Enum
from ObjectBuilding.GameObject import GameObject
from PySide6.QtGui import QVector3D
import DIContainer
from Utilities import MiscFunctions


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
        self.keep_aspect_ratios = True
        pass

    def set_image_count(self, count):
        self.image_count = count

    def calculate_normal_distribution(self, count):
        square_root = math.sqrt(count)
        self.normal_deviation[0] = square_root * 0.25
        self.normal_deviation[1] = square_root * 0.5
        self.normal_deviation[2] = square_root * 0.25

    def calculate_all_positions(self, count):
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

    def generate_cluster_positions(self, means: list, count):
        """Generates positions for a cluster based on a normal distribution algorithm"""
        # Calculating distributions
        deviation = []
        square_root = math.sqrt(count)

        deviation.append(square_root * 0.5)
        deviation.append(square_root * 0.5)
        deviation.append(square_root * 0.5)

        distributions = (np.random.normal(means[0], deviation[0], count),
                         np.random.normal(means[1], deviation[1], count),
                         np.random.normal(means[2], deviation[2], count))

        # Generating positions
        positions = []
        for i in range(0, count):
            positions.append(QVector3D(distributions[0][i], distributions[1][i], distributions[2][i]))

        return positions

    def keep_one_cluster_active(self, image_cluster):
        """Deactivates other clusters and repositions the images from the given one"""
        predicted_values = DIContainer.image_searcher.predicted_values
        classes_counts = MiscFunctions.get_classes_counts()
        cluster_positions = self.calculate_all_positions(int(classes_counts[image_cluster]))
        position_index = -1
        print("Keeping cluster " + str(image_cluster) + " active")
        for i in range(0, len(predicted_values)):
            if predicted_values[i] != image_cluster:
                DIContainer.scene.objects[i].setEnabled(False)
            else:
                position_index += 1
                DIContainer.scene.objects[i].setEnabled(True)
                DIContainer.scene.objects[i].transform.setTranslation(cluster_positions[position_index])

    def group_clusters(self):
        """Repositions all images to highlight the clusters"""
        number_of_clusters = DIContainer.image_searcher.k
        classes_counts = MiscFunctions.get_classes_counts()
        predicted_values = DIContainer.image_searcher.predicted_values
        objects = DIContainer.scene.objects

        # Generating positions matrix that holds all positions for every cluster
        positions_matrix = []
        for i in range(0, number_of_clusters):
            means = [i * 10, i * 10, i * 10]
            positions_matrix.append(self.generate_cluster_positions(means, classes_counts[i]))

        # Grouping the images
        positions_counter_matrix = np.zeros(number_of_clusters, dtype='int')
        for i in range(0, len(objects)):
            image_class = predicted_values[i]
            position_index = positions_counter_matrix[image_class]
            objects[i].transform.setTranslation(positions_matrix[image_class][position_index])
            positions_counter_matrix[image_class] += 1

        pass
