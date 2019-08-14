####################################################################################################################
# Python Qt5 Testbed Tester Show ISIS Database Seed Analysis File Builder
# MODULE:  ShowISISAdjancencySeedAnalysisFileBuilder
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
# Show Isis Database Seed Analysis File Builder
#-----------------------------------------------------------------------
class ShowIsisDatabaseSeedAnalysisFileBuilder:
  "Show Isis Database Seed Analysis File Builder"
  #----------------------------------------------------------------------------------------------------------------
  def __init__( self, parent = None ):
    self.name = "Show Isis Database Seed Analysis File Builder"
    self.parent = parent
    self.seed = parent.seed
    self.gparent = parent.parent.parent.parent
    self.filename_time_extension = self.parent.filename_time_extension
    self.cmd_list = parent.cmd_list
    self.with_line_numbers = "No"
    self.debug = False
    self.isis_database_analysis_filename = ""
    self.isis_database_data_filename = ""
    self.isis_database_analysis_fd = None
    self.isis_data_fd = None
    self.prepare_analysis_flag = False
    self.start_analysis_flag = False
    self.start_but_skip_one_analysis_flag = False
    self.isis_database_table = []
    self.isis_router_id = ""
    self.index = 0
  #----------------------------------------------------------------------------------------------------------------
  def execute( self ):
    #----------------------------------------------------------------------------------------------------------------
    self.interfaces_to_match = self.cmd_list[SeedCommandDictionaryProcessor.interfaces]
    self.device_being_matched = self.cmd_list[SeedCommandDictionaryProcessor.device]
    if self.cmd_list[SeedCommandDictionaryProcessor.verbose] == 'Yes':
      self.message_str = \
        "Build Show Isis Database Seed File command started at: {}.".\
          format( datetime.datetime.now().strftime( "%d%b%Y-%H%M-%S" ) )
      self.gparent.logger_message_signal.emit(self.message_str)
    self.message_str = "Building seed file: {}.".\
          format( self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] )
    self.gparent.logger_message_signal.emit( self.message_str )
    try:
      self.analysis_filename = str( self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] )
      self.isis_database_analysis_fd = open( self.analysis_filename, "w+" )
    except:
      raise Exception( "{}: ShowIsisDatabaseSeedAnalysisFileBuilder file I/O error with \"{}\". "
                       "Build Show Isis Database Seed File Command terminated. ".
                       format( self.name,
                               self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] )  )
    self.data_filename = self.cmd_list[SeedCommandDictionaryProcessor.commandpath] + \
                         self.cmd_list[SeedCommandDictionaryProcessor.commands] + \
                         self.filename_time_extension
    try:
      with open( self.data_filename, "r" ) as self.isis_data_fd:
        for self.isis_data in self.isis_data_fd:
          self.index += len( self.isis_data )
          if self.start_analysis_flag:
            if self.isis_data.startswith( "\n" ):
              continue
            if self.device_being_matched == "juniper":
              self.build_juniper_isis_database_analysis_seed_file()
            if self.device_being_matched == "cisco":
              try:
                self.build_cisco_isis_database_analysis_seed_file()
              except Exception as e:
                print(e)
            self.isis_database_analysis_fd.close()
            self.isis_data_fd.close()
            break
          elif self.isis_data.startswith( "IS-IS" ):
            self.isis_router_id = self.isis_data.split()[1]
            # FIXME REMOVE THIS TEST elif self.prepare_analysis_flag and self.isis_data.startswith( "LSPID" ):
            self.start_analysis_flag = True
          elif self.isis_data.startswith( "DUT(" ) and \
                  self.isis_data.find( ")-> show isis database detail" ) != -1:
            # FIXME REMOVE AFTER TEST WITH CISCO self.isis_data.find( ")-> show isis database | no-more" ) != -1:
            self.prepare_analysis_flag = True
            continue
          else:
            continue
    except Exception as e:
      raise Exception( "ShowIsisDatabaseSeedAnalysisFileBuilder: {}".format(e) )
    return()
  #----------------------------------------------------------------------------------------------------------------
  #----------------------------------------------------------------------------------------------------------------
  def build_cisco_isis_database_analysis_seed_file( self ):
    self.isis_database_table = []
    for self.isis_data in self.isis_data_fd:
      self.index += len( self.isis_data )
      if self.isis_data.startswith( "\n" ):
        continue
      if self.isis_data.split()[0].startswith( "Total" ):
        break
      if not self.isis_data.startswith( " " ):
        self.isis_data_list = self.isis_data.split()
        if self.isis_data_list[1] == "*":
          self.lsp_offset = 1
          self.originating_lsp_received = self.isis_data_list[1]
        else:
          self.lsp_offset = 0
          self.originating_lsp_received = ""
        try:
          self.lspid_received = self.isis_data_list[0]
        except:
          self.lspid_received = ""
        try:
          self.sequence_number_received = self.isis_data_list[self.lsp_offset + 1]
        except:
          self.sequence_number_received = ""
        try:
          self.checksum_received = self.isis_data_list[self.lsp_offset + 2]
        except:
          self.checksum_received = ""
        try:
          self.hold_time_received = self.isis_data_list[self.lsp_offset + 3]
        except:
          self.hold_time_received = ""
        try:
          self.att_pol_received = self.isis_data_list[self.lsp_offset + 4]
        except:
          self.att_pol_received = ""
      for self.isis_data in self.isis_data_fd:
        print(self.isis_data)
        self.index += len( self.isis_data )
        self.isis_data_list = self.isis_data.split()
        if self.isis_data.startswith( "\n" ):
          continue
        if self.isis_data_list[0].startswith( "Total" ):
          self.isis_data_fd.seek( 0,2 )
          break
        if not self.isis_data.startswith( " " ):
          self.isis_data_fd.seek( self.index - len( self.isis_data ) )
          self.index -= len( self.isis_data )
          break
        if self.isis_data_list[0].startswith( "Auth" ):
          try:
            self.auth_algorithm_received = self.isis_data_list[2]
          except:
            self.auth_algorithm_received = ""
          try:
            self.auth_length_received = self.isis_data_list[4]
          except:
            self.auth_length_received = ""
          self.isis_database_table.append( "{" + \
                                             "\"show isis database detail\":\"show isis database detail\"," \
                                             "\"device\":\"{}\"," \
                                             "\"lspid\":\"{}\"," \
                                             "\"originating lsp\":\"{}\"," \
                                             "\"sequence number\":\"{}\"," \
                                             "\"checksum\":\"{}\"," \
                                             "\"hold time\":\"{}\"," \
                                             "\"att pol\":\"{}\"," \
                                             "\"auth algorithm\":\"{}\"," \
                                             "\"auth length\":\"{}\"" \
                                             .format( self.device_being_matched,
                                                      self.lspid_received,
                                                      self.originating_lsp_received,
                                                      self.sequence_number_received,
                                                      self.checksum_received,
                                                      self.hold_time_received,
                                                      self.att_pol_received,
                                                      self.auth_algorithm_received,
                                                      self.auth_length_received
                                                     ) + \
                                             "};")
          continue
        if self.isis_data_list[0].startswith( "Area" ):
          try:
            self.area_address_received = self.isis_data_list[2]
          except:
            self.area_address_received = ""
          self.isis_database_table.append( "{" + \
                                           "\"show isis database detail\":\"show isis database detail\"," \
                                           "\"device\":\"{}\"," \
                                           "\"lspid\":\"{}\"," \
                                           "\"originating lsp\":\"{}\"," \
                                           "\"sequence number\":\"{}\"," \
                                           "\"checksum\":\"{}\"," \
                                           "\"hold time\":\"{}\"," \
                                           "\"att pol\":\"{}\"," \
                                           "\"area address\":\"{}\"" \
                                           .format( self.device_being_matched,
                                                    self.lspid_received,
                                                    self.originating_lsp_received,
                                                    self.sequence_number_received,
                                                    self.checksum_received,
                                                    self.hold_time_received,
                                                    self.att_pol_received,
                                                    self.area_address_received
                                                    ) + \
                                           "};" )
          continue
        if self.isis_data_list[0].startswith( "NLPID" ):
          try:
            self.nlpid_received = self.isis_data_list[1]
          except:
            self.nlpid_address_received = ""
          self.isis_database_table.append( "{" + \
                                           "\"show isis database detail\":\"show isis database detail\"," \
                                           "\"device\":\"{}\"," \
                                           "\"lspid\":\"{}\"," \
                                           "\"originating lsp\":\"{}\"," \
                                           "\"sequence number\":\"{}\"," \
                                           "\"checksum\":\"{}\"," \
                                           "\"hold time\":\"{}\"," \
                                           "\"att pol\":\"{}\"," \
                                           "\"nlpid\":\"{}\"" \
                                           .format( self.device_being_matched,
                                                    self.lspid_received,
                                                    self.originating_lsp_received,
                                                    self.sequence_number_received,
                                                    self.checksum_received,
                                                    self.hold_time_received,
                                                    self.att_pol_received,
                                                    self.nlpid_received
                                                    ) + \
                                           "};" )
          continue
        if self.isis_data_list[0].startswith( "Hostname" ):
          try:
            self.hostname_received = self.isis_data_list[1]
          except:
            self.hostname_received = ""
          self.isis_database_table.append( "{" + \
                                           "\"show isis database detail\":\"show isis database detail\"," \
                                           "\"device\":\"{}\"," \
                                           "\"lspid\":\"{}\"," \
                                           "\"originating lsp\":\"{}\"," \
                                           "\"sequence number\":\"{}\"," \
                                           "\"checksum\":\"{}\"," \
                                           "\"hold time\":\"{}\"," \
                                           "\"att pol\":\"{}\"," \
                                           "\"hostname\":\"{}\"" \
                                           .format( self.device_being_matched,
                                                    self.lspid_received,
                                                    self.originating_lsp_received,
                                                    self.sequence_number_received,
                                                    self.checksum_received,
                                                    self.hold_time_received,
                                                    self.att_pol_received,
                                                    self.hostname_received
                                                    ) + \
                                           "};" )
          continue
        if self.isis_data_list[0].startswith( "IP" ):
          try:
            self.ip_address_received = self.isis_data_list[2]
          except:
            self.ip_address_received = ""
          self.isis_database_table.append( "{" + \
                                           "\"show isis database detail\":\"show isis database detail\"," \
                                           "\"device\":\"{}\"," \
                                           "\"lspid\":\"{}\"," \
                                           "\"originating lsp\":\"{}\"," \
                                           "\"sequence number\":\"{}\"," \
                                           "\"checksum\":\"{}\"," \
                                           "\"hold time\":\"{}\"," \
                                           "\"att pol\":\"{}\"," \
                                           "\"ip address\":\"{}\"" \
                                           .format( self.device_being_matched,
                                                    self.lspid_received,
                                                    self.originating_lsp_received,
                                                    self.sequence_number_received,
                                                    self.checksum_received,
                                                    self.hold_time_received,
                                                    self.att_pol_received,
                                                    self.ip_address_received
                                                    ) + \
                                           "};" )
          continue
        if self.isis_data_list[0].startswith( "Router" ):
          try:
            self.router_id_received = self.isis_data_list[2]
          except:
            self.router_id_received = ""
          self.isis_database_table.append( "{" + \
                                           "\"show isis database detail\":\"show isis database detail\"," \
                                           "\"device\":\"{}\"," \
                                           "\"lspid\":\"{}\"," \
                                           "\"originating lsp\":\"{}\"," \
                                           "\"sequence number\":\"{}\"," \
                                           "\"checksum\":\"{}\"," \
                                           "\"hold time\":\"{}\"," \
                                           "\"att pol\":\"{}\"," \
                                           "\"router id\":\"{}\"" \
                                           .format( self.device_being_matched,
                                                    self.lspid_received,
                                                    self.originating_lsp_received,
                                                    self.sequence_number_received,
                                                    self.checksum_received,
                                                    self.hold_time_received,
                                                    self.att_pol_received,
                                                    self.router_id_received
                                                    ) + \
                                           "};" )
          continue
        if self.isis_data_list[0].startswith( "Metric" ):
          try:
            self.metric_received = self.isis_data_list[2]
          except:
            self.metric_received = ""
          try:
            self.ip_extended_received = self.isis_data_list[3]
          except:
            self.ip_extended_received = ""
          self.isis_database_table.append( "{" + \
                                             "\"show isis database detail\":\"show isis database detail\"," \
                                             "\"device\":\"{}\"," \
                                             "\"lspid\":\"{}\"," \
                                             "\"originating lsp\":\"{}\"," \
                                             "\"sequence number\":\"{}\"," \
                                             "\"checksum\":\"{}\"," \
                                             "\"hold time\":\"{}\"," \
                                             "\"att pol\":\"{}\"," \
                                             "\"metric\":\"{}\"," \
                                             "\"ip extended\":\"{}\"" \
                                             .format( self.device_being_matched,
                                                      self.lspid_received,
                                                      self.originating_lsp_received,
                                                      self.sequence_number_received,
                                                      self.checksum_received,
                                                      self.hold_time_received,
                                                      self.att_pol_received,
                                                      self.metric_received,
                                                      self.ip_extended_received
                                                     ) + \
                                             "};")
          continue
    for self.seed_dictionary in self.isis_database_table:
      # FIXME DEBUG print(seed_dictionary)
      try:
        self.isis_database_analysis_fd.write( self.seed_dictionary + "\n" )
      except:
        print( "Seed dictionary file write failed." )
    return()
  #----------------------------------------------------------------------------------------------------------------
  #----------------------------------------------------------------------------------------------------------------
  def build_juniper_isis_database_analysis_seed_file( self ):
    isis_database_table = []
    for self.isis_data in self.isis_data_fd:
      if self.isis_data.startswith( "\n" ):
        break
      else:
        try:
          self.interface = self.isis_data.split()[0]
        except:
          self.interface = ""
        try:
          self.system = self.isis_data.split()[1]
        except:
          self.system = ""
        try:
          self.level = self.isis_data.split()[2]
        except:
          self.level = ""
        try:
          self.state = self.isis_data.split()[3]
        except:
          self.state = ""
        try:
          self.hold = self.isis_data.split()[4]
        except:
          self.hold = ""
        try:
          self.snpa = self.isis_data.split()[5]
        except:
          self.snpa = ""
        isis_database_table.append( "{" + \
                                     "\"show isis database detail\":\"show isis database detail\",\"device\":\"juniper\"," \
                                     "\"interface\":\"{}\",\"system\":\"{}\"," \
                                     "\"level\":\"{}\",\"state\":\"{}\"," \
                                     "\"hold\":\"{}\",\"snpa\":\"{}\"".format( self.interface,
                                                                               self.system,
                                                                               self.level,
                                                                               self.state,
                                                                               self.hold,
                                                                               self.snpa ) + \
                                     "};")
    for seed_dictionary in isis_database_table:
      # FIXME DEBUG print(seed_dictionary)
      try:
        self.isis_database_analysis_fd.write(seed_dictionary + "\n")
      except:
        print("Seed dictionary file write failed.")
    return()
###################################################################################################################
