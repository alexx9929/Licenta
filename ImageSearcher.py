from sklearn.cluster import KMeans
from Utilities import MiscFunctions, DataVisualization
import DIContainer


class ImageSearcher:

    def __init__(self):
        pass

    def get_predicted_values(self):
        # Machine learning
        data = MiscFunctions.get_channels_means_array()
        k_means = KMeans(n_clusters=10, init='k-means++', max_iter=300, n_init=10, random_state=0)
        model = k_means.fit(data)
        predicted_values = k_means.predict(data)

        # Plotting results
        r, g, b = MiscFunctions.get_channels_means()
        DataVisualization.ml_color_channels_scatter(r, g, b, predicted_values)
        return predicted_values
