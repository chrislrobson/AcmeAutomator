"""****************************************************************************
FILE: WriteAnalysisSeedFile
CLASS:    WriteAnalysisSeedFile
Author: Christopher Robson
Copyright by:    Christopher Robson
Copyright date: 01Jan2016
 CRITICAL !! THIS CLASS IS PROPRIETARY AND MAY NOT BE REUSED BY ANYONE BUT THE AUTHOR!!
 CRITICAL THIS MODULE DOES NOT BELONG TO ANY CONTRACTING COMPANY OR THE GOVERNMENT!
 CRITICAL This software is not FREE!    Use or destribution of the software system and its
 CRITICAL subsystem modules, libraries, configuration file and "seed" file without the
 CRITICAL express permission of the author is strictly PROHIBITED!
FUNCTION:    Module builds a seed file used to analyze collected data
****************************************************************************"""
"""
LIBRARIES:    Python libraries
"""
import datetime
import os, sys, stat
from collections import OrderedDict
import ast
"""
LIBRARIES:    Testbed Tester specific libraries
"""
from Globals import *
from DecodeDataProcessor import DecoderInfo
from Decoder import __str__
"""
CLASS: WriteAnalysisSeedFile:
DESCRIPTION: Saves created analysis seed file for later reference
INPUT: 
OUTPUT:
"""
class WriteAnalysisSeedFile:
    "Write Analysis Analysis Seed File"
    """"""
    def __init__( self, parent = None ):
        self.name = self.__class__.__name__
        self.parent = parent
    """"""
    def write_analysis_seed_file(self, table=None, analysis_fd=None, dictionary=None):
        self.analysis_fd = analysis_fd
        self.dictionary = dictionary
        self.table = table
        try:
            for seed_dictionary in self.table:
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

