####################################################################################################################
# Python Qt5 Testbed Tester Show Interface Status Seed Analysis File Builder
# MODULE:  ShowInterfaceStatusSeedAnalysisFileBuilder
# Author: Christopher Robson
# Copyright by:  Christopher Robson
# Copyright date: 01Jan2016
# This software is not FREE!  Use or destribution of the software system and its
# subsystem modules, libraries, configuration file and "seed" file without the
# express permission of the author is strictly PROHIBITED!
# FUNCTION:  Module builds a seed file for analysizing collected data.
####################################################################################################################
import datetime
import os, sys, stat
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
# Home grown
#------------------------------------------------------------------------------------------------------------------
from Globals import *
from Exceptions import *
from SeedDictionary import SeedCommandDictionaryProcessor
from ShowInterfacesStatusStringParser import ShowInterfaceStatusStringParser
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
# Show Interface Status SeedAnalysis File Builder
#-----------------------------------------------------------------------
class ShowInterfaceStatusSeedAnalysisFileBuilder:
  "Show Interface Status Seed Analysis File Builder"
  #----------------------------------------------------------------------------------------------------------------
  def __init__( self, parent = None ):
    self.name = "Show Interface Status Seed Analysis File Builder"
    self.parent = parent
    self.seed = parent.seed
    self.gparent = parent.parent.parent.parent
    self.filename_time_extension = self.parent.filename_time_extension
    self.cmd_list = parent.cmd_list
    self.with_line_numbers = "No"
    self.debug = False
    self.status_interfaces_status_analysis_filename = ""
    self.status_interfaces_status_data_filename = ""
    self.status_interfaces_status_analysis_fd = None
    self.status_data_fd = None
    self.prepare_analysis_flag = False
    self.start_analysis_flag = False
    self.start_but_skip_one_analysis_flag = False
    self.status_router_id = ""
    self.status_interfaces_status_table = []
  #----------------------------------------------------------------------------------------------------------------
  def execute( self ):
    self.results = ""
    self.received_data = ""
    #----------------------------------------------------------------------------------------------------------------
    if self.cmd_list[SeedCommandDictionaryProcessor.verbose] == 'Yes':
      self.message_str = \
        "Build Show Interface Status Seed File command started at: {}\n".\
          format( datetime.datetime.now().strftime( "%d%b%Y-%H%M-%S" ) )
      self.gparent.processor_message_signal.emit(self.message_str)
    self.message_str = "Building seed file: {}.".\
          format( self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] )
    self.gparent.logger_message_signal.emit( self.message_str )
    try:
      self.analysis_filename = str( self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] )
      self.status_interfaces_status_analysis_fd = open( self.analysis_filename, "w+" )
    except:
      raise Exception( "{}: ShowInterfaceStatusSeedAnalysisFileBuilder file I/O error with \"{}\". "
                       "Build Show Interface Status Seed File Command terminated. ".
                       format( self.name,
                               self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] )  )
    self.data_filename = self.cmd_list[SeedCommandDictionaryProcessor.commandpath] + \
                         self.cmd_list[SeedCommandDictionaryProcessor.commands] + \
                         self.filename_time_extension
    try:
      with open( self.data_filename, "r" ) as self.status_data_fd:
        for self.status_data in self.status_data_fd:
          if self.start_analysis_flag and \
               self.status_data.startswith( "Port           Name             Status       Vlan" ):
            self.build_interfaces_status_analysis_seed_file()
            self.status_interfaces_status_analysis_fd.close()
            self.status_data_fd.close()
            break
          elif self.status_data.startswith( "DUT(" ) and \
               self.status_data.find( ")-> show interfaces status" ) != -1:
            self.start_analysis_flag = True
            continue
          else:
            continue
    except Exception as e:
      raise Exception( "ShowInterfaceStatusSeedAnalysisFileBuilder: {}".format(e) )
    return()
  #----------------------------------------------------------------------------------------------------------------
  def build_interfaces_status_analysis_seed_file( self ):
    for self.status_data in self.status_data_fd:
      self.interface_received,\
      self.name_received,\
      self.status_received,\
      self.vlan_received,\
      self.duplex_received,\
      self.speed_received,\
      self.type_received = ShowInterfaceStatusStringParser().show_interface_status_string_parser( self.status_data )
      self.status_interfaces_status_table.append(
        "{" + \
        "\"show interfaces status\":\"show interfaces status\"," \
        "\"device\":\"cisco\"," \
        "\"interface\":\"{}\"," \
        "\"name\":\"{}\",\"status\":\"{}\"," \
        "\"vlan\":\"{}\",\"duplex\":\"{}\"," \
        "\"speed\":\"{}\",\"type\":\"{}\"".format( self.interface_received,
                                                  self.name_received,
                                                  self.status_received,
                                                  self.vlan_received,
                                                  self.duplex_received,
                                                  self.speed_received,
                                                  self.type_received ) + \
        "};" )
    for seed_dictionary in self.status_interfaces_status_table:
      try:
        self.status_interfaces_status_analysis_fd.write( seed_dictionary + "\n" )
      except Exception as e:
        raise Exception( "ShowInterfaceStatusSeedAnalysisFileBuilder: {}".format(e) )
    return ()
####################################################################################################################
