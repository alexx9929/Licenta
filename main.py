import sys
from PySide6.QtGui import *
from PySide6.Qt3DExtras import Qt3DExtras
from PySide6.Qt3DRender import Qt3DRender
from PySide6.QtCore import QRect
from Scene import Scene
from ObjectBuilder.GameObject import GameObject
import DIContainer
from ObjectBuilder.Visuals import MeshBuilder

# Set up the application window
app = QGuiApplication(sys.argv)
view = DIContainer.view = Qt3DExtras.Qt3DWindow()
scene = DIContainer.scene = Scene()
scene.initialize()


class MyTexture(Qt3DRender.QPaintedTextureImage):

    def __init__(self):
        super().__init__()
        self.setWidth(100)
        self.setHeight(100)
        pass

    def paint(self, painter: QPainter):
        url = "creeper.jpg"
        image = QImage(url)
        w = painter.device().width()
        h = painter.device().height()
        painter.drawImage(QRect(0, 0, w, h), image)


def CreateMaterial(obj):
    obj.texture = texture = Qt3DRender.QTexture2D()
    obj.textureImage = textureImage = MyTexture()

    texture.addTextureImage(textureImage)
    material = Qt3DExtras.QTextureMaterial()
    material.setTexture(texture)
    return material


for i in range(0, 1):
    e = GameObject()
    e.add_mesh(MeshBuilder.create_plane_mesh())
    e.add_material(CreateMaterial(e))
    e.transform.setTranslation(QVector3D(i * 5, i * 5, -i * 1.5))
    e.transform.setRotationX(0)
    scene.objects.append(e)


view.setRootEntity(scene)
view.show()

# execute and cleanup
app.exec()
