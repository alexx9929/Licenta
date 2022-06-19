from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QSizePolicy

import DIContainer
import folium


class MapWidget(QWebEngineView):

    def __init__(self):
        super().__init__()
        DIContainer.map_widget = self
        pass

    def load_page(self, url):
        self.load(QUrl(url))

    def new_map(self, north: float, east: float):
        map = folium.Map(location=[north, east],tiles='Stamen Toner')
        folium.Marker([north, east], popup="<i>Mt. Hood Meadows</i>").add_to(map)
        self.setHtml(map.get_root().render())
