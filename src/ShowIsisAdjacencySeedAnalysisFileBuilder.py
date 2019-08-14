####################################################################################################################
# Python Qt5 Testbed Tester Show ISIS Adjacency Seed Analysis File Builder
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
# Show Isis Adjacency Seed Analysis File Builder
#-----------------------------------------------------------------------
class ShowIsisAdjacencySeedAnalysisFileBuilder:
  "Show Isis Adjacency Seed Analysis File Builder"
  #----------------------------------------------------------------------------------------------------------------
  def __init__( self, parent = None ):
    self.name = "Show Isis Adjacency Seed Analysis File Builder"
    self.parent = parent
    self.seed = parent.seed
    self.gparent = parent.parent.parent.parent
    self.filename_time_extension = self.parent.filename_time_extension
    self.cmd_list = parent.cmd_list
    self.with_line_numbers = "No"
    self.debug = False
    self.isis_adjacency_analysis_filename = ""
    self.isis_adjacency_data_filename = ""
    self.isis_adjacency_analysis_fd = None
    self.isis_data_fd = None
    self.prepare_analysis_flag = False
    self.start_analysis_flag = False
    self.start_but_skip_one_analysis_flag = False
    self.isis_adjacency_table = []
    self.isis_router_id = ""
  #----------------------------------------------------------------------------------------------------------------
  def execute( self ):
    #----------------------------------------------------------------------------------------------------------------
    self.interfaces_to_match = self.cmd_list[SeedCommandDictionaryProcessor.interfaces]
    self.device_being_matched = self.cmd_list[SeedCommandDictionaryProcessor.device]
    if self.device_being_matched == "juniper":
      self.title_str = "Interface             System         L State"
    elif self.device_being_matched == "cisco":
      self.title_str = "System Id      Interface        SNPA           State Hold Changed  NSF IPv4 IPv6"
    else:
      raise Exception( "ShowIsisAdjacencySeedAnalysisFileBuilder: UNKNOWN DEVICE TYPE" )
    if self.cmd_list[SeedCommandDictionaryProcessor.verbose] == 'Yes':
      self.message_str = \
        "Build Show Isis Adjacency Seed File command started at: {}.".\
          format( datetime.datetime.now().strftime( "%d%b%Y-%H%M-%S" ) )
      self.gparent.logger_message_signal.emit(self.message_str)
    self.message_str = "Building seed file: {}.".\
          format( self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] )
    self.gparent.logger_message_signal.emit( self.message_str )
    try:
      self.analysis_filename = str( self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] )
      self.isis_adjacency_analysis_fd = open( self.analysis_filename, "w+" )
    except:
      raise Exception( "{}: ShowIsisAdjacencySeedAnalysisFileBuilder file I/O error with \"{}\". "
                       "Build Show Isis Adjacency Seed File Command terminated. ".
                       format( self.name,
                               self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] )  )
    self.data_filename = self.cmd_list[SeedCommandDictionaryProcessor.commandpath] + \
                         self.cmd_list[SeedCommandDictionaryProcessor.commands] + \
                         self.filename_time_extension
    try:
      with open( self.data_filename, "r" ) as self.isis_data_fd:
        for self.isis_data in self.isis_data_fd:
          if self.isis_data.startswith( "\n" ):
            continue
          elif self.isis_data.startswith( "IS-IS" ):
            self.isis_router_id = self.isis_data.split()[1]
          elif self.prepare_analysis_flag and \
             self.isis_data.startswith( self.title_str ):
            if self.device_being_matched == "juniper":
              self.build_juniper_isis_adjacency_analysis_seed_file()
            if self.device_being_matched == "cisco":
              self.build_cisco_isis_adjacency_analysis_seed_file()
            else:
              raise Exception( "ShowIsisAdjacencySeedAnalysisFileBuilder: UNKNOWN DEVICE TYPE" )
            self.isis_adjacency_analysis_fd.close()
            self.isis_data_fd.close()
            break
          elif self.isis_data.startswith( "DUT(" ) and \
               self.isis_data.find( ")-> show isis adjacency" ) != -1:
               # FIXME REMOVE AFTER TEST WITH CISCO self.isis_data.find( ")-> show isis adjacency | no-more" ) != -1:
            self.prepare_analysis_flag = True
            continue
          else:
            continue
    except Exception as e:
      raise Exception( "ShowIsisAdjacencySeedAnalysisFileBuilder: {}".format(e) )
    return()
  #----------------------------------------------------------------------------------------------------------------
  # FIXME ANOTHER QUICK AND DIRTY FIX the nesxt two methods should be OOPed!!!!!!
  #----------------------------------------------------------------------------------------------------------------
  # System Id      Interface        SNPA           State Hold Changed  NSF IPv4 IPv6
  # R91A-ASR9010   PO0/0/1/0        *PtoP*         Up    27   3w3d     Yes None None
  #----------------------------------------------------------------------------------------------------------------
  def build_cisco_isis_adjacency_analysis_seed_file( self ):
    isis_adjacency_table = []
    for self.isis_data in self.isis_data_fd:
      if self.isis_data.startswith( "\n" ) or self.isis_data.startswith( " " ):
        continue
      if self.isis_data.startswith( "Total" ):
        break
      else:
        self.isis_data_list = self.isis_data.split()
        try:
          self.system = self.isis_data_list[0]
        except:
          self.system = ""
        try:
          self.interface = self.isis_data_list[1]
        except:
          self.interface = ""
        try:
          self.snpa = self.isis_data_list[2]
        except:
          self.snpa = ""
        try:
          self.state = self.isis_data_list[3]
        except:
          self.state = ""
        try:
          self.hold = self.isis_data_list[4]
        except:
          self.hold = ""
        try:
          self.nsf = self.isis_data_list[6]
        except:
          self.nsf = ""
        try:
          self.ipv4bfd = self.isis_data_list[7]
        except:
          self.ipv4bfd = ""
        try:
          self.ipv6bfd = self.isis_data_list[8]
        except:
          self.ipv6bfd = ""
        isis_adjacency_table.append( "{" + \
                                     "\"show isis adjacency\":\"show isis adjacency\"," \
                                     "\"device\":\"{}\"," \
                                     "\"router id\":\"{}\"," \
                                     "\"interface\":\"{}\",\"system\":\"{}\"," \
                                     "\"snpa\":\"{}\",\"state\":\"{}\"," \
                                     "\"hold\":\"{}\"," \
                                     "\"nsf\":\"{}\"," \
                                     "\"ipv4 bfd\":\"{}\"," \
                                     "\"ipv6 bfd\":\"{}\"".format( self.device_being_matched,
                                                                   self.isis_router_id,
                                                                   self.interface,
                                                                   self.system,
                                                                   self.snpa,
                                                                   self.state,
                                                                   self.hold,
                                                                   self.nsf,
                                                                   self.ipv4bfd,
                                                                   self.ipv6bfd ) + \
                                     "};")
    for seed_dictionary in isis_adjacency_table:
      # FIXME DEBUG print(seed_dictionary)
      try:
        self.isis_adjacency_analysis_fd.write(seed_dictionary + "\n")
      except:
        print("Seed dictionary file write failed.")
    return()
  #----------------------------------------------------------------------------------------------------------------
  #----------------------------------------------------------------------------------------------------------------
  def build_juniper_isis_adjacency_analysis_seed_file( self ):
    isis_adjacency_table = []
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
        isis_adjacency_table.append( "{" + \
                                     "\"show isis adjacency\":\"show_isis_adjacency\",\"device\":\"juniper\"," \
                                     "\"interface\":\"{}\",\"system\":\"{}\"," \
                                     "\"level\":\"{}\",\"state\":\"{}\"," \
                                     "\"hold\":\"{}\",\"snpa\":\"{}\"".format( self.interface,
                                                                               self.system,
                                                                               self.level,
                                                                               self.state,
                                                                               self.hold,
                                                                               self.snpa ) + \
                                     "};")
    for seed_dictionary in isis_adjacency_table:
      # FIXME DEBUG print(seed_dictionary)
      try:
        self.isis_adjacency_analysis_fd.write(seed_dictionary + "\n")
      except:
        print("Seed dictionary file write failed.")
    return()
###################################################################################################################
