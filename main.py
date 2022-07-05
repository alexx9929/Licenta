import sys, DIContainer
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.Qt3DExtras import Qt3DExtras
from PySide6.Qt3DRender import Qt3DRender

import GUI.InputHandler
from Scene import Scene
from GUI.MainWindow import MainWindow
from ResourcesManagement import SceneManager, ResourcesManager
from ImageSearcher import ImageSearcher
from ObjectBuilding.Visuals import MeshBuilder
import os
from time import perf_counter


app = DIContainer.app = QApplication(sys.argv)
DIContainer.input_handler = GUI.InputHandler.InputHandler()
view = DIContainer.view = Qt3DExtras.Qt3DWindow()
view.renderSettings().pickingSettings().setPickMethod(Qt3DRender.QPickingSettings.PrimitivePicking)

DIContainer.resources_manager = ResourcesManager.ResourcesManager()
DIContainer.scene_manager = SceneManager.SceneManager()
DIContainer.window_container = QWidget.createWindowContainer(view)
DIContainer.image_searcher = ImageSearcher()
window = DIContainer.main_window = MainWindow()

scene = DIContainer.scene = Scene()
Scene.recreate_mesh()
scene.initialize()

view.setRootEntity(scene)

window.show()

# number_of_threads = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
# time_in_seconds = [82.0051377000018, 43.2753260999998, 38.28501310000138, 35.816619099998206, 33.6425049999998, 37.58361409999998,
#         36.814639699998224, 35.52565010000035, 40.26514700000189, 40.96661550000135, 38.051321500002814, 38.82357369999954,
#         39.131365900000674, 37.05955660000109, 37.007576300002256, 38.47854610000286, 35.49107069999809, 37.08883330000026,
#         36.96655799999644, 37.86817780000274, 35.89931579999757, 37.30617609999899, 36.86379400000078]
# manager = DIContainer.resources_manager
# scene_manager = DIContainer.scene_manager
# count = 100
#
# scene_manager.image_count = count
# positions = scene_manager.calculate_all_positions(count)
# files = os.listdir(DIContainer.working_directory)
# manager.load_images_in_scene(count, files, positions)

# from Utilities import ImagesUtilities
# import cv2
#
# img = cv2.imread("C:\\Users\\serba\Desktop\\train2017\\000000000009.jpg")
# hist = ImagesUtilities.get_image_histograms(img)
#
# import matplotlib.pyplot as plt
# plt.figure()
# plt.title("Multithreading performance")
# plt.plot(number_of_threads, time_in_seconds)
# plt.xlabel("Number of threads")
# plt.ylabel("Time [seconds]")
# plt.show()
# execute and cleanup
app.exec()
