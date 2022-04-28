import sys, os, gc

from PySide6.QtWidgets import *
from PySide6.Qt3DExtras import Qt3DExtras
from Scene import Scene
import DIContainer
from GUI.MainWindow import MainWindow

# Set up the application window
app = QApplication(sys.argv)
view = DIContainer.view = Qt3DExtras.Qt3DWindow()
container = DIContainer.window_container = QWidget.createWindowContainer(view)
window = DIContainer.main_window = MainWindow()

scene = DIContainer.scene = Scene()
scene.initialize()

window.load_images_in_scene(window.defaultImageDirectory, 100)
view.setRootEntity(scene)

window.show()

# execute and cleanup
app.exec()
