from PySide6.QtGui import *
from PySide6.QtCore import QRect, QSize, Qt
from PySide6.Qt3DRender import Qt3DRender
from memory_profiler import profile


class TextureImage(Qt3DRender.QPaintedTextureImage):

    def __init__(self, width: int, height: int, image_path=None, image=None):
        super().__init__()
        # Variables
        self.image_path = image_path
        self.image = QImage(self.image_path) if image_path else image

        # Setting sizes
        self.setWidth(width)
        self.setHeight(height)
        pass

    def paint(self, painter: QPainter):
        w = painter.device().width()
        h = painter.device().height()
        painter.drawImage(QRect(0, 0, w, h), self.image)
