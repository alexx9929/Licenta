from matplotlib import pyplot as plt
from Utilities import MiscFunctions
from ObjectBuilding.Visuals.TextureImage import TextureImage
from Utilities import ImagesUtilities


def image_histogram(image: TextureImage):
    plt.figure()
    plt.plot(image.histograms[0], "r")
    plt.plot(image.histograms[1], "g")
    plt.plot(image.histograms[2], "b")
    plt.show()


def images_histograms():
    for i in MiscFunctions.get_all_texture_images():
        image_histogram(i)


def color_channels_means():
    r, g, b = ImagesUtilities.get_channels_means()
    scatter_plot(r, g, b)


def ml_color_channels_scatter(r_means, g_means, b_means, classes):
    plt.figure()
    ax = plt.axes(projection='3d')
    ax.scatter3D(r_means, g_means, b_means, c=classes, cmap='viridis')
    ax.set_xlabel('R channel mean')
    ax.set_ylabel('G channel mean')
    ax.set_zlabel('B channel mean')
    plt.show()


def scatter_plot(x_data, y_data, z_data):
    plt.figure()
    ax = plt.axes(projection='3d')
    ax.scatter3D(x_data, y_data, z_data, cmap='Greens')
    plt.show()
