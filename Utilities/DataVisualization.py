from matplotlib import pyplot as plt
from Utilities import MiscFunctions
from ObjectBuilding.Visuals.TextureImage import TextureImage

# def show_image_contrast_histogram():
#     plt.figure()
#     plt.title('Color distribution ' + self.filename)
#     plt.plot(self.cumulative_histogram[0], color='b')
#     plt.plot(self.cumulative_histogram[1], color='g')
#     plt.plot(self.cumulative_histogram[2], color='r')
#     plt.title('Intensities ' + self.filename)
#     plt.show()


def image_histogram(image: TextureImage):
    plt.figure()
    plt.plot(image.histogram[0], "b")
    plt.plot(image.histogram[1], "g")
    plt.plot(image.histogram[2], "r")
    plt.show()


def images_histograms():
    for i in MiscFunctions.get_all_texture_images():
        image_histogram(i)


def color_channels_means():
    b_mean = []
    r_mean = []
    g_mean = []

    for i in MiscFunctions.get_all_texture_images():
        b_mean.append(i.channel_means[0])
        g_mean.append(i.channel_means[1])
        r_mean.append(i.channel_means[2])

    scatter_plot(r_mean, b_mean, g_mean)


def scatter_plot(x_data, y_data, z_data):
    plt.figure()
    ax = plt.axes(projection='3d')
    ax.scatter3D(x_data, y_data, z_data, cmap='Greens')
    plt.show()

