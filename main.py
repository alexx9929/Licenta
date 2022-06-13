import sys, os, gc, DIContainer
import PySide6
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.Qt3DExtras import Qt3DExtras
from PySide6.QtCore import QObject, QEvent

import GUI.InputHandler
from Scene import Scene
from GUI.MainWindow import MainWindow
from ResourcesManagement import SceneManager, ResourcesManager
from ImageSearcher import ImageSearcher

# Set up the application window
app = DIContainer.app = QApplication(sys.argv)
DIContainer.input_handler = GUI.InputHandler.InputHandler()
view = DIContainer.view = Qt3DExtras.Qt3DWindow()

DIContainer.resources_manager = ResourcesManager.ResourcesManager()
DIContainer.scene_manager = SceneManager.SceneManager()
DIContainer.window_container = QWidget.createWindowContainer(view)
DIContainer.image_searcher = ImageSearcher()
window = DIContainer.main_window = MainWindow()

scene = DIContainer.scene = Scene()
scene.initialize()

view.setRootEntity(scene)

window.show()
window.start_loading_images_in_scene(window.defaultImageDirectory, 1000)

# execute and cleanup
app.exec()
