#!/usr/bin/python3
"""*******************************************************************************************
* FILE: Capitalization
* PROJECT: DataCollectionAnalysisReportingAutomation
* CLASS(s): Capitalization
* MEMBER(s):
* AUTHOR: Christopher L. Robson (UID): 
* DATE: 9/18/18 TIME: 08:30:00
* COPYRIGHT (c): 9/18/18 Christopher L. Robson. All rights reserved.
*                This software is not FREE!  Use or destribution of the software system
*                and its subsystem modules, libraries, configuration file and "seed" file
*                without the express permission of the author is strictly PROHIBITED!
* DESCRIPTION:
*
*******************************************************************************************"""
"""
CLASS: Capitalization
METHOD: Capitalization
DESCRIPTION: 
INPUT: 
OUTPUT: 
"""


class Capitalization():
  "Capitalization"

  def __init__(self, parent = None):
    super(Capitalization, self).__init__()
    self.name = self.__class__.__name__
    self.parent = parent

  """
  Capitalization
  """
  def capitalize_it(self, data, capitalize = "lower"):
    capitalize_it = {
      "": "{}".format(data),
      "lower": "{}".format(data).lower(),
      "upper": "{}".format(data).upper(),
      "capitalize": "{}".format(data).capitalize(),
      "title": "{}".format(data).title()
    }
    return (capitalize_it[capitalize])

"""*******************************************************************************************
End of Capitalization
*******************************************************************************************"""