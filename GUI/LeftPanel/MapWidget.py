from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl


class MapWidget(QWebEngineView):

    def __init__(self):
        super().__init__()
        self.load_page("https://maps.google.com")
        pass

    def load_page(self, url):
        self.load(QUrl(url))
