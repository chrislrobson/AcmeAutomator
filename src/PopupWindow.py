"""
Module:  Popup Window
Author: Christopher Robson
Copyright by:  Christopher Robson
Copyright date: 01Jan2016
This software is not FREE!  Use or destribution of the software system and its
subsystem modules, libraries, configuration file and "seed" file without the
express permission of the author is strictly PROHIBITED!
Yes I will sue your ass off if you decode, destribute or do ANYTHING without my expressed permission.
This includes any government agency, any company or any employee of those orgainizations.
THIS IS NOT FREE SOFTWARE
FUNCTION: Popup windows
"""
"""
LIBRARIES:  Python libraries
"""
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QMessageBox
"""
LIBRARIES:  Home grown specific libraries
"""
from Capitalization import Capitalization
from BoldType import BoldType
from WriteListData import WriteListData

"""
CLASS: PopupWindowOnly
DESCRIPTION: Displays tab init process
INPUT: Window setup 
OUTPUT: Tab window
"""
class PopupWindow( QWidget):
  "Popup Window"
  def __init__(self, parent = None, data="", title="", weight="normal", capitalize="", fontsize=12, framed=True, corner=550, offset=300, width=1460, height=740, color="#000000"):
    super().__init__()  # notes super() is shorthand for "QtWidgets.QMainWindow.__init__(self) which is saying set this up as main window"
    self.parent = parent
    self.capitalize = capitalize
    self.data = Capitalization().capitalize_it(data, self.capitalize)
    self.title = title
    self.weight = weight
    self.framed = framed
    self.fontsize = fontsize
    self.corner = corner
    self.offset = offset
    self.width = width
    self.height = height
    self.color = color
    self.setStyleSheet("QWidget{\n"
                       "border-style: solid;\n"
                       "border-width: 1px;\n"
                       "}")
    self.setGeometry(QtCore.QRect(self.corner, self.offset, self.width, self.height))
    self.setWindowTitle( title )
    """
    Remove FramelessWindowHint to restore Window min/max/kill
    """
    if not framed:
      self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    self.data_area = QtWidgets.QLabel( self )
    self.data_area.setFrameShape(QtWidgets.QFrame.Box)
    self.data_area.setFrameShadow(QtWidgets.QFrame.Raised)
    self.data_area.setLineWidth(4)
    self.data_area.setObjectName("{}PopupData".format(title))
    self.data_area.resize(self.width, self.height)
    self.data_area.setStyleSheet("QLabel{{\n"
                                 "color:#000000;\n"
                                 "font: {} {}px;\n"
                                 "border-style: groove;\n"
                                 "border-width: 1px;\n"
                                 "border-color: #000000;\n"
                                 "border-radius: 4px;\n"
                                 "padding: 0px;\n"
                                 "margin: 0px;\n"
                                 "background: #FFFFD7;\n"
                                 "}}".format(self.weight, self.fontsize))
    self.data_area.setText(self.data)
    self.show()

"""
CLASS: PopupWindow
DESCRIPTION: Displays tab init process
INPUT: Window setup 
OUTPUT: Tab window
"""
class PopupListWindow( QWidget):
  "Popup List Window"
  def __init__(self, parent = None, title="", weight="normal", capitalize="", fontsize=12, framed=True, corner=550, offset=300, width=1460, height=740, color="#000000"):
    super().__init__()  # notes super() is shorthand for "QtWidgets.QMainWindow.__init__(self) which is saying set this up as main window"
    self.name = self.__class__.__name__
    self.parent = parent
    self.title = title
    self.weight = weight
    self.framed = framed
    self.fontsize = fontsize
    self.capitalize = capitalize
    self.corner = corner
    self.offset = offset
    self.width = width
    self.height = height
    self.color = color
    self.popup_window = QtWidgets.QWidget()
    self.popup_window.setStyleSheet("QWidget{\n"
                                    "border-style: solid;\n"
                                    "border-width: 1px;\n"
                                    "}")
    self.popup_window.setObjectName("popup_window")
    self.popup_window.setGeometry(QtCore.QRect(self.corner, self.offset, self.width, self.height))
    self.popup_window.setWindowTitle( title )
    if not self.framed:
      self.popup_window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    self.gridLayout = QtWidgets.QGridLayout(self.popup_window)
    self.gridLayout.setObjectName("gridLayout")
    self.popup_list_widget = QtWidgets.QListWidget(self.popup_window)
    self.popup_list_widget.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    self.popup_list_widget.setStyleSheet("QListWidget{{\n"
                                         "color:#000000;\n"
                                         "font: {} {}px;\n"
                                         "border-style: groove;\n"
                                         "border-width: 1px;\n"
                                         "border-color: #000000;\n"
                                         "border-radius: 4px;\n"
                                         "padding: 0px;\n"
                                         "margin: 0px;\n"
                                         "background: #FFFFD7;\n"
                                         "}}".format(self.weight, self.fontsize))
    # fixme VERTICAL scroll nNOT WORKING HERE !!!!!!!!!!!!!!!!!!!
    self.popup_list_widget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
    self.popup_list_widget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
    self.popup_list_widget.setObjectName("popup_list_widget")
    self.gridLayout.addWidget(self.popup_list_widget, 0, 0)
    self.popup_window.show()

  def write_popup_message(self, message = "", additional_message = "", detailed_information = "", title = ""):
    self.message = message
    self.additional_message = additional_message
    self.detailed_information = detailed_information
    self.title = title
    if not self.message:
      return
    WriteListData().write_list_data(self.popup_list_widget, data = self.message)
"""
CLASS: ImageDisplay
DESCRIPTION: Decode physical interface received data.
INPUT: class to decode data
OUTPUT: decoded data
"""
class ImageDisplay( QWidget ):
  "ImageDisplay"
  def __init__(self, parent = None, title="", image="", framed=False, corner=550, offset=300, width=1460, height=740, text="Version 0"):
    super().__init__()  # notes super() is shorthand for "QtWidgets.QMainWindow.__init__(self) which is saying set this up as main window"
    self.setGeometry(QtCore.QRect(corner, offset, width, height))
    self.setWindowTitle( title )
    self.parent = parent
    """
    Remove FramelessWindowHint to restore Window min/max/kill
    """
    if not framed:
      self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    self.pictureArea = QtWidgets.QLabel( self )
    self.pictureArea.setFrameShape(QtWidgets.QFrame.Box)
    self.pictureArea.setFrameShadow(QtWidgets.QFrame.Raised)
    self.pictureArea.setLineWidth(4)
    self.pictureArea.setText(text)
    self.size_map_pixmap = QPixmap( image )
    self.pictureArea.setPixmap(self.size_map_pixmap)
    self.pictureArea.resize(self.size_map_pixmap.width(), self.size_map_pixmap.height() + 20)
    self.resize(self.size_map_pixmap.width() + 2, self.size_map_pixmap.height() + 22)
    if not image == "":
      self.pictureArea.setPixmap(QtGui.QPixmap("{}".format( image )))
    self.pictureArea.setObjectName("{}ImageDisplay".format(title))
    self.show()
"""
End of File
"""
