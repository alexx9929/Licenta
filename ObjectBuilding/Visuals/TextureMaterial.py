from PySide6.Qt3DExtras import Qt3DExtras
from PySide6.Qt3DRender import Qt3DRender
from ObjectBuilding.Visuals.TextureImage import TextureImage


class TextureMaterial(Qt3DExtras.QTextureMaterial):

    def __init__(self, texture_image: TextureImage):
        super().__init__()
        # Variables
        self._texture = Qt3DRender.QTexture2D()
        self.texture_image = texture_image

        # Adding texture
        self._texture.addTextureImage(self.texture_image)
        self.setTexture(self._texture)
        pass
