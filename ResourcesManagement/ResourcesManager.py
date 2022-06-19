import os, sys
import time

from PySide6.QtGui import *
from Utilities import MiscFunctions
from PySide6.QtCore import QRect, QSize, Qt, QObject, Signal, QTimer
from memory_profiler import profile
import numpy as np
import imagesize
from ObjectBuilding.ObjectBuilder import ObjectBuilder
import DIContainer
import threading, queue
from ObjectBuilding.SerializedGameObject import SerializedGameObject
import cv2
from Utilities import ImagesUtilities


class ResourcesManager(QObject):

    def __init__(self):
        super().__init__()
        self.number_of_threads = 10
        self.threads = []
        self.thread_actions = []

        self.create_threads()
        self.queue = queue.Queue()

        self.directory = None
        self.files = None
        self.positions = None
        pass

    def on_object_serialized(self, obj):
        self.deserialize_object(obj)

    # region Default thread methods
    def create_threads(self):
        for i in range(0, self.number_of_threads):
            self.thread_actions.append(None)
            self.threads.append(threading.Thread(target=lambda x=i: self.thread_loop(x)))
            self.threads[i].start()

    def thread_loop(self, action_index: int):
        while True:
            if len(self.thread_actions) > action_index and self.thread_actions[action_index] is not None:
                self.thread_actions[action_index]()

            time.sleep(0)

    def stop_thread(self):
        for i in range(0, self.number_of_threads):
            if threading.current_thread() == self.threads[i]:
                self.thread_actions[i] = None
                print("Thread " + str(threading.get_ident()) + " finished loading")

    # endregion

    def thread_start_classification(self, thread_index):
        self.thread_actions[thread_index] = self.start_classification

    # region Multithreading top-level actions
    def start_classification(self):
        DIContainer.image_searcher.start_classification(True)
        DIContainer.post_load_widget.enable_group_clusters_button(True)
        self.stop_thread()

    def load_images_in_scene(self, count: int, files: list, positions: list):
        """Will assign equal amounts of image data to load for every available thread and will start loading"""
        self.files = files
        self.positions = positions

        images_per_thread = int(count / self.number_of_threads)

        # Dividing the data and assigning it to every available thread and starting the loop
        for i in range(0, self.number_of_threads):
            start = i * images_per_thread
            end = (i + 1) * images_per_thread - 1

            if count % self.number_of_threads != 0 and i == self.number_of_threads - 1:
                end += count % self.number_of_threads

            self.thread_start_loading_images(lambda x=start, y=end: self.load_batch_of_images(x, y), i)

        # Creating objects from the loaded data
        self.process_queue(lambda x=count: self.objects_not_loaded(x), self.deserialize_queue_item)

        DIContainer.post_load_widget.enable_group_clusters_button(False)
        DIContainer.post_load_widget.enable_search_button(False)
        DIContainer.post_load_widget.enable_classification_button(True)

    # endregion

    # region Queue processing
    @staticmethod
    def process_queue(condition, process_method):
        """While condition is true, process_method will be called"""
        while condition():
            process_method()

    def deserialize_queue_item(self):
        """Pops a serialized object from the queue and creates an object from it"""
        serialized_object = self.queue.get()
        obj = serialized_object.create_object()
        DIContainer.scene.objects.append(obj)
        obj.material.texture_image.setSize(QSize(DIContainer.texture_size, DIContainer.texture_size))

    def deserialize_object(self, serialized_object):
        obj = serialized_object.create_object()
        DIContainer.scene.objects.append(obj)
        obj.material.texture_image.setSize(QSize(DIContainer.texture_size, DIContainer.texture_size))

    @staticmethod
    def objects_not_loaded(count):
        return len(DIContainer.scene.objects) != count

    # endregion

    # region Loading images thread methods
    def thread_start_loading_images(self, action, thread_index):
        """Overrides action at index for the thread with same index to start the action"""
        self.thread_actions[thread_index] = action

    def load_batch_of_images(self, start_index: int, end_index: int):
        """Function used by worker threads to read images and generate info"""
        for i in range(start_index, end_index + 1):
            self.generate_object_info(self.files[i], self.positions[i])
        self.stop_thread()

    def generate_object_info(self, file: str, position: QVector3D):
        """Calculates the necessary data to create an object and puts it in the queue
        so that the main thread can create it"""
        ratio = 1
        full_path = os.path.join(DIContainer.working_directory, file)

        if DIContainer.scene_manager.keep_aspect_ratios:
            width, height = imagesize.get(full_path)
            ratio = width / height

        # Creating serialized object and transform parameters
        serialized_object = SerializedGameObject()
        serialized_object.filename = file
        serialized_object.position = position
        serialized_object.rotation = QQuaternion.fromEulerAngles(90, 0, 0)
        serialized_object.scale = QVector3D(ratio, 1, 1)

        # Creating image parameters
        serialized_object.texture_size = DIContainer.texture_size
        self.calculate_image(full_path, serialized_object)
       # self.object_serialized.emit(serialized_object)

        self.queue.put(serialized_object)

    @staticmethod
    def calculate_image(path, obj):
        """Reads an image and calculates the histogram in order to create the object"""
        # Loading image with cv2
        cv_img = cv2.imread(path)
        height, width, channel = cv_img.shape
        bytes_per_line = 3 * width
        histogram = ImagesUtilities.image_histogram(cv_img, 'HSV', 20)

        # Creating a QImage from the cv2 image
        image = QImage(cv_img.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped().scaled(
            QSize(DIContainer.texture_size, DIContainer.texture_size), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        # channels_means = cv2.mean(cv_img)[:3]
        obj.image = image
        obj.histogram = histogram

    # endregion

    @staticmethod
    def load_image(path: str, image_size=0):
        if image_size > 0:
            return QImage(path).scaled(QSize(image_size, image_size), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        else:
            return QImage(path)

    @staticmethod
    def load_images(directory: str, count: int, image_size: int):
        files = os.listdir(directory)
        images = []
        for i in range(0, count):
            path = os.path.join(directory, files[i])
            images.append(
                QImage(path).scaled(QSize(image_size, image_size), Qt.IgnoreAspectRatio, Qt.SmoothTransformation))

        return images

    @staticmethod
    def get_ratios(directory: str, files, count: int):
        """This method will return a dictionary that contains the ratios of the images
         and the count for each ratio"""

        ratios = {}

        for i in range(0, count):
            path = os.path.join(directory, files[i])
            width, height = imagesize.get(path)
            ratio = width / height
            ratio_str = str(ratio)[:3]
            if ratio_str in ratios.keys():
                ratios[ratio_str] += 1
            else:
                ratios[ratio_str] = 1

        return ratios
