import sklearn.metrics
from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import silhouette_score, confusion_matrix, plot_confusion_matrix,ConfusionMatrixDisplay
from Utilities import MiscFunctions, DataVisualization, ImagesUtilities
import DIContainer, cv2, math
from matplotlib import pyplot as plt
import numpy as np
from scipy.spatial.distance import cdist
from kneed import KneeLocator
from time import perf_counter
from pretty_confusion_matrix import pp_matrix_from_data


class ImageSearcher:

    def __init__(self):
        self.k = 0
        self.predicted_values = None
        self.labels = None
        pass

    def start_classification(self, use_histograms):
        """Applies a K-means algorithm to classify the data using histograms or the color channels of the images"""
        t1 = perf_counter()
        self.predicted_values = self.get_predicted_values()
        t2 = perf_counter()
        print("Machine learning time: " + str(t2 - t1)[:4])

        #count = len(DIContainer.scene.objects)
       # self.confusion_matrix()
        #DIContainer.image_searcher.test_n_image_search(count, self.predicted_values)
        pass

    def search_image(self, path):
        """Searches the image through the clusters using a KNN algorithm"""
        image_cluster = self.get_image_cluster(path)
        DIContainer.camera_controller.start_movement_to_cluster(image_cluster)
        #DIContainer.scene_manager.keep_one_cluster_active(image_cluster)
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

    def confusion_matrix(self):
        test_values = self.predicted_values
        predicted_values = []
        count = len(DIContainer.scene.objects)

        for i in range(0, count):
            print("Searching " + str(i))
            img = cv2.imread(DIContainer.scene.objects[i].get_texture_image().get_full_path())
            predicted_values.append(self.get_image_class(img))

        pp_matrix_from_data(test_values, predicted_values)

    def test_n_image_search(self, n, predicted_values):
        passed_tests = 0
        failed_tests = 0

        for i in range(0, n):
            print("Testing " + str(i))
            value = self.test_image_search(predicted_values)
            if value:
                passed_tests += 1
            else:
                failed_tests += 1

        print("Passed tests: " + str(passed_tests))
        print("Failed tests: " + str(failed_tests))

    def test_image_search(self, predicted_values):
        # A random index from the available ones
        image_index = np.random.randint(len(predicted_values) - 1)

        # The object that contains the image
        obj = MiscFunctions.get_all_texture_images()[image_index]

        # Path of the image
        path = obj.get_full_path()

        # The cluster to which the image belongs, taken from the predicted values
        image_class = predicted_values[image_index]

        # KNN predicts to which cluster the image belongs
        image = cv2.imread(path)
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

    def get_optimal_k(self, data, using_elbow, using_distorions=False):
        """Uses elbow method or silhouette method with either distortion scores or inertia scores"""
        max_k = 30 if len(data) >= 30 else len(data)
        data = np.array(data)
        k_values = []
        scores = []

        if not using_elbow:
            for k in range(2, 11):
                k_values.append(k)
                kmeans = KMeans(n_clusters=k).fit(data)
                print(kmeans.labels_)
                sil_coeff = silhouette_score(data, kmeans.labels_, metric='euclidean')
                scores.append(sil_coeff)
                print("For n_clusters={}, The Silhouette Coefficient is {}".format(k, sil_coeff))

            max = np.max(scores)
            index = scores.index(max)
            optimal_k = k_values[index]
            print("Optimal K: " + str(optimal_k))
            return optimal_k
        else:
            for k in range(2, max_k + 1):
                print("K: " + str(k))
                k_values.append(k)
                kmeans = KMeans(n_clusters=k)
                kmeans.fit(data)

                if using_distorions:
                    distortion_score = sum(np.min(cdist(data, kmeans.cluster_centers_, 'euclidean'), axis=1)) / data.shape[0]
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

    def get_predicted_values(self):
        # Machine learning
        data = ImagesUtilities.get_histograms()
        #self.k = int(len(data) / 10)
        self.k = self.get_optimal_k(data, True, False)

        print("Optimal K: " + str(self.k))
        k_means = KMeans(n_clusters=self.k)
        model = k_means.fit(data)
        predicted_values = k_means.predict(data)
        self.labels = k_means.labels_

        return predicted_values

    def get_image_class(self, image):
        data = ImagesUtilities.get_histograms()
        searched_data = np.array(ImagesUtilities.get_histogram(image)).reshape(1, -1)

        # Using the KNN algorithm
        knn = KNeighborsClassifier(n_neighbors=3, weights='distance')
        knn.fit(data, self.predicted_values)
        predicted_class = knn.predict(searched_data)

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
