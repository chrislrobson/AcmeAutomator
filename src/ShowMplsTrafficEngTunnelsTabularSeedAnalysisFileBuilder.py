####################################################################################################################
# Python Qt5 Testbed Tester Show MPLS TrafficEng Tunnels Tabular Seed Analysis File Builder
# MODULE:  ShowMplsTrafficEngTunnelsTabularSeedAnalysisFileBuilder
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
# Show Mpls TrafficEng Tunnels Tabular Seed Analysis File Builder
#-----------------------------------------------------------------------
class ShowMplsTrafficEngTunnelsTabularSeedAnalysisFileBuilder:
  "Show Mpls TrafficEng Tunnels Tabular Seed Analysis File Builder"
  #----------------------------------------------------------------------------------------------------------------
  def __init__( self, parent = None ):
    self.name = "Show Mpls TrafficEng Tunnels Tabular Seed Analysis File Builder"
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
        "Build Show Mpls TrafficEng Tunnels Tabular Seed File command started at: {}\n".\
          format( datetime.datetime.now().strftime( "%d%b%Y-%H%M-%S" ) )
      self.gparent.processor_message_signal.emit(self.message_str)
    self.message_str = "Building seed file: {}.".\
          format( self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] )
    self.gparent.logger_message_signal.emit( self.message_str )
    try:
      self.analysis_filename = str( self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] )
      self.mpls_analysis_fd = open( self.analysis_filename, "w+" )
    except:
      raise Exception( "{}: ShowMplsTrafficEngTunnelsTabularSeedAnalysisFileBuilder file I/O error with \"{}\". "
                       "Build Show Mpls TrafficEng TunnelsTabular Seed File Command terminated. ".
                       format( self.name,
                               self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] )  )
    self.data_filename = self.cmd_list[SeedCommandDictionaryProcessor.commandpath] + \
                         self.cmd_list[SeedCommandDictionaryProcessor.commands] + \
                         self.filename_time_extension
    self.device = self.cmd_list[SeedCommandDictionaryProcessor.device]
    if self.device == "":
      raise CriticalFailure( "ShowMplsTrafficEngTunnelsTabularSeedAnalysisFileBuilder: Invalid seed file!" )
    try:
      with open( self.data_filename, "r" ) as self.mpls_data_fd:
        for self.mpls_data in self.mpls_data_fd:
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
               self.mpls_data.find( ")-> show mpls traffic-eng tunnels tabular" ) != -1:
            self.start_analysis_flag = True
            continue
          else:
            continue
    except Exception as e:
      raise Exception( "ShowMplsTrafficEngTunnelsTabularSeedAnalysisFileBuilder: {}".format(e) )
    return()
  #----------------------------------------------------------------------------------------------------------------
  # FIXME ANOTHER QUICK AND DIRTY FIX the nesxt two methods should be OOPed!!!!!!
  #----------------------------------------------------------------------------------------------------------------
  def build_cisco_analysis_seed_file( self ):
    self.mpls_table = []
    self.line_length = 0
    for self.mpls_data in self.mpls_data_fd:
      if self.mpls_data.startswith( "+ = automatically created mesh tunnel" ):
        break
      self.line_length += len( self.mpls_data )
      self.mpls_data_list = self.mpls_data.split()
      if self.mpls_data.startswith( "\n" ):
        continue
      self.title = "".join( self.mpls_data_list )
      if not self.title.startswith( "NameIDAddressAddressStateStateRoleProt" ):
        continue
      else:
        for self.mpls_data in self.mpls_data_fd:
          if self.mpls_data.startswith( "* = automatically created backup tunnel" ):
            break
          self.line_length += len( self.mpls_data )
          self.mpls_data_list = self.mpls_data.split()
          if self.mpls_data.startswith( "\n" ):
            continue
          if self.mpls_data.startswith( "----------------- -----" ):
            continue
          if self.mpls_data_list[0][:1] == "*" or \
             self.mpls_data_list[0][:1] == "^" or \
             self.mpls_data_list[0][:1] == "+":
            self.mpls_tunnel_type_received = self.mpls_data_list[0][:1]
            try:
              self.mpls_name_received = self.mpls_data_list[0][1:]
            except:
              self.mpls_name_received = ""
          else:
            self.mpls_tunnel_type_received = ""
            try:
              self.mpls_name_received = self.mpls_data_list[0]
            except:
              self.mpls_name_received = ""
          try:
            self.mpls_lsp_id_received = self.mpls_data_list[1]
          except:
            self.mpls_lsp_id_received = ""
          try:
            self.mpls_destination_address_received = self.mpls_data_list[2]
          except:
            self.mpls_destination_address_received = ""
          try:
            self.mpls_source_address_received = self.mpls_data_list[3]
          except:
            self.mpls_source_address_received = ""
          try:
            self.mpls_state_received = self.mpls_data_list[4]
          except:
            self.mpls_state_received = ""
          try:
            self.mpls_frr_state_received = self.mpls_data_list[5]
          except:
            self.mpls_frr_state_received = ""
          try:
            self.mpls_lsp_role_received = self.mpls_data_list[6]
          except:
            self.mpls_lsp_role_received = ""
          try:
            self.mpls_path_protocol_received = self.mpls_data_list[7]
          except:
            self.mpls_path_protocol_received = ""
          #-----------------------------------------------------------------------------------------
          self.mpls_table.append( "{" + \
                                       "\"show mpls traffic-eng tunnels tabular\":"
                                       "\"show mpls traffic-eng tunnels tabular\"," \
                                       "\"device\":\"{}\"," \
                                       "\"mpls tunnel type\":\"{}\"," \
                                       "\"mpls name\":\"{}\"," \
                                       "\"mpls lsp id\":\"{}\"," \
                                       "\"mpls destination address\":\"{}\"," \
                                       "\"mpls source address\":\"{}\"," \
                                       "\"mpls state\":\"{}\"," \
                                       "\"mpls frr state\":\"{}\"," \
                                       "\"mpls lsp role\":\"{}\"," \
                                       "\"mpls path protocol\":\"{}\"". \
                                            format( self.device,
                                                    self.mpls_tunnel_type_received,
                                                    self.mpls_name_received,
                                                    self.mpls_lsp_id_received,
                                                    self.mpls_destination_address_received,
                                                    self.mpls_source_address_received,
                                                    self.mpls_state_received,
                                                    self.mpls_frr_state_received,
                                                    self.mpls_lsp_role_received,
                                                    self.mpls_path_protocol_received ) + \
                                       "};")
          continue
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
