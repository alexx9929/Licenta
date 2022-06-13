import os, sys
import time

from PySide6.QtGui import *
from time import perf_counter
from Utilities import MiscFunctions
from PySide6.QtCore import QRect, QSize, Qt
from memory_profiler import profile
import numpy as np
import imagesize
from ObjectBuilding.ObjectBuilder import ObjectBuilder
import DIContainer
import threading


class ResourcesManager:

    def __init__(self):
        self.number_of_threads = 4
        self.threads = []
        self.thread_actions = []
        self.create_threads()

        self.directory = None
        self.files = None
        self.positions = None
        self.texture_size = 255
        pass

    def create_threads(self):
        for i in range(0, self.number_of_threads):
            self.thread_actions.append(None)
            self.threads.append(threading.Thread(target=lambda x=i: self.thread_action(x)))
            self.threads[i].start()

    def thread_action(self, action_index: int):
        while True:
            if len(self.thread_actions) > action_index and self.thread_actions[action_index] is not None:
                self.thread_actions[action_index]()

            time.sleep(0)

    def load_images_in_scene(self, count: int, directory: str, files: list, positions: list, texture_size: int):
        self.directory = directory
        self.files = files
        self.positions = positions
        self.texture_size = texture_size

        images_per_thread = int(count / self.number_of_threads)

        for i in range(0, self.number_of_threads):
            start = i * images_per_thread
            end = (i + 1) * images_per_thread - 1

            if count % self.number_of_threads != 0 and i == self.number_of_threads - 1:
                end += count % self.number_of_threads

            self.thread_start_loading_images(lambda x=start, y=end: self.load_batch_of_images(x, y), i)
            #print("Start: " + str(start) + " End: " + str(end))

    def thread_start_loading_images(self, action, thread_index):
        """Overrides action at index for the thread with same index to start the action"""
        self.thread_actions[thread_index] = action

    def load_batch_of_images(self, start_index: int, end_index: int):
        for i in range(start_index, end_index + 1):
            self.load_image_in_scene(self.directory, self.files[i], self.positions[i], self.texture_size)

        self.stop_thread()

    def stop_thread(self):
        for i in range(0, self.number_of_threads):
            if threading.current_thread() == self.threads[i]:
                self.thread_actions[i] = None
                print("Thread " + str(threading.get_ident()) + " finished loading")

    @staticmethod
    def load_image_in_scene(directory: str, file: str, position: QVector3D, texture_size: int):
        path = file
        ratio = 1

        if DIContainer.scene_manager.keep_aspect_ratios:
            full_path = os.path.join(directory, file)
            width, height = imagesize.get(full_path)
            ratio = width / height

        position = position
        rotation = QQuaternion.fromEulerAngles(90, 0, 0)
        scale = QVector3D(ratio, 1, 1)

        ObjectBuilder.create_textured_plane(position, rotation, scale, texture_size, image_path=path)

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
