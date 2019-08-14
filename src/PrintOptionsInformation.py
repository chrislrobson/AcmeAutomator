#!/usr/bin/python3
"""*******************************************************************************************
* FILE: PrintOptionsInformation
* PROJECT: DataCollectionAnalysisReportingAutomation
* CLASS(s): PrintOptionsInformation
* MEMBER(s):
* AUTHOR: Christopher L. Robson (UID): 
* DATE: 9/18/18 TIME: 15:40:00
* COPYRIGHT (c): 9/18/18 Christopher L. Robson. All rights reserved.
*                This software is not FREE!  Use or destribution of the software system
*                and its subsystem modules, libraries, configuration file and "seed" file
*                without the express permission of the author is strictly PROHIBITED!
* DESCRIPTION:
*
*******************************************************************************************"""
"""
CLASS: PrintOptionsInformation
METHOD: PrintOptionsInformation
DESCRIPTION: 
INPUT: 
OUTPUT: 
"""


class PrintOptionsInformation():
  "PrintOptionsInformation"

  def __init__(self, parent = None):
    super(PrintOptionsInformation, self).__init__()
    self.name = self.__class__.__name__
    self.parent = parent

  def print_options_information(self, consoleListWidget, profiles = "", profiles_path = "", playbook = "", playbook_path = ""):
    if profiles:
      self.report_message = "Profiles: {}".format(profiles)
    if profiles_path:
      self.report_message = "Profiles directory: {}".format(profiles_path)
    if playbook:
      self.report_message = "Playbook: {}".format(playbook)
    if playbook_path:
      self.report_message = "Playbook directory: {}".format(playbook_path)
    return ()


"""*******************************************************************************************
End of PrintOptionsInformation
*******************************************************************************************"""