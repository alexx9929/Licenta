from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QSizePolicy

import DIContainer
import folium


class MapWidget(QWebEngineView):

    def __init__(self):
        super().__init__()
        DIContainer.map_widget = self
        self.new_map(0, 0, 1, False)
        pass

    def load_page(self, url):
        self.load(QUrl(url))

    def new_map(self, north: float, east: float, zoom_level=9, add_marker=True):
        folium_map = folium.Map(location=[north, east], tiles='cartodbdark_matter', zoom_start=zoom_level)

        if add_marker:
            tooltip = "N: " + str(north)[:7] + " E: " + str(east)[:7]
            folium.Marker([north, east], tooltip=tooltip).add_to(folium_map)
        self.setHtml(folium_map.get_root().render())
