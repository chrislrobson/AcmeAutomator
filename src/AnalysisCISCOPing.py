####################################################################################################################
# Python Qt5 Testbed Tester Analysis CISCO Ping
# MODULE:  AnalysisCiscoPing
# Author: Christopher Robson
# Copyright by:  Christopher Robson
# Copyright date: 01Jan2016
# This software is not FREE!  Use or destribution of the software system and its
# subsystem modules, libraries, configuration file and "seed" file without the
# express permission of the author is strictly PROHIBITED!
# FUNCTION:  Module analysis ping packets
####################################################################################################################
import datetime
import ast
import collections
import sys
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
# Home grown
#------------------------------------------------------------------------------------------------------------------
from Globals import *
from Exceptions import *
from SeedDictionary import SeedCommandDictionaryProcessor
from SeedCommandlinePreprocessor import SeedCommandlinePreprocessor
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
# CISCO Ping analysis processor
#-----------------------------------------------------------------------
class CISCOPing:
  "CISCO Ping"
  #----------------------------------------------------------------------------------------------------------------
  def __init__( self, parent = None ):
    self.name = "CISCO Ping Analysis"
    self.parent = parent
    self.ggparent = parent.parent.parent.parent
    self.seed = parent.seed
    self.ip = parent.ip
    self.ssh_handle = parent.ssh_handle
    self.filename_time_extension = parent.filename_time_extension
    self.process_reply = parent.process_reply
    self.cmd_list = parent.cmd_list
  #----------------------------------------------------------------------------------------------------------------
  def execute( self ):
    self.results = ""
    self.received_data = ""
    #----------------------------------------------------------------------------------------------------------------
    try:
      self.cmd_list[SeedCommandDictionaryProcessor.archivefilenameFD].\
                    write( "\nDUT ANALYSIS REPORT =================================="
                           "===============================================\n" )
      self.cmd_list[SeedCommandDictionaryProcessor.archivefilenameFD].\
                    write( "DUT Analysis Report File date/time: {}\n".format( self.filename_time_extension ) )
    except:
      raise Exception( "{}: Command file I/O error with \"{}\". "
          "command terminated. ".format( self.name,
                                              self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] )  )
    if self.cmd_list[SeedCommandDictionaryProcessor.verbose] == 'Yes':
      self.message_str = \
        "{} started at: {}\n".\
          format( self.name, datetime.datetime.now().strftime( "%d%b%Y-%H%M-%S" ) )
      self.ggparent.logger_message_signal.emit(self.message_str)
    try:
      with open( self.cmd_list[SeedCommandDictionaryProcessor.commandpath] +
                     self.cmd_list[SeedCommandDictionaryProcessor.commands], 'r' ) as self.cmd_file_FD:
        self.message_str = "Processing CISCO Ping Analysis file: {}.".\
          format( self.cmd_list[SeedCommandDictionaryProcessor.commands] )
        self.ggparent.logger_message_signal.emit( self.message_str )
        for self.cmd_data_str in self.cmd_file_FD:
          if not SeedCommandlinePreprocessor( self ).seed_commandline_preprocessor( self.cmd_data_str ):
            pass
          else:
            self.cmd_dict = ast.literal_eval( self.cmd_data_str.split( ";\n" )[0] )
            self.path = self.cmd_dict["savepath"]
            self.targetip = self.cmd_dict["targetip"]
            self.count = self.cmd_dict["count"]
            self.successfull_pings = 0
            self.failed_pings = 0
            try:
              self.filename = self.cmd_dict["exactfilename"]
            except:
              self.filename = self.cmd_dict["filename"] + self.filename_time_extension
            try:
              with open( self.path + self.filename, 'r' ) as self.reportFD:
                for self.report_data in self.reportFD:
                  if self.report_data.startswith( "DUT(" ):
                    if self.targetip in self.report_data:
                      while( not self.report_data.startswith( "DUT=======" ) ):
                        try:
                          self.report_data = next( self.reportFD )
                        except:
                          sys.exc_info()
                          break
                        if self.report_data.startswith( "Sending {}".format( self.count ) ):
                          while( not self.report_data.startswith( "DUT=======" ) ):
                            try:
                              self.report_data = next( self.reportFD )
                            except:
                              sys.exc_info()
                              break
                            if "DUT=======" in self.report_data:
                              break
                            else:
                              self.success_fails = collections.Counter( self.report_data )
                              self.successfull_pings += self.success_fails['!']
                              self.failed_pings += self.success_fails['.']
                else:
                  if not self.failed_pings and not self.successfull_pings:
                    self.cmd_list[SeedCommandDictionaryProcessor.archivefilenameFD].\
                      write( "An attempt to analysis ping results for {} failed, "
                           "address not found.".format( self.targetip ) )
                    self.message_str =  "An attempt to analysis ping results for {} failed, " \
                                        "address not found.".format( self.targetip )
                    self.ggparent.processor_message_signal.emit( self.message_str )
                  else:
                    self.cmd_list[SeedCommandDictionaryProcessor.archivefilenameFD].\
                      write( "Ping report for IP Address:\t  {}\n".format( self.targetip ) )
                    self.cmd_list[SeedCommandDictionaryProcessor.archivefilenameFD]. \
                      write( "Successful pings:\t\t  {}\n".format( str( self.successfull_pings ) ) )
                    self.cmd_list[SeedCommandDictionaryProcessor.archivefilenameFD].\
                      write( "Failed pings:\t\t\t  {}\n".format( str( self.failed_pings ) ) )
                    self.message_str = "Ping report for IP Address:\t  {}\n".format( self.targetip ) + \
                                       "Successful pings:\t  {}\n".format( str( self.successfull_pings ) ) + \
                                       "Failed pings:\t\t  {}".format( str( self.failed_pings ) )
                    self.ggparent.processor_message_signal.emit( self.message_str )
              self.reportFD.close()
            except OSError as error:
              raise CriticalFailure( "{}: File error: {} with {}.".format( self.name, error.args[1], self.path + self.filename ) )
    except OSError as error:
      raise CriticalFailure( "{}: File error: {} with {}.".format( self.name, error.args[1], self.path + self.filename ) )
    except:
      try:
        self.cmd_list[SeedCommandDictionaryProcessor.archivefilenameFD].close()
      except:
        pass
      raise
    try:
      self.cmd_list[SeedCommandDictionaryProcessor.archivefilenameFD].close()
      Globals().\
       set_show_file_list( self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] )
    except:
      pass
    return()
#####################################################################################################################