#10 April 2025
# This is a template and at the same time a demo on how to create a stand alone application
#that loads an existing project from QGIS. It has pan and zoom in, zoom out function.


import os
import sys


from MainWindow import Ui_MainWindow

#QGIS imports
from qgis.PyQt.QtCore import Qt

from qgis.PyQt.QtWidgets import (
    QApplication, QWidget,
    QMainWindow, QFrame,
    QGridLayout, QTextEdit,
    QLabel, QFrame, QLineEdit,
    QAction
    )

from qgis.PyQt.QtGui import *

from qgis.gui import (
    QgsMapCanvas, QgsMapToolPan,
    QgsLayerTreeMapCanvasBridge,
    QgsMapToolZoom)


#from qgis.core import *
from qgis.core import (
    QgsVectorLayer,
    QgsProject,
    QgsApplication,
    QgsRasterLayer, QgsPoint,
    QgsPointXY, QgsCoordinateReferenceSystem,
    qgsRound, QgsRectangle
    
)

from myUtilities import CustomMapTool
#===================================================================#

basedir = os.path.dirname(__file__)
QgsApplication.setPrefixPath("/usr/share/qgis", True)
qgs = QgsApplication([], True)

qgs.initQgis()
path_to_gpkg = basedir + "/data/data.gpkg"


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
        self.actionGetCoords.triggered.connect(self.GetCoordinates)

        #To add it in a toolbar of its own (preferred)        
##        self.toolbar = self.addToolBar("Canvas actions")
##        self.toolbar.addAction(self.actionZoomIn)
##        self.toolbar.addAction(self.actionZoomOut)
##        self.toolbar.addAction(self.actionPan)
        
        #This is how I added it to the MainWindow toolbar.
##        self.toolBar.addAction(self.actionZoomIn)
##        self.toolBar.addAction(self.actionZoomOut)
##        self.toolBar.addAction(self.actionPan)        
        
        # create the map tools
        self.toolPan = QgsMapToolPan(self.map_canvas)
        self.toolPan.setAction(self.actionPan)
        
        self.toolZoomIn = QgsMapToolZoom(self.map_canvas, False) # false = in
        self.toolZoomIn.setAction(self.actionZoomIn)
        self.toolZoomOut = QgsMapToolZoom(self.map_canvas, True) # true = out
        self.toolZoomOut.setAction(self.actionZoomOut)

        self.pan()
        
#===========================================================================#

#==============Load project method========================================#
        self.project = QgsProject.instance()
        self.root = self.project.layerTreeRoot()
        self.basedir = os.path.dirname(__file__) + "/project1.qgz"

        self.map_canvas.setCanvasColor(Qt.white) #I'll opt for this!
        self.map_canvas.enableAntiAliasing(True)

        #setup map tool:
        self.map_tool = CustomMapTool(self.map_canvas) #from myUtilities
        self.map_canvas.setMapTool(self.map_tool)
        self.map_tool.canvasClicked.connect(self.handle_click)

        self.bridge = QgsLayerTreeMapCanvasBridge(self.root, self.map_canvas)
        self.project.read(self.basedir)

        #This is an alternative. Don't delete this...
##        self.map_canvas.setExtent(QgsRectangle(QgsPointXY(117.3, 11.16),QgsPointXY(120.47, 8.15))) #result is the same
##        self.extent = self.map_canvas.extent()
##        self.map_canvas.setExtent(extent)

        self.map_canvas.refreshAllLayers()

        self.pan() #set panning mode on launch

        
#================END LOAD PROJECT==========================================#

        
#=====================Coordinates display stuff=====================#
#NOTE: Be careful not to turn this code on if you are getting the coordinates by left clicking
#       Messes things up!!! Unless you know what you are doing i.e you can make both functions work.

        #Method1 
##        self.lblXY = QLabel()
##        self.lblXY.setFrameStyle( QFrame.Box )
##        self.lblXY.setMinimumWidth( 170 )
##        self.lblXY.setAlignment( Qt.AlignCenter )
##        self.statusbar.setSizeGripEnabled( False )
##        self.statusbar.addPermanentWidget( self.lblXY, 0 )

##        self.lblScale = QLabel()
##        self.lblScale.setFrameStyle( QFrame.StyledPanel )
##        self.lblScale.setMinimumWidth( 140 )
##        self.statusbar.addPermanentWidget( self.lblScale, 0 )
##
##    def mouseMoveEvent(self, event):
##        x, y = self.map_canvas.getCoordinateTransform().toMapCoordinates(event.pos().x(), event.pos().y())
##        #point = QgsPoint(x, y)

##        self.map_canvas.scaleChanged.connect(self.showScale(self.map_canvas.scale()))
##        #self.showXY(point)
##
##    def showXY( self, p ):
##        """ SLOT. Show coordinates """
##        self.lblXY.setText("Long: " + str(qgsRound(p.x(),2)) + " | " + "Lat: "+ str(qgsRound(p.y(),2)) )

##    def showScale( self, scale ):
##        """ SLOT. Show scale """
##        self.lblScale.setText( "Scale 1:" + scale)
        #Should be here?
##        self.map_canvas.scaleChanged.connect(self.showScale(self.map_canvas.scale()))
#==================================================================================================================#
       
        self.map_canvas.setDestinationCrs(QgsCoordinateReferenceSystem("EPSG:4326"))

        
    #panning and zooming methods...
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
        self.actionGetCoords.setChecked(False) #Worked!!!        
        self.map_canvas.setMapTool(self.toolPan)
        
#===========END Method 2=================================================================#

#method to get coordinates on click:
    def GetCoordinates(self):
        self.actionPan.setChecked(False)
        self.map_tool = CustomMapTool(self.map_canvas) #from myUtilities
        self.map_canvas.setMapTool(self.map_tool)
        self.map_tool.canvasClicked.connect(self.handle_click)
        
    def handle_click(self, point, button):
        self.latEdit.setText(str(qgsRound(point.y(),2)))
        self.longEdit.setText(str(qgsRound(point.x(), 2)))



window = MainWindow()
window.show()
qgs.exec()
qgs.exitQgis()
