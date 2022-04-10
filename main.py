import sys, os
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.Qt3DExtras import Qt3DExtras
from PySide6.QtCore import *
from Scene import Scene
from ObjectBuilder.GameObject import GameObject
import DIContainer
from ObjectBuilder.Visuals import MeshBuilder, TextureMaterial
from time import perf_counter
from GUI.MainWindow import MainWindow

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
textureSize = 512
imagesPerRow = 10
offset = 1
imageCount = 100

tic = perf_counter()
for i in range(0, imageCount):
    currentRow = int(i / imagesPerRow)
    currentCol = i % imagesPerRow

    path = os.path.join(image_directory, a[i])
    e = GameObject()
    e.add_mesh(MeshBuilder.create_plane_mesh())
    e.add_material(TextureMaterial.TextureMaterial(path, textureSize, textureSize))
    e.transform.setTranslation(QVector3D(currentCol * (planeSize + offset), -currentRow * (planeSize + offset), 0))
    e.transform.setRotationX(90)
    scene.objects.append(e)

toc = perf_counter()
print(f"Created {len(scene.objects)} objects in {toc - tic:0.2f} seconds")
view.setRootEntity(scene)

# centering camera
window.center_camera()
window.show()

# execute and cleanup
app.exec()
