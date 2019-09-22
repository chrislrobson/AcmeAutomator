"""
FILE: ShowInterfaceDetailSeedAnalysisFileBuilder
CLASS:  ShowInterfacesDetailSeedAnalysisFileBuilder
Author: Christopher Robson
Copyright by:  Christopher Robson
Copyright date: 01Jan2016
This software is not FREE!  Use or destribution of the software system and its
subsystem modules, libraries, configuration file and "seed" file without the
express permission of the author is strictly PROHIBITED!
FUNCTION:  Module builds a seed file for analysizing collected data.
"""
"""
LIBRARIES:  Python libraries
"""
import datetime
import os, sys, stat
from collections import OrderedDict
import ast
"""
LIBRARIES:  Testbed Tester specific libraries
"""
from Globals import *
from Exceptions import *
from SeedDictionary import SeedCommandDictionaryProcessor,\
                                                                SeedCommandlinePreprocessor
from DecodeDataProcessor import DecoderInfo
from Decoder import __str__
"""
CLASS: ShowInterfacesDetailSeedAnalysisFileBuilder:
DESCRIPTION: Create "show interface detail" Analysis Edit data
INPUT: "show interface detail" captured data
OUTPUT: "EditAnalysisSeedFile" input data
"""
class ShowInterfacesDetailSeedAnalysisFileBuilder:
  "Show Interface Detail Seed Analysis File Builder"
  """----------------------------------------------------------------------------"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.seed = parent.seed
    self.gparent = parent.parent.parent.parent
    self.filename_time_extension = self.parent.filename_time_extension
    self.cmd_list = parent.cmd_list
    self.with_line_numbers = "No"
    self.debug = False
    self.detail_interfaces_detail_analysis_filename = ""
    self.detail_interfaces_detail_data_filename = ""
    self.detail_interfaces_detail_analysis_fd = None
    self.detail_data_fd = None
    self.start_analysis_flag = False
    self.show_interfaces_detail_table = []
    self.interfaces_to_match = ""
    self.decoder_utility = self.parent.parent.parent.decoder_class
    # FIXME remove all the below during cleanup
    self.line_index = 0
    """
    Establish the instances of the decoder that will be processing this data
    """
    self.decoder_instance = DecoderInfo()
    self.decoder_instance.decoder_utility = self.decoder_utility
    self.decoder_instance.decoded_data = OrderedDict()
  """
  CLASS: execute:
  DESCRIPTION: Create "show interface detail" Analysis Edit data entry point.
               Determines input data to process and passes this data onto processing methods.
  INPUT: "show interface detail" captured data
  OUTPUT: "EditAnalysisSeedFile" input data
  """
  def execute( self ):
    self.results = ""
    self.received_data = ""
    self.interfaces_to_match = self.cmd_list[SeedCommandDictionaryProcessor.interfaces]
    if self.interfaces_to_match == "":
      raise Exception( "ShowInterfacesDetailSeedAnalysisFileBuilder "
                       "error INTERFACE match list is empty."
                     )
    if self.cmd_list[SeedCommandDictionaryProcessor.verbose] == 'Yes':
      self.message_str = \
        "Build Show Interfaces Detail Seed File command started at: {}.".\
          format( datetime.datetime.now().strftime( "%d%b%Y-%H%M-%S" ) )
      self.gparent.logger_message_signal.emit(self.message_str)
    self.message_str = "Building seed file: {}.".\
          format( self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] )
    self.gparent.logger_message_signal.emit( self.message_str )
    try:
      self.analysis_filename = str( self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] )
      self.detail_interfaces_detail_analysis_fd = open( self.analysis_filename, "w+" )
    except:
      raise Exception( "{}: ShowInterfacesDetailSeedAnalysisFileBuilder file I/O error with \"{}\". "
                       "Build Show Interface Detail Seed File Command terminated. ".
                       format( self.name,
                               self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] )  )
    self.data_filename = self.cmd_list[SeedCommandDictionaryProcessor.commandpath] + \
                         self.cmd_list[SeedCommandDictionaryProcessor.commands] + \
                         self.filename_time_extension
    self.device = self.cmd_list[SeedCommandDictionaryProcessor.device]
    if self.device == "":
      raise CriticalFailure( "ShowInterfacesDetailSeedAnalysisFileBuilder: Invalid seed file!" )
    try:
      with open( self.data_filename, "r" ) as self.detail_data_fd:
        # FIXME remove all the below during cleanup
        self.line_index = 0
        # FIXME remove above
        for self.detail_data in self.detail_data_fd:
          """
          Skip comments and line beginning with carriage returns or
          process the special script control keyword string
          """
          if self.detail_data.startswith( "\n" ) or self.detail_data.startswith( "#" ):
            if self.detail_data.startswith( "#@@!!" ):
              # FIXME TOBE DONE MAYBE A FORLOOP here
              pass
            self.decoder_instance.previous_index = self.decoder_instance.current_index
            self.decoder_instance.current_index += len( self.detail_data )
            # FIXME remove all the below during cleanup
            self.line_index += len( self.detail_data )
            # FIXME remove above
            continue
          """
          Before doing nay processing find the command issued 
          which indicates data is to follow
          """
          if self.detail_data.startswith( "DUT(" ) and \
                  self.detail_data.find( ")-> show interfaces" ) != -1:
            self.start_analysis_flag = True
            self.decoder_instance.previous_index = self.decoder_instance.current_index
            self.decoder_instance.current_index += len( self.detail_data )
            # FIXME remove all the below during cleanup
            self.line_index += len( self.detail_data )
            # FIXME remove above
            continue
          """
          Check for first line.  By doing this the data file can contain
          more than one command output data.
          Juniper data string to match: "Physical interface"
          Cisco data string to match: ", line protocol is" 
          """
          if self.start_analysis_flag and \
             self.detail_data.startswith( "Physical interface:" ) or \
             self.detail_data.find( ", line protocol is" ) != -1:
            self.detail_data_fd.seek( self.decoder_instance.current_index )
            if self.device == "juniper":
              try:
                self.reportFD = self.build_juniper_analysis_seed_file()
              except Exception as error:
                self.message_str = "Building seed file error: {}.".format( error )
                self.gparent.logger_message_signal.emit( self.message_str )
                self.detail_interfaces_detail_analysis_fd.close()
                self.detail_data_fd.close()
                raise Exception( error )
              self.detail_interfaces_detail_analysis_fd.close()
              self.detail_data_fd.close()
              break
            if self.start_analysis_flag and self.device == "cisco":
              try:
                self.reportFD = self.build_cisco_analysis_seed_file()
              except Exception as error:
                self.message_str = "Building seed file error: {}.".format( error )
                self.gparent.logger_message_signal.emit( self.message_str )
                self.detail_interfaces_detail_analysis_fd.close()
                self.detail_data_fd.close()
                raise Exception( error )
              self.detail_interfaces_detail_analysis_fd.close()
              self.detail_data_fd.close()
              break
          else:
            self.decoder_instance.previous_index = self.decoder_instance.current_index
            self.decoder_instance.current_index += len( self.detail_data )
            self.line_index += len( self.detail_data )
            continue
        else:
          if self.cmd_list[SeedCommandDictionaryProcessor.verbose] == 'Yes':
            self.message_str = "No interface data found."
            self.gparent.logger_message_signal.emit(self.message_str)
    except Exception as e:
      raise Exception( "ShowInterfacesDetailSeedAnalysisFileBuilder: {}".format(e) )
    return()
  # FIXME
  # FIXME more places oop'ing these two methods below would be a good idea, aka, factories maybe or importlib's
  # FIXME
  """
  METHOD: build_cisco_analysis_seed_file( self ):
  DESCRIPTION: Create "show interface detail" Analysis Edit data
  INPUT: CISCO "show interface detail" captured data
  OUTPUT: "EditAnalysisSeedFile" input data
  """
  def build_cisco_analysis_seed_file( self ):
    self.start_processing_details_flag = False
    for self.detail_data in self.detail_data_fd:
      if self.detail_data.startswith( "\n" ):
        continue
      try:
        self.detail_data_list = self.detail_data.split()
      except:
        continue
      if not self.detail_data.startswith( " " ):
        if self.interfaces_to_match != "" and not self.start_processing_details_flag:
          for self.intf in self.interfaces_to_match.split():
            if self.detail_data_list[0].startswith( self.intf ):
              self.interface_received = self.detail_data_list[0]
              self.interface_received = self.interface_received.replace( ":", "~" )
              self.interface_admin_state_received = self.detail_data_list[2].split( "," )[0]
              self.interface_line_protocol_state_received = self.detail_data_list[6]
              self.start_processing_details_flag = True
              break
          else:
            # print(self.detail_data.split()[0])
            continue
        else:
          continue
      # FIXME
      # FIXME YET ANOTHER OOP CANIDATE !!!
      # FIXME
      if self.start_processing_details_flag:
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
        self.number_of_bundled_interfaces_received = ""
        self.bundled_interfaces_received = ""
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
        """
        Process the "show interface detail data by reading the input data and
        initialize specific data according to flag settings
        """
        if self.cmd_list[SeedCommandDictionaryProcessor.initializedata] == 'No' or \
           self.cmd_list[SeedCommandDictionaryProcessor.initializedata] == 'AllCounters' :
          for self.detail_data_str in self.detail_data_fd:
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
                      self.hardware_address_received = self.detail_data_list[4]
                  except:
                    pass
                continue
              if self.detail_data.startswith( "Layer" ):
                self.layer_received = self.detail_data_list[1]
                continue
              if self.detail_data.startswith( "Description" ):
                self.description_received = " ".join( self.detail_data.split()[1:] ).replace( "\"", "" )
                self.description_received = self.description_received.replace( ":", "~" )
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
                self.arp_timeout_received = self.detail_data_list[5].replace( ":", "~" )
                continue
              if self.detail_data.find( "No. of members in this bundle:" ) != -1:
                self.number_of_bundled_interfaces_received = self.detail_data_list[6]
                self.counter = int( self.number_of_bundled_interfaces_received  )
                for self.intf_count in range( self.counter ):
                  for self.detail_data in self.detail_data_fd:
                    self.bundled_interfaces_received += "\"bundle {}\":".format( self.intf_count + 1 )
                    self.bundled_interfaces_received += "{"
                    self.a, self.b, self.c, self.d = self.detail_data.split()
                    self.bundled_interfaces_received += "\"interface\":\"{}\",".format( self.a )
                    self.bundled_interfaces_received += "\"duplex\":\"{}\",".format( self.b )
                    self.bundled_interfaces_received += "\"bits/ps\":\"{}\",".format( self.c )
                    self.bundled_interfaces_received += "\"mode\":\"{}\"".format( self.d )
                    self.bundled_interfaces_received += "},"
                    break
                continue
              if self.detail_data.startswith( "Input/output data rate is" ):
                self.input_output_data_rate_received = self.detail_data_list[4].split( "." )[0]
                continue
              if self.detail_data.startswith( "Last input" ):
                self.last_input_time_received = self.detail_data_list[2].split( "," )[0].replace( ":", "~" )
                self.last_output_time_received = self.detail_data_list[4].replace( ":", "~" )
                continue
              if self.detail_data.startswith( "Last clearing" ):
                self.last_clear_received = self.detail_data_list[6].replace( ":", "~" )
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
        Initialize specific data according to flag settings
        then create the seed file used by the Analysis Engine
        """
        if self.cmd_list[SeedCommandDictionaryProcessor.initializedata] == 'AllCounters':
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
          """
          Use the collected data and initialize values to
          create the Analysis Engine seed file dictionary KEY:VALUE
          """
          self.show_interfaces_detail_table.append(
               "{" + \
                 "\"show interfaces detail\":\"show interfaces detail\"," \
                 "\"device\":\"cisco\"," \
                 "\"interface\":\"{}\"," \
                 "\"admin state\":\"{}\"," \
                 "\"line protocol\":\"{}\"," \
                 "\"state transitions\":\"{}\"," \
                 "\"hardware\":\"{}\"," \
                 "\"hardware address\":\"{}\"," \
                 "\"hardware address bia\":\"{}\"," \
                 "\"layer\":\"{}\"," \
                 "\"description\":\"{}\"," \
                 "\"internet address\":\"{}\"," \
                 "\"mtu\":\"{}\"," \
                 "\"bandwidth\":\"{}\"," \
                 "\"reliability\":\"{}\"," \
                 "\"transmit load\":\"{}\"," \
                 "\"receive load\":\"{}\"," \
                 "\"encaps\":\"{}\"," \
                 "\"duplex\":\"{}\"," \
                 "\"bit per sec\":\"{}\"," \
                 "\"link type\":\"{}\"," \
                 "\"output flow control\":\"{}\"," \
                 "\"input flow control\":\"{}\"," \
                 "\"carrier delay state\":\"{}\"," \
                 "\"loopback state\":\"{}\"," \
                 "\"flapped\":\"{}\"," \
                 "\"arp type\":\"{}\"," \
                 "\"arp timeout\":\"{}\"," \
                 "\"number of bundled interfaces\":\"{}\"," \
                 "{}" \
                 "\"input output data rate\":\"{}\"," \
                 "\"last input time\":\"{}\"," \
                 "\"last output time\":\"{}\"," \
                 "\"last clear\":\"{}\"," \
                 "\"input rate\":\"{}\"," \
                 "\"input packet rate\":\"{}\"," \
                 "\"output rate\":\"{}\"," \
                 "\"output packet rate\":\"{}\"," \
                 "\"input packets\":\"{}\"," \
                 "\"input bytes\":\"{}\"," \
                 "\"input drops\":\"{}\"," \
                 "\"up level protocol drops\":\"{}\"," \
                 "\"input broadcast packets\":\"{}\"," \
                 "\"input multicast packets\":\"{}\"," \
                 "\"input errors\":\"{}\"," \
                 "\"input crc\":\"{}\"," \
                 "\"input frame\":\"{}\"," \
                 "\"input overrun\":\"{}\"," \
                 "\"input ignore\":\"{}\"," \
                 "\"input abort\":\"{}\"," \
                 "\"output packets\":\"{}\"," \
                 "\"output bytes\":\"{}\"," \
                 "\"output drops\":\"{}\"," \
                 "\"output broadcast packets\":\"{}\"," \
                 "\"output multicast packets\":\"{}\"," \
                 "\"output errors\":\"{}\"," \
                 "\"output underruns\":\"{}\"," \
                 "\"output applique\":\"{}\"," \
                 "\"output resets\":\"{}\"," \
                 "\"output buffer failures\":\"{}\"," \
                 "\"output buffer swapouts\":\"{}\"," \
                 "\"carrier transitions\":\"{}\"".format( self.interface_received,
                                                          self.interface_admin_state_received,
                                                          self.interface_line_protocol_state_received,
                                                          self.state_transitions_received,
                                                          self.hardware_received,
                                                          self.hardware_address_received,
                                                          self.hardware_address_bia_received,
                                                          self.layer_received,
                                                          self.description_received,
                                                          self.internet_address_received,
                                                          self.mtu_received,
                                                          self.bandwidth_received,
                                                          self.reliability_received,
                                                          self.transmit_load_received,
                                                          self.receive_load_received,
                                                          self.encaps_received,
                                                          self.duplex_received,
                                                          self.bit_per_sec_received,
                                                          self.link_type_received,
                                                          self.output_flow_control_received,
                                                          self.input_flow_control_received,
                                                          self.carrier_delay_state_received,
                                                          self.loopback_state_received,
                                                          self.flapped_received,
                                                          self.arp_type_received,
                                                          self.arp_timeout_received,
                                                          self.number_of_bundled_interfaces_received,
                                                          self.bundled_interfaces_received,
                                                          self.input_output_data_rate_received,
                                                          self.last_input_time_received,
                                                          self.last_output_time_received,
                                                          self.last_clear_received,
                                                          self.input_rate_received,
                                                          self.input_packet_rate_received,
                                                          self.output_rate_received,
                                                          self.output_packet_rate_received,
                                                          self.input_packets_received,
                                                          self.input_bytes_received,
                                                          self.input_drops_received,
                                                          self.up_level_protocol_drops_received,
                                                          self.input_broadcast_packets_received,
                                                          self.input_multicast_packets_received,
                                                          self.input_errors_received,
                                                          self.input_crc_received,
                                                          self.input_frame_received,
                                                          self.input_overrun_received,
                                                          self.input_ignore_received,
                                                          self.input_abort_received,
                                                          self.output_packets_received,
                                                          self.output_bytes_received,
                                                          self.output_drops_received,
                                                          self.output_broadcast_packets_received,
                                                          self.output_multicast_packets_received,
                                                          self.output_errors_received,
                                                          self.output_underruns_received,
                                                          self.output_applique_received,
                                                          self.output_resets_received,
                                                          self.output_buffer_failures_received,
                                                          self.output_buffer_swapouts_received,
                                                          self.carrier_transitions_received ) + \
               "};" )
          self.start_processing_details_flag = False
        else:
          continue
    """
    Create the Analysis Engine seed file
    """
    for seed_dictionary in self.show_interfaces_detail_table:
      try:
        self.detail_interfaces_detail_analysis_fd.write( seed_dictionary + "\n" )
      except Exception as e:
        raise Exception( "ShowInterfacesDetailSeedAnalysisFileBuilder: {}".format(e) )
    else:
      if self.cmd_list[SeedCommandDictionaryProcessor.verbose] == 'Yes':
        self.message_str = \
          "No inetrfaces found for building seed analsysis file."
        self.gparent.logger_message_signal.emit( self.message_str )
    return ()
  """
  METHOD: build_juniper_analysis_seed_file( self ):
  DESCRIPTION: Create "show interface detail" Analysis Edit data
  INPUT: JUNIPER "show interface detail" captured data
  OUTPUT: "EditAnalysisSeedFile" input data
  """
  def build_juniper_analysis_seed_file( self ):
    self.current_interface = ""
    self.show_interfaces_detail_table = []
    """
    Start scanning for physcial interface lines to 
    process based on the seed file interface list, ignoring any not in the list.
    """
    for self.detail_data in self.detail_data_fd:
      self.start_processing_details_flag = False
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.detail_data )
      self.line_index += len( self.detail_data )
      if self.detail_data.startswith( "\n" ):
        continue
      try:
        self.detail_data_list = self.detail_data.split()
      except Exception as error:
        raise Exception( "SHOWINTERFACESDETAILEDSEEDANALYSISFILEBUILDER: "
                         "Juniper interface processing error: {}".format( error ) )
      if self.detail_data.startswith( "Physical interface:" ):
        for self.intf in self.interfaces_to_match.split():
          self.current_interface = self.detail_data_list[2]
          if self.detail_data_list[2].startswith( self.intf ):
            self.start_processing_details_flag = True
            break
        if not self.start_processing_details_flag:
          continue
        else:
          """
          Reset file location to the Physical Interface blocks first line.
          Since the starting process above has pulled past it.
          """
          self.decoder_instance.current_index = self.decoder_instance.previous_index
          self.detail_data_fd.seek( self.decoder_instance.current_index )
          for self.detail_data in self.detail_data_fd:
            # FIXME DEBUG CODE
            # FIXME DEBUG CODE if self.detail_data.find("Autonegotiation information:") != -1:
            # FIXME DEBUG CODE   print(self.detail_data)
            # FIXME DEBUG CODE elif self.detail_data.find("CoS information:") != -1:
            # FIXME DEBUG CODE   print(self.detail_data)
            # FIXME DEBUG CODE
            """
            Stop processing current "Physical INterface" block of data ends
            """
            try:
              if self.detail_data.startswith( "Physical interface:" ) and \
                 self.current_interface != self.detail_data.split()[2]:
                self.build_analysis_seed_file_entry(self.device, self.decoder_instance)
                self.decoder_instance.decoder_class = ""
                self.decoder_instance.decoder_class_name = ""
                self.decoder_instance.decoder_class_name_key = ""
                self.decoder_instance.decoder_class_name_key_added = ""
                self.decoder_instance.decoded_data = OrderedDict()
                """
                Reset file pointer so its back at the "Physical Interface line
                """
                self.detail_data_fd.seek( self.decoder_instance.current_index )
                break
            except:
              """
              Failure here means really are not on the Phyiscal Interface line.
              """
              pass
            """
            Track the file index.  This is required because Python can only
            seek forward, aka, by reference to the beggining of a file.
            !! NOTE IMPORTANT!!  This is a nasty dependence but needs to be done
            and done correctly or as the file is processed the logic will
            get out of sync with the beginning of each line under analysis! 
            """
            self.decoder_instance.previous_index = self.decoder_instance.current_index
            self.decoder_instance.current_index += len( self.detail_data )
            self.line_index += len( self.detail_data )
            """
            Ignore empty lines
            """
            if self.detail_data.startswith( "\n" ):
              continue
            try:
              __str__.decode( __str__(),
                              self.decoder_instance,
                              self.device,
                              self.detail_data_fd,
                              self.detail_data,
                              self.line_index
                            )
            except Exception as error:
              raise Exception( error )
    """"""
    # Use the collected data and initialize values to
    # create the Analysis Engine seed file dictionary of KEY:VALUE's
    self.write_analysis_seed_file( self.show_interfaces_detail_table )
    return ()
  """
  Build analysis seed file entry
  """
  def build_analysis_seed_file_entry( self, device, decoder_instance ):
    self.entry = ""
    self.entry_dict_str = ""
    self.device = device
    self.decoded_instance = decoder_instance
    self.decoded_list = list( self.decoder_instance.decoded_data.items() )
    self.physical_interface = ""
    for self.key, self.value in self.decoder_instance.decoded_data.items():
      if self.physical_interface == "":
        try:
          self.physical_interface_str = self.decoder_instance.decoded_data[self.key]
          self.physical_interface_dict = ast.literal_eval( self.physical_interface_str )
          self.physical_interface = self.physical_interface_dict["interface"]
        except:
          pass
      self.entry += "\"{}\":{},".format( self.key, self.value )
    self.entry = self.entry[:-1]
    self.entry_dict_str = \
      "{{\"show interfaces {} detail\":\"show interfaces {} detail\"," \
      "\"device\":\"{}\"," \
      "{}}};\n".format( self.physical_interface,
                        self.physical_interface,
                        self.device,
                        self.entry )
    self.show_interfaces_detail_table.append( self.entry_dict_str )
    #FIXME DEBUG CODE
    #FIXME DEBUG CODE for i in self.show_interfaces_detail_table:
    #FIXME DEBUG CODE   print(i)
    #FIXME DEBUG CODE
    return()
  """
  Create the Analysis Engine seed file
  """
  def write_analysis_seed_file( self, show_interfaces_detail_table ):
    self.show_interfaces_detail_table = show_interfaces_detail_table
    for seed_dictionary in self.show_interfaces_detail_table:
      try:
        self.detail_interfaces_detail_analysis_fd.write( seed_dictionary + "\n" )
      except Exception as e:
        raise Exception( "ShowInterfacesDetailSeedAnalysisFileBuilder: {}".format( e ) )
    else:
      if self.cmd_list[SeedCommandDictionaryProcessor.verbose] == 'Yes':
        self.message_str = \
          "No interfaces found for building seed analsysis file."
        self.gparent.logger_message_signal.emit( self.message_str )
    return()
####################################################################################################################
