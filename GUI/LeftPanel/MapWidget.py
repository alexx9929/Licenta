from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QSizePolicy

import DIContainer
import folium
import numpy as np
import alphashape


class MapWidget(QWebEngineView):

    def __init__(self):
        super().__init__()
        DIContainer.map_widget = self
        self.polygon = []
        self.center = [0, 0]
        self.reset_map()
        pass

    def load_page(self, url):
        self.load(QUrl(url))

    def new_map(self, north: float, east: float, zoom_level=9, add_marker=True):
        if self.polygon is not None and len(self.polygon) > 4:
            folium_map = folium.Map(location=[self.center[0], self.center[1]], tiles='cartodbdark_matter', zoom_start=9)
            folium.Polygon(self.polygon,
                           color="red",
                           weight=2,
                           fill=True,
                           fill_color="white",
                           fill_opacity=0.4).add_to(folium_map)
        else:
            folium_map = folium.Map(location=[north, east], tiles='cartodbdark_matter', zoom_start=zoom_level)

        if add_marker:
            tooltip = "N: " + str(north)[:7] + " E: " + str(east)[:7]
            folium.Marker([north, east], tooltip=tooltip).add_to(folium_map)

        self.setHtml(folium_map.get_root().render())

    def reset_map(self):
        self.new_map(0, 0, 1, False)

    def set_polygon(self, polygon: list):
        self.polygon = polygon
        self.center = [0, 0]
        average_n = 0
        average_e = 0
        count = 0
        for i in self.polygon:
            average_n += i[0]
            average_e += i[1]
            count += 1

        if count > 0:
            self.center[0] = average_n / count
            self.center[1] = average_e / count
        pass