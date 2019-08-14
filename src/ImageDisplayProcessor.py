"""
Testbed Tester Welcome
Author: Christopher Robson
Copyright by:  Christopher Robson
Copyright date: 01Jan2016
This software is not FREE!  Use or destribution of the software system and its
subsystem modules, libraries, configuration file and "seed" file without the
express permission of the author is strictly PROHIBITED!
Yes I will sue your ass off if you decode, destribute or do ANYTHING without my expressed permission.
This includes any government agency, any company or any employee of those orgainizations.
THIS IS NOT FREE SOFTWARE
FUNCTION:  Main GUI Welcome Window
"""
"""
LIBRARIES:  Python libraries
"""
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QTextCursor, QFont, QPalette, QColor, QBrush, QPen
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
"""
LIBRARIES:  Testbed Tester specific libraries
"""
"""
CLASS: ImageDisplayWindow
DESCRIPTION: Displays various images to dedicated detached windows
INPUT: Window setup values
OUTPUT: Detached window is displayed
FIXME Not enough colors supported if this is used so keep for historical reasons
   QPalette() METHOD:
     ImageDisplayWindow.setAutoFillBackground(True)
     self.palette = QPalette()
     self.palette.setColor(ImageDisplayWindow.backgroundRole(), Qt.yellow)
     ImageDisplayWindow.setPalette(self.palette)
"""
class ImageDisplayProcessor(object):
  "Image Display Processor"
  def __init__(self):
    super().__init__()
    self.name = self.__class__.__name__
  """"""
  def image_display(self,
                    ImageDisplayWindow,
                    text_color = "black",
                    parent_background_color = "000000",
                    child_background_color = "#ffffff",
                    title = "Testbed Tester",
                    font = "bold 12pt",
                    left = 0,
                    top = 0,
                    width = 1000,
                    height = 700,
                    background_image = ""
                    ):
    self.parent_backgound_color_styles = \
      "font: {}; background-color: {}; border-color: black;".format(font, parent_background_color)
    self.child_backgound_color_styles = \
      "font: {}; background-color: {}; border-color: black;".format(font, child_background_color)
    ImageDisplayWindow.setObjectName("ImageDisplayWindow")
    ImageDisplayWindow.move(left, top)
    ImageDisplayWindow.resize(width, height)
    ImageDisplayWindow.setWindowTitle(title)
    ImageDisplayWindow.setStyleSheet(self.parent_backgound_color_styles)
    self.centralWidget = QtWidgets.QWidget(ImageDisplayWindow)
    self.centralWidget.setObjectName("centralWidget")
    self.gridLayout = QtWidgets.QGridLayout(self.centralWidget)
    self.gridLayout.setObjectName("gridLayout")
    self.listWidget = QtWidgets.QListWidget(self.centralWidget)
    self.listWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
    self.listWidget.setAutoScroll(True)
    self.listWidget.setObjectName("listWidget")
    self.listWidget.scrollToBottom()  # Just remonder here that this must be done after every write!
    self.listWidget.setStyleSheet(self.child_backgound_color_styles)
    self.gridLayout.addWidget(self.listWidget, 0, 0, 1, 1)
    if background_image:
      self.pictureArea = QtWidgets.QLabel( self.centralWidget )
      self.pictureArea.setFrameShape(QtWidgets.QFrame.Box)
      self.pictureArea.setFrameShadow(QtWidgets.QFrame.Raised)
      self.pictureArea.setLineWidth(4)
      self.isis_map_pixmap = QPixmap( background_image )
      self.pictureArea.setPixmap(self.isis_map_pixmap)
      self.pictureArea.resize(self.isis_map_pixmap.width(), self.isis_map_pixmap.height())
      ImageDisplayWindow.resize(self.isis_map_pixmap.width(), self.isis_map_pixmap.height())
      self.pictureArea.setObjectName("pictureArea")
    ImageDisplayWindow.setCentralWidget(self.centralWidget)
    QtCore.QMetaObject.connectSlotsByName(ImageDisplayWindow)
    ImageDisplayWindow.show()
"""
End of File
"""
