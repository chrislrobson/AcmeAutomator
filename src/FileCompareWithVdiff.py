####################################################################################################################
# Python Qt5 Testbed Tester File Compare Vdiff
# MODULE:   File Compare Vdiff
# Author: Christopher Robson
# Copyright by:  Christopher Robson
# Copyright date: 01Jan2016
# This software is not FREE!  Use or destribution of the software system and its
# subsystem modules, libraries, configuration file and "seed" file without the
# express permission of the author is strictly PROHIBITED!
# FUNCTION:  Module provides another coompare tool for reading test result files.
#            Message passing between the GUI and the testing modules is accomplished
#            using Qt5 "Signal and Slot" processing system.
####################################################################################################################
from vdiff import Vdiff
#------------------------------------------------------------------------------------------------------------------
# Home grown
#------------------------------------------------------------------------------------------------------------------
from Globals import *
#------------------------------------------------------------------------------------------------------------------
# Compare Files with Vdiff
#--------------------------------------------------------------------------------------------------------------------
class CompareFilesWithVdiff:
  "Compare Files With Vdiff"
  #----------------------------------------------------------------------------------------------------------------
  def __init__( self, parent = None ):
    self.name = "Compare Files with Vdiff"
    self.parent = parent
    self.seed = parent.seed
    self.ip = parent.parent.ip
    self.ggparent = parent.parent.parent
    self.ssh_handle = parent.parent.ssh_handle
    self.filename_time_extension = self.parent.parent.filename_time_extension
  # ----------------------------------------------------------------------------------------------------------------
  # ----------------------------------------------------------------------------------------------------------------
  def execute( self, cmd_dict ):
    if self.ggparent.testbed_tester.verbose:
      self.ggparent.logger_message_signal.emit("VDiff compare files command is running")
    try:
      self.commandsfilename = cmd_dict['commands']
    except:
      self.message_str = Globals.RED_MESSAGE + \
                         "VDIFF COMPARE: CMD_DICT[commands]!" + \
                         Globals.SPAN_END_MESSAGE
      self.ggparent.logger_message_signal.emit(self.message_str)
      return ()
    try:
      self.command_path = cmd_dict['commandpath']
    except:
      self.command_path = './'
    try:
      self.save_path = cmd_dict['savepath']
    except:
      self.save_path = './'
    try:
      self.verbose = cmd_dict['verbose']
    except:
      self.verbose = 'No'
    try:
      self.comparefilesFD = open( self.command_path + self.commandsfilename, "r" )
    except Exception as e:
      self.message_str = Globals.RED_MESSAGE + \
                         "VDIFF COMPARE: {}{} open file error ".format( self.command_path, self.commandsfilename, e.args ) + \
                         Globals.SPAN_END_MESSAGE
      self.ggparent.logger_message_signal.emit( self.message_str )
      self.message_str = Globals.RED_MESSAGE + \
                         "VDIFF COMPARE: command terminated." + \
                         Globals.SPAN_END_MESSAGE
      self.ggparent.logger_message_signal.emit( self.message_str )
      return ()
    #--------------------------------------------------------------------------------------------------------------
    # Loop thru the seed file extracting files to compare and calling Vdiff to compare them
    #--------------------------------------------------------------------------------------------------------------
    for self.comparefiles in self.comparefilesFD:
      if self.comparefiles.startswith("#"):
        pass
      elif self.comparefiles.startswith("\n"):
        pass
      else:
        self.Baselinefile = self.comparefiles.split()[0] + self.filename_time_extension
        self.Upgradefile = self.comparefiles.split()[1] + self.filename_time_extension
        CompareFiles().compare_files( self, self.Baselinefile, self.Upgradefile )
    return()
#--------------------------------------------------------------------------------------------------------------------
# Compare Files
# This class is entered either thru a command call from the "master profiles" seed file via the OOP "execute" method
# call or thru the GUI's menu pull down.
#--------------------------------------------------------------------------------------------------------------------
class CompareFiles:
  "Compare files"
  #------------------------------------------------------------------------------------------------------------------
  def __init__(self):
    self.name = "Compare Files"
  #------------------------------------------------------------------------------------------------------------------
  def compare_files(self, parent = None, filename1 = None, filename2 = None):
    self.vdiff = Vdiff( filename1, filename2 )
    try:
      if self.vdiff.differ():
        self.vdiff.edit()
      else:
        self.message_ptr = "{} and {} are the same.".format( filename1, filename2 )
        parent.ggparent.processor_message_signal.emit( self.message_ptr )
    except KeyboardInterrupt:
      self.vdiff.cleanup()
      self.message_ptr = "VDiff closed."
      parent.ggparent.processor_message_signal.emit( self.message_ptr )
    except Exception as e:
     self.message_str = Globals.RED_MESSAGE + \
                        "Command exception failure {}".format( e.args ) + \
                        Globals.SPAN_END_MESSAGE
     parent.ggparent.logger_message_signal.emit(self.message_str)
    return()
#####################################################################################################################
