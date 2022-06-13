from ObjectBuilding.Visuals import TextureMaterial, TextureImage
from ObjectBuilding.GameObject import GameObject
import DIContainer
from PySide6.QtCore import QRect, QSize, Qt


class SerializedGameObject:

    def __init__(self):
        # Transform fields
        self.position = None
        self.rotation = None
        self.scale = None

        # Texture image fields
        self.filename = None
        self.image = None
        self.histogram = None
        self.texture_size = None

    def create_object(self):
        obj = GameObject(DIContainer.scene)
        texture_image = self.create_texture_image()
        texture_material = TextureMaterial.TextureMaterial(texture_image)

        obj.add_mesh(DIContainer.default_mesh)
        obj.add_material(texture_material)

        # Adding transform
        obj.transform.setTranslation(self.position)
        obj.transform.setRotation(self.rotation)
        obj.transform.setScale3D(self.scale)

        # Adding object picker
        obj.add_object_picker()
        return obj

    def create_texture_image(self):
        texture_image = TextureImage.TextureImage()
        texture_image.filename = self.filename
        texture_image.image = self.image
        texture_image.histogram = self.histogram
        texture_image.setSize(QSize(self.texture_size, self.texture_size))
        return texture_image
