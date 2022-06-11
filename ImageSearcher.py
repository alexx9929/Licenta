from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier
from Utilities import MiscFunctions, DataVisualization, ImagesUtilities
import DIContainer, cv2, math
from matplotlib import pyplot as plt
import numpy as np
from scipy.spatial.distance import cdist
from kneed import KneeLocator
from time import perf_counter


class ImageSearcher:

    def __init__(self):
        self.k = 0
        self.predicted_values = None
        pass

    def start_classification(self, use_histograms):
        """Applies a K-means algorithm to classify the data using histograms or the color channels of the images"""
        t1 = perf_counter()
        self.predicted_values = self.get_predicted_values(use_histograms)
        t2 = perf_counter()
        print("Machine learning time: " + str(t2 - t1)[:4])
        pass

    def search_image(self, path):
        """Searches the image through the clusters using a KNN algorithm"""
        image_cluster = self.get_image_cluster(path)
        DIContainer.scene_manager.keep_one_cluster_active(image_cluster)
        pass

    def get_image_cluster(self, path):
        image = cv2.imread(path)
        print("Searching image: " + path)
        t1 = perf_counter()
        image_class = self.get_image_class(image)
        t2 = perf_counter()
        print("Searching time: " + str(t2 - t1)[:5])
        return image_class
        # correlations = self.get_histogram_correlations(cv_img)

    def test_n_image_search(self, n, predicted_values):
        passed_tests = 0
        failed_tests = 0

        for i in range(0, n):
            value = self.test_image_search(predicted_values)
            if value:
                passed_tests += 1
            else:
                failed_tests += 1

        print("Passed tests: " + str(passed_tests))
        print("Failed tests: " + str(failed_tests))

    def test_image_search(self, predicted_values):
        image_index = np.random.randint(len(predicted_values) - 1)
        obj = MiscFunctions.get_all_texture_images()[image_index]
        path = obj.get_full_path()
        image_class = predicted_values[image_index]
        image = cv2.imread(path)

        # print("Image index: " + str(image_index))
        # print("Searching " + path)
        # print("Image class: " + str(image_class))
        predicted_class = self.get_image_class(image)
        return predicted_class == image_class

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
        # plt.figure()
        # plt.title("Optimal K")
        # plt.plot(scores)
        # plt.show()
        return kneedle.knee

    def get_predicted_values(self, use_histograms):
        # Machine learning
        data = ImagesUtilities.get_histograms() if use_histograms else ImagesUtilities.get_channels_means_array()
        self.k = self.get_optimal_k(data, True)

        print("Optimal K: " + str(self.k))
        k_means = KMeans(n_clusters=self.k)
        model = k_means.fit(data)
        predicted_values = k_means.predict(data)

        # # Plotting results
        # r, g, b = ImagesUtilities.get_channels_means()
        # DataVisualization.ml_color_channels_scatter(r, g, b, predicted_values)
        return predicted_values

    def get_image_class(self, image):
        data = ImagesUtilities.get_channels_means_array()

        # Preparing the image data
        array = ImagesUtilities.swap_channels(cv2.mean(image)[:3])
        converted_array = np.array(array).reshape(1, -1)

        # Using the KNN algorithm
        knn = KNeighborsClassifier(n_neighbors=3, weights='distance')
        knn.fit(data, self.predicted_values)
        predicted_class = knn.predict(converted_array)

        return predicted_class[0]

    @staticmethod
    def euclidian_distance_array(a1, a2):
        array = []
        for i in range(0, len(a1)):
            array.append(ImageSearcher.euclidian_distance(a1[i], a2[i]))
        return array

    @staticmethod
    def euclidian_distance(p1, p2):
        return math.sqrt(math.pow(p2[0] - p1[0], 2) + math.pow(p2[1] - p1[1], 2) + math.pow(p2[2] - p1[2], 2))
