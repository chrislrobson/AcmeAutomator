"""*******************************************************************************************
* FILE: ManageTabWidgets
* PROJECT: DataCollectionAnalysisReportingAutomation
* CLASS(s): ManageTabWidgets
* MEMBER(s):
* AUTHOR: Christopher L. Robson (UID): 
* DATE: 9/19/18 TIME: 06:20:00
* COPYRIGHT (c): 9/19/18 Christopher L. Robson. All rights reserved.
*                This software is not FREE!  Use or destribution of the software system
*                and its subsystem modules, libraries, configuration file and "seed" file
*                without the express permission of the author is strictly PROHIBITED!
* DESCRIPTION: Manage a new tab wihtin the main GUI,
*              typically the tab title is pulled from the DUT list
*
*******************************************************************************************"""
from PyQt5 import QtCore, QtWidgets
import datetime
"""
CLASS: ManageTabWidgets
METHOD: ManageTabWidgets
DESCRIPTION: 
INPUT: 
OUTPUT: 
"""

class ManageTabWidgets():
  "Manage Tab Widgets"

  def __init__(self, parent = None):
    super(ManageTabWidgets, self).__init__()
    self.name = self.__class__.__name__
    self.parent = parent

  def create_tab_widget(self, tab_widgets, tab_id):
    self.tab_widgets = tab_widgets
    self.tab_id = tab_id
    try:
      return(self.get_tab_list_widget(tab_widgets = self.tab_widgets, tab_id = self.tab_id, list_widget = self.tab_id))
    except:
      self.new_tab = QtWidgets.QWidget()
      self.new_tab.setStyleSheet("QWidget{\n"
                                 "border-style: solid;\n"
                                 "border-width: 1px;\n"
                                 "}")
      self.new_tab.setObjectName(self.tab_id.lstrip().strip())
      self.new_tab_vertical_layout = QtWidgets.QVBoxLayout(self.new_tab)
      self.new_tab_vertical_layout.setObjectName(self.tab_id.lstrip().strip())
      self.new_vertical_layout = QtWidgets.QVBoxLayout()
      self.new_vertical_layout.setObjectName(self.tab_id.lstrip().strip())
      self.new_tab_list_widget = QtWidgets.QListWidget(self.new_tab)
      self.new_tab_list_widget.setStyleSheet("QListWidget{\n"
                                             "color:#000000;\n"
                                             "font: normal 10px;\n"
                                             "border-style: groove;\n"
                                             "border-width: 1px;\n"
                                             "border-color: #000000;\n"
                                             "border-radius: 4px;\n"
                                             "padding: 0px;\n"
                                             "margin: 0px;\n"
                                             "background: #FFFFFF;\n"
                                             "}")
      self.new_tab_list_widget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
      self.new_tab_list_widget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
      self.new_tab_list_widget.setObjectName(self.tab_id.lstrip().strip())
      self.new_vertical_layout.addWidget(self.new_tab_list_widget)
      self.new_tab_vertical_layout.addLayout(self.new_vertical_layout)
      self.tab_widgets.addTab(self.new_tab, "")
      self.tab_widgets.setTabText(self.tab_widgets.indexOf(self.new_tab), QtCore.QCoreApplication.translate("gui_window", self.tab_id))
      return(self.new_tab)

  def set_tab_title(self, tab, tab_id):
    self.tab = tab
    self.tab_id = tab_id
    self.tab_widgets.setTabText(self.tab_widgets.indexOf(self.tab), QtCore.QCoreApplication.translate("gui_window", tab_id))
    return()

  def get_tab_list_widget(self, tab_widgets = None, tab_id = None, list_widget = None):
    self.tab_widgets = tab_widgets
    self.tab_id = tab_id.lstrip().strip()
    self.list_widget = list_widget.lstrip().strip()
    for self.tab_index in range(self.tab_widgets.count()):
      try:
        if self.tab_widgets.tabText(self.tab_index).lstrip().strip() == self.tab_id:
          self.tab_widget = self.tab_widgets.widget(self.tab_index)
          for self.child_widget in self.tab_widget.children():
            if isinstance(self.child_widget, QtWidgets.QListWidget):
              """
              Need to match tab id "and" object name to get correct list window some tabs have multiple list widgets
              """
              if self.list_widget and self.list_widget == self.child_widget.objectName():
                return(self.child_widget, self.tab_index)
              elif not self.list_widget:
                return(self.child_widget, self.tab_index)
              else:
                continue
          break
      except Exception as error:
        raise(error)
    raise Exception("Failed to find ListWidget")

"""*******************************************************************************************
End of ManageTabWidgets
*******************************************************************************************"""