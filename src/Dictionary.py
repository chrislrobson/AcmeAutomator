"""**********************************************************************************************
* FILE: Dictionary
* PROJECT: AcmeAutomator
* CLASS(s): Dictionary
* MEMBER(s):
* AUTHOR: Christopher L. Robson (UID): 
* DATE: 9/29/18 TIME: 06:18:00
* COPYRIGHT (c): 9/29/18 Christopher L. Robson. All rights reserved.
*                This software is not FREE!  Use or destribution of the software system
*                and its subsystem modules, libraries, configuration file and "seed" file
*                without the express permission of the author is strictly PROHIBITED!
* DESCRIPTION:
*
**********************************************************************************************"""
"""
Home grown libraries
"""
from Globals import Globals
"""
CLASS: Dictionary
DESCRIPTION: Executes comands passed from seed file.
INPUT: Seed file extracted line converted to dictionary
OUTPUT: Seed dictionary converted to runtime dictionary
"""
class Dictionary():
  "Dictionary"

  """"""
  def __init__(self, parent = None):
    super(Dictionary, self).__init__()
    self.name = self.__class__.__name__
    self.parent = parent

  """"""
  def dictionary(self, target = None, baseline = None):
    self.baseline = baseline
    self.target = self.get_dictionary(target)
    try:
      for self.key, self.value in self.baseline.items():
        try:
          self.valid = self.target[self.key]
        except:
          self.target[self.key] = self.baseline[self.key]
    except Exception as error:
      raise("{}: processing dictionary({}) {}".format(self.name, self.target, error))
    return(self.target)

  """"""
  def build_seed_dictionary(self, dicitonary = None, ip = "", filename_time_extension = ""):
    self.dictionary = dicitonary
    self.ip = ip
    self.filename_time_extension = filename_time_extension
    self.cmd_dict = self.get_dictionary(self.dictionary)
    if not (self.cmd_dict):
      return(dicitonary)
    try:
      self.cmd_dict['commands'] = self.cmd_dict['commands']
    except Exception as error:
      self.message = "{{{}{}: no {} file provided{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
      self.cmd_dict['loggerwidget'].emit(self.message)
      raise Exception
    self.cmd_dict['relativepath'] = Globals.relativepath
    try:
      self.cmd_dict['prompt'] = self.cmd_dict['prompt']
      self.cmd_dict['processreply'].set_prompt_string(self.cmd_dict['prompt'], "Continue")
    except:
      pass  # assume done by connect command
    try:
      self.cmd_dict['session'] = self.cmd_dict['session']
    except:
      self.cmd_dict['session'] = "NONE"
    try:
      self.cmd_dict['delay'] = float(self.cmd_dict['delay'])
    except:
      self.cmd_dict['delay'] = .1
    try:
      self.cmd_dict['loopcnt'] = int(float(self.cmd_dict['loopcnt']))
    except:
      self.cmd_dict['loopcnt'] = 240
    try:
      self.cmd_dict['commandpath'] = self.cmd_dict['commandpath']
    except:
      self.cmd_dict['commandpath'] = "./"
    try:
      self.cmd_dict['savepath'] = self.cmd_dict['savepath']
    except:
      self.cmd_dict['savepath'] = "./"
    try:
      self.cmd_dict['issave'] = self.cmd_dict['issave']
    except:
      self.cmd_dict['issave'] = True
    try:
      self.cmd_dict['fullscan'] = self.cmd_dict['fullscan']
    except:
      self.cmd_dict['fullscan'] = False
    try:
      self.cmd_dict['stdout'] = self.cmd_dict['stdout']
    except:
      self.cmd_dict['stdout'] = False
    try:
      self.cmd_dict['verbose'] = self.cmd_dict['verbose']
    except:
      self.cmd_dict['verbose'] = False
    try:
      self.cmd_dict['fileoutput'] = self.cmd_dict['fileoutput']
    except:
      self.cmd_dict['fileoutput'] = False
    try:
      if self.cmd_dict['user'] == "NONE":
        self.cmd_dict['user'] = Globals().user_to_use
      else:
        self.cmd_dict['user'] = self.cmd_dict['user']
    except:
      self.cmd_dict['user'] = Globals().user_to_use
    try:
      if self.cmd_dict['pwd'] == "NONE":
        self.cmd_dict['pwd'] = Globals().password_to_use
      else:
        self.cmd_dict['pwd'] = self.cmd_dict['pwd']
    except:
      self.cmd_dict['pwd'] = Globals().password_to_use
    if self.cmd_dict['fileoutput']:
      try:
        self.cmd_dict['archivefilename'] = Globals.relativepath + self.cmd_dict['savepath'] + self.cmd_dict['exactfilename']
      except:
        try:
          self.cmd_dict['archivefilename'] = Globals.relativepath + self.cmd_dict['savepath'] + self.cmd_dict['filename'] + self.filename_time_extension
        except:
          self.cmd_dict['archivefilename'] = Globals.relativepath + self.ip + self.filename_time_extension
    else:
      self.cmd_dict['archivefilename'] = ""
    try:
      self.cmd_dict['interfaces'] = self.cmd_dict['interfaces']
    except:
      self.cmd_dict['interfaces'] = ""
    try:
      self.cmd_dict['device'] = self.cmd_dict['device']
    except Exception as error:
      self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
      self.cmd_dict['loggerwidget'].emit(self.message)
      raise Exception
    try:
      self.cmd_dict['initializedata'] = self.cmd_dict['initializedata']
    except:
      self.cmd_dict['initializedata'] = False
    try:
      self.cmd_dict['detailedresults'] = self.cmd_dict['detailedresults']
    except:
      self.cmd_dict['detailedresults'] = 'Yes'
    """
    Return the original dictionary so the "RunCommand" class can morph the command to run
    which is extracted from the first key and used as the command classes keyword name. 
    """
    return(self.cmd_dict)

  """"""
  def get_dictionary(self, dictionary = None):
    self.dictionary = dictionary
    if list(self.dictionary.keys())[0] == "connect" or list(self.dictionary.keys())[0] == "disconnect":
      return ({})
    elif list(self.dictionary.keys())[0] == "analysis":
      return (list(list(self.dictionary.values())[0].values())[0])
    else:
      return(list(self.dictionary.values())[0])

  """"""
  def update_dictionary(self, dictionary = None, key = None, value = None):
    self.key = key
    self.value = value
    self.dictionary = dictionary
    try:
      self.dictionary[self.key] = self.value
    except Exception as error:
      raise("{}: processing dictionary({}:{}) {}".format(self.name, self.dictionary, self.value, error))
    return(self.dictionary[self.key])

"""**********************************************************************************************
End of File
**********************************************************************************************"""
