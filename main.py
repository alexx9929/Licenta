import sys, os
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.Qt3DExtras import Qt3DExtras
from PySide6.Qt3DRender import Qt3DRender
from Scene import Scene
from ObjectBuilder.GameObject import GameObject
import DIContainer
from ObjectBuilder.Visuals import MeshBuilder, TextureMaterial
from time import perf_counter

# Set up the application window
app = QGuiApplication(sys.argv)
view = DIContainer.view = Qt3DExtras.Qt3DWindow()
scene = DIContainer.scene = Scene()
scene.initialize()

image_directory = 'C:\\Users\\serba\\Desktop\\test2014'
a = os.listdir(image_directory)

imagesPerRow = 100
offset = 1

tic = perf_counter()
for i in range(0, 10000):
    currentRow = int(i / imagesPerRow)
    currentCol = i % imagesPerRow

    path = os.path.join(image_directory, a[i])
    e = GameObject()
    e.add_mesh(MeshBuilder.create_plane_mesh())
    e.add_material(TextureMaterial.TextureMaterial(path, 512, 512))
    e.transform.setTranslation(QVector3D(currentCol * (10 + offset), -currentRow * (10 + offset), 0))
    e.transform.setRotationX(90)
    scene.objects.append(e)

toc = perf_counter()
print(f"Created {len(scene.objects)} objects in {toc - tic:0.2f} seconds")
view.setRootEntity(scene)
view.show()

# execute and cleanup
app.exec()
