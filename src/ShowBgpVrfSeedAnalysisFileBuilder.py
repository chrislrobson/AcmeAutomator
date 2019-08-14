####################################################################################################################
# Python Qt5 Testbed Tester Show BGP VRF Seed Analysis File Builder
# MODULE:  ShowBgpVrfSeedAnalysisFileBuilder
# Author: Christopher Robson
# Copyright by:  Christopher Robson
# Copyright date: 01Jan2016
# This software is not FREE!  Use or destribution of the software system and its
# subsystem modules, libraries, configuration file and "seed" file without the
# express permission of the author is strictly PROHIBITED!
# FUNCTION:  Module builds a seed file for analysizing collected data.
####################################################################################################################
import datetime
import re
import os, sys, stat
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
# Home grown
#------------------------------------------------------------------------------------------------------------------
from Globals import *
from Exceptions import *
from SeedDictionary import SeedCommandDictionaryProcessor,\
                                                                SeedCommandlinePreprocessor
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
# Show BgpVrf Seed Analysis File Builder
#-----------------------------------------------------------------------
class ShowBgpVrfSeedAnalysisFileBuilder:
  "Show Bgp Vrf Seed Analysis File Builder"
  #----------------------------------------------------------------------------------------------------------------
  def __init__( self, parent = None ):
    self.name = "Show Bgp Vrf Seed Analysis File Builder"
    self.parent = parent
    self.seed = parent.seed
    self.gparent = parent.parent.parent.parent
    self.filename_time_extension = self.parent.filename_time_extension
    self.cmd_list = parent.cmd_list
    self.with_line_numbers = "No"
    self.debug = False
    self.bgp_route_analysis_filename = ""
    self.bgp_route_data_filename = ""
    self.bgp_route_analysis_fd = None
    self.bgp_data_fd = None
    self.prepare_analysis_flag = False
    self.start_analysis_flag = False
    self.start_but_skip_one_analysis_flag = False
    self.address_family_flag = False
    self.empty_address_family_flag = True
    self.bgp_route_table = []
    #-----------------------------------------------------------------------------------------------------------
    self.total_routes = 0
    self.address_family = ""
    self.bgp_router_identifier = ""
    self.bgp_local_AS_number = ""
    self.bgp_generic_scan_interval = ""
    self.bgp_nonstop_routing = ""
    self.bgp_table_state = ""
    self.bgp_table_id = ""
    self.bgp_routing_table_version = ""
    self.bgp_rd_version = ""
    self.bgp_nsr_initsync_version = ""
    self.bgp_nsr_issu_syncgroup_versions = ""
    self.bgp_dampening_mode = ""
    self.bgp_scan_interval = ""
    self.bgp_operating_mode = ""
    self.index = 0
    self.bgp_route_list = []
    self.bgp_route_dict = {"route distiguisher":"","rd vrf":"",
                           "nexthop": "","network/mask":"",
                           "valid":"","status":"","origin":"",
                           "metric": "","localpref": "",
                           "weight": "","path": ""}
  #----------------------------------------------------------------------------------------------------------------
  def execute( self ):
    #----------------------------------------------------------------------------------------------------------------
    self.interfaces_to_match = self.cmd_list[SeedCommandDictionaryProcessor.interfaces]
    self.device_being_matched = self.cmd_list[SeedCommandDictionaryProcessor.device]
    if self.cmd_list[SeedCommandDictionaryProcessor.verbose] == 'Yes':
      self.message_str = \
        "Build Show Bgp Vrf Seed File command started at: {}\n".\
          format( datetime.datetime.now().strftime( "%d%b%Y-%H%M-%S" ) )
      self.gparent.logger_message_signal.emit(self.message_str)
    self.message_str = "Building seed file: {}.".\
          format( self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] )
    self.gparent.logger_message_signal.emit( self.message_str )
    try:
      self.analysis_filename = str( self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] )
      self.bgp_summary_analysis_fd = open( self.analysis_filename, "w+" )
    except:
      raise Exception( "{}: ShowBgpVrfSeedAnalysisFileBuilder file I/O error with \"{}\". "
                       "Build Show Bgp Vrf Seed File Command terminated. ".
                       format( self.name,
                               self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] )  )
    self.data_filename = self.cmd_list[SeedCommandDictionaryProcessor.commandpath] + \
                         self.cmd_list[SeedCommandDictionaryProcessor.commands] + \
                         self.filename_time_extension
    self.device = self.cmd_list[SeedCommandDictionaryProcessor.device]
    if self.device == "":
      raise CriticalFailure( "ShowBgpVrfSeedAnalysisFileBuilder: Invalid seed file!" )
    try:
      # FIXME DEBUG USE with open( "TEST-10.10.9.40-r95-show-bgp-data", "r" ) as self.bgp_data_fd:
      with open( self.data_filename, "r" ) as self.bgp_data_fd:
        for self.bgp_data in self.bgp_data_fd:
          self.index += len( self.bgp_data )
          if self.start_analysis_flag and self.device == "juniper":
            self.reportFD = self.build_juniper_analysis_seed_file()
            self.bgp_summary_analysis_fd.close()
            self.bgp_data_fd.close()
            break
          elif self.start_analysis_flag and self.device == "cisco":
            try:
              self.reportFD = self.build_cisco_analysis_seed_file()
            except Exception as error:
              self.message_str = \
                "Build seed file error: {}\n". \
                  format( error )
              self.gparent.logger_message_signal.emit( self.message_str )
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
      raise Exception( "ShowBgpVrfSeedAnalysisFileBuilder: {}".format(e) )
    #--------------------------------------------------------------------------------------------------------------
    if self.cmd_list[SeedCommandDictionaryProcessor.verbose] == 'Yes':
      self.message_str = \
        "Total routes built in seed file: {}\n".format( self.total_routes )
      self.gparent.processor_message_signal.emit(self.message_str)
    return()
  #----------------------------------------------------------------------------------------------------------------
  # FIXME ANOTHER QUICK AND DIRTY FIX the nesxt two methods should be OOPed!!!!!!
  #----------------------------------------------------------------------------------------------------------------

  #----------------------------------------------------------------------------------------------------------------
  def build_cisco_analysis_seed_file( self ):
    self.bgp_summary_table = []
    for self.bgp_data in self.bgp_data_fd:
      self.index += len( self.bgp_data )
      self.bgp_data_list = self.bgp_data.split()
      if self.bgp_data.startswith( "\n" ):
        continue
      if not self.bgp_data.startswith( "BGP VRF" ):
        try:
          self.bgp_vrf_name = self.bgp_data_list[2].split( "," )[0]
        except:
          self.bgp_vrf_name = ""
        try:
          self.bgp_vrf_state = self.bgp_data_list[4].split( "\n" )[0]
        except:
          self.bgp_vrf_state = ""
        continue
      else:
        for self.bgp_data in self.bgp_data_fd:
          self.index += len( self.bgp_data )
          if self.bgp_data.startswith( "\n" ):
            continue
          else:
            self.empty_address_family_flag = False
            self.address_family = ""
            self.bgp_router_identifier = ""
            self.bgp_local_AS_number = ""
            self.bgp_generic_scan_interval = ""
            self.bgp_nonstop_routing = ""
            self.bgp_table_state = ""
            self.bgp_table_id = ""
            self.bgp_routing_table_version = ""
            self.bgp_rd_version = ""
            self.bgp_nsr_initsync_version = ""
            self.bgp_nsr_issu_syncgroup_versions = ""
            self.bgp_dampening_mode = ""
            self.bgp_scan_interval = ""
            self.bgp_operating_mode = ""
            self.bgp_route_dict["route distiguisher"] = ""
            self.bgp_route_dict["rd vrf"] = ""
            self.bgp_route_dict["nexthop"] = ""
            self.bgp_route_dict["network/mask"] = ""
            self.bgp_route_dict["valid"] = ""
            self.bgp_route_dict["status"] = ""
            self.bgp_route_dict["origin"] = ""
            self.bgp_route_dict["metric"] = ""
            self.bgp_route_dict["localpref"] = ""
            self.bgp_route_dict["weight"] = ""
            self.bgp_route_dict["path"] = ""
            self.address_family = self.bgp_data.split( ":" )[1].split( "\n" )[0]
            for self.bgp_data in self.bgp_data_fd:
              self.index += len( self.bgp_data )
              self.bgp_data_list = self.bgp_data.split()
              if self.bgp_data.startswith( "\n" ):  # NOTE, this must be before bgp_data_list or it traps!!!!
                continue
              """
               RP/0/RSP0/CPU0:R91A-ASR9010#show bgp vrf ABCX79 
               Tue Sep 12 05:28:24.833 EDT
               BGP VRF ABCX79, state: Active
               BGP Route Distinguisher: 27060:79
               VRF ID: 0x60000005
               BGP router identifier 33.20.0.91, local AS number 27064
               Non-stop routing is enabled
               BGP table state: Active
               Table ID: 0xe0000014   RD version: 699426
               BGP main routing table version 699427
               BGP NSR Initial initsync version 63642 (Reached)
               BGP NSR/ISSU Sync-Group versions 699427/0
               """
              if self.bgp_data.startswith( "BGP router identifier" ):
                try:
                  self.bgp_router_identifier = self.bgp_data_list[3].split( "," )[0]
                except:
                  self.bgp_router_identifier = ""
                try:
                  self.bgp_local_AS_number = self.bgp_data_list[7]
                except:
                  self.bgp_local_AS_number = ""
                continue
              if self.bgp_data.startswith( "BGP generic scan interval" ):
                try:
                  self.bgp_generic_scan_interval = self.bgp_data_list[4]
                except:
                  self.bgp_generic_scan_interval = 0
                continue
              if self.bgp_data.startswith( "Non-stop routing" ):
                try:
                  self.bgp_nonstop_routing = self.bgp_data_list[3]
                except:
                  self.bgp_nonstop_routing = ""
                continue
              if self.bgp_data.startswith( "BGP table state" ):
                try:
                  self.bgp_table_state = self.bgp_data_list[3]
                except:
                  self.bgp_table_state = ""
                continue
              if self.bgp_data.startswith( "Table ID" ):
                try:
                  self.bgp_table_id = self.bgp_data_list[2]
                except:
                  self.bgp_table_id = ""
                try:
                  self.bgp_rd_version = self.bgp_data_list[5]
                except:
                  self.bgp_rd_version = ""
                continue
              if self.bgp_data.startswith( "BGP main routing table version" ):
                try:
                  self.bgp_routing_table_version = self.bgp_data_list[5]
                except:
                  self.bgp_routing_table_version = ""
                continue
              if self.bgp_data.startswith( "BGP NSR Initial initsync version" ):
                try:
                  self.bgp_nsr_initsync_version = self.bgp_data_list[5]
                except:
                  self.bgp_nsr_initsync_version = ""
                continue
              if self.bgp_data.startswith( "BGP NSR/ISSU Sync-Group versions" ):
                try:
                  self.bgp_nsr_issu_syncgroup_versions = self.bgp_data_list[4]
                except:
                  self.bgp_nsr_issu_syncgroup_versions = ""
                continue
              if self.bgp_data.startswith( "Dampening" ):
                try:
                  self.bgp_dampening_mode = self.bgp_data_list[1]
                except:
                  self.bgp_dampening_mode = ""
                continue
              if self.bgp_data.startswith( "BGP scan interval" ):
                try:
                  self.bgp_scan_interval = self.bgp_data_list[4]
                except:
                  self.bgp_scan_interval = ""
                continue
              if self.bgp_data.startswith( "BGP is operating" ):
                try:
                  self.bgp_operating_mode = self.bgp_data_list[4]
                except:
                  self.bgp_operating_mode = ""
                continue
              if self.bgp_data.startswith( "Processed" ) and \
                      self.bgp_data.find( "prefixes," ) != -1 and self.bgp_data.find( "paths" ) != -1:
                self.address_family_flag = False
                break
              if self.bgp_data.startswith( "Route Distinguisher:" ):
                try:
                  self.bgp_route_dict["route distiguisher"] = self.bgp_data_list[2].replace( ":", "~" )
                except:
                  self.bgp_route_dict["route distiguisher"] = ""
                try:
                  self.bgp_route_dict["rd vrf"] = self.bgp_data_list[6].split( ")" )[0]
                except:
                  self.bgp_route_dict["rd vrf"] = ""
              for self.bgp_data in self.bgp_data_fd:
                self.index += len( self.bgp_data )
                self.bgp_data_list = self.bgp_data.split()
                if self.bgp_data.startswith( "Processed" ) and \
                   self.bgp_data.find( "prefixes," ) != -1 and self.bgp_data.find( "paths" ) != -1:
                  self.address_family_flag = False
                  break
                if self.bgp_data.startswith( "\n" ):
                  continue
                if self.bgp_data.startswith( "Route Distinguisher:" ):
                  try:
                    self.bgp_route_dict["route distiguisher"] = self.bgp_data_list[2].replace( ":", "~" )
                  except:
                    self.bgp_route_dict["route distiguisher"] = ""
                  try:
                    self.bgp_route_dict["rd vrf"] = self.bgp_data_list[6].split( ")" )[0]
                  except:
                    self.bgp_route_dict["rd vrf"] = ""
                  continue
                try:
                  self.bgp_route_dict["valid"] = self.bgp_data[0]
                except:
                  self.bgp_route_dict["valid"] = " "
                try:
                  self.bgp_route_dict["status"] = self.bgp_data[1]
                except:
                  self.bgp_route_dict["status"] = " "
                try:
                  self.bgp_route_dict["origin"] = self.bgp_data[2]
                except:
                  self.bgp_route_dict["origin"] = " "
                #-------------------------------------------------------------------------------------------------
                # Now have fun decoding the route entries stupid cisco format that it is!
                #-------------------------------------------------------------------------------------------------
                if self.bgp_data[3].isdigit():
                  try:
                    self.bgp_route_dict["network/mask"], \
                    self.bgp_route_dict["nexthop"], \
                    self.bgp_route_dict["metric"], \
                    self.bgp_route_dict["locprf"], \
                    self.bgp_route_dict["weight"] = self.bgp_data[3:62].split()
                    self.bgp_route_dict["path"] = self.bgp_data[63:].split( "\n" )[0]
                    self.total_routes += 1
                  except:
                    if self.bgp_data[3].isdigit():
                      self.bgp_route_dict["network/mask"] = self.bgp_data[3:].split()[0]
                    else:
                      self.bgp_route_dict["network/mask"] = ""
                    if self.bgp_data[22].isdigit():
                      self.bgp_route_dict["nexthop"] = self.bgp_data[22:].split()[0]
                      self.total_routes += 1
                    else:
                      self.bgp_route_dict["nexthop"] = "INVALID NEXTHOP"
                    if re.search( '\d', self.bgp_data[42:48] ):
                      self.bgp_route_dict["metric"] = self.bgp_data[42:].split()[0]
                    else:
                      self.bgp_route_dict["metric"] = "0"
                    if re.search( '\d', self.bgp_data[49:55] ):
                      self.bgp_route_dict["locprf"] = self.bgp_data[49:].split()[0]
                    else:
                      self.bgp_route_dict["locprf"] = "0"
                    if re.search( '\d', self.bgp_data[56:62] ):
                      self.bgp_route_dict["weight"] = self.bgp_data[56:].split()[0]
                    else:
                      self.bgp_route_dict["weight"] = "0"
                    try:
                      self.bgp_route_dict["path"] = self.bgp_data[63:].split( "\n" )[0]
                    except:
                      self.bgp_route_dict["path"] = "?"
                else:
                  try:
                    self.bgp_route_dict["network/mask"] = ""
                    self.bgp_route_dict["nexthop"], \
                    self.bgp_route_dict["metric"], \
                    self.bgp_route_dict["locprf"], \
                    self.bgp_route_dict["weight"] = self.bgp_data[22:62].split()
                    self.bgp_route_dict["path"] = self.bgp_data[63:].split( "\n" )[0]
                    self.total_routes += 1
                  except:
                    if self.bgp_data[22].isdigit():
                      self.bgp_route_dict["nexthop"] = self.bgp_data[22:].split()[0]
                      self.total_routes += 1
                    else:
                      self.bgp_route_dict["nexthop"] = "INVALID NEXTHOP"
                    if re.search( "\d", self.bgp_data[42:48] ):
                      self.bgp_route_dict["metric"] = self.bgp_data[42:].split()[0]
                    else:
                      self.bgp_route_dict["metric"] = "0"
                    if re.search( "\d", self.bgp_data[49:55] ):
                      self.bgp_route_dict["locprf"] = self.bgp_data[49:].split()[0]
                    else:
                      self.bgp_route_dict["locprf"] = "0"
                    if re.search( "\d", self.bgp_data[56:61] ):
                      self.bgp_route_dict["weight"] = self.bgp_data[56:].split()[0]
                    else:
                      self.bgp_route_dict["weight"] = "0"
                    try:
                      self.bgp_route_dict["path"] = self.bgp_data[63:].split( "\n" )[0]
                    except:
                      self.bgp_route_dict["path"] = "?"
                self.bgp_route_list.append( dict( self.bgp_route_dict ) )
                if not self.address_family_flag:
                  break
            if self.empty_address_family_flag:
              continue
            #------------------------------------------------------------------------------------------------------------
            for self.bgp_route_table_entry in self.bgp_route_list:
              self.bgp_route_table.append( "{" + \
                                             "\"show bgp\":\"show bgp\"," \
                                             "\"device\":\"{}\"," \
                                             "\"address family\":\"{}\"," \
                                             "\"router identifier\":\"{}\"," \
                                             "\"local AS number\":\"{}\"," \
                                             "\"generic scan interval\":\"{}\"," \
                                             "\"non-stop routing\":\"{}\"," \
                                             "\"table state\":\"{}\"," \
                                             "\"table id\":\"{}\"," \
                                             "\"routing table version\":\"{}\"," \
                                             "\"rd version\":\"{}\"," \
                                             "\"nsr initsync version\":\"{}\"," \
                                             "\"nsr issu syncgroup versions\":\"{}\"," \
                                             "\"dampening mode\":\"{}\"," \
                                             "\"scan interval\":\"{}\"," \
                                             "\"operating mode\":\"{}\"," \
                                             "\"route distiguisher\":\"{}\"," \
                                             "\"rd vrf\":\"{}\"," \
                                             "\"valid\":\"{}\"," \
                                             "\"status\":\"{}\"," \
                                             "\"origin\":\"{}\"," \
                                             "\"network/mask\":\"{}\"," \
                                             "\"nexthop\":\"{}\"," \
                                             "\"metric\":\"{}\"," \
                                             "\"locprf\":\"{}\"," \
                                             "\"weight\":\"{}\"," \
                                             "\"path\":\"{}\"" \
                                             .format( self.device,
                                                      self.address_family,
                                                      self.bgp_router_identifier,
                                                      self.bgp_local_AS_number,
                                                      self.bgp_generic_scan_interval,
                                                      self.bgp_nonstop_routing,
                                                      self.bgp_table_state,
                                                      self.bgp_table_id,
                                                      self.bgp_routing_table_version,
                                                      self.bgp_rd_version,
                                                      self.bgp_nsr_initsync_version,
                                                      self.bgp_nsr_issu_syncgroup_versions,
                                                      self.bgp_dampening_mode,
                                                      self.bgp_scan_interval,
                                                      self.bgp_operating_mode,
                                                      self.bgp_route_table_entry["route distiguisher"],
                                                      self.bgp_route_table_entry["rd vrf"],
                                                      self.bgp_route_table_entry["valid"],
                                                      self.bgp_route_table_entry["status"],
                                                      self.bgp_route_table_entry["origin"],
                                                      self.bgp_route_table_entry["network/mask"],
                                                      self.bgp_route_table_entry["nexthop"],
                                                      self.bgp_route_table_entry["metric"],
                                                      self.bgp_route_table_entry["locprf"],
                                                      self.bgp_route_table_entry["weight"],
                                                      self.bgp_route_table_entry["path"],
                                                  ) + \
                                           "};")
    for seed_dictionary in self.bgp_route_table:
      # FIXME DEBUG print(seed_dictionary)
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
