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

objectsCreationTime = []
textureCreationTime = []

t01 = perf_counter()
images = ResourcesManager.load_images(image_directory, 100)
t02 = perf_counter()
print(f"{len(images)} images read in {t02 - t01:0.2f} seconds")

for i in range(0, len(images)):
    currentRow = int(i / window.imagesPerRow)
    currentCol = i % window.imagesPerRow

    xPos = float(currentCol * (planeSize + window.imageOffset))
    yPos = float(-currentRow * (planeSize + window.imageOffset))
    zPos = 0

    position = QVector3D(xPos, yPos, zPos)

    rotation = QQuaternion.fromEulerAngles(90, 0, 0)
    scale = QVector3D(1, 1, 1)

    t11 = perf_counter()
    ObjectBuilder.create_textured_plane(position, rotation, scale, window.textureSize, image=images[i])
    t12 = perf_counter()
    objectsCreationTime.append(t12 - t11)

print(f"Average object creation time: {(sum(objectsCreationTime) / len(objectsCreationTime)) * 1000:0.6f} ms")
t03 = perf_counter()
print(f"{len(images)} objects created in {t03 - t01:0.2f} seconds")

view.setRootEntity(scene)

# centering camera
window.center_camera()
window.show()

# execute and cleanup
app.exec()
