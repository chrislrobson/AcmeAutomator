####################################################################################################################
# Python Qt5 Testbed Tester Show MPLS TrafficEng Tunnels Lsp Seed Analysis File Builder
# MODULE:  ShowMplsTrafficEngTunnelsLspSeedAnalysisFileBuilder
# Author: Christopher Robson
# Copyright by:  Christopher Robson
# Copyright date: 01Jan2016
# This software is not FREE!  Use or destribution of the software system and its
# subsystem modules, libraries, configuration file and "seed" file without the
# express permission of the author is strictly PROHIBITED!
# FUNCTION:  Module builds a seed file for analysizing collected data.
####################################################################################################################
import datetime
import binascii
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
# Show Mpls TrafficEng Tunnels Lsp Seed Analysis File Builder
#-----------------------------------------------------------------------
class ShowMplsTrafficEngTunnelsLspSeedAnalysisFileBuilder:
  "Show Mpls TrafficEng Tunnels Lsp Seed Analysis File Builder"
  #----------------------------------------------------------------------------------------------------------------
  def __init__( self, parent = None ):
    self.skiper = 0
    self.name = "Show Mpls TrafficEng Tunnels Lsp Seed Analysis File Builder"
    self.parent = parent
    self.seed = parent.seed
    self.gparent = parent.parent.parent.parent
    self.filename_time_extension = self.parent.filename_time_extension
    self.cmd_list = parent.cmd_list
    self.with_line_numbers = "No"
    self.debug = False
    self.mpls_analysis_filename = ""
    self.mpls_data_filename = ""
    self.mpls_analysis_fd = None
    self.mpls_data_fd = None
    self.prepare_analysis_flag = False
    self.start_analysis_flag = False
    self.start_but_skip_one_analysis_flag = False
    self.mpls_table = []
    #-----------------------------------------------------------------------------------------------------------
    self.line_length = 0  # CRITICAL !!!! MUST DO THIS AT INIT TIME !!!!
    #-----------------------------------------------------------------------------------------------------------
    self.mpls_tunnel_type_received = ""
    self.mpls_name_received = ""
    self.mpls_lsp_id_received = ""
    self.mpls_destination_address_received = ""
    self.mpls_source_address_received = ""
    self.mpls_state_received = ""
    self.mpls_frr_state_received = ""
    self.mpls_lsp_role_received = ""
    self.mpls_path_protocol_received = ""
  #----------------------------------------------------------------------------------------------------------------
  def execute( self ):
    #----------------------------------------------------------------------------------------------------------------
    self.interfaces_to_match = self.cmd_list[SeedCommandDictionaryProcessor.interfaces]
    self.device_being_matched = self.cmd_list[SeedCommandDictionaryProcessor.device]
    if self.cmd_list[SeedCommandDictionaryProcessor.verbose] == 'Yes':
      self.message_str = \
        "Build Show Mpls TrafficEng Tunnels Lsp Seed File command started at: {}\n".\
          format( datetime.datetime.now().strftime( "%d%b%Y-%H%M-%S" ) )
      self.gparent.processor_message_signal.emit(self.message_str)
    self.message_str = "Building seed file: {}.".\
          format( self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] )
    self.gparent.logger_message_signal.emit( self.message_str )
    try:
      self.analysis_filename = str( self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] )
      self.mpls_analysis_fd = open( self.analysis_filename, "w+" )
    except:
      raise Exception( "{}: ShowMplsTrafficEngTunnelsLspSeedAnalysisFileBuilder file I/O error with \"{}\". "
                       "Build Show Mpls TrafficEng Tunnels Lsp Seed File Command terminated. ".
                       format( self.name,
                               self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] )  )
    self.data_filename = self.cmd_list[SeedCommandDictionaryProcessor.commandpath] + \
                         self.cmd_list[SeedCommandDictionaryProcessor.commands] + \
                         self.filename_time_extension
    self.device = self.cmd_list[SeedCommandDictionaryProcessor.device]
    if self.device == "":
      raise CriticalFailure( "ShowMplsTrafficEngTunnelsLspSeedAnalysisFileBuilder: Invalid seed file!" )
    try:
      with open( self.data_filename, "r" ) as self.mpls_data_fd:
        for self.mpls_data in self.mpls_data_fd:
          self.line_length += len( self.mpls_data )
          if self.start_analysis_flag and self.device == "juniper":
            self.reportFD = self.build_juniper_analysis_seed_file()
            self.mpls_analysis_fd.close()
            self.mpls_data_fd.close()
            break
          elif self.start_analysis_flag and self.device == "cisco":
            self.reportFD = self.build_cisco_analysis_seed_file()
            self.mpls_analysis_fd.close()
            self.mpls_data_fd.close()
            break
          elif self.mpls_data.startswith( "DUT(" ) and \
               self.mpls_data.find( ")-> show mpls traffic-eng tunnels" ) != -1:
            self.start_analysis_flag = True
            continue
          else:
            continue
    except Exception as e:
      raise Exception( "ShowMplsTrafficEngTunnelsLspSeedAnalysisFileBuilder: {}".format(e) )
    return()
  #----------------------------------------------------------------------------------------------------------------
  # FIXME ANOTHER QUICK AND DIRTY FIX the nesxt two methods should be OOPed!!!!!!
  #----------------------------------------------------------------------------------------------------------------
  def build_cisco_analysis_seed_file( self ):
    self.mpls_table = []
    self.tunnel_process_completed_flag = False
    self.mpls_tunnel_id_received = ""
    self.mpls_tunnel_number_received = ""
    self.mpls_tunnel_unspec_field_received = ""
    self.mpls_tunnel_state_received = ""
    self.mpls_tunnel_signalling_status_received = ""
    self.mpls_tunnel_name_received = ""
    self.mpls_tunnel_role_received = ""
    self.mpls_inlabel_address_received = ""
    self.mpls_inlabel_type_received = ""
    self.mpls_signal_source_address_received = ""
    self.mpls_signal_destination_address_received = ""
    self.mpls_signal_tunnel_id_received = ""
    self.mpls_signal_tunnel_inst_received = ""
    self.mpls_signal_external_id_received = ""
    self.mpls_signal_router_id_upstream_id_received = ""
    self.mpls_signal_router_id_local_id_received = ""
    self.mpls_signal_bandwidth_received = ""
    self.mpls_signal_class_type_received = ""
    self.mpls_signal_priority_received = ""
    self.mpls_signal_dste_class_received = ""
    self.mpls_signal_soft_preempt_received = ""
    self.mpls_signal_srlgs_received = ""
    self.mpls_path_incoming_address_received = ""
    self.mpls_path_explicit_incoming_route_received = ""
    self.mpls_path_explicit_outgoing_route_received = ""
    self.mpls_path_record_route_state_received = ""
    self.mpls_path_record_route_entries_received = ""
    self.mpls_path_avg_rate_received = ""
    self.mpls_path_burst_received = ""
    self.mpls_path_peak_rate_received = ""
    self.mpls_path_session_local_prot_state_received = ""
    self.mpls_path_session_node_prot_state_received = ""
    self.mpls_path_session_bw_prot_state_received = ""
    self.mpls_path_session_soft_preemption_state_received = ""
    self.mpls_path_session_soft_preemption_state_received = ""
    self.mpls_reserve_info_received = ""
    self.mpls_reserver_info_received = ""
    self.mpls_reserve_record_route_state_received = ""
    self.mpls_reserve_record_route_entries_received = ""
    self.mpls_reserve_fspec_avg_rate_received = ""
    self.mpls_reserve_fspec_burst_received = ""
    self.mpls_reserve_fspec_peak_rate_received = ""
    for self.mpls_data in self.mpls_data_fd:
      self.line_length += len( self.mpls_data )
      self.mpls_data_list = self.mpls_data.split()
      #---------------------------------------------------------------------------------------------------------
      # Order of checking things is important, aka, look first for ending of data signaled by "Displayed" string
      # Next blank lines then skip anything NOT "LSP Tunnel" string
      #---------------------------------------------------------------------------------------------------------
      if self.mpls_data.startswith( "Displayed " ):
        break
      if self.mpls_data.startswith( "\n" ):
        continue
      if not self.mpls_data.startswith( "LSP Tunnel" ):
        continue
      else:
        self.tunnel_process_completed_flag = True
        self.mpls_tunnel_id_received = self.mpls_data_list[2]
        self.mpls_tunnel_number_received = self.mpls_data_list[3]
        self.mpls_tunnel_unspec_field_received = self.mpls_data_list[4].replace( "[", "" ).replace( "]", "" )
        self.mpls_tunnel_state_received = self.mpls_data_list[6].split( "," )[0]
        self.mpls_tunnel_signalling_status_received = self.mpls_data_list[9]
        for self.mpls_data in self.mpls_data_fd:
          if self.mpls_data.startswith( "LSP Tunnel" ) or \
             self.mpls_data.startswith( "Displayed " ):
            self.mpls_data_fd.seek( self.line_length )
            break
          self.line_length += len( self.mpls_data )
          self.mpls_data_list = self.mpls_data.split()
          if self.mpls_data.startswith( "\n" ):
            continue
          if self.mpls_data[2:].startswith( "Tunnel Name" ):
            try:
              self.mpls_tunnel_name_received = self.mpls_data_list[2].replace( ":", "~" )
            except:
              self.mpls_tunnel_name_received = ""
            try:
              self.mpls_tunnel_role_received = self.mpls_data_list[5]
            except:
              self.mpls_tunnel_role_received = ""
            continue
          if self.mpls_data[2:].startswith( "InLabel" ):
            try:
              self.mpls_inlabel_address_received = self.mpls_data_list[1].split( "," )[0]
            except:
              self.mpls_inlabel_address_received = ""
            continue
          if self.mpls_data[2:].startswith( "OutLabel" ):
            try:
              self.mpls_outlabel_address_received = self.mpls_data_list[1].split( "," )[0]
            except:
              self.mpls_outlabel_address_received = ""
            continue
          if self.mpls_data[2:].startswith( "Signalling Info:" ):
            for self.mpls_data in self.mpls_data_fd:
              if self.mpls_data.startswith( "LSP Tunnel" ) or \
                 self.mpls_data.startswith( "Displayed " ):
                self.mpls_data_fd.seek( self.line_length )
                break
              self.line_length += len( self.mpls_data )
              self.mpls_data_list = self.mpls_data.split()
              if self.mpls_data[4:].startswith( "Src" ):
                try:
                  self.mpls_signal_source_address_received = self.mpls_data_list[1]
                except:
                  self.mpls_signal_source_address_received = ""
                try:
                  self.mpls_signal_destination_address_received = self.mpls_data_list[3].split( "," )[0]
                except:
                  self.mpls_signal_destination_address_received = ""
                try:
                  self.mpls_signal_tunnel_id_received = self.mpls_data_list[6].split( "," )[0]
                except:
                  self.mpls_signal_tunnel_id_received = ""
                try:
                  self.mpls_signal_tunnel_inst_received = self.mpls_data_list[9].split( "," )[0]
                except:
                  self.mpls_signal_tunnel_inst_received = ""
                try:
                  self.mpls_signal_external_id_received = self.mpls_data_list[12]
                except:
                  self.mpls_signal_external_id_received = ""
                continue
              if self.mpls_data[4:].startswith( "Router-IDs" ):
                try:
                  self.mpls_signal_router_id_upstream_id_received = self.mpls_data_list[2]
                except:
                  self.mpls_signal_router_id_upstream_id_received = ""
                for self.mpls_data in self.mpls_data_fd:
                  if self.mpls_data[4:].startswith( "Bandwidth" ):
                    self.mpls_data_fd.seek( self.line_length )
                    break
                  self.line_length += len( self.mpls_data )
                  self.mpls_data_list = self.mpls_data.split()
                  if self.mpls_data_list[0].startswith( "local" ):
                    try:
                      self.mpls_signal_router_id_local_id_received = self.mpls_data_list[1]
                    except:
                      self.mpls_signal_router_id_local_id_received = ""
                    continue
                  if self.mpls_data_list[0].startswith( "downstream" ):
                    try:
                      self.mpls_signal_router_id_downstream_id_received = self.mpls_data_list[1]
                    except:
                      self.mpls_signal_router_id_downstream_id_received = ""
                continue
              if self.mpls_data[4:].startswith( "Bandwidth" ):
                try:
                  self.mpls_signal_bandwidth_received = "{} {}".format( self.mpls_data_list[1],
                                                                        self.mpls_data_list[2] )
                except:
                  self.mpls_signal_bandwidth_received = ""
                try:
                  self.mpls_signal_class_type_received = self.mpls_data_list[3].replace( "(", "" ).replace( ")", "" )
                except:
                  self.mpls_signal_class_type_received = ""
                try:
                  self.mpls_signal_priority_received = "{} {}".format( self.mpls_data_list[5], self.mpls_data_list[6] )
                except:
                  self.mpls_signal_priority_received = ""
                try:
                  self.mpls_signal_dste_class_received = self.mpls_data_list[8]
                except:
                  self.mpls_signal_dste_class_received = ""
                continue
              if self.mpls_data[4:].startswith( "Soft Preemption" ):
                try:
                  self.mpls_signal_soft_preempt_received = self.mpls_data_list[2]
                except:
                  self.mpls_signal_soft_preempt_received = ""
                continue
              if self.mpls_data[4:].startswith( "SRLGs" ):
                try:
                  self.mpls_signal_srlgs_received = self.mpls_data[11:-1]
                except:
                  self.mpls_signal_srlgs_received = ""
                continue
              #---------------------------------------------------------------------------------------------------
              #---------------------------------------------------------------------------------------------------
              if self.mpls_data[4:].startswith( "Path Info" ):
                self.path_record_route = 0
                for self.mpls_data in self.mpls_data_fd:
                  if self.mpls_data[4:].startswith( "Resv Info" ):
                    self.mpls_data_fd.seek( self.line_length )
                    break
                  self.line_length += len( self.mpls_data )
                  self.mpls_data_list = self.mpls_data.split()
                  if self.mpls_data.startswith( "\n" ):
                    continue
                  if self.mpls_data[6:].startswith( "Incoming Address" ):
                    try:
                      self.mpls_path_incoming_address_received = self.mpls_data_list[2]
                    except:
                      self.mpls_path_incoming_address_received = ""
                    continue
                  if self.mpls_data[6:].startswith( "Incoming" ):
                    for self.mpls_data in self.mpls_data_fd:
                      #---------------------------------------------------------
                      # FIXME THE NEXT LINE IS BECAUSE CISCO CODE IS FUCKED UP
                      # The output string for "Explicit Route" string is NOT
                      # indented... how utterly brain dead!!!!!
                      #---------------------------------------------------------
                      self.mpls_data_mod = " ".join( self.mpls_data.split() )
                      if self.mpls_data[6:].startswith( "Record Route" ):
                        self.mpls_data_fd.seek( self.line_length )
                        break
                      if self.mpls_data[6:].startswith( "Outgoing" ):
                        self.mpls_data_fd.seek( self.line_length )
                        break
                      self.line_length += len( self.mpls_data )
                      self.mpls_data_list = self.mpls_data.split()
                      if self.mpls_data.startswith( "\n" ):
                        continue
                      if self.mpls_data_mod.startswith( "Explicit Route" ):
                        continue
                      try:
                        self.mpls_path_explicit_incoming_route_received += \
                        self.mpls_data_list[1] + " "
                      except:
                        pass
                      continue
                    continue
                  if self.mpls_data[6:].startswith( "Outgoing" ):
                    for self.mpls_data in self.mpls_data_fd:
                      self.mpls_data_mod = " ".join( self.mpls_data.split() )
                      if self.mpls_data[6:].startswith( "Resv Info" ):
                        self.mpls_data_fd.seek( self.line_length )
                        break
                      if self.mpls_data[6:].startswith( "Record Route" ):
                        self.mpls_data_fd.seek( self.line_length )
                        break
                      self.line_length += len( self.mpls_data )
                      self.mpls_data_list = self.mpls_data.split()
                      if self.mpls_data.startswith( "\n" ):
                        continue
                      if self.mpls_data_mod.startswith( "Explicit Route" ):
                        continue
                      try:
                        self.mpls_path_explicit_outgoing_route_received += \
                        self.mpls_data_list[1] + " "
                      except:
                        pass
                      continue
                    continue
                  if self.mpls_data[6:].startswith( "Record Route" ):
                    try:
                      self.mpls_path_record_route_state_received = \
                      self.mpls_data.split( ":" )[1].split( "\n" )[0].split()[0]
                    except:
                      self.mpls_path_record_route_state_received = ""
                    for self.mpls_data in self.mpls_data_fd:
                      self.path_record_route += 1
                      if self.mpls_data[6:].startswith( "Tspec" ):
                        if self.mpls_path_record_route_state_received.find( "Disabled" ):
                          self.mpls_path_record_route_entry_received = \
                               "\"path record route \"{}\":".format( self.path_record_route ) + \
                               "{\"inet\":\"\"," \
                               "\"ip\":\"\"," \
                               "\"flags\":\"\"," \
                               "\"protection\":\"\"},"
                          self.mpls_path_record_route_entries_received += \
                          self.mpls_path_record_route_entry_received
                        self.mpls_data_fd.seek( self.line_length )
                        break
                      self.line_length += len( self.mpls_data )
                      self.mpls_data_list = self.mpls_data.split()
                      try:
                        self.mpls_path_record_route_entry_received = \
                             "\"path record route \"{}\":".format( self.path_record_route ) + \
                             "{" + \
                             "\"inet\":\"{}\"," \
                             "\"ip\":\"{}\"," \
                             "\"flags\":\"{}\"," \
                             "\"protection\":\"{}\"".format( self.mpls_data_list[0],
                                                             self.mpls_data_list[1].split( "," )[0].
                                                                  replace( ":", "~" ),
                                                             self.mpls_data_list[3],
                                                             " ".join( self.mpls_data_list[5].split( ":" )[0].
                                                                       replace( " ", "" ).replace( ")", "" ).
                                                                       replace( ",", " " ).split() )
                                                            ) + \
                             "},"
                        self.mpls_path_record_route_entries_received += \
                        self.mpls_path_record_route_entry_received
                      except:
                        self.mpls_path_record_route_entry_received = ""
                    continue
                  if self.mpls_data[6:].startswith( "Tspec" ):
                    try:
                      self.mpls_path_avg_rate_received = \
                      self.mpls_data.split( "," )[0].split( "=" )[1]
                    except:
                      self.mpls_path_avg_rate_received = ""
                    try:
                      self.mpls_path_burst_received = \
                      self.mpls_data.split( "," )[1].split( "=" )[1]
                    except:
                      self.mpls_path_burst_received = ""
                    try:
                      self.mpls_path_peak_rate_received = \
                      self.mpls_data.split( "," )[2]. \
                                     split( "=" )[1].split( "\n" )[0]
                    except:
                      self.mpls_path_peak_rate_received = ""
                    continue
                  if self.mpls_data[6:].startswith( "Session Attributes" ):
                    try:
                      self.mpls_path_session_local_prot_state_received = \
                      self.mpls_data_list[4].split( "," )[0]
                    except:
                      self.mpls_path_session_local_prot_state_received = ""
                    try:
                      self.mpls_path_session_node_prot_state_received = \
                      self.mpls_data_list[7].split( "," )[0]
                    except:
                      self.mpls_path_session_node_prot_state_received = ""
                    try:
                      self.mpls_path_session_bw_prot_state_received = \
                      self.mpls_data.split( ":" ).split( "\n" )[0]
                    except:
                      self.mpls_path_session_bw_prot_state_received = ""
                    for self.mpls_data in self.mpls_data_fd:
                      if self.mpls_data[4:].startswith( "Resv Info" ):
                        self.mpls_data_fd.seek( self.line_length )
                        break
                      self.line_length += len( self.mpls_data )
                      try:
                        self.mpls_path_session_soft_preemption_state_received = \
                        self.mpls_data.split( ":" )[1].split( "\n" )[1:]
                      except:
                        self.mpls_path_session_soft_preemption_state_received = ""
                    continue
              #---------------------------------------------------------------------------------------------------
              #---------------------------------------------------------------------------------------------------
              if self.mpls_data[4:].startswith( "Resv Info" ):
                self.reserve_record_route = 0
                try:
                  self.mpls_reserve_info_received = \
                  self.mpls_data.split( ":" ).split( "\n" )[0]
                except:
                  self.mpls_reserver_info_received = ""
                for self.mpls_data in self.mpls_data_fd:
                  if self.mpls_data.startswith( "LSP Tunnel" ) or \
                     self.mpls_data.startswith( "Displayed " ):
                    self.mpls_data_fd.seek( self.line_length )
                    break
                  self.line_length += len( self.mpls_data )
                  if self.mpls_data[6:].startswith( "Record Route" ):
                    try:
                      self.mpls_reserve_record_route_state_received = \
                      self.mpls_data.split( ":" )[1].split( "\n" )[0].split()[0]
                    except:
                      self.mpls_reserve_record_route_state_received = ""
                    for self.mpls_data in self.mpls_data_fd:
                      self.reserve_record_route += 1
                      if self.mpls_data[6:].startswith( "Fspec" ):
                        if self.mpls_path_record_route_state_received.find( "Empty" ):
                          self.mpls_reserve_record_route_entry_received = \
                               "\"reserve record route \"{}\":".format( self.reserve_record_route ) + \
                               "{\"inet\":\"\"," \
                               "\"ip\":\"\"," \
                               "\"flags\":\"\"," \
                               "\"node\":\"\"},"
                          self.mpls_reserve_record_route_entries_received += \
                          self.mpls_reserve_record_route_entry_received
                          self.mpls_reserve_record_route_entry_received = \
                              "\"reserve label record route \"{}\":".format( self.reserve_record_route ) + \
                              "{\"label\":\"\"," \
                               "\"flags\":\"\"},"
                          self.mpls_reserve_record_route_entries_received += \
                          self.mpls_reserve_record_route_entry_received
                        self.mpls_data_fd.seek( self.line_length )
                        break
                      self.line_length += len( self.mpls_data )
                      self.mpls_data_list = self.mpls_data.split()
                      if self.mpls_data_list[0].startswith( "IPv4" ) or \
                         self.mpls_data_list[0].startswith( "IPv6" ):
                        try:
                          self.mpls_reserve_record_route_entry_received = \
                            "\"reserve record route \"{}\":".format( self.reserve_record_route ) + \
                            "{" + \
                            "\"inet\":\"{}\"," \
                            "\"ip\":\"{}\"," \
                            "\"flags\":\"{}\"," \
                            "\"node\":\"{}\"".\
                               format( self.mpls_data_list[0],
                                       self.mpls_data_list[1].split( "," )[0].replace( ":", "~" ),
                                       self.mpls_data_list[3],
                                       self.mpls_data_list[4].replace( "(", "" ).replace( ")", "" )
                                      ) + \
                            "},"
                          self.mpls_reserve_record_route_entries_received += \
                          self.mpls_reserve_record_route_entry_received
                        except:
                          try:
                            self.mpls_reserve_record_route_entry_received = \
                              "\"reserve record route \"{}\":".format( self.reserve_record_route ) + \
                              "{" + \
                              "\"inet\":\"{}\"," \
                              "\"ip\":\"{}\"," \
                              "\"flags\":\"{}\"". \
                                format( self.mpls_data_list[0],
                                        self.mpls_data_list[1].split( "," )[0].replace( ":", "~" ),
                                        self.mpls_data_list[3]
                                        ) + \
                              "},"
                            self.mpls_reserve_record_route_entries_received += \
                            self.mpls_reserve_record_route_entry_received
                          except:
                            try:
                              self.mpls_reserve_record_route_entry_received = \
                                "\"reserve record route \"{}\":".format( self.reserve_record_route ) + \
                                "{" + \
                                "\"inet\":\"{}\"," \
                                "\"ip\":\"{}\"". \
                                  format( self.mpls_data_list[0],
                                          self.mpls_data_list[1].split( "," )[0].replace( ":", "~" )
                                        ) + \
                                "},"
                              self.mpls_reserve_record_route_entries_received += \
                              self.mpls_reserve_record_route_entry_received
                            except:
                              self.mpls_reserve_record_route_entry_received = ""
                        continue
                      if self.mpls_data_list[0].startswith( "Label" ):
                        try:
                          self.mpls_reserve_record_route_entry_received = \
                            "\"reserve label record route \"{}\":".format( self.reserve_record_route ) + \
                            "{" + \
                            "\"label\":\"{}\"," \
                            "\"flags\":\"{}\"".format( self.mpls_data_list[0].split( "," )[0],
                                                      self.mpls_data_list[3]
                                                      ) + \
                            "},"
                          self.mpls_reserve_record_route_entries_received += \
                          self.mpls_reserve_record_route_entry_received
                        except:
                          self.mpls_reserve_record_route_entry_received = ""
                        continue
                    continue
                  if self.mpls_data[6:].startswith( "Fspec" ):
                    try:
                      self.mpls_reserve_fspec_avg_rate_received = \
                      self.mpls_data.split( "," )[0].split( "=" )[1]
                    except:
                      self.mpls_reserve_fspec_avg_rate_received = ""
                    try:
                      self.mpls_reserve_fspec_burst_received = \
                      self.mpls_data.split( "," )[1].split( "=" )[1]
                    except:
                      self.mpls_reserve_fspec_burst_received = ""
                    try:
                      self.mpls_reserve_fspec_peak_rate_received = \
                      self.mpls_data.split( "," )[2]. \
                           split( "=" )[1].split( "\n" )[0]
                    except:
                      self.mpls_reserve_fspec_peak_rate_received = ""
                  continue
                continue
      #-------------------------------------------------------------------------------------------------------------
      if self.tunnel_process_completed_flag:
        self.tunnel_process_completed_flag = False
        self.mpls_table.append( "{" + \
                                "\"show mpls traffic-eng tunnels {}\":" \
                                "\"show mpls traffic-eng tunnels {}\"," \
                                "\"device\":\"{}\"," \
                                "\"mpls tunnel id\":\"{}\"," \
                                "\"mpls tunnel number\":\"{}\"," \
                                "\"mpls tunnel unspec field\":\"{}\"," \
                                "\"mpls tunnel state\":\"{}\"," \
                                "\"mpls tunnel signalling status\":\"{}\"," \
                                "\"mpls tunnel name\":\"{}\"," \
                                "\"mpls tunnel role\":\"{}\"," \
                                "\"mpls inlabel address\":\"{}\"," \
                                "\"mpls inlabel type\":\"{}\"," \
                                "\"mpls signal source address\":\"{}\"," \
                                "\"mpls signal destination address\":\"{}\"," \
                                "\"mpls signal tunnel id\":\"{}\"," \
                                "\"mpls signal tunnel inst\":\"{}\"," \
                                "\"mpls signal external id\":\"{}\"," \
                                "\"mpls signal router id upstream id\":\"{}\"," \
                                "\"mpls signal router id local id\":\"{}\"," \
                                "\"mpls signal router id downstream id\":\"{}\"," \
                                "\"mpls signal bandwidth\":\"{}\"," \
                                "\"mpls signal class type\":\"{}\"," \
                                "\"mpls signal priority\":\"{}\"," \
                                "\"mpls signal dste class\":\"{}\"," \
                                "\"mpls signal soft preempt\":\"{}\"," \
                                "\"mpls signal srlgs\":\"{}\"," \
                                "\"mpls path incoming address\":\"{}\"," \
                                "\"mpls path expicit incoming route\":\"{}\"," \
                                "\"mpls path expicit outgoing route\":\"{}\"," \
                                "\"mpls path record route state\":\"{}\"," \
                                "{}," \
                                "\"mpls path avg rate\":\"{}\"," \
                                "\"mpls path burst\":\"{}\"," \
                                "\"mpls path peak rate\":\"{}\"," \
                                "\"mpls path session local prot state\":\"{}\"," \
                                "\"mpls path session node prot state\":\"{}\"," \
                                "\"mpls path session bw prot state\":\"{}\"," \
                                "\"mpls path session  soft preemption state\":\"{}\"," \
                                "\"mpls path session soft preemption state\":\"{}\"," \
                                "\"mpls reserve info\":\"{}\"," \
                                "\"mpls reserve record route state\":\"{}\"," \
                                "{}," \
                                "\"mpls reserve fspec avg rate\":\"{}\"," \
                                "\"mpls reserve fspec burst\":\"{}\"," \
                                "\"mpls reserve fspec peak rate\":\"{}\"". \
                                format( self.mpls_tunnel_number_received,
                                        self.mpls_tunnel_number_received,
                                        self.device,
                                        self.mpls_tunnel_id_received,
                                        self.mpls_tunnel_number_received,
                                        self.mpls_tunnel_unspec_field_received,
                                        self.mpls_tunnel_state_received,
                                        self.mpls_tunnel_signalling_status_received,
                                        self.mpls_tunnel_name_received,
                                        self.mpls_tunnel_role_received,
                                        self.mpls_inlabel_address_received,
                                        self.mpls_inlabel_type_received,
                                        self.mpls_signal_source_address_received,
                                        self.mpls_signal_destination_address_received,
                                        self.mpls_signal_tunnel_id_received,
                                        self.mpls_signal_tunnel_inst_received,
                                        self.mpls_signal_external_id_received,
                                        self.mpls_signal_router_id_upstream_id_received,
                                        self.mpls_signal_router_id_local_id_received,
                                        self.mpls_signal_router_id_downstream_id_received,
                                        self.mpls_signal_bandwidth_received,
                                        self.mpls_signal_class_type_received,
                                        self.mpls_signal_priority_received,
                                        self.mpls_signal_dste_class_received,
                                        self.mpls_signal_soft_preempt_received,
                                        self.mpls_signal_srlgs_received,
                                        self.mpls_path_incoming_address_received,
                                        self.mpls_path_explicit_incoming_route_received[:-1],
                                        self.mpls_path_explicit_outgoing_route_received[:-1],
                                        self.mpls_path_record_route_state_received,
                                        self.mpls_path_record_route_entries_received,
                                        self.mpls_path_avg_rate_received,
                                        self.mpls_path_burst_received,
                                        self.mpls_path_peak_rate_received,
                                        self.mpls_path_session_local_prot_state_received,
                                        self.mpls_path_session_node_prot_state_received,
                                        self.mpls_path_session_bw_prot_state_received,
                                        self.mpls_path_session_soft_preemption_state_received,
                                        self.mpls_path_session_soft_preemption_state_received,
                                        self.mpls_reserve_info_received,
                                        self.mpls_reserve_record_route_state_received,
                                        self.mpls_reserve_record_route_entries_received,
                                        self.mpls_reserve_fspec_avg_rate_received,
                                        self.mpls_reserve_fspec_burst_received,
                                        self.mpls_reserve_fspec_peak_rate_received
                                      ) + \
                                "};")
    #-------------------------------------------------------------------------------------------------------------
    for seed_dictionary in self.mpls_table:
      # FIXME DEBUG ONLY print(seed_dictionary)
      try:
        self.mpls_analysis_fd.write(seed_dictionary + "\n")
      except:
        print("Seed dictionary file write failed.")
    return()
  #----------------------------------------------------------------------------------------------------------------
  #----------------------------------------------------------------------------------------------------------------
  # FIXME DEBUG ONLY        print( "{" + \
  # FIXME DEBUG ONLY                               "\"show mpls traffic-eng tunnels {}\":" \
  # FIXME DEBUG ONLY                               "\"show mpls traffic-eng tunnels {}\",\n" \
  # FIXME DEBUG ONLY                               "\"device\":\"{}\",\n" \
  # FIXME DEBUG ONLY                               "\"mpls tunnel id\":\"{}\",\n" \
  # FIXME DEBUG ONLY                               "\"mpls tunnel number\":\"{}\",\n" \
  # FIXME DEBUG ONLY                               "\"mpls tunnel unspec field\":\"{}\",\n" \
  # FIXME DEBUG ONLY                               "\"mpls tunnel state\":\"{}\",\n" \
  # FIXME DEBUG ONLY                               "\"mpls tunnel signalling status\":\"{}\",\n" \
  # FIXME DEBUG ONLY                               "\"mpls tunnel name\":\"{}\",\n" \
  # FIXME DEBUG ONLY                               "\"mpls tunnel role\":\"{}\",\n" \
  # FIXME DEBUG ONLY                               "\"mpls inlabel address\":\"{}\",\n" \
  # FIXME DEBUG ONLY                               "\"mpls inlabel type\":\"{}\",\n" \
  # FIXME DEBUG ONLY                               "\"mpls signal source address\":\"{}\",\n" \
  # FIXME DEBUG ONLY                               "\"mpls signal destination address\":\"{}\",\n" \
  # FIXME DEBUG ONLY                               "\"mpls signal tunnel id\":\"{}\",\n" \
  # FIXME DEBUG ONLY                               "\"mpls signal tunnel inst\":\"{}\",\n" \
  # FIXME DEBUG ONLY                               "\"mpls signal external id\":\"{}\",\n" \
  # FIXME DEBUG ONLY                               "\"mpls signal router id upstream id\":\"{}\",\n" \
  # FIXME DEBUG ONLY                               "\"mpls signal router id local id\":\"{}\",\n" \
  # FIXME DEBUG ONLY                               "\"mpls signal router id downstream id\":\"{}\",\n" \
  # FIXME DEBUG ONLY                               "\"mpls signal bandwidth\":\"{}\",\n" \
  # FIXME DEBUG ONLY                               "\"mpls signal class type\":\"{}\",\n" \
  # FIXME DEBUG ONLY                               "\"mpls signal priority\":\"{}\",\n" \
  # FIXME DEBUG ONLY                               "\"mpls signal dste class\":\"{}\",\n" \
  # FIXME DEBUG ONLY                               "\"mpls signal soft preempt\":\"{}\",\n" \
  # FIXME DEBUG ONLY                               "\"mpls signal srlgs\":\"{}\",\n" \
  # FIXME DEBUG ONLY                               "\"mpls path incoming address\":\"{}\",\n" \
  # FIXME DEBUG ONLY                               "\"mpls path expicit incoming route\":\"{}\",\n" \
  # FIXME DEBUG ONLY                               "\"mpls path expicit outgoing route\":\"{}\",\n" \
  # FIXME DEBUG ONLY                               "\"mpls path record route state\":\"{}\",\n" \
  # FIXME DEBUG ONLY                               "\"mpls path record route entries\":\"{}\",\n" \
  # FIXME DEBUG ONLY                               "\"mpls path avg rate\":\"{}\",\n" \
  # FIXME DEBUG ONLY                               "\"mpls path burst\":\"{}\",\n" \
  # FIXME DEBUG ONLY                               "\"mpls path peak rate\":\"{}\",\n" \
  # FIXME DEBUG ONLY                               "\"mpls path session local prot state\":\"{}\",\n" \
  # FIXME DEBUG ONLY                               "\"mpls path session node prot state\":\"{}\",\n" \
  # FIXME DEBUG ONLY                               "\"mpls path session bw prot state\":\"{}\",\n" \
  # FIXME DEBUG ONLY                               "\"mpls path session  soft preemption state\":\"{}\",\n" \
  # FIXME DEBUG ONLY                               "\"mpls path session soft preemption state\":\"{}\",\n" \
  # FIXME DEBUG ONLY                               "\"mpls reserve info\":\"{}\",\n" \
  # FIXME DEBUG ONLY                               "\"mpls reserve record route state\":\"{}\",\n" \
  # FIXME DEBUG ONLY                               "\"mpls reserve record route entries\":\"{}\",\n" \
  # FIXME DEBUG ONLY                               "\"mpls reserve fspec avg rate\":\"{}\",\n" \
  # FIXME DEBUG ONLY                               "\"mpls reserve fspec burst\":\"{}\",\n" \
  # FIXME DEBUG ONLY                               "\"mpls reserve fspec peak rate\":\"{}\"\n". \
  # FIXME DEBUG ONLY                               format( self.mpls_tunnel_number_received,
  # FIXME DEBUG ONLY                                       self.mpls_tunnel_number_received,
  # FIXME DEBUG ONLY                                       self.device,
  # FIXME DEBUG ONLY                                       self.mpls_tunnel_id_received,
  # FIXME DEBUG ONLY                                       self.mpls_tunnel_number_received,
  # FIXME DEBUG ONLY                                       self.mpls_tunnel_unspec_field_received,
  # FIXME DEBUG ONLY                                       self.mpls_tunnel_state_received,
  # FIXME DEBUG ONLY                                       self.mpls_tunnel_signalling_status_received,
  # FIXME DEBUG ONLY                                       self.mpls_tunnel_name_received,
  # FIXME DEBUG ONLY                                       self.mpls_tunnel_role_received,
  # FIXME DEBUG ONLY                                       self.mpls_inlabel_address_received,
  # FIXME DEBUG ONLY                                       self.mpls_inlabel_type_received,
  # FIXME DEBUG ONLY                                       self.mpls_signal_source_address_received,
  # FIXME DEBUG ONLY                                       self.mpls_signal_destination_address_received,
  # FIXME DEBUG ONLY                                       self.mpls_signal_tunnel_id_received,
  # FIXME DEBUG ONLY                                       self.mpls_signal_tunnel_inst_received,
  # FIXME DEBUG ONLY                                       self.mpls_signal_external_id_received,
  # FIXME DEBUG ONLY                                       self.mpls_signal_router_id_upstream_id_received,
  # FIXME DEBUG ONLY                                       self.mpls_signal_router_id_local_id_received,
  # FIXME DEBUG ONLY                                       self.mpls_signal_router_id_downstream_id_received,
  # FIXME DEBUG ONLY                                       self.mpls_signal_bandwidth_received,
  # FIXME DEBUG ONLY                                       self.mpls_signal_class_type_received,
  # FIXME DEBUG ONLY                                       self.mpls_signal_priority_received,
  # FIXME DEBUG ONLY                                       self.mpls_signal_dste_class_received,
  # FIXME DEBUG ONLY                                       self.mpls_signal_soft_preempt_received,
  # FIXME DEBUG ONLY                                       self.mpls_signal_srlgs_received,
  # FIXME DEBUG ONLY                                       self.mpls_path_incoming_address_received,
  # FIXME DEBUG ONLY                                       self.mpls_path_explicit_incoming_route_received[:-1],
  # FIXME DEBUG ONLY                                       self.mpls_path_explicit_outgoing_route_received[:-1],
  # FIXME DEBUG ONLY                                       self.mpls_path_record_route_state_received,
  # FIXME DEBUG ONLY                                       self.mpls_path_record_route_entries_received,
  # FIXME DEBUG ONLY                                       self.mpls_path_avg_rate_received,
  # FIXME DEBUG ONLY                                       self.mpls_path_burst_received,
  # FIXME DEBUG ONLY                                       self.mpls_path_peak_rate_received,
  # FIXME DEBUG ONLY                                       self.mpls_path_session_local_prot_state_received,
  # FIXME DEBUG ONLY                                       self.mpls_path_session_node_prot_state_received,
  # FIXME DEBUG ONLY                                       self.mpls_path_session_bw_prot_state_received,
  # FIXME DEBUG ONLY                                       self.mpls_path_session_soft_preemption_state_received,
  # FIXME DEBUG ONLY                                       self.mpls_path_session_soft_preemption_state_received,
  # FIXME DEBUG ONLY                                       self.mpls_reserve_info_received,
  # FIXME DEBUG ONLY                                       self.mpls_reserve_record_route_state_received,
  # FIXME DEBUG ONLY                                       self.mpls_reserve_record_route_entries_received,
  # FIXME DEBUG ONLY                                       self.mpls_reserve_fspec_avg_rate_received,
  # FIXME DEBUG ONLY                                       self.mpls_reserve_fspec_burst_received,
  # FIXME DEBUG ONLY                                       self.mpls_reserve_fspec_peak_rate_received
  # FIXME DEBUG ONLY                                     ) + \
  # FIXME DEBUG ONLY                               "};")
  #----------------------------------------------------------------------------------------------------------------
  #----------------------------------------------------------------------------------------------------------------
  def build_juniper_analysis_seed_file( self ):
    mpls_table = []
    for self.mpls_data in self.mpls_data_fd:
      if self.mpls_data.startswith( "\n" ):
        break
      else:
        try:
          self.interface = self.mpls_data.split()[0]
        except:
          self.interface = ""
        try:
          self.system = self.mpls_data.split()[1]
        except:
          self.system = ""
        try:
          self.level = self.mpls_data.split()[2]
        except:
          self.level = ""
        try:
          self.state = self.mpls_data.split()[3]
        except:
          self.state = ""
        try:
          self.hold = self.mpls_data.split()[4]
        except:
          self.hold = ""
        try:
          self.snpa = self.mpls_data.split()[5]
        except:
          self.snpa = ""
        mpls_table.append( "{" + \
                                     "\"show rsvp neighbors\":\"show_mpls\",\"device\":\"juniper\"," \
                                     "\"interface\":\"{}\",\"system\":\"{}\"," \
                                     "\"level\":\"{}\",\"state\":\"{}\"," \
                                     "\"hold\":\"{}\",\"snpa\":\"{}\"".format( self.interface,
                                                                               self.system,
                                                                               self.level,
                                                                               self.state,
                                                                               self.hold,
                                                                               self.snpa ) + \
                                     "};")
    for seed_dictionary in mpls_table:
      # FIXME DEBUG print(seed_dictionary)
      try:
        self.mpls_analysis_fd.write(seed_dictionary + "\n")
      except:
        print("Seed dictionary file write failed.")
    return()
###################################################################################################################
