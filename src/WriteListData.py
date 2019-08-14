"""*******************************************************************************************
* FILE: WriteListData
* PROJECT: AcmeAutomator
* CLASS(s): WriteListData
* MEMBER(s):
* AUTHOR: Christopher L. Robson (UID): 
* DATE: 9/18/18 TIME: 16:17:00
* COPYRIGHT (c): 9/18/18 Christopher L. Robson. All rights reserved.
*                This software is not FREE!  Use or destribution of the software system
*                and its subsystem modules, libraries, configuration file and "seed" file
*                without the express permission of the author is strictly PROHIBITED!
* DESCRIPTION: Common class for writing data to list widgets
*
*******************************************************************************************"""
from PyQt5 import QtCore, QtGui, QtWidgets
"""
LIBRARIES:  Home grown specific libraries
"""
from ManageTabWidgets import ManageTabWidgets
from Capitalization import Capitalization
from BoldType import BoldType
"""
CLASS: WriteListData
METHOD: WriteListData
DESCRIPTION: 
INPUT: 
OUTPUT: 
"""
class WriteListData():
  "Write List Data"
  def __init__(self, parent = None ):
    super(WriteListData, self).__init__()
    self.name = self.__class__.__name__
    self.parent = parent
  """"""
  def message_window_initializer(self, consoleDutTabWidget = None, tab_id = ""):
    self.consoleDutTabWidget = consoleDutTabWidget
    self.tab_id = tab_id
    ManageTabWidgets().create_tab_widget(self.consoleDutTabWidget, self.tab_id)
  """
  Add item to Report window
  """
  def write_list_data(self, list_widget = None, data = None, color = "black", bold = "normal", highlight = True, fontsize = 12, capitalize = "", sorted = False, qtapplication = None):
    if data == None or len(data) == 0:
      return ()
    self.qtapplication = qtapplication
    self.sorted = sorted
    self.list_widget = list_widget
    self.data = data
    self.color = color
    self.bold = bold
    self.capitalize = capitalize
    self.highlight = highlight
    self.fontsize = fontsize
    self.font = QtGui.QFont()
    self.font.setWeight(BoldType().bold_type(self.bold))
    self.font.setPointSize(self.fontsize)
    try:
      for self.line in self.data.split("\n"):
        self.line = Capitalization().capitalize_it(self.line, self.capitalize)
        self.message_item = QtWidgets.QListWidgetItem("{}".format(self.line))
        self.message_item.setForeground(QtGui.QColor(self.color))
        self.message_item.setFont(self.font)
        self.message_item.setSelected(self.highlight)
        self.list_widget.addItem(self.message_item)
        if self.sorted:
          self.list_widget.sortItems(QtCore.Qt.AscendingOrder)
        self.list_widget.scrollToBottom()  # notes Just reminder here that this must be done after every write!
        if qtapplication:
          try:
            """
            This needs to be done so GUI wont lockup during long outputs!
            """
            self.qtapplication.processEvents(QtCore.QEventLoop.AllEvents)
          except Exception as error:
            pass # not critical ignore it also qtapplication may not have been passed
    except Exception as error:
      print("{}: {}".format(self.parent.name, error))
    return (True)
"""*******************************************************************************************
End of WriteListData
*******************************************************************************************"""