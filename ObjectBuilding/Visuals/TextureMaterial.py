from PySide6.Qt3DExtras import Qt3DExtras
from PySide6.Qt3DRender import Qt3DRender
from ObjectBuilding.Visuals.TextureImage import TextureImage
from memory_profiler import profile


class TextureMaterial(Qt3DExtras.QTextureMaterial):

    def __init__(self, texture_width: int, texture_height: int, image_path=None, image=None):
        super().__init__()
        # Variables
        self._texture = Qt3DRender.QTexture2D()
        self.texture_image = TextureImage(texture_width, texture_height, image_path, image)

        # Adding texture
        self._texture.addTextureImage(self.texture_image)
        self.setTexture(self._texture)
        pass
