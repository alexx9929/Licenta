import sys
from PySide6.QtGui import QGuiApplication
from PySide6.Qt3DExtras import Qt3DExtras
from Scene import Scene
from PySide6.QtGui import QVector3D, QQuaternion
import DIContainer
from GameObject import GameObject
import MeshBuilder

# Set up the application window
app = QGuiApplication(sys.argv)
view = DIContainer.view = Qt3DExtras.Qt3DWindow()
scene = DIContainer.scene = Scene()
scene.initialize()

for i in range(0, 10):
    e = GameObject()
    e.AddMesh(MeshBuilder.create_plane_mesh())
    e.AddMaterial(Qt3DExtras.QPhongMaterial())
    e.transform.setTranslation(QVector3D(i * 5, i * 5, -i * 1.5))
    scene.objects.append(e)

view.setRootEntity(scene)
view.show()

# execute and cleanup
app.exec()
