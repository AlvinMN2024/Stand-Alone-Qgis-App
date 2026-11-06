"""Standalone PyQGIS map viewer example for QGIS 4.x / Qt 6."""

import os
import sys
from pathlib import Path

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QMainWindow
from qgis.core import QgsApplication, QgsCoordinateReferenceSystem, QgsProject, qgsRound
from qgis.gui import QgsLayerTreeMapCanvasBridge, QgsMapToolPan, QgsMapToolZoom

from MainWindow import Ui_MainWindow
from myUtilities import CustomMapTool


APP_DIR = Path(__file__).resolve().parent
PROJECT_PATH = APP_DIR / "project1.qgz"

# Override this when QGIS is installed outside the usual Linux prefix.
QGIS_PREFIX = os.environ.get("QGIS_PREFIX_PATH", "/usr")
QgsApplication.setPrefixPath(QGIS_PREFIX, True)
qgis_argv = [os.fsencode(arg) for arg in sys.argv]
app = QgsApplication(qgis_argv, True)
app.initQgis()


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.actionClose.triggered.connect(self.close)
        self.actionSubmit.setStatusTip("Submit request")

        self.actionZoomIn.setCheckable(True)
        self.actionZoomOut.setCheckable(True)
        self.actionPan.setCheckable(True)
        self.actionGetCoords.setCheckable(True)
        self.actionZoomIn.triggered.connect(self.zoomIn)
        self.actionZoomOut.triggered.connect(self.zoomOut)
        self.actionPan.triggered.connect(self.pan)
        self.actionGetCoords.triggered.connect(self.getCoordinates)

        self.map_canvas.setCanvasColor(Qt.GlobalColor.white)
        self.map_canvas.enableAntiAliasing(True)

        self.project = QgsProject.instance()
        self.bridge = QgsLayerTreeMapCanvasBridge(
            self.project.layerTreeRoot(), self.map_canvas
        )
        if not self.project.read(str(PROJECT_PATH)):
            raise RuntimeError(f"Could not read QGIS project: {PROJECT_PATH}")
        self.map_canvas.setDestinationCrs(QgsCoordinateReferenceSystem("EPSG:4326"))
        self.map_canvas.refreshAllLayers()

        self.toolPan = QgsMapToolPan(self.map_canvas)
        self.toolZoomIn = QgsMapToolZoom(self.map_canvas, False)
        self.toolZoomOut = QgsMapToolZoom(self.map_canvas, True)
        self.toolPan.setAction(self.actionPan)
        self.toolZoomIn.setAction(self.actionZoomIn)
        self.toolZoomOut.setAction(self.actionZoomOut)

        self.map_tool = CustomMapTool(self.map_canvas)
        self.map_tool.canvasClicked.connect(self.handle_click)
        self.pan()

    def zoomIn(self):
        self.actionGetCoords.setChecked(False)
        self.actionPan.setChecked(False)
        self.actionZoomOut.setChecked(False)
        self.map_canvas.setMapTool(self.toolZoomIn)

    def zoomOut(self):
        self.actionGetCoords.setChecked(False)
        self.actionZoomIn.setChecked(False)
        self.actionPan.setChecked(False)
        self.map_canvas.setMapTool(self.toolZoomOut)

    def pan(self):
        self.actionZoomIn.setChecked(False)
        self.actionZoomOut.setChecked(False)
        self.actionGetCoords.setChecked(False)
        self.map_canvas.setMapTool(self.toolPan)

    def getCoordinates(self):
        self.actionPan.setChecked(False)
        self.actionZoomIn.setChecked(False)
        self.actionZoomOut.setChecked(False)
        self.map_canvas.setMapTool(self.map_tool)

    def handle_click(self, point, _button):
        self.latEdit.setText(str(qgsRound(point.y(), 2)))
        self.longEdit.setText(str(qgsRound(point.x(), 2)))


window = MainWindow()
window.show()
exit_code = app.exec()
app.exitQgis()
sys.exit(exit_code)
