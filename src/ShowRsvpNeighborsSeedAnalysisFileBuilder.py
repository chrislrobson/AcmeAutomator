####################################################################################################################
# Python Qt5 Testbed Tester Show RSVP Neighbors Seed Analysis File Builder
# MODULE:  ShowRsvpNeighborsSeedAnalysisFileBuilder
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
from SeedDictionary import SeedCommandDictionaryProcessor,\
                                                                SeedCommandlinePreprocessor
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
# Show Rsvp Neighbors Seed Analysis File Builder
#-----------------------------------------------------------------------
class ShowRsvpNeighborsSeedAnalysisFileBuilder:
  "Show Rsvp Neighbors Seed Analysis File Builder"
  #----------------------------------------------------------------------------------------------------------------
  def __init__( self, parent = None ):
    self.name = "Show Rsvp Neighbors Seed Analysis File Builder"
    self.parent = parent
    self.seed = parent.seed
    self.gparent = parent.parent.parent.parent
    self.filename_time_extension = self.parent.filename_time_extension
    self.cmd_list = parent.cmd_list
    self.with_line_numbers = "No"
    self.debug = False
    self.rsvp_neighbors_analysis_filename = ""
    self.rsvp_neighbors_data_filename = ""
    self.rsvp_neighbors_analysis_fd = None
    self.rsvp_data_fd = None
    self.prepare_analysis_flag = False
    self.start_analysis_flag = False
    self.start_but_skip_one_analysis_flag = False
    self.rsvp_neighbors_table = []
    #-----------------------------------------------------------------------------------------------------------
    self.rsvp_global_neighbor = ""
    self.rsvp_interface_neighbor = ""
    self.rsvp_interface = ""
    self.rsvp_refresh_reduction = ""
    self.rsvp_remote_epoch = ""
    self.rsvp_out_of_order_count = ""
    self.rsvp_retransmitted_count = ""
  #----------------------------------------------------------------------------------------------------------------
  def execute( self ):
    #----------------------------------------------------------------------------------------------------------------
    self.interfaces_to_match = self.cmd_list[SeedCommandDictionaryProcessor.interfaces]
    self.device_being_matched = self.cmd_list[SeedCommandDictionaryProcessor.device]
    if self.cmd_list[SeedCommandDictionaryProcessor.verbose] == 'Yes':
      self.message_str = \
        "Build Show Rsvp Neighbors Seed File command started at: {}\n".\
          format( datetime.datetime.now().strftime( "%d%b%Y-%H%M-%S" ) )
      self.gparent.processor_message_signal.emit(self.message_str)
    self.message_str = "Building seed file: {}.".\
          format( self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] )
    self.gparent.logger_message_signal.emit( self.message_str )
    try:
      self.analysis_filename = str( self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] )
      self.rsvp_neighbors_analysis_fd = open( self.analysis_filename, "w+" )
    except:
      raise Exception( "{}: ShowRsvpNeighborsSeedAnalysisFileBuilder file I/O error with \"{}\". "
                       "Build Show Rsvp Neighbors Seed File Command terminated. ".
                       format( self.name,
                               self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] )  )
    self.data_filename = self.cmd_list[SeedCommandDictionaryProcessor.commandpath] + \
                         self.cmd_list[SeedCommandDictionaryProcessor.commands] + \
                         self.filename_time_extension
    self.device = self.cmd_list[SeedCommandDictionaryProcessor.device]
    if self.device == "":
      raise CriticalFailure( "ShowRsvpNeighborsSeedAnalysisFileBuilder: Invalid seed file!" )
    try:
      with open( self.data_filename, "r" ) as self.rsvp_data_fd:
        for self.rsvp_data in self.rsvp_data_fd:
          if self.start_analysis_flag and self.device == "juniper":
            self.reportFD = self.build_juniper_analysis_seed_file()
            self.rsvp_neighbors_analysis_fd.close()
            self.rsvp_data_fd.close()
            break
          elif self.start_analysis_flag and self.device == "cisco":
            self.reportFD = self.build_cisco_analysis_seed_file()
            self.rsvp_neighbors_analysis_fd.close()
            self.rsvp_data_fd.close()
            break
          elif self.rsvp_data.startswith( "DUT(" ) and \
               self.rsvp_data.find( ")-> show rsvp neighbors" ) != -1:
            self.start_analysis_flag = True
            continue
          else:
            continue
    except Exception as e:
      raise Exception( "ShowRsvpNeighborsSeedAnalysisFileBuilder: {}".format(e) )
    return()
  #----------------------------------------------------------------------------------------------------------------
  # FIXME ANOTHER QUICK AND DIRTY FIX the nesxt two methods should be OOPed!!!!!!
  #----------------------------------------------------------------------------------------------------------------
  #----------------------------------------------------------------------------------------------------------------
  def build_cisco_analysis_seed_file( self ):
    self.rsvp_neighbors_table = []
    self.line_length = 0
    for self.rsvp_data in self.rsvp_data_fd:
      self.line_length += len( self.rsvp_data )
      if self.rsvp_data.startswith( "\n" ):
        continue
      else:
        self.rsvp_data_list = self.rsvp_data.split()
        if self.rsvp_data.startswith( "Global Neighbor" ):
          try:
            self.rsvp_global_neighbor = self.rsvp_data_list[2]
          except:
            self.rsvp_global_neighbor = ""
          for self.rsvp_data in self.rsvp_data_fd:
            self.line_length += len( self.rsvp_data )
            if self.rsvp_data.startswith( "\n" ):
              continue
            else:
              self.rsvp_data_list = self.rsvp_data.split()
              if self.rsvp_data.startswith( "  Interface Neighbor" ):
                try:
                  self.rsvp_interface_neighbor = self.rsvp_data_list[2]
                except:
                  self.rsvp_interface_neighbor = ""
                for self.rsvp_data in self.rsvp_data_fd:
                  self.line_length += len( self.rsvp_data )
                  if self.rsvp_data.startswith( "\n" ):
                    continue
                  else:
                    self.rsvp_data_list = self.rsvp_data.split()
                    if self.rsvp_data.startswith( "    Interface" ):
                      try:
                        self.rsvp_interface = self.rsvp_data_list[1]
                      except:
                        self.rsvp_interface = ""
                    elif self.rsvp_data.startswith( "    Refresh Reduction" ):
                      try:
                        self.rsvp_refresh_reduction = self.rsvp_data_list[2]
                      except:
                        self.rsvp_refresh_reduction = ""
                    elif self.rsvp_data.startswith( "    Remote epoch" ):
                      try:
                        self.rsvp_remote_epoch = self.rsvp_data_list[2]
                      except:
                        self.rsvp_remote_epoch = ""
                    elif self.rsvp_data.startswith( "    Counters" ):
                      for self.rsvp_data in self.rsvp_data_fd:
                        if self.rsvp_data.startswith( "Global Neighbor" ):
                          self.rsvp_data_fd.seek( self.line_length)
                          break
                        self.line_length += len( self.rsvp_data )
                        if self.rsvp_data.startswith( "\n" ):
                          continue
                        else:
                          self.move_back_length = 0
                          self.line_length += len( self.rsvp_data )
                          self.rsvp_data_list = self.rsvp_data.split()
                          if self.rsvp_data.startswith( "      Out of order messages" ):
                            try:
                              self.rsvp_out_of_order_count = self.rsvp_data_list[4]
                            except:
                              self.rsvp_out_of_order_count = ""
                          elif self.rsvp_data.startswith( "      Retransmitted messages" ):
                            self.move_back_length = len( self.rsvp_data )
                            try:
                              self.rsvp_retransmitted_count = self.rsvp_data_list[2]
                            except:
                              self.rsvp_retransmitted_count = ""
                      #-----------------------------------------------------------------------------------------
                      self.rsvp_neighbors_table.append( "{" + \
                                                   "\"show rsvp neighbors detail\":\"show rsvp neighbors detail\"," \
                                                   "\"device\":\"{}\"," \
                                                   "\"rsvp global neighbor\":\"{}\"," \
                                                   "\"rsvp interface neighbor\":\"{}\"," \
                                                   "\"rsvp interface\":\"{}\"," \
                                                   "\"rsvp refresh reduction\":\"{}\"," \
                                                   "\"rsvp remote epoch\":\"{}\"," \
                                                   "\"rsvp out of order count\":\"{}\"," \
                                                   "\"rsvp retransmitted count\":\"{}\"".
                                                        format( self.device,
                                                                self.rsvp_global_neighbor,
                                                                self.rsvp_interface_neighbor,
                                                                self.rsvp_interface,
                                                                self.rsvp_refresh_reduction,
                                                                self.rsvp_remote_epoch,
                                                                self.rsvp_out_of_order_count,
                                                                self.rsvp_retransmitted_count) + \
                                                   "};")
                      break
            break
    #-------------------------------------------------------------------------------------------------------------
    for seed_dictionary in self.rsvp_neighbors_table:
      # FIXME DEBUG ONLY print(seed_dictionary)
      try:
        self.rsvp_neighbors_analysis_fd.write(seed_dictionary + "\n")
      except:
        print("Seed dictionary file write failed.")
    return()
  #----------------------------------------------------------------------------------------------------------------
  #----------------------------------------------------------------------------------------------------------------
  def build_juniper_analysis_seed_file( self ):
    rsvp_neighbors_table = []
    for self.rsvp_data in self.rsvp_data_fd:
      if self.rsvp_data.startswith( "\n" ):
        break
      else:
        try:
          self.interface = self.rsvp_data.split()[0]
        except:
          self.interface = ""
        try:
          self.system = self.rsvp_data.split()[1]
        except:
          self.system = ""
        try:
          self.level = self.rsvp_data.split()[2]
        except:
          self.level = ""
        try:
          self.state = self.rsvp_data.split()[3]
        except:
          self.state = ""
        try:
          self.hold = self.rsvp_data.split()[4]
        except:
          self.hold = ""
        try:
          self.snpa = self.rsvp_data.split()[5]
        except:
          self.snpa = ""
        rsvp_neighbors_table.append( "{" + \
                                     "\"show rsvp neighbors\":\"show_rsvp_neighbors\",\"device\":\"juniper\"," \
                                     "\"interface\":\"{}\",\"system\":\"{}\"," \
                                     "\"level\":\"{}\",\"state\":\"{}\"," \
                                     "\"hold\":\"{}\",\"snpa\":\"{}\"".format( self.interface,
                                                                               self.system,
                                                                               self.level,
                                                                               self.state,
                                                                               self.hold,
                                                                               self.snpa ) + \
                                     "};")
    for seed_dictionary in rsvp_neighbors_table:
      # FIXME DEBUG print(seed_dictionary)
      try:
        self.rsvp_neighbors_analysis_fd.write(seed_dictionary + "\n")
      except:
        print("Seed dictionary file write failed.")
    return()
###################################################################################################################
