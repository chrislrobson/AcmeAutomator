####################################################################################################################
# Python Qt5 Testbed Tester Show Snmp Interface Seed Analysis File Builder
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
# Show Snmp Interface Seed Analysis File Builder
#-----------------------------------------------------------------------
class ShowSnmpInterfaceSeedAnalysisFileBuilder:
  "Show Snmp Interface Seed Analysis File Builder"
  #----------------------------------------------------------------------------------------------------------------
  def __init__( self, parent = None ):
    self.name = "Show Snmp Interface Seed Analysis File Builder"
    self.parent = parent
    self.seed = parent.seed
    self.gparent = parent.parent.parent.parent
    self.filename_time_extension = self.parent.filename_time_extension
    self.cmd_list = parent.cmd_list
    self.with_line_numbers = "No"
    self.debug = False
    self.snmp_interface_analysis_filename = ""
    self.snmp_interface_data_filename = ""
    self.snmp_interface_analysis_fd = None
    self.snmp_data_fd = None
    self.prepare_analysis_flag = False
    self.start_analysis_flag = False
    self.start_but_skip_one_analysis_flag = False
    self.snmp_interface_table = []
    self.interfaces_to_match = ""
  #----------------------------------------------------------------------------------------------------------------
  def execute( self ):
    #----------------------------------------------------------------------------------------------------------------
    self.interfaces_to_match = self.cmd_list[SeedCommandDictionaryProcessor.interfaces]
    self.device_being_matched = self.cmd_list[SeedCommandDictionaryProcessor.device]
    if self.device_being_matched == "juniper":
      self.title_str = "Interface             System         L State"
    elif self.device_being_matched == "cisco":
      self.title_str = "ifName : "
    else:
      raise Exception( "ShowSnmpInterfaceSeedAnalysisFileBuilder: UNKNOWN DEVICE TYPE" )
    if self.cmd_list[SeedCommandDictionaryProcessor.verbose] == 'Yes':
      self.message_str = \
        "Build Show Snmp Interface Seed File command started at: {}\n".\
          format( datetime.datetime.now().strftime( "%d%b%Y-%H%M-%S" ) )
      self.gparent.processor_message_signal.emit(self.message_str)
    self.message_str = "Building seed file: {}.".\
          format( self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] )
    self.gparent.logger_message_signal.emit( self.message_str )
    try:
      self.analysis_filename = str( self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] )
      self.snmp_interface_analysis_fd = open( self.analysis_filename, "w+" )
    except:
      raise Exception( "{}: ShowSnmpInterfaceSeedAnalysisFileBuilder file I/O error with \"{}\". "
                       "Build Show Snmp Interface Seed File Command terminated. ".
                       format( self.name,
                               self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] )  )
    self.data_filename = self.cmd_list[SeedCommandDictionaryProcessor.commandpath] + \
                         self.cmd_list[SeedCommandDictionaryProcessor.commands] + \
                         self.filename_time_extension
    try:
      with open( self.data_filename, "r" ) as self.snmp_data_fd:
        for self.snmp_data in self.snmp_data_fd:
          if self.snmp_data.startswith( "\n" ):
            continue
          elif self.prepare_analysis_flag and \
             self.snmp_data.startswith( self.title_str ):
            if self.device_being_matched == "juniper":
              self.build_juniper_snmp_interface_analysis_seed_file()
            if self.device_being_matched == "cisco":
              self.build_cisco_snmp_interface_analysis_seed_file()
            else:
              raise Exception( "ShowSnmpInterfaceSeedAnalysisFileBuilder: UNKNOWN DEVICE TYPE" )
            self.snmp_interface_analysis_fd.close()
            self.snmp_data_fd.close()
            break
          elif self.snmp_data.startswith( "DUT(" ) and \
               self.snmp_data.find( ")-> show snmp interface" ) != -1:
               # FIXME REMOVE AFTER TEST WITH CISCO self.snmp_data.find( ")-> show snmp interface | no-more" ) != -1:
            self.prepare_analysis_flag = True
            continue
          else:
            continue
    except Exception as e:
      raise Exception( "ShowSnmpInterfaceSeedAnalysisFileBuilder: {}".format(e) )
    return()
  #----------------------------------------------------------------------------------------------------------------
  # FIXME ANOTHER QUICK AND DIRTY FIX the nesxt two methods should be OOPed!!!!!!
  #----------------------------------------------------------------------------------------------------------------
  # ifName : Null0                 ifIndex : 2
  #----------------------------------------------------------------------------------------------------------------
  def build_cisco_snmp_interface_analysis_seed_file( self ):
    snmp_interface_table = []
    for self.snmp_data in self.snmp_data_fd:
      if self.snmp_data.startswith( "\n" ) or self.snmp_data.startswith( " " ):
        continue
      self.snmp_data_list = self.snmp_data.split()
      if self.interfaces_to_match != "":
        for self.intf in self.interfaces_to_match.split():
          if self.snmp_data_list[2].startswith( self.intf ):
            break
        else:
          # print(self.snmp_data_list[2])
          continue
      try:
        self.interface = self.snmp_data_list[2]
      except:
        self.interface = ""
      try:
        self.ifindex = self.snmp_data_list[5]
      except:
        self.ifindex = ""
      snmp_interface_table.append( "{" + \
                                   "\"show snmp interface\":\"show snmp interface\"," \
                                   "\"device\":\"{}\"," \
                                   "\"interface\":\"{}\"," \
                                   "\"ifindex\":\"{}\"".format( self.device_being_matched,
                                                                 self.interface,
                                                                 self.ifindex ) + \
                                   "};")
    for seed_dictionary in snmp_interface_table:
      # FIXME DEBUG print(seed_dictionary)
      try:
        self.snmp_interface_analysis_fd.write(seed_dictionary + "\n")
      except:
        print("Seed dictionary file write failed.")
    return()
  #----------------------------------------------------------------------------------------------------------------
  #----------------------------------------------------------------------------------------------------------------
  def build_juniper_snmp_interface_analysis_seed_file( self ):
    snmp_interface_table = []
    for self.snmp_data in self.snmp_data_fd:
      if self.snmp_data.startswith( "\n" ):
        break
      else:
        try:
          self.interface = self.snmp_data.split()[0]
        except:
          self.interface = ""
        try:
          self.system = self.snmp_data.split()[1]
        except:
          self.system = ""
        try:
          self.level = self.snmp_data.split()[2]
        except:
          self.level = ""
        try:
          self.state = self.snmp_data.split()[3]
        except:
          self.state = ""
        try:
          self.hold = self.snmp_data.split()[4]
        except:
          self.hold = ""
        try:
          self.snpa = self.snmp_data.split()[5]
        except:
          self.snpa = ""
        snmp_interface_table.append( "{" + \
                                     "\"show snmp interface\":\"show_snmp_interface\",\"device\":\"juniper\"," \
                                     "\"interface\":\"{}\",\"system\":\"{}\"," \
                                     "\"level\":\"{}\",\"state\":\"{}\"," \
                                     "\"hold\":\"{}\",\"snpa\":\"{}\"".format( self.interface,
                                                                               self.system,
                                                                               self.level,
                                                                               self.state,
                                                                               self.hold,
                                                                               self.snpa ) + \
                                     "};")
    for seed_dictionary in snmp_interface_table:
      # FIXME DEBUG print(seed_dictionary)
      try:
        self.snmp_interface_analysis_fd.write(seed_dictionary + "\n")
      except:
        print("Seed dictionary file write failed.")
    return()
###################################################################################################################
