####################################################################################################################
# Python Qt5 Testbed Tester SNMP Utilities
# MODULE:
# Author: Christopher Robson
# Copyright by:  Christopher Robson
# Copyright date: 01Jan2016
# This software is not FREE!  Use or destribution of the software system and its
# subsystem modules, libraries, configuration file and "seed" file without the
# express permission of the author is strictly PROHIBITED!
# FUNCTION:  Module provides snmp functions to script.
####################################################################################################################
import datetime
from pysnmp.hlapi import *
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
# Show Device Information/Status/Configuration
#-----------------------------------------------------------------------
class SnmpUtilities:
  "SNMP Utiltities"
  # ----------------------------------------------------------------------------------------------------------------
  def __init__( self, parent = None ):
    self.name = "SNMP Utilities"
    self.parent = parent
    self.seed = parent.seed
    self.gparent = parent.parent.parent.parent
    self.filename_time_extension = self.parent.filename_time_extension
    self.cmd_list = parent.cmd_list
    self.with_line_numbers = "No"
    self.debug = False
    self.brief_interfaces_brief_analysis_filename = ""
    self.brief_interfaces_brief_data_filename = ""
    self.brief_interfaces_brief_analysis_fd = None
    self.brief_data_fd = None
    self.prepare_analysis_flag = False
    self.start_analysis_flag = False
    self.start_but_skip_one_analysis_flag = False
    self.brief_router_id = ""
    self.brief_interfaces_brief_table = []
    self.interfaces_to_match = ""
  #----------------------------------------------------------------------------------------------------------------
  def execute( self ):
    self.results = ""
    self.received_data = ""
    #--------------------------------------------------------------------------------------------------------------
    self.interfaces_to_match = self.cmd_list[SeedCommandDictionaryProcessor.interfaces]
    if self.cmd_list[SeedCommandDictionaryProcessor.verbose] == 'Yes':
      self.message_str = \
        "Build Show Interface Brief Seed File command started at: {}\n". \
          format( datetime.datetime.now().strftime( "%d%b%Y-%H%M-%S" ) )
      self.gparent.processor_message_signal.emit( self.message_str )
    self.message_str = "Building seed file: {}.". \
      format( self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] )
    self.gparent.logger_message_signal.emit( self.message_str )
    try:
      self.analysis_filename = str( self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] )
      self.brief_interfaces_brief_analysis_fd = open( self.analysis_filename, "w+" )
    except:
      raise Exception( "{}: ShowInterfaceBriefSeedAnalysisFileBuilder file I/O error with \"{}\". "
                       "Build Show Interface Brief Seed File Command terminated. ".
                       format( self.name,
                               self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] ) )
    self.data_filename = self.cmd_list[SeedCommandDictionaryProcessor.commandpath] + \
                         self.cmd_list[SeedCommandDictionaryProcessor.commands] + \
                         self.filename_time_extension
    # FIXME remove later try:
    # FIXME remove later   with open( self.data_filename, "r" ) as self.brief_data_fd:
    # FIXME remove later     for self.brief_data in self.brief_data_fd:
    return()
  #----------------------------------------------------------------------------------------------------------------
  def build_show_snmp_interface_seed_file( self ):
    #--------------------------------------------------------------------------------------------------------------
    for index in range(900):
      try:
        iterator = getCmd(SnmpEngine(),
                          CommunityData('gigbelab'),
                          UdpTransportTarget(('10.10.9.30', 161)),
                          ContextData(),
                          ObjectType( ObjectIdentity('IF-MIB','ifIndex', index)))
        errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

        if errorIndication:  # SNMP engine errors
            print(errorIndication)
        else:
            if errorStatus:  # SNMP agent errors
                print('%s at %s' % (errorStatus.prettyPrint(), varBinds[int(errorIndex)-1] if errorIndex else '?'))
            else:
              for varBind in varBinds:  # SNMP response contents
               print(' = '.join([x.prettyPrint() for x in varBind]))
      except:
        continue
####################################################################################################################
