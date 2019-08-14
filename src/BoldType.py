#!/usr/bin/python3
"""*******************************************************************************************
* FILE: BoldType
* PROJECT: DataCollectionAnalysisReportingAutomation
* CLASS(s): BoldType
* MEMBER(s):
* AUTHOR: Christopher L. Robson (UID): 
* DATE: 9/18/18 TIME: 08:32:00
* COPYRIGHT (c): 9/18/18 Christopher L. Robson. All rights reserved.
*                This software is not FREE!  Use or destribution of the software system
*                and its subsystem modules, libraries, configuration file and "seed" file
*                without the express permission of the author is strictly PROHIBITED!
* DESCRIPTION:
*
*******************************************************************************************"""
from PyQt5 import QtGui
"""
CLASS: BoldType
METHOD: BoldType
DESCRIPTION: 
INPUT: 
OUTPUT: 
"""

class BoldType():
  "BoldType"

  def __init__(self, parent = None):
    super(BoldType, self).__init__()
    self.name = self.__class__.__name__
    self.parent = parent

  """
  Weigth, aka bold types
  """
  def bold_type(self, bold = "normal"):
    bold_type = {
      "extralight": QtGui.QFont.ExtraLight,
      "light": QtGui.QFont.Light,
      "normal": QtGui.QFont.Normal,
      "demibold": QtGui.QFont.DemiBold,
      "bold": QtGui.QFont.Bold,
      "extrabold": QtGui.QFont.ExtraBold,
    }
    return (bold_type[bold])

"""*******************************************************************************************
End of BoldType
*******************************************************************************************"""