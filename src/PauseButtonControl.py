"""*******************************************************************************************
* FILE: PauseSystem
* PROJECT: AcmeAutomtor Data collection analysis reporting automation system
* CLASS(s): PauseSystem
* MEMBER(s):
* AUTHOR: Christopher L. Robson (UID): 
* DATE: 9/17/18 TIME: 12:02:00
* COPYRIGHT (c): 9/17/18 Christopher L. Robson. All rights reserved.
*                This software is not FREE!  Use or destribution of the software system
*                and its subsystem modules, libraries, configuration file and "seed" file
*                without the express permission of the author is strictly PROHIBITED!
* DESCRIPTION:
*
*******************************************************************************************"""
"""
System libraries
"""
import subprocess
from PyQt5 import QtWidgets
"""
Home grown libraries
"""
from Globals import *
"""
CLASS: PaueButtonControl
METHOD: PaueButtonControl
DESCRIPTION: 
INPUT: 
OUTPUT: 
"""
class PauseButtonControl(QtWidgets.QWidget):
  def __init__(self, parent = None):
    super(PauseButtonControl, self).__init__()
    self.name = self.__class__.__name__
    self.parent = parent
    self.parent_name = self.parent.name

  def pause_system(self):
    self.err_str = ""
    try:
      self.output = subprocess.Popen("python3 PauseButtonMain.py", stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
      try:
        self.outputresults, self.err = self.output.communicate()
      except Exception as error:
        self.message = "{{{}{}/{} {}{}}}".format(Globals.RED_MESSAGE, self.parent.name, self.name, error, Globals.SPAN_END_MESSAGE)
        raise Exception(self.message)
      self.results = str(self.outputresults, "utf-8")
      self.err_str = str(self.err, "utf-8")
      if self.err_str != "":
        self.error = self.err_str.replace(":", " ").replace("\n", "")
        self.message = "{{{}{}/{} {}{}}}".format(Globals.RED_MESSAGE, self.parent.name, self.name, self.error, Globals.SPAN_END_MESSAGE)
        raise Exception(self.message)
    except Exception as error:
      if not error.args:
        self.message = "{{{}{}/{} {}{}}}".format(Globals.RED_MESSAGE, self.parent.name, self.name, error, Globals.SPAN_END_MESSAGE)
        raise Exception(self.message)
      else:
        raise Exception(error)
    return ()

"""*******************************************************************************************
End of 
*******************************************************************************************"""