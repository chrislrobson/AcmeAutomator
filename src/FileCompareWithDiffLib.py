####################################################################################################################
# Python Qt5 Testbed Tester File Compare DiffLib
# MODULE:   File Compare DiffLib
# Author: Christopher Robson
# Copyright by:  Christopher Robson
# Copyright date: 01Jan2016
# This software is not FREE!  Use or destribution of the software system and its
# subsystem modules, libraries, configuration file and "seed" file without the
# express permission of the author is strictly PROHIBITED!
# FUNCTION:  Module provides another compare tool for reading test result files.
#            Message passing between the GUI and the testing modules is accomplished
#            using Qt5 "Signal and Slot" processing system.
####################################################################################################################
import difflib
import os
#------------------------------------------------------------------------------------------------------------------
# Home grown
#------------------------------------------------------------------------------------------------------------------
from Globals import *
#------------------------------------------------------------------------------------------------------------------
# Compare Files with Vdiff
#--------------------------------------------------------------------------------------------------------------------
class CompareFilesWithDiffLib:
  "Compare Files With DiffLib"
  #----------------------------------------------------------------------------------------------------------------
  def __init__( self, parent = None ):
    self.name = "Compare Files with DiffLib"
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
      self.ggparent.logger_message_signal.emit("DiffLib compare files command is running")
    try:
      self.commandsfilename = cmd_dict['commands']
    except:
      self.message_str = Globals.RED_MESSAGE + \
                         "DIFFLIB COMPARE: CMD_DICT[commands]!" + \
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
                         "DIFFLIB COMPARE: {}{} open file error ".format( self.command_path, self.commandsfilename, e.args ) + \
                         Globals.SPAN_END_MESSAGE
      self.ggparent.logger_message_signal.emit( self.message_str )
      self.message_str = Globals.RED_MESSAGE + \
                         "DIFFLIB COMPARE: command terminated." + \
                         Globals.SPAN_END_MESSAGE
      self.ggparent.logger_message_signal.emit( self.message_str )
      return ()
    try:
      self.fileoutput = cmd_dict['fileoutput']
    except:
      self.fileoutput = 'No'
    if self.fileoutput == "Yes":
      try:
        self.archive_filename = self.save_path + cmd_dict['exactfilename']
      except:
        try:
          self.archive_filename = self.save_path + cmd_dict['filename'] + \
                                  self.filename_time_extension
        except:
            self.archive_filename =  self.save_path + self.ip + \
                                     self.filename_time_extension
      try:
          self.archiveFD = open( self.archive_filename, "a+" )
      except:
        self.message_str = Globals.RED_MESSAGE + \
                           "DiffLib file I/O error with \"{}\".".format( self.archive_filename ) + \
                           Globals.SPAN_END_MESSAGE
        self.ggparent.logger_message_signal.emit(self.message_str)
        self.message_str = Globals.RED_MESSAGE + \
                           "DiffLib terminated." + \
                           Globals.SPAN_END_MESSAGE
        self.ggparent.logger_message_signal.emit(self.message_str)
        return()
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
        try:
          self.baseline_file_size = os.path.getsize( self.Baselinefile )
          self.upgrade_file_size = os.path.getsize( self.Upgradefile )
        except:
          self.message_str = Globals.RED_MESSAGE + \
                             "DiffLib file I/O error with \"{}\" or \"{}\".".\
                             format( self.Baselinefile, self.Baselinefile  ) + \
                             Globals.SPAN_END_MESSAGE
          self.ggparent.logger_message_signal.emit( self.message_str )
          continue
        if self.baseline_file_size > 1000000:
          self.message_str = Globals.RED_ONLY_MESSAGE + \
                             "DiffLib file \"{}\" is to large to process.".\
                             format( self.Baselinefile ) + \
                             Globals.SPAN_END_MESSAGE
          self.ggparent.logger_message_signal.emit( self.message_str )
          continue
        elif self.upgrade_file_size > 1000000:
          self.message_str = Globals.RED_ONLY_MESSAGE + \
                             "DiffLib file \"{}\" is to large to process.". \
                               format( self.Upgradefile ) + \
                             Globals.SPAN_END_MESSAGE
          self.ggparent.logger_message_signal.emit( self.message_str )
          continue
        if self.verbose == "Yes":
          self.message_str = self.Baselinefile + " : " + self.Upgradefile
          self.ggparent.logger_message_signal.emit(self.message_str)
        CompareFiles().compare_files( self, self.Baselinefile, self.Upgradefile, self.archiveFD )
    self.archiveFD.close()
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
  # ------------------------------------------------------------------------------------------------------------------
  def compare_files(self, parent = None, filename1 = None, filename2 = None, archiveFD = None ):
    try:
      self.fromlines, self.tolines = self.get_compare_files_data( parent, filename1, filename2)
    except:
      return ()
    for self.line in "".join( difflib.Differ().compare( self.fromlines, self.tolines ) ).splitlines():
      if self.line.startswith( "-" ):
        parent.ggparent.processor_message_signal.emit( self.line )
      elif self.line.startswith( "+" ):
        self.line_str = Globals.BLUE_ONLY_MESSAGE + \
                         self.line + \
                         Globals.SPAN_END_MESSAGE
        parent.ggparent.processor_message_signal.emit( self.line_str )
      try:
        archiveFD.write( self.line + "\n" )
      except:
        pass
    return()
  #------------------------------------------------------------------------------------------------------------------
  def get_compare_files_data(self, parent = None, filename1=None, filename2=None):
    try:
      with open( filename1, 'r' ) as FD:
        self.fromlines = FD.readlines()
    except Exception as e:
      self.message_str = Globals.RED_MESSAGE + \
                         "DIFFLIB COMPARE: {} read file error {}".format( filename1, e.args ) + \
                         Globals.SPAN_END_MESSAGE
      parent.ggparent.logger_message_signal.emit( self.message_str )
      return()
    try:
      with open( filename2, 'r' ) as FD:
        self.tolines = FD.readlines()
    except Exception as e:
      self.message_str = Globals.RED_MESSAGE + \
                         "DIFFLIB COMPARE: {} read file error {} ".format( filename2, e.args ) + \
                         Globals.SPAN_END_MESSAGE
      parent.ggparent.logger_message_signal.emit( self.message_str )
      return()
    return ( self.fromlines, self.tolines )
#--------------------------------------------------------------------------------------------------------------------
#####################################################################################################################
