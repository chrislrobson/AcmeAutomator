####################################################################################################################
# Python Qt5 Testbed Tester Show BGP Summary Seed Analysis File Builder
# MODULE:  ShowBgpSummarySeedAnalysisFileBuilder
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
# Show Bgp Summary Seed Analysis File Builder
#-----------------------------------------------------------------------
class ShowBgpSummarySeedAnalysisFileBuilder:
  "Show Bgp Summary Seed Analysis File Builder"
  #----------------------------------------------------------------------------------------------------------------
  def __init__( self, parent = None ):
    self.name = "Show Bgp Summary Seed Analysis File Builder"
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
    self.bgp_summary_table = []
    #-----------------------------------------------------------------------------------------------------------
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
    self.bgp_StandbyVer = ""
    self.bgp_SendTblVer = ""
    self.bgp_ImportVer = ""
    self.bgp_LabelVer = ""
    self.bgp_bRIBRIB = ""
    self.bgp_RcvTblVer = ""
    self.neighbor_list = []
    self.neighbor_dict = {"Neighbor":"", "Spk": "", "AS": "",
                          "MsgRcvd": "", "MsgSent": "", "TblVer": "",
                          "InQ": "", "OutQ": "",
                          "Up/Down": "","St/PfxRcd": ""}
  #----------------------------------------------------------------------------------------------------------------
  def execute( self ):
    #----------------------------------------------------------------------------------------------------------------
    self.interfaces_to_match = self.cmd_list[SeedCommandDictionaryProcessor.interfaces]
    self.device_being_matched = self.cmd_list[SeedCommandDictionaryProcessor.device]
    if self.cmd_list[SeedCommandDictionaryProcessor.verbose] == 'Yes':
      self.message_str = \
        "Build Show Bgp Summary Seed File command started at: {}\n".\
          format( datetime.datetime.now().strftime( "%d%b%Y-%H%M-%S" ) )
      self.gparent.processor_message_signal.emit(self.message_str)
    self.message_str = "Building seed file: {}.".\
          format( self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] )
    self.gparent.logger_message_signal.emit( self.message_str )
    try:
      self.analysis_filename = str( self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] )
      self.bgp_summary_analysis_fd = open( self.analysis_filename, "w+" )
    except:
      raise Exception( "{}: ShowBgpSummarySeedAnalysisFileBuilder file I/O error with \"{}\". "
                       "Build Show Bgp Summary Seed File Command terminated. ".
                       format( self.name,
                               self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] )  )
    self.data_filename = self.cmd_list[SeedCommandDictionaryProcessor.commandpath] + \
                         self.cmd_list[SeedCommandDictionaryProcessor.commands] + \
                         self.filename_time_extension
    self.device = self.cmd_list[SeedCommandDictionaryProcessor.device]
    if self.device == "":
      raise CriticalFailure( "ShowBgpSummarySeedAnalysisFileBuilder: Invalid seed file!" )
    try:
      with open( self.data_filename, "r" ) as self.bgp_data_fd:
        for self.bgp_data in self.bgp_data_fd:
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
               self.bgp_data.find( ")-> show bgp summary" ) != -1:
            self.start_analysis_flag = True
            continue
          else:
            continue
    except Exception as e:
      raise Exception( "ShowBgpSummarySeedAnalysisFileBuilder: {}".format(e) )
    return()
  #----------------------------------------------------------------------------------------------------------------
  # FIXME ANOTHER QUICK AND DIRTY FIX the nesxt two methods should be OOPed!!!!!!
  #----------------------------------------------------------------------------------------------------------------
  #----------------------------------------------------------------------------------------------------------------
  def build_cisco_analysis_seed_file( self ):
    self.bgp_summary_table = []
    for self.bgp_data in self.bgp_data_fd:
      if self.bgp_data.startswith( "\n" ):
        continue
      else:
        self.bgp_data_list = self.bgp_data.split()
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
        if self.bgp_data.startswith( "Speaker" ):
          try:
            self.bgp_RcvTblVer = self.bgp_data_list[4]
          except:
            self.bgp_RcvTblVer = ""
          try:
            self.bgp_bRIB_RIB = self.bgp_data_list[4]
          except:
            self.bgp_bRIB_RIB = ""
          try:
            self.bgp_LabelVer = self.bgp_data_list[4]
          except:
            self.bgp_LabelVer = ""
          try:
            self.bgp_ImportVer = self.bgp_data_list[4]
          except:
            self.bgp_ImportVer = ""
          try:
            self.bgp_SendTblVer = self.bgp_data_list[4]
          except:
            self.bgp_SendTblVer = ""
          try:
            self.bgp_StandbyVer = self.bgp_data_list[4]
          except:
            self.bgp_StandbyVer = ""
          continue
        if self.bgp_data.startswith( "Neighbor" ):
          for self.bgp_data in self.bgp_data_fd:
            if self.bgp_data.startswith( "\n" ):
              continue
            else:
              self.neighbor_dict["Neighbor"], \
              self.neighbor_dict["Spk"], \
              self.neighbor_dict["AS"], \
              self.neighbor_dict["MsgRcvd"], \
              self.neighbor_dict["MsgSent"], \
              self.neighbor_dict["TblVer"], \
              self.neighbor_dict["InQ"],\
              self.neighbor_dict["OutQ"], \
              self.neighbor_dict["Up/Down"], \
              self.neighbor_dict["St/PfxRcd"] \
                = self.bgp_data.split()
              self.neighbor_dict["Up/Down"] = self.neighbor_dict["Up/Down"].replace( ":", "~" )
              self.neighbor_list.append( dict( self.neighbor_dict ) )
    #------------------------------------------------------------------------------------------------------------
    for self.neighbor_ip in self.neighbor_list:
      self.bgp_summary_table.append( "{" + \
                                   "\"show bgp summary\":\"show bgp summary\"," \
                                   "\"device\":\"{}\"," \
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
                                   "\"StandbyVer\":\"{}\"," \
                                   "\"SendTblVer\":\"{}\"," \
                                   "\"ImportVer\":\"{}\"," \
                                   "\"LabelVer\":\"{}\"," \
                                   "\"bRIBRIB\":\"{}\"," \
                                   "\"RcvTblVer\":\"{}\"," \
                                   "\"Neighbor\":\"{}\"," \
                                   "\"Spk\":\"{}\"," \
                                   "\"AS\":\"{}\"," \
                                   "\"MsgRcvd\":\"{}\"," \
                                   "\"MsgSent\":\"{}\"," \
                                   "\"TblVer\":\"{}\"," \
                                   "\"InQ\":\"{}\"," \
                                   "\"OutQ\":\"{}\"," \
                                   "\"Up/Down\":\"{}\"," \
                                   "\"St/PfxRcd\":\"{}\"".format( self.device,
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
                                                                  self.bgp_StandbyVer,
                                                                  self.bgp_SendTblVer,
                                                                  self.bgp_ImportVer,
                                                                  self.bgp_LabelVer,
                                                                  self.bgp_bRIBRIB,
                                                                  self.bgp_RcvTblVer,
                                                                  self.neighbor_ip["Neighbor"],
                                                                  self.neighbor_ip["Spk"],
                                                                  self.neighbor_ip["AS"],
                                                                  self.neighbor_ip["MsgRcvd"],
                                                                  self.neighbor_ip["MsgSent"],
                                                                  self.neighbor_ip["TblVer"],
                                                                  self.neighbor_ip["InQ"],
                                                                  self.neighbor_ip["OutQ"],
                                                                  self.neighbor_ip["Up/Down"],
                                                                  self.neighbor_ip["St/PfxRcd"]) + \
                                   "};")
    else:
      self.bgp_summary_table.append( "{" + \
                                     "\"show bgp summary\":\"show bgp summary\"," \
                                     "\"device\":\"{}\"," \
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
                                     "\"operating mode\":\"{}\",". \
                                                            format( self.device,
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
                                                                    self.bgp_operating_mode
                                                                   ) + \
                                     "};")
    for seed_dictionary in self.bgp_summary_table:
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
