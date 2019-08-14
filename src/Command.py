"""**************************************************************************************************
FILE: Command
MODULE: Command
Author: Christopher Robson
Copyright by:  Christopher Robson
Copyright date: 01Jan2016
This software is not FREE!  Use or destribution of the software system and its
subsystem modules, libraries, configuration file and "seed" file without the
express permission of the author is strictly PROHIBITED!
FUNCTION:  Module provides the results from a network device "command" command.
           Message passing between the GUI and the testing modules is accomplished
           using Qt5 "Signal and Slot" processing system.
**************************************************************************************************"""
"""
Python Libraries
"""
import datetime
import socket
import os, stat
"""
Script Libraries
"""
from Globals import *
from Exceptions import *
from SSHChannelProcessor import SendDataThroughSSHChannel
from NormalizeData import NormalizeData
from SeedCommandlinePreprocessor import SeedCommandlinePreprocessor
from ManageTabWidgets import ManageTabWidgets
from ScpFileCopyNameTranslator import ScpFileCopyNameTranslator
from CallClass import CallClass
from Directory import Directory
"""
CLASS: Command
DESCRIPTION: Executes comands passed from seed file.
INPUT: seed file with commands to execute
OUTPUT: device command output
"""
class Command:
  "Command"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.ssh_handle = parent.parent.ssh_handle
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dictionary = dictionary
    self.results = ""
    self.received_data = ""
    self.archivefileFD = None
    """"""
    if self.dictionary['verbose']:
      self.message = "{} started at: {}.".format(self.name.title(), datetime.datetime.now().strftime( "%d%b%Y-%H%M-%S" ) )
      self.dictionary['loggerwidget'].emit(self.message)
    try:
      if self.dictionary['fileoutput']:
        Directory(self).create(os.path.abspath(self.dictionary['archivefilename'].split(os.path.basename(self.dictionary['archivefilename']))[0]))
        try:
          self.archivefileFD = open(self.dictionary['archivefilename'], 'w+')
        except Exception as error:
          self.message = "{{{}{}: {} with {}{}}}".format(Globals.RED_MESSAGE, self.name, error, self.dictionary['archivefilename'], Globals.SPAN_END_MESSAGE)
          self.dictionary['loggerwidget'].emit(self.message)
          raise Exception
      with open(self.dictionary["relativepath"] + self.dictionary['commandpath'] + self.dictionary['commands'], 'r' ) as self.commandsFD:
        if self.dictionary['fileoutput']:
          try:
            self.archivefileFD.write("DUT File date/time: {}\n".format(self.dictionary['datetime'][1:]))
          except Exception as error:
            self.archivefileFD.close()
            os.remove(self.dictionary['archivefilename'])
            self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
            self.dictionary['loggerwidget'].emit(self.message)
            raise Exception
        self.message = "Processing: {}.".format(self.dictionary['commands'] )
        self.dictionary['loggerwidget'].emit(self.message )
        for self.cmd_data in self.commandsFD:
          if not SeedCommandlinePreprocessor(self).preprocessor(message_signal = self.dictionary['loggerwidget'], data = self.cmd_data):
            continue
          else:
            try:
              if self.dictionary['verbose']:
                self.dictionary['loggerwidget'].emit(self.cmd_data)
              self.cmd_data = ScpFileCopyNameTranslator(self).scp_file_copy(dictionary = self.dictionary, data = self.cmd_data)
              Globals.request_command_counter += 1
              self.received_data = SendDataThroughSSHChannel(self).send_data_through_ssh_channel(dictionary = self.dictionary,
                                                                                                 data = self.cmd_data.split('\n')[0],
                                                                                                 delay = float(self.dictionary['delay']))
            except (SSHSocketError, SSHConnectionError, KeyError, Exception) as error:
              if self.dictionary['fileoutput']:
                try:
                  self.archivefileFD.close()
                  os.chmod( self.dictionary['archivefilename'], stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO )
                except:
                  pass
              if error.args:
                self.message =  "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                self.dictionary['loggerwidget'].emit( self.message )
              raise Exception
            # todo-debug if self.received_data.find("confirm") != -1 or self.received_data.find("Destination file name") != -1:
            # todo-debug   print(self.received_data)
            if self.dictionary['verbose']:
              """
              Only dump 128 characters to keep output from getting swamped.
              """
              self.message = "{}".format( NormalizeData(self).normalize_data(dictionary = self.dictionary, data = self.received_data))
              self.dictionary['loggerwidget'].emit( self.message )
            """
            Process the reply data from the requested command sent to the device
            """
            self.reply_action = self.dictionary['processreply'].find_prompt(self.received_data, self.dictionary['processreply'].prompt_automaton)
            for self.action_type in self.reply_action:
              if not "Continue" in self.action_type:
                self.reply = self.action_type[1]
                break
            else:
              self.reply = self.action_type[1]
            try:
              self.results = CallClass(self).call_class(module_name = "ProcessReply", class_name = self.reply,
                                                        method_name = "execute", dictionary = self.dictionary)
            except SwitchProcessorBusy as error:
              if self.dictionary['verbose']:
                self.message = "{{{}{} {}{}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                self.dictionary['loggerwidget'].emit(self.message)
            except Exception as error:
              if error.args:
                self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                self.dictionary['loggerwidget'].emit(self.message)
              raise Exception
            self.received_data_norm = self.preprocess_received_data(dictionary = self.dictionary, data = self.received_data)
            if self.received_data_norm:
              if self.archivefileFD != None:
                try:
                  try:
                    self.hostname = socket.gethostbyaddr( self.dictionary['ip'] )[0]
                  except:
                    self.hostname = ""
                  self.archivefileFD.write("DUT( {}/{})-> {}\n".format(self.hostname, self.dictionary['ip'], self.cmd_data.split("\n")[0]))
                except Exception as error:
                  self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                  self.dictionary['loggerwidget'].emit(self.message)
                  raise Exception
                try:
                  self.archivefileFD.write(self.received_data_norm)
                except Exception as error:
                  try:
                    self.archivefileFD.close()
                    os.chmod(self.dictionary['archivefilename'], stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO )
                  except:
                    pass
                  self.message_str = "{}: {}".format(self.name, error)
                  self.dictionary['loggerwidget'].emit(self.message_str)
                  raise Exception
              if self.dictionary['stdout']:
                self.title_msg = "DUT({})-> {}".format(self.dictionary['ip'], self.cmd_data.split("\n")[0])
                try:
                  self.report_widget, self.tab_index = ManageTabWidgets().get_tab_list_widget(tab_widgets = self.dictionary['widget'], tab_id = self.dictionary['tab_id'], list_widget = self.dictionary['tab_id'])
                except Exception as error:
                  self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                  self.dictionary['loggerwidget'].emit(self.message)
                  self.archivefileFD.close()
                  raise Exception
                self.dictionary['reportwidget'].emit(self.title_msg, self.report_widget, self.dictionary['tab_id'])
                self.dictionary['reportwidget'].emit(self.received_data_norm, self.report_widget, self.dictionary['tab_id'])
    except OSError as error:
      if self.archivefileFD != None:
        self.archivefileFD.close()
      self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
      self.dictionary['loggerwidget'].emit(self.message)
      raise Exception
    except Exception as error:
      if error.args:
        if self.dictionary['fileoutput']:
          try:
            self.archivefileFD.close()
            os.chmod(self.dictionary['archivefilename'], stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO )
          except KeyError as fileerror:
            self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, fileerror, Globals.SPAN_END_MESSAGE)
            self.dictionary['loggerwidget'].emit( self.message )
        self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
        self.dictionary['loggerwidget'].emit( self.message )
      raise Exception
    if self.dictionary['fileoutput']:
      try:
        self.archivefileFD.close()
        os.chmod(self.dictionary['archivefilename'], stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO )
      except:
        pass
    return()
  """
  Deal with CISCO's stupid code routine!
  Before writing data to the disk file clean out the prompt string and any control characters
  and the command string that is transmitted as well from stupid Cisco routers... they are BRAIN-DEAD!
  """
  def preprocess_received_data(self, dictionary = None, data = None):
    self.data = data
    self.dictionary = dictionary
    if self.dictionary['device'] == "cisco":
      normalize_it = NormalizeData(self)
      self.received_data_norm_strip_cmd = normalize_it.normalize_data(dictionary = self.dictionary, data = self.data)
      self.data_list = self.received_data_norm_strip_cmd.split("\n")
      self.prompt_str = self.data_list[-1]
      self.cmd_string_to_strip = "{}{}".format(self.prompt_str, self.data.split("\n")[0])
      if self.received_data_norm_strip_cmd.startswith(self.cmd_string_to_strip):
        self.data_pre = self.received_data_norm_strip_cmd.split(self.cmd_string_to_strip)[1]
        try:
          self.received_data_norm = self.data_pre.split(self.prompt_str)[0]
        except:
          self.received_data_norm = self.data_pre
      elif self.received_data_norm_strip_cmd.split()[0].startswith(self.data.split()[0]):
        try:
          self.received_data_norm = self.received_data_norm_strip_cmd.split(self.data)[1].split(self.prompt_str)[0]
        except:
          try:
            self.received_data_norm = "\n".join(self.data_list[1:])
            try:
              self.received_data_norm = self.received_data_norm.split(self.prompt_str)[0]
            except:
              pass
          except:
            self.received_data_norm = self.received_data_norm_strip_cmd
      else:
        self.received_data_norm = self.received_data_norm_strip_cmd
    else:
      """
      All other good routers writing data to the disk file clean out the prompt string and any control characters
      """
      self.data_to_use = ""
      normalize_it = NormalizeData(self)
      self.received_data_norm = normalize_it.normalize_data(dictionary = self.dictionary, data = self.data)
      self.received_data_norm = self.received_data_norm.replace("\r", "\n")
      self.data_list = self.received_data_norm.split("\n")
      self.prompt_str = self.data_list[-1]
      self.cmd_first = "{} {} ".format(self.received_data_norm.split()[0], self.data.split()[1])
      for self.item_data in self.received_data_norm.split("\n"):
        if self.item_data.startswith("\n"):
          self.data_to_use += self.item_data
          continue
        try:
          self.rcv_first = "{} {} ".format(self.item_data.split()[0], self.item_data.split()[1])
        except:
          pass
        if self.rcv_first.startswith(self.cmd_first):
          continue
        if self.item_data.startswith(self.prompt_str):
          continue
        self.data_to_use += self.item_data + "\n"
      self.received_data_norm = self.data_to_use
    if self.received_data_norm.startswith("\n"):
      self.received_data_norm = self.received_data_norm[1:]
    return(self.received_data_norm)
"""*********************************************************************************************
End of File
********************************************************************************************"""
