####################################################################################################################
# Python Qt5 Testbed Tester Linux IP Addr Show
# MODULE:  LinuxIPAddrShow
# Author: Christopher Robson
# Copyright by:  Christopher Robson
# Copyright date: 01Jan2016
# This software is not FREE!  Use or destribution of the software system and its
# subsystem modules, libraries, configuration file and "seed" file without the
# express permission of the author is strictly PROHIBITED!
# FUNCTION:  Module analyzes data in the linux command "ip addr show".
# NOTE!!  Big dumps from the show command will require the loop_counter and delay_counters to be adjusted.
#         For example a 30G file will require the loop_counter to be set at 512 and delay at 5 seconds.
#-----------------------------------------------------------------------------------
# Because this is a ssh connection the "loopcnt must be set to at least "512" and
# "delay" must be set to at least "2"
####################################################################################################################
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
# Home grown
#------------------------------------------------------------------------------------------------------------------
from Globals import *
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
# linuxipaddrshow
#-----------------------------------------------------------------------
class linuxipaddrshow:
  "default"
  #----------------------------------------------------------------------------------------------------------------
  def __init__( self, parent = None ):
    self.name = "Linux Ip Addr Show"
    self.parent = parent
    self.verbose = parent.verbose
    self.ggparent = parent.ggparent
    self.filename_time_extension = parent.filename_time_extension
  #----------------------------------------------------------------------------------------------------------------
  def execute( self, seed_file, data_file ):
    if self.ggparent.testbed_tester.verbose:
      self.ggparent.logger_message_signal.emit( "Linux address processing is running" )
    self.results = ""
    #----------------------------------------------------------------------------------------------------------------
    try:
      self.dataFD = open( data_file + self.filename_time_extension, "r" )
    except:
      self.message_str = Globals.RED_MESSAGE + \
                         "LINUXIPADDRSHOW: data file I/O error with \"{}\".".format( seed_file ) + \
                         Globals.SPAN_END_MESSAGE
      self.ggparent.logger_message_signal.emit(self.message_str)
      self.message_str = Globals.RED_MESSAGE + \
                         "LINUXIPADDRSHOW: analysis terminated." + \
                         Globals.SPAN_END_MESSAGE
      self.ggparent.logger_message_signal.emit(self.message_str)
    self.message_str =  Globals.BLUE_FONT1O_BOLD_MESSAGE + \
                         "Interface Analysis Report:" + \
                         Globals.SPAN_END_MESSAGE
    self.ggparent.processor_message_signal.emit(self.message_str)
    try:
      with open( seed_file, 'r' ) as self.seed_file_FD:
        for self.seed_data in self.seed_file_FD:
          if self.seed_data.startswith( "#" ) or \
             self.seed_data.startswith( "!" ) or \
             self.seed_data.startswith( "\n" ):
            pass
          else:
            self.dataFD.seek( 0 )
            self.keyword = self.seed_data.split()[0]
            self.found = False
            for self.line in self.dataFD:
              if self.line.find( self.keyword ) != -1:
                for self.line in self.dataFD:
                  if self.line.find( self.keyword ) != -1:
                    self.found = True
                    if self.verbose == "Yes":
                      self.message_str = "FOUND {} with ip {}".\
                           format( self.line.split( "\n" )[0].split()[0],
                                   self.line.split( "\n" )[0].split()[1] )
                      self.ggparent.processor_message_signal.emit( self.message_str )
                      self.results += "FOUND {} with ip {}\n".\
                                      format( self.line.split( "\n" )[0].split()[0],
                                      self.line.split( "\n" )[0].split()[1] )
                    break
            if not self.found:
              self.message_str = Globals.RED_BOLD_ONLY_MESSAGE + \
                                 "NOT FOUND: " + \
                                 Globals.SPAN_END_MESSAGE
              self.message_str += "{} addressed interface". \
                                 format( self.keyword )
              self.results += "NOT FOUND: {} addressed interface\n".format( self.keyword )
              self.ggparent.processor_message_signal.emit( self.message_str )
            continue
    except:
      self.message_str = Globals.RED_MESSAGE + \
                         "LINUXIPADDRSHOW: File I/O error with \"{}\".". \
                           format( data_file + self.filename_time_extension ) + \
                         Globals.SPAN_END_MESSAGE
      self.ggparent.logger_message_signal.emit(self.message_str)
    self.message_str =  Globals.BLUE_FONT1O_BOLD_MESSAGE + \
                         "Interface Analysis Report Completed." + \
                         Globals.SPAN_END_MESSAGE
    self.ggparent.processor_message_signal.emit(self.message_str)
    return( self.results )
#####################################################################################################################