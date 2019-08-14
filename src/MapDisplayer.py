"""
METHOD:  MapDisplay
This program runs as a stand alone  network map displayer
"""
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import time
#-------------------------------------------------------------------------------------------------------------------
class IsisMap( QWidget ):
  def __init__( self ):
    super().__init__()
    self.name = self.__class__.__name__
    self.isis_map = QWidget( self )
    self.isis_map.setWindowTitle( "Testbed Automator Lab Topology Mapper" )
    self.pictureArea = QLabel( self.isis_map )
    self.pictureArea.setFrameShape(QtWidgets.QFrame.Box)
    self.pictureArea.setFrameShadow(QtWidgets.QFrame.Raised)
    self.pictureArea.setLineWidth(2)
    self.isis_map_pixmap = QPixmap( "./.AcmeAutomator/myARCHIVES/NETWORK-MAP/Testbed-Tester-ISIS-Map.png" )
    self.pictureArea.setPixmap(self.isis_map_pixmap)
    self.pictureArea.resize(self.isis_map_pixmap.width(), self.isis_map_pixmap.height())
    self.isis_map.resize(self.isis_map_pixmap.width(), self.isis_map_pixmap.height())
    self.pictureArea.setObjectName( "pictureArea" )
    self.isis_map.show()
"""
End of File
"""
