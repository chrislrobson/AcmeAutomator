####################################################################################################################
# Python Qt5 Testbed Tester Show Interface Terse Seed Analysis File Builder
# MODULE:  ShowInterfaceTerseSeedAnalysisFileBuilder
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
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
# Show Interface Terse SeedAnalysis File Builder
#-----------------------------------------------------------------------
class ShowInterfaceTerseSeedAnalysisFileBuilder:
  "Show Interface Terse Seed Analysis File Builder"
  #----------------------------------------------------------------------------------------------------------------
  def __init__( self, parent = None ):
    self.name = "Show Interface Terse Seed Analysis File Builder"
    self.parent = parent
    self.seed = parent.seed
    self.gparent = parent.parent.parent.parent
    self.filename_time_extension = self.parent.filename_time_extension
    self.cmd_list = parent.cmd_list
    self.with_line_numbers = "No"
    self.debug = False
    self.terse_interfaces_terse_analysis_filename = ""
    self.terse_interfaces_terse_data_filename = ""
    self.terse_interfaces_terse_analysis_fd = None
    self.terse_data_fd = None
    self.prepare_analysis_flag = False
    self.start_analysis_flag = False
    self.start_but_skip_one_analysis_flag = False
    self.terse_router_id = ""
    self.terse_interfaces_terse_table = []
    self.interfaces_to_match = ""
  #----------------------------------------------------------------------------------------------------------------
  def execute( self ):
    self.results = ""
    self.received_data = ""
    #----------------------------------------------------------------------------------------------------------------
    self.interfaces_to_match = self.cmd_list[SeedCommandDictionaryProcessor.interfaces]
    if self.cmd_list[SeedCommandDictionaryProcessor.verbose] == 'Yes':
      self.message_str = \
        "Build Show Interface Terse Seed File command started at: {}\n".\
          format( datetime.datetime.now().strftime( "%d%b%Y-%H%M-%S" ) )
      self.gparent.processor_message_signal.emit(self.message_str)
    self.message_str = "Building seed file: {}.".\
          format( self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] )
    self.gparent.logger_message_signal.emit( self.message_str )
    try:
      self.analysis_filename = str( self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] )
      self.terse_interfaces_terse_analysis_fd = open( self.analysis_filename, "w+" )
    except:
      raise Exception( "{}: ShowInterfaceTerseSeedAnalysisFileBuilder file I/O error with \"{}\". "
                       "Build Show Interface Terse Seed File Command terminated. ".
                       format( self.name,
                               self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] )  )
    self.data_filename = self.cmd_list[SeedCommandDictionaryProcessor.commandpath] + \
                         self.cmd_list[SeedCommandDictionaryProcessor.commands] + \
                         self.filename_time_extension
    try:
      with open( self.data_filename, "r" ) as self.terse_data_fd:
        for self.terse_data in self.terse_data_fd:
          if self.prepare_analysis_flag and \
             self.terse_data.startswith( "Interface               Admin Link Proto    Local" ):
            self.build_interfaces_terse_analysis_seed_file()
            self.terse_interfaces_terse_analysis_fd.close()
            self.terse_data_fd.close()
            break
          elif self.terse_data.startswith( "DUT(" ) and \
               self.terse_data.find( ")-> show interfaces terse | no-more" ) != -1:
            self.prepare_analysis_flag = True
            continue
          else:
            continue
    except Exception as e:
      raise Exception( "ShowInterfaceTerseSeedAnalysisFileBuilder: {}".format(e) )
    return()
  #----------------------------------------------------------------------------------------------------------------
  # ge-5/3/3.0              up    up   inet     150.20.192.133/30
  #----------------------------------------------------------------------------------------------------------------
  def build_interfaces_terse_analysis_seed_file( self ):
    for self.terse_data in self.terse_data_fd:
      self.terse_data_list = self.terse_data.split()
      #------------------------------------------------------------------------------------------------------------
      # Strip out crap that we dont care about and "will" screw up the analysis process
      #------------------------------------------------------------------------------------------------------------
      if self.terse_data.startswith( "        " ) or \
         self.terse_data.startswith( "{master}" ) or self.terse_data.startswith( "\n" ):
        continue
      if self.interfaces_to_match != "":
        for self.intf in self.interfaces_to_match.split():
          if self.terse_data_list[0].startswith( self.intf ):
            break
        else:
          continue
      try:
        self.interface_received = self.terse_data_list[0].replace( ":", "~" )
      except:
        self.interface_received = ""
      try:
        self.admin_received = self.terse_data_list[1]
      except:
        self.admin_received = ""
      try:
        self.link_received = self.terse_data_list[2]
      except:
        self.link_received = ""
      try:
        self.proto_received = self.terse_data_list[3]
        try:
          self.address_received = self.terse_data_list[4].replace( ":", "~" )
        except:
          self.address_received = ""
      except:
        self.proto_received = ""
        self.address_received = ""
      if self.proto_received != "" and self.address_received != "":
        self.terse_interfaces_terse_table.append(
          "{" + \
          "\"show interfaces terse\":\"show interfaces terse\"," \
          "\"device\":\"juniper\"," \
          "\"interface\":\"{}\"," \
          "\"admin\":\"{}\",\"link\":\"{}\"," \
          "\"proto\":\"{}\",\"address\":\"{}\"".format( self.interface_received,
                                                        self.admin_received,
                                                        self.link_received,
                                                        self.proto_received,
                                                        self.address_received ) + \
          "};" )
      elif self.proto_received != "" and self.address_received == "":
        self.terse_interfaces_terse_table.append(
          "{" + \
          "\"show interfaces terse\":\"show interfaces terse\"," \
          "\"device\":\"juniper\"," \
          "\"interface\":\"{}\"," \
          "\"admin\":\"{}\",\"link\":\"{}\"," \
          "\"proto\":\"{}\"".format( self.interface_received,
                                     self.admin_received,
                                     self.link_received,
                                     self.proto_received ) + \
          "};" )
      else:
        self.terse_interfaces_terse_table.append(
          "{" + \
          "\"show interfaces terse\":\"show interfaces terse\"," \
          "\"device\":\"juniper\"," \
          "\"interface\":\"{}\"," \
          "\"admin\":\"{}\",\"link\":\"{}\"".format( self.interface_received,
                                                     self.admin_received,
                                                     self.link_received ) + \
          "};" )
    for seed_dictionary in self.terse_interfaces_terse_table:
      try:
        self.terse_interfaces_terse_analysis_fd.write( seed_dictionary + "\n" )
      except Exception as e:
        raise Exception( "ShowInterfaceTerseSeedAnalysisFileBuilder: {}".format(e) )
    return ()
####################################################################################################################
