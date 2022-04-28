from PySide6.QtGui import QImage, QPainter
from PySide6.QtCore import QRect
from PySide6.Qt3DRender import Qt3DRender
import os

import DIContainer


class TextureImage(Qt3DRender.QPaintedTextureImage):

    def __init__(self, width: int, height: int, image_path=None):
        super().__init__()
        # Variables
        self.filename = image_path

        # Setting sizes
        self.setWidth(width)
        self.setHeight(height)
        pass

    def paint(self, painter: QPainter):
        if not self.filename:
            return

        painter.drawImage(QRect(0, 0, self.width(), self.height()),
                          QImage(os.path.join(DIContainer.main_window.defaultImageDirectory, self.filename)))
