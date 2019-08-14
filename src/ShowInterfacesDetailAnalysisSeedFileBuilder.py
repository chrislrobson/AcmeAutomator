"""****************************************************************************
FILE: ShowInterfaceDetailSeedAnalysisFileBuilder
CLASS:  ShowInterfacesDetailSeedAnalysisFileBuilder
Author: Christopher Robson
Copyright by:  Christopher Robson
Copyright date: 01Jan2016
 CRITICAL !! THIS CLASS IS PROPRIETARY AND MAY NOT BE REUSED BY ANYONE BUT THE AUTHOR!!
 CRITICAL THIS MODULE DOES NOT BELONG TO ANY CONTRACTING COMPANY OR THE GOVERNMENT!
 CRITICAL This software is not FREE!  Use or destribution of the software system and its
 CRITICAL subsystem modules, libraries, configuration file and "seed" file without the
 CRITICAL express permission of the author is strictly PROHIBITED!
FUNCTION:  Module builds a seed file for analysizing collected data.
****************************************************************************"""
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
from DecodeDataProcessor import DecoderInfo
from DecoderFactory import __str__
"""
CLASS: ShowInterfacesDetailAnalysisSeedFileBuilder:
DESCRIPTION: Create "show interface detail" Analysis Edit data
INPUT: "show interface detail" captured data
OUTPUT: "EditAnalysisSeedFile" input data
"""
class ShowInterfacesDetailAnalysisSeedFileBuilder:
  "Show Interfaces Detail Analysis Seed File Builder"

  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.gparent = parent.parent.parent.parent
    self.with_line_numbers = "No"
    self.debug = False
    self.detail_interfaces_detail_analysis_filename = ""
    self.detail_interfaces_detail_data_filename = ""
    self.detail_data_fd = None
    self.start_analysis_flag = False
    self.show_interfaces_detail_table = []
    self.interfaces_to_match = ""
    self.decoder_utility = self.parent.parent.parent.decoder_class
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
  def execute( self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dictionary = dictionary
    self.results = ""
    self.received_data = ""
    self.interfaces_to_match = self.dictionary["interfaces"]
    if self.interfaces_to_match == "":
      self.message = "{{{}{}: error INTERFACE match list is empty{}}}".format(Globals.RED_MESSAGE, self.name, Globals.SPAN_END_MESSAGE)
      self.dictionary['loggerwidget'].emit(self.message)
      raise Exception
    if self.dictionary['verbose']:
      self.message = "{} started at: {}.".format(self.name, datetime.datetime.now().strftime( "%d%b%Y-%H%M-%S" ) )
      self.dictionary['loggerwidget'].emit(self.message)
    self.message = "Building Analysis Seed Data: {}.".format(self.dictionary["filename"])
    self.dictionary['loggerwidget'].emit(self.message)
    try:
      self.analysis_fd = open(self.dictionary['archivefilename'], 'w+')
    except Exception as error:
      self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
      self.dictionary['loggerwidget'].emit(self.message)
      raise Exception
    self.data_filename = "{}{}{}{}".format(self.dictionary["relativepath"], self.dictionary["commandpath"], self.dictionary["commands"], self.dictionary['datetime'])
    if self.dictionary["device"] == "":
      self.message = "{{{}{}: invalid seed file{}}}".format(Globals.RED_MESSAGE, self.name, Globals.SPAN_END_MESSAGE)
      self.dictionary['loggerwidget'].emit(self.message)
      raise Exception
    try:
      with open( self.data_filename, "r" ) as self.detail_data_fd:
        self.line_index = 0
        for self.detail_data in self.detail_data_fd:
          """
          Skip comments and line beginning with carriage returns or
          process the special script control keyword string
          """
          if self.detail_data.startswith( "\n" ) or self.detail_data.startswith( "#" ):
            if self.detail_data.startswith( "#@@!!" ):
              # fixme TOBE DONE MAYBE A FORLOOP here to repeat the command?
              pass
            self.decoder_instance.previous_index = self.decoder_instance.current_index
            self.decoder_instance.current_index += len( self.detail_data )
            self.line_index += len( self.detail_data )
            continue
          """
          Before doing nay processing find the command issued 
          which indicates data is to follow
          """
          if self.detail_data.startswith( "DUT(" ) and self.detail_data.find( ")-> show interfaces" ) != -1:
            self.start_analysis_flag = True
            self.decoder_instance.previous_index = self.decoder_instance.current_index
            self.decoder_instance.current_index += len( self.detail_data )
            self.line_index += len( self.detail_data )
            continue
          """
          Check for first line.  By doing this the data file can contain
          more than one command output data.
          Juniper data string to match: "Physical interface"
          Cisco data string to match: ", line protocol is" 
          """
          if self.start_analysis_flag and self.detail_data.startswith( "Physical interface:" ) or self.detail_data.find( ", line protocol is" ) != -1:
            self.detail_data_fd.seek( self.decoder_instance.current_index )
            if self.dictionary["device"] == "juniper":
              try:
                self.reportFD = self.build_juniper_analysis_seed_file(self.analysis_fd, self.dictionary)
              except Exception as error:
                self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                self.dictionary['loggerwidget'].emit(self.message)
                self.analysis_fd.close()
                self.detail_data_fd.close()
                raise
              self.analysis_fd.close()
              self.detail_data_fd.close()
              break
            if self.start_analysis_flag and self.dictionary["device"] == "cisco":
              try:
                self.reportFD = self.build_cisco_analysis_seed_file(self.analysis_fd, self.dictionary)
              except Exception as error:
                self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                self.dictionary['loggerwidget'].emit(self.message)
                self.analysis_fd.close()
                self.detail_data_fd.close()
                raise
              self.analysis_fd.close()
              self.detail_data_fd.close()
              break
          else:
            self.decoder_instance.previous_index = self.decoder_instance.current_index
            self.decoder_instance.current_index += len( self.detail_data )
            self.line_index += len( self.detail_data )
            continue
        else:
          if self.dictionary['verbose']:
            self.message = "{{{}{}: No interface data found{}".format(Globals.RED_MESSAGE, self.name, Globals.SPAN_END_MESSAGE)
            self.dictionary['loggerwidget'].emit(self.message)
    except Exception as error:
      self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
      self.dictionary['loggerwidget'].emit(self.message)
      raise Exception( "{}: {}".format(self.name, error) )
    self.detail_data_fd.close()
    return()
  """
  METHOD: build_cisco_analysis_seed_file( self ):
  DESCRIPTION: Create "show interface detail" Analysis Edit data
  INPUT: CISCO "show interface detail" captured data
  OUTPUT: "EditAnalysisSeedFile" input data
  """
  def build_cisco_analysis_seed_file(self, analysis_fd, dictionary):
    self.analysis_fd = analysis_fd
    self.dictionary = dictionary
    for self.detail_data in self.detail_data_fd:

      # notes DEBUG CODE self.detail_data_fd.seek(self.decoder_instance.previous_index)
      # notes DEBUG CODE self.detail_data = next( self.detail_data_fd )
      # notes DEBUG CODE print( "PREVIOUS INTERFACE DATA: {}".format(self.detail_data) )
      # notes DEBUG CODE self.detail_data_fd.seek(self.decoder_instance.current_index)
      # notes DEBUG CODE self.detail_data = next( self.detail_data_fd )
      # notes DEBUG CODE print( "CURRENT INTERFACE: {}".format(self.detail_data) )

      # notes DEBUG CODE if self.detail_data.startswith("GigabitEthernet0/0/0/5.200"):
      # notes DEBUG CODE   print(self.detail_data)

      self.interface_found_flag = False
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.detail_data )
      self.line_index += len( self.detail_data )
      if self.detail_data.startswith( "\n" ):
        continue
      try:
        self.detail_data_list = self.detail_data.split()
      except Exception as error:
        continue
      if not self.detail_data.startswith( " " ):
        if self.interfaces_to_match != "":
          for self.intf in self.interfaces_to_match.split():
            if self.detail_data_list[0].startswith( self.intf ):
              self.interface_found_flag = True
              self.interface_received = self.detail_data_list[0]
              self.interface_received = self.interface_received.replace( ":", "." )
              if self.interface_received.startswith( "Bundle" ) or self.interface_received.startswith( "tunnel" ):
                self.decoder_instance.decoder_class_name_key = "logical interface {}".format(self.interface_received)
              else:
                self.decoder_instance.decoder_class_name_key = "physical interface {}".format( self.interface_received )
              self.value = "\"interface\":\"{}\"," \
                            "\"administrative state\":\"{}\"," \
                            "\"line protocol\":\"{}\"".\
                            format(
                                    self.interface_received,
                                    self.detail_data.split("is")[1].split(",")[0].lstrip(),
                                    self.detail_data.split( "is" )[2].split( "\n" )[0].lstrip().strip()
                                  )
              self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key + " " +
                                                 self.interface_received ] = \
                   "{{{}}}".format(self.value)
              break
          else:
            """
            The current interface was found in the interface-to-test list so blow past all this
            interface's sub-data to get to the next interface to test
            """
            for self.detail_data in self.detail_data_fd:
              self.decoder_instance.previous_index = self.decoder_instance.current_index
              self.decoder_instance.current_index += len( self.detail_data )
              self.line_index += len( self.detail_data )
              if self.detail_data.startswith( " " ):
                continue
              else:
                break
            continue
        else:
          continue
        # notes DEBUG CODE
        # notes DEBUG CODE if self.detail_data.find("Autonegotiation information:") != -1:
        # notes DEBUG CODE   print(self.detail_data)
        # notes DEBUG CODE elif self.detail_data.find("CoS information:") != -1:
        # notes DEBUG CODE   print(self.detail_data)
        # notes DEBUG CODE
        if not self.interface_found_flag:
          continue
        else:
          for self.detail_data in self.detail_data_fd:

            # notes DEBUG CODE print( "CURRENT DATA: {}".format(self.detail_data) )
            # notes DEBUG CODE self.detail_data_fd.seek(self.decoder_instance.previous_index)
            # notes DEBUG CODE self.detail_data = next( self.detail_data_fd )
            # notes DEBUG CODE print( "PREVIOUS INTERFACE DATA: {}".format(self.detail_data) )
            # notes DEBUG CODE self.detail_data_fd.seek(self.decoder_instance.current_index)
            # notes DEBUG CODE self.detail_data = next( self.detail_data_fd )
            # notes DEBUG CODE print( "CURRENT INTERFACE: {}".format(self.detail_data) )

            self.decoder_instance.previous_index = self.decoder_instance.current_index
            self.decoder_instance.current_index += len( self.detail_data )
            self.line_index += len( self.detail_data )
            if self.detail_data.startswith( "\n" ):
              """
              Create the next decoder entry from collected data
              """
              self.build_analysis_seed_file_entry(dictionary = self.dictionary, decoder_instance = self.decoder_instance)
              self.decoder_instance.decoder_class = ""
              self.decoder_instance.decoder_class_name = ""
              self.decoder_instance.decoder_class_name_key = ""
              self.decoder_instance.decoder_class_name_key_added = ""
              self.decoder_instance.decoded_data = OrderedDict()
              break
            try:
              self.detail_data_list = self.detail_data.split()
              self.detail_data = " ".join( self.detail_data_list )
            except Exception as error:
              continue
            if self.detail_data.startswith( "Interface state transitions:" ):
              try:
                self.value = "\"transition state\":\"{}\"".format( self.detail_data_list[3] )
              except Exception as error:
                continue
              self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                                 " interface transitions"] = "{{{}}}".format(self.value)
              self.detail_data_fd.seek( self.decoder_instance.current_index )
              continue
            if self.detail_data.startswith( "Hardware is" ):
              try:
                self.value_pre = "\"hw name\":\"{}\"," \
                                 "\"hw address\":\"{}\"". \
                                 format(
                                         " ".join( self.detail_data.split("is")[1].split(",")[0].split() ),
                                         self.detail_data.split(",")[1].split("is")[1].split()[0],
                                        )
              except Exception as error:
                try:
                  self.value_pre = "\"name\":\"{}\",". \
                    format( self.detail_data.split("is")[1].split( "\n" )[0].lstrip() )
                except Exception as error:
                  self.message = "{{{}{}: Error processing \"hardware is\" {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                  self.dictionary['loggerwidget'].emit(self.message)
                  raise
              try:
                self.value_pre_bia = ",\"bia\":\"{}\"".\
                     format( self.detail_data.split("bia")[1].split( ")" )[0].lstrip() )
              except Exception as error:
                self.value_pre_bia = ""
              self.value = "{}{}".format( self.value_pre, self.value_pre_bia )
              self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                                 " hardware"] = "{{{}}}".format(self.value)
              self.detail_data_fd.seek( self.decoder_instance.current_index )
              continue
            if self.detail_data.find( "Transport Mode" ) != -1:
              try:
                self.value = "\"mode\":\"{}\"".format( self.detail_data_list[1] )
              except Exception as error:
                self.message = "{{{}{}: Error processing \"Transport mode\" {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                self.dictionary['loggerwidget'].emit(self.message)
                raise
              self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                                 " transport mode"] = "{{{}}}".format(self.value)
              self.detail_data_fd.seek( self.decoder_instance.current_index )
              continue
            if self.detail_data.find( "Protocol Handling" ) != -1:
              try:
                self.value_pre = "\"mode\":\"{}\"".format( self.detail_data_list[1] )
              except Exception as error:
                self.message = "{{{}{}: Error processing \"Procotol Handling\" {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                self.dictionary['loggerwidget'].emit(self.message)
                raise
              self.detail_data = next( self.detail_data_fd )
              self.decoder_instance.previous_index = self.decoder_instance.current_index
              self.decoder_instance.current_index += len( self.detail_data )
              self.line_index += len( self.detail_data )
              self.detail_data = " ".join( self.detail_data.split() )
              if self.detail_data.find( "Layer 2 Protocol Statistics to display" ) == -1:
                self.message = "{{{}{}: NEED TO REPAIR THIS NOT CODED BECAUSE AT THE TIME IT DIDNT EXIST{}}}".format(Globals.RED_MESSAGE, self.name, Globals.SPAN_END_MESSAGE)
                self.dictionary['loggerwidget'].emit(self.message)
                raise Exception
              else:
                try:
                  self.value_pre = "\"statistics\":\"{}\"".format(self.detail_data_list[1])
                except Exception as error:
                  self.message = "{{{}{}: Error processing No Layer 2 - {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                  self.dictionary['loggerwidget'].emit(self.message)
                  raise
              self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                                 " layer 2 protocol handling"] = \
                                                 "{{{}}}".format(self.value)
              self.detail_data_fd.seek( self.decoder_instance.current_index )
              continue
            if self.detail_data.startswith( "Description" ):
              try:
                self.description_received = " ".join( self.detail_data.split()[1:] ).replace( "\"", "" )
                self.description_received = self.description_received.replace( ":", "." )
                self.value = "\"description\":\"{}\"".format( self.description_received )
              except Exception as error:
                self.message = "{{{}{}: Error processing \"Description\" {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                self.dictionary['loggerwidget'].emit(self.message)
                raise
              self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                                 " description"] = "{{{}}}".format(self.value)
              self.detail_data_fd.seek( self.decoder_instance.current_index )
              continue
            if self.detail_data.startswith( "Internet address is" ):
              try:
                self.value = "\"address\":\"{}\"".format( self.detail_data_list[3] )
                self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                                   " internet"] = "{{{}}}".format(self.value)
              except Exception as error:
                self.message = "{{{}{}: Error processing \"Internet address\"{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                self.dictionary['loggerwidget'].emit(self.message)
                raise
              self.detail_data_fd.seek( self.decoder_instance.current_index )
              continue
            if self.detail_data.startswith( "MTU" ):
              try:
                self.value_pre = "\"mtu\":\"{}\"," \
                                 "\"bandwidth\":\"{} {}\"," \
                                 "\"max bandwidth\":\"{}\"". \
                                   format(
                                         self.detail_data_list[1],
                                         self.detail_data_list[4],
                                         self.detail_data_list[5],
                                         self.detail_data_list[7]
                                       )
              except Exception as error:
                try:
                  self.value_pre = "\"mtu\":\"{}\"," \
                                   "\"bandwidth\":\"{} {}\"". \
                                   format(
                                           self.detail_data_list[1],
                                           self.detail_data_list[4],
                                           self.detail_data_list[5],
                                         )
                except Exception as error:
                  self.message = "{{{}{}: Error processing \"MTU\" {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                  self.dictionary['loggerwidget'].emit(self.message)
                  raise
              self.detail_data = next( self.detail_data_fd )
              if self.detail_data.find( "reliability" ) == -1:
                self.detail_data_fd.seek( self.decoder_instance.current_index )
              else:
                self.decoder_instance.previous_index = self.decoder_instance.current_index
                self.decoder_instance.current_index += len( self.detail_data )
                self.line_index += len( self.detail_data )
                self.detail_data_list = self.detail_data.split()
                try:
                  self.value_pre += ",\"reliability\":\"{}\"," \
                                    "\"transmit load\":\"{}\"," \
                                    "\"receive load\":\"{}\"".\
                                    format(
                                            self.detail_data_list[1].split( "," )[0],
                                            self.detail_data_list[3].split( "," )[0],
                                            self.detail_data_list[5]
                                          )
                except Exception as error:
                  self.message = "{{{}{}: Error processing \"MTU reliability\" - {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                  self.dictionary['loggerwidget'].emit(self.message)
                  raise
              self.value = self.value_pre
              self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                                 " mtu/bandwidth/reliability/load"] = \
                                                 "{{{}}}".format(self.value)
              self.detail_data_fd.seek( self.decoder_instance.current_index )
              continue
            if self.detail_data.startswith( "Encapsulation" ):
              self.encapsulation_subdata_flag = False
              self.value_pre = ""
              try:
                self.value = "\"encapsulation\":\"{}\"". \
                                 format( self.detail_data.split( "Encapsulation" )[1].split( "," )[0].lstrip() )
              except Exception as error:
                self.message = "{{{}{}: Error processing \"Encapsulation\" - {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                self.dictionary['loggerwidget'].emit(self.message)
                raise
              if self.detail_data.find( "VLAN Id" ) != -1:
                try:
                  self.value_pre += ",\"vlan id\":\"{}\"".\
                       format( self.detail_data.split( "VLAN Id" )[1].split( "," )[0].lstrip() )
                except Exception as error:
                  self.message = "{{{}{}: Error processing Encapsulation \"VLAN Id\" - {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                  self.dictionary['loggerwidget'].emit(self.message)
                  raise
              if self.detail_data.find( "loopback" ) != -1:
                try:
                  self.value_pre += ",\"loopback\":\"{}\"". \
                    format( self.detail_data.split( "loopback" )[1].split( "," )[0].lstrip() )
                except Exception as error:
                  self.message = "{{{}{}: Error processing \"Encapsulation loopback\" - {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                  self.dictionary['loggerwidget'].emit(self.message)
                  raise
              """
              Now see if there are Encapsulation sub data
              """
              for self.detail_data in self.detail_data_fd:
                self.detail_data_list = self.detail_data.split()
                """
                   Outer Match: Dot1Q VLAN 300
                   Match is exact
                   Ethertype Any, MAC Match src any, dest any
                """
                if self.detail_data.find( "Outer Match:" ) != -1:
                  self.encapsulation_subdata_flag = True
                  self.value_pre += ",\"{}\":\"{}\"".format( self.detail_data.split( ":" )[0].lstrip(),
                                               self.detail_data.split( ":" )[1].split( "\n" )[0].lstrip() )
                elif self.detail_data.find( "Match is" ) != -1:
                  self.encapsulation_subdata_flag = True
                  self.value_pre += ",\"{}\":\"{}\"".\
                                    format( self.detail_data.split( "is" )[0].lower().lstrip(),
                                            self.detail_data.split( "is" )[1].split( "\n" )[0].lstrip() )
                elif self.detail_data.find( "Ethertype" ) != -1:
                  """
                  Ethertype Any, MAC Match src any, dest any
                  """
                  self.encapsulation_subdata_flag = True
                  self.value_pre += ",\"{}\":\"{}\"," \
                                    "\"{}\":\"{}\"," \
                                    "\"{}\":\"{}\"".\
                       format(
                                " ".join( self.detail_data.split( "," )[0].split()[:-1] ).lower(),
                                self.detail_data.split( "," )[0].split()[-1].lower(),
                                " ".join( self.detail_data.split( "," )[1].split()[:-1] ).lower(),
                                self.detail_data.split( ", " )[1].split()[-1].lower(),
                                " ".join( self.detail_data.split( "," )[2].split()[:-1] ).lower(),
                                self.detail_data.split( "," )[2].split()[-1].lower()
                              )
                else:
                  """
                  Restore file pointer when no sub-data found
                  and proceed on through other lines of data
                  """
                  if not self.encapsulation_subdata_flag:
                    self.detail_data_fd.seek( self.decoder_instance.current_index )
                  break
                """
                There was encapsulation sub-data so increament file pointers
                """
                self.decoder_instance.previous_index = self.decoder_instance.current_index
                self.decoder_instance.current_index += len( self.detail_data )
                self.line_index += len( self.detail_data )
              """
              Done scanning for additional Encapsulation data
              """
              self.value += self.value_pre
              self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                                 " encapsulation"] = "{{{}}}".format(self.value)
              self.detail_data_fd.seek( self.decoder_instance.current_index )
              continue
            if self.detail_data.find( "-duplex" ) != -1:
              try:
                self.value = "\"duplex\":\"{}\"," \
                              "\"bit per sec\":\"{}\"," \
                              "\"link type\":\"{}\"".format(
                                                                self.detail_data_list[0].split( "-" )[0],
                                                                self.detail_data_list[1].split( "," )[0],
                                                                self.detail_data.split( "is" )[1].lstrip()
                                                              )
              except Exception as error:
                try:
                  self.value = "\"duplex\":\"{}\"," \
                                "\"bit per sec\":\"{}\"".format(
                    self.detail_data_list[0].split( "-" )[0],
                    self.detail_data_list[1].split( "," )[0]
                  )
                except Exception as error:
                  self.message = "{{{}{}: Error processing \"Full-duplex\" - {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                  self.dictionary['loggerwidget'].emit(self.message)
                  raise
              self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                                 " {}-duplex".format( self.detail_data_list[0].split( "-" )[0] )] = \
                                                 "{{{}}}".format(self.value)
              self.detail_data_fd.seek( self.decoder_instance.current_index )
              continue
            if self.detail_data.startswith( "Duplex" ):
              try:
                self.value = "\"duplex\":\"{}\"," \
                              "\"bit per sec\":\"{}\"," \
                              "\"link type\":\"{}\"".format(
                                                                self.detail_data_list[1].split( "," )[0],
                                                                self.detail_data_list[2].split( "," )[0],
                                                                self.detail_data.split( "is" )[1].lstrip()
                                                              )
              except Exception as error:
                self.message = "{{{}{}: Error processing \"Duplex\" - {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                self.dictionary['loggerwidget'].emit(self.message)
                raise
              self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                                 " duplex"] = "{{{}}}".format(self.value)
              self.detail_data_fd.seek( self.decoder_instance.current_index )
              continue
            if self.detail_data.startswith( "output flow control is" ):
              self.value = "\"flow ctrl output\":\"{}\"," \
                            "\"flow ctrl input\":\"{}\"".format(
                                                          self.detail_data_list[4].split( "," )[0],
                                                          self.detail_data_list[9]
                                                        )
              self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                                 " flow control"] = "{{{}}}".format(self.value)
              self.detail_data_fd.seek( self.decoder_instance.current_index )
              continue
            if self.detail_data.startswith( "Carrier delay" ):
              try:
                self.value = "\"carrier delay state\":\"{}\",\"msec\":\"{}\"".\
                              format(
                                      self.detail_data.split( "is" )[0].split( "(")[1].split( ")" )[0],
                                      self.detail_data.split( "is" )[1].lstrip()
                                    )
              except Exception as error:
                self.message = "{{{}{}: Error processing \"Carrier delay\" - {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                self.dictionary['loggerwidget'].emit(self.message)
                raise
              self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                                 " carrier delay"] = "{{{}}}".format(self.value)
              self.detail_data_fd.seek( self.decoder_instance.current_index )
              continue
            if self.detail_data.startswith( "loopback" ):
              try:
                self.value = "\"loopback\":\"{}\"".\
                              format( self.detail_data.split( "loopback" )[1].
                                                       split( "\n" )[0].split( "," )[0].lstrip() )
              except Exception as error:
                self.message = "{{{}{}: Error processing \"loopback\" - {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                self.dictionary['loggerwidget'].emit(self.message)
                raise
              self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                                 " loopback"] = "{{{}}}".format(self.value)
              self.detail_data_fd.seek( self.decoder_instance.current_index )
              continue
            if self.detail_data.startswith( "Last link flapped" ):
              try:
                self.value = "\"flapped\":\"{}\"".\
                     format( self.detail_data_list[3].split( "\n" )[0] )
              except Exception as error:
                self.message = "{{{}{}: Error processing \"Last link flapped\" - {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                self.dictionary['loggerwidget'].emit(self.message)
                raise
              self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                                 " last link"] = "{{{}}}".format(self.value)
              self.detail_data_fd.seek( self.decoder_instance.current_index )
              continue
            if self.detail_data.startswith( "ARP type" ):
              try:
                self.value = "\"type\":\"{}\",\"timeout\":\"{}\"".\
                  format( self.detail_data_list[2].split( "," )[0],
                          self.detail_data_list[5].replace( ":", "." ) )
              except Exception as error:
                self.message = "{{{}{}: Error processing \"ARP type\" - {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                self.dictionary['loggerwidget'].emit(self.message)
                raise
              self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                                 " arp"] = "{{{}}}".format(self.value)
              self.detail_data_fd.seek( self.decoder_instance.current_index )
              continue
            if self.detail_data.find( "No. of members in this bundle:" ) != -1:
              try:
                self.value = "\"number\":\"{}\"".\
                              format( self.detail_data_list[6] )
              except Exception as error:
                self.message = "{{{}{}: Error processing \"No. of members in this bundle\" - {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                self.dictionary['loggerwidget'].emit(self.message)
                raise
              self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                                 " bundled interfaces"] = "{{{}}}".format(self.value)
              self.counter = int( self.detail_data_list[6] )
              for self.intf_count in range( self.counter ):
                for self.detail_data in self.detail_data_fd:
                  self.a, self.b, self.c, self.d = self.detail_data.split()
                  self.value = "\"interface\":\"{}\",".format( self.a )
                  self.value += "\"duplex\":\"{}\",".format( self.b )
                  self.value += "\"bits/ps\":\"{}\",".format( self.c )
                  self.value += "\"mode\":\"{}\"".format( self.d )
                  self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                                     " bundled interface " + str( self.intf_count )] = \
                                                     "{{{}}}".format(self.value)
                  break
              continue
            if self.detail_data.startswith( "Last input" ):
              try:
                self.value = "\"last input\":\"{}\"," \
                              "\"last output\":\"{}\"".\
                              format( self.detail_data_list[2].split( "," )[0].replace( ":", "." ),
                                      self.detail_data_list[4].replace( ":", "." ) )
              except Exception as error:
                self.message = "{{{}{}: Error processing \"Last input\" - {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                self.dictionary['loggerwidget'].emit(self.message)
                raise
              self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                                 " last input/output"] = "{{{}}}".format(self.value)
              self.detail_data_fd.seek( self.decoder_instance.current_index )
              continue
            if self.detail_data.startswith( "Last clearing" ):
              try:
                self.value = "\"last clear time\":\"{}\"".\
                              format( self.detail_data_list[6].replace( ":", "." ) )
              except Exception as error:
                self.message = "{{{}{}: Error processing \"Last clearing\" - {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                self.dictionary['loggerwidget'].emit(self.message)
                raise
              self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                                 " last clearing"] = "{{{}}}".format(self.value)
              self.detail_data_fd.seek( self.decoder_instance.current_index )
              continue
            if self.detail_data.find( "input rate" ) != -1:
              try:
                self.value = "\"input rate time\":\"{}\"," \
                             "\"input rate bits per sec\":\"{}\"," \
                             "\"input rate packets per sec\":\"{}\"". \
                                format(
                                        self.detail_data_list[0],
                                        self.detail_data_list[4],
                                        self.detail_data_list[6]
                                      )
              except Exception as error:
                self.message = "{{{}{}: Error processing \"input rate\" - {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                self.dictionary['loggerwidget'].emit(self.message)
                raise
              self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                                 " input rate"] = "{{{}}}".format(self.value)
              self.detail_data_fd.seek( self.decoder_instance.current_index )
              continue
            if self.detail_data.find( "output rate" ) != -1:
              try:
                self.value = "\"output rate time\":\"{}\"," \
                             "\"output rate bits per sec\":\"{}\"," \
                             "\"output rate packets per sec\":\"{}\"". \
                              format(
                                      self.detail_data_list[0],
                                      self.detail_data_list[4],
                                      self.detail_data_list[6]
                                    )
              except Exception as error:
                self.message = "{{{}{}: Error processing \"output rate\" - {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                self.dictionary['loggerwidget'].emit(self.message)
                raise
              self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                                 " output rate"] = "{{{}}}".format(self.value)
              self.detail_data_fd.seek( self.decoder_instance.current_index )
              continue
            if self.detail_data.find( "packets input," ) != -1:
              try:
                self.value = "\"input packets\":\"{}\"," \
                             "\"input bytes\":\"{}\"," \
                             "\"input total drops\":\"{}\"". \
                              format(
                                      self.detail_data_list[0],
                                      self.detail_data_list[3],
                                      self.detail_data_list[5]
                                    )
              except Exception as error:
                try:
                  self.value = "\"input packets\":\"{}\",\"input bytes\":\"{}\"". \
                    format(
                    self.detail_data_list[0],
                    self.detail_data_list[3]
                  )
                except Exception as error:
                  self.message = "{{{}{}: Error processing \"packet input\" - {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                  self.dictionary['loggerwidget'].emit(self.message)
                  raise
              self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                                 " packets/bytes inputs/total drops"] = "{{{}}}".\
                                                 format(self.value)
              self.detail_data_fd.seek( self.decoder_instance.current_index )
              continue
            if self.detail_data.find( "input drops," ) != -1:
              try:
                self.value = "\"input drops\":\"{}\"," \
                             "\"input queue drops\":\"{}\"," \
                             "\"input drop errors\":\"{}\"". \
                              format(
                                      self.detail_data_list[0],
                                      self.detail_data_list[3],
                                      self.detail_data_list[6]
                                    )
              except Exception as error:
                self.message = "{{{}{}: Error processing \"input/queue drops/errors\" - {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                self.dictionary['loggerwidget'].emit(self.message)
                raise
              self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                                 " input/queue drops/errors"] = "{{{}}}".format(self.value)
              self.detail_data_fd.seek( self.decoder_instance.current_index )
              continue
            if self.detail_data.find( "unrecognized upper-level protocol" ) != -1:
              try:
                self.value = "\"drops\":\"{}\"".format( self.detail_data_list[0] )
              except Exception as error:
                self.message = "{{{}{}: Error processing \"unrecognized upper-level protocol\" - {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                self.dictionary['loggerwidget'].emit(self.message)
                raise
              self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                                 " upper-level protocol"] = "{{{}}}".format(self.value)
              self.detail_data_fd.seek( self.decoder_instance.current_index )
              continue
            if self.detail_data.startswith( "Received" ):
              try:
                self.detail_data_list = self.detail_data.split()
                self.value = "\"received broadcast packets\":\"{}\",\"received multicast packets\":\"{}\"".\
                             format( self.detail_data_list[1], self.detail_data_list[4] )
                """
                Look ahead if runts exist process else restore previous point
                and move on to next line of data
                """
                self.detail_data = next( self.detail_data_fd )
                if not self.detail_data.split()[1].startswith( "runts" ):
                  self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                                     " received"] = "{{{}}}".format(self.value)
                  self.detail_data_fd.seek( self.decoder_instance.current_index )
                  continue
                self.detail_data_list = self.detail_data.split()
                self.decoder_instance.previous_index = self.decoder_instance.current_index
                self.decoder_instance.current_index += len( self.detail_data )
                self.line_index += len( self.detail_data )
                self.value += ",\"runts\":\"{}\"," \
                              "\"giants\":\"{}\"," \
                              "\"throttles\":\"{}\"," \
                              "\"parity\":\"{}\"".format(
                                                          self.detail_data_list[0],
                                                          self.detail_data_list[2],
                                                          self.detail_data_list[4],
                                                          self.detail_data_list[6],
                                                         )
              except Exception as error:
                self.message = "{{{}{}: Error processing \"Received\" - {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                self.dictionary['loggerwidget'].emit(self.message)
                raise
              self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                                 " received"] = "{{{}}}".format(self.value)
              self.detail_data_fd.seek( self.decoder_instance.current_index )
              continue
            if self.detail_data.find( "input errors," ) != -1:
              try:
                self.value = "\"input errors\":\"{}\"," \
                              "\"input crc\":\"{}\"," \
                              "\"input frame\":\"{}\"," \
                              "\"input overrun\":\"{}\"," \
                              "\"input ignore\":\"{}\"," \
                              "\"input abort\":\"{}\"".format(
                                                                  self.detail_data_list[0],
                                                                  self.detail_data_list[3],
                                                                  self.detail_data_list[5],
                                                                  self.detail_data_list[7],
                                                                  self.detail_data_list[9],
                                                                  self.detail_data_list[11],
                                                                )
              except Exception as error:
                self.message = "{{{}{}: Error processing \"input errors\" - {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                self.dictionary['loggerwidget'].emit(self.message)
                raise
              self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                                 " input errors"] = "{{{}}}".format(self.value)
              self.detail_data_fd.seek( self.decoder_instance.current_index )
              continue
            if self.detail_data.find( "packets output," ) != -1:
              try:
                self.value = "\"output packets\":\"{}\"," \
                             "\"output bytes\":\"{}\"," \
                             "\"output total drops\":\"{}\"". \
                             format(
                                     self.detail_data_list[0],
                                     self.detail_data_list[3],
                                     self.detail_data_list[5]
                                   )
              except Exception as error:
                try:
                  self.value = "\"output packets\":\"{}\",\"output bytes\":\"{}\"". \
                    format(
                    self.detail_data_list[0],
                    self.detail_data_list[3],
                  )
                except Exception as error:
                  self.message = "{{{}{}: Error processing \"packet errors\" - {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                  self.dictionary['loggerwidget'].emit(self.message)
                  raise
              self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                                 " packets output"] = "{{{}}}".format(self.value)
              self.detail_data_fd.seek( self.decoder_instance.current_index )
              continue
            if self.detail_data.find( "output drops," ) != -1:
              try:
                self.value = "\"output drops\":\"{}\"," \
                             "\"output queues\":\"{}\"," \
                             "\"output errors\":\"{}\"". \
                  format(
                  self.detail_data_list[0],
                  self.detail_data_list[3],
                  self.detail_data_list[6]
                )
              except Exception as error:
                self.message = "{{{}{}: Error processing \"output/queue drops/errors\" - {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                self.dictionary['loggerwidget'].emit(self.message)
                raise
              self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                                 " output/dropped/errors"] = "{{{}}}".format(self.value)
              self.detail_data_fd.seek( self.decoder_instance.current_index )
              continue
            if self.detail_data.startswith( "Output" ):
              try:
                self.value = "\"output broadcast packets\":\"{}\"," \
                              "\"output multicast packets\":\"{}\"".format( self.detail_data_list[1],
                                                                        self.detail_data_list[4] )
              except Exception as error:
                self.message = "{{{}{}: \"Output\" - {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                self.dictionary['loggerwidget'].emit(self.message)
                raise
              self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                                 " output"] = "{{{}}}".format(self.value)
              self.detail_data_fd.seek( self.decoder_instance.current_index )
              continue
            if self.detail_data.find( "output errors," ) != -1:
              try:
                self.value = "\"output errors\":\"{}\"," \
                              "\"output underruns\":\"{}\"," \
                              "\"output applique\":\"{}\"," \
                              "\"output resets\":\"{}\"".format( self.detail_data_list[0],
                                                             self.detail_data_list[3],
                                                             self.detail_data_list[5],
                                                             self.detail_data_list[7] )
              except Exception as error:
                self.message = "{{{}{}: Error processing \"output errors\" - {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                self.dictionary['loggerwidget'].emit(self.message)
                raise
              self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                                 " output errors"] = "{{{}}}".format(self.value)
              self.detail_data_fd.seek( self.decoder_instance.current_index )
              continue
            if self.detail_data.find( "output buffer failures," ) != -1:
              try:
                self.value = "\"failures\":\"{}\"," \
                             "\"swapouts\":\"{}\"".\
                             format( self.detail_data_list[0],
                                     self.detail_data_list[4] )
              except Exception as error:
                self.message = "{{{}{}: Error processing \"output buffer failures\" - {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                self.dictionary['loggerwidget'].emit(self.message)
                raise
              self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                                 " output buffer"] = "{{{}}}".format(self.value)
              self.detail_data_fd.seek( self.decoder_instance.current_index )
              continue
            if self.detail_data.startswith( "Input/output data rate is" ):
              try:
                self.value = "\"data rate\":\"{}\"". \
                              format( self.detail_data.split()[-1].split( "." )[0] )
              except Exception as error:
                self.message = "{{{}{}: Error processing \"Input/output data rate is\" - {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                self.dictionary['loggerwidget'].emit(self.message)
                raise
              self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                                 " input/output"] = "{{{}}}".format(self.value)
              self.detail_data_fd.seek( self.decoder_instance.current_index )
              continue
            if self.detail_data_list[1].startswith( "carrier" ) and \
                self.detail_data_list[2].startswith( "transitions" ):
              try:
                self.value = "\"transitions\":\"{}\"".format( self.detail_data_list[0] )
              except Exception as error:
                self.message = "{{{}{}: Error processing \"carrier transition\" - {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                self.dictionary['loggerwidget'].emit(self.message)
                raise
              self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                                 " carrier"] = "{{{}}}".format(self.value)
              self.detail_data_fd.seek( self.decoder_instance.current_index )
              continue
            else:
              self.message = "{{{}{}: Error processing CISCO DATA - UNEXPECTED INPUT!{}}}".format(Globals.RED_MESSAGE, self.name, Globals.SPAN_END_MESSAGE)
              self.dictionary['loggerwidget'].emit(self.message)
              raise Exception
    """
    Use the collected data and initialize values to
    create the Analysis Engine seed file dictionary of KEY:VALUE's
    """
    try:
      self.write_analysis_seed_file(self.show_interfaces_detail_table, self.analysis_fd, self.dictionary)
    except:
      raise
    return ()
  """
  METHOD: build_juniper_analysis_seed_file( self ):
  DESCRIPTION: Create "show interface detail" Analysis Edit data
  INPUT: JUNIPER "show interface detail" captured data
  OUTPUT: "EditAnalysisSeedFile" input data
  """
  def build_juniper_analysis_seed_file(self, analysis_fd, dictionary):
    self.dictionary = dictionary
    self.analysis_fd = analysis_fd
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
        self.message = "{{{}{}: Juniper interface processing error: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
        self.dictionary['loggerwidget'].emit(self.message)
        raise
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
            # notes DEBUG CODE
            # notes DEBUG CODE if self.detail_data.find("so-1/2/1") != -1:
            # notes DEBUG CODE   print(self.detail_data)
            # notes DEBUG CODE elif self.detail_data.find("CoS information:") != -1:
            # notes DEBUG CODE   print(self.detail_data)
            # notes DEBUG CODE
            """
            Stop processing current "Physical Interface" block of data ends
            """
            try:
              if self.detail_data.startswith( "Physical interface:" ) and self.current_interface != self.detail_data.split()[2]:
                self.build_analysis_seed_file_entry(dictionary = self.dictionary, decoder_instance = self.decoder_instance)
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
            except Exception as error:
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
                              decoder_instance = self.decoder_instance,
                              dictionary = self.dictionary,
                              descriptor = self.detail_data_fd,
                              data = self.detail_data,
                              index = self.line_index
                            )
            except Exception as error:
              self.message = "{{{}{} is an unknown data decoder type, Please put into the " \
                             "DecoderDataDictionary.py file{} {}}}".format(Globals.RED_MESSAGE, self.detail_data.split()[0], error, Globals.SPAN_END_MESSAGE)
              self.dictionary['logger_message_signal'].emit(self.message)
              raise
    """"""
    # Use the collected data and initialize values to
    # create the Analysis Engine seed file dictionary of KEY:VALUE's
    try:
      self.write_analysis_seed_file(self.show_interfaces_detail_table, self.analysis_fd, self.dictionary)
    except:
      raise
    return ()
  """
  Build analysis seed file entry
  """
  def build_analysis_seed_file_entry( self, dictionary = None, decoder_instance = None ):
    self.entry = ""
    self.entry_dict_str = ""
    self.dictionary = dictionary
    self.decoded_instance = decoder_instance
    self.decoded_list = list( self.decoder_instance.decoded_data.items() )
    self.physical_interface = ""
    for self.key, self.value in self.decoder_instance.decoded_data.items():
      if self.physical_interface == "":
        try:
          self.physical_interface_str = self.decoder_instance.decoded_data[self.key]
          self.physical_interface_dict = ast.literal_eval( self.physical_interface_str )
          self.physical_interface = self.physical_interface_dict["interface"]
        except Exception as error:
          pass
      self.entry += "\"{}\":{},".format( self.key, self.value )
    self.entry = self.entry[:-1]
    self.entry_dict_str = \
      "{{\"show interfaces {} detail\":\"show interfaces {} detail\"," \
      "\"device\":\"{}\", {}}};\n".format(self.physical_interface,
                                          self.physical_interface,
                                          self.dictionary["device"],
                                          self.entry)
    self.show_interfaces_detail_table.append( self.entry_dict_str )
    # notes DEBUG CODE
    # notes DEBUG CODE for i in self.show_interfaces_detail_table:
    # notes DEBUG CODE   print(i)
    # notes DEBUG CODE
    return()
  """
  Create the Analysis Engine seed file
  """
  def write_analysis_seed_file(self, show_interfaces_detail_table, analysis_fd, dictionary):
    self.analysis_fd = analysis_fd
    self.dictionary = dictionary
    self.show_interfaces_detail_table = show_interfaces_detail_table
    try:
      for seed_dictionary in self.show_interfaces_detail_table:
        try:
          self.analysis_fd.write( seed_dictionary + "\n" )
        except Exception as error:
          self.analysis_fd.close()
          self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
          self.dictionary['loggerwidget'].emit(self.message)
          raise
    except Exception as error:
      if self.dictionary['verbose']:
        self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
        self.dictionary['loggerwidget'].emit(self.message)
        raise
    self.analysis_fd.close()
    return()
"""****************************************************************************************************
End of File
****************************************************************************************************"""

