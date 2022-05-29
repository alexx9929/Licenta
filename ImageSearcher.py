from sklearn.cluster import KMeans
from Utilities import MiscFunctions, DataVisualization, ImagesUtilities
import DIContainer, cv2
from matplotlib import pyplot as plt


class ImageSearcher:

    def __init__(self):
        pass

    def search_image(self, path):
        cv_img = cv2.imread(path)
        correlations = self.get_histogram_correlations(cv_img)
        print(correlations)

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

    def get_predicted_values(self):
        # Machine learning
        data = ImagesUtilities.get_channels_means_array()
        k_means = KMeans(n_clusters=10, init='k-means++', max_iter=300, n_init=10, random_state=0)
        model = k_means.fit(data)
        predicted_values = k_means.predict(data)

        # Plotting results
        r, g, b = ImagesUtilities.get_channels_means()
        DataVisualization.ml_color_channels_scatter(r, g, b, predicted_values)
        return predicted_values
