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

# execute and cleanup
app.exec()
