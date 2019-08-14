"""******************************************************************************************************************
* FILE: ScpFileCopyNameTranslator
* PROJECT: AcmeAutomator
* CLASS(s): ScpFileCopyNameTranslator
* MEMBER(s):
* AUTHOR: Christopher L. Robson (UID): 
* DATE: 9/27/18 TIME: 09:25:00
* COPYRIGHT (c): 9/27/18 Christopher L. Robson. All rights reserved.
*                This software is not FREE!  Use or destribution of the software system
*                and its subsystem modules, libraries, configuration file and "seed" file
*                without the express permission of the author is strictly PROHIBITED!
* DESCRIPTION: Appends the datetime onto SCP files sent to/from the host (aka NOT the target device)
*              However, if the "scpexactname" keyword is set true (in the master-profile.prf file,
*              then DONT modify the filename with the datetime.  Typically, expecting the datetime on
*              the file (after the .cfg extension) is done when the master-profile.prf file is both
*              saving (downloading) and pushing (uploading) the configuration file.
*              Default is to append datetime aka, no scpexactname keyword is found.
*
# CRITICAL notes The file path on the host as well as the network device "MUST" be exact, for example
#          notes on a Cisco the receiving file on the router MUST include the "disk0:" path or the file will NOT transfer
*      Cisco:
*      scp disk0:/running-configuration test@192.168.1.68:/archived-running-configuration.cfg
*      scp test@192.168.1.68:/running-configuration.cfg disk0:/running-configuration
*
*      Juniper:
*      file copy scp://test@192.168.1.68/configuration.cfg configuration
*      file copy configuration scp://test@192.168.1.68/configuration.cfg
*
*********************************************************************************************************************"""
class ScpFileCopyNameTranslator():
  "Scp File Copy Name Translator"
  def __init__(self, parent = None):
    super(ScpFileCopyNameTranslator, self).__init__()
    self.name = self.__class__.__name__
    self.parent = parent
  """"""
  def scp_file_copy(self, dictionary = None, data = None):
    self.dictionary = dictionary
    self.data = data
    try:
      if self.data.startswith("file copy ") or self.data.startswith("scp ") and '@' in self.data.split()[1] or '@' in self.data.split()[2]:
        try:
          if dictionary['scpexactname']:
            return(self.data)
        except Exception as error:
          """
          If "scpexactname" key not present then we need to append datetime to filename
          """
          pass
        self.data = self.data.split("\n")[0]
        if self.dictionary['device'] == "juniper":
          if self.data.startswith("file copy") and self.data.split()[3].startswith("scp://") and '@' in self.data.split()[3]:
            self.data =  "{}{}\n".format(self.data, self.dictionary['datetime'])
          elif self.data.startswith("file copy scp://") and '@' in self.data.split()[2]:
            self.data =  "{} {} {}{} {}\n".format(self.data.split()[0], self.data.split()[1], self.data.split()[2], self.dictionary['datetime'], self.data.split()[3])
        elif self.dictionary['device'] == "cisco":
          if self.data.startswith("scp ") and '@' in self.data.split()[1]:
            self.data = "{} {}{} {}\n".format(self.data.split()[0], self.data.split()[1], self.dictionary['datetime'], self.data.split()[2])
          elif self.data.startswith("scp ") and '@' in self.data.split()[2]:
            self.data = "{}{}\n".format(self.data, self.dictionary['datetime'])
    except Exception as error:
      """
      Must not be a scp file transfer command so ignore error caused by data split command
      """
      pass
    return(self.data)
"""**********************************************************************************************
End of File
**********************************************************************************************"""