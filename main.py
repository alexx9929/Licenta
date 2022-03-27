import sys
from PySide6.QtGui import *
from PySide6.Qt3DExtras import Qt3DExtras
from PySide6.Qt3DRender import Qt3DRender
from Scene import Scene
from ObjectBuilder.GameObject import GameObject
import DIContainer
from ObjectBuilder.Visuals import MeshBuilder, TextureMaterial

# Set up the application window
app = QGuiApplication(sys.argv)
view = DIContainer.view = Qt3DExtras.Qt3DWindow()
scene = DIContainer.scene = Scene()
scene.initialize()

for i in range(0, 10):
    e = GameObject()
    e.add_mesh(MeshBuilder.create_plane_mesh())
    e.add_material(TextureMaterial.TextureMaterial('creeper.jpg', 100, 100))
    e.transform.setTranslation(QVector3D(i * 5, i * 5, -i * 1.5))
    e.transform.setRotationX(45)
    scene.objects.append(e)

view.setRootEntity(scene)
view.show()

# execute and cleanup
app.exec()
