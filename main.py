import sys, os, gc
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.Qt3DExtras import Qt3DExtras
from PySide6.QtCore import *
from Scene import Scene
from ObjectBuilding.GameObject import GameObject
from ObjectBuilding.ObjectBuilder import ObjectBuilder
import DIContainer
from ObjectBuilding.Visuals import MeshBuilder, TextureMaterial
from time import perf_counter
from GUI.MainWindow import MainWindow
from ResourcesManagement.ResourcesManager import ResourcesManager


# Set up the application window
app = QApplication(sys.argv)
view = DIContainer.view = Qt3DExtras.Qt3DWindow()
container = DIContainer.window_container = QWidget.createWindowContainer(view)
window = MainWindow()

scene = DIContainer.scene = Scene()
scene.initialize()

view.setRootEntity(scene)

# centering camera
window.center_camera()
window.show()

# execute and cleanup
app.exec()
