import sys, os
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

window = MainWindow()
container = DIContainer.container = QWidget.createWindowContainer(view)
window.layout.addWidget(container)

scene = DIContainer.scene = Scene()
scene.initialize()

image_directory = 'C:\\Users\\serba\\Desktop\\test2014'
a = os.listdir(image_directory)

planeSize = GameObject.__DEFAULT__PLANE_LENGTH__()
window.imageCount = imageCount = 100

tic = perf_counter()
objectsCreationTime = []
textureCreationTime = []

images = ResourcesManager.load_images(image_directory, 100)

for i in range(0, len(images)):
    currentRow = int(i / window.imagesPerRow)
    currentCol = i % window.imagesPerRow

    xPos = float(currentCol * (planeSize + window.imageOffset))
    yPos = float(-currentRow * (planeSize + window.imageOffset))
    zPos = 0

    position = QVector3D(xPos, yPos, zPos)

    rotation = QQuaternion.fromEulerAngles(90, 0, 0)
    scale = QVector3D(1, 1, 1)
    ObjectBuilder.create_textured_plane(position, rotation, scale, window.textureSize, image=images[i])
# for i in range(0, imageCount):
#     t1 = perf_counter()
#     currentRow = int(i / window.imagesPerRow)
#     currentCol = i % window.imagesPerRow
#
#     path = os.path.join(image_directory, a[i])
#     e = GameObject()
#     e.add_mesh(MeshBuilder.create_plane_mesh())
#
#     t11 = perf_counter()
#     e.add_material(TextureMaterial.TextureMaterial(path, window.textureSize, window.textureSize))
#     t12 = perf_counter()
#     textureCreationTime.append(t12 - t11)
#
#     e.transform.setTranslation(QVector3D(currentCol * (planeSize + window.imageOffset), -currentRow * (planeSize + window.imageOffset), 0))
#     e.transform.setRotationX(90)
#     scene.objects.append(e)
#     t2 = perf_counter()
#     objectsCreationTime.append(t2 - t1)

toc = perf_counter()
print(f"Created {len(scene.objects)} objects in {toc - tic:0.2f} seconds")
# print(f"Average object creation time: {(sum(objectsCreationTime) / len(objectsCreationTime)) * 1000:0.6f} ms")
# print(f"Average texture creation time: {(sum(textureCreationTime) / len(textureCreationTime)) * 1000:0.6f} ms")

view.setRootEntity(scene)

# centering camera
window.center_camera()
window.show()

# execute and cleanup
app.exec()
