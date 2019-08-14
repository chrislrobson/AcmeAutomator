####################################################################################################################
# Python Qt5 Testbed Tester Show Interface Brief Seed Analysis File Builder
# MODULE:  ShowInterfaceBriefSeedAnalysisFileBuilder
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
# Show Interface Brief SeedAnalysis File Builder
#-----------------------------------------------------------------------
class ShowInterfaceBriefSeedAnalysisFileBuilder:
  "Show Interface Brief Seed Analysis File Builder"
  #----------------------------------------------------------------------------------------------------------------
  def __init__( self, parent = None ):
    self.name = "Show Interface Brief Seed Analysis File Builder"
    self.parent = parent
    self.seed = parent.seed
    self.gparent = parent.parent.parent.parent
    self.filename_time_extension = self.parent.filename_time_extension
    self.cmd_list = parent.cmd_list
    self.with_line_numbers = "No"
    self.debug = False
    self.brief_interfaces_brief_analysis_filename = ""
    self.brief_interfaces_brief_data_filename = ""
    self.brief_interfaces_brief_analysis_fd = None
    self.brief_data_fd = None
    self.prepare_analysis_flag = False
    self.start_analysis_flag = False
    self.start_but_skip_one_analysis_flag = False
    self.brief_router_id = ""
    self.brief_interfaces_brief_table = []
    self.interfaces_to_match = ""
  #----------------------------------------------------------------------------------------------------------------
  def execute( self ):
    self.results = ""
    self.received_data = ""
    #----------------------------------------------------------------------------------------------------------------
    self.interfaces_to_match = self.cmd_list[SeedCommandDictionaryProcessor.interfaces]
    if self.cmd_list[SeedCommandDictionaryProcessor.verbose] == 'Yes':
      self.message_str = \
        "Build Show Interface Brief Seed File command started at: {}\n".\
          format( datetime.datetime.now().strftime( "%d%b%Y-%H%M-%S" ) )
      self.gparent.processor_message_signal.emit(self.message_str)
    self.message_str = "Building seed file: {}.".\
          format( self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] )
    self.gparent.logger_message_signal.emit( self.message_str )
    try:
      self.analysis_filename = str( self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] )
      self.brief_interfaces_brief_analysis_fd = open( self.analysis_filename, "w+" )
    except:
      raise Exception( "{}: ShowInterfaceBriefSeedAnalysisFileBuilder file I/O error with \"{}\". "
                       "Build Show Interface Brief Seed File Command terminated. ".
                       format( self.name,
                               self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] )  )
    self.data_filename = self.cmd_list[SeedCommandDictionaryProcessor.commandpath] + \
                         self.cmd_list[SeedCommandDictionaryProcessor.commands] + \
                         self.filename_time_extension
    try:
      with open( self.data_filename, "r" ) as self.brief_data_fd:
        for self.brief_data in self.brief_data_fd:
          if self.start_analysis_flag:
            self.build_interfaces_brief_analysis_seed_file()
            self.brief_interfaces_brief_analysis_fd.close()
            self.brief_data_fd.close()
            break
          elif self.prepare_analysis_flag and \
               self.brief_data.startswith( "               Name       State       State               Type" ):
            self.start_analysis_flag = True
          elif self.brief_data.startswith( "DUT(" ) and \
               self.brief_data.find( ")-> show interfaces brief" ) != -1:
            self.prepare_analysis_flag = True
            continue
          else:
            continue
    except Exception as e:
      raise Exception( "ShowInterfaceBriefSeedAnalysisFileBuilder: {}".format(e) )
    return()
  #----------------------------------------------------------------------------------------------------------------
  def build_interfaces_brief_analysis_seed_file( self ):
    for self.brief_data in self.brief_data_fd:
      if self.brief_data.startswith( "\n" ):
        continue
      if self.interfaces_to_match != "":
        for self.intf in self.interfaces_to_match.split():
          if self.brief_data.split()[0].startswith( self.intf ):
            break
        else:
          # print(self.brief_data.split()[0])
          continue
      try:
        self.interface_received = self.brief_data.split()[0]
        self.interface_received = self.interface_received.replace( ":", "~" )
      except:
        self.interface_received = ""
      try:
        self.admin_received = self.brief_data.split()[1]
      except:
        self.admin_received = ""
      try:
        self.link_received = self.brief_data.split()[2]
      except:
        self.link_received = ""
      try:
        self.encap_received = self.brief_data.split()[3]
      except:
        self.encap_received = ""
      try:
        self.mtu_received = self.brief_data.split()[4]
      except:
        self.mtu_received = ""
      try:
        self.bandwidth_received = self.brief_data.split()[5]
      except:
        self.bandwidth_received = ""
      self.brief_interfaces_brief_table.append(
        "{" + \
        "\"show interfaces brief\":\"show interfaces brief\"," \
        "\"device\":\"cisco\"," \
        "\"interface\":\"{}\"," \
        "\"admin\":\"{}\",\"link\":\"{}\"," \
        "\"encap\":\"{}\",\"mtu\":\"{}\",\"bandwidth\":\"{}\"".format( self.interface_received,
                                                  self.admin_received,
                                                  self.link_received,
                                                  self.encap_received,
                                                  self.mtu_received,
                                                  self.bandwidth_received ) + \
        "};" )
    for seed_dictionary in self.brief_interfaces_brief_table:
      try:
        self.brief_interfaces_brief_analysis_fd.write( seed_dictionary + "\n" )
      except Exception as e:
        raise Exception( "ShowInterfaceBriefSeedAnalysisFileBuilder: {}".format(e) )
    return ()
####################################################################################################################
