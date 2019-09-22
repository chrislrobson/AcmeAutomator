"""****************************************************************************
FILE: ShowInterfacesDetailAnalysisSeedFileBuilder
CLASS:    ShowInterfacesDetailAnalysisSeedFileBuilder
Author: Christopher Robson
Copyright by:    Christopher Robson
Copyright date: 01Jan2016
 CRITICAL !! THIS CLASS IS PROPRIETARY AND MAY NOT BE REUSED BY ANYONE BUT THE AUTHOR!!
 CRITICAL THIS MODULE DOES NOT BELONG TO ANY CONTRACTING COMPANY OR THE GOVERNMENT!
 CRITICAL This software is not FREE!    Use or destribution of the software system and its
 CRITICAL subsystem modules, libraries, configuration file and "seed" file without the
 CRITICAL express permission of the author is strictly PROHIBITED!
FUNCTION:    Module builds a seed file for analyzing collected data.
****************************************************************************"""
"""
LIBRARIES:    Python libraries
"""
import datetime, os
from collections import OrderedDict
"""
LIBRARIES:    Testbed Tester specific libraries
"""
from Globals import *
from DecodeDataProcessor import DecoderInfo
from WriteAnalysisSeedFile import WriteAnalysisSeedFile
"""
CLASS: ShowInterfacesDetailAnalysisSeedFileBuilder:
DESCRIPTION: Create "show interface detail" Analysis Edit data
INPUT: "show interface detail" captured data
OUTPUT: "EditAnalysisSeedFile" input data
"""
class ShowIsisAdjacencySeedAnalysisFileBuilder:
    "Show Isis Adjacency Seed Analysis File Builder"
    """"""
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
    METHOD: execute:
    DESCRIPTION: Create "show ISIS Adjacency" Analysis Edit data entry point.
                 Determines input data to process and passes this data onto processing methods.
    INPUT: "show interface detail" captured data
    OUTPUT: "EditAnalysisSeedFile" input data
    """
    def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
        self.dictionary = dictionary
        self.results = ""
        self.received_data = ""
        self.dictionary = dictionary
        self.results = ""
        self.received_data = ""
        if self.dictionary['verbose']:
            self.message = "{} started at: {}.".format(self.name, datetime.datetime.now().strftime( "%d%b%Y-%H%M-%S" ) )
            self.dictionary['loggerwidget'].emit(self.message)
        self.message = "Building Analysis Seed Data: {}.".format(self.dictionary["filename"])
        self.dictionary['loggerwidget'].emit(self.message)
        self.data_filename = "{}{}{}{}".format(self.dictionary["relativepath"], self.dictionary["commandpath"], self.dictionary["commands"], self.dictionary['datetime'])
        try:
            self.analysis_fd = open(self.dictionary['archivefilename'], 'w+')
        except Exception as error:
            self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
            self.dictionary['loggerwidget'].emit(self.message)
            raise Exception
        if self.dictionary["device"] == "":
            self.message = "{{{}{}: invalid seed file{}}}".format(Globals.RED_MESSAGE, self.name, Globals.SPAN_END_MESSAGE)
            self.dictionary['loggerwidget'].emit(self.message)
            raise Exception
        if self.dictionary["device"] == "juniper":
            self.title_str = "Interface                         System                 L State"
        elif self.dictionary["device"] == "cisco":
            self.title_str = "System Id         Interface              SNPA                   State Hold Changed  NSF IPv4 IPv6"
        else:
            self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, "UNKNOWN DEVICE TYPE", Globals.SPAN_END_MESSAGE)
            self.dictionary['loggerwidget'].emit(self.message)
            raise Exception
        try:
            with open( self.data_filename, "r" ) as self.detail_data_fd:
                for self.isis_data in self.detail_data_fd:
                    if self.isis_data.startswith( "\n" ):
                        continue
                    elif self.isis_data.startswith( "IS-IS" ):
                        self.isis_router_id = self.isis_data.split()[1]
                    elif self.start_analysis_flag and self.isis_data.startswith( self.title_str ):
                        if self.dictionary["device"] == "juniper":
                            try:
                                self.build_juniper_isis_adjacency_analysis_seed_file(self.analysis_fd, self.dictionary)
                            except Exception as error:
                                self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                                self.dictionary['loggerwidget'].emit(self.message)
                                self.analysis_fd.close()
                                self.detail_data_fd.close()
                                raise
                            break
                        if self.start_analysis_flag and self.dictionary["device"] == "cisco":
                            try:
                                self.build_cisco_isis_adjacency_analysis_seed_file(self.analysis_fd, self.dictionary)
                            except Exception as error:
                                self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                                self.dictionary['loggerwidget'].emit(self.message)
                                self.analysis_fd.close()
                                self.detail_data_fd.close()
                                raise
                            break
                    elif self.isis_data.startswith( "DUT(" ) and self.isis_data.find( ")-> show isis adjacency" ) != -1:
                             # FIXME REMOVE AFTER TEST WITH CISCO self.isis_data.find( ")-> show isis adjacency | no-more" ) != -1:
                        self.start_analysis_flag = True
                        continue
                    else:
                        continue
        except Exception as error:
            self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
            self.dictionary['loggerwidget'].emit(self.message)
            raise Exception
        self.analysis_fd.close()
        self.detail_data_fd.close()
        if os.stat(self.dictionary['archivefilename']).st_size == 0:
            self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, "No report data found, empty seed file generated.", Globals.SPAN_END_MESSAGE)
            self.dictionary['loggerwidget'].emit(self.message)
        return()
    # fixme
    # fixme ANOTHER QUICK AND DIRTY FIX the next two methods should be OOPed!!!!!!
    """
     System Id            Interface                SNPA                     State Hold Changed    NSF IPv4 IPv6
     R91A-ASR9010         PO0/0/1/0                *PtoP*                     Up   27   3w3d      Yes None None
    """
    """
    METHOD: build_cisco_isis_adjacency_analysis_seed_file( self ):
    DESCRIPTION: Create "show adjacency" Analysis Edit data
    INPUT: CISCO "show adjacency" captured data
    OUTPUT: Analysis seed file data
    """
    def build_cisco_isis_adjacency_analysis_seed_file(self, analysis_fd, dictionary):
        self.analysis_fd = analysis_fd
        self.dictionary = dictionary
        self.isis_adjacency_table = []
        for self.isis_data in self.detail_data_fd:
            if self.isis_data.startswith( "\n" ) or self.isis_data.startswith( " " ):
                continue
            if self.isis_data.startswith( "Total" ):
                break
            else:
                self.isis_data_list = self.isis_data.split()
                try:
                    self.system = self.isis_data_list[0]
                except:
                    self.system = ""
                try:
                    self.interface = self.isis_data_list[1]
                except:
                    self.interface = ""
                try:
                    self.snpa = self.isis_data_list[2]
                except:
                    self.snpa = ""
                try:
                    self.state = self.isis_data_list[3]
                except:
                    self.state = ""
                try:
                    self.hold = self.isis_data_list[4]
                except:
                    self.hold = ""
                try:
                    self.nsf = self.isis_data_list[6]
                except:
                    self.nsf = ""
                try:
                    self.ipv4bfd = self.isis_data_list[7]
                except:
                    self.ipv4bfd = ""
                try:
                    self.ipv6bfd = self.isis_data_list[8]
                except:
                    self.ipv6bfd = ""
                self.isis_adjacency_table.append("{" + \
                                                 "\"show isis adjacency\":\"show isis adjacency\"," \
                                                 "\"device\":\"{}\"," \
                                                 "\"router id\":\"{}\"," \
                                                 "\"interface\":\"{}\",\"system\":\"{}\"," \
                                                 "\"snpa\":\"{}\",\"state\":\"{}\"," \
                                                 "\"hold\":\"{}\"," \
                                                 "\"nsf\":\"{}\"," \
                                                 "\"ipv4 bfd\":\"{}\"," \
                                                 "\"ipv6 bfd\":\"{}\"".format(self.dictionary["device"],
                                                                              self.isis_router_id,
                                                                              self.interface,
                                                                              self.system,
                                                                              self.snpa,
                                                                              self.state,
                                                                              self.hold,
                                                                              self.nsf,
                                                                              self.ipv4bfd,
                                                                              self.ipv6bfd ) + \
                                                 "};")
        """
        Use the collected data and initialize values to
        create the Analysis Engine seed file dictionary of KEY:VALUE's
        """
        try:
            WriteAnalysisSeedFile(self).write_analysis_seed_file(table=self.isis_adjacency_table,
                                                                 analysis_fd=self.analysis_fd,
                                                                 dictionary=self.dictionary)
        except:
            raise
        return()
    """
    METHOD: build_juniper_isis_adjacency_analysis_seed_file( self ):
    DESCRIPTION: Create "show adjacency" Analysis Edit data
    INPUT: JUNIPER "show adjacency" captured data
    OUTPUT: Analysis seed file data
    """
    def build_juniper_isis_adjacency_analysis_seed_file(self, analysis_fd, dictionary):
        self.analysis_fd = analysis_fd
        self.dictionary = dictionary
        self.isis_adjacency_table = []
        for self.isis_data in self.detail_data_fd:
            if self.isis_data.startswith("\n"):
                break
            else:
                try:
                    self.interface = self.isis_data.split()[0]
                except:
                    self.interface = ""
                try:
                    self.system = self.isis_data.split()[1]
                except:
                    self.system = ""
                try:
                    self.level = self.isis_data.split()[2]
                except:
                    self.level = ""
                try:
                    self.state = self.isis_data.split()[3]
                except:
                    self.state = ""
                try:
                    self.hold = self.isis_data.split()[4]
                except:
                    self.hold = ""
                try:
                    self.snpa = self.isis_data.split()[5]
                except:
                    self.snpa = ""
                self.isis_adjacency_table.append("{" + \
                                                 "\"show isis adjacency\":\"show_isis_adjacency\","
                                                 "\"device\":\"juniper\"," \
                                                 "\"interface\":\"{}\",\"system\":\"{}\"," \
                                                 "\"level\":\"{}\",\"state\":\"{}\"," \
                                                 "\"hold\":\"{}\",\"snpa\":\"{}\"".format(self.interface,
                                                                                          self.system,
                                                                                          self.level,
                                                                                          self.state,
                                                                                          self.hold,
                                                                                          self.snpa ) + \
                                                 "};")
        """
        Use the collected data and initialize values to
        create the Analysis Engine seed file dictionary of KEY:VALUE's
        """
        try:
            WriteAnalysisSeedFile(self).write_analysis_seed_file(table=self.isis_adjacency_table,
                                                                 analysis_fd=self.analysis_fd,
                                                                 dictionary=self.dictionary)
        except:
            raise
        return()
"""*******************************************************************************************************************
End of File
*******************************************************************************************************************"""
