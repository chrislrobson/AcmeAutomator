"""****************************************************************************
FILE: BuildAnalysisSeedFile
CLASS:  BuildAnalysisSeedFile
Author: Christopher Robson
Copyright by:  Christopher Robson
Copyright date: 01Jan2016
 CRITICAL !! THIS CLASS IS PROPRIETARY AND MAY NOT BE REUSED BY ANYONE BUT THE AUTHOR!!
 CRITICAL THIS MODULE DOES NOT BELONG TO ANY CONTRACTING COMPANY OR THE GOVERNMENT!
 CRITICAL This software is not FREE!  Use or destribution of the software system and its
 CRITICAL subsystem modules, libraries, configuration file and "seed" file without the
 CRITICAL express permission of the author is strictly PROHIBITED!
FUNCTION:  Module builds a seed file used to analyze collected data
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
from Decoder import __str__
"""
CLASS: BuildAnalysisSeedFile:
DESCRIPTION: Saves created analysis seed file for later reference
INPUT: 
OUTPUT:
"""
class BuildAnalysisSeedFile:
    "Build Analysis Analysis Seed File"
    """"""
    def __init__( self, parent = None ):
        self.name = self.__class__.__name__
        self.parent = parent
    """"""
    def build_analysis_seed_file_entry( self, dictionary = None, decoder_instance = None ):
        self.entry = ""
        self.entry_dict_str = ""
        self.dictionary = dictionary
        self.decoded_instance = decoder_instance
        self.decoded_list = list( self.parent.decoder_instance.decoded_data.items() )
        self.physical_interface = ""
        for self.key, self.value in self.parent.decoder_instance.decoded_data.items():
          if self.physical_interface == "":
            try:
              self.physical_interface_str = self.parent.decoder_instance.decoded_data[self.key]
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
        self.parent.show_interfaces_detail_table.append( self.entry_dict_str )
        # notes DEBUG CODE
        # notes DEBUG CODE for i in self.show_interfaces_detail_table:
        # notes DEBUG CODE   print(i)
        # notes DEBUG CODE
        return()
"""****************************************************************************************************
End of File
****************************************************************************************************"""

