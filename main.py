import sys, os, gc, DIContainer
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.Qt3DExtras import Qt3DExtras
from Scene import Scene
from GUI.MainWindow import MainWindow
from ResourcesManagement import SceneManager

# Set up the application window
app = QApplication(sys.argv)
view = DIContainer.view = Qt3DExtras.Qt3DWindow()
scene_manager = DIContainer.scene_manager = SceneManager.SceneManager()
container = DIContainer.window_container = QWidget.createWindowContainer(view)
window = DIContainer.main_window = MainWindow()

scene = DIContainer.scene = Scene()
scene.initialize()

view.setRootEntity(scene)

window.show()
window.load_images_in_scene(window.defaultImageDirectory, 100)

# execute and cleanup
app.exec()
