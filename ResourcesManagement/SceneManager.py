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

        self.clusters_distributions = []

        self.clusters_center = [0, 0, 0]
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

    def generate_cluster_positions(self, means: list, deviations: list, count):
        """Generates positions for a cluster based on a normal distribution algorithm"""
        # Calculating distributions
        deviation = []
        square_root = math.sqrt(count)

        deviation.append(square_root * 0.5)
        deviation.append(square_root * 0.5)
        deviation.append(square_root * 0.5)

        distributions = (np.random.normal(means[0], deviations[0], count),
                         np.random.normal(means[1], deviations[1], count),
                         np.random.normal(means[2], deviations[2], count))

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
        min_array = [999, 999, 999]
        max_array = [0, 0, 0]
        self.clusters_center = [0, 0, 0]
        self.clusters_distributions = []
        number_of_clusters = DIContainer.image_searcher.k
        classes_counts = MiscFunctions.get_classes_counts()
        predicted_values = DIContainer.image_searcher.predicted_values
        objects = DIContainer.scene.objects

        # Generating positions matrix that holds all positions for every cluster
        positions_matrix = []
        last_x_deviation = 0
        last_x_mean = 0
        x_offset = 4
        y_offset = 4

        deviation_sum = 0
        for i in range(0, number_of_clusters):
            number_of_images_in_cluster = classes_counts[i]
            square_root = math.sqrt(number_of_images_in_cluster)
            deviation_sum += square_root * 0.5

        average_deviation = deviation_sum / number_of_clusters
        clusters_per_row = int(math.sqrt(number_of_clusters))
        last_row_index = 0

        for i in range(0, number_of_clusters):
            number_of_images_in_cluster = classes_counts[i]

            # Calculating deviations of the cluster
            square_root = math.sqrt(number_of_images_in_cluster)
            deviations = [square_root * 0.5, square_root * 0.5, square_root * 0.5]

            # Calculating means for a new normal distribution
            new_x_mean = last_x_mean + last_x_deviation * 3 + deviations[0] * 3 + x_offset

            last_x_deviation = deviations[0]

            current_row = int(i / clusters_per_row)

            if current_row != last_row_index:
                new_x_mean = 0

            last_x_mean = new_x_mean

            last_row_index = current_row
            new_y_mean = current_row * (average_deviation * 3 + deviations[1] * 3 + y_offset)
            means = [new_x_mean, new_y_mean, 0]
            self.clusters_distributions.append((means, deviations))
            positions_matrix.append(self.generate_cluster_positions(means, deviations, classes_counts[i]))

        # Grouping the images
        positions_counter_matrix = np.zeros(number_of_clusters, dtype='int')
        for i in range(0, len(objects)):
            image_class = predicted_values[i]
            position_index = positions_counter_matrix[image_class]
            objects[i].transform.setTranslation(positions_matrix[image_class][position_index])
            positions_counter_matrix[image_class] += 1

        for i in range(0, len(positions_matrix)):
            for j in range(0, len(positions_matrix[i])):
                if positions_matrix[i][j].x() > max_array[0]:
                    max_array[0] = positions_matrix[i][j].x()
                if positions_matrix[i][j].x() < min_array[0]:
                    min_array[0] = positions_matrix[i][j].x()

                if positions_matrix[i][j].y() > max_array[1]:
                    max_array[1] = positions_matrix[i][j].y()
                if positions_matrix[i][j].y() < min_array[1]:
                    min_array[1] = positions_matrix[i][j].y()

                if positions_matrix[i][j].z() > max_array[2]:
                    max_array[2] = positions_matrix[i][j].z()
                if positions_matrix[i][j].z() < min_array[2]:
                    min_array[2] = positions_matrix[i][j].z()

        self.clusters_center = QVector3D((min_array[0] + max_array[0]) / 2, (min_array[1] + max_array[1]) / 2, 40)
        DIContainer.camera_controller.center_camera()
        pass

    def group_cluster(self, objects, predicted_values, cluster_index, positions):
        position_counter = 0
        for i in range(0, len(objects)):
            image_class = predicted_values[i]
            if image_class == cluster_index:
                objects[i].transform.setTranslation(positions[position_counter])
                position_counter += 1
