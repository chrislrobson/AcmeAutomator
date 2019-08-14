####################################################################################################################
# Python Qt5 Testbed Tester Analysis Custom Processor
# MODULE:   Analysis Custom Processor
# Author: Christopher Robson
# Copyright by:  Christopher Robson
# Copyright date: 01Jan2016
# This software is not FREE!  Use or destribution of the software system and its
# subsystem modules, libraries, configuration file and "seed" file without the
# express permission of the author is strictly PROHIBITED!
# FUNCTION:  Module analysis report data from network devices
####################################################################################################################
import os
import ast
import itertools
import collections
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
# Home grown
#------------------------------------------------------------------------------------------------------------------
from Globals import *
from Exceptions import *
from AnalysisWordDocumentTableProcessor import WordDocumentTableProcessor
from SeedDictionary import SeedCommandDictionaryProcessor
from AnalysisWordDocumentProcessor import WordDocumentProcessor
from ShowInterfacesStatusStringParser import ShowInterfaceStatusStringParser
from L2VpnXconnectReceiveDataParcer import L2VpnXconnectReceiveDataParcer
from ReportGenerator import ReportGenerator
from RichTextProcessor import RichTextProcessor
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
# Combine Report Document
#------------------------------------------------------------------------------------------------------------------
class CombineReportDocument:
  "Combine Report Document"
  #----------------------------------------------------------------------------------------------------------------
  def __init__( self, parent = None ):
    self.name = "Combine Report Document"
    self.parent = parent
    self.filename_time_extension = parent.filename_time_extension
    self.report_file_list = parent.report_file_list
    self.process_reply = self.parent.process_reply
    self.cmd_list = self.parent.cmd_list
    self.is_search_item = self.parent.is_search_item
    self.testcase_name = self.parent.testcase_name
    self.analysis_data_filename = self.parent.analysis_data_filename
    self.seed_list = []
    self.command_issued = ""
    self.line_number = 0
    self.line_number_head = 0
  #----------------------------------------------------------------------------------------------------------------
  def execute( self, seed_logical_dict, reportFD ):
    self.reportFD = reportFD
    self.seed_logical_dict = dict( seed_logical_dict )
    try:
      self.savepath = self.seed_logical_dict['savepath']
      self.report_filename = self.seed_logical_dict['filename'] + self.filename_time_extension
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    WordDocumentProcessor( self ).automatically_combine_word_documents( self.savepath,
                                                                                             self.report_filename )
    self.reportFD.seek( 0 )
    return (self.reportFD)
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
# Show BGP VRF Static Analysis
#------------------------------------------------------------------------------------------------------------------
class ShowBgpVrfStaticAnalysis:
  "Show BGP VRF"
  #----------------------------------------------------------------------------------------------------------------
  def __init__( self, parent = None ):
    self.name = "Show BGP VRF"
    self.parent = parent
    self.filename_time_extension = parent.filename_time_extension
    self.process_reply = self.parent.process_reply
    self.cmd_list = self.parent.cmd_list
    self.is_search_item = self.parent.is_search_item
    self.testcase_name = self.parent.testcase_name
    self.analysis_data_filename = self.parent.analysis_data_filename
    self.seed_list = []
    self.command_issued = ""
    self.line_number = 0
    self.line_number_head = 0
    self.fragment_type = ""
    self.check_list = ""
  #----------------------------------------------------------------------------------------------------------------
  #----------------------------------------------------------------------------------------------------------------
  def execute( self, seed_logical_dict, reportFD ):
    self.reportFD = reportFD
    self.seed_logical_dict = seed_logical_dict
    self.main_key, self.main_value = next( self.seed_logical_dict )
    #--------------------------------------------------------------------------------------------------------------
    self.offset = 0
    self.offset_vrf = 0
    for self.report_data in self.reportFD:
      self.line_number += 1
      self.offset += len( self.report_data )
      if self.report_data.startswith( "\n" ):
        continue
      elif self.report_data.startswith( "DUT(" ) and \
           self.report_data.split( ")-> " )[1].split( "\n" )[0].startswith( self.main_value ):
        self.command_issued = self.report_data.split( ")-> " )[1].split( "\n" )[0]
        self.break_flag = False
        self.offset_working = 0
        self.index_vrf = 0
        for self.vrf_key, self.vrf_value in self.seed_logical_dict:
          self.index_vrf += 1
          self.vrf_key.replace( "%", ":" )
          self.vrf_value.replace( "%", ":" )
          if self.break_flag:
            break
          for self.vrf_data in self.reportFD:
            self.line_number += 1
            self.offset_working += len( self.vrf_data )
            if self.vrf_data.startswith( "DUT(" ):
              self.break_flag = True
              self.reportFD.seek( 0,2 )
              break
            if self.vrf_data.startswith( self.vrf_key ) and \
               self.vrf_data.split()[1].startswith( self.vrf_value ):
              if self.index_vrf == 1:
                self.offset_vrf = self.offset_working + self.offset
              #self.set_pass_fail( "Passed" )
              print( "PASSED: {} {}".format( self.vrf_key, self.vrf_value ) )
              self.reportFD.seek( self.offset_vrf )
              break
          else:
            #self.set_pass_fail( "Failed" )
            print( "FAILED: {} {}".format( self.vrf_key, self.vrf_value ) )
            self.reportFD.seek( self.offset_vrf )
        else:
          self.reportFD.seek( 0,2 )
    return()
  #------------------------------------------------------------------------------------------------------------------
  #----------------------------------------------------------------------------------------------------------------
  def set_pass_fail( self, pass_fail ):
    self.is_search_item.set_test_results_string( "KEY: {}, VALUE: {}".
                                                 format( self.fragment_type,
                                                         self.check_list ),
                                                 self.testcase_name,
                                                 pass_fail,
                                                 "{}".format( self.command_issued ),
                                                 "{}".format( self.analysis_data_filename ),
                                                 str( self.line_number_head ),
                                                 str( self.line_number ) )
    return ()
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
# Show BGP Summary Static Analysis
#------------------------------------------------------------------------------------------------------------------
class ShowBgpSummaryStaticAnalysis:
  "Show BGP Summary"
  #----------------------------------------------------------------------------------------------------------------
  def __init__( self, parent = None ):
    self.name = "Show BGP Summary Static Analysis"
    self.parent = parent
    self.filename_time_extension = parent.filename_time_extension
    self.process_reply = self.parent.process_reply
    self.cmd_list = self.parent.cmd_list
    self.is_search_item = self.parent.is_search_item
    self.testcase_name = self.parent.testcase_name
    self.analysis_data_filename = self.parent.analysis_data_filename
    self.seed_list = []
    self.command_issued = ""
    self.line_number = 0
    self.line_number_head = 0
    self.fragment_type = ""
    self.check_list = ""
  #----------------------------------------------------------------------------------------------------------------
  def execute( self, seed_logical_dict, reportFD ):
    self.reportFD = reportFD
    self.seed_logical_dict = dict( seed_logical_dict )
    #self.seed_logical_dict_pre = collections.OrderedDict( seed_logical_dict )
    self.seed_logical_dict_tee = itertools.tee( self.seed_logical_dict, 2 )
    self.offset = 0
    for self.report_data in self.reportFD:
      self.line_number += 1
      self.offset += len( self.report_data )
      if self.report_data.startswith( "\n" ):
        continue
      elif self.report_data.startswith( "DUT(" ):
        self.command_issued = self.report_data.split( ")->" )[1].split( "\n" )[0]
        if self.seed_logical_dict["device"] == "cisco":
          self.reportFD = self.cisco_isis( self.seed_logical_dict, self.reportFD )
          break
        elif self.seed_logical_dict["device"] == "juniper":
          self.reportFD = self.juniper_isis( self.seed_logical_dict, self.reportFD )
          break
        else:
          break
    else:
      raise CriticalFailure( "SHOWBGPSUMMARY ERROR: \"data not found!" )
    return ()
  #----------------------------------------------------------------------------------------------------------------
  def cisco_isis( self, seed_logical_dict, reportFD ):
    self.seed_logical_dict = collections.OrderedDict( seed_logical_dict )
    self.seed_logical_dict_tee = itertools.tee( self.seed_logical_dict, 2 )
    self.reportFD = reportFD
    #--------------------------------------------------------------------------------------------------------------
    try:
      self.router_identifier_to_check = self.seed_logical_dict["rid"]
      self.local_autonomous_system_number_to_check = self.seed_logical_dict["localAS"]
      self.table_state_to_check = self.seed_logical_dict["tablestate"]
      self.neighbor_to_check = self.seed_logical_dict["neighbor"]
      self.autonomous_system_number_to_check = self.seed_logical_dict["AS"]
      self.messages_received_to_check = self.seed_logical_dict["messagesreceived"]
      self.messages_sent_to_check = self.seed_logical_dict["messagessent"]
      self.up_down_time_to_check = self.seed_logical_dict["updown"].replace( "~", ":" )
      self.state_to_check = self.seed_logical_dict["state"]
    except:
      raise CriticalFailure( "SHOWBGPSUMMARY ERROR: Bad seed file data." )
    #--------------------------------------------------------------------------------------------------------------
    # BGP router identifier 33.20.0.98, local AS number 27064
    # BGP generic scan interval 60 secs
    # Non-stop routing is enabled
    # BGP table state: Active
    # Table ID: 0xe0000000   RD version: 1391
    # BGP main routing table version 1391
    # BGP NSR Initial initsync version 1391 (Reached)
    # BGP NSR/ISSU Sync-Group versions 0/0
    # Dampening enabled
    # BGP scan interval 60 secs
    # BGP is operating in STANDALONE mode.
    # Process       RcvTblVer   bRIB/RIB   LabelVer  ImportVer  SendTblVer  StandbyVer
    # Speaker            1391       1391       1391       1391        1391           0
    # Neighbor        Spk    AS MsgRcvd MsgSent   TblVer  InQ OutQ  Up/Down  St/PfxRcd
    # 33.20.0.16        0 27064    1473    1579     1391    0    0    1d00h          2
    # 33.20.0.102       0 27064    1620    1580     1391    0    0    1d00h          7
    # 150.20.90.1       0 27064    3592    2951     1391    0    0    1d00h         29
    #--------------------------------------------------------------------------------------------------------------
    self.show_bgp_summary_passed_flag = False
    self.pass_fail_str = "Failed"
    for self.report_data in self.reportFD:
      self.line_number += 1
      self.line_number_head = self.line_number
      if self.report_data.startswith( "\n" ):
        continue
      # ------------------------------------------------------------------------------------------------------------
      if self.report_data.startswith( "BGP router identifier" ) and \
         self.report_data.split()[3].split( "," )[0].startswith( self.router_identifier_to_check ) and \
         self.report_data.split()[7].startswith( self.local_autonomous_system_number_to_check ):
        self.router_identifier_received = self.report_data.split()[3].split( "," )[0]
        self.local_autonomous_system_number_received = self.report_data.split()[7]
      if self.report_data.startswith( "BGP table state:" ):
        self.table_state_received = self.report_data.split()[3]
        for self.report_data in self.reportFD:
          self.line_number += 1
          if self.report_data.startswith( "\n" ):
            continue
          if self.report_data.startswith( "Neighbor" ):
            for self.report_data in self.reportFD:
              self.line_number += 1
              if self.report_data.startswith( "\n" ):
                continue
              else:
                self.neighbor_received = self.report_data.split()[0]
                if self.neighbor_received == self.neighbor_to_check:
                  self.autonomous_system_number_received = self.report_data.split()[2]
                  self.messages_received_received = self.report_data.split()[3]
                  self.messages_sent_received = self.report_data.split()[4]
                  self.up_down_time_received = self.report_data.split()[8]
                  self.state_received = self.report_data.split()[9]
                  #---------------------------------------------------------------------------------------------------
                  if self.neighbor_received == self.neighbor_to_check:
                    self.show_bgp_summary_passed_flag = True
                  else:
                    self.show_bgp_summary_passed_flag = False
                    self.reportFD.seek( 0,2 )
                    break
                  if self.autonomous_system_number_received == self.autonomous_system_number_to_check:
                    self.show_bgp_summary_passed_flag = True
                  else:
                    self.show_bgp_summary_passed_flag = False
                    self.reportFD.seek( 0,2 )
                    break
                  if int( self.messages_received_received ) >= int( self.messages_received_to_check ):
                    self.show_bgp_summary_passed_flag = True
                  else:
                    self.show_bgp_summary_passed_flag = False
                    self.reportFD.seek( 0,2 )
                    break
                  if int( self.messages_sent_received ) >= int( self.messages_sent_to_check ):
                    self.show_bgp_summary_passed_flag = True
                  else:
                    self.show_bgp_summary_passed_flag = False
                    self.reportFD.seek( 0,2 )
                    break
                  if self.up_down_time_received != "00:00:00":
                    self.show_bgp_summary_passed_flag = True
                  elif self.state_to_check == "Idle":
                    self.show_bgp_summary_passed_flag = True
                  else:
                    self.show_bgp_summary_passed_flag = False
                    self.reportFD.seek( 0,2 )
                    break
                  if self.state_received.isdigit():
                    self.show_bgp_summary_passed_flag = True
                  elif self.state_received == self.state_to_check:
                    self.show_bgp_summary_passed_flag = True
                  else:
                    self.show_bgp_summary_passed_flag = False
                    self.reportFD.seek( 0,2 )
                    break
                  self.reportFD.seek( 0,2 )
                else:
                  continue
            else:
              self.reportFD.seek( 0,2 )
    if self.show_bgp_summary_passed_flag:
      self.pass_fail_str = "Passed"
      self.message_test = "Bgp summary validated"
    else:
      self.pass_fail_str = "Failed"
      self.message_test = "RID:{} Detected:{} " \
                          "Local AS:{} Detected:{} " \
                          "Table state:{} Detected:{} " \
                          "Neighbor:{} Detected:{} " \
                          "AS:{} Detected:{} " \
                          "Msg receive:{} Detected: {} " \
                          "Msg sent:{} Detected: {} " \
                          "Up/Down:{} Detected:{} " \
                          "State:{} Detected:{} ".format( self.router_identifier_to_check,
                                                          self.router_identifier_received,
                                                          self.local_autonomous_system_number_to_check,
                                                          self.local_autonomous_system_number_received,
                                                          self.table_state_to_check,
                                                          self.table_state_received,
                                                          self.neighbor_to_check,
                                                          self.neighbor_received,
                                                          self.autonomous_system_number_to_check,
                                                          self.autonomous_system_number_received,
                                                          self.messages_received_to_check,
                                                          self.messages_received_received,
                                                          self.messages_sent_to_check,
                                                          self.messages_sent_received,
                                                          self.up_down_time_to_check,
                                                          self.up_down_time_received,
                                                          self.state_to_check,
                                                          self.state_received )
    self.is_search_item.set_test_results_string( self.message_test,
                                                 self.testcase_name,
                                                 self.pass_fail_str,
                                                 "{}".format( self.command_issued ),
                                                 "{}".format( self.analysis_data_filename ),
                                                 str( self.line_number_head ),
                                                 str( self.line_number ) )
    self.reportFD.seek( 0 )
    return (self.reportFD)
  #----------------------------------------------------------------------------------------------------------------
  def juniper_isis( self, seed_logical_dict, reportFD ):
    self.reportFD = reportFD
    self.seed_logical_dict = seed_logical_dict
    return( self.reportFD )
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
# Show ISIS Database Summary
#------------------------------------------------------------------------------------------------------------------
class ShowIsisDatabaseSummary:
  "Show Isis Database Summary"
  #----------------------------------------------------------------------------------------------------------------
  def __init__( self, parent = None ):
    self.name = "Show Isis Database Summary"
    self.parent = parent
    self.filename_time_extension = parent.filename_time_extension
    self.process_reply = self.parent.process_reply
    self.cmd_list = self.parent.cmd_list
    self.is_search_item = self.parent.is_search_item
    self.testcase_name = self.parent.testcase_name
    self.analysis_data_filename = self.parent.analysis_data_filename
    self.seed_list = []
    self.command_issued = ""
    self.line_number = 0
    self.line_number_head = 0
    self.fragment_type = ""
    self.check_list = ""
    #----------------------------------------------------------------------------------------------------------------
  def execute( self, seed_logical_dict, reportFD ):
    self.reportFD = reportFD
    self.seed_logical_dict = seed_logical_dict
    self.offset = 0
    #--------------------------------------------------------------------------------------------------------------
    for self.report_data in self.reportFD:
      self.line_number += 1
      self.offset += len( self.report_data )
      if self.report_data.startswith( "\n" ):
        continue
      elif self.report_data.startswith( "DUT(" ):
        self.command_issued = self.report_data.split( ")->" )[1].split( "\n" )[0]
      elif self.report_data.split()[0].startswith( "IS-IS" ):
        if self.report_data.split()[2].isdigit:
          self.reportFD = self.cisco_isis( self.seed_logical_dict, self.reportFD )
          break
        else:
          self.reportFD = self.juniper_isis(  self.seed_logical_dict, self.reportFD )
          break
      elif self.report_data.startswith( "No IS-IS instances found" ):
        self.reportFD.seek( self.offset - len( self.report_data ) )
        self.reportFD = self.cisco_isis( self.seed_logical_dict, self.reportFD )
        break
    else:
      raise CriticalFailure( "SHOWISISDATABASECOMMAND ERROR: \"data not found!" )
    return()
  #----------------------------------------------------------------------------------------------------------------
  def cisco_isis( self, seed_logical_dict, reportFD ):
    self.reportFD = reportFD
    self.seed_logical_dict = seed_logical_dict
    self.dict = dict( self.seed_logical_dict )
    try:
      self.check_list = self.dict["data"]
    except:
      self.fragment_type = "NO data values provided"
      self.check_list = " "
      self.set_pass_fail( "Failed" )
    try:
      self.fragment_type = self.dict["row"]
    except:
      self.fragment_type = "NO key provided"
      self.check_list = " "
      self.set_pass_fail( "Failed" )
    #--------------------------------------------------------------------------------------------------------------
    self.flag = False
    for self.isis_data in self.reportFD:
      self.line_number += 1
      if self.flag:
        break
      if self.isis_data.startswith( "\n" ):
        continue
      self.data = " ".join( self.isis_data.split() )
      if self.data.startswith( "No IS-IS instances found" ):
        if self.isis_data.startswith( "No IS-IS instances found" ):
          self.set_pass_fail( "Passed" )
        else:
          self.set_pass_fail( "Failed" )
        return()
      #--------------------------------------------------------------------------------------------------------------
      if self.isis_data.startswith( self.fragment_type.split()[0] ) or \
         self.isis_data.startswith( " ".join( self.fragment_type.split()[:2] ) ):
        self.line_number_head = self.line_number
        for self.isis_data in self.reportFD:
          self.line_number += 1
          if self.isis_data.startswith( "\n" ):
            continue
          self.data_pre = " ".join( self.isis_data.split() )
          if not self.data_pre.startswith( " ".join( self.fragment_type.split()[1:] ) ) and not \
                 self.data_pre.startswith( " ".join( self.fragment_type.split()[2:] ) ):
            continue
          self.data = "".join( self.isis_data.split( ":" )[1].split() )
          for index, self.check in enumerate( self.check_list.split() ):
            if int( self.check ) > 0 and int( self.data[index] ) >= int( self.check ):
              self.set_pass_fail( "Passed" )
              self.flag = True
            elif int( self.check ) == int( self.data[index] ):
              self.set_pass_fail( "Passed" )
              self.flag = True
            else:
              self.set_pass_fail( "Failed" )
              self.flag = True
          else:
            if not self.flag:
              self.set_pass_fail( "Failed" )
          break
        else:
          self.set_pass_fail( "Failed" )
    else:
      self.set_pass_fail( "Failed" )
    self.reportFD.seek( 0 )
    return( self.reportFD )
  #----------------------------------------------------------------------------------------------------------------
  def juniper_isis( self, seed_logical_dict, reportFD ):
    self.reportFD = reportFD
    self.seed_logical_dict = seed_logical_dict
    return( self.reportFD )
  #------------------------------------------------------------------------------------------------------------------
  #----------------------------------------------------------------------------------------------------------------
  def set_pass_fail( self, pass_fail ):
    self.is_search_item.set_test_results_string( "KEY: {}, VALUE: {}".
                                                 format( self.fragment_type,
                                                         self.check_list ),
                                                 self.testcase_name,
                                                 pass_fail,
                                                 "{}".format( self.command_issued ),
                                                 "{}".format( self.analysis_data_filename ),
                                                 str( self.line_number_head ),
                                                 str( self.line_number ) )
    return()
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
# Show ISIS Adjacency
#------------------------------------------------------------------------------------------------------------------
class ShowIsisAdjacency:
  "Show Isis Adjacency"
  #----------------------------------------------------------------------------------------------------------------
  def __init__( self, parent = None ):
    self.name = "Show Isis Adjacency"
    self.parent = parent
    self.filename_time_extension = parent.filename_time_extension
    self.process_reply = self.parent.process_reply
    self.cmd_list = self.parent.cmd_list
    self.is_search_item = self.parent.is_search_item
    self.testcase_name = self.parent.testcase_name
    self.analysis_data_filename = self.parent.analysis_data_filename
    self.seed_list = []
    self.command_issued = ""
    self.line_number = 0
    self.line_number_head = 0
  #----------------------------------------------------------------------------------------------------------------
  def execute( self, seed_logical_dict, reportFD ):
    self.reportFD = reportFD
    self.seed_logical_dict = dict( seed_logical_dict )
    #--------------------------------------------------------------------------------------------------------------
    if self.seed_logical_dict["device"] == "juniper":
      self.reportFD = self.juniper_isis_adjacency_analysis( self.seed_logical_dict, self.reportFD )
    elif self.seed_logical_dict["device"] == "cisco":
      self.reportFD = self.cisco_isis_adjacency_analysis( self.seed_logical_dict, self.reportFD )
    else:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    return ()
  #----------------------------------------------------------------------------------------------------------------
  def cisco_isis_adjacency_analysis( self, seed_logical_dict, reportFD ):
    self.reportFD = reportFD
    self.seed_logical_dict = seed_logical_dict
    # -------------------------------------------------------------------------------------------------------------
    # FIXME UGLY!!! FIND A BETTER WAY THAN FLAGS !!!!!
    self.found_title_flag = False
    self.found_router_id_flag = False
    try:
      self.command_issued_str = self.seed_logical_dict["show isis adjacency"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.interface_to_check = self.seed_logical_dict["interface"]
      self.interface_to_check = self.interface_to_check.replace( "~", ":" )
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.system_to_check = self.seed_logical_dict["system"]
    except:
      self.system_to_check = ""
    try:
      self.router_id_to_check = self.seed_logical_dict["router id"]
    except:
      self.router_id_to_check = ""
    try:
      self.snpa_to_check = self.seed_logical_dict["snpa"]
    except:
      self.snpa_to_check = ""
    try:
      self.state_to_check = self.seed_logical_dict["state"]
    except:
      self.state_to_check = ""
    try:
      self.hold_to_check = self.seed_logical_dict["hold"]
    except:
      self.hold_to_check = ""
    try:
      self.nsf_to_check = self.seed_logical_dict["nsf"]
    except:
      self.nsf_to_check = ""
    try:
      self.ipv4_bfd_to_check = self.seed_logical_dict["ipv4 bfd"]
    except:
      self.ipv4_bfd_to_check = ""
    try:
      self.ipv6_bfd_to_check = self.seed_logical_dict["ipv6 bfd"]
    except:
      self.ipv6_bfd_to_check = ""
    #--------------------------------------------------------------------------------------------------------------
    self.router_id_received = ""
    for self.report_data in self.reportFD:
      self.line_number += 1
      if self.report_data.startswith( "\n" ) or self.report_data.startswith( " " ):
        continue
      #------------------------------------------------------------------------------------------------------------
      # FIXME FIND A BTTER WAY THAN USING AN UGLY FLAG!!!!!!
      elif self.found_title_flag:
        self.isis_data_list = self.report_data.split()
        try:
          self.system_received = self.isis_data_list[0]
        except:
          self.system_received = ""
        try:
          self.interface_received = self.isis_data_list[1]
        except:
          self.interface_received = ""
        try:
          self.snpa_received = self.isis_data_list[2]
        except:
          self.snpa_received = ""
        try:
          self.state_received = self.isis_data_list[3]
        except:
          self.state_received = ""
        try:
          self.hold_received = self.isis_data_list[4]
        except:
          self.hold_received = ""
        try:
          self.nsf_received = self.isis_data_list[6]
        except:
          self.nsf_received = ""
        try:
          self.ipv4_bfd_received = self.isis_data_list[7]
        except:
          self.ipv4_bfd_received = ""
        try:
          self.ipv6_bfd_received = self.isis_data_list[8]
        except:
          self.ipv6_bfd_received = ""
        #--------------------------------------------------------------------------------------------------------
        if self.router_id_received.startswith( self.router_id_to_check ) and \
           self.interface_received.startswith( self.interface_to_check ) :
          self.found_router_id_flag = True
          if self.interface_received.startswith( self.interface_to_check ) and \
              self.system_received.startswith( self.system_to_check ) and \
              self.state_received.startswith( self.state_to_check ) and \
              self.snpa_received.startswith( self.snpa_to_check ) and \
              self.nsf_received.startswith( self.nsf_to_check ) and \
              self.ipv4_bfd_received.startswith( self.ipv4_bfd_to_check ) and \
              self.ipv6_bfd_received.startswith( self.ipv6_bfd_to_check ):
            # FIXME REMOVE L8R self.is_search_item.set_test_results_string( "Router ID: {} Detected:{} "
            # FIXME REMOVE L8R                                              "Interface: {} Detected:{} "
            # FIXME REMOVE L8R                                              "System:{} Detected:{} "
            # FIXME REMOVE L8R                                              "State: {} Detected: {} "
            # FIXME REMOVE L8R                                              "SNPA: {} Detected: {} "
            # FIXME REMOVE L8R                                              "NSF: {} Detected: {} "
            # FIXME REMOVE L8R                                              "IPv4 BFD: {} Detected: {} "
            # FIXME REMOVE L8R                                              "IPv6 BFD:{} Detected:{}".
            # FIXME REMOVE L8R                                              format( self.router_id_to_check,
            # FIXME REMOVE L8R                                                      self.router_id_received,
            # FIXME REMOVE L8R                                                      self.interface_to_check,
            # FIXME REMOVE L8R                                                      self.interface_received,
            # FIXME REMOVE L8R                                                      self.system_to_check,
            # FIXME REMOVE L8R                                                      self.system_received,
            # FIXME REMOVE L8R                                                      self.state_to_check,
            # FIXME REMOVE L8R                                                      self.state_received,
            # FIXME REMOVE L8R                                                      self.snpa_to_check,
            # FIXME REMOVE L8R                                                      self.snpa_received,
            # FIXME REMOVE L8R                                                      self.nsf_to_check,
            # FIXME REMOVE L8R                                                      self.nsf_received,
            # FIXME REMOVE L8R                                                      self.ipv4_bfd_to_check,
            # FIXME REMOVE L8R                                                      self.ipv4_bfd_received,
            # FIXME REMOVE L8R                                                      self.ipv6_bfd_to_check,
            # FIXME REMOVE L8R                                                      self.ipv6_bfd_received ),
            self.is_search_item.set_test_results_string( "ISIS {}/{} validated".
                                                         format( self.router_id_to_check,
                                                                 self.interface_to_check ),
                                                         self.testcase_name,
                                                         "Passed",
                                                         "{}".format( self.command_issued_str ),
                                                         "{}".format( self.analysis_data_filename ),
                                                         str( self.line_number_head ),
                                                         str( self.line_number ) )
            break
          else:
            self.is_search_item.set_test_results_string( "Router ID: {} Detected:{} "
                                                         "Interface: {} Detected:{} "
                                                         "System:{} Detected:{} "
                                                         "State: {} Detected: {} "
                                                         "SNPA: {} Detected: {} "
                                                         "NSF: {} Detected: {} "
                                                         "IPv4 BFD: {} Detected: {} "
                                                         "IPv6 BFD:{} Detected:{}".
                                                         format( self.router_id_to_check,
                                                                 self.router_id_received,
                                                                 self.interface_to_check,
                                                                 self.interface_received,
                                                                 self.system_to_check,
                                                                 self.system_received,
                                                                 self.state_to_check,
                                                                 self.state_received,
                                                                 self.snpa_to_check,
                                                                 self.snpa_received,
                                                                 self.nsf_to_check,
                                                                 self.nsf_received,
                                                                 self.ipv4_bfd_to_check,
                                                                 self.ipv4_bfd_received,
                                                                 self.ipv6_bfd_to_check,
                                                                 self.ipv6_bfd_received ),
                                                         self.testcase_name,
                                                         "Failed",
                                                         "{}".format( self.command_issued_str ),
                                                         "{}".format( self.analysis_data_filename ),
                                                         str( self.line_number_head ),
                                                         str( self.line_number ) )
            break
        else:
          continue
      elif self.report_data.startswith( "IS-IS" ):
        self.router_id_received = self.report_data.split()[1]
        continue
      elif self.report_data.startswith( "System Id      Interface        SNPA           State Hold Changed  NSF IPv4 IPv6" ):
        self.found_title_flag = True
        self.line_number_head = self.line_number
    if not self.found_router_id_flag:
      self.is_search_item.set_test_results_string( "Router ID: {} Interface: {} System: {}".
                                                   format( self.router_id_to_check,
                                                           self.interface_to_check,
                                                           self.system_to_check),
                                                   self.testcase_name,
                                                   "Failed",
                                                   "{} {}".format( self.router_id_to_check,
                                                                   " NOT found on device" ),
                                                   "{}".format( self.analysis_data_filename ),
                                                   str( self.line_number_head ),
                                                   str( self.line_number ) )
    elif not self.found_title_flag:
      raise NotAnError( "No interface data found" )
    self.reportFD.seek( 0 )
    return (self.reportFD)
    #----------------------------------------------------------------------------------------------------------------
  def juniper_isis_adjacency_analysis( self, seed_logical_dict, reportFD ):
    self.reportFD = reportFD
    self.seed_logical_dict = seed_logical_dict
    #--------------------------------------------------------------------------------------------------------------
    return (self.reportFD)
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
# Show RSVP Neighbors Detail
#------------------------------------------------------------------------------------------------------------------
class ShowRsvpNeighborsDetail:
  "Show Rsvp Neighbors Detail"
  # ----------------------------------------------------------------------------------------------------------------
  def __init__( self, parent = None ):
    self.name = "Show Rsvp Neighbors Detail"
    self.parent = parent
    self.filename_time_extension = parent.filename_time_extension
    self.process_reply = self.parent.process_reply
    self.cmd_list = self.parent.cmd_list
    self.is_search_item = self.parent.is_search_item
    self.testcase_name = self.parent.testcase_name
    self.analysis_data_filename = self.parent.analysis_data_filename
    self.seed_list = []
    self.command_issued = ""
    self.line_number = 0
    self.line_number_head = 0
  #----------------------------------------------------------------------------------------------------------------
  def execute( self, seed_logical_dict, reportFD ):
    self.reportFD = reportFD
    self.seed_logical_dict = dict( seed_logical_dict )
    #--------------------------------------------------------------------------------------------------------------
    if self.seed_logical_dict["device"] == "juniper":
      self.reportFD = self.juniper_rsvp_neighbors_analysis( self.seed_logical_dict, self.reportFD )
    elif self.seed_logical_dict["device"] == "cisco":
      self.reportFD = self.cisco_rsvp_neighbors_analysis( self.seed_logical_dict, self.reportFD )
    else:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    return ()
  #----------------------------------------------------------------------------------------------------------------
  def cisco_rsvp_neighbors_analysis( self, seed_logical_dict, reportFD ):
    self.reportFD = reportFD
    self.seed_logical_dict = seed_logical_dict
    # -------------------------------------------------------------------------------------------------------------
    # FIXME UGLY!!! FIND A BETTER WAY THAN FLAGS !!!!!
    self.found_rsvp_flag = False
    try:
      self.command_issued_str = self.seed_logical_dict["show rsvp neighbors detail"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.rsvp_global_neighbor_to_check = self.seed_logical_dict["rsvp global neighbor"]
      self.rsvp_global_neighbor_to_check = self.rsvp_global_neighbor_to_check.replace( "~", ":" )
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.rsvp_interface_neighbor_to_check = self.seed_logical_dict["rsvp interface neighbor"]
      self.rsvp_interface_neighbor_to_check = self.rsvp_interface_neighbor_to_check.replace( "~", ":" )
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.rsvp_interface_to_check = self.seed_logical_dict["rsvp interface"]
      self.rsvp_interface_to_check = self.rsvp_interface_to_check.replace( "~", ":" )
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.rsvp_refresh_reduction_to_check = self.seed_logical_dict["rsvp refresh reduction"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.rsvp_remote_epoch_to_check = self.seed_logical_dict["rsvp remote epoch"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.rsvp_out_of_order_count_to_check = self.seed_logical_dict["rsvp out of order count"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.rsvp_retransmitted_count_to_check = self.seed_logical_dict["rsvp retransmitted count"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    # --------------------------------------------------------------------------------------------------------------
    self.line_length = 0
    for self.rsvp_data in self.reportFD:
      self.line_number += 1
      self.line_length += len( self.rsvp_data )
      if self.rsvp_data.startswith( "\n" ):
        continue
      else:
        self.rsvp_data_list = self.rsvp_data.split()
        if self.rsvp_data.startswith( "Global Neighbor" ) and \
                self.rsvp_data.find( self.rsvp_global_neighbor_to_check ) != -1:
          try:
            self.rsvp_global_neighbor_received = self.rsvp_data_list[2]
          except:
            self.rsvp_global_neighbor_received = ""
          for self.rsvp_data in self.reportFD:
            self.line_length += len( self.rsvp_data )
            if self.rsvp_data.startswith( "\n" ):
              continue
            else:
              self.rsvp_data_list = self.rsvp_data.split()
              if self.rsvp_data.startswith( "  Interface Neighbor" ):
                try:
                  self.rsvp_interface_neighbor_received = self.rsvp_data_list[2]
                except:
                  self.rsvp_interface_neighbor_received = ""
                for self.rsvp_data in self.reportFD:
                  self.line_length += len( self.rsvp_data )
                  if self.rsvp_data.startswith( "\n" ):
                    continue
                  else:
                    self.rsvp_data_list = self.rsvp_data.split()
                    if self.rsvp_data.startswith( "    Interface" ):
                      try:
                        self.rsvp_interface_received = self.rsvp_data_list[1]
                      except:
                        self.rsvp_interface_received = ""
                    elif self.rsvp_data.startswith( "    Refresh Reduction" ):
                      try:
                        self.rsvp_refresh_reduction_received = self.rsvp_data_list[2]
                      except:
                        self.rsvp_refresh_reduction_received = ""
                    elif self.rsvp_data.startswith( "    Remote epoch" ):
                      try:
                        self.rsvp_remote_epoch_received = self.rsvp_data_list[2]
                      except:
                        self.rsvp_remote_epoch_received = ""
                    elif self.rsvp_data.startswith( "    Counters" ):
                      for self.rsvp_data in self.reportFD:
                        self.line_length += len( self.rsvp_data )
                        if self.rsvp_data.startswith( "\n" ):
                          continue
                        else:
                          self.move_back_length = 0
                          if self.rsvp_data.startswith( "Global Neighbor" ):
                            self.reportFD.seek( self.line_length - self.move_back_length, 0 )
                            break
                          self.line_length += len( self.rsvp_data )
                          self.rsvp_data_list = self.rsvp_data.split()
                          if self.rsvp_data.startswith( "      Out of order messages" ):
                            try:
                              self.rsvp_out_of_order_count_received = self.rsvp_data_list[4]
                            except:
                              self.rsvp_out_of_order_count_received = ""
                          elif self.rsvp_data.startswith( "      Retransmitted messages" ):
                            self.move_back_length = len( self.rsvp_data )
                            try:
                              self.rsvp_retransmitted_count_received = self.rsvp_data_list[2]
                            except:
                              self.rsvp_retransmitted_count_received = ""
                            break   # All done with this Global Neighbor
                      #--------------------------------------------------------------------------------------------------------
                      self.found_rsvp_flag = True
                      if self.rsvp_interface_neighbor_received.startswith( self.rsvp_interface_neighbor_to_check ) and \
                          self.rsvp_interface_received.startswith( self.rsvp_interface_to_check ) and \
                          self.rsvp_refresh_reduction_received.startswith( self.rsvp_refresh_reduction_to_check ) and \
                          int( self.rsvp_remote_epoch_received, 0 ) >= \
                              int( self.rsvp_remote_epoch_to_check, 0 ) and \
                          int( self.rsvp_out_of_order_count_received ) <= \
                              int( self.rsvp_out_of_order_count_to_check )  and \
                          int( self.rsvp_retransmitted_count_received ) <= \
                              int( self.rsvp_retransmitted_count_to_check ) :
                        # FIXME REMOVE LATER ! self.is_search_item.set_test_results_string( "Global Neighbor: {} Detected:{} "
                        # FIXME REMOVE LATER !                                              "Interface Neighbor: {} Detected:{} "
                        # FIXME REMOVE LATER !                                              "Interface: {} Detected:{} "
                        # FIXME REMOVE LATER !                                              "Refresh Reduction:{} Detected:{} "
                        # FIXME REMOVE LATER !                                              "Remote Epoch: {} Detected: {} "
                        # FIXME REMOVE LATER !                                              "Out of Order Count: {} Detected: {} "
                        # FIXME REMOVE LATER !                                              "Retransmitted Count: {} Detected: {} ".
                        # FIXME REMOVE LATER !                                              format( self.rsvp_global_neighbor_to_check,
                        # FIXME REMOVE LATER !                                                      self.rsvp_global_neighbor_received,
                        # FIXME REMOVE LATER !                                                      self.rsvp_interface_neighbor_to_check,
                        # FIXME REMOVE LATER !                                                      self.rsvp_interface_neighbor_received,
                        # FIXME REMOVE LATER !                                                      self.rsvp_interface_to_check,
                        # FIXME REMOVE LATER !                                                      self.rsvp_interface_received,
                        # FIXME REMOVE LATER !                                                      self.rsvp_refresh_reduction_to_check,
                        # FIXME REMOVE LATER !                                                      self.rsvp_refresh_reduction_received,
                        # FIXME REMOVE LATER !                                                      self.rsvp_remote_epoch_to_check,
                        # FIXME REMOVE LATER !                                                      self.rsvp_remote_epoch_received,
                        # FIXME REMOVE LATER !                                                      self.rsvp_out_of_order_count_to_check,
                        # FIXME REMOVE LATER !                                                      self.rsvp_out_of_order_count_received,
                        # FIXME REMOVE LATER !                                                      self.rsvp_retransmitted_count_to_check,
                        # FIXME REMOVE LATER !                                                      self.rsvp_retransmitted_count_received ),
                        self.is_search_item.set_test_results_string( "RSVP global {} validated".
                                                                     format( self.rsvp_global_neighbor_to_check ),
                                                                     self.testcase_name,
                                                                     "Passed",
                                                                     "{}".format( self.command_issued_str ),
                                                                     "{}".format( self.analysis_data_filename ),
                                                                     str( self.line_number_head ),
                                                                     str( self.line_number ) )
                        break
                      else:
                        self.is_search_item.set_test_results_string( "Global Neighbor: {} Detected:{} "
                                                                     "Interface Neighbor: {} Detected:{} "
                                                                     "Interface: {} Detected:{} "
                                                                     "Refresh Reduction:{} Detected:{} "
                                                                     "Remote Epoch: {} Detected: {} "
                                                                     "Out of Order Count: {} Detected: {} "
                                                                     "Retransmitted Count: {} Detected: {} ".
                                                                     format( self.rsvp_global_neighbor_to_check,
                                                                             self.rsvp_global_neighbor_received,
                                                                             self.rsvp_interface_neighbor_to_check,
                                                                             self.rsvp_interface_neighbor_received,
                                                                             self.rsvp_interface_to_check,
                                                                             self.rsvp_interface_received,
                                                                             self.rsvp_refresh_reduction_to_check,
                                                                             self.rsvp_refresh_reduction_received,
                                                                             self.rsvp_remote_epoch_to_check,
                                                                             self.rsvp_remote_epoch_received,
                                                                             self.rsvp_out_of_order_count_to_check,
                                                                             self.rsvp_out_of_order_count_received,
                                                                             self.rsvp_retransmitted_count_to_check,
                                                                             self.rsvp_retransmitted_count_received ),
                                                                     self.testcase_name,
                                                                     "Failed",
                                                                     "{}".format( self.command_issued_str ),
                                                                     "{}".format( self.analysis_data_filename ),
                                                                     str( self.line_number_head ),
                                                                     str( self.line_number ) )
                        break
                break # Force enof so we break out of all for loops processing just read buffer data
          break # Force enof so we break out of all for loops processing just read buffer data
        else:
          continue
    if not self.found_rsvp_flag:
      self.is_search_item.set_test_results_string( "Global Neighbor {} expect but not received".
                                                   format( self.rsvp_global_neighbor_to_check ),
                                                   self.testcase_name,
                                                   "Failed",
                                                   "{}".format( self.command_issued_str ),
                                                   "{}".format( self.analysis_data_filename ),
                                                   str( self.line_number_head ),
                                                   str( self.line_number ) )
    self.reportFD.seek( 0 )
    return( self.reportFD )
  #----------------------------------------------------------------------------------------------------------------
  def juniper_rsvp_neighbors_analysis( self, seed_logical_dict, reportFD ):
    self.reportFD = reportFD
    self.seed_logical_dict = seed_logical_dict
    #--------------------------------------------------------------------------------------------------------------
    return (self.reportFD)
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
# Show BGP Summary Detail
#------------------------------------------------------------------------------------------------------------------
class ShowBgpSummary:
  "Show Bgp Summary"
  #----------------------------------------------------------------------------------------------------------------
  def __init__( self, parent = None ):
    self.name = "Show Bgp Summary"
    self.parent = parent
    self.filename_time_extension = parent.filename_time_extension
    self.process_reply = self.parent.process_reply
    self.cmd_list = self.parent.cmd_list
    self.is_search_item = self.parent.is_search_item
    self.testcase_name = self.parent.testcase_name
    self.analysis_data_filename = self.parent.analysis_data_filename
    self.seed_list = []
    self.command_issued = ""
    self.line_number = 0
    self.line_number_head = 0
    self.bgp_local_AS_number_received = ""
    self.bgp_generic_scan_interval_received = "0"
    self.bgp_nonstop_routing_received = ""
    self.bgp_table_state_received = ""
    self.bgp_table_id_received = "0"
    self.bgp_rd_version_received = "0"
    self.bgp_routing_table_version_received = "0"
    self.bgp_nsr_initsync_version_received = "0"
    self.bgp_nsr_issu_syncgroup_versions_received = "0"
    self.bgp_dampening_mode_received = ""
    self.bgp_scan_interval_received = "0"
    self.bgp_operating_mode_received = ""
    self.bgp_RcvTblVer_received = ""
    self.bgp_bRIBRIB_received = ""
    self.bgp_LabelVer_received = ""
    self.bgp_ImportVer_received = ""
    self.bgp_SendTblVer_received = ""
    self.bgp_StandbyVer_received = ""
  #----------------------------------------------------------------------------------------------------------------
  def execute( self, seed_logical_dict, reportFD ):
    self.reportFD = reportFD
    self.seed_logical_dict = dict( seed_logical_dict )
    #--------------------------------------------------------------------------------------------------------------
    try:
      if self.seed_logical_dict["device"] == "juniper":
        self.reportFD = self.juniper_bgp_summary_analysis( self.seed_logical_dict, self.reportFD )
      elif self.seed_logical_dict["device"] == "cisco":
        self.reportFD = self.cisco_bgp_summary_analysis( self.seed_logical_dict, self.reportFD )
      else:
        raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    except Exception as error:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    return ()
  #----------------------------------------------------------------------------------------------------------------
  def cisco_bgp_summary_analysis( self, seed_logical_dict, reportFD ):
    self.reportFD = reportFD
    self.seed_logical_dict = seed_logical_dict
    # -------------------------------------------------------------------------------------------------------------
    # FIXME UGLY!!! FIND A BETTER WAY THAN FLAGS !!!!!
    self.found_bgp_flag = False
    try:
      self.command_issued_str = self.seed_logical_dict["show bgp summary"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_router_identifier_to_check = self.seed_logical_dict["router identifier"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_local_AS_number_to_check = self.seed_logical_dict["local AS number"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_generic_scan_interval_to_check = self.seed_logical_dict["generic scan interval"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_nonstop_routing_to_check = self.seed_logical_dict["non-stop routing"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_table_state_to_check = self.seed_logical_dict["table state"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_table_id_to_check = self.seed_logical_dict["table id"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_routing_table_version_to_check = self.seed_logical_dict["routing table version"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_rd_version_to_check = self.seed_logical_dict["rd version"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_nsr_initsync_version_to_check = self.seed_logical_dict["nsr initsync version"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_nsr_issu_syncgroup_versions_to_check = self.seed_logical_dict["nsr issu syncgroup versions"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_dampening_mode_to_check = self.seed_logical_dict["dampening mode"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_scan_interval_to_check = self.seed_logical_dict["scan interval"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_operating_mode_to_check = self.seed_logical_dict["operating mode"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_StandbyVer_to_check = self.seed_logical_dict["StandbyVer"]
    except:
      self.bgp_StandbyVer_to_check = ""
    try:
      self.bgp_SendTblVer_to_check = self.seed_logical_dict["SendTblVer"]
    except:
      self.bgp_SendTblVer_to_check = ""
    try:
      self.bgp_ImportVer_to_check = self.seed_logical_dict["ImportVer"]
    except:
      self.bgp_ImportVer_to_check = ""
    try:
      self.bgp_LabelVer_to_check = self.seed_logical_dict["LabelVer"]
    except:
      self.bgp_LabelVer_to_check = ""
    try:
      self.bgp_bRIBRIB_to_check = self.seed_logical_dict["bRIBRIB"]
    except:
      self.bgp_bRIBRIB_to_check = ""
    try:
      self.bgp_RcvTblVer_to_check = self.seed_logical_dict["RcvTblVer"]
    except:
      self.bgp_RcvTblVer_to_check = ""
    try:
      self.bgp_Neighbor_to_check = self.seed_logical_dict["Neighbor"]
    except:
      self.bgp_Neighbor_to_check = ""
    try:
      self.bgp_Spk_to_check = self.seed_logical_dict["Spk"]
    except:
      self.bgp_Spk_to_check = ""
    try:
      self.bgp_AS_to_check = self.seed_logical_dict["AS"]
    except:
      self.bgp_AS_to_check = ""
    try:
      self.bgp_MsgRcvd_to_check = self.seed_logical_dict["MsgRcvd"]
    except:
      self.bgp_MsgRcvd_to_check = ""
    try:
      self.bgp_MsgSent_to_check = self.seed_logical_dict["MsgSent"]
    except:
      self.bgp_MsgSent_to_check = ""
    try:
      self.bgp_TblVer_to_check = self.seed_logical_dict["TblVer"]
    except:
      self.bgp_TblVer_to_check = ""
    try:
      self.bgp_InQ_to_check = self.seed_logical_dict["InQ"]
    except:
      self.bgp_InQ_to_check = ""
    try:
      self.bgp_OutQ_to_check = self.seed_logical_dict["OutQ"]
    except:
      self.bgp_OutQ_to_check = ""
    try:
      self.bgp_UpDown_to_check = self.seed_logical_dict["Up/Down"]
      self.bgp_UpDown_to_check = self.bgp_UpDown_to_check.replace( "~", ":" )
    except:
      self.bgp_UpDown_to_check = ""
    try:
      self.bgp_StPfxRcd_to_check = self.seed_logical_dict["St/PfxRcd"]
    except:
      self.bgp_StPfxRcd_to_check = ""
    # --------------------------------------------------------------------------------------------------------------
    self.line_length = 0
    for self.bgp_data in self.reportFD:
      self.line_number += 1
      self.line_length += len( self.bgp_data )
      if self.bgp_data.startswith( "\n" ):
        continue
      else:
        self.bgp_data_list = self.bgp_data.split()
        if self.bgp_data.startswith( "BGP router identifier" ):
          try:
            self.bgp_router_identifier_received = self.bgp_data_list[3].split( "," )[0]
          except:
            self.bgp_router_identifier_received = ""
          try:
            self.bgp_local_AS_number_received = self.bgp_data_list[7]
          except:
            self.bgp_local_AS_number_received = ""
          #------------------------------------------------------------------------------------------------------
          self.found_neighbors = False
          for self.bgp_data in self.reportFD:
            if self.bgp_data.startswith( "BGP router identifier" ):
              self.reportFD.seek( self.line_number )
              break
            self.line_number += 1
            self.line_length += len( self.bgp_data )
            if self.bgp_data.startswith( "\n" ):
              continue
            self.bgp_data_list = self.bgp_data.split()
            if self.bgp_data.startswith( "BGP generic scan interval" ):
              try:
                self.bgp_generic_scan_interval_received = self.bgp_data_list[4]
              except:
                self.bgp_generic_scan_interval_received = 0
              continue
            if self.bgp_data.startswith( "Non-stop routing" ):
              try:
                self.bgp_nonstop_routing_received = self.bgp_data_list[3]
              except:
                self.bgp_nonstop_routing_received = ""
              continue
            if self.bgp_data.startswith( "BGP table state" ):
              try:
                self.bgp_table_state_received = self.bgp_data_list[3]
              except:
                self.bgp_table_state_received = ""
              continue
            if self.bgp_data.startswith( "Table ID" ):
              try:
                self.bgp_table_id_received = self.bgp_data_list[2]
              except:
                self.bgp_table_id_received = ""
              try:
                self.bgp_rd_version_received = self.bgp_data_list[5]
              except:
                self.bgp_rd_version_received = ""
              continue
            if self.bgp_data.startswith( "BGP main routing table version" ):
              try:
                self.bgp_routing_table_version_received = self.bgp_data_list[5]
              except:
                self.bgp_routing_table_version_received = ""
              continue
            if self.bgp_data.startswith( "BGP NSR Initial initsync version" ):
              try:
                self.bgp_nsr_initsync_version_received = self.bgp_data_list[5]
              except:
                self.bgp_nsr_initsync_version_received = ""
              continue
            if self.bgp_data.startswith( "BGP NSR/ISSU Sync-Group versions" ):
              try:
                self.bgp_nsr_issu_syncgroup_versions_received = self.bgp_data_list[4]
              except:
                self.bgp_nsr_issu_syncgroup_versions_received = ""
              continue
            if self.bgp_data.startswith( "Dampening" ):
              try:
                self.bgp_dampening_mode_received = self.bgp_data_list[1]
              except:
                self.bgp_dampening_mode_received = ""
              continue
            if self.bgp_data.startswith( "BGP scan interval" ):
              try:
                self.bgp_scan_interval_received = self.bgp_data_list[4]
              except:
                self.bgp_scan_interval_received = ""
              continue
            if self.bgp_data.startswith( "BGP is operating" ):
              try:
                self.bgp_operating_mode_received = self.bgp_data_list[4]
              except:
                self.bgp_operating_mode_received = ""
              continue
            if self.bgp_data.startswith( "Speaker" ):
              try:
                self.bgp_RcvTblVer_received = self.bgp_data_list[4]
              except:
                self.bgp_RcvTblVer_received = ""
              try:
                self.bgp_bRIBRIB_received = self.bgp_data_list[4]
              except:
                self.bgp_bRIBRIB_received = ""
              try:
                self.bgp_LabelVer_received = self.bgp_data_list[4]
              except:
                self.bgp_LabelVer_received = ""
              try:
                self.bgp_ImportVer_received = self.bgp_data_list[4]
              except:
                self.bgp_ImportVer_received = ""
              try:
                self.bgp_SendTblVer_received = self.bgp_data_list[4]
              except:
                self.bgp_SendTblVer_received = ""
              try:
                self.bgp_StandbyVer_received = self.bgp_data_list[4]
              except:
                self.bgp_StandbyVer_received = ""
              continue
            if self.bgp_data.startswith( "Neighbor" ):
              for self.bgp_data in self.reportFD:
                if self.bgp_data.startswith( "\n" ):
                  continue
                else:
                  self.found_neighbors = True
                  self.bgp_Neighbor_received, \
                  self.bgp_Spk_received, \
                  self.bgp_AS_received, \
                  self.bgp_MsgRcvd_received, \
                  self.bgp_MsgSent_received, \
                  self.bgp_TblVer_received, \
                  self.bgp_InQ_received, \
                  self.bgp_OutQ_received, \
                  self.bgp_UpDown_received, \
                  self.bgp_StPfxRcd_received \
                    = self.bgp_data.split()
                  #-------------------------------------------------------------------------------------------------
                  if not self.bgp_Neighbor_to_check.startswith( self.bgp_Neighbor_received ):
                    continue
                  self.found_bgp_flag = True
                  #-------------------------------------------------------------------------------------------------
                  # Compares that really dont make sense to do:
                  # self.bgp_UpDown_received.startswith( self.bgp_UpDown_to_check )
                  #------------------------------------------------------------------------------------------------
                  if self.bgp_router_identifier_received.startswith( self.bgp_router_identifier_to_check ) and \
                     self.bgp_local_AS_number_received.startswith( self.bgp_local_AS_number_to_check ) and \
                     self.bgp_generic_scan_interval_received == self.bgp_generic_scan_interval_to_check and \
                     self.bgp_nonstop_routing_received.startswith( self.bgp_nonstop_routing_to_check ) and \
                     self.bgp_table_state_received.startswith( self.bgp_table_state_to_check ) and \
                     self.bgp_table_id_received.startswith( self.bgp_table_id_to_check ) or \
                     int( self.bgp_table_id_received, 0 ) != 0 and \
                     self.bgp_rd_version_received.startswith( self.bgp_rd_version_to_check ) or \
                     int( self.bgp_rd_version_received ) != 0 and \
                     self.bgp_routing_table_version_received.startswith(
                          self.bgp_routing_table_version_to_check ) or \
                     int( self.bgp_routing_table_version_received ) != 0 and \
                     self.bgp_nsr_initsync_version_received.startswith(
                          self.bgp_nsr_initsync_version_to_check ) and \
                     self.bgp_nsr_issu_syncgroup_versions_received.startswith(
                          self.bgp_nsr_issu_syncgroup_versions_to_check ) or \
                     int( self.bgp_nsr_issu_syncgroup_versions_received ) != 0 and \
                     self.bgp_dampening_mode_received.startswith( self.bgp_dampening_mode_to_check ) and \
                     self.bgp_scan_interval_received.startswith( self.bgp_scan_interval_to_check ) and \
                     self.bgp_operating_mode_received.startswith( self.bgp_operating_mode_to_check ) and \
                     self.bgp_RcvTblVer_received.startswith( self.bgp_RcvTblVer_to_check ) and \
                     self.bgp_bRIBRIB_received >= self.bgp_bRIBRIB_to_check and \
                     self.bgp_LabelVer_received.startswith( self.bgp_LabelVer_to_check ) or \
                     int( self.bgp_LabelVer_received ) != 0 and \
                     self.bgp_ImportVer_received.startswith( self.bgp_ImportVer_to_check ) or \
                     int( self.bgp_ImportVer_received ) != 0 and \
                     self.bgp_SendTblVer_received.startswith( self.bgp_SendTblVer_to_check ) or \
                     int( self.bgp_SendTblVer_received ) != 0 and \
                     self.bgp_StandbyVer_received.startswith( self.bgp_StandbyVer_to_check ) or \
                     int( self.bgp_StandbyVer_received ) != 0 and \
                     self.bgp_Spk_received.startswith( self.bgp_Spk_to_check ) and \
                     self.bgp_AS_received.startswith( self.bgp_AS_to_check ) and \
                     self.bgp_MsgRcvd_received >= self.bgp_MsgRcvd_to_check and \
                     self.bgp_MsgSent_received >= self.bgp_MsgSent_to_check and \
                     self.bgp_TblVer_received.startswith( self.bgp_TblVer_to_check ) and \
                     self.bgp_InQ_received == self.bgp_InQ_to_check and \
                     self.bgp_OutQ_received == self.bgp_OutQ_to_check and \
                     self.bgp_StPfxRcd_received.startswith( self.bgp_StPfxRcd_to_check ):
                    # FIXME REMOVE MAYBE ? self.is_search_item.set_test_results_string(
                    # FIXME REMOVE MAYBE ?                                              "Router Identifier: {}  Detected: {} "
                    # FIXME REMOVE MAYBE ?                                              "Local AS Number: {}  Detected: {} "
                    # FIXME REMOVE MAYBE ?                                              "Generic Scan Interval: {}  Detected: {} "
                    # FIXME REMOVE MAYBE ?                                              "Nonstop Routing: {}  Detected: {} "
                    # FIXME REMOVE MAYBE ?                                              "Table State: {}  Detected: {} "
                    # FIXME REMOVE MAYBE ?                                              "Table Id: {}  Detected: {} "
                    # FIXME REMOVE MAYBE ?                                              "Rd Version: {}  Detected: {} "
                    # FIXME REMOVE MAYBE ?                                              "Routing Table Version: {}  Detected: {} "
                    # FIXME REMOVE MAYBE ?                                              "Nsr Initsync Version: {}  Detected: {} "
                    # FIXME REMOVE MAYBE ?                                              "Nsr Issu Syncgroup Versions: {}  Detected: {} "
                    # FIXME REMOVE MAYBE ?                                              "Dampening: {}  Detected: {} "
                    # FIXME REMOVE MAYBE ?                                              "Scan Interval: {}  Detected: {} "
                    # FIXME REMOVE MAYBE ?                                              "Operating Mode: {}  Detected: {} "
                    # FIXME REMOVE MAYBE ?                                              "RcvTblVer: {}  Detected: {} "
                    # FIXME REMOVE MAYBE ?                                              "bRIB RIB: {}  Detected: {} "
                    # FIXME REMOVE MAYBE ?                                              "LabelVer: {}  Detected: {} "
                    # FIXME REMOVE MAYBE ?                                              "ImportVer: {}  Detected: {} "
                    # FIXME REMOVE MAYBE ?                                              "SendTblVer: {}  Detected: {} "
                    # FIXME REMOVE MAYBE ?                                              "StandbyVer: {}  Detected: {} "
                    # FIXME REMOVE MAYBE ?                                              "Neighbor: {}  Detected: {} "
                    # FIXME REMOVE MAYBE ?                                              "Spk: {}  Detected: {} "
                    # FIXME REMOVE MAYBE ?                                              "AS: {}  Detected: {} "
                    # FIXME REMOVE MAYBE ?                                              "MsgRcvd: {}  Detected: {} "
                    # FIXME REMOVE MAYBE ?                                              "MsgSent: {}  Detected: {} "
                    # FIXME REMOVE MAYBE ?                                              "TblVer: {}  Detected: {} "
                    # FIXME REMOVE MAYBE ?                                              "InQ: {}  Detected: {} "
                    # FIXME REMOVE MAYBE ?                                              "OutQ: {}  Detected: {} "
                    # FIXME REMOVE MAYBE ?                                              "UpDown: {}  Detected: {} "
                    # FIXME REMOVE MAYBE ?                                              "StPfxRcd: {}  Detected: {}".
                    # FIXME REMOVE MAYBE ?                                              format(
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_router_identifier_to_check,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_router_identifier_received,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_local_AS_number_to_check,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_local_AS_number_received,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_generic_scan_interval_to_check,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_generic_scan_interval_received,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_nonstop_routing_to_check,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_nonstop_routing_received,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_table_state_to_check,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_table_state_received,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_table_id_to_check,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_table_id_received,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_rd_version_to_check,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_rd_version_received,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_routing_table_version_to_check,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_routing_table_version_received,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_nsr_initsync_version_to_check,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_nsr_initsync_version_received,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_nsr_issu_syncgroup_versions_to_check,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_nsr_issu_syncgroup_versions_received,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_dampening_mode_to_check,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_dampening_mode_received,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_scan_interval_to_check,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_scan_interval_received,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_operating_mode_to_check,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_operating_mode_received,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_RcvTblVer_to_check,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_RcvTblVer_received,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_bRIBRIB_to_check,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_bRIBRIB_received,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_LabelVer_to_check,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_LabelVer_received,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_ImportVer_to_check,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_ImportVer_received,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_SendTblVer_to_check,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_SendTblVer_received,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_StandbyVer_to_check,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_StandbyVer_received,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_Neighbor_to_check,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_Neighbor_received,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_Spk_to_check,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_Spk_received,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_AS_to_check,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_AS_received,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_MsgRcvd_to_check,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_MsgRcvd_received,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_MsgSent_to_check,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_MsgSent_received,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_TblVer_to_check,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_TblVer_received,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_InQ_to_check,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_InQ_received,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_OutQ_to_check,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_OutQ_received,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_UpDown_to_check,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_UpDown_received,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_StPfxRcd_to_check,
                    # FIXME REMOVE MAYBE ?                                                      self.bgp_StPfxRcd_received
                    # FIXME REMOVE MAYBE ?                                                    ),
                    self.is_search_item.set_test_results_string( "BGP RID {} validated".
                                                                 format( self.bgp_router_identifier_to_check ),
                                                                 self.testcase_name,
                                                                 "Passed",
                                                                 "{}".format( self.command_issued_str ),
                                                                 "{}".format( self.analysis_data_filename ),
                                                                 str( self.line_number_head ),
                                                                 str( self.line_number )
                                                               )
                    self.reportFD.seek( 0, 2 )
                    break
                  else:
                    self.is_search_item.set_test_results_string(
                                                                 "Router Identifier: {}  Detected: {} "
                                                                 "Local AS Number: {}  Detected: {} "
                                                                 "Generic Scan Interval: {}  Detected: {} "
                                                                 "Nonstop Routing: {}  Detected: {} "
                                                                 "Table State: {}  Detected: {} "
                                                                 "Table Id: {}  Detected: {} "
                                                                 "Rd Version: {}  Detected: {} "
                                                                 "Routing Table Version: {}  Detected: {} "
                                                                 "Nsr Initsync Version: {}  Detected: {} "
                                                                 "Nsr Issu Syncgroup Versions: {}  Detected: {} "
                                                                 "Dampening: {}  Detected: {} "
                                                                 "Scan Interval: {}  Detected: {} "
                                                                 "Operating Mode: {}  Detected: {} "
                                                                 "RcvTblVer: {}  Detected: {} "
                                                                 "bRIB RIB: {}  Detected: {} "
                                                                 "LabelVer: {}  Detected: {} "
                                                                 "ImportVer: {}  Detected: {} "
                                                                 "SendTblVer: {}  Detected: {} "
                                                                 "StandbyVer: {}  Detected: {} "
                                                                 "Neighbor: {}  Detected: {} "
                                                                 "Spk: {}  Detected: {} "
                                                                 "AS: {}  Detected: {} "
                                                                 "MsgRcvd: {}  Detected: {} "
                                                                 "MsgSent: {}  Detected: {} "
                                                                 "TblVer: {}  Detected: {} "
                                                                 "InQ: {}  Detected: {} "
                                                                 "OutQ: {}  Detected: {} "
                                                                 "UpDown: {}  Detected: {} "
                                                                 "StPfxRcd: {}  Detected: {}".
                                                                   format(
                                                                   self.bgp_router_identifier_to_check,
                                                                   self.bgp_router_identifier_received,
                                                                   self.bgp_local_AS_number_to_check,
                                                                   self.bgp_local_AS_number_received,
                                                                   self.bgp_generic_scan_interval_to_check,
                                                                   self.bgp_generic_scan_interval_received,
                                                                   self.bgp_nonstop_routing_to_check,
                                                                   self.bgp_nonstop_routing_received,
                                                                   self.bgp_table_state_to_check,
                                                                   self.bgp_table_state_received,
                                                                   self.bgp_table_id_to_check,
                                                                   self.bgp_table_id_received,
                                                                   self.bgp_rd_version_to_check,
                                                                   self.bgp_rd_version_received,
                                                                   self.bgp_routing_table_version_to_check,
                                                                   self.bgp_routing_table_version_received,
                                                                   self.bgp_nsr_initsync_version_to_check,
                                                                   self.bgp_nsr_initsync_version_received,
                                                                   self.bgp_nsr_issu_syncgroup_versions_to_check,
                                                                   self.bgp_nsr_issu_syncgroup_versions_received,
                                                                   self.bgp_dampening_mode_to_check,
                                                                   self.bgp_dampening_mode_received,
                                                                   self.bgp_scan_interval_to_check,
                                                                   self.bgp_scan_interval_received,
                                                                   self.bgp_operating_mode_to_check,
                                                                   self.bgp_operating_mode_received,
                                                                   self.bgp_RcvTblVer_to_check,
                                                                   self.bgp_RcvTblVer_received,
                                                                   self.bgp_bRIBRIB_to_check,
                                                                   self.bgp_bRIBRIB_received,
                                                                   self.bgp_LabelVer_to_check,
                                                                   self.bgp_LabelVer_received,
                                                                   self.bgp_ImportVer_to_check,
                                                                   self.bgp_ImportVer_received,
                                                                   self.bgp_SendTblVer_to_check,
                                                                   self.bgp_SendTblVer_received,
                                                                   self.bgp_StandbyVer_to_check,
                                                                   self.bgp_StandbyVer_received,
                                                                   self.bgp_Neighbor_to_check,
                                                                   self.bgp_Neighbor_received,
                                                                   self.bgp_Spk_to_check,
                                                                   self.bgp_Spk_received,
                                                                   self.bgp_AS_to_check,
                                                                   self.bgp_AS_received,
                                                                   self.bgp_MsgRcvd_to_check,
                                                                   self.bgp_MsgRcvd_received,
                                                                   self.bgp_MsgSent_to_check,
                                                                   self.bgp_MsgSent_received,
                                                                   self.bgp_TblVer_to_check,
                                                                   self.bgp_TblVer_received,
                                                                   self.bgp_InQ_to_check,
                                                                   self.bgp_InQ_received,
                                                                   self.bgp_OutQ_to_check,
                                                                   self.bgp_OutQ_received,
                                                                   self.bgp_UpDown_to_check,
                                                                   self.bgp_UpDown_received,
                                                                   self.bgp_StPfxRcd_to_check,
                                                                   self.bgp_StPfxRcd_received
                                                                 ),
                                                                 self.testcase_name,
                                                                 "Failed",
                                                                 "{}".format( self.command_issued_str ),
                                                                 "{}".format( self.analysis_data_filename ),
                                                                 str( self.line_number_head ),
                                                                 str( self.line_number )
                                                               )
                    self.reportFD.seek( 0, 2 )
                    break
          if not self.found_neighbors:
              self.found_bgp_flag = True
              # -------------------------------------------------------------------------------------------------
              # Compares that really dont make sense to do:
              # self.bgp_UpDown_received.startswith( self.bgp_UpDown_to_check )
              # ------------------------------------------------------------------------------------------------
              if self.bgp_router_identifier_received.startswith( self.bgp_router_identifier_to_check ) and \
                 self.bgp_local_AS_number_received.startswith( self.bgp_local_AS_number_to_check ) and \
                 self.bgp_generic_scan_interval_received == self.bgp_generic_scan_interval_to_check and \
                 self.bgp_nonstop_routing_received.startswith( self.bgp_nonstop_routing_to_check ) and \
                 self.bgp_table_state_received.startswith( self.bgp_table_state_to_check ) and \
                 self.bgp_table_id_received.startswith( self.bgp_table_id_to_check ) or \
                      int( self.bgp_table_id_received, 0 ) != 0 and \
                 self.bgp_rd_version_received.startswith( self.bgp_rd_version_to_check ) or \
                      int( self.bgp_rd_version_received ) != 0 and \
                 self.bgp_routing_table_version_received.startswith(
                 self.bgp_routing_table_version_to_check ) or \
                      int( self.bgp_routing_table_version_received ) != 0 and \
                 self.bgp_nsr_initsync_version_received.startswith(
                 self.bgp_nsr_initsync_version_to_check ) and \
                 self.bgp_nsr_issu_syncgroup_versions_received.startswith(
                 self.bgp_nsr_issu_syncgroup_versions_to_check ) or \
                      int( self.bgp_nsr_issu_syncgroup_versions_received ) != 0 and \
                 self.bgp_dampening_mode_received.startswith(
                 self.bgp_dampening_mode_to_check ) and \
                 self.bgp_scan_interval_received.startswith( self.bgp_scan_interval_to_check ) and \
                 self.bgp_operating_mode_received.startswith( self.bgp_operating_mode_to_check ):
                self.is_search_item.set_test_results_string( "BGP RID {} validated".
                                                             format( self.bgp_router_identifier_to_check ),
                                                             self.testcase_name,
                                                             "Passed",
                                                             "{}".format( self.command_issued_str ),
                                                             "{}".format( self.analysis_data_filename ),
                                                             str( self.line_number_head ),
                                                             str( self.line_number )
                                                             )
                self.reportFD.seek( 0, 2 )
                break
              else:
                self.is_search_item.set_test_results_string(
                  "Router Identifier: {}  Detected: {} "
                  "Local AS Number: {}  Detected: {} "
                  "Generic Scan Interval: {}  Detected: {} "
                  "Nonstop Routing: {}  Detected: {} "
                  "Table State: {}  Detected: {} "
                  "Table Id: {}  Detected: {} "
                  "Rd Version: {}  Detected: {} "
                  "Routing Table Version: {}  Detected: {} "
                  "Nsr Initsync Version: {}  Detected: {} "
                  "Nsr Issu Syncgroup Versions: {}  Detected: {} "
                  "Dampening: {}  Detected: {} "
                  "Scan Interval: {}  Detected: {} "
                  "Operating Mode: {}  Detected: {} ".
                    format(
                    self.bgp_router_identifier_to_check,
                    self.bgp_router_identifier_received,
                    self.bgp_local_AS_number_to_check,
                    self.bgp_local_AS_number_received,
                    self.bgp_generic_scan_interval_to_check,
                    self.bgp_generic_scan_interval_received,
                    self.bgp_nonstop_routing_to_check,
                    self.bgp_nonstop_routing_received,
                    self.bgp_table_state_to_check,
                    self.bgp_table_state_received,
                    self.bgp_table_id_to_check,
                    self.bgp_table_id_received,
                    self.bgp_rd_version_to_check,
                    self.bgp_rd_version_received,
                    self.bgp_routing_table_version_to_check,
                    self.bgp_routing_table_version_received,
                    self.bgp_nsr_initsync_version_to_check,
                    self.bgp_nsr_initsync_version_received,
                    self.bgp_nsr_issu_syncgroup_versions_to_check,
                    self.bgp_nsr_issu_syncgroup_versions_received,
                    self.bgp_dampening_mode_to_check,
                    self.bgp_dampening_mode_received,
                    self.bgp_scan_interval_to_check,
                    self.bgp_scan_interval_received,
                    self.bgp_operating_mode_to_check,
                    self.bgp_operating_mode_received
                  ),
                  self.testcase_name,
                  "Failed",
                  "{}".format( self.command_issued_str ),
                  "{}".format( self.analysis_data_filename ),
                  str( self.line_number_head ),
                  str( self.line_number )
                )
                self.reportFD.seek( 0, 2 )
                break
          else:
            continue
    if not self.found_bgp_flag:
      self.is_search_item.set_test_results_string( "Neighbor {} expect but not received".
                                                   format( self.bgp_Neighbor_to_check ),
                                                   self.testcase_name,
                                                   "Failed",
                                                   "{}".format( self.command_issued_str ),
                                                   "{}".format( self.analysis_data_filename ),
                                                   str( self.line_number_head ),
                                                   str( self.line_number ) )
    self.reportFD.seek( 0 )
    return( self.reportFD )
  #----------------------------------------------------------------------------------------------------------------
  def juniper_bgp_summary_analysis( self, seed_logical_dict, reportFD ):
    self.reportFD = reportFD
    self.seed_logical_dict = seed_logical_dict
    #--------------------------------------------------------------------------------------------------------------
    return (self.reportFD)
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
# Show BGP Vrf All Neighbors Detail
#------------------------------------------------------------------------------------------------------------------
class ShowBgpVrfAllNeighborsDetail:
  "Show Bgp Vrf All Neighbors Detail"
  #----------------------------------------------------------------------------------------------------------------
  def __init__( self, parent = None ):
    self.name = "Show Bgp Vrf All Neighbors Detail"
    self.parent = parent
    self.filename_time_extension = parent.filename_time_extension
    self.process_reply = self.parent.process_reply
    self.cmd_list = self.parent.cmd_list
    self.is_search_item = self.parent.is_search_item
    self.testcase_name = self.parent.testcase_name
    self.analysis_data_filename = self.parent.analysis_data_filename
    self.seed_list = []
    self.command_issued = ""
    self.line_number = 0
    self.line_number_head = 0
    #--------------------------------------------------------------------------------------------------------------
    self.bgp_vrf_data_found = False
    self.bgp_vrf_name_completed = False
    self.bgp_vrf_name_to_check = ""
    self.bgp_vrf_name_received = ""
    self.bgp_vrf_neighbor_to_check = ""
    self.bgp_vrf_neighbor_received = ""
    self.bgp_vrf_remote_AS_to_check = ""
    self.bgp_vrf_remote_AS_received = ""
    self.bgp_vrf_local_AS_to_check = ""
    self.bgp_vrf_local_AS_received = ""
    self.bgp_vrf_link_to_check = ""
    self.bgp_vrf_link_received = ""
    self.bgp_vrf_description_to_check = ""
    self.bgp_vrf_description_received = ""
    self.bgp_vrf_remote_router_id_to_check = ""
    self.bgp_vrf_remote_router_id_received = ""
    self.bgp_vrf_state_to_check = ""
    self.bgp_vrf_state_received = ""
    self.bgp_vrf_up_time_to_check = "00:00:00"
    self.bgp_vrf_up_time_received = "00:00:00"
    self.bgp_vrf_accepted_prefixes_to_check = "0"
    self.bgp_vrf_accepted_prefixes_received = "0"
    self.bgp_vrf_denied_prefixes_to_check = "0"
    self.bgp_vrf_denied_prefixes_received = "0"
    self.bgp_vrf_advertise_prefixes_to_check = "0"
    self.bgp_vrf_advertise_prefixes_received = "0"
    self.bgp_vrf_suppressed_prefixes_to_check = "0"
    self.bgp_vrf_suppressed_prefixes_received = "0"
    self.bgp_vrf_withdrawn_prefixes_to_check = "0"
    self.bgp_vrf_withdrawn_prefixes_received = "0"
    self.bgp_vrf_connections_established_to_check = "0"
    self.bgp_vrf_connections_established_received = "0"
    self.bgp_vrf_connections_dropped_to_check = "0"
    self.bgp_vrf_connections_dropped_received = "0"
    self.bgp_vrf_local_host_to_check = ""
    self.bgp_vrf_local_host_received = ""
    self.bgp_vrf_local_port_to_check = ""
    self.bgp_vrf_local_port_received = ""
    self.bgp_vrf_foreign_host_to_check = ""
    self.bgp_vrf_foreign_host_received = ""
    self.bgp_vrf_foreign_port_to_check = ""
    self.bgp_vrf_foreign_port_received = ""
  #----------------------------------------------------------------------------------------------------------------
  def execute( self, seed_logical_dict, reportFD ):
    self.reportFD = reportFD
    self.seed_logical_dict = dict( seed_logical_dict )
    #--------------------------------------------------------------------------------------------------------------
    try:
      if self.seed_logical_dict["device"] == "juniper":
        self.reportFD = self.juniper_bgp_vrf_all_neighbors_analysis( self.seed_logical_dict, self.reportFD )
      elif self.seed_logical_dict["device"] == "cisco":
        self.reportFD = self.cisco_bgp_vrf_all_neighbors_analysis( self.seed_logical_dict, self.reportFD )
      else:
        raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    except Exception as error:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    return ()
  #----------------------------------------------------------------------------------------------------------------
  def cisco_bgp_vrf_all_neighbors_analysis( self, seed_logical_dict, reportFD ):
    self.reportFD = reportFD
    self.seed_logical_dict = seed_logical_dict
    #-------------------------------------------------------------------------------------------------------------
    try:
      self.command_issued_str = self.seed_logical_dict["show bgp vrf all neighbors detail"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.device = self.seed_logical_dict["device"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_vrf_name_to_check = self.seed_logical_dict["name"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_vrf_neighbor_to_check = self.seed_logical_dict["neighbor"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_vrf_remote_AS_to_check = self.seed_logical_dict["remote AS"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_vrf_local_AS_to_check = self.seed_logical_dict["local AS"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_vrf_link_to_check = self.seed_logical_dict["link"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_vrf_description_to_check = self.seed_logical_dict["description"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_vrf_remote_router_id_to_check = self.seed_logical_dict["remote router id"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_vrf_state_to_check = self.seed_logical_dict["state"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_vrf_up_time_to_check = self.seed_logical_dict["up time"].replace( ",", ":" )
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_vrf_accepted_prefixes_to_check = self.seed_logical_dict["accepted prefixes"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_vrf_denied_prefixes_to_check = self.seed_logical_dict["denied prefixes"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_vrf_advertise_prefixes_to_check = self.seed_logical_dict["advertise prefixes"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_vrf_suppressed_prefixes_to_check = self.seed_logical_dict["suppressed prefixes"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_vrf_withdrawn_prefixes_to_check = self.seed_logical_dict["withdrawn prefixes"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_vrf_connections_established_to_check = self.seed_logical_dict["connections established"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_vrf_connections_dropped_to_check = self.seed_logical_dict["connections dropped"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_vrf_local_host_to_check = self.seed_logical_dict["local host"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_vrf_local_port_to_check = self.seed_logical_dict["local port"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_vrf_foreign_host_to_check = self.seed_logical_dict["foreign host"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_vrf_foreign_port_to_check = self.seed_logical_dict["foreign port"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    #--------------------------------------------------------------------------------------------------------------
    self.line_length = 0
    self.ignore_this_name = False
    for self.bgp_data in self.reportFD:
      self.bgp_vrf_data_found = False
      self.bgp_vrf_name_completed = False
      self.line_length += len( self.bgp_data )
      if self.bgp_data.startswith( "\n" ):
        continue
      else:
        self.bgp_data_list = self.bgp_data.split()
        if self.bgp_data.startswith( "BGP neighbor is" ):
          self.bgp_vrf_data_found = True
          self.bgp_vrf_name_completed = True
          try:
            self.bgp_vrf_name_received = self.bgp_data_list[5]
          except:
            self.bgp_vrf_name_received = ""
          try:
            self.bgp_vrf_neighbor_received = self.bgp_data_list[3].split( "," )[0]
          except:
            self.bgp_vrf_neighbor_received = ""
          # ---------------------------------------------------------------------------------------------------------
          # Now cycle thru this neighbor
          for self.bgp_data in self.reportFD:
            if self.bgp_data.startswith( "VRF:" ) or \
               self.bgp_data.startswith( "BGP neighbor is" ):
              self.reportFD.seek( self.line_length )
              self.bgp_vrf_name_completed = True
              break  # done with this neighbor
            self.line_length += len( self.bgp_data )
            self.bgp_data_list = self.bgp_data.split()
            if self.bgp_data.startswith( "\n" ):
              continue
            if self.bgp_data.startswith( " Remote AS" ):
              try:
                self.bgp_vrf_remote_AS_received = self.bgp_data_list[2].split( "," )[0]
              except:
                self.bgp_vrf_remote_AS_received = ""
              try:
                self.bgp_vrf_local_AS_received = self.bgp_data_list[5].split( "," )[0]
              except:
                self.bgp_vrf_local_AS_received = ""
              try:
                self.bgp_vrf_link_received = self.bgp_data.split( "," )[2].split( "\n" )[0][1:]
              except:
                self.bgp_vrf_link_received = ""
              continue
            if self.bgp_data.startswith( " Description" ):
              try:
                self.bgp_vrf_description_received = self.bgp_data.split( ":" )[1].replace( "\"", "" ).split( "\n" )[0]
              except:
                self.bgp_vrf_description_received = ""
              continue
            if self.bgp_data.startswith( " Remote router ID" ):
              try:
                self.bgp_vrf_remote_router_id_received = self.bgp_data_list[3]
              except:
                self.bgp_vrf_remote_router_id_received = ""
              for self.bgp_data in self.reportFD:
                if self.bgp_data.startswith( " For Address Family:" ):
                  self.reportFD.seek( self.line_length )
                  break  # done with this neighbor
                self.line_length += len( self.bgp_data )
                self.bgp_data_list = self.bgp_data.split()
                if self.bgp_data.startswith( "\n" ):
                  continue
                if self.bgp_data.startswith( "  BGP state" ):
                  try:
                    self.bgp_vrf_state_received = self.bgp_data_list[3].split( "," )[0]
                  except:
                    self.bgp_vrf_state_received = ""
                  try:
                    self.bgp_vrf_up_time_received = self.bgp_data_list[6]
                  except:
                    self.bgp_vrf_up_time_received = ""
                  continue
              continue
            if self.bgp_data.startswith( " For Address Family:" ):
              for self.bgp_data in self.reportFD:
                if self.bgp_data.startswith( "VRF:" ) or \
                   self.bgp_data.startswith( " For Address Family:" ) or \
                   self.bgp_data.startswith( "BGP neighbor is" ):
                  self.reportFD.seek( self.line_length )
                  self.bgp_vrf_name_completed = True
                  break  # done with this neighbor
                self.line_length += len( self.bgp_data )
                self.bgp_data_list = self.bgp_data.split()
                if self.bgp_data.startswith( "\n" ):
                  continue
                if self.bgp_data.find( "accepted prefixes," ) != -1:
                  try:
                    self.bgp_vrf_accepted_prefixes_received = self.bgp_data_list[0]
                  except:
                    self.bgp_vrf_accepted_prefixes_received = "0"
                  continue
                if self.bgp_data.startswith( "  Cumulative no. of prefixes denied:" ):
                  try:
                    self.bgp_vrf_denied_prefixes_received = self.bgp_data_list[5].split( "." )[0]
                  except:
                    self.bgp_vrf_denied_prefixes_received = "0"
                  continue
                if self.bgp_data.startswith( "  Prefix advertised" ):
                  try:
                    self.bgp_vrf_advertise_prefixes_received = self.bgp_data_list[2].split( "," )[0]
                  except:
                    self.bgp_vrf_advertise_prefixes_received = "0"
                  try:
                    self.bgp_vrf_suppressed_prefixes_received = self.bgp_data_list[4].split( "," )[0]
                  except:
                    self.bgp_vrf_suppressed_prefixes_received = "0"
                  try:
                    self.bgp_vrf_withdrawn_prefixes_received = self.bgp_data_list[6].split( "\n" )[0]
                  except:
                    self.bgp_vrf_withdrawn_prefixes_received = "0"
                  continue
                if self.bgp_data.startswith( "  Connections established" ):
                  try:
                    self.bgp_vrf_connections_established_received = self.bgp_data_list[2].split( ";" )[0]
                  except:
                    self.bgp_vrf_connections_established_received = "0"
                  try:
                    self.bgp_vrf_connections_dropped_received = self.bgp_data_list[4].split( "\n" )[0]
                  except:
                    self.bgp_vrf_connections_dropped_received = "0"
                  continue
                if self.bgp_data.startswith( "  Local host" ):
                  try:
                    self.bgp_vrf_local_host_received = self.bgp_data_list[2].split( "," )[0]
                  except:
                    self.bgp_vrf_local_host_received = "0"
                  try:
                    self.bgp_vrf_local_port_received = self.bgp_data_list[5].split( "," )[0]
                  except:
                    self.bgp_vrf_local_port_received = "0"
                  continue
                if self.bgp_data.startswith( "  Foreign host" ):
                  try:
                    self.bgp_vrf_foreign_host_received = self.bgp_data_list[2].split( "," )[0]
                  except:
                    self.bgp_vrf_foreign_host_received = "0"
                  try:
                    self.bgp_vrf_foreign_port_received = self.bgp_data_list[5].split( "\n" )[0]
                  except:
                    self.bgp_vrf_foreign_port_received = "0"
                  continue
              if self.bgp_vrf_name_completed:
                self.build_and_generate_report()
                break
          if self.bgp_vrf_name_completed:
            self.build_and_generate_report()
            break
          continue  # done with this neighbor
    #------------------------------------------------------------------------------------------------------
    if not self.bgp_vrf_data_found:
      self.pass_fail = "Failed"
      self.message = "BGP VRF data not found."
      self.generate_report( self.pass_fail, self.message )
    return()
  #----------------------------------------------------------------------------------------------------------------
  def build_and_generate_report( self ):
    self.bgp_vrf_name_completed = False
    if self.bgp_vrf_name_to_check != self.bgp_vrf_name_received and \
        self.bgp_vrf_neighbor_to_check != self.bgp_vrf_neighbor_received or \
        self.bgp_vrf_name_to_check != self.bgp_vrf_name_received and \
        self.bgp_vrf_neighbor_to_check == self.bgp_vrf_neighbor_received or \
        self.bgp_vrf_name_to_check == self.bgp_vrf_name_received and \
        self.bgp_vrf_neighbor_to_check != self.bgp_vrf_neighbor_received:
      return()
    self.reportFD.seek( 0, 2 )
    #----------------------------------------------------------------------------
    # FIXME VALUES WITH ISSUES
    # self.bgp_vrf_foreign_port_to_check != self.bgp_vrf_foreign_port_received:
    # self.bgp_vrf_local_port_to_check != self.bgp_vrf_local_port_received or
    #----------------------------------------------------------------------------
    if self.bgp_vrf_remote_AS_to_check != self.bgp_vrf_remote_AS_received or \
       self.bgp_vrf_local_AS_to_check != self.bgp_vrf_local_AS_received or \
       self.bgp_vrf_link_to_check != self.bgp_vrf_link_received or \
       self.bgp_vrf_description_to_check != self.bgp_vrf_description_received or \
       self.bgp_vrf_remote_router_id_to_check != self.bgp_vrf_remote_router_id_received or \
       self.bgp_vrf_state_to_check != self.bgp_vrf_state_received or \
       self.bgp_vrf_up_time_received == "00:00:00" or \
       self.bgp_vrf_accepted_prefixes_to_check != "-1" and \
       int( self.bgp_vrf_accepted_prefixes_to_check ) > \
            int( self.bgp_vrf_accepted_prefixes_received ) or \
       self.bgp_vrf_denied_prefixes_to_check != "-1" and \
       int( self.bgp_vrf_denied_prefixes_received ) > \
            int( self.bgp_vrf_denied_prefixes_to_check ) or \
       self.bgp_vrf_advertise_prefixes_to_check != "-1" and \
       int( self.bgp_vrf_advertise_prefixes_to_check ) > \
            int( self.bgp_vrf_advertise_prefixes_received ) or \
       self.bgp_vrf_suppressed_prefixes_to_check != "-1" and \
       int( self.bgp_vrf_suppressed_prefixes_received ) > \
            int( self.bgp_vrf_suppressed_prefixes_to_check ) or \
       self.bgp_vrf_withdrawn_prefixes_to_check != "-1" and \
       int( self.bgp_vrf_withdrawn_prefixes_received ) > \
            int( self.bgp_vrf_withdrawn_prefixes_to_check ) or \
       int( self.bgp_vrf_connections_established_to_check ) > \
            int( self.bgp_vrf_connections_established_received ) or \
       self.bgp_vrf_connections_dropped_to_check != "-1" and \
       int( self.bgp_vrf_connections_dropped_received ) > \
            int( self.bgp_vrf_connections_dropped_to_check ) or \
       self.bgp_vrf_local_host_to_check != self.bgp_vrf_local_host_received or \
       self.bgp_vrf_foreign_host_to_check != self.bgp_vrf_foreign_host_received:
      self.message = \
        "Name:{} Detected:{} " \
        "Neighbor:{} Detected:{} " \
        "Remote AS:{} Detected:{} " \
        "Local AS:{} Detected:{} " \
        "Link:{} Detected:{} " \
        "Description:{} Detected:{} " \
        "Remote Router Id:{} Detected:{} " \
        "State:{} Detected:{} " \
        "Up Time:{} Detected:{} " \
        "Accepted Prefixes:{} Detected:{} " \
        "Denied Prefixes:{} Detected:{} " \
        "Advertise Prefixes:{} Detected:{} " \
        "Suppressed Prefixes:{} Detected:{} " \
        "Withdrawn Prefixes:{} Detected:{} " \
        "Connections Established:{} Detected:{} " \
        "Connections Dropped:{} Detected:{} " \
        "Local Host:{} Detected:{} " \
        "Local Port:{} Detected:{} " \
        "Foreign Host:{} Detected:{} " \
        "Foreign Port:{} Detected:{} ". \
          format(
          self.bgp_vrf_name_to_check,
          self.bgp_vrf_name_received,
          self.bgp_vrf_neighbor_to_check,
          self.bgp_vrf_neighbor_received,
          self.bgp_vrf_remote_AS_to_check,
          self.bgp_vrf_remote_AS_received,
          self.bgp_vrf_local_AS_to_check,
          self.bgp_vrf_local_AS_received,
          self.bgp_vrf_link_to_check,
          self.bgp_vrf_link_received,
          self.bgp_vrf_description_to_check,
          self.bgp_vrf_description_received,
          self.bgp_vrf_remote_router_id_to_check,
          self.bgp_vrf_remote_router_id_received,
          self.bgp_vrf_state_to_check,
          self.bgp_vrf_state_received,
          self.bgp_vrf_up_time_to_check,
          self.bgp_vrf_up_time_received,
          self.bgp_vrf_accepted_prefixes_to_check,
          self.bgp_vrf_accepted_prefixes_received,
          self.bgp_vrf_denied_prefixes_to_check,
          self.bgp_vrf_denied_prefixes_received,
          self.bgp_vrf_advertise_prefixes_to_check,
          self.bgp_vrf_advertise_prefixes_received,
          self.bgp_vrf_suppressed_prefixes_to_check,
          self.bgp_vrf_suppressed_prefixes_received,
          self.bgp_vrf_withdrawn_prefixes_to_check,
          self.bgp_vrf_withdrawn_prefixes_received,
          self.bgp_vrf_connections_established_to_check,
          self.bgp_vrf_connections_established_received,
          self.bgp_vrf_connections_dropped_to_check,
          self.bgp_vrf_connections_dropped_received,
          self.bgp_vrf_local_host_to_check,
          self.bgp_vrf_local_host_received,
          self.bgp_vrf_local_port_to_check,
          self.bgp_vrf_local_port_received,
          self.bgp_vrf_foreign_host_to_check,
          self.bgp_vrf_foreign_host_received,
          self.bgp_vrf_foreign_port_to_check,
          self.bgp_vrf_foreign_port_received
        )
      self.pass_fail = "Failed"
      self.generate_report( self.pass_fail, self.message )
      return ()
    else:
      self.pass_fail = "Passed"
      self.message = "{}/{} validated".format( self.bgp_vrf_name_to_check, self.bgp_vrf_neighbor_to_check )
      self.generate_report( self.pass_fail, self.message )
      return ()
  #----------------------------------------------------------------------------------------------------------------
  def generate_report( self, pass_fail, message ):
    self.pass_fail = pass_fail
    self.message = message
    self.is_search_item.set_test_results_string(
                                                  self.message,
                                                  self.testcase_name,
                                                  self.pass_fail,
                                                  "{}".format( self.command_issued_str ),
                                                  "{}".format( self.analysis_data_filename ),
                                                  str( self.line_number_head ),
                                                  str( self.line_number )
                                                )
    return()
  #----------------------------------------------------------------------------------------------------------------
  def juniper_bgp_vrf_all_neighbors_analysis( self, seed_logical_dict, reportFD ):
    self.reportFD = reportFD
    self.seed_logical_dict = seed_logical_dict
    return()
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
# Show BGP VRF Summary
#------------------------------------------------------------------------------------------------------------------
class ShowBgpVrf:
  "Show Bgp Vrf"
  #----------------------------------------------------------------------------------------------------------------
  def __init__( self, parent = None ):
    self.name = "Show Bgp Vrf"
    self.parent = parent
    self.filename_time_extension = parent.filename_time_extension
    self.process_reply = self.parent.process_reply
    self.cmd_list = self.parent.cmd_list
    self.is_search_item = self.parent.is_search_item
    self.testcase_name = self.parent.testcase_name
    self.analysis_data_filename = self.parent.analysis_data_filename
    self.seed_list = []
    self.command_issued = ""
    self.line_number = 0
    self.line_number_head = 0
  #----------------------------------------------------------------------------------------------------------------
  def execute( self, seed_logical_dict, reportFD ):
    self.reportFD = reportFD
    self.seed_logical_dict = dict( seed_logical_dict )
    #--------------------------------------------------------------------------------------------------------------
    try:
      if self.seed_logical_dict["device"] == "juniper":
        self.reportFD = self.juniper_bgp_vrf_analysis( self.seed_logical_dict, self.reportFD )
      elif self.seed_logical_dict["device"] == "cisco":
        self.reportFD = self.cisco_bgp_vrf_analysis( self.seed_logical_dict, self.reportFD )
      else:
        raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    except Exception as error:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    return ()
  #----------------------------------------------------------------------------------------------------------------
  def cisco_bgp_vrf_analysis( self, seed_logical_dict, reportFD ):
    self.reportFD = reportFD
    self.seed_logical_dict = seed_logical_dict
    # -------------------------------------------------------------------------------------------------------------
    # FIXME UGLY!!! FIND A BETTER WAY THAN FLAGS !!!!!
    self.found_bgp_flag = False
    try:
      self.command_issued_str = self.seed_logical_dict["show bgp vrf"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_vrf_name_to_check = self.seed_logical_dict["vrf name"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_vrf_state_to_check = self.seed_logical_dict["vrf state"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_route_distinguisher_to_check = self.seed_logical_dict["route distinguisher"]
      self.bgp_route_distinguisher_to_check = self.bgp_route_distinguisher_to_check.replace( "~", ":" )
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_vrf_id_to_check = self.seed_logical_dict["vrf id"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_router_identifier_to_check = self.seed_logical_dict["router identifier"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_local_AS_number_to_check = self.seed_logical_dict["local AS number"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_nonstop_routing_to_check = self.seed_logical_dict["non-stop routing"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_table_state_to_check = self.seed_logical_dict["table state"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_table_id_to_check = self.seed_logical_dict["table id"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_routing_table_version_to_check = self.seed_logical_dict["routing table version"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_rd_version_to_check = self.seed_logical_dict["rd version"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_nsr_initsync_version_to_check = self.seed_logical_dict["nsr initsync version"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_nsr_issu_syncgroup_versions_to_check = self.seed_logical_dict["nsr issu syncgroup versions"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_operating_mode_to_check = self.seed_logical_dict["operating mode"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_StandbyVer_to_check = self.seed_logical_dict["StandbyVer"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_SendTblVer_to_check = self.seed_logical_dict["SendTblVer"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_ImportVer_to_check = self.seed_logical_dict["ImportVer"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_LabelVer_to_check = self.seed_logical_dict["LabelVer"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_bRIBRIB_to_check = self.seed_logical_dict["bRIBRIB"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_RcvTblVer_to_check = self.seed_logical_dict["RcvTblVer"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_Neighbor_to_check = self.seed_logical_dict["Neighbor"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_Spk_to_check = self.seed_logical_dict["Spk"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_AS_to_check = self.seed_logical_dict["AS"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_MsgRcvd_to_check = self.seed_logical_dict["MsgRcvd"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_MsgSent_to_check = self.seed_logical_dict["MsgSent"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_TblVer_to_check = self.seed_logical_dict["TblVer"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_InQ_to_check = self.seed_logical_dict["InQ"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_OutQ_to_check = self.seed_logical_dict["OutQ"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_UpDown_to_check = self.seed_logical_dict["Up/Down"]
      self.bgp_UpDown_to_check = self.bgp_UpDown_to_check.replace( "~", ":" )
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.bgp_StPfxRcd_to_check = self.seed_logical_dict["St/PfxRcd"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    #--------------------------------------------------------------------------------------------------------------
    self.line_length = 0
    for self.bgp_data in self.reportFD:
      self.line_number += 1
      self.line_length += len( self.bgp_data )
      if self.bgp_data.startswith( "\n" ):
        continue
      else:
        self.bgp_data_list = self.bgp_data.split()
        if self.bgp_data.startswith( "BGP VRF" ):
          try:
            self.bgp_vrf_name_received = self.bgp_data_list[2].split( "," )[0]
          except:
            self.bgp_vrf_name_received = ""
          try:
            self.bgp_vrf_state_received = self.bgp_data_list[4]
          except:
            self.bgp_vrf_state_received = ""
          continue
        if self.bgp_data.startswith( "BGP Route Distinguisher" ):
          try:
            self.bgp_route_distinguisher_received = self.bgp_data_list[3]
          except:
            self.bgp_route_distinguisher_received = ""
          continue
        if self.bgp_data.startswith( "VRF ID" ):
          try:
            self.bgp_vrf_id_received = self.bgp_data_list[2]
          except:
            self.bgp_vrf_id_received = ""
          continue
        if self.bgp_data.startswith( "BGP router identifier" ):
          try:
            self.bgp_router_identifier_received = self.bgp_data_list[3].split( "," )[0]
          except:
            self.bgp_router_identifier_received = ""
          try:
            self.bgp_local_AS_number_received = self.bgp_data_list[7]
          except:
            self.bgp_local_AS_number_received = ""
          continue
        if self.bgp_data.startswith( "Non-stop routing" ):
          try:
            self.bgp_nonstop_routing_received = self.bgp_data_list[3]
          except:
            self.bgp_nonstop_routing_received = ""
          continue
        if self.bgp_data.startswith( "BGP table state" ):
          try:
            self.bgp_table_state_received = self.bgp_data_list[3]
          except:
            self.bgp_table_state_received = ""
          continue
        if self.bgp_data.startswith( "Table ID" ):
          try:
            self.bgp_table_id_received = self.bgp_data_list[2]
          except:
            self.bgp_table_id_received = ""
          try:
            self.bgp_rd_version_received = self.bgp_data_list[5]
          except:
            self.bgp_rd_version_received = ""
          continue
        if self.bgp_data.startswith( "BGP main routing table version" ):
          try:
            self.bgp_routing_table_version_received = self.bgp_data_list[5]
          except:
            self.bgp_routing_table_version_received = ""
          continue
        if self.bgp_data.startswith( "BGP NSR Initial initsync version" ):
          try:
            self.bgp_nsr_initsync_version_received = self.bgp_data_list[5]
          except:
            self.bgp_nsr_initsync_version_received = ""
          continue
        if self.bgp_data.startswith( "BGP NSR/ISSU Sync-Group versions" ):
          try:
            self.bgp_nsr_issu_syncgroup_versions_received = self.bgp_data_list[4]
          except:
            self.bgp_nsr_issu_syncgroup_versions_received = ""
          continue
        if self.bgp_data.startswith( "BGP is operating" ):
          try:
            self.bgp_operating_mode_received = self.bgp_data_list[4]
          except:
            self.bgp_operating_mode_received = ""
          continue
        if self.bgp_data.startswith( "Speaker" ):
          try:
            self.bgp_RcvTblVer_received = self.bgp_data_list[4]
          except:
            self.bgp_RcvTblVer_received = ""
          try:
            self.bgp_bRIBRIB_received = self.bgp_data_list[4]
          except:
            self.bgp_bRIBRIB_received = ""
          try:
            self.bgp_LabelVer_received = self.bgp_data_list[4]
          except:
            self.bgp_LabelVer_received = ""
          try:
            self.bgp_ImportVer_received = self.bgp_data_list[4]
          except:
            self.bgp_ImportVer_received = ""
          try:
            self.bgp_SendTblVer_received = self.bgp_data_list[4]
          except:
            self.bgp_SendTblVer_received = ""
          try:
            self.bgp_StandbyVer_received = self.bgp_data_list[4]
          except:
            self.bgp_StandbyVer_received = ""
          continue
        if self.bgp_data.startswith( "Neighbor" ):
          for self.bgp_data in self.reportFD:
            if self.bgp_data.startswith( "\n" ):
              continue
            else:
              self.bgp_Neighbor_received, \
              self.bgp_Spk_received, \
              self.bgp_AS_received, \
              self.bgp_MsgRcvd_received, \
              self.bgp_MsgSent_received, \
              self.bgp_TblVer_received, \
              self.bgp_InQ_received, \
              self.bgp_OutQ_received, \
              self.bgp_UpDown_received, \
              self.bgp_StPfxRcd_received \
                = self.bgp_data.split()
              #-------------------------------------------------------------------------------------------------
              if not self.bgp_Neighbor_to_check.startswith( self.bgp_Neighbor_received ):
                continue
              self.found_bgp_flag = True
              #-------------------------------------------------------------------------------------------------
              # Compares that really dont make sense to do:
              # self.bgp_UpDown_received.startswith( self.bgp_UpDown_to_check )
              # self.bgp_vrf_id_received.startswith( self.bgp_vrf_id_to_check )
              # self.bgp_table_id_received.startswith( self.bgp_table_id_to_check )
              #------------------------------------------------------------------------------------------------
              if self.bgp_vrf_name_received.startswith( self.bgp_vrf_name_to_check ) and \
                 self.bgp_vrf_state_received.startswith( self.bgp_vrf_state_to_check ) and \
                 self.bgp_route_distinguisher_received.startswith( self.bgp_route_distinguisher_to_check ) and \
                 self.bgp_router_identifier_received.startswith( self.bgp_router_identifier_to_check ) and \
                 self.bgp_local_AS_number_received.startswith( self.bgp_local_AS_number_to_check ) and \
                 self.bgp_nonstop_routing_received.startswith( self.bgp_nonstop_routing_to_check ) and \
                 self.bgp_table_state_received.startswith( self.bgp_table_state_to_check ) and \
                 self.bgp_rd_version_received.startswith( self.bgp_rd_version_to_check ) and \
                 self.bgp_routing_table_version_received.startswith( self.bgp_routing_table_version_to_check ) and \
                 self.bgp_nsr_initsync_version_received.startswith( self.bgp_nsr_initsync_version_to_check ) and \
                 self.bgp_nsr_issu_syncgroup_versions_received.\
                     startswith( self.bgp_nsr_issu_syncgroup_versions_to_check ) and \
                 self.bgp_operating_mode_received.startswith( self.bgp_operating_mode_to_check ) and \
                 self.bgp_RcvTblVer_received.startswith( self.bgp_RcvTblVer_to_check ) and \
                 self.bgp_bRIBRIB_received.startswith( self.bgp_bRIBRIB_to_check ) and \
                 self.bgp_LabelVer_received.startswith( self.bgp_LabelVer_to_check ) and \
                 self.bgp_ImportVer_received.startswith( self.bgp_ImportVer_to_check ) and \
                 self.bgp_SendTblVer_received.startswith( self.bgp_SendTblVer_to_check ) and \
                 self.bgp_StandbyVer_received.startswith( self.bgp_StandbyVer_to_check ) and \
                 self.bgp_Spk_received.startswith( self.bgp_Spk_to_check ) and \
                 self.bgp_AS_received.startswith( self.bgp_AS_to_check ) and \
                 int( self.bgp_MsgRcvd_received ) >= int( self.bgp_MsgRcvd_to_check ) and \
                 int( self.bgp_MsgSent_received ) >= int( self.bgp_MsgSent_to_check ) and \
                 self.bgp_TblVer_received.startswith( self.bgp_TblVer_to_check ) and \
                 int( self.bgp_InQ_received ) >= int( self.bgp_InQ_to_check ) and \
                 int( self.bgp_OutQ_received ) >= int( self.bgp_OutQ_to_check ) and \
                 self.bgp_StPfxRcd_received.startswith( self.bgp_StPfxRcd_to_check ):
                self.is_search_item.set_test_results_string(
                  "BGP VRF: {}  Detected: {} "
                  "VRF State: {}  Detected: {} "
                  "Route Distinguisher: {}  Detected: {} "
                  "Router Identifier: {}  Detected: {} "
                  "Local AS Number: {}  Detected: {} "
                  "Nonstop Routing: {}  Detected: {} "
                  "Table State: {}  Detected: {} "
                  "Rd Version: {}  Detected: {} "
                  "Routing Table Version: {}  Detected: {} "
                  "Nsr Initsync Version: {}  Detected: {} "
                  "Nsr Issu Syncgroup Versions: {}  Detected: {} "
                  "Operating Mode: {}  Detected: {} "
                  "RcvTblVer: {}  Detected: {} "
                  "bRIB RIB: {}  Detected: {} "
                  "LabelVer: {}  Detected: {} "
                  "ImportVer: {}  Detected: {} "
                  "SendTblVer: {}  Detected: {} "
                  "StandbyVer: {}  Detected: {} "
                  "Neighbor: {}  Detected: {} "
                  "Spk: {}  Detected: {} "
                  "AS: {}  Detected: {} "
                  "MsgRcvd: {}  Detected: {} "
                  "MsgSent: {}  Detected: {} "
                  "TblVer: {}  Detected: {} "
                  "InQ: {}  Detected: {} "
                  "OutQ: {}  Detected: {} "
                  "UpDown: {}  Detected: {} "
                  "StPfxRcd: {}  Detected: {}".
                    format(
                    self.bgp_vrf_name_to_check,
                    self.bgp_vrf_name_received,
                    self.bgp_vrf_state_to_check,
                    self.bgp_vrf_state_received,
                    self.bgp_route_distinguisher_to_check,
                    self.bgp_route_distinguisher_received,
                    self.bgp_router_identifier_to_check,
                    self.bgp_router_identifier_received,
                    self.bgp_local_AS_number_to_check,
                    self.bgp_local_AS_number_received,
                    self.bgp_nonstop_routing_to_check,
                    self.bgp_nonstop_routing_received,
                    self.bgp_table_state_to_check,
                    self.bgp_table_state_received,
                    self.bgp_rd_version_to_check,
                    self.bgp_rd_version_received,
                    self.bgp_routing_table_version_to_check,
                    self.bgp_routing_table_version_received,
                    self.bgp_nsr_initsync_version_to_check,
                    self.bgp_nsr_initsync_version_received,
                    self.bgp_nsr_issu_syncgroup_versions_to_check,
                    self.bgp_nsr_issu_syncgroup_versions_received,
                    self.bgp_operating_mode_to_check,
                    self.bgp_operating_mode_received,
                    self.bgp_RcvTblVer_to_check,
                    self.bgp_RcvTblVer_received,
                    self.bgp_bRIBRIB_to_check,
                    self.bgp_bRIBRIB_received,
                    self.bgp_LabelVer_to_check,
                    self.bgp_LabelVer_received,
                    self.bgp_ImportVer_to_check,
                    self.bgp_ImportVer_received,
                    self.bgp_SendTblVer_to_check,
                    self.bgp_SendTblVer_received,
                    self.bgp_StandbyVer_to_check,
                    self.bgp_StandbyVer_received,
                    self.bgp_Neighbor_to_check,
                    self.bgp_Neighbor_received,
                    self.bgp_Spk_to_check,
                    self.bgp_Spk_received,
                    self.bgp_AS_to_check,
                    self.bgp_AS_received,
                    self.bgp_MsgRcvd_to_check,
                    self.bgp_MsgRcvd_received,
                    self.bgp_MsgSent_to_check,
                    self.bgp_MsgSent_received,
                    self.bgp_TblVer_to_check,
                    self.bgp_TblVer_received,
                    self.bgp_InQ_to_check,
                    self.bgp_InQ_received,
                    self.bgp_OutQ_to_check,
                    self.bgp_OutQ_received,
                    self.bgp_UpDown_to_check,
                    self.bgp_UpDown_received,
                    self.bgp_StPfxRcd_to_check,
                    self.bgp_StPfxRcd_received
                  ),
                  self.testcase_name,
                  "Passed",
                  "{}".format( self.command_issued_str ),
                  "{}".format( self.analysis_data_filename ),
                  str( self.line_number_head ),
                  str( self.line_number )
                )
                break
              else:
                self.is_search_item.set_test_results_string(
                  "BGP VRF: {}  Detected: {} "
                  "VRF State: {}  Detected: {} "
                  "Route Distinguisher: {}  Detected: {} "
                  "Router Identifier: {}  Detected: {} "
                  "Local AS Number: {}  Detected: {} "
                  "Nonstop Routing: {}  Detected: {} "
                  "Table State: {}  Detected: {} "
                  "Rd Version: {}  Detected: {} "
                  "Routing Table Version: {}  Detected: {} "
                  "Nsr Initsync Version: {}  Detected: {} "
                  "Nsr Issu Syncgroup Versions: {}  Detected: {} "
                  "Operating Mode: {}  Detected: {} "
                  "RcvTblVer: {}  Detected: {} "
                  "bRIB RIB: {}  Detected: {} "
                  "LabelVer: {}  Detected: {} "
                  "ImportVer: {}  Detected: {} "
                  "SendTblVer: {}  Detected: {} "
                  "StandbyVer: {}  Detected: {} "
                  "Neighbor: {}  Detected: {} "
                  "Spk: {}  Detected: {} "
                  "AS: {}  Detected: {} "
                  "MsgRcvd: {}  Detected: {} "
                  "MsgSent: {}  Detected: {} "
                  "TblVer: {}  Detected: {} "
                  "InQ: {}  Detected: {} "
                  "OutQ: {}  Detected: {} "
                  "UpDown: {}  Detected: {} "
                  "StPfxRcd: {}  Detected: {}".
                    format(
                    self.bgp_vrf_name_to_check,
                    self.bgp_vrf_name_received,
                    self.bgp_vrf_state_to_check,
                    self.bgp_vrf_state_received,
                    self.bgp_route_distinguisher_to_check,
                    self.bgp_route_distinguisher_received,
                    self.bgp_router_identifier_to_check,
                    self.bgp_router_identifier_received,
                    self.bgp_local_AS_number_to_check,
                    self.bgp_local_AS_number_received,
                    self.bgp_nonstop_routing_to_check,
                    self.bgp_nonstop_routing_received,
                    self.bgp_table_state_to_check,
                    self.bgp_table_state_received,
                    self.bgp_rd_version_to_check,
                    self.bgp_rd_version_received,
                    self.bgp_routing_table_version_to_check,
                    self.bgp_routing_table_version_received,
                    self.bgp_nsr_initsync_version_to_check,
                    self.bgp_nsr_initsync_version_received,
                    self.bgp_nsr_issu_syncgroup_versions_to_check,
                    self.bgp_nsr_issu_syncgroup_versions_received,
                    self.bgp_operating_mode_to_check,
                    self.bgp_operating_mode_received,
                    self.bgp_RcvTblVer_to_check,
                    self.bgp_RcvTblVer_received,
                    self.bgp_bRIBRIB_to_check,
                    self.bgp_bRIBRIB_received,
                    self.bgp_LabelVer_to_check,
                    self.bgp_LabelVer_received,
                    self.bgp_ImportVer_to_check,
                    self.bgp_ImportVer_received,
                    self.bgp_SendTblVer_to_check,
                    self.bgp_SendTblVer_received,
                    self.bgp_StandbyVer_to_check,
                    self.bgp_StandbyVer_received,
                    self.bgp_Neighbor_to_check,
                    self.bgp_Neighbor_received,
                    self.bgp_Spk_to_check,
                    self.bgp_Spk_received,
                    self.bgp_AS_to_check,
                    self.bgp_AS_received,
                    self.bgp_MsgRcvd_to_check,
                    self.bgp_MsgRcvd_received,
                    self.bgp_MsgSent_to_check,
                    self.bgp_MsgSent_received,
                    self.bgp_TblVer_to_check,
                    self.bgp_TblVer_received,
                    self.bgp_InQ_to_check,
                    self.bgp_InQ_received,
                    self.bgp_OutQ_to_check,
                    self.bgp_OutQ_received,
                    self.bgp_UpDown_to_check,
                    self.bgp_UpDown_received,
                    self.bgp_StPfxRcd_to_check,
                    self.bgp_StPfxRcd_received
                  ),
                  self.testcase_name,
                  "Failed",
                  "{}".format( self.command_issued_str ),
                  "{}".format( self.analysis_data_filename ),
                  str( self.line_number_head ),
                  str( self.line_number )
                )
                break
        else:
          continue
    if not self.found_bgp_flag:
      self.is_search_item.set_test_results_string( "Neighbor {} expect but not received".
                                                   format( self.bgp_Neighbor_to_check ),
                                                   self.testcase_name,
                                                   "Failed",
                                                   "{}".format( self.command_issued_str ),
                                                   "{}".format( self.analysis_data_filename ),
                                                   str( self.line_number_head ),
                                                   str( self.line_number ) )
    self.reportFD.seek( 0 )
    return( self.reportFD )
  #----------------------------------------------------------------------------------------------------------------
  def juniper_bgp_vrf_analysis( self, seed_logical_dict, reportFD ):
    self.reportFD = reportFD
    self.seed_logical_dict = seed_logical_dict
    #--------------------------------------------------------------------------------------------------------------
    return (self.reportFD)
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
# Show Interfaces Status
#------------------------------------------------------------------------------------------------------------------
class ShowInterfacesStatus:
  "Show Interface Status"
  # ----------------------------------------------------------------------------------------------------------------
  def __init__( self, parent = None ):
    self.name = "Show Interfaces Status"
    self.parent = parent
    self.filename_time_extension = parent.filename_time_extension
    self.process_reply = self.parent.process_reply
    self.cmd_list = self.parent.cmd_list
    self.is_search_item = self.parent.is_search_item
    self.testcase_name = self.parent.testcase_name
    self.analysis_data_filename = self.parent.analysis_data_filename
    self.seed_list = []
    self.command_issued = ""
    self.line_number = 0
    self.line_number_head = 0
  #----------------------------------------------------------------------------------------------------------------
  def execute( self, seed_logical_dict, reportFD ):
    self.reportFD = reportFD
    self.seed_logical_dict = dict( seed_logical_dict )
    #--------------------------------------------------------------------------------------------------------------
    if self.seed_logical_dict["device"] == "juniper":
      self.reportFD = self.juniper_interface( self.seed_logical_dict, self.reportFD )
    elif self.seed_logical_dict["device"] == "cisco":
      self.reportFD = self.cisco_interface( self.seed_logical_dict, self.reportFD )
    else:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    return ()
  #----------------------------------------------------------------------------------------------------------------
  def cisco_interface( self, seed_logical_dict, reportFD ):
    self.reportFD = reportFD
    self.seed_logical_dict = seed_logical_dict
    #-------------------------------------------------------------------------------------------------------------
    # FIXME UGLY!!! FIND A BETTER WAY THAN FLAGS !!!!!
    self.found_Interface_Title_flag = False
    self.found_Interface_flag = False
    try:
      self.command_issued_str = self.seed_logical_dict["show interfaces status"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.interface_to_check = self.seed_logical_dict["interface"]
      self.interface_to_check = self.interface_to_check.replace( "~", ":" )
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.name_to_check = self.seed_logical_dict["name"]
    except:
      pass
    try:
      self.status_to_check = self.seed_logical_dict["status"]
    except:
      pass
    try:
      self.vlan_to_check = self.seed_logical_dict["vlan"]
    except:
      pass
    try:
      self.duplex_to_check = self.seed_logical_dict["duplex"]
    except:
      pass
    try:
      self.speed_to_check = self.seed_logical_dict["speed"]
    except:
      pass
    try:
      self.type_to_check = self.seed_logical_dict["type"]
    except:
      pass
    #--------------------------------------------------------------------------------------------------------------
    for self.report_data in self.reportFD:
      self.line_number += 1
      if self.report_data.startswith( "\n" ):
        continue
      #------------------------------------------------------------------------------------------------------------
      # FIXME FIND A BTTER WAY THAN USING AN UGLY FLAG!!!!!!
      elif self.found_Interface_Title_flag:
        self.interface_received, \
        self.name_received, \
        self.status_received, \
        self.vlan_received, \
        self.duplex_received, \
        self.speed_received, \
        self.type_received = ShowInterfaceStatusStringParser().show_interface_status_string_parser( self.report_data )
        if self.interface_received.startswith(self.interface_to_check ):
          self.found_Interface_flag = True
          if self.status_received.startswith( self.status_to_check ) and \
             self.vlan_received.startswith( self.vlan_to_check ) and \
             self.duplex_received.startswith( self.duplex_to_check ) and \
             self.speed_received.startswith( self.speed_to_check ) and \
             self.type_received.startswith( self.type_to_check ):
            self.is_search_item.set_test_results_string( "Interface: {} Name:{} "
                                                         "Status:{} Detected:{} "
                                                         "VLAN: {} Detected: {} "
                                                         "Duplex: {} Dtected: {} "
                                                         "Speed: {} Detected: {} "
                                                         "Type:{} Detected:{}".
                                                         format( self.interface_received,
                                                                 self.name_received,
                                                                 self.status_to_check, self.status_received,
                                                                 self.vlan_to_check, self.vlan_received,
                                                                 self.duplex_to_check, self.duplex_received,
                                                                 self.speed_to_check, self.speed_received,
                                                                 self.type_to_check, self.type_received ),
                                                         self.testcase_name,
                                                         "Passed",
                                                         "{}".format( self.command_issued_str ),
                                                         "{}".format( self.analysis_data_filename ),
                                                         str( self.line_number_head ),
                                                         str( self.line_number ) )
            break
          else:
            self.is_search_item.set_test_results_string( "Interface: {} Name:{} "
                                                         "Status:{} Detected:{} "
                                                         "VLAN: {} Detected: {} "
                                                         "Duplex: {} Dtected: {} "
                                                         "Speed: {} Detected: {} "
                                                         "Type:{} Detected:{}".
                                                         format( self.interface_received,
                                                                 self.name_received,
                                                                 self.status_to_check, self.status_received,
                                                                 self.vlan_to_check, self.vlan_received,
                                                                 self.duplex_to_check, self.duplex_received,
                                                                 self.speed_to_check, self.speed_received,
                                                                 self.type_to_check, self.type_received ),
                                                         self.testcase_name,
                                                         "Failed",
                                                         "{}".format( self.command_issued_str ),
                                                         "{}".format( self.analysis_data_filename ),
                                                         str( self.line_number_head ),
                                                         str( self.line_number ) )
            break
        else:
          continue
      elif self.report_data.startswith( "Port           Name             Status       Vlan" ):
        self.found_Interface_Title_flag = True
        self.line_number_head = self.line_number
    if not self.found_Interface_flag:
      self.is_search_item.set_test_results_string( "Interface: {}".
                                                   format( self.interface_to_check ),
                                                   self.testcase_name,
                                                   "Failed",
                                                   "{} {}".format( self.interface_to_check,
                                                                   " NOT found on device" ),
                                                   "{}".format( self.analysis_data_filename ),
                                                   str( self.line_number_head ),
                                                   str( self.line_number ) )
    elif not self.found_Interface_Title_flag:
      raise NotAnError( "No interface data found" )
    self.reportFD.seek( 0 )
    return (self.reportFD)
  #----------------------------------------------------------------------------------------------------------------
  def juniper_interface( self, seed_logical_dict, reportFD ):
    self.reportFD = reportFD
    self.seed_logical_dict = seed_logical_dict
    #--------------------------------------------------------------------------------------------------------------
    return (self.reportFD)
    #--------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
# Show Ipv4 Interface Brief
#------------------------------------------------------------------------------------------------------------------
class ShowIpv4InterfaceBrief:
  "Show Ipv4 Interface Brief"
  # ----------------------------------------------------------------------------------------------------------------
  def __init__( self, parent = None ):
    self.name = "Show Ipv4 Interface Brief"
    self.parent = parent
    self.filename_time_extension = parent.filename_time_extension
    self.process_reply = self.parent.process_reply
    self.cmd_list = self.parent.cmd_list
    self.is_search_item = self.parent.is_search_item
    self.testcase_name = self.parent.testcase_name
    self.analysis_data_filename = self.parent.analysis_data_filename
    self.seed_list = []
    self.command_issued = ""
    self.line_number = 0
    self.line_number_head = 0
  # ----------------------------------------------------------------------------------------------------------------
  def execute( self, seed_logical_dict, reportFD ):
    self.reportFD = reportFD
    self.seed_logical_dict = dict( seed_logical_dict )
    #--------------------------------------------------------------------------------------------------------------
    if self.seed_logical_dict["device"] == "juniper":
      self.reportFD = self.juniper_interface( self.seed_logical_dict, self.reportFD )
    elif self.seed_logical_dict["device"] == "cisco":
      self.reportFD = self.cisco_interface( self.seed_logical_dict, self.reportFD )
    else:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    return ()
  #----------------------------------------------------------------------------------------------------------------
  def cisco_interface( self, seed_logical_dict, reportFD ):
    self.reportFD = reportFD
    self.seed_logical_dict = seed_logical_dict
    #-------------------------------------------------------------------------------------------------------------
    try:
      self.command_issued_str = self.seed_logical_dict["show ipv4 interface brief"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.interface_name_to_check = self.seed_logical_dict["interface name"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.ip_to_check = self.seed_logical_dict["ip"]
    except:
      self.ip_to_check = ""
    try:
      self.status_to_check = self.seed_logical_dict["status"]
    except:
      self.status_to_check = ""
    try:
      self.protocol_to_check = self.seed_logical_dict["protocol"]
    except:
      self.protocol_to_check = ""
    try:
      self.vrf_name_to_check = self.seed_logical_dict["vrf-name"]
    except:
      self.vrf_name_to_check = ""
    #--------------------------------------------------------------------------------------------------------------
    for self.report_data in self.reportFD:
      self.line_number += 1
      if self.report_data.startswith( "\n" ):
        continue
      #------------------------------------------------------------------------------------------------------------
      # FIXME FIND A BTTER WAY THAN USING AN UGLY FLAG!!!!!!
      if self.report_data.startswith(
          "Interface                      IP-Address      Status          Protocol Vrf-Name" ):
        for self.report_data in self.reportFD:
          self.line_number += 1
          if self.report_data.startswith( "\n" ):
            continue
          self.report_data_list = self.report_data.split()
          try:
            self.interface_name_received = self.report_data.split()[0]
          except:
            self.interface_name_received = ""
          try:
            self.ip_received = self.report_data.split()[1]
          except:
            self.ip_received = ""
          try:
            self.status_received = self.report_data.split()[2]
          except:
            self.status_received = ""
          try:
            self.protocol_received = self.report_data.split()[3]
          except:
            self.protocol_received = ""
          try:
            self.vrf_name_received = self.report_data.split()[4]
          except:
            self.vrf_name_received = ""
          if self.interface_name_received.startswith(self.interface_name_to_check ):
            if self.ip_received.startswith( self.ip_to_check ) and \
                self.status_received.startswith( self.status_to_check ) and \
                self.protocol_received.startswith( self.protocol_to_check ) and \
                self.vrf_name_received.startswith( self.vrf_name_to_check ):
              self.is_search_item.set_test_results_string( "Interface {} validated ".
                                                           format( self.interface_name_to_check ),
                                                           self.testcase_name,
                                                           "Passed",
                                                           "{}".format( self.command_issued_str ),
                                                           "{}".format( self.analysis_data_filename ),
                                                           str( self.line_number_head ),
                                                           str( self.line_number ) )
              self.reportFD.seek( 0 )
              return( self.reportFD )
            else:
              self.is_search_item.set_test_results_string( "Interface: {} "
                                                           "IP:{} Detected:{} "
                                                           "Status: {} Detected: {} "
                                                           "Protocol: {} Detected: {} "
                                                           "Vrf-Name:{} Detected:{}".
                                                           format( self.interface_name_to_check,
                                                                   self.interface_name_received,
                                                                   self.ip_to_check,
                                                                   self.ip_received,
                                                                   self.status_to_check,
                                                                   self.status_received,
                                                                   self.protocol_to_check,
                                                                   self.protocol_received,
                                                                   self.vrf_name_to_check,
                                                                   self.vrf_name_received ),
                                                           self.testcase_name,
                                                           "Failed",
                                                           "{}".format( self.command_issued_str ),
                                                           "{}".format( self.analysis_data_filename ),
                                                           str( self.line_number_head ),
                                                           str( self.line_number ) )
              self.reportFD.seek( 0 )
              return( self.reportFD )
      else:
        continue
    self.is_search_item.set_test_results_string( "Interface: {}".
                                                 format( self.interface_name_to_check ),
                                                 self.testcase_name,
                                                 "Failed",
                                                 "{}".format( self.command_issued_str ),
                                                 "{}".format( self.analysis_data_filename ),
                                                 str( self.line_number_head ),
                                                 str( self.line_number ) )
    self.reportFD.seek( 0 )
    return (self.reportFD)
  #----------------------------------------------------------------------------------------------------------------
  def juniper_interface( self, seed_logical_dict, reportFD ):
    self.reportFD = reportFD
    self.seed_logical_dict = seed_logical_dict
    #--------------------------------------------------------------------------------------------------------------
    return (self.reportFD)
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
# Show Interfaces Brief
#------------------------------------------------------------------------------------------------------------------
class ShowInterfacesBrief:
  "Show Interface Brief"
  # ----------------------------------------------------------------------------------------------------------------
  def __init__( self, parent = None ):
    self.name = "Show Interfaces Brief"
    self.parent = parent
    self.filename_time_extension = parent.filename_time_extension
    self.process_reply = self.parent.process_reply
    self.cmd_list = self.parent.cmd_list
    self.is_search_item = self.parent.is_search_item
    self.testcase_name = self.parent.testcase_name
    self.analysis_data_filename = self.parent.analysis_data_filename
    self.seed_list = []
    self.command_issued = ""
    self.line_number = 0
    self.line_number_head = 0
  # ----------------------------------------------------------------------------------------------------------------
  def execute( self, seed_logical_dict, reportFD ):
    self.reportFD = reportFD
    self.seed_logical_dict = dict( seed_logical_dict )
    #--------------------------------------------------------------------------------------------------------------
    if self.seed_logical_dict["device"] == "juniper":
      self.reportFD = self.juniper_interface( self.seed_logical_dict, self.reportFD )
    elif self.seed_logical_dict["device"] == "cisco":
      self.reportFD = self.cisco_interface( self.seed_logical_dict, self.reportFD )
    else:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    return ()
  #----------------------------------------------------------------------------------------------------------------
  def cisco_interface( self, seed_logical_dict, reportFD ):
    self.reportFD = reportFD
    self.seed_logical_dict = seed_logical_dict
    #-------------------------------------------------------------------------------------------------------------
    # FIXME UGLY!!! FIND A BETTER WAY THAN FLAGS !!!!!
    self.found_Interface_Title_flag = False
    self.found_Interface_flag = False
    try:
      self.command_issued_str = self.seed_logical_dict["show interfaces brief"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.interface_to_check = self.seed_logical_dict["interface"]
      self.interface_to_check = self.interface_to_check.replace( "~", ":" )
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.admin_status_to_check = self.seed_logical_dict["admin"]
    except:
      self.admin_status_to_check = ""
    try:
      self.link_status_to_check = self.seed_logical_dict["link"]
    except:
      self.link_status_to_check = ""
    try:
      self.encap_to_check = self.seed_logical_dict["encap"]
    except:
      self.encap_to_check = ""
    try:
      self.mtu_to_check = self.seed_logical_dict["mtu"]
    except:
      self.mtu_to_check = ""
    try:
      self.bandwidth_to_check = self.seed_logical_dict["bandwidth"]
    except:
      self.bandwidth_to_check = ""
    #--------------------------------------------------------------------------------------------------------------
    for self.report_data in self.reportFD:
      self.line_number += 1
      if self.report_data.startswith( "\n" ):
        continue
      #------------------------------------------------------------------------------------------------------------
      # FIXME FIND A BTTER WAY THAN USING AN UGLY FLAG!!!!!!
      elif self.found_Interface_Title_flag:
        self.report_data_list = self.report_data.split()
        try:
          self.interface_received = self.report_data.split()[0]
        except:
          self.interface_received = ""
        try:
          self.admin_status_received = self.report_data.split()[1]
        except:
          self.admin_status_received = ""
        try:
          self.link_status_received = self.report_data.split()[2]
        except:
          self.link_status_received = ""
        try:
          self.encap_received = self.report_data.split()[3]
        except:
          self.encap_received = ""
        try:
          self.mtu_received = self.report_data.split()[4]
        except:
          self.mtu_received = ""
        try:
          self.bandwidth_received = self.report_data.split()[5]
        except:
          self.bandwidth_received = ""
        if self.interface_received.startswith(self.interface_to_check ):
          self.found_Interface_flag = True
          if self.admin_status_received.startswith( self.admin_status_to_check ) and \
             self.link_status_received.startswith( self.link_status_to_check ) and \
             self.encap_received.startswith( self.encap_to_check ) and \
             self.mtu_received.startswith( self.mtu_to_check ) and \
             self.bandwidth_received.startswith( self.bandwidth_to_check ):
            self.is_search_item.set_test_results_string( "Interface: {} "
                                                         "Admin:{} Detected:{} "
                                                         "Link: {} Detected: {} "
                                                         "Encap: {} Detected: {} "
                                                         "MTU: {} Detected: {} "
                                                         "Bandwidth:{} Detected:{}".
                                                         format( self.interface_received,
                                                                 self.admin_status_to_check,
                                                                 self.admin_status_received,
                                                                 self.link_status_to_check,
                                                                 self.link_status_received,
                                                                 self.encap_to_check,
                                                                 self.encap_received,
                                                                 self.mtu_to_check,
                                                                 self.mtu_received,
                                                                 self.bandwidth_to_check,
                                                                 self.bandwidth_received ),
                                                         self.testcase_name,
                                                         "Passed",
                                                         "{}".format( self.command_issued_str ),
                                                         "{}".format( self.analysis_data_filename ),
                                                         str( self.line_number_head ),
                                                         str( self.line_number ) )
            break
          else:
            self.is_search_item.set_test_results_string( "Interface: {} "
                                                         "Admin:{} Detected:{} "
                                                         "Link: {} Detected: {} "
                                                         "Encap: {} Detected: {} "
                                                         "MTU: {} Detected: {} "
                                                         "Bandwidth:{} Detected:{}".
                                                         format( self.interface_received,
                                                                 self.admin_status_to_check,
                                                                 self.admin_status_received,
                                                                 self.link_status_to_check,
                                                                 self.link_status_received,
                                                                 self.encap_to_check,
                                                                 self.encap_received,
                                                                 self.mtu_to_check,
                                                                 self.mtu_received,
                                                                 self.bandwidth_to_check,
                                                                 self.bandwidth_received ),
                                                         self.testcase_name,
                                                         "Failed",
                                                         "{}".format( self.command_issued_str ),
                                                         "{}".format( self.analysis_data_filename ),
                                                         str( self.line_number_head ),
                                                         str( self.line_number ) )
            break
        else:
          continue
      elif self.report_data.startswith( "---------------------------------" ):
        self.found_Interface_Title_flag = True
        self.line_number_head = self.line_number
    if not self.found_Interface_flag:
      self.is_search_item.set_test_results_string( "Interface: {}".
                                                   format( self.interface_to_check ),
                                                   self.testcase_name,
                                                   "Failed",
                                                   "{} {}".format( self.interface_to_check,
                                                                   " NOT found on device" ),
                                                   "{}".format( self.analysis_data_filename ),
                                                   str( self.line_number_head ),
                                                   str( self.line_number ) )
    elif not self.found_Interface_Title_flag:
      raise NotAnError( "No interface data found" )
    self.reportFD.seek( 0 )
    return (self.reportFD)
  #----------------------------------------------------------------------------------------------------------------
  def juniper_interface( self, seed_logical_dict, reportFD ):
    self.reportFD = reportFD
    self.seed_logical_dict = seed_logical_dict
    #--------------------------------------------------------------------------------------------------------------
    return (self.reportFD)
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
# Show Interface Terse
#------------------------------------------------------------------------------------------------------------------
class ShowInterfacesTerse:
  "Show Interfaces Terse"
  #----------------------------------------------------------------------------------------------------------------
  def __init__( self, parent = None ):
    self.name = "Show Interface Terse"
    self.parent = parent
    self.filename_time_extension = parent.filename_time_extension
    self.process_reply = self.parent.process_reply
    self.cmd_list = self.parent.cmd_list
    self.is_search_item = self.parent.is_search_item
    self.testcase_name = self.parent.testcase_name
    self.analysis_data_filename = self.parent.analysis_data_filename
    self.seed_list = []
    self.command_issued = ""
    self.line_number = 0
    self.line_number_head = 0
  #----------------------------------------------------------------------------------------------------------------
  def execute( self, seed_logical_dict, reportFD ):
    self.reportFD = reportFD
    self.seed_logical_dict = dict( seed_logical_dict )
    #--------------------------------------------------------------------------------------------------------------
    if self.seed_logical_dict["device"] == "juniper":
      self.reportFD = self.juniper_interface( self.seed_logical_dict, self.reportFD )
    elif self.seed_logical_dict["device"] == "cisco":
      self.reportFD = self.cisco_interface( self.seed_logical_dict, self.reportFD )
    else:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    return ()
  #----------------------------------------------------------------------------------------------------------------
  def cisco_interface( self, seed_logical_dict, reportFD ):
    self.reportFD = reportFD
    self.seed_logical_dict = seed_logical_dict
    #--------------------------------------------------------------------------------------------------------------
    return (self.reportFD)
  #----------------------------------------------------------------------------------------------------------------
  def juniper_interface( self, seed_logical_dict, reportFD ):
    self.reportFD = reportFD
    self.seed_logical_dict = seed_logical_dict
    #-------------------------------------------------------------------------------------------------------------
    # FIXME UGLY!!! FIND A BETTER WAY THAN FLAGS !!!!!
    self.found_Interface_Title_flag = False
    self.found_Interface_flag = False
    #-----------------------------------------------------------------------------------------------------------
    try:
      self.command_issued_str = self.seed_logical_dict["show interfaces terse"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.interface_to_check = self.seed_logical_dict["interface"]
      self.interface_to_check = self.interface_to_check.replace( "~", ":" )
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.admin_status_to_check = self.seed_logical_dict["admin"]
    except:
      self.admin_status_to_check = ""
    try:
      self.link_status_to_check = self.seed_logical_dict["link"]
    except:
      self.link_status_to_check = ""
    try:
      self.proto_to_check = self.seed_logical_dict["proto"]
    except:
      self.proto_to_check = ""
    try:
      self.address_to_check = self.seed_logical_dict["address"]
      self.address_to_check = self.address_to_check.replace( "~", ":" )
    except:
      self.address_to_check = ""
    #-------------------------------------------------------------------------------------------------------------
    self.prepare_analysis_flag = False
    for self.terse_data in self.reportFD:
      self.line_number += 1
      if self.prepare_analysis_flag and \
              self.terse_data.startswith( "Interface               Admin Link Proto    Local" ):
        self.analyze_interfaces_terse_data( self.reportFD )
        break
      elif self.terse_data.startswith( "DUT(" ) and \
              self.terse_data.find( ")-> show interfaces terse | no-more" ) != -1:
        self.prepare_analysis_flag = True
        continue
      else:
        continue
    self.reportFD.seek( 0 )
    return (self.reportFD)
  #-------------------------------------------------------------------------------------------------------------
  def analyze_interfaces_terse_data( self, reportFD ):
    self.line_number_head = self.line_number
    for self.terse_data in reportFD:
      self.line_number += 1
      self.terse_data_list = self.terse_data.split()
      try:
        self.interface_received = self.terse_data_list[0]
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
          self.address_received = self.terse_data_list[4]
        except:
          self.address_received = ""
      except:
        self.proto_received = ""
        self.address_received = ""
      #-------------------------------------------------------------------------------------------------------------
      if self.interface_received == self.interface_to_check and self.proto_to_check == "":
        #-----------------------------------------------------------------------------------------------------------
        # Land here if the interface is found and there is no protocol filed to check aka or address files
        #-----------------------------------------------------------------------------------------------------------
        if self.admin_received == self.admin_status_to_check and \
                self.link_received == self.link_status_to_check:
          self.is_search_item.set_test_results_string( "Interface:{} Detected:{} "
                                                       "Admin:{} Detected:{} "
                                                       "Link:{} Detected:{} "
                                                       "Protocol:{} Detected:{} "
                                                       "IP:{} Detected:{}".
                                                       format( self.interface_to_check,
                                                               self.interface_received,
                                                               self.admin_status_to_check,
                                                               self.admin_received,
                                                               self.link_status_to_check,
                                                               self.link_received,
                                                               self.proto_to_check,
                                                               self.proto_received,
                                                               self.address_to_check,
                                                               self.address_received ),
                                                       self.testcase_name,
                                                       "Passed",
                                                       "{}".format( self.command_issued_str ),
                                                       "{}".format( self.analysis_data_filename ),
                                                       str( self.line_number_head ),
                                                       str( self.line_number ) )
          break
        else:
          #-----------------------------------------------------------------------------------------------------------
          # Land here if the interface is found and matches but not any of the other fields
          #-----------------------------------------------------------------------------------------------------------
          self.is_search_item.set_test_results_string( "Interface:{} Detected:{} "
                                                       "Admin:{} Detected:{} "
                                                       "Link:{} Detected:{} "
                                                       "Protocol:{} Detected:{} "
                                                       "IP:{} Detected:{}".
                                                       format( self.interface_to_check,
                                                               self.interface_received,
                                                               self.admin_status_to_check,
                                                               self.admin_received,
                                                               self.link_status_to_check,
                                                               self.link_received,
                                                               self.proto_to_check,
                                                               self.proto_received,
                                                               self.address_to_check,
                                                               self.address_received ),
                                                       self.testcase_name,
                                                       "Failed",
                                                       "{}".format( self.command_issued_str ),
                                                       "{}".format( self.analysis_data_filename ),
                                                       str( self.line_number_head ),
                                                       str( self.line_number ) )
          break
      #-------------------------------------------------------------------------------------------------------------
      elif self.interface_received == self.interface_to_check and \
           self.proto_to_check != "" and self.address_to_check == "":
        #-----------------------------------------------------------------------------------------------------------
        # Land here if the interface is found and there is no protocol filed to check aka or address files
        #-----------------------------------------------------------------------------------------------------------
        if self.admin_received == self.admin_status_to_check and \
           self.link_received == self.link_status_to_check and \
           self.proto_received == self.proto_to_check:
          self.is_search_item.set_test_results_string( "Interface:{} Detected:{} "
                                                       "Admin:{} Detected:{} "
                                                       "Link:{} Detected:{} "
                                                       "Protocol:{} Detected:{} "
                                                       "IP:{} Detected:{}".
                                                       format( self.interface_to_check,
                                                               self.interface_received,
                                                               self.admin_status_to_check,
                                                               self.admin_received,
                                                               self.link_status_to_check,
                                                               self.link_received,
                                                               self.proto_to_check,
                                                               self.proto_received,
                                                               self.address_to_check,
                                                               self.address_received ),
                                                       self.testcase_name,
                                                       "Passed",
                                                       "{}".format( self.command_issued_str ),
                                                       "{}".format( self.analysis_data_filename ),
                                                       str( self.line_number_head ),
                                                       str( self.line_number ) )
          break
        else :
          # -----------------------------------------------------------------------------------------------------------
          # Land here if the interface is found and matches but not any of the other fields
          # -----------------------------------------------------------------------------------------------------------
          self.is_search_item.set_test_results_string( "Interface:{} Detected:{} "
                                                       "Admin:{} Detected:{} "
                                                       "Link:{} Detected:{} "
                                                       "Protocol:{} Detected:{} "
                                                       "IP:{} Detected:{}".
                                                       format( self.interface_to_check,
                                                               self.interface_received,
                                                               self.admin_status_to_check,
                                                               self.admin_received,
                                                               self.link_status_to_check,
                                                               self.link_received,
                                                               self.proto_to_check,
                                                               self.proto_received,
                                                               self.address_to_check,
                                                               self.address_received ),
                                                       self.testcase_name,
                                                       "Failed",
                                                       "{}".format( self.command_issued_str ),
                                                       "{}".format( self.analysis_data_filename ),
                                                       str( self.line_number_head ),
                                                       str( self.line_number ) )
          break
      elif self.interface_received == self.interface_to_check and \
           self.proto_to_check != "" and self.address_to_check != "":
        #-----------------------------------------------------------------------------------------------------------
        # Land here if the interface is found and all fields matches
        #-----------------------------------------------------------------------------------------------------------
        if self.admin_received == self.admin_status_to_check and \
           self.link_received == self.link_status_to_check and \
           self.proto_received == self.proto_to_check and \
          self.address_received == self.address_to_check:
          self.is_search_item.set_test_results_string( "Interface:{} Detected:{} "
                                                       "Admin:{} Detected:{} "
                                                       "Link:{} Detected:{} "
                                                       "Protocol:{} Detected:{} "
                                                       "IP:{} Detected:{}".
                                                       format( self.interface_to_check,
                                                               self.interface_received,
                                                               self.admin_status_to_check,
                                                               self.admin_received,
                                                               self.link_status_to_check,
                                                               self.link_received,
                                                               self.proto_to_check,
                                                               self.proto_received,
                                                               self.address_to_check,
                                                               self.address_received ),
                                                       self.testcase_name,
                                                       "Passed",
                                                       "{}".format( self.command_issued_str ),
                                                       "{}".format( self.analysis_data_filename ),
                                                       str( self.line_number_head ),
                                                       str( self.line_number ) )
          break
        else:
          #-----------------------------------------------------------------------------------------------------------
          # Land here if the interface is found and matches but not any of the other fields
          #-----------------------------------------------------------------------------------------------------------
          self.is_search_item.set_test_results_string( "Interface:{} Detected:{} "
                                                       "Admin:{} Detected:{} "
                                                       "Link:{} Detected:{} "
                                                       "Protocol:{} Detected:{} "
                                                       "IP:{} Detected:{}".
                                                       format( self.interface_to_check,
                                                               self.interface_received,
                                                               self.admin_status_to_check,
                                                               self.admin_received,
                                                               self.link_status_to_check,
                                                               self.link_received,
                                                               self.proto_to_check,
                                                               self.proto_received,
                                                               self.address_to_check,
                                                               self.address_received ),
                                                       self.testcase_name,
                                                       "Failed",
                                                       "{}".format( self.command_issued_str ),
                                                       "{}".format( self.analysis_data_filename ),
                                                       str( self.line_number_head ),
                                                       str( self.line_number ) )
          break
      else:
        continue
    else:
      #-----------------------------------------------------------------------------------------------------------
      # Land here if the interface is not found or does not match
      #-----------------------------------------------------------------------------------------------------------
      self.is_search_item.set_test_results_string( "Interface NOT FOUND:{} ".format( self.interface_to_check ),
                                                   self.testcase_name,
                                                   "Failed",
                                                   "{}".format( self.command_issued_str ),
                                                   "{}".format( self.analysis_data_filename ),
                                                   str( self.line_number_head ),
                                                   str( self.line_number ) )
    return()

#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
# Ping
#------------------------------------------------------------------------------------------------------------------
class Ping:
  "Ping"
  #----------------------------------------------------------------------------------------------------------------
  def __init__( self, parent = None ):
    self.name = "Ping"
    self.parent = parent
    self.filename_time_extension = parent.filename_time_extension
    self.process_reply = self.parent.process_reply
    self.cmd_list = self.parent.cmd_list
    self.is_search_item = self.parent.is_search_item
    self.is_search_item_index = self.parent.is_search_item_index
    self.testcase_name = self.parent.testcase_name
    self.analysis_data_filename = self.parent.analysis_data_filename
    self.seed_list = []
    self.command_issued = ""
    self.line_number = 0
    self.line_number_head = 0
  #----------------------------------------------------------------------------------------------------------------
  def execute( self, seed_logical_dict, reportFD ):
    self.reportFD = reportFD
    self.seed_logical_dict = dict( seed_logical_dict )
    #--------------------------------------------------------------------------------------------------------------
    if self.seed_logical_dict["device"] == "juniper":
      self.reportFD = self.juniper_interface( self.seed_logical_dict, self.reportFD )
    elif self.seed_logical_dict["device"] == "cisco":
      self.reportFD = self.cisco_interface( self.seed_logical_dict, self.reportFD )
    else:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    return ()
  #----------------------------------------------------------------------------------------------------------------
  def cisco_interface( self, seed_logical_dict, reportFD ):
    self.reportFD = reportFD
    self.seed_logical_dict = seed_logical_dict
    #--------------------------------------------------------------------------------------------------------------
    try:
      self.command_issued_str = self.seed_logical_dict["ping"]
      self.command_issued_str_list = self.command_issued_str.split()
      if self.command_issued_str_list[1][0].isdigit():
        self.pinged_ip = self.command_issued_str_list[1]
      else:
        self.pinged_ip = self.command_issued_str_list[3]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.success_rate_to_check = self.seed_logical_dict["successrate"]
    except:
      self.success_rate_to_check = "100"
    try:
      self.round_trip_min_to_check = self.seed_logical_dict["rtmin"]
    except:
      self.round_trip_min_to_check = ""
    try:
      self.round_trip_avg_to_check = self.seed_logical_dict["rtavg"]
    except:
      self.round_trip_avg_to_check = ""
    try:
      self.round_trip_max_to_check = self.seed_logical_dict["rtmax"]
    except:
      self.round_trip_max_to_check = ""
    #-------------------------------------------------------------------------------------------------------------
    self.prepare_analysis_flag = False
    self.ping_found_flag = False
    for self.ping_data in self.reportFD:
      self.line_number += 1
      if self.ping_data.find( self.command_issued_str ) != -1:
        for self.ping_data in self.reportFD:
          self.line_number += 1
          if self.ping_data.startswith( "DUT(" ):
            self.reportFD.seek( 0, 2 )
            break
          if self.ping_data.startswith( "Success rate is" ):
            self.analyze_ping_data( self.ping_data )
            self.ping_found_flag = True
            self.reportFD.seek( 0, 2 )
            break
          ## FIXME REMOVE THIS elif self.ping_data.startswith( "DUT(" ) and \
          ## FIXME REMOVE THIS         self.ping_data.find( ")-> ping" ) != -1:
          ## FIXME REMOVE THIS   self.line_number_head = self.line_number
          ## FIXME REMOVE THIS   self.prepare_analysis_flag = True
          ## FIXME REMOVE THIS   continue
      else:
        continue
    if not self.ping_found_flag:
      self.is_search_item.set_test_results_string( "{}".format( self.command_issued_str  ),
                                                   self.testcase_name,
                                                   "Failed",
                                                   "{}".format( self.command_issued_str ),
                                                   "{}".format( self.analysis_data_filename ),
                                                   str( self.line_number_head ),
                                                   str( self.line_number ) )
    self.reportFD.seek( 0 )
    return (self.reportFD)
  #----------------------------------------------------------------------------------------------------------------
  def juniper_interface( self, seed_logical_dict, reportFD ):
    self.reportFD = reportFD
    self.seed_logical_dict = seed_logical_dict
    #-------------------------------------------------------------------------------------------------------------
    return (self.reportFD)
  #-------------------------------------------------------------------------------------------------------------
  def analyze_ping_data( self, ping_data ):
    self.ping_data_list = ping_data.split()
    try:
      self.success_rate_received = self.ping_data_list[3]
    except:
      self.success_rate_received = ""
    try:
      self.round_trip_min_received = self.ping_data_list[9].split( "/" )[0]
    except:
      self.round_trip_min_received = ""
    try:
      self.round_trip_avg_received = self.ping_data_list[9].split( "/" )[1]
    except:
      self.round_trip_avg_received = ""
    try:
      self.round_trip_max_received = self.ping_data_list[9].split( "/" )[2]
    except:
      self.round_trip_max_received = ""
    #-------------------------------------------------------------------------------------------------------------
    if self.success_rate_received == self.success_rate_to_check:
      # FIXME MAYBE DELETE ? self.is_search_item.set_test_results_string( "{}. Ping:{} Detected:{} ".
      # FIXME MAYBE DELETE ?                                              format( str( self.is_search_item_index ),
      # FIXME MAYBE DELETE ?                                                      self.success_rate_to_check,
      # FIXME MAYBE DELETE ?                                                      self.success_rate_received ),
      self.is_search_item.set_test_results_string( "Ping to {} validated".format( self.pinged_ip ),
                                                   self.testcase_name,
                                                   "Passed",
                                                   "{}".format( self.command_issued_str ),
                                                   "{}".format( self.analysis_data_filename ),
                                                   str( self.line_number_head ),
                                                   str( self.line_number ) )
    else:
      self.is_search_item.set_test_results_string( "{}. Ping:{} Detected:{} ".
                                                   format( str( self.is_search_item_index ),
                                                           self.success_rate_to_check,
                                                           self.success_rate_received ),
                                                   self.testcase_name,
                                                   "Failed",
                                                   "{}".format( self.command_issued_str ),
                                                   "{}".format( self.analysis_data_filename ),
                                                   str( self.line_number_head ),
                                                   str( self.line_number ) )
    return ()
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
# Show Interface Detail
#------------------------------------------------------------------------------------------------------------------
class ShowInterfacesDetail:
  "Show Interfaces Datail"
  #----------------------------------------------------------------------------------------------------------------
  def __init__( self, parent = None ):
    self.name = "Show Interface Detail"
    self.parent = parent
    self.filename_time_extension = parent.filename_time_extension
    self.process_reply = self.parent.process_reply
    self.cmd_list = self.parent.cmd_list
    self.is_search_item = self.parent.is_search_item
    self.testcase_name = self.parent.testcase_name
    self.analysis_data_filename = self.parent.analysis_data_filename
    self.seed_list = self.parent.seed_list
    self.command_issued = ""
    self.character_count = 0
    self.line_number = 0
    self.line_number_head = 0
    self.start_analysis_flag = False
    self.days_of_the_week_skip = "Sun Mon Tue Wed Thu Fri Sat"
    self.interface_to_check = ""
    self.interface_admin_state_to_check = ""
    self.interface_line_protocol_state_to_check = ""
    self.state_transitions_to_check = ""
    self.hardware_to_check = ""
    self.hardware_address_to_check = ""
    self.hardware_address_bia_to_check = ""
    self.layer_to_check = ""
    self.description_to_check = ""
    self.internet_address_to_check = ""
    self.mtu_to_check = ""
    self.bandwidth_to_check = ""
    self.reliability_to_check = ""
    self.transmit_load_to_check = ""
    self.receive_load_to_check = ""
    self.encaps_to_check = ""
    self.duplex_to_check = ""
    self.bit_per_sec_to_check = ""
    self.link_type_to_check = ""
    self.output_flow_control_to_check = 0
    self.input_flow_control_to_check = 0
    self.carrier_delay_state_to_check = 0
    self.loopback_state_to_check = 0
    self.flapped_to_check = ""
    self.arp_type_to_check = ""
    self.arp_timeout_to_check = ""
    self.number_of_bundled_interfaces_to_check = 0
    self.bundled_interfaces_to_check = []
    self.input_output_data_rate_to_check = ""
    self.last_input_time_to_check = ""
    self.last_output_time_to_check = ""
    self.last_clear_to_check = ""
    self.input_rate_to_check = 0
    self.input_packet_rate_to_check = 0
    self.output_rate_to_check = 0
    self.output_packet_rate_to_check = 0
    self.input_packets_to_check = 0
    self.input_bytes_to_check = 0
    self.input_drops_to_check = 0
    self.up_level_protocol_drops_to_check = 0
    self.input_broadcast_packets_to_check = 0
    self.input_multicast_packets_to_check = 0
    self.input_errors_to_check = 0
    self.input_crc_to_check = 0
    self.input_frame_to_check = 0
    self.input_overrun_to_check = 0
    self.input_ignore_to_check = 0
    self.input_abort_to_check = 0
    self.output_packets_to_check = 0
    self.output_bytes_to_check = 0
    self.output_drops_to_check = 0
    self.output_broadcast_packets_to_check = 0
    self.output_multicast_packets_to_check = 0
    self.output_errors_to_check = 0
    self.output_underruns_to_check = 0
    self.output_applique_to_check = 0
    self.output_resets_to_check = 0
    self.output_buffer_failures_to_check = 0
    self.output_buffer_swapouts_to_check = 0
    self.carrier_transitions_to_check = 0
    self.testcase = {
      "testcase": "",
      "testcasetitle": "",
      "descriptiondata": "",
      "configurationtitle": "",
      "configurationdata": "",
      "proceduretitle": "",
      "proceduredata": "",
      "criteriadata": "",
      "resultsdata": "",
      "statusdata": "",
      "analysisdata":[],
      "detailedresultsdata": ""
    }
  #----------------------------------------------------------------------------------------------------------------
  def execute( self, seed_logical_dict, reportFD ):
    self.reportFD = reportFD
    self.seed_logical_dict = dict( seed_logical_dict )
    # --------------------------------------------------------------------------------------------------------------
    if self.seed_logical_dict["device"] == "juniper":
      self.reportFD = self.juniper_interface( self.seed_logical_dict, self.reportFD )
    elif self.seed_logical_dict["device"] == "cisco":
      self.reportFD = self.cisco_interface( self.seed_logical_dict, self.reportFD )
    else:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    return ()
  #----------------------------------------------------------------------------------------------------------------
  def cisco_interface( self, seed_logical_dict, reportFD ):
    self.reportFD = reportFD
    self.seed_logical_dict = seed_logical_dict
    #--------------------------------------------------------------------------------------------------------------
    #-------------------------------------------------------------------------------------------------------------
    # FIXME UGLY!!! FIND A BETTER WAY THAN FLAGS !!!!!
    self.found_Interface_flag = False
    #-----------------------------------------------------------------------------------------------------------
    try:
      self.command_issued_str = self.seed_logical_dict["show interfaces detail"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.interface_to_check = self.seed_logical_dict["interface"]
      self.interface_to_check = self.interface_to_check.replace( "~", ":" )
      self.interface_admin_state_to_check = self.seed_logical_dict["admin state"]
      self.interface_line_protocol_state_to_check = self.seed_logical_dict["line protocol"]
    except:
      pass
    try:
      self.state_transitions_to_check = self.seed_logical_dict["state transitions"]
    except:
      pass
    try:
      self.hardware_to_check = self.seed_logical_dict["hardware"]
    except:
      pass
    try:
      self.hardware_address_to_check = self.seed_logical_dict["hardware address"]
    except:
      pass
    try:
      self.hardware_address_bia_to_check = self.seed_logical_dict["hardware address bia"]
    except:
      pass
    try:
      self.layer_to_check = self.seed_logical_dict["layer"]
    except:
      pass
    try:
      self.description_to_check = self.seed_logical_dict["description"]
      self.description_to_check = self.description_to_check.replace( "~", ":" )
    except:
      pass
    try:
      self.internet_address_to_check = self.seed_logical_dict["internet address"]
    except:
      pass
    try:
      self.mtu_to_check = self.seed_logical_dict["mtu"]
    except:
      pass
    try:
      self.bandwidth_to_check = self.seed_logical_dict["bandwidth"]
    except:
      pass
    try:
      self.reliability_to_check = self.seed_logical_dict["reliability"]
    except:
      pass
    try:
      self.transmit_load_to_check = self.seed_logical_dict["transmit load"]
    except:
      pass
    try:
      self.receive_load_to_check = self.seed_logical_dict["receive load"]
    except:
      pass
    try:
      self.encaps_to_check = self.seed_logical_dict["encaps"]
    except:
      pass
    try:
      self.duplex_to_check = self.seed_logical_dict["duplex"]
    except:
      pass
    try:
      self.bit_per_sec_to_check = self.seed_logical_dict["bit per sec"]
    except:
      pass
    try:
      self.link_type_to_check = self.seed_logical_dict["link type"]
    except:
      pass
    try:
      self.output_flow_control_to_check = self.seed_logical_dict["output flow control"]
    except:
      pass
    try:
      self.input_flow_control_to_check = self.seed_logical_dict["input flow control"]
    except:
      pass
    try:
      self.carrier_delay_state_to_check = self.seed_logical_dict["carrier delay state"]
    except:
      pass
    try:
      self.loopback_state_to_check = self.seed_logical_dict["loopback state"]
    except:
      pass
    try:
      self.flapped_to_check = self.seed_logical_dict["flapped"]
    except:
      pass
    try:
      self.arp_type_to_check = self.seed_logical_dict["arp type"]
    except:
      pass
    try:
      self.arp_timeout_to_check = self.seed_logical_dict["arp timeout"]
      self.arp_timeout_to_check = self.arp_timeout_to_check.replace( "~", ":" )
    except:
      pass
    try:
      self.number_of_bundled_interfaces_to_check = self.seed_logical_dict["number of bundled interfaces"]
    except:
      self.number_of_bundled_interfaces_to_check = "0"
    try:
      for self.bintfindex in range( int( self.number_of_bundled_interfaces_to_check ) ):
        self.bundled_interfaces_to_check.append(
             dict( self.seed_logical_dict["bundle {}".format( self.bintfindex + 1 )] ) )
    except:
      pass
    try:
      self.input_output_data_rate_to_check = self.seed_logical_dict["input output data rate"]
    except:
      pass
    try:
      self.last_input_time_to_check = self.seed_logical_dict["last input time"]
      self.last_input_time_to_check = self.last_input_time_to_check.replace( "~", ":" )
    except:
      pass
    try:
      self.last_output_time_to_check = self.seed_logical_dict["last output time"]
      self.last_output_time_to_check = self.last_output_time_to_check.replace( "~", ":" )
    except:
      pass
    try:
      self.last_clear_to_check = self.seed_logical_dict["last clear"]
      self.last_clear_to_check = self.last_clear_to_check.replace( "~", ":" )
    except:
      pass
    try:
      self.input_rate_to_check = int( self.seed_logical_dict["input rate"] )
    except:
      self.input_rate_to_check = 0
    try:
      self.input_packet_rate_to_check = int( self.seed_logical_dict["input packet rate"] )
    except:
      pass
    try:
      self.output_rate_to_check = int( self.seed_logical_dict["output rate"] )
    except:
      self.output_rate_to_check = 0
    try:
      self.output_packet_rate_to_check = int( self.seed_logical_dict["output packet rate"] )
    except:
      self.output_packet_rate_to_check = 0
    try:
      self.input_packets_to_check = int( self.seed_logical_dict["input packets"] )
    except:
      self.input_packets_to_check = 0
    try:
      self.input_bytes_to_check = int( self.seed_logical_dict["input bytes"] )
    except:
      self.input_bytes_to_check = 0
    try:
      self.input_drops_to_check = int( self.seed_logical_dict["input drops"] )
    except:
      self.input_drops_to_check = 0
    try:
      self.up_level_protocol_drops_to_check = int( self.seed_logical_dict["up level protocol drops"] )
    except:
      self.up_level_protocol_drops_to_check = 0
    try:
      self.input_broadcast_packets_to_check = int( self.seed_logical_dict["input broadcast packets"] )
    except:
      self.input_broadcast_packets_to_check = 0
    try:
      self.input_multicast_packets_to_check = int( self.seed_logical_dict["input multicast packets"] )
    except:
      self.input_multicast_packets_to_check = 0
    try:
      self.input_errors_to_check = int( self.seed_logical_dict["input errors"] )
    except:
      self.input_errors_to_check = 0
    try:
      self.input_crc_to_check = int( self.seed_logical_dict["input crc"] )
    except:
      self.input_crc_to_check = 0
    try:
      self.input_frame_to_check = int( self.seed_logical_dict["input frame"] )
    except:
      self.input_frame_to_check = 0
    try:
      self.input_overrun_to_check = int( self.seed_logical_dict["input overrun"] )
    except:
      self.input_overrun_to_check = 0
    try:
      self.input_ignore_to_check = int( self.seed_logical_dict["input ignore"] )
    except:
      self.input_ignore_to_check = 0
    try:
      self.input_abort_to_check = int( self.seed_logical_dict["input abort"] )
    except:
      self.input_abort_to_check = 0
    try:
      self.output_packets_to_check = int( self.seed_logical_dict["output packets"] )
    except:
      self.output_packets_to_check = 0
    try:
      self.output_bytes_to_check = int( self.seed_logical_dict["output bytes"] )
    except:
      self.output_bytes_to_check = 0
    try:
      self.output_drops_to_check = int( self.seed_logical_dict["output drops"] )
    except:
      self.output_drops_to_check = 0
    try:
      self.output_broadcast_packets_to_check = int( self.seed_logical_dict["output broadcast packets"] )
    except:
      self.output_broadcast_packets_to_check = 0
    try:
      self.output_multicast_packets_to_check = int( self.seed_logical_dict["output multicast packets"] )
    except:
      self.output_multicast_packets_to_check = 0
    try:
      self.output_errors_to_check = int( self.seed_logical_dict["output errors"] )
    except:
      self.output_errors_to_check = 0
    try:
      self.output_underruns_to_check = int( self.seed_logical_dict["output underruns"] )
    except:
      self.output_underruns_to_check = 0
    try:
      self.output_applique_to_check = int( self.seed_logical_dict["output applique"] )
    except:
      self.output_applique_to_check = 0
    try:
      self.output_resets_to_check = int( self.seed_logical_dict["output resets"] )
    except:
      self.output_resets_to_check = 0
    try:
      self.output_buffer_failures_to_check = int( self.seed_logical_dict["output buffer failures"] )
    except:
      self.output_buffer_failures_to_check = 0
    try:
      self.output_buffer_swapouts_to_check = int( self.seed_logical_dict["output buffer swapouts"] )
    except:
      self.output_buffer_swapouts_to_check = 0
    try:
      self.carrier_transitions_to_check = int( self.seed_logical_dict["carrier transitions"] )
    except:
      self.carrier_transitions_to_check = 0
    """
    Handle both show types, all interfaces or single
    """
    self.single_interface_command = "show interfaces {} detail".format( self.interface_to_check )
    """"""
    self.start_processing_details_flag = False
    for self.detail_data in self.reportFD:
      self.line_number += 1
      if not self.detail_data.startswith( "DUT(" ) and \
              self.detail_data.find( ")-> show interfaces detail" ) == -1 or \
              self.detail_data.find( self.single_interface_command ) == -1:
        self.start_processing_details_flag = True
        self.found_Interface_flag = False
        self.character_count += len( self.detail_data )
        continue
      # -----------------------------------------------------------------------------------------------------------
      # FIXME YET ANOTHER OOP CANIDATE !!!
      # -----------------------------------------------------------------------------------------------------------
      if self.start_processing_details_flag:
        for self.detail_data_str in self.reportFD:
          self.line_number += 1
          if self.detail_data_str.startswith( "\n" ):
            continue
          try:
            self.detail_data_list = self.detail_data_str.split()
            self.detail_data = " ".join( self.detail_data_list )
          except:
            continue
          if self.detail_data.find( ", line protocol is " ) != -1:
              self.interface_received = self.detail_data_list[0]
              self.interface_admin_state_received = self.detail_data_list[2].split( "," )[0]
              self.interface_line_protocol_state_received = self.detail_data_list[6]
              self.found_Interface_flag = True
          if self.found_Interface_flag == True:
            if self.interface_to_check == self.interface_received:
              self.state_transitions_received = ""
              self.hardware_received = ""
              self.hardware_address_received = ""
              self.hardware_address_bia_received = ""
              self.layer_received = ""
              self.description_received = ""
              self.internet_address_received = ""
              self.mtu_received = ""
              self.bandwidth_received = ""
              self.reliability_received = ""
              self.transmit_load_received = ""
              self.receive_load_received = ""
              self.encaps_received = ""
              self.duplex_received = ""
              self.bit_per_sec_received = ""
              self.link_type_received = ""
              self.output_flow_control_received = ""
              self.input_flow_control_received = ""
              self.carrier_delay_state_received = ""
              self.loopback_state_received = ""
              self.flapped_received = ""
              self.arp_type_received = ""
              self.arp_timeout_received = ""
              self.number_of_bundled_interfaces_received = 0
              self.bundled_interfaces_received = []
              self.input_output_data_rate_received = ""
              self.last_input_time_received = ""
              self.last_output_time_received = ""
              self.last_clear_received = ""
              self.input_rate_received = 0
              self.input_packet_rate_received = 0
              self.output_rate_received = 0
              self.output_packet_rate_received = 0
              self.input_packets_received = 0
              self.input_bytes_received = 0
              self.input_drops_received = 0
              self.up_level_protocol_drops_received = 0
              self.input_broadcast_packets_received = 0
              self.input_multicast_packets_received = 0
              self.input_errors_received = 0
              self.input_crc_received = 0
              self.input_frame_received = 0
              self.input_overrun_received = 0
              self.input_ignore_received = 0
              self.input_abort_received = 0
              self.output_packets_received = 0
              self.output_bytes_received = 0
              self.output_drops_received = 0
              self.output_broadcast_packets_received = 0
              self.output_multicast_packets_received = 0
              self.output_errors_received = 0
              self.output_underruns_received = 0
              self.output_applique_received = 0
              self.output_resets_received = 0
              self.output_buffer_failures_received = 0
              self.output_buffer_swapouts_received = 0
              self.carrier_transitions_received = 0
              for self.detail_data_str in self.reportFD:
                self.line_number += 1
                if self.detail_data_str.startswith( "\n" ):
                  break
                try:
                  self.detail_data_list = self.detail_data_str.split()
                  self.detail_data = " ".join( self.detail_data_list )
                except:
                  continue
                try:
                  if self.detail_data.startswith( "Interface state transitions:" ):
                    self.state_transitions_received = self.detail_data_list[3]
                    continue
                  if self.detail_data.startswith( "Hardware is" ):
                    try:
                      self.hardware_received = " ".join( self.detail_data.split( "is" )[1].split( "," )[0].split() )
                    except:
                      pass
                    try:
                      if self.detail_data.split( "," )[1].startswith( " address" ):
                        self.addr = self.detail_data.split( "," )[1].split( "is" )[1].split()
                        self.hardware_address_received = self.addr[0]
                        try:
                          self.hardware_address_bia_received = self.addr[2].split( ")" )[0]
                        except:
                          pass
                    except:
                      try:
                        if self.detail_data_list[3] == "over":
                          self.hardware_received = self.detail_data_list[2]
                          self.hardware_address = self.detail_data_list[4]
                      except:
                        pass
                    continue
                  if self.detail_data.startswith( "Layer" ):
                    self.layer_received = self.detail_data_list[1]
                    continue
                  if self.detail_data.startswith( "Description" ):
                    self.description_received = " ".join( self.detail_data.split()[1:] ).replace( "\"", "" )
                    continue
                  if self.detail_data.startswith( "Internet address is" ):
                    self.internet_address_received = self.detail_data_list[3]
                    continue
                  if self.detail_data.startswith( "MTU" ):
                    self.mtu_received = self.detail_data_list[1]
                    self.bandwidth_received = self.detail_data_list[4]
                    continue
                  elif self.detail_data.startswith( "reliability" ):
                    self.reliability_received = self.detail_data_list[1].split( "," )[0]
                    self.transmit_load_received = self.detail_data_list[3].split( "," )[0]
                    self.receive_load_received = self.detail_data_list[5]
                    continue
                  if self.detail_data.startswith( "Encapsulation" ):
                    self.encaps_received = self.detail_data_list[1].split( "," )[0]
                    continue
                  if self.detail_data.find( "-duplex" ) != -1:
                    self.duplex_received = self.detail_data_list[0].split( "-" )[0]
                    self.bit_per_sec_received = self.detail_data_list[1].split( "," )[0]
                    try:
                      self.link_type_received = self.detail_data.split( "is" )[1]
                    except:
                      self.link_type_received = ""
                    continue
                  if self.detail_data.startswith( "Duplex" ):
                    self.duplex_received = self.detail_data_list[1].split( "," )[0]
                    self.bit_per_sec_received = self.detail_data_list[2].split( "," )[0]
                    try:
                      self.link_type_received = self.detail_data.split( "is" )[1]
                    except:
                      self.link_type_received = ""
                    continue
                  if self.detail_data.startswith( "output flow control is" ):
                    self.output_flow_control_received = self.detail_data_list[4].split( "," )[0]
                    self.input_flow_control_received = self.detail_data_list[9]
                    continue
                  if self.detail_data.startswith( "Carrier delay" ):
                    self.carrier_delay_state_received = self.detail_data_list[2].split( ")" )[0].split( "(" )[1]
                    self.loopback_state_received = self.detail_data_list[
                      1]  # If value is "not" or empty FIXME GUESSING HERE
                    continue
                  if self.detail_data.startswith( "Last link flapped" ):
                    self.flapped_received = self.detail_data_list[3]
                    continue
                  if self.detail_data.startswith( "ARP type" ):
                    self.arp_type_received = self.detail_data_list[2].split( "," )[0]
                    self.arp_timeout_received = self.detail_data_list[5]
                    continue
                  #----------------------------------------------------------------------------------------------
                  # FIXME REALLY F'in UGLY code FIX it!!!!
                  if self.detail_data.find( "No. of members in this bundle:" ) != -1:
                    self.number_of_bundled_interfaces_received = self.detail_data_list[6]
                    self.counter = int( self.number_of_bundled_interfaces_received )
                    self.bundled_interfaces_received_str = "{"
                    for self.intf_count in range( self.counter ):
                      for self.detail_data in self.reportFD:
                        self.bundled_interfaces_received_str += "\"bundle {}\":".format( self.intf_count + 1 )
                        self.bundled_interfaces_received_str += "{"
                        self.a, self.b, self.c, self.d = self.detail_data.split()
                        self.bundled_interfaces_received_str += "\"interface\":\"{}\",".format( self.a )
                        self.bundled_interfaces_received_str += "\"duplex\":\"{}\",".format( self.b )
                        self.bundled_interfaces_received_str += "\"bits/ps\":\"{}\",".format( self.c )
                        self.bundled_interfaces_received_str += "\"mode\":\"{}\"".format( self.d )
                        self.bundled_interfaces_received_str += "},"
                        break
                    self.bundled_interfaces_received_dict = \
                         dict( ast.literal_eval( "{}".format( self.bundled_interfaces_received_str[:-1] ) +
                                                 "}" ) )
                    for key, interface_data in self.bundled_interfaces_received_dict.items():
                      self.bundled_interfaces_received.append( interface_data )
                    continue
                  if self.detail_data.startswith( "Input/output data rate is" ):
                    self.input_output_data_rate_received = self.detail_data_list[4].split( "." )[0]
                    continue
                  if self.detail_data.startswith( "Last input" ):
                    self.last_input_time_received = self.detail_data_list[2].split( "," )[0]
                    self.last_output_time_received = self.detail_data_list[4]
                    continue
                  if self.detail_data.startswith( "Last clearing" ):
                    self.last_clear_received = self.detail_data_list[6]
                    continue
                  if self.detail_data.find( "input rate" ) != -1:
                    try:
                      self.input_rate_received = int( self.detail_data_list[0] )
                    except:
                      self.input_rate_received = 0
                    try:
                      self.input_packet_rate_received = int( self.detail_data_list[6] )
                    except:
                      self.input_packet_rate_received = 0
                    continue
                  if self.detail_data.find( "output rate" ) != -1:
                    try:
                      self.output_rate_received = int( self.detail_data_list[0] )
                    except:
                      self.output_rate_received = 0
                    try:
                      self.output_packet_rate_received = int( self.detail_data_list[6] )
                    except:
                      self.output_packet_rate_received = 0
                    continue
                  if self.detail_data.find( "input drops," ) != -1:
                    try:
                      self.input_ignore_received = int( self.detail_data_list[0] )
                    except:
                      self.input_ignore_received = 0
                    try:
                      self.input_abort_received = int( self.detail_data_list[3] )
                    except:
                      self.input_abort_received = 0
                    try:
                      self.input_errors_received = int( self.detail_data_list[6] )
                    except:
                      self.input_errors_received = 0
                    continue
                  if self.detail_data.find( "output drops," ) != -1:
                    try:
                      self.output_applique_received = int( self.detail_data_list[0] )
                    except:
                      self.output_applique_received = 0
                    try:
                      self.output_resets_received = int( self.detail_data_list[3] )
                    except:
                      self.output_resets_received = 0
                    try:
                      self.output_errors_received = int( self.detail_data_list[6] )
                    except:
                      self.output_errors_received = 0
                    continue
                  if self.detail_data.find( "packets input," ) != -1:
                    try:
                      self.input_packets_received = int( self.detail_data_list[0] )
                    except:
                      self.input_packets_received = 0
                    try:
                      self.input_bytes_received = int( self.detail_data_list[3] )
                    except:
                      self.input_bytes_received = 0
                    try:
                      self.input_drops_received = int( self.detail_data_list[5] )
                    except:
                      self.input_drops_received = 0
                    continue
                  if self.detail_data.find( "drops for" ) != -1:
                    try:
                      self.up_level_protocol_drops_received = int( self.detail_data_list[0] )
                    except:
                      self.up_level_protocol_drops_received = 0
                    continue
                  if self.detail_data.startswith( "Received" ):
                    try:
                      self.input_broadcast_packets_received = int( self.detail_data_list[1] )
                    except:
                      self.input_broadcast_packets_received = 0
                    try:
                      self.input_multicast_packets_received = int( self.detail_data_list[4] )
                    except:
                      self.input_multicast_packets_received = 0
                    continue
                  if self.detail_data.find( "input errors," ) != -1:
                    try:
                      self.input_errors_received = int( self.detail_data_list[0] )
                    except:
                      self.input_errors_received = 0
                    try:
                      self.input_crc_received = int( self.detail_data_list[3] )
                    except:
                      self.input_crc_received = 0
                    try:
                      self.input_frame_received = int( self.detail_data_list[5] )
                    except:
                      self.input_frame_received = 0
                    try:
                      self.input_overrun_received = int( self.detail_data_list[7] )
                    except:
                      self.input_overrun_received = 0
                    try:
                      self.input_ignore_received = int( self.detail_data_list[9] )
                    except:
                      self.input_ignore_received = 0
                    try:
                      self.input_abort_received = int( self.detail_data_list[11] )
                    except:
                      self.input_abort_received = 0
                    continue
                  if self.detail_data.find( "packets output," ) != -1:
                    try:
                      self.output_packets_received = int( self.detail_data_list[0] )
                    except:
                      self.output_packets_received = 0
                    try:
                      self.output_bytes_received = int( self.detail_data_list[3] )
                    except:
                      self.output_bytes_received = 0
                    try:
                      self.output_drops_received = int( self.detail_data_list[5] )
                    except:
                      self.output_drops_received = 0
                    continue
                  if self.detail_data.startswith( "Output" ):
                    try:
                      self.output_broadcast_packets_received = int( self.detail_data_list[1] )
                    except:
                      self.output_broadcast_packets_received = 0
                    try:
                      self.output_multicast_packets_received = int( self.detail_data_list[4] )
                    except:
                      self.output_multicast_packets_received = 0
                    continue
                  if self.detail_data.find( "output errors," ) != -1:
                    try:
                      self.output_errors_received = int( self.detail_data_list[0] )
                    except:
                      self.output_errors_received = 0
                    try:
                      self.output_underruns_received = int( self.detail_data_list[3] )
                    except:
                      self.output_underruns_received = 0
                    try:
                      self.output_applique_received = int( self.detail_data_list[5] )
                    except:
                      self.output_applique_received = 0
                    try:
                      self.output_resets_received = int( self.detail_data_list[7] )
                    except:
                      self.output_resets_received = 0
                    continue
                  if self.detail_data.find( "output buffer failures," ) != -1:
                    try:
                      self.output_buffer_failures_received = int( self.detail_data_list[0] )
                    except:
                      self.output_buffer_failures_received = 0
                    try:
                      self.output_buffer_swapouts_received = int( self.detail_data_list[4] )
                    except:
                      self.output_buffer_swapouts_received = 0
                    continue
                  if self.detail_data_list[1].startswith( "carrier" ) and \
                      self.detail_data_list[2].startswith( "transitions" ):
                    try:
                      self.carrier_transitions_received = int( self.detail_data_list[0] )
                    except:
                      self.carrier_transitions_received = 0
                    continue
                except Exception as error:
                  raise Exception( "ShowInterfacesDetailAnalysisFileBuilder: "
                                   "error processing input: {}".format( error ) )
              """
              Now start checking for expected values
              """
              """
              Initialized Word document variables
              """
              if int( self.number_of_bundled_interfaces_to_check ) != \
                 int( self.number_of_bundled_interfaces_received ):
                self.msg_str = "{{\'cols\':[\'Number of Bundled Interfaces Expected:\',\'{}\'," \
                                          "\'Detected:\',\'{}\']}}". \
                  format( self.number_of_bundled_interfaces_to_check, self.number_of_bundled_interfaces_received )
                self.msgdict = ast.literal_eval( self.msg_str )
                self.testcase["analysisdata"].append( self.msgdict )
                # FIXME REMOVE ?self.generate_report( "Failed", self.testcase, self.reportFD, self.character_count )
                # FIXME REOVE ? self.reportFD.seek( 0, 2 )
                # FIXME REOVE ? break
              else:
                self.bundled_interfaces_test = True
                for self.key_value_dict_to_check in self.bundled_interfaces_to_check:
                  for self.key_value_dict_received in self.bundled_interfaces_received:
                    if self.key_value_dict_to_check != self.key_value_dict_received:
                      self.msg_str = "{{\'cols\':[\'Bundled Interface Expected:\',\'{}\'," \
                                     "\'Detected:\',\'{}\']}}". \
                        format( self.key_value_dict_to_check, self.key_value_dict_received )
                      self.msgdict = ast.literal_eval( self.msg_str )
                      self.testcase["analysisdata"].append( self.msgdict )
                      # FIXME REMOVE ?self.generate_report( "Failed", self.testcase, self.reportFD, self.character_count )
                      continue
                    else:
                      break
                # FIXME REMOVE ? self.reportFD.seek( 0, 2 )
                # FIXME REMOVE ? break
              """
              Validate all detected(received) values are less-then expected values
              """
              self.islessthan()
              # FIXME REMOVE ? if self.testcase["analysisdata"]:
              # FIXME REMOVE ?   self.generate_report( "Failed", self.testcase, self.reportFD, self.character_count )
              # FIXME   # FIXME REMOVE ? self.reportFD.seek( 0, 2 )
              # FIXME   # FIXME REMOVE ? break
              self.isgreaterthan()
              # FIXME if self.testcase["analysisdata"]:
              # FIXME   self.generate_report( "Failed", self.testcase, self.reportFD, self.character_count )
              # FIXME   # FIXME REMOVE ? self.reportFD.seek( 0, 2 )
              # FIXME   # FIXME REMOVE ? break
              """"
              CHecks that really dont make sense at this time!
              last_input_time_to_check         ==  last_input_time_received 
              last_output_time_to_check        ==  last_output_time_received 
              flapped_to_check                 ==  flapped_received:
              input_rate_to_check              ==  input_rate_received 
              output_rate_to_check             ==  output_rate_received 
              input_output_data_rate_to_check  ==  input_output_data_rate_received 
              last_clear_to_check              ==  last_clear_received 
              transmit_load_to_check           ==  transmit_load_received 
              receive_load_to_check            ==  receive_load_received 
              carrier_delay_state_to_check     ==  carrier_delay_state_received 
              loopback_state_to_check          ==  loopback_state_received 
              """
              self.isequalto()
              if self.testcase["analysisdata"]:
                self.generate_report( "Failed", self.testcase, self.reportFD, self.character_count )
                self.reportFD.seek( 0, 2 )
              else:
                "{{\'cols\':[\'Interface Admin State\',\'{}\',\'{}\']}}"
                self.isequaltomsg_str = "{{\'cols\':[\'All parameters\',\'{}\',\'{}\']}}". \
                                        format( "VALIDATED", "" )
                self.isequaltomsgdict = ast.literal_eval( self.isequaltomsg_str )
                RichTextProcessor().plain_text_to_richtext_format( self.isequaltomsgdict )
                self.testcase["analysisdata"].append( self.isequaltomsgdict )
                self.generate_report( "Passed", self.testcase, self.reportFD, self.character_count )
                self.reportFD.seek( 0, 2 )
            else:
              self.found_Interface_flag = False
          else:
            continue
        else:
          self.start_processing_details_flag = False
          continue
    if not self.found_Interface_flag:
      self.msg_str = "{{\'cols\':[\'Interface Expected:\',\'{}\'," \
                     "\'Detected:\',\'{}\']}}". \
        format( self.interface_to_check , "NOT FOUND!" )
      self.msgdict = ast.literal_eval( self.msg_str )
      self.testcase["analysisdata"] = self.msgdict
      self.generate_report( "Failed", self.testcase, self.reportFD, self.character_count )
    self.reportFD.seek( 0 )
    return (self.reportFD)
  """
  """
  def juniper_interface( self, seed_logical_dict, reportFD ):
    self.reportFD = reportFD
    self.seed_logical_dict = seed_logical_dict
    return (self.reportFD)
  """
  Checks the expected equal values,
  reporting anything values received that are not equal to what is expected
  """
  def isequalto( self ):
    if self.interface_admin_state_to_check != self.interface_admin_state_received:
      self.isequaltomsg_str = "{{\'cols\':[\'Interface Admin State\',\'{}\',\'{}\']}}". \
        format( self.interface_admin_state_to_check, self.interface_admin_state_received )
      self.isequaltomsgdict = ast.literal_eval( self.isequaltomsg_str )
      RichTextProcessor().plain_text_to_richtext_format( self.isequaltomsgdict )
      self.testcase["analysisdata"].append( self.isequaltomsgdict )
    if self.interface_line_protocol_state_to_check != self.interface_line_protocol_state_received:
      self.isequaltomsg_str = "{{\'cols\':[\'Interface Line Protocol State\',\'{}\',\'{}\']}}". \
        format( self.interface_line_protocol_state_to_check, self.interface_line_protocol_state_received )
      self.isequaltomsgdict = ast.literal_eval( self.isequaltomsg_str )
      RichTextProcessor().plain_text_to_richtext_format( self.isequaltomsgdict )
      self.testcase["analysisdata"].append( self.isequaltomsgdict )
    if self.state_transitions_to_check != "-1" and int(self.state_transitions_to_check) > int(self.state_transitions_received):
      self.isequaltomsg_str = "{{\'cols\':[\'Interface State Transition\',\'{}\',\'{}\']}}". \
        format( self.state_transitions_to_check, self.state_transitions_received )
      self.isequaltomsgdict = ast.literal_eval( self.isequaltomsg_str )
      RichTextProcessor().plain_text_to_richtext_format( self.isequaltomsgdict )
      self.testcase["analysisdata"].append( self.isequaltomsgdict )
    if self.hardware_to_check != self.hardware_received:
      self.isequaltomsg_str = "{{\'cols\':[\'Hardware\',\'{}\',\'{}\']}}". \
        format( self.hardware_to_check, self.hardware_received )
      self.isequaltomsgdict = ast.literal_eval( self.isequaltomsg_str )
      RichTextProcessor().plain_text_to_richtext_format( self.isequaltomsgdict )
      self.testcase["analysisdata"].append( self.isequaltomsgdict )
    if self.hardware_address_to_check != self.hardware_address_received:
      self.isequaltomsg_str = "{{\'cols\':[\'Hardware Address\',\'{}\',\'{}\']}}". \
        format( self.hardware_address_to_check, self.hardware_address_received )
      self.isequaltomsgdict = ast.literal_eval( self.isequaltomsg_str )
      RichTextProcessor().plain_text_to_richtext_format( self.isequaltomsgdict )
      self.testcase["analysisdata"].append( self.isequaltomsgdict )
    if self.hardware_address_bia_to_check != self.hardware_address_bia_received:
      self.isequaltomsg_str = "{{\'cols\':[\'Hardware Address Bia\',\'{}\',\'{}\']}}". \
        format( self.hardware_address_bia_to_check, self.hardware_address_bia_received )
      self.isequaltomsgdict = ast.literal_eval( self.isequaltomsg_str )
      RichTextProcessor().plain_text_to_richtext_format( self.isequaltomsgdict )
      self.testcase["analysisdata"].append( self.isequaltomsgdict )
    if self.layer_to_check != self.layer_received:
      self.isequaltomsg_str = "{{\'cols\':[\'Layer\',\'{}\',\'{}\']}}". \
        format( self.layer_to_check, self.layer_received )
      self.isequaltomsgdict = ast.literal_eval( self.isequaltomsg_str )
      RichTextProcessor().plain_text_to_richtext_format( self.isequaltomsgdict )
      self.testcase["analysisdata"].append( self.isequaltomsgdict )
    if self.description_to_check != self.description_received:
      self.isequaltomsg_str = "{{\'cols\':[\'Description\',\'{}\',\'{}\']}}". \
        format( self.description_to_check, self.description_received )
      self.isequaltomsgdict = ast.literal_eval( self.isequaltomsg_str )
      RichTextProcessor().plain_text_to_richtext_format( self.isequaltomsgdict )
      self.testcase["analysisdata"].append( self.isequaltomsgdict )
    if self.internet_address_to_check != self.internet_address_received:
      self.isequaltomsg_str = "{{\'cols\':[\'Internet Address\',\'{}\',\'{}\']}}". \
        format( self.internet_address_to_check, self.internet_address_received )
      self.isequaltomsgdict = ast.literal_eval( self.isequaltomsg_str )
      RichTextProcessor().plain_text_to_richtext_format( self.isequaltomsgdict )
      self.testcase["analysisdata"].append( self.isequaltomsgdict )
    if self.mtu_to_check != self.mtu_received:
      self.isequaltomsg_str = "{{\'cols\':[\'MTU\',\'{}\',\'{}\']}}". \
        format( self.mtu_to_check, self.mtu_received )
      self.isequaltomsgdict = ast.literal_eval( self.isequaltomsg_str )
      RichTextProcessor().plain_text_to_richtext_format( self.isequaltomsgdict )
      self.testcase["analysisdata"].append( self.isequaltomsgdict )
    if self.bandwidth_to_check != self.bandwidth_received:
      self.isequaltomsg_str = "{{\'cols\':[\'Bandwidth\',\'{}\',\'{}\']}}". \
        format( self.bandwidth_to_check, self.bandwidth_received )
      self.isequaltomsgdict = ast.literal_eval( self.isequaltomsg_str )
      RichTextProcessor().plain_text_to_richtext_format( self.isequaltomsgdict )
      self.testcase["analysisdata"].append( self.isequaltomsgdict )
    if self.reliability_to_check != self.reliability_received:
      self.isequaltomsg_str = "{{\'cols\':[\'Reliability\',\'{}\',\'{}\']}}". \
        format( self.reliability_to_check, self.reliability_received )
      self.isequaltomsgdict = ast.literal_eval( self.isequaltomsg_str )
      RichTextProcessor().plain_text_to_richtext_format( self.isequaltomsgdict )
      self.testcase["analysisdata"].append( self.isequaltomsgdict )
    if self.encaps_to_check != self.encaps_received:
      self.isequaltomsg_str = "{{\'cols\':[\'Encapsulation\',\'{}\',\'{}\']}}". \
        format( self.encaps_to_check, self.encaps_received )
      self.isequaltomsgdict = ast.literal_eval( self.isequaltomsg_str )
      RichTextProcessor().plain_text_to_richtext_format( self.isequaltomsgdict )
      self.testcase["analysisdata"].append( self.isequaltomsgdict )
    if self.duplex_to_check != self.duplex_received:
      self.isequaltomsg_str = "{{\'cols\':[\'Dumplex\',\'{}\',\'{}\']}}". \
        format( self.duplex_to_check, self.duplex_received )
      self.isequaltomsgdict = ast.literal_eval( self.isequaltomsg_str )
      RichTextProcessor().plain_text_to_richtext_format( self.isequaltomsgdict )
      self.testcase["analysisdata"].append( self.isequaltomsgdict )
    if self.bit_per_sec_to_check != self.bit_per_sec_received:
      self.isequaltomsg_str = "{{\'cols\':[\'Bits Per Second\',\'{}\',\'{}\']}}". \
        format( self.bit_per_sec_to_check, self.bit_per_sec_received )
      self.isequaltomsgdict = ast.literal_eval( self.isequaltomsg_str )
      RichTextProcessor().plain_text_to_richtext_format( self.isequaltomsgdict )
      self.testcase["analysisdata"].append( self.isequaltomsgdict )
    if self.link_type_to_check != self.link_type_received:
      self.isequaltomsg_str = "{{\'cols\':[\'Link Type\',\'{}\',\'{}\']}}". \
        format( self.link_type_to_check, self.link_type_received )
      self.isequaltomsgdict = ast.literal_eval( self.isequaltomsg_str )
      RichTextProcessor().plain_text_to_richtext_format( self.isequaltomsgdict )
      self.testcase["analysisdata"].append( self.isequaltomsgdict )
    if self.output_flow_control_to_check != self.output_flow_control_received:
      self.isequaltomsg_str = "{{\'cols\':[\'Output Flow Control\',\'{}\',\'{}\']}}". \
        format( self.output_flow_control_to_check, self.output_flow_control_received )
      self.isequaltomsgdict = ast.literal_eval( self.isequaltomsg_str )
      RichTextProcessor().plain_text_to_richtext_format( self.isequaltomsgdict )
      self.testcase["analysisdata"].append( self.isequaltomsgdict )
    if self.input_flow_control_to_check != self.input_flow_control_received:
      self.isequaltomsg_str = "{{\'cols\':[\'Input Flow Control\',\'{}\',\'{}\']}}". \
        format( self.input_flow_control_to_check, self.input_flow_control_received )
      self.isequaltomsgdict = ast.literal_eval( self.isequaltomsg_str )
      RichTextProcessor().plain_text_to_richtext_format( self.isequaltomsgdict )
      self.testcase["analysisdata"].append( self.isequaltomsgdict )
    if self.arp_type_to_check != self.arp_type_received:
      self.isequaltomsg_str = "{{\'cols\':[\'ARP Type\',\'{}\',\'{}\']}}". \
        format( self.arp_type_to_check, self.arp_type_received )
      self.isequaltomsgdict = ast.literal_eval( self.isequaltomsg_str )
      RichTextProcessor().plain_text_to_richtext_format( self.isequaltomsgdict )
      self.testcase["analysisdata"].append( self.isequaltomsgdict )
    if self.arp_timeout_to_check != self.arp_timeout_received:
      self.isequaltomsg_str = "{{\'cols\':[\'ARP Timeout\',\'{}\',\'{}\']}}". \
        format( self.arp_timeout_to_check, self.arp_timeout_received )
      self.isequaltomsgdict = ast.literal_eval( self.isequaltomsg_str )
      RichTextProcessor().plain_text_to_richtext_format( self.isequaltomsgdict )
      self.testcase["analysisdata"].append( self.isequaltomsgdict )
    return()
  """
  Checks the expected greater-than values,
  reporting anything values received that are less then expected
  """
  def isgreaterthan( self ):
    if self.input_packets_to_check > self.input_packets_received:
      self.greaterthanmsg_str = "{{\'cols\':[\'Input Packets\',\'{}\',\'{}\']}}". \
        format( self.input_packets_to_check, self.input_packets_received )
      self.greaterthanmsgdict = ast.literal_eval( self.greaterthanmsg_str )
      RichTextProcessor().plain_text_to_richtext_format( self.greaterthanmsgdict )
      self.testcase["analysisdata"].append( self.greaterthanmsgdict )
    if self.input_bytes_to_check > self.input_bytes_received:
      self.greaterthanmsg_str = "{{\'cols\':[\'Input Bytes\',\'{}\',\'{}\']}}". \
        format( self.input_bytes_to_check, self.input_bytes_received )
      self.greaterthanmsgdict = ast.literal_eval( self.greaterthanmsg_str )
      RichTextProcessor().plain_text_to_richtext_format( self.greaterthanmsgdict )
      self.testcase["analysisdata"].append( self.greaterthanmsgdict )
    if self.output_packets_to_check > self.output_packets_received:
      self.greaterthanmsg_str = "{{\'cols\':[\'Output Packets\',\'{}\',\'{}\']}}". \
        format( self.output_packets_to_check, self.output_packets_received )
      self.greaterthanmsgdict = ast.literal_eval( self.greaterthanmsg_str )
      RichTextProcessor().plain_text_to_richtext_format( self.greaterthanmsgdict )
      self.testcase["analysisdata"].append( self.greaterthanmsgdict )
    if self.output_bytes_to_check > self.output_bytes_received:
      self.greaterthanmsg_str = "{{\'cols\':[\'Output Bytes\',\'{}\',\'{}\']}}". \
        format( self.output_bytes_to_check, self.output_bytes_received )
      self.greaterthanmsgdict = ast.literal_eval( self.greaterthanmsg_str )
      RichTextProcessor().plain_text_to_richtext_format( self.greaterthanmsgdict )
      self.testcase["analysisdata"].append( self.greaterthanmsgdict )
    if self.input_packet_rate_to_check > self.input_packet_rate_received:
      self.greaterthanmsg_str = "{{\'cols\':[\'Input Packet Rate\',\'{}\',\'{}\']}}". \
        format( self.input_packet_rate_to_check, self.input_packet_rate_received )
      self.greaterthanmsgdict = ast.literal_eval( self.greaterthanmsg_str )
      RichTextProcessor().plain_text_to_richtext_format( self.greaterthanmsgdict )
      self.testcase["analysisdata"].append( self.greaterthanmsgdict )
    if self.output_packet_rate_to_check > self.output_packet_rate_received:
      self.greaterthanmsg_str = "{{\'cols\':[\'Output Packets\',\'{}\',\'{}\']}}". \
        format( self.output_packet_rate_to_check, self.output_packet_rate_received )
      self.greaterthanmsgdict = ast.literal_eval( self.greaterthanmsg_str )
      RichTextProcessor().plain_text_to_richtext_format( self.greaterthanmsgdict )
      self.testcase["analysisdata"].append( self.greaterthanmsgdict )
    if self.input_broadcast_packets_to_check > self.input_broadcast_packets_received:
      self.greaterthanmsg_str = "{{\'cols\':[\'Input Broadcast Packets\',\'{}\',\'{}\']}}". \
        format( self.input_broadcast_packets_to_check, self.input_broadcast_packets_received )
      self.greaterthanmsgdict = ast.literal_eval( self.greaterthanmsg_str )
      RichTextProcessor().plain_text_to_richtext_format( self.greaterthanmsgdict )
      self.testcase["analysisdata"].append( self.greaterthanmsgdict )
    if self.input_multicast_packets_to_check > self.input_multicast_packets_received:
      self.greaterthanmsg_str = "{{\'cols\':[\'Input Multicast Packets\',\'{}\',\'{}\']}}". \
        format( self.input_multicast_packets_to_check, self.input_multicast_packets_received )
      self.greaterthanmsgdict = ast.literal_eval( self.greaterthanmsg_str )
      RichTextProcessor().plain_text_to_richtext_format( self.greaterthanmsgdict )
      self.testcase["analysisdata"].append( self.greaterthanmsgdict )
    return()
  """
  Checks the expected less-than values,
  reporting anything values received that are more then expected
  """
  def islessthan( self ):
    if self.input_crc_to_check < self.input_crc_received:
      self.lessthanmsg_str = "{{\'cols\':[\'CRC\',\'{}\',\'{}\']}}".\
          format( self.input_crc_to_check, self.input_crc_received )
      self.lessthanmsgdict = ast.literal_eval( self.lessthanmsg_str )
      RichTextProcessor().plain_text_to_richtext_format( self.lessthanmsgdict )
      self.testcase["analysisdata"].append( self.lessthanmsgdict )
    if self.input_frame_to_check < self.input_frame_received:
      self.lessthanmsg_str = "{{\'cols\':[\'Frame\',\'{}\',\'{}\']}}".\
          format( self.input_frame_to_check, self.input_frame_received )
      self.lessthanmsgdict = ast.literal_eval( self.lessthanmsg_str )
      RichTextProcessor().plain_text_to_richtext_format( self.lessthanmsgdict )
      self.testcase["analysisdata"].append( self.lessthanmsgdict )
    if self.input_overrun_to_check < self.input_overrun_received:
      self.lessthanmsg_str = "{{\'cols\':[\'Overruns\',\'{}\',\'{}\']}}".\
          format( self.input_overrun_to_check, self.input_overrun_received )
      self.lessthanmsgdict = ast.literal_eval( self.lessthanmsg_str )
      RichTextProcessor().plain_text_to_richtext_format( self.lessthanmsgdict )
      self.testcase["analysisdata"].append( self.lessthanmsgdict )
    if self.input_drops_to_check < self.input_drops_received:
      self.lessthanmsg_str = "{{\'cols\':[\'Input Drops\',\'{}\',\'{}\']}}".\
          format( self.input_drops_to_check, self.input_drops_received )
      self.lessthanmsgdict = ast.literal_eval( self.lessthanmsg_str )
      RichTextProcessor().plain_text_to_richtext_format( self.lessthanmsgdict )
      self.testcase["analysisdata"].append( self.lessthanmsgdict )
    if self.up_level_protocol_drops_to_check < self.up_level_protocol_drops_received:
      self.lessthanmsg_str = "{{\'cols\':[\'Protocol Drops\',\'{}\',\'{}\']}}".\
          format( self.up_level_protocol_drops_to_check, self.up_level_protocol_drops_received )
      self.lessthanmsgdict = ast.literal_eval( self.lessthanmsg_str )
      RichTextProcessor().plain_text_to_richtext_format( self.lessthanmsgdict )
      self.testcase["analysisdata"].append( self.lessthanmsgdict )
    if self.output_errors_to_check < self.output_errors_received:
      self.lessthanmsg_str = "{{\'cols\':[\'Output Errors\',\'{}\',\'{}\']}}".\
          format( self.output_errors_to_check, self.output_errors_received )
      self.lessthanmsgdict = ast.literal_eval( self.lessthanmsg_str )
      RichTextProcessor().plain_text_to_richtext_format( self.lessthanmsgdict )
      self.testcase["analysisdata"].append( self.lessthanmsgdict )
    if self.output_underruns_to_check < self.output_underruns_received:
      self.lessthanmsg_str = "{{\'cols\':[\'Underruns\',\'{}\',\'{}\']}}".\
          format( self.output_underruns_to_check, self.output_underruns_received )
      self.lessthanmsgdict = ast.literal_eval( self.lessthanmsg_str )
      RichTextProcessor().plain_text_to_richtext_format( self.lessthanmsgdict )
      self.testcase["analysisdata"].append( self.lessthanmsgdict )
    if self.input_errors_to_check < self.input_errors_received:
      self.lessthanmsg_str = "{{\'cols\':[\'Input Errors\',\'{}\',\'{}\']}}".\
          format( self.input_errors_to_check, self.input_errors_received )
      self.lessthanmsgdict = ast.literal_eval( self.lessthanmsg_str )
      RichTextProcessor().plain_text_to_richtext_format( self.lessthanmsgdict )
      self.testcase["analysisdata"].append( self.lessthanmsgdict )
    if self.input_ignore_to_check < self.input_ignore_received:
      self.lessthanmsg_str = "{{\'cols\':[\'Input Ignores\',\'{}\',\'{}\']}}".\
          format( self.input_ignore_to_check, self.input_ignore_received )
      self.lessthanmsgdict = ast.literal_eval( self.lessthanmsg_str )
      RichTextProcessor().plain_text_to_richtext_format( self.lessthanmsgdict )
      self.testcase["analysisdata"].append( self.lessthanmsgdict )
    if self.input_abort_to_check < self.input_abort_received:
      self.lessthanmsg_str = "{{\'cols\':[\'Input Aborts\',\'{}\',\'{}\']}}".\
          format( self.input_abort_to_check, self.input_abort_received )
      self.lessthanmsgdict = ast.literal_eval( self.lessthanmsg_str )
      RichTextProcessor().plain_text_to_richtext_format( self.lessthanmsgdict )
      self.testcase["analysisdata"].append( self.lessthanmsgdict )
    if self.output_drops_to_check < self.output_drops_received:
      self.lessthanmsg_str = "{{\'cols\':[\'Output Drops\',\'{}\',\'{}\']}}".\
          format( self.output_drops_to_check, self.output_drops_received )
      self.lessthanmsgdict = ast.literal_eval( self.lessthanmsg_str )
      RichTextProcessor().plain_text_to_richtext_format( self.lessthanmsgdict )
      self.testcase["analysisdata"].append( self.lessthanmsgdict )
    if self.output_applique_to_check < self.output_applique_received:
      self.lessthanmsg_str = "{{\'cols\':[\'Applique\',\'{}\',\'{}\']}}".\
          format( self.output_applique_to_check, self.output_applique_received )
      self.lessthanmsgdict = ast.literal_eval( self.lessthanmsg_str )
      RichTextProcessor().plain_text_to_richtext_format( self.lessthanmsgdict )
      self.testcase["analysisdata"].append( self.lessthanmsgdict )
    if self.output_resets_to_check < self.output_resets_received:
      self.lessthanmsg_str = "{{\'cols\':[\'Output Resets\',\'{}\',\'{}\']}}".\
          format( self.output_resets_to_check, self.output_resets_received )
      self.lessthanmsgdict = ast.literal_eval( self.lessthanmsg_str )
      RichTextProcessor().plain_text_to_richtext_format( self.lessthanmsgdict )
      self.testcase["analysisdata"].append( self.lessthanmsgdict )
    if self.output_buffer_failures_to_check < self.output_buffer_failures_received:
      self.lessthanmsg_str = "{{\'cols\':[\'Output Buffer Failures\',\'{}\',\'{}\']}}".\
          format( self.output_buffer_failures_to_check, self.output_buffer_failures_received )
      self.lessthanmsgdict = ast.literal_eval( self.lessthanmsg_str )
      RichTextProcessor().plain_text_to_richtext_format( self.lessthanmsgdict )
      self.testcase["analysisdata"].append( self.lessthanmsgdict )
    if self.output_buffer_swapouts_to_check < self.output_buffer_swapouts_received:
      self.lessthanmsg_str = "{{\'cols\':[\'Output Buffer Swapouts\',\'{}\',\'{}\']}}".\
          format( self.output_buffer_swapouts_to_check, self.output_buffer_swapouts_received )
      self.lessthanmsgdict = ast.literal_eval( self.lessthanmsg_str )
      RichTextProcessor().plain_text_to_richtext_format( self.lessthanmsgdict )
      self.testcase["analysisdata"].append( self.lessthanmsgdict )
    if self.carrier_transitions_to_check < self.carrier_transitions_received:
      self.lessthanmsg_str = "{{\'cols\':[\'Carrier Transition\',\'{}\',\'{}\']}}".\
          format( self.carrier_transitions_to_check, self.carrier_transitions_received )
      self.lessthanmsgdict = ast.literal_eval( self.lessthanmsg_str )
      RichTextProcessor().plain_text_to_richtext_format( self.lessthanmsgdict )
      self.testcase["analysisdata"].append( self.lessthanmsgdict )
    return()
  #----------------------------------------------------------------------------------------------------------------
  #----------------------------------------------------------------------------------------------------------------
  # NOT REPORTED TBD
  #
  #  "Carrier Delay State:{} Detected:{} "
  #  "Loopback State:{} Detected:{} "
  #  self.carrier_delay_state_to_check, self.carrier_delay_state_received,
  #  self.loopback_state_to_check, self.loopback_state_received,
  #----------------------------------------------------------------------------------------------------------------
  def generate_report( self, pass_fail, testcase, reportFD, character_count ):
    self.testcase = testcase
    self.reportFD = reportFD
    self.reportFD.seek( character_count )
    for self.report_data in self.reportFD:
      self.testcase["detailedresultsdata"] += self.report_data
    self.testcase["statusdata"] = "COMPLETED"
    if pass_fail == "Failed":
      self.testcase["resultsdata"] = "FAILED"
      self.message_str = "Testcase FAILED!"
    else:
      self.testcase["resultsdata"] = "PASSED"
      self.message_str = "Testcase PASSED."
    ReportGenerator( self ).report_generator( self.testcase )
    self.parent.ggparent.processor_message_signal.emit( self.message_str )
    return()
  #----------------------------------------------------------------------------------------------------------------
  # FIXME DEBUG STUFF
  #----------------------------------------------------------------------------------------------------------------
  def print_table_data( self ):
    print(
      "Interface:{} Detected:{} \n"
      "Admin:{} Detected:{} \n"
      "Line:{} Detected:{} \n"
      "State Transitions:{} Detected:{} \n"
      "Hardware:{} Detected:{} \n"
      "Hardware Address:{} Detected:{} \n"
      "Hardware Address Bia:{} Detected:{} \n"
      "Layer:{} Detected:{} \n"
      "Description:{} Detected:{} \n"
      "Internet Address:{} Detected:{} \n"
      "Mtu:{} Detected:{} \n"
      "Bandwidth:{} Detected:{} \n"
      "Reliability:{} Detected:{} \n"
      "Transmit Load:{} Detected:{} \n"
      "Receive Load:{} Detected:{} \n"
      "Encaps:{} Detected:{} \n"
      "Duplex:{} Detected:{} \n"
      "Bit Per Sec:{} Detected:{} \n"
      "Link Type:{} Detected:{} \n"
      "Output Flow Control:{} Detected:{} \n"
      "Input Flow Control:{} Detected:{} \n"
      "Carrier Delay State:{} Detected:{} \n"
      "Loopback State:{} Detected:{} \n"
      "Flapped:{} Detected:{} \n"
      "Arp Type:{} Detected:{} \n"
      "Arp Timeout:{} Detected:{} \n"
      "Input Output Data Rate Received:{} Detected:{} \n"
      "Last Input Time:{} Detected:{} \n"
      "Last Output Time:{} Detected:{} \n"
      "Last Clear:{} Detected:{} \n"
      "Input Rate:{} Detected:{} \n"
      "Input Packet Rate:{} Detected:{} \n"
      "Output Rate:{} Detected:{} \n"
      "Output Packet Rate:{} Detected:{} \n"
      "Input Packets:{} Detected:{} \n"
      "Input Bytes:{} Detected:{} \n"
      "Input Drops:{} Detected:{} \n"
      "Up Level Protocol Drops:{} Detected:{} \n"
      "Input Broadcast Packets:{} Detected:{} \n"
      "Input Multicast Packets:{} Detected:{} \n"
      "Input Errors:{} Detected:{} \n"
      "Input Crc:{} Detected:{} \n"
      "Input Frame:{} Detected:{} \n"
      "Input Overrun:{} Detected:{} \n"
      "Input Ignore:{} Detected:{} \n"
      "Input Abort:{} Detected:{} \n"
      "Output Packets:{} Detected:{} \n"
      "Output Bytes:{} Detected:{} \n"
      "Output Drops:{} Detected:{} \n"
      "Output Broadcast Packets:{} Detected:{} \n"
      "Output Multicast Packets:{} Detected:{} \n"
      "Output Errors:{} Detected:{} \n"
      "Output Underruns:{} Detected:{} \n"
      "Output Applique:{} Detected:{} \n"
      "Output Resets:{} Detected:{} \n"
      "Output Buffer Failures:{} Detected:{} \n"
      "Output Buffer Swapouts:{} Detected:{} \n"
      "Carrier Transitions:{} Detected:{}\n".
        format(
        self.interface_to_check, self.interface_received,
        self.interface_admin_state_to_check, self.interface_admin_state_received,
        self.interface_line_protocol_state_to_check, self.interface_line_protocol_state_received,
        self.state_transitions_to_check, self.state_transitions_received,
        self.hardware_to_check, self.hardware_received,
        self.hardware_address_to_check, self.hardware_address_received,
        self.hardware_address_bia_to_check, self.hardware_address_bia_received,
        self.layer_to_check, self.layer_received,
        self.description_to_check, self.description_received,
        self.internet_address_to_check, self.internet_address_received,
        self.mtu_to_check, self.mtu_received,
        self.bandwidth_to_check, self.bandwidth_received,
        self.reliability_to_check, self.reliability_received,
        self.transmit_load_to_check, self.transmit_load_received,
        self.receive_load_to_check, self.receive_load_received,
        self.encaps_to_check, self.encaps_received,
        self.duplex_to_check, self.duplex_received,
        self.bit_per_sec_to_check, self.bit_per_sec_received,
        self.link_type_to_check, self.link_type_received,
        self.output_flow_control_to_check, self.output_flow_control_received,
        self.input_flow_control_to_check, self.input_flow_control_received,
        self.carrier_delay_state_to_check, self.carrier_delay_state_received,
        self.loopback_state_to_check, self.loopback_state_received,
        self.flapped_to_check, self.flapped_received,
        self.arp_type_to_check, self.arp_type_received,
        self.arp_timeout_to_check, self.arp_timeout_received,
        self.input_output_data_rate_to_check, self.input_output_data_rate_received,
        self.last_input_time_to_check, self.last_input_time_received,
        self.last_output_time_to_check, self.last_output_time_received,
        self.last_clear_to_check, self.last_clear_received,
        self.input_rate_to_check, self.input_rate_received,
        self.input_packet_rate_to_check, self.input_packet_rate_received,
        self.output_rate_to_check, self.output_rate_received,
        self.output_packet_rate_to_check, self.output_packet_rate_received,
        self.input_packets_to_check, self.input_packets_received,
        self.input_bytes_to_check, self.input_bytes_received,
        self.input_drops_to_check, self.input_drops_received,
        self.up_level_protocol_drops_to_check, self.up_level_protocol_drops_received,
        self.input_broadcast_packets_to_check, self.input_broadcast_packets_received,
        self.input_multicast_packets_to_check, self.input_multicast_packets_received,
        self.input_errors_to_check, self.input_errors_received,
        self.input_crc_to_check, self.input_crc_received,
        self.input_frame_to_check, self.input_frame_received,
        self.input_overrun_to_check, self.input_overrun_received,
        self.input_ignore_to_check, self.input_ignore_received,
        self.input_abort_to_check, self.input_abort_received,
        self.output_packets_to_check, self.output_packets_received,
        self.output_bytes_to_check, self.output_bytes_received,
        self.output_drops_to_check, self.output_drops_received,
        self.output_broadcast_packets_to_check, self.output_broadcast_packets_received,
        self.output_multicast_packets_to_check, self.output_multicast_packets_received,
        self.output_errors_to_check, self.output_errors_received,
        self.output_underruns_to_check, self.output_underruns_received,
        self.output_applique_to_check, self.output_applique_received,
        self.output_resets_to_check, self.output_resets_received,
        self.output_buffer_failures_to_check, self.output_buffer_failures_received,
        self.output_buffer_swapouts_to_check, self.output_buffer_swapouts_received,
        self.carrier_transitions_to_check, self.carrier_transitions_received
      ) )
    return()
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
# Show L2VPN Xconnect Detail
#------------------------------------------------------------------------------------------------------------------
class ShowL2VpnXconnectDetail:
  "Show L2Vpn Xconnect Detail"
  #----------------------------------------------------------------------------------------------------------------
  def __init__( self, parent = None ):
    self.name = "Show L2Vpn Xconnect Detail"
    self.parent = parent
    self.filename_time_extension = parent.filename_time_extension
    self.process_reply = self.parent.process_reply
    self.cmd_list = self.parent.cmd_list
    self.is_search_item = self.parent.is_search_item
    self.testcase_name = self.parent.testcase_name
    self.analysis_data_filename = self.parent.analysis_data_filename
    self.seed_list = []
    self.command_issued = ""
    self.line_number = 0
    self.line_number_head = 0
    self.device = ""
    #--------------------------------------------------------------------------------------------------------------
    self.l2vpn_intfac_to_check = []
    self.l2vpn_neighborpw_to_check = []
    self.l2vpn_acgroup_to_check = []
    self.l2vpn_pwgroup_to_check = []
    self.l2vpn_intfac_received = []
    self.l2vpn_neighborpw_received = []
    self.l2vpn_acgroup_received = []
    self.l2vpn_pwgroup_received = []
    self.l2vpn_xconnect_received = []
    self.l2vpn_xconnects_received = []
  #----------------------------------------------------------------------------------------------------------------
  def execute( self, seed_logical_dict, reportFD ):
    self.reportFD = reportFD
    self.seed_logical_dict = collections.OrderedDict( seed_logical_dict )
    self.device = self.seed_logical_dict["device"]
    #--------------------------------------------------------------------------------------------------------------
    if self.seed_logical_dict["device"] == "juniper":
      self.reportFD = self.juniper_l2vpn_xconnect_detail_analysis( self.seed_logical_dict, self.reportFD )
    elif self.seed_logical_dict["device"] == "cisco":
      self.reportFD = self.cisco_l2vpn_xconnect_detail_analysis( self.seed_logical_dict, self.reportFD )
    else:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    return ()
  #----------------------------------------------------------------------------------------------------------------
  def cisco_l2vpn_xconnect_detail_analysis( self, seed_logical_dict, reportFD ):
    self.reportFD = reportFD
    self.seed_logical_dict = seed_logical_dict
    #-------------------------------------------------------------------------------------------------------------
    # FIXME UGLY!!! FIND A BETTER WAY THAN FLAGS !!!!!
    self.found_l2vpn_flag = False
    #-------------------------------------------------------------------------------------------------------------
    try:
      self.command_issued_str = self.seed_logical_dict["show l2vpn xconnect detail"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.l2vpn_device_to_check = self.seed_logical_dict["device"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.l2vpn_group_to_check = self.seed_logical_dict["group"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.l2vpn_xconnect_to_check = self.seed_logical_dict["xconnect"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.l2vpn_group_state_to_check = self.seed_logical_dict["state"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    try:
      self.l2vpn_group_interwork_to_check = self.seed_logical_dict["interwork"]
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    #------------------------------------------------------------------------------------------------------------
    # FIXME here is an example of rework needed.  If the key names where better hard coded key names could
    # FIXME be avoided
    #------------------------------------------------------------------------------------------------------------
    try:
      for self.key, self.value in self.seed_logical_dict.items():
        if self.key.split()[0].startswith( "intf" ):
          self.build_list_to_check( self.key, self.value, self.l2vpn_intfac_to_check )
          continue
        if self.key.split()[0].startswith( "neighborpw" ):
          self.build_list_to_check( self.key, self.value, self.l2vpn_neighborpw_to_check )
          continue
        if self.key.startswith( "acgroup" ):
          self.build_list_to_check( self.key, self.value, self.l2vpn_acgroup_to_check )
          continue
        if self.key.startswith( "pwgroup" ):
          self.build_list_to_check( self.key, self.value, self.l2vpn_pwgroup_to_check )
          continue
    except:
      raise CriticalFailure( "AnalysisCustomProcessor: Invalid seed file!" )
    #--------------------------------------------------------------------------------------------------------------
    self.line_length = 0
    try:
      L2VpnXconnectReceiveDataParcer().l2vpn_xconnect_receive_data_parcer( self.device,
                                                                           self.reportFD,
                                                                           self.l2vpn_xconnect_received,
                                                                           self.l2vpn_xconnects_received
                                                                         )
    except Exception as error:
      raise CriticalFailure( error )
    self.line_index = 0
    self.line_index_tail = 0
    for self.key_value_str_received in self.l2vpn_xconnects_received:
      try:
        self.key_values_received = ast.literal_eval( self.key_value_str_received )
      except Exception as error:
        raise CriticalFailure( error )
      if self.key_values_received["group"].startswith( self.l2vpn_group_to_check ):
        if not self.key_values_received["xconnect"].startswith( self.l2vpn_xconnect_to_check ):
          continue # Skip there could be multiple XC-Group associations
        if not self.key_values_received["state"].startswith( self.l2vpn_group_state_to_check ):
          self.data_match_results = "Failed"
          self.l2vpn_print_report( self.data_match_results,
                                   "Group state: {} Detected: {} ".
                                   format( self.l2vpn_group_state_to_check, self.key_values_received["state"] ),
                                   self.line_index, self.line_index_tail )
          break
        if not self.key_values_received["interwork"].startswith( self.l2vpn_group_interwork_to_check ):
          self.data_match_results = "Failed"
          self.l2vpn_print_report( self.data_match_results,
                                   "Group: {} "
                                   "Internetwork: {} Detected: {} ".
                                   format( self.l2vpn_group_to_check,
                                           self.l2vpn_group_interwork_to_check,
                                           self.key_values_received["interwork"] ),
                                   self.line_index, self.line_index_tail )
          break
        for self.intf_key_value_to_check in self.l2vpn_intfac_to_check:
          self.l2vpn_interface_to_check = dict( ast.literal_eval( self.intf_key_value_to_check ) )["intf"]
          self.l2vpn_state_to_check = dict( ast.literal_eval( self.intf_key_value_to_check ) )["{} state".
               format(dict( ast.literal_eval( self.intf_key_value_to_check ) )["intf"])]
          try:
            self.l2vpn_state_received = self.key_values_received["intf {}".format( self.l2vpn_interface_to_check )]
          except:
            self.data_match_results = "Failed"
            self.l2vpn_print_report( self.data_match_results,
                                     "Group: {} "
                                     "Interface: {} NOT Detected ".
                                     format( self.l2vpn_group_to_check,
                                             self.l2vpn_interface_to_check ),
                                     self.line_index, self.line_index_tail )
            break
          if self.l2vpn_state_to_check.startswith( self.l2vpn_state_received["state"] ):
            self.data_match_results = "Passed"
            continue
          else:
            self.data_match_results = "Failed"
            self.l2vpn_print_report( self.data_match_results,
                                     "Group: {} "
                                     "Interface State: {} Detected: {} ".
                                     format( self.l2vpn_group_to_check,
                                             self.l2vpn_state_to_check,
                                             self.l2vpn_state_received["state"] ),
                                     self.line_index, self.line_index_tail )
            break
        #-----------------------------------------------------------------------------------------------------------
        # AC Group
        #-----------------------------------------------------------------------------------------------------------
        for self.intf_key_value_to_check in self.l2vpn_acgroup_to_check:
          self.acgroup_id = dict( ast.literal_eval( self.intf_key_value_to_check ) )["acgroup"]
          self.vpivci_to_check = \
               dict( ast.literal_eval( self.intf_key_value_to_check ) )["{} vpi/vci".format( self.acgroup_id )]
          self.number_ranges_to_check = \
               dict( ast.literal_eval( self.intf_key_value_to_check ) )["{} number ranges".format( self.acgroup_id )]
          try:
            self.vlan_ranges_to_check = \
              dict( ast.literal_eval( self.intf_key_value_to_check ) )["{} vlan ranges".format( self.acgroup_id )]
          except:
            self.vlan_ranges_to_check = ""
          self.mtu_to_check = \
               dict( ast.literal_eval( self.intf_key_value_to_check ) )["{} mtu".format( self.acgroup_id )]
          self.xcid_to_check = \
               dict( ast.literal_eval( self.intf_key_value_to_check ) )["{} xc id".format( self.acgroup_id )]
          self.internetwork_to_check = \
               dict( ast.literal_eval( self.intf_key_value_to_check ) )["{} internetwork".format( self.acgroup_id )]
          self.packetsreceived_to_check = \
               dict( ast.literal_eval( self.intf_key_value_to_check ) )["{} packets received".format( self.acgroup_id )]
          self.packetssent_to_check = \
               dict( ast.literal_eval( self.intf_key_value_to_check ) )["{} packets sent".format( self.acgroup_id )]
          self.bytesreceived_to_check = \
               dict( ast.literal_eval( self.intf_key_value_to_check ) )["{} bytes received".format( self.acgroup_id )]
          self.bytessent_to_check = \
               dict( ast.literal_eval( self.intf_key_value_to_check ) )["{} bytes sent".format( self.acgroup_id )]
          #---------------------------------------------------------------------------------------------------------
          self.acgroup_id_rcv = "acgroup "
          for self.key in self.key_values_received:
            if self.key.startswith( "intf" ):
              self.acgroup_id_rcv += self.key.split()[1]
              break
          #---------------------------------------------------------------------------------------------------------
          try:
            self.acgroup_rcv = self.key_values_received[self.acgroup_id_rcv]
          except:
            self.data_match_results = "Failed"
            self.l2vpn_print_report( self.data_match_results, self.acgroup_id_rcv,
                                     self.line_index, self.line_index_tail )
            break
          if not self.xcid_to_check and self.acgroup_rcv["xc id"] or \
             self.xcid_to_check and not self.acgroup_rcv["xc id"]:
            self.data_match_results = "Failed"
            self.l2vpn_print_report( self.data_match_results,
                                     "Group: {} "
                                     "AC XC: {} Detected: {} ".
                                     format( self.l2vpn_group_to_check,
                                             self.xcid_to_check,
                                             self.acgroup_rcv["xc id"] ),
                                     self.line_index, self.line_index_tail )
            break
          if int( self.packetsreceived_to_check ) > int( self.acgroup_rcv["packets received"] ) or \
             int( self.packetssent_to_check ) > int( self.acgroup_rcv["packets sent"] ) or \
             int( self.bytesreceived_to_check ) > int( self.acgroup_rcv["bytes received"] ) or \
             int( self.bytessent_to_check ) > int( self.acgroup_rcv["bytes sent"] ):
            self.data_match_results = "Failed"
            self.l2vpn_print_report( self.data_match_results,
                                     "Group: {} "
                                     "Packets Received: {} Detected: {} "
                                     "Packets Sent: {} Detected: {} "
                                     "Bytes Received: {} Detected: {} "
                                     "Bytes Sent: {} Detected: {} ".
                                     format( self.l2vpn_group_to_check,
                                             self.packetsreceived_to_check,
                                             self.acgroup_rcv["packets received"],
                                             self.packetssent_to_check,
                                             self.acgroup_rcv["packets sent"],
                                             self.bytesreceived_to_check,
                                             self.acgroup_rcv["bytes received"],
                                             self.bytessent_to_check,
                                             self.acgroup_rcv["bytes sent"] ),
                                     self.line_index, self.line_index_tail )
            break
          if self.vpivci_to_check and not self.acgroup_rcv["vpi/vci"] or \
             not self.vpivci_to_check and self.acgroup_rcv["vpi/vci"] or \
             self.number_ranges_to_check and not self.acgroup_rcv["number ranges"] and \
             not self.number_ranges_to_check and self.acgroup_rcv["number ranges"] or \
             self.vlan_ranges_to_check and not self.acgroup_rcv["vlan ranges"] and \
             not self.vlan_ranges_to_check and self.acgroup_rcv["vlan ranges"] or \
             not self.internetwork_to_check == self.acgroup_rcv["internetwork"]:
            self.data_match_results = "Failed"
            self.l2vpn_print_report( self.data_match_results,
                                     "Group: {} "
                                     "AC VPI/VCI: {} Detected: {} "
                                     "AC # Range: {} Detected: {} "
                                     "AC VLAN Range: {} Detected: {} "
                                     "AC Internetwork: {} Detected: {} ".
                                     format( self.l2vpn_group_to_check,
                                             self.vpivci_to_check,
                                             self.acgroup_rcv["vpi/vci"],
                                             self.number_ranges_to_check,
                                             self.acgroup_rcv["number ranges"],
                                             self.vlan_ranges_to_check,
                                             self.acgroup_rcv["vlan ranges"],
                                             self.internetwork_to_check,
                                             self.acgroup_rcv["internetwork"]),
                                     self.line_index, self.line_index_tail )
            break
          if int( self.mtu_to_check ) > 0:
            if int( self.acgroup_rcv["mtu"] ) == 0:
              self.data_match_results = "Failed"
              self.l2vpn_print_report( self.data_match_results,
                                       "Group: {} "
                                       "AC MTU: {} Detected: {} ".
                                       format( self.l2vpn_group_to_check,
                                               self.mtu_to_check,
                                               self.acgroup_rcv["mtu"]),
                                       self.line_index, self.line_index_tail )
              break
        #-----------------------------------------------------------------------------------------------------------
        # Neighbor PW
        #-----------------------------------------------------------------------------------------------------------
        for self.intf_key_value_to_check in self.l2vpn_neighborpw_to_check:
          self.neighborpw_id = dict( ast.literal_eval( self.intf_key_value_to_check ) )["neighborpw"]
          self.id_to_check = \
            dict( ast.literal_eval( self.intf_key_value_to_check ) )["{} id".format( self.neighborpw_id )]
          self.state_to_check = \
            dict( ast.literal_eval( self.intf_key_value_to_check ) )["{} state".format( self.neighborpw_id )]
          self.mode_to_check = \
            dict( ast.literal_eval( self.intf_key_value_to_check ) )["{} mode".format( self.neighborpw_id )]
          # ---------------------------------------------------------------------------------------------------------
          self.neighborpw_id_rcv = "neighborpw "
          for self.key in self.key_values_received:
            if self.key.startswith( "neighborpw" ):
              self.neighborpw_id_rcv += self.key.split()[1]
              break
          # ---------------------------------------------------------------------------------------------------------
          try:
            self.neighborpw_rcv = self.key_values_received[self.neighborpw_id_rcv]
          except:
            self.data_match_results = "Failed"
            self.l2vpn_print_report( self.data_match_results,
                                     "PW: {}".
                                     format( self.neighborpw_id_rcv ),
                                     self.line_index, self.line_index_tail )
            break
          if not self.id_to_check == self.neighborpw_rcv["id"] or \
              not self.state_to_check == self.neighborpw_rcv["state"] or \
              not self.mode_to_check == self.neighborpw_rcv["mode"]:
            self.data_match_results = "Failed"
            self.l2vpn_print_report( self.data_match_results,
                                     "Group: {} "
                                     "Neighbor ID: {} Detected: {} "
                                     "Neighbor State: {} Detected: {} "
                                     "Neighbor Mode: {} Detected: {} ".
                                     format( self.l2vpn_group_to_check,
                                             self.id_to_check,
                                             self.neighborpw_rcv["id"],
                                             self.state_to_check,
                                             self.neighborpw_rcv["state"],
                                             self.mode_to_check,
                                             self.neighborpw_rcv["mode"]),
                                     self.line_index, self.line_index_tail )
            break
        #---------------------------------------------------------------------------------------------------------
        # PW Group
        #-----------------------------------------------------------------------------------------------------------
        for self.intf_key_value_to_check in self.l2vpn_pwgroup_to_check:
          self.pwgroup_id = dict( ast.literal_eval( self.intf_key_value_to_check ) )["pwgroup"]
          self.protocol_to_check = \
            dict( ast.literal_eval( self.intf_key_value_to_check ) )["{} protocol".format( self.pwgroup_id )]
          self.encapsulation_to_check = \
            dict( ast.literal_eval( self.intf_key_value_to_check ) )["{} encapsulation".format( self.pwgroup_id )]
          self.class_to_check = \
            dict( ast.literal_eval( self.intf_key_value_to_check ) )["{} class".format( self.pwgroup_id )]
          self.type_to_check = \
            dict( ast.literal_eval( self.intf_key_value_to_check ) )["{} type".format( self.pwgroup_id )]
          self.sourceaddress_to_check = \
            dict( ast.literal_eval( self.intf_key_value_to_check ) )["{} source address".format( self.pwgroup_id )]
          self.mtu_to_check = \
            dict( ast.literal_eval( self.intf_key_value_to_check ) )["{} mtu".format( self.pwgroup_id )]
          self.xcid_to_check = \
            dict( ast.literal_eval( self.intf_key_value_to_check ) )["{} xc id".format( self.pwgroup_id )]
          self.controlword_to_check = \
            dict( ast.literal_eval( self.intf_key_value_to_check ) )["{} control word".format( self.pwgroup_id )]
          self.interworking_to_check = \
            dict( ast.literal_eval( self.intf_key_value_to_check ) )["{} interworking".format( self.pwgroup_id )]
          self.backup_to_check = \
            dict( ast.literal_eval( self.intf_key_value_to_check ) )["{} backup".format( self.pwgroup_id )]
          self.delay_to_check = \
            dict( ast.literal_eval( self.intf_key_value_to_check ) )["{} delay".format( self.pwgroup_id )]
          self.sequence_to_check = \
            dict( ast.literal_eval( self.intf_key_value_to_check ) )["{} sequence".format( self.pwgroup_id )]
          #------------------------------------------------------------------------------------------------------
          # YET AGAIN!!! Anothere Cisco example of HORRIBLE!!! quality control they are a$$-h0les!!!!
          try:
            self.status_to_check = \
              dict( ast.literal_eval( self.intf_key_value_to_check ) )["{} status".format( self.pwgroup_id )]
          except:
            self.status_to_check = ""
          self.label_to_check = \
            dict( ast.literal_eval( self.intf_key_value_to_check ) )["{} label".format( self.pwgroup_id )]
          self.groupid_to_check = \
            dict( ast.literal_eval( self.intf_key_value_to_check ) )["{} group id".format( self.pwgroup_id )]
          self.interface_to_check = \
            dict( ast.literal_eval( self.intf_key_value_to_check ) )["{} interface".format( self.pwgroup_id )]
          self.statuscontrolword_to_check = \
            dict( ast.literal_eval( self.intf_key_value_to_check ) )["{} status control word".format( self.pwgroup_id )]
          self.pwtype_to_check = \
            dict( ast.literal_eval( self.intf_key_value_to_check ) )["{} pw type".format( self.pwgroup_id )]
          self.vccvCVtype_to_check = \
            dict( ast.literal_eval( self.intf_key_value_to_check ) )["{} vccv CV type".format( self.pwgroup_id )]
          self.vccvCCtype_to_check = \
            dict( ast.literal_eval( self.intf_key_value_to_check ) )["{} vccv CC type".format( self.pwgroup_id )]
          self.packetsreceived_to_check = \
            dict( ast.literal_eval( self.intf_key_value_to_check ) )["{} packets received".format( self.pwgroup_id )]
          self.packetssent_to_check = \
            dict( ast.literal_eval( self.intf_key_value_to_check ) )["{} packets sent".format( self.pwgroup_id )]
          self.bytesreceived_to_check = \
            dict( ast.literal_eval( self.intf_key_value_to_check ) )["{} bytes received".format( self.pwgroup_id )]
          self.bytessent_to_check = \
            dict( ast.literal_eval( self.intf_key_value_to_check ) )["{} bytes sent".format( self.pwgroup_id )]
          #---------------------------------------------------------------------------------------------------------
          self.pwgroup_id_rcv = "pwgroup "
          for self.key in self.key_values_received:
            if self.key.startswith( "pwgroup" ):
              self.pwgroup_id_rcv += self.key.split()[1]
              break
          #---------------------------------------------------------------------------------------------------------
          try:
            self.pwgroup_rcv = self.key_values_received[self.pwgroup_id_rcv]
          except:
            self.data_match_results = "Failed"
            self.l2vpn_print_report( self.data_match_results, "PW Group Error with : {} ".
                                     format( self.pwgroup_id_rcv ),
                                     self.line_index, self.line_index_tail )
            break
          if not self.xcid_to_check and self.pwgroup_rcv["xc id"] or \
             self.xcid_to_check and not self.pwgroup_rcv["xc id"] or \
             not self.groupid_to_check and self.pwgroup_rcv["group id"] or \
             self.groupid_to_check and not self.pwgroup_rcv["group id"] or \
             not self.label_to_check and self.pwgroup_rcv["label"] or \
             self.label_to_check and not self.pwgroup_rcv["label"]:
            self.data_match_results = "Failed"
            self.l2vpn_print_report( self.data_match_results,
                                     "Group: {} "
                                     "PW XC ID: {} Detected: {} "
                                     "PW Group ID: {} Detected: {} "
                                     "Label: {} Detected: {} ".
                                     format( self.l2vpn_group_to_check,
                                             self.xcid_to_check,
                                             self.pwgroup_rcv["xc id"],
                                             self.groupid_to_check,
                                             self.pwgroup_rcv["group id"],
                                             self.label_to_check,
                                             self.pwgroup_rcv["label"] ),
                                     self.line_index, self.line_index_tail )
            break
          if int( self.packetsreceived_to_check ) > int( self.pwgroup_rcv["packets received"] ) or \
                  int( self.packetsreceived_to_check ) > int( self.pwgroup_rcv["packets sent"] ) or \
                  int( self.packetsreceived_to_check ) > int( self.pwgroup_rcv["bytes received"] ) or \
                  int( self.packetsreceived_to_check ) > int( self.pwgroup_rcv["bytes sent"] ):
            self.data_match_results = "Failed"
            self.l2vpn_print_report( self.data_match_results,
                                     "Group: {} "
                                     "Packets Received: {} Detected: {} "
                                     "Packets Sent: {} Detected: {} "
                                     "Bytes Received: {} Detected: {} "
                                     "Bytes Sent: {} Detected: {} ".
                                     format( self.l2vpn_group_to_check,
                                             self.packetsreceived_to_check,
                                             self.pwgroup_rcv["packets received"],
                                             self.packetssent_to_check,
                                             self.pwgroup_rcv["packets sent"],
                                             self.bytesreceived_to_check,
                                             self.pwgroup_rcv["bytes received"],
                                             self.bytessent_to_check,
                                             self.pwgroup_rcv["bytes sent"] ),
                                     self.line_index, self.line_index_tail )
            break
          #------------------------------------------------------------------------------------------------------
          # As stated before CISCO quality control SUCK!!!! ergo this dependency is required A$$-WHIPES!!!!
          if self.status_to_check and \
             not self.status_to_check == self.pwgroup_rcv["status"]:
            self.data_match_results = "Failed"
            self.l2vpn_print_report( self.data_match_results,
                                     "Group: {} Xconnect {} "
                                     "PW Status: {} Detected: {} ".
                                     format( self.l2vpn_group_to_check,
                                             self.l2vpn_xconnect_to_check,
                                             self.status_to_check,
                                             self.pwgroup_rcv["status"]),
                                     self.line_index, self.line_index_tail )
            break
          if self.vccvCVtype_to_check and not self.pwgroup_rcv["vccv CV type"] or \
             not self.vccvCVtype_to_check and self.pwgroup_rcv["vccv CV type"] or \
             self.vccvCCtype_to_check and not self.pwgroup_rcv["vccv CC type"] or \
             not self.vccvCCtype_to_check and self.pwgroup_rcv["vccv CC type"]:
            self.data_match_results = "Failed"
            self.l2vpn_print_report( self.data_match_results,
                                     "Group: {} Xconnect {} "
                                     "CV: {} Detected: {} "
                                     "CC: {} Detected: {} ".
                                     format( self.l2vpn_group_to_check,
                                             self.l2vpn_xconnect_to_check,
                                             self.vccvCVtype_to_check,
                                             self.pwgroup_rcv["vccv CV type"],
                                             self.vccvCCtype_to_check,
                                             self.pwgroup_rcv["vccv CC type"] ),
                                     self.line_index, self.line_index_tail )
            break
          if not self.class_to_check == self.pwgroup_rcv["class"] or \
              not self.encapsulation_to_check == self.pwgroup_rcv["encapsulation"] or \
              not self.interworking_to_check == self.pwgroup_rcv["interworking"] or \
              not self.protocol_to_check == self.pwgroup_rcv["protocol"] or \
              not self.sourceaddress_to_check == self.pwgroup_rcv["source address"] or \
              not self.type_to_check == self.pwgroup_rcv["type"] or \
              not self.controlword_to_check == self.pwgroup_rcv["control word"] or \
              not self.backup_to_check == self.pwgroup_rcv["backup"] or \
              not self.delay_to_check == self.pwgroup_rcv["delay"] or \
              not self.sequence_to_check == self.pwgroup_rcv["sequence"] or \
              not self.interface_to_check == self.pwgroup_rcv["interface"] or \
              not self.statuscontrolword_to_check == self.pwgroup_rcv["status control word"] or \
              not self.pwtype_to_check == self.pwgroup_rcv["pw type"] or \
              not self.mtu_to_check == self.pwgroup_rcv["mtu"]:
            self.data_match_results = "Failed"
            self.l2vpn_print_report( self.data_match_results,
                                     "Group: {} Xconnect {} "
                                     "Class: {} Detected: {} "
                                     "Encapsulation: {} Detected: {} "
                                     "Internetworking: {} Detected: {} "
                                     "Protocol: {} Detected: {} "
                                     "Source Address: {} Detected: {} "
                                     "Type: {} Detected: {} "
                                     "Control Word: {} Detected: {} "
                                     "Backup: {} Detected: {} "
                                     "Delay: {} Detected: {} "
                                     "Sequence: {} Detected: {} "
                                     "Interface: {} Detected: {} "
                                     "Status Ctl Word: {} Detected: {} "
                                     "PW Type: {} Detected: {} "
                                     "MTU: {} Detected: {} ".
                                     format( self.l2vpn_group_to_check,
                                             self.l2vpn_xconnect_to_check,
                                             self.class_to_check,
                                             self.pwgroup_rcv["class"],
                                             self.encapsulation_to_check,
                                             self.pwgroup_rcv["encapsulation"],
                                             self.interworking_to_check,
                                             self.pwgroup_rcv["interworking"],
                                             self.protocol_to_check,
                                             self.pwgroup_rcv["protocol"],
                                             self.sourceaddress_to_check,
                                             self.pwgroup_rcv["source address"],
                                             self.type_to_check,
                                             self.pwgroup_rcv["type"],
                                             self.controlword_to_check,
                                             self.pwgroup_rcv["control word"],
                                             self.backup_to_check,
                                             self.pwgroup_rcv["backup"],
                                             self.delay_to_check,
                                             self.pwgroup_rcv["delay"],
                                             self.sequence_to_check,
                                             self.pwgroup_rcv["sequence"],
                                             self.interface_to_check,
                                             self.pwgroup_rcv["interface"],
                                             self.statuscontrolword_to_check,
                                             self.pwgroup_rcv["status control word"],
                                             self.pwtype_to_check,
                                             self.pwgroup_rcv["pw type"],
                                             self.mtu_to_check,
                                             self.pwgroup_rcv["mtu"] ),
                                     self.line_index, self.line_index_tail )
            break
        #-----------------------------------------------------------------------------------------------------------
        # All tests have passed report the results!
        #-----------------------------------------------------------------------------------------------------------
        if self.data_match_results == "Passed":
          self.l2vpn_print_report( self.data_match_results,
                                   "Group: {} ".format( self.l2vpn_group_to_check ),
                                   self.line_index, self.line_index_tail )
        return()
      else:  # Look at next group received to see if its the one we want
        continue
    else:
      self.data_match_results = "Failed"
      self.l2vpn_print_report( self.data_match_results,
                               "ERROR RETRIEVING L2VPN XCONNECT DATA!",
                               self.line_index, self.line_index_tail )
    return()
  #----------------------------------------------------------------------------------------------------------------
  def l2vpn_print_report( self, data_match_results, error, line_index, line_index_tail ):
    self.data_match_results = data_match_results
    self.error = error
    self.is_search_item.set_test_results_string( "{}".
                                                 format( self.error ),
                                                 self.testcase_name,
                                                 self.data_match_results,
                                                 "{}".format( self.command_issued_str ),
                                                 "{}".format( self.analysis_data_filename ),
                                                 str( line_index ),
                                                 str( line_index_tail ) )
    return()
  #----------------------------------------------------------------------------------------------------------------
  def build_list_to_check( self, key, value, list_to_build ):
    self.list_to_build = list_to_build
    self.build_list_str = "(\"{}\",\"{}\"),".format( key.split()[0], key.split()[1] )
    for self.subkey, self.subvalue in value:
      self.build_list_str += "(\"{} {}\",\"{}\"),".format( key.split()[1],
                                                           self.subkey,
                                                           self.subvalue )
    self.list_to_build.append( self.build_list_str[:-1] )
    return( self.list_to_build )
  #----------------------------------------------------------------------------------------------------------------
  #----------------------------------------------------------------------------------------------------------------
  def juniper_l2vpn_xconnect_detail_analysis( self, seed_logical_dict, reportFD ):
    self.reportFD = reportFD
    self.seed_logical_dict = seed_logical_dict
    #--------------------------------------------------------------------------------------------------------------
    return (self.reportFD)
    #--------------------------------------------------------------------------------------------------------------
#####################################################################################################################