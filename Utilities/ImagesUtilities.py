import cv2
import numpy as np
from Utilities import MiscFunctions
import matplotlib.pyplot as plt
from PIL import Image
import PIL.ExifTags
import datetime


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

    # plt.figure()
    for i in range(3):
        channel = img[:, :, i]
        hist = cv2.calcHist([channel], [0], None, [bins], [0, max_val[i]])
        concat_hist.append(hist)
        # plt.plot(hist)

    # plt.show()
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


def get_histogram(cv_img):
    return image_histogram(cv_img, 'HSV', 20)


def swap_channels(channels_array):
    """Used to swap from BGR to RGB"""
    return np.array([channels_array[2], channels_array[1], channels_array[0]])


def get_info_from_object(obj):
    info = {}
    texture_image = obj.get_texture_image()
    img = PIL.Image.open(texture_image.get_full_path())
    info['Name'] = texture_image.filename

    if img._getexif() is not None:
        exif_data = {
            PIL.ExifTags.TAGS[key]: value
            for key, value in img._getexif().items()
            if key in PIL.ExifTags.TAGS
        }

        if exif_data.keys().__contains__('GPSInfo'):
            dd_north = dms_to_dd(exif_data['GPSInfo'][2][0], exif_data['GPSInfo'][2][1],
                                 exif_data['GPSInfo'][2][2])
            dd_east = dms_to_dd(exif_data['GPSInfo'][4][0], exif_data['GPSInfo'][4][1], exif_data['GPSInfo'][4][2])
            info['N'] = dd_north
            info['E'] = dd_east

            above_sea_level = int.from_bytes(exif_data['GPSInfo'][5], 'big') == 1
            alt = exif_data['GPSInfo'][6]

            altitude_string = str(alt) + "m " + "below sea level" if above_sea_level else str(
                alt) + "m " + "above sea level"

            info['Altitude'] = altitude_string

        if exif_data.keys().__contains__("DateTime"):
            string = exif_data["DateTime"]
            split = string.split(" ")
            date = split[0]
            time = split[1]

            date_split = date.split(":")
            date_time_obj = datetime.datetime.strptime(date_split[1], "%m")
            month_name = date_time_obj.strftime("%b")

            formatted_date = date_split[2] + " " + month_name + " " + date_split[0]
            info['Date'] = formatted_date
            info['Time'] = time

    return info


def get_dataset_infos(objs):
    infos = []

    for i in objs:
        infos.append(get_info_from_object(i))

    return infos


def get_coords_from_info(info: dict):
    if info.keys().__contains__('N') and info.keys().__contains__('E'):
        return (info['N'], info['E'])
    else:
        return None


def get_coords(infos: dict):
    all_coords = []
    for i in infos:
        coords = get_coords_from_info(i)
        if coords is not None:
            all_coords.append(coords)

    return all_coords


def dms_to_dd(d, m, s):
    dd = d + float(m) / 60 + float(s) / 3600
    return dd
