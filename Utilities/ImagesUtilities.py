import cv2
import numpy as np
from Utilities import MiscFunctions


def image_histogram(img, color_space, bins):
    if color_space == 'HSV':
        code = cv2.COLOR_BGR2HSV
        max_val = [360, 1, 256]
    else:
        if color_space == 'RGB':
            code = cv2.COLOR_BGR2RGB
            max_val = [256, 256, 256]
        else:
            print('Invalid colorspace')
            return

    img = cv2.cvtColor(img, code=code)
    concat_hist = []

    for i in range(3):
        channel = img[:, :, i]
        hist = cv2.calcHist([channel], [0], None, [bins], [0, max_val[i]])
        concat_hist.append(hist)

    return np.array(concat_hist).flatten()


def get_image_histograms(image):
    """Will return R,G,B histograms"""
    # Define colors to plot the histograms
    colors = ('b', 'g', 'r')
    histograms = []

    # Compute the image histograms and channel means
    for i, color in enumerate(colors):
        hist = cv2.calcHist([image], [i], None, [256], [0, 256])
        flat = hist.flatten()
        histograms.append(flat)

    return [histograms[2], histograms[1], histograms[0]]


def get_channels_means():
    r_mean = []
    g_mean = []
    b_mean = []

    for i in MiscFunctions.get_all_texture_images():
        r_mean.append(i.channels_means[2])
        g_mean.append(i.channels_means[1])
        b_mean.append(i.channels_means[0])

    return r_mean, g_mean, b_mean


def get_channels_means_array():
    array = []
    for i in MiscFunctions.get_all_texture_images():
        array.append([i.channels_means[2], i.channels_means[1], i.channels_means[0]])
    return array


def get_histograms():
    array = []
    for i in MiscFunctions.get_all_texture_images():
        array.append(i.histogram)

    return array


def swap_channels(channels_array):
    """Used to swap from BGR to RGB"""
    return np.array([channels_array[2], channels_array[1], channels_array[0]])
