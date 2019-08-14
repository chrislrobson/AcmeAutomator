####################################################################################################################
# Python Qt5 Testbed Tester Show BGP VRF Neighbor Seed Analysis File Builder
# MODULE:  ShowBgpVrfNeighborSeedAnalysisFileBuilder
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
# Show Bgp Vrf Neighbor Seed Analysis File Builder
#-----------------------------------------------------------------------
class ShowBgpVrfNeighborSeedAnalysisFileBuilder:
  "Show Bgp Vrf Neighbor Seed Analysis File Builder"
  #----------------------------------------------------------------------------------------------------------------
  def __init__( self, parent = None ):
    self.name = "Show Bgp Vrf Neighbor Seed Analysis File Builder"
    self.parent = parent
    self.seed = parent.seed
    self.gparent = parent.parent.parent.parent
    self.filename_time_extension = self.parent.filename_time_extension
    self.cmd_list = parent.cmd_list
    self.with_line_numbers = "No"
    self.debug = False
    self.bgp_summary_analysis_filename = ""
    self.bgp_summary_data_filename = ""
    self.bgp_summary_analysis_fd = None
    self.bgp_data_fd = None
    self.prepare_analysis_flag = False
    self.start_analysis_flag = False
    self.start_but_skip_one_analysis_flag = False
    self.line_length = 0  # CRITICAL !!!! MUST DO THIS AT INIT TIME !!!!
    self.bgp_vrf_remote_AS = ""
    self.bgp_vrf_local_AS = ""
    self.bgp_vrf_link = ""
    self.bgp_vrf_description = ""
    self.bgp_vrf_remote_router_id = ""
    self.bgp_vrf_state = ""
    self.bgp_vrf_up_time = ""
    self.bgp_vrf_accepted_prefixes = "-1"
    self.bgp_vrf_denied_prefixes = "-1"
    self.bgp_vrf_advertise_prefixes = "-1"
    self.bgp_vrf_suppressed_prefixes = "-1"
    self.bgp_vrf_withdrawn_prefixes = "-1"
    self.bgp_vrf_connections_established = ""
    self.bgp_vrf_connections_dropped = "-1"
    self.bgp_vrf_local_host = ""
    self.bgp_vrf_local_port = ""
    self.bgp_vrf_foreign_host = ""
    self.bgp_vrf_foreign_port = ""
    self.bgp_vrf_dict_list = []
  #----------------------------------------------------------------------------------------------------------------
  def execute( self ):
    #--------------------------------------------------------------------------------------------------------------
    self.interfaces_to_match = self.cmd_list[SeedCommandDictionaryProcessor.interfaces]
    self.device_being_matched = self.cmd_list[SeedCommandDictionaryProcessor.device]
    if self.cmd_list[SeedCommandDictionaryProcessor.verbose] == 'Yes':
      self.message_str = \
        "Build Show Bgp Vrf Neighbor Seed File command started at: {}\n".\
          format( datetime.datetime.now().strftime( "%d%b%Y-%H%M-%S" ) )
      self.gparent.processor_message_signal.emit(self.message_str)
    self.message_str = "Building seed file: {}.".\
          format( self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] )
    self.gparent.logger_message_signal.emit( self.message_str )
    try:
      self.analysis_filename = str( self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] )
      self.bgp_summary_analysis_fd = open( self.analysis_filename, "w+" )
    except:
      raise Exception( "{}: ShowBgpVrfNeighborSeedAnalysisFileBuilder file I/O error with \"{}\". "
                       "Build Show Bgp Vrf Neighbor Seed File Command terminated. ".
                       format( self.name,
                               self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] )  )
    self.data_filename = self.cmd_list[SeedCommandDictionaryProcessor.commandpath] + \
                         self.cmd_list[SeedCommandDictionaryProcessor.commands] + \
                         self.filename_time_extension
    self.device = self.cmd_list[SeedCommandDictionaryProcessor.device]
    if self.device == "":
      raise CriticalFailure( "ShowBgpVrfNeighborSeedAnalysisFileBuilder: Invalid seed file!" )
    try:
      with open( self.data_filename, "r" ) as self.bgp_data_fd:
        for self.bgp_data in self.bgp_data_fd:
          self.line_length += len( self.bgp_data )
          if self.start_analysis_flag and self.device == "juniper":
            self.reportFD = self.build_juniper_analysis_seed_file()
            self.bgp_summary_analysis_fd.close()
            self.bgp_data_fd.close()
            break
          elif self.start_analysis_flag and self.device == "cisco":
            self.reportFD = self.build_cisco_analysis_seed_file()
            self.bgp_summary_analysis_fd.close()
            self.bgp_data_fd.close()
            break
          elif self.bgp_data.startswith( "DUT(" ) and \
               self.bgp_data.find( ")-> show bgp vrf" ) != -1:
            self.start_analysis_flag = True
            continue
          else:
            continue
    except Exception as e:
      raise Exception( "ShowBgpVrfNeighborSeedAnalysisFileBuilder: {}".format(e) )
    return()
  #----------------------------------------------------------------------------------------------------------------
  # FIXME ANOTHER QUICK AND DIRTY FIX the nesxt two methods should be OOPed!!!!!!
  #----------------------------------------------------------------------------------------------------------------
  def build_cisco_analysis_seed_file( self ):
    for self.bgp_data in self.bgp_data_fd:
      self.line_length += len( self.bgp_data )
      if self.bgp_data.startswith( "\n" ):
        continue
      else:
        self.bgp_data_list = self.bgp_data.split()
        if self.bgp_data.startswith( "BGP neighbor is" ):
          try:
            self.bgp_vrf_name = self.bgp_data_list[5]
          except:
            self.bgp_vrf_name = ""
          try:
            self.bgp_vrf_neighbor = self.bgp_data_list[3].split( "," )[0]
          except:
            self.bgp_vrf_neighbor = ""
          #---------------------------------------------------------------------------------------------------------
          # Now cycle thru this neighbor
          for self.bgp_data in self.bgp_data_fd:
            if self.bgp_data.startswith( "VRF:" ) or \
               self.bgp_data.startswith( "BGP neighbor is" ):
              self.bgp_data_fd.seek( self.line_length )
              break  # done with this neighbor
            self.line_length += len( self.bgp_data )
            self.bgp_data_list = self.bgp_data.split()
            if self.bgp_data.startswith( "\n" ):
              continue
            if self.bgp_data.startswith( " Remote AS" ):
              try:
                self.bgp_vrf_remote_AS = self.bgp_data_list[2].split( "," )[0]
              except:
                self.bgp_vrf_remote_AS = ""
              try:
                self.bgp_vrf_local_AS = self.bgp_data_list[5].split( "," )[0]
              except:
                self.bgp_vrf_local_AS = ""
              try:
                self.bgp_vrf_link = self.bgp_data.split( "," )[2].split( "\n" )[0][1:]
              except:
                self.bgp_vrf_link = ""
              continue
            if self.bgp_data.startswith( " Description" ):
              try:
                self.bgp_vrf_description = self.bgp_data.split( ":" )[1].replace( "\"", "" ).split( "\n" )[0]
              except:
                self.bgp_vrf_description = ""
              continue
            if self.bgp_data.startswith( " Remote router ID" ):
              try:
                self.bgp_vrf_remote_router_id = self.bgp_data_list[3]
              except:
                self.bgp_vrf_remote_router_id = ""
              for self.bgp_data in self.bgp_data_fd:
                if self.bgp_data.startswith( "VRF:" ) or \
                   self.bgp_data.startswith( " For Address Family:" ) or \
                   self.bgp_data.startswith( "BGP neighbor is" ):
                  self.bgp_data_fd.seek( self.line_length )
                  break  # done with this neighbor
                self.line_length += len( self.bgp_data )
                self.bgp_data_list = self.bgp_data.split()
                if self.bgp_data.startswith( "\n" ):
                  continue
                if self.bgp_data.startswith( "  BGP state" ):
                  try:
                    self.bgp_vrf_state = self.bgp_data_list[3].split( "," )[0]
                  except:
                    self.bgp_vrf_state = ""
                  try:
                    self.bgp_vrf_up_time = self.bgp_data_list[6]
                  except:
                    self.bgp_vrf_up_time = ""
                  continue
              continue
            if self.bgp_data.startswith( " For Address Family:" ):
              for self.bgp_data in self.bgp_data_fd:
                if self.bgp_data.startswith( "VRF:" ) or \
                   self.bgp_data.startswith( " For Address Family:" ) or \
                   self.bgp_data.startswith( "BGP neighbor is" ):
                  self.bgp_data_fd.seek( self.line_length )
                  break  # done with this neighbor
                self.line_length += len( self.bgp_data )
                self.bgp_data_list = self.bgp_data.split()
                if self.bgp_data.startswith( "\n" ):
                  continue
                if self.bgp_data.find( "accepted prefixes," ) != -1:
                  try:
                    self.bgp_vrf_accepted_prefixes = self.bgp_data_list[0]
                  except:
                    self.bgp_vrf_accepted_prefixes = "-1"
                  continue
                if self.bgp_data.startswith( "  Cumulative no. of prefixes denied:" ):
                  try:
                    self.bgp_vrf_denied_prefixes = self.bgp_data_list[5].split( "." )[0]
                  except:
                    self.bgp_vrf_denied_prefixes = "-1"
                  continue
                if self.bgp_data.startswith( "  Prefix advertised" ):
                  try:
                    self.bgp_vrf_advertise_prefixes = self.bgp_data_list[2].split( "," )[0]
                  except:
                    self.bgp_vrf_advertise_prefixes = "-1"
                  try:
                    self.bgp_vrf_suppressed_prefixes = self.bgp_data_list[4].split( "," )[0]
                  except:
                    self.bgp_vrf_suppressed_prefixes = "-1"
                  try:
                    self.bgp_vrf_withdrawn_prefixes = self.bgp_data_list[6].split( "\n" )[0]
                  except:
                    self.bgp_vrf_withdrawn_prefixes = "-1"
                  continue
                if self.bgp_data.startswith( "  Connections established" ):
                  try:
                    self.bgp_vrf_connections_established = self.bgp_data_list[2].split( ";" )[0]
                  except:
                    self.bgp_vrf_connections_established = "0"
                  try:
                    self.bgp_vrf_connections_dropped = self.bgp_data_list[4].split( "\n" )[0]
                  except:
                    self.bgp_vrf_connections_dropped = "-1"
                  continue
                if self.bgp_data.startswith( "  Local host" ):
                  try:
                    self.bgp_vrf_local_host = self.bgp_data_list[2].split( "," )[0]
                  except:
                    self.bgp_vrf_local_host = "0"
                  try:
                    self.bgp_vrf_local_port = self.bgp_data_list[5].split( "," )[0]
                  except:
                    self.bgp_vrf_local_port = "0"
                  continue
                if self.bgp_data.startswith( "  Foreign host" ):
                  try:
                    self.bgp_vrf_foreign_host = self.bgp_data_list[2].split( "," )[0]
                  except:
                    self.bgp_vrf_foreign_host = "0"
                  try:
                    self.bgp_vrf_foreign_port = self.bgp_data_list[5].split( "\n" )[0]
                  except:
                    self.bgp_vrf_foreign_port = "0"
                  continue
          if self.cmd_list[SeedCommandDictionaryProcessor.initializedata] == 'No' or \
                  self.cmd_list[SeedCommandDictionaryProcessor.initializedata] == 'AllCounters':
            self.bgp_vrf_accepted_prefixes = "-1"
            self.bgp_vrf_denied_prefixes = "-1"
            self.bgp_vrf_advertise_prefixes = "-1"
            self.bgp_vrf_suppressed_prefixes = "-1"
            self.bgp_vrf_withdrawn_prefixes = "-1"
            self.bgp_vrf_connections_established = "0"
            self.bgp_vrf_connections_dropped = "-1"
          self.bgp_vrf_dict_list.append( "{{"
                                         "\"show bgp vrf all neighbors detail\":" \
                                         "\"show bgp vrf all neighbors detail\"," \
                                         "\"device\":\"{}\"," \
                                         "\"name\":\"{}\"," \
                                         "\"neighbor\":\"{}\"," \
                                         "\"remote AS\":\"{}\"," \
                                         "\"local AS\":\"{}\"," \
                                         "\"link\":\"{}\"," \
                                         "\"description\":\"{}\"," \
                                         "\"remote router id\":\"{}\"," \
                                         "\"state\":\"{}\"," \
                                         "\"up time\":\"{}\"," \
                                         "\"accepted prefixes\":\"{}\"," \
                                         "\"denied prefixes\":\"{}\"," \
                                         "\"advertise prefixes\":\"{}\"," \
                                         "\"suppressed prefixes\":\"{}\"," \
                                         "\"withdrawn prefixes\":\"{}\"," \
                                         "\"connections established\":\"{}\"," \
                                         "\"connections dropped\":\"{}\"," \
                                         "\"local host\":\"{}\"," \
                                         "\"local port\":\"{}\"," \
                                         "\"foreign host\":\"{}\"," \
                                         "\"foreign port\":\"{}\"}};".format(
                                                                         self.device,
                                                                         self.bgp_vrf_name,
                                                                         self.bgp_vrf_neighbor,
                                                                         self.bgp_vrf_remote_AS,
                                                                         self.bgp_vrf_local_AS,
                                                                         self.bgp_vrf_link,
                                                                         self.bgp_vrf_description,
                                                                         self.bgp_vrf_remote_router_id,
                                                                         self.bgp_vrf_state,
                                                                         self.bgp_vrf_up_time,
                                                                         self.bgp_vrf_accepted_prefixes,
                                                                         self.bgp_vrf_denied_prefixes,
                                                                         self.bgp_vrf_advertise_prefixes,
                                                                         self.bgp_vrf_suppressed_prefixes,
                                                                         self.bgp_vrf_withdrawn_prefixes,
                                                                         self.bgp_vrf_connections_established,
                                                                         self.bgp_vrf_connections_dropped,
                                                                         self.bgp_vrf_local_host,
                                                                         self.bgp_vrf_local_port,
                                                                         self.bgp_vrf_foreign_host,
                                                                         self.bgp_vrf_foreign_port
                                    ) )
    for seed_dictionary in self.bgp_vrf_dict_list:
      # FIXME DEBUG -> print(seed_dictionary)
      try:
        self.bgp_summary_analysis_fd.write(seed_dictionary + "\n")
      except:
        print("Seed dictionary file write failed.")
    return()
  #----------------------------------------------------------------------------------------------------------------
  #----------------------------------------------------------------------------------------------------------------
  def build_juniper_analysis_seed_file( self ):
    bgp_summary_table = []
    for self.bgp_data in self.bgp_data_fd:
      if self.bgp_data.startswith( "\n" ):
        break
      else:
        try:
          self.interface = self.bgp_data.split()[0]
        except:
          self.interface = ""
        try:
          self.system = self.bgp_data.split()[1]
        except:
          self.system = ""
        try:
          self.level = self.bgp_data.split()[2]
        except:
          self.level = ""
        try:
          self.state = self.bgp_data.split()[3]
        except:
          self.state = ""
        try:
          self.hold = self.bgp_data.split()[4]
        except:
          self.hold = ""
        try:
          self.snpa = self.bgp_data.split()[5]
        except:
          self.snpa = ""
        bgp_summary_table.append( "{" + \
                                     "\"show bgp summary\":\"show_bgp_summary\",\"device\":\"juniper\"," \
                                     "\"interface\":\"{}\",\"system\":\"{}\"," \
                                     "\"level\":\"{}\",\"state\":\"{}\"," \
                                     "\"hold\":\"{}\",\"snpa\":\"{}\"".format( self.interface,
                                                                               self.system,
                                                                               self.level,
                                                                               self.state,
                                                                               self.hold,
                                                                               self.snpa ) + \
                                     "};")
    for seed_dictionary in bgp_summary_table:
      # FIXME DEBUG print(seed_dictionary)
      try:
        self.bgp_summary_analysis_fd.write(seed_dictionary + "\n")
      except:
        print("Seed dictionary file write failed.")
    return()
###################################################################################################################
