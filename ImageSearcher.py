from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier
from Utilities import MiscFunctions, DataVisualization, ImagesUtilities
import DIContainer, cv2, math
from matplotlib import pyplot as plt
import numpy as np
from scipy.spatial.distance import cdist
from kneed import KneeLocator


class ImageSearcher:

    def __init__(self):
        self.k = 0
        pass

    def search_image(self, path, predicted_values, centroids):
        image = cv2.imread(path)
        print("Searching image: " + path)
        image_class = self.get_image_class(image, predicted_values)
        # correlations = self.get_histogram_correlations(cv_img)

    def get_histogram_correlations(self, searched_image):
        histograms = ImagesUtilities.get_image_histograms(searched_image)
        images = MiscFunctions.get_all_texture_images()
        correlations = []

        for i in images:
            r_correlation = cv2.compareHist(histograms[0], i.histograms[0], cv2.HISTCMP_CORREL)
            g_correlation = cv2.compareHist(histograms[1], i.histograms[1], cv2.HISTCMP_CORREL)
            b_correlation = cv2.compareHist(histograms[2], i.histograms[2], cv2.HISTCMP_CORREL)
            correlations.append([r_correlation, g_correlation, b_correlation])

        return correlations

    def get_optimal_k(self, data, using_distorions=False):
        """Uses elbow method with either distortion scores or inertia scores"""
        max_k = 20 if len(data) >= 20 else len(data)
        scores = []
        data = np.array(data)
        k_values = []

        for k in range(2, max_k + 1):
            k_values.append(k)
            kmeans = KMeans(n_clusters=k)
            kmeans.fit(data)

            if using_distorions:
                centers = kmeans.cluster_centers_
                distortion_score = sum(np.min(cdist(data, centers, 'euclidean'), axis=1)) / data.shape[0]
                scores.append(distortion_score)
            else:
                inertia_score = kmeans.inertia_
                scores.append(inertia_score)

        kneedle = KneeLocator(k_values, scores, curve="convex", direction="decreasing")
        plt.figure()
        plt.title("Optimal K")
        plt.plot(scores)
        plt.show()
        return kneedle.knee

    def get_optimal_neighbors(self, image, data, predicted_values):
        max_k = math.floor(math.sqrt(len(predicted_values)))
        scores = []
        data = np.array(data)
        k_values = []

        # Image data
        array = ImagesUtilities.swap_channels(cv2.mean(image)[:3])
        converted_array = np.array(array).reshape(1, -1)

        print("Searched array: " + str(converted_array))
        print("Data: " + str(data))
        for k in range(1, max_k + 1):
            k_values.append(k)
            knn = KNeighborsClassifier(n_neighbors=k, weights='distance')
            knn.fit(data, predicted_values)
            predicted_class = knn.predict(converted_array)
            score = 1 if predicted_class[0] == predicted_values[0] else 0
            scores.append(score)

        plt.figure()
        plt.title("Optimal neighbours using distance")
        plt.plot(scores)
        plt.show()
        return

    def get_predicted_values(self):
        # Machine learning
        data = ImagesUtilities.get_channels_means_array()
        self.k = self.get_optimal_k(data, True)

        print("Optimal K: " + str(self.k))
        k_means = KMeans(n_clusters=self.k, init='k-means++', max_iter=300, n_init=10, random_state=0)
        model = k_means.fit(data)
        predicted_values = k_means.predict(data)

        # Plotting results
        r, g, b = ImagesUtilities.get_channels_means()
        DataVisualization.ml_color_channels_scatter(r, g, b, predicted_values)
        return predicted_values, k_means.cluster_centers_

    def get_image_class(self, image, predicted_values):
        data = ImagesUtilities.get_channels_means_array()
        # self.get_optimal_neighbors(image, data, predicted_values)

        # Preparing the image data
        array = ImagesUtilities.swap_channels(cv2.mean(image)[:3])
        converted_array = np.array(array).reshape(1, -1)

        # Using the KNN algorithm
        knn = KNeighborsClassifier(n_neighbors=3, weights='distance')
        knn.fit(data, predicted_values)
        predicted_class = knn.predict(converted_array)

        print("Class of first image: " + str(predicted_values[0]))
        print("Predicted class: " + str(predicted_class[0]))
        return predicted_class

    @staticmethod
    def euclidian_distance_array(a1, a2):
        array = []
        for i in range(0, len(a1)):
            array.append(ImageSearcher.euclidian_distance(a1[i], a2[i]))
        return array

    @staticmethod
    def euclidian_distance(p1, p2):
        return math.sqrt(math.pow(p2[0] - p1[0], 2) + math.pow(p2[1] - p1[1], 2) + math.pow(p2[2] - p1[2], 2))
