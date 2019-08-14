"""*******************************************************************************************
* FILE: EnableDisableButtons
* PROJECT: AcmeAutomtor Data collection analysis reporting automation system
* CLASS(s): EnableDisableButtons
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
"""
Home grown libraries
"""
"""
CLASS: EnableDisableButtons
METHOD: EnableDisableButtons
DESCRIPTION: 
INPUT: 
OUTPUT: 
"""
class EnableDisableButtons():
  def __init__(self, parent = None):
    super(EnableDisableButtons, self).__init__()
    self.name = self.__class__.__name__
    self.parent = parent

  def EnableDisableButtons(self, button, state = False, color = "#000000", stylesheet = None):
    self.button = button
    self.state = state
    self.color = color
    self.stylesheet = stylesheet
    if stylesheet:
      self.button.setStyleSheet(self.stylesheet)
    else:
      if not color.startswith("#") or len(color) < 7:
        self.color = "#000000"
      if state:
        self.button.setStyleSheet("QPushButton{{\n"
                                  "color:{};\n"
                                  "font: bold 24px;\n"
                                  "font-style: normal;\n"
                                  "font-family: Times New Roman;\n"
                                  "border-style: solid;\n"
                                  "border-width: 1px;\n"
                                  "border-color: #008000;\n"
                                  "border-radius: 6px;\n"
                                  "padding: 4px;\n"
                                  "margin: 6px;\n"
                                  "background: #FFFFFF;\n"
                                  "}}".format(self.color))
      else:
        self.button.setStyleSheet("QPushButton{\n"
                                  "color:#6C6C6C;\n"
                                  "font: bold 12px;\n"
                                  "font-style: normal;\n"
                                  "font-family: Times New Roman;\n"
                                  "border-style: solid;\n"
                                  "border-width: 1px;\n"
                                  "border-color: #4E4E4E;\n"
                                  "border-radius: 6px;\n"
                                  "padding: 2px;\n"
                                  "margin: 6px;\n"
                                  "background: #FFFFFF;\n"
                                  "}")
    self.button.setEnabled(state)
    return ()

"""*******************************************************************************************
End of EnableDisableButtons
*******************************************************************************************"""