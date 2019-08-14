"""
FILE: ShowClass of ServiceDetailSeedAnalysisFileBuilder
CLASS:  ShowClassOfServiceSeedAnalysisFileBuilder
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
from SeedDictionary import SeedCommandDictionaryProcessor
from Dictionary import ValidateAnalysisSeedFileDictionary
from DecodeDataProcessor import DecoderInfo
from DecoderFactory import __str__
"""
CLASS: ShowClassOfServiceSeedAnalysisFileBuilder:
DESCRIPTION: Create "show class of service detail" Analysis Edit data
INPUT: "show class of service detail" captured data
OUTPUT: "EditAnalysisSeedFile" input data
"""
class ShowClassOfServiceSeedAnalysisFileBuilder:
  "Show Class of Service Detail Seed Analysis File Builder"
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
  DESCRIPTION: Create "show class of service detail" Analysis Edit data entry point.
               Determines input data to process and passes this data onto processing methods.
  INPUT: "show class of service detail" captured data
  OUTPUT: "EditAnalysisSeedFile" input data
  """
  def execute(self, dictionary):
    self.results = ""
    self.received_data = ""

    self.dictionary = ValidateAnalysisSeedFileDictionary(dictionary)


    self.interfaces_to_match = self.cmd_list[SeedCommandDictionaryProcessor.interfaces]
    if self.interfaces_to_match == "":
      raise Exception( "ShowClassOfServiceSeedAnalysisFileBuilder "
                       "error INTERFACE match list is empty."
                     )
    if self.cmd_list[SeedCommandDictionaryProcessor.verbose] == 'Yes':
      self.message_str = \
        "Build Show Class of Services Detail Seed File command started at: {}.".\
          format( datetime.datetime.now().strftime( "%d%b%Y-%H%M-%S" ) )
      self.gparent.logger_message_signal.emit(self.message_str)
    self.message_str = "Building seed file: {}.".\
          format( self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] )
    self.gparent.logger_message_signal.emit( self.message_str )
    try:
      self.analysis_filename = str( self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] )
      self.detail_interfaces_detail_analysis_fd = open( self.analysis_filename, "w+" )
    except:
      raise Exception( "{}: ShowClassOfServiceSeedAnalysisFileBuilder file I/O error with \"{}\". "
                       "Build Show Class of Service Detail Seed File Command terminated. ".
                       format( self.name,
                               self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] )  )
    self.data_filename = self.cmd_list[SeedCommandDictionaryProcessor.commandpath] + \
                         self.cmd_list[SeedCommandDictionaryProcessor.commands] + \
                         self.filename_time_extension
    self.device = self.cmd_list[SeedCommandDictionaryProcessor.device]
    if self.device == "":
      raise CriticalFailure( "ShowClassOfServiceSeedAnalysisFileBuilder: Invalid seed file!" )
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
            self.message_str = "No class of service data found."
            self.gparent.logger_message_signal.emit(self.message_str)
    except Exception as e:
      raise Exception( "ShowClassOfServiceSeedAnalysisFileBuilder: {}".format(e) )
    return()
  # FIXME
  # FIXME more places oop'ing these two methods below would be a good idea, aka, factories maybe or importlib's
  # FIXME
  """
  METHOD: build_cisco_analysis_seed_file( self ):
  DESCRIPTION: Create "show class of service detail" Analysis Edit data
  INPUT: CISCO "show class of service detail" captured data
  OUTPUT: "EditAnalysisSeedFile" input data
  """
  def build_cisco_analysis_seed_file( self ):
    return ()
  """
  METHOD: build_juniper_analysis_seed_file( self ):
  DESCRIPTION: Create "show class of service detail" Analysis Edit data
  INPUT: JUNIPER "show class of service detail" captured data
  OUTPUT: "EditAnalysisSeedFile" input data
  """
  def build_juniper_analysis_seed_file( self ):
    self.current_interface = ""
    self.show_interfaces_detail_table = []
    """
    Start scanning for physcial class of service lines to 
    process based on the seed file class of service list, ignoring any not in the list.
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
                         "Juniper class of service processing error: {}".format( error ) )
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
          Reset file location to the Physical Class of Service blocks first line.
          Since the starting process above has pulled past it.
          """
          self.decoder_instance.current_index = self.decoder_instance.previous_index
          self.detail_data_fd.seek( self.decoder_instance.current_index )
          for self.detail_data in self.detail_data_fd:
            """
            Stop processing current "Physical Interface" block of data ends
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
                Reset file pointer so its back at the "Physical Class of Service line
                """
                self.detail_data_fd.seek( self.decoder_instance.current_index )
                break
            except:
              """
              Failure here means really are not on the Phyiscal Class of Service line.
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
        raise Exception( "ShowClassOfServiceSeedAnalysisFileBuilder: {}".format( e ) )
    else:
      if self.cmd_list[SeedCommandDictionaryProcessor.verbose] == 'Yes':
        self.message_str = \
          "No interfaces found for building seed analsysis file."
        self.gparent.logger_message_signal.emit( self.message_str )
    return()
####################################################################################################################
