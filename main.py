import sys
from pathlib import Path

import PySide6.Qt3DExtras
from PySide6.QtQuick import QQuickView
from PySide6.QtCore import QStringListModel, QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.Qt3DExtras import Qt3DExtras
from PySide6.Qt3DCore import Qt3DCore
from Scene import Scene
from PySide6.Qt3DRender import Qt3DRender
from PySide6.QtGui import QVector3D, QQuaternion
import DIContainer
from GameObject import GameObject
import MeshBuilder

# Set up the application window
app = QGuiApplication(sys.argv)
view = Qt3DExtras.Qt3DWindow()

scene = DIContainer.scene = Scene()

for i in range(0, 10):
    e = GameObject()
    e.AddMesh(MeshBuilder.CreateTorusMesh())
    e.AddMaterial(Qt3DExtras.QPhongMaterial())
    e.transform.setTranslation(QVector3D(i * 5, i * 5, -i * 1.5))
    scene.objects.append(e)
    print(e.name)

sceneEntity = scene

# Camera
camera = view.camera()
camera.lens().setPerspectiveProjection(45, 16 / 9, 0.1, 1000)
camera.setPosition(QVector3D(0, 0, 40))
camera.setViewCenter(QVector3D(0, 0, 0))

# Camera controls
camController = Qt3DExtras.QOrbitCameraController(sceneEntity)
camController.setLinearSpeed(50)
camController.setLookSpeed(180)
camController.setCamera(camera)

# Load the QML file
# qml_file = Path(__file__).parent / "view.qml"
# view.setSource(QUrl.fromLocalFile(qml_file.resolve()))


view.setRootEntity(sceneEntity)
view.show()
# execute and cleanup
app.exec()
