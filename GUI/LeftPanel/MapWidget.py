from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QSizePolicy

import DIContainer


class MapWidget(QWebEngineView):

    def __init__(self):
        super().__init__()
        DIContainer.map_widget = self
        self.load_page("https://maps.google.com")
        pass

    def load_page(self, url):
        self.load(QUrl(url))
