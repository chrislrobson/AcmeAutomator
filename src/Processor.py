"""***************************************************************************************************************
FILE: Processor
MODULE:   Processor
Author: Christopher Robson
Copyright by:  Christopher Robson
Copyright date: 01Jan2016
This software is not FREE!  Use or destribution of the software system and its
subsystem modules, libraries, configuration file and "seed" file without the
express permission of the author is strictly PROHIBITED!
FUNCTION:  Class provides the interface between the thread control worker "NoneBlocking" classes and the testing classes.
           Message passing between the GUI and the testing classes is accomplished
           using Qt5 "Signal and Slot" processing system and threaded classes.
           Called by selecting the "Execute" button on the menu "Test DUT" and passed to the threaded "Worker" class.
           This class is the main processing loop.
           Its function is to read the seed master file, extract each command (the very first quoted word of each
          line(string) in the master seed file and using that first word, called the command control word,
          and spawn the associated comands class/methods via the importlib function
Return:  Returns to the calling class any data collected from the DUT for further
         processing by the calling class.
Errors:  Errors are logged directly to the report or logger scroll window at the subclass level via the
         Qt5 Signal/Slot flow control with messages eventual processed by the Worker class calling the thread.
Processing Flow:  GUI (select) ---> Worker (connect) ---> Processor (importlib)---> Command Classes (ssh)---> devices
                  divices (data) ---> Command Classes (signal/exception) ---> Processor (signal/exception) --->
                  Worker (signal) ---> GUI (present)
***************************************************************************************************************"""
"""
Python Libraries
"""
from PyQt5 import QtCore, QtWidgets
import ast
import datetime
import importlib
import time
from io import *
"""
Script Libraries
"""
from Globals import *
from CallClass import CallClass
from ValidateCommand import ValidateCommand
from Dictionary import Dictionary
from SeedCommandlinePreprocessor import SeedCommandlinePreprocessor
from Utility import Utility
from DecoderUtility import DecoderUtility
from AnalyzeActionUtility import AnalyzeActionUtility
import ReceivedDataReplyDictionary
import SearchListDictionary
import DecodeDataDictionary
import AnalyzeActionSelector
"""
While these modules and classes are not "called" directly from within this module/class it is still required to
specify the modules and classes specifically so the "importlib.import_module" can properly reference the
class and spawn the method for execution.  All part of the OOP thing dude!
"""
from SSHConnectionProcessor import Connect, Disconnect
from FileCompareWithDiffLib import CompareFilesWithDiffLib
from FileCompareWithVdiff import CompareFilesWithVdiff
from HostCommand import Hostcommand
from Command import Command
from Analysis import Analysis
from SSHChannelProcessor import SSHChannel
from ShowInterfacesDetailAnalysisSeedFileBuilder import ShowInterfacesDetailAnalysisSeedFileBuilder
"""
CLASS: Processor
DESCRIPTION: Main thread subsystem processing logci starting point
INPUT: seed files, windowing system hooks
OUTPUT: reports
"""
class Processor( QtCore.QThread ):
  " Processor "
  """"""
  def __init__(self, parent = None):
    super(Processor, self).__init__(parent)
    self.name = self.__class__.__name__
    self.parent = parent
    self.logger_message_signal = self.parent.logger_message_signal
    """
    Report tab window
    """
    self.consoleDutTabWidget = self.parent.nonBlocking.consoleDutTabWidget
    self.report_list_widget = None
    self.ip = ""
    self.ssh_handle = -1
    self.scp_handle = -1
    Globals().ssh_connection_dict = []
    self.filename_time_extension = datetime.datetime.now().strftime("-%d%b%Y-%H%M-%S")
    self.report_file_list = []
    """
    Set up the analysis results reporting database.  Here all analysis data is tagged as either
    "Fail" or "Pass".  Then when all analysis processing is completed this list can be built
    into a single unified reporting table for presentation into the Test Plan Report
    """
    self.analysis_results = Utility(SearchListDictionary)
    """
    Start by initializing the prompt string processor object.  This object is used to scan each
    data received buffer for a session terminating string from a session transmitted command
    to a device.
    """
    self.process_reply = Utility(ReceivedDataReplyDictionary)
    """
    Decoder_class is a group of classes whose names match device data reporting strings.  The class called
    is determined by building the class name from the input data.  The build name is passed to the 
    importlib class.
    """
    self.decoder_class = DecoderUtility(DecodeDataDictionary)
    """
    Used to determine the action taken between values being analyzed.
    """
    self.analyze_class = AnalyzeActionUtility(AnalyzeActionSelector)
    """
    Valid Master seed file command keywords
    Using a dictionary provides a mechanism for translating keywords
    """
  """
  Entry point where the AcmeAutomator starts process all testing functions.
  It is here the "master" seed files are read to determine how each test run will functions.
  """
  def processor(self):
    if self.parent.nonBlocking.verbose:
      self.parent.console_message_signal.emit("AcmeAutomator started at: {}".format(datetime.datetime.today().strftime("%d%b%Y-%H%M-%S")))
    self.dut_ip_test_list = Globals().get_dut_to_be_tested_list()
    if not self.dut_ip_test_list:
      self.message = "{{{}NO devices selected, test has aborted!{}}}".format(Globals.RED_MESSAGE, Globals.SPAN_END_MESSAGE)
      self.logger_message_signal.emit(self.message)
      return()
    try:
      for self.ip_line in self.dut_ip_test_list:
        self.ip = self.ip_line.split("-")[0]
        self.ip_and_name = "".join(self.ip_line.split())
        self.parent.create_tab_signal.emit(self.consoleDutTabWidget, self.ip)
        try:
          self.filebeingopenned = str(Globals.profiles_directory + Globals().get_dut_ip_list_dict()[self.ip_and_name])
          self.message = "Processing master seed file: \n{}.".format(self.filebeingopenned)
          self.logger_message_signal.emit(self.message)
          with open(self.filebeingopenned, 'r') as self.devicectlFD:
            for self.devicectl in self.devicectlFD:
              if not SeedCommandlinePreprocessor(self).preprocessor(message_signal = self.logger_message_signal, data = self.devicectl):
                continue
              """
              Skip command until we find a connect and it gets established which will set ssh_handle to
              something "other than -1"
              However, "hostcommand" and "analysis" control words can be processed 
              since they dont require a connection to a remote device, such as the processing of
              priorly obtained data and stored in an archived file.
              """
              self.keyword = ValidateCommand().validate_command(self.ssh_handle, self.devicectl[2:].split("\":")[0])
              if self.keyword == "":
                continue
              else:
                try:
                  """
                  Convert seed file entry to dictionary and process so required entries are checked and/or defaults set.
                  """
                  self.cmdline_dict   = ast.literal_eval(self.devicectl.split(';')[0])
                  self.dict = Dictionary(self)
                  self.dictionary = self.dict.build_seed_dictionary(dicitonary = self.cmdline_dict, ip = self.ip, filename_time_extension = self.filename_time_extension)
                  self.dict.update_dictionary(self.dictionary, 'processreply', self.process_reply)
                  self.dict.update_dictionary(self.dictionary, 'analyzeaction', self.analyze_class)
                  self.dict.update_dictionary(self.dictionary, 'tab_id', self.ip)
                  self.dict.update_dictionary(self.dictionary, 'ip', self.ip)
                  self.dict.update_dictionary(self.dictionary, 'widget', self.consoleDutTabWidget)
                  self.dict.update_dictionary(self.dictionary, 'loggerwidget', self.parent.logger_message_signal)
                  self.dict.update_dictionary(self.dictionary, 'consolewidget', self.parent.console_message_signal)
                  self.dict.update_dictionary(self.dictionary, 'reportwidget', self.parent.report_message_signal)
                  self.dict.update_dictionary(self.dictionary, 'datetime', self.filename_time_extension)
                  self.results = RunSeedFileCommand(self).run_seed_file_command_device(cmdline_dict = self.cmdline_dict, dictionary = self.dictionary)
                  continue
                except SyntaxError as error:
                  """
                  Order here is important Syntax errors MUST be checked first before the "Generic Exception"
                  check that follows.  This helps reduce code.  Further, since this is syntax error with the
                  seed file dictionary string, stop all processing and fail out of this seed file processing.
                  """
                  self.message = "{{{}{}: {} {}{}}}".format(Globals.RED_MESSAGE, self.name, self.filebeingopenned, error, Globals.SPAN_END_MESSAGE)
                  self.logger_message_signal.emit(self.message)
                  raise Exception
                except Exception as error:
                  """
                  Since this error is NOT a Syntax error with the seed file, reset the connection handle
                  and scan for another connection request since a seed file can connect to more than one
                  device at a time within a single seed file. 
                  """
                  self.ssh_handle = -1
                  continue
        except Exception as error:
          if error.args:
            self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
            self.logger_message_signal.emit(self.message)
          raise Exception
    except Exception as error:
      if error.args:
        self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
      else:
        self.message = "{{{}{}: failure, processing terminated{}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
      self.logger_message_signal.emit(self.message)
      raise Exception
    return()
"""
Execute seed file command
"""
class RunSeedFileCommand:
  "Run Seed File Command"
  def __init__(self, parent = None):
    self.name = self.__class__.__name__
    self.parent = parent
  """"""
  def run_seed_file_command_device(self, cmdline_dict = None, dictionary = None):
    self.results = ""
    self.cmdline_dict = cmdline_dict
    self.dictionary = dictionary
    self.module_method = None
    try:
        self.method = list(self.cmdline_dict.keys())[0]
        self.dict = list(self.cmdline_dict.values())[0]
        try:
          # notes Add Slot/signal pointers to subclass dictionary
          self.dict['processreply'] = self.dictionary['processreply']
          self.dict['analyzeaction'] = self.dictionary['analyzeaction']
          self.dict['ip'] = self.dictionary['ip']
          self.dict['tab_id'] = self.dictionary['tab_id']
          self.dict['widget'] = self.dictionary['widget']
          self.dict['loggerwidget'] = self.dictionary['loggerwidget']
          self.dict['consolewidget'] = self.dictionary['consolewidget']
          self.dict['reportwidget'] = self.dictionary['reportwidget']
          self.dict['datetime'] = self.dictionary['datetime']
          self.results = CallClass(self).call_class(module_name = self.parent.name, class_name = self.method.title(), method_name = "execute", dictionary = self.dict)
        except Exception as error:
          if error.args:
            """
            DO NOT print errors at this level, Errors MUST be displayed "as" they occur at the lower slot level
            """
            self.message = "{{{}{}(run): failure {} NOTE(!!!) Coding violation error MUST be processed at lower level{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
            self.cmdline_dict['loggerwidget'].emit(self.message)
          raise Exception
    except Exception as error:
      if error.args:
        self.message = "{{{}{}: failure {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
      raise Exception
    return(self.results)
"""********************************************************************************************************************
End of File
********************************************************************************************************************"""
