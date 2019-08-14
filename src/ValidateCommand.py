"""*******************************************************************************************
* FILE: ValidateCommand
* PROJECT: AcmeAutomation
* CLASS(s): ValidateCommand
* MEMBER(s):
* AUTHOR: Christopher L. Robson (UID): 
* DATE: 9/23/18 TIME: 06:37:00
* COPYRIGHT (c): 9/23/18 Christopher L. Robson. All rights reserved.
*                This software is not FREE!  Use or destribution of the software system
*                and its subsystem modules, libraries, configuration file and "seed" file
*                without the express permission of the author is strictly PROHIBITED!
* DESCRIPTION:  Validates the seed file command "keywords" before processing.
*               Since a table look up is used to validate, a translation of the command
*               is possible.
* NOTES!        Test to assure if connect has been established for any "command"
*
*******************************************************************************************"""
"""
CLASS: ValidateCommand
METHOD: ValidateCommand
DESCRIPTION: 
INPUT: 
OUTPUT: 
"""

class ValidateCommand():
  "Valid Command"

  """"""
  def __init__(self, parent = None):
    super(ValidateCommand, self).__init__()
    self.name = self.__class__.__name__
    self.parent = parent
    self.command = {
      "connect": "connect",
      "command": "command",
      "hostcommand": "hostcommand",
      "analysis": "analysis",
      "disconnect": "disconnect"
    }

  """"""
  def validate_command(self, ssh_handle = -1, keyword = ""):
    self.keyword = keyword
    self.ssh_handle = ssh_handle
    try:
      if self.ssh_handle == -1 and self.command[self.keyword] == "command":
        return("")
      else:
        return(self.command[self.keyword])
    except:
      return("")

"""*******************************************************************************************
End of ValidCommand
*******************************************************************************************"""