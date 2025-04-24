#from PyQt5.QtCore import Qt, pyqtSignal
from qgis.PyQt.QtCore import Qt, pyqtSignal
from qgis.gui import (
    QgsMapCanvas, QgsMapToolEmitPoint,
    QgsMapToolPan, QgsMapToolZoom
    )

#ORIGINAL
class CustomMapTool(QgsMapToolEmitPoint):
    canvasClicked = pyqtSignal(object, object)

    def canvasPressEvent(self, event):
        point = self.toMapCoordinates(event.pos())
        self.canvasClicked.emit(point, event.button())
        super(CustomMapTool, self).canvasPressEvent(event)


