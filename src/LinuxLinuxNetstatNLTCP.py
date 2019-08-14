####################################################################################################################
# Python Qt5 Testbed Tester Linux Netstat NL TCP
# MODULE:  LinuxNetstatNLTCP
# Author: Christopher Robson
# Copyright by:  Christopher Robson
# Copyright date: 01Jan2016
# This software is not FREE!  Use or destribution of the software system and its
# subsystem modules, libraries, configuration file and "seed" file without the
# express permission of the author is strictly PROHIBITED!
# FUNCTION:  Module analyzes data in the linux command "ip route show".  The first word in the data file is
#            "default" which gives this class its name.  Example data to be analyzed may be:
#                   "default via 10.168.1.1 dev enp0s3  proto static  metric 100 "
#                   "10.168.1.0/24 dev enp0s3  proto kernel  scope link  src 10.168.1.66  metric 100 "
#                   "192.168.122.0/24 dev virbr0  proto kernel  scope link  src 192.168.122.1 linkdown "
#
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
# linuxiprouteshow
#-----------------------------------------------------------------------
class linuxnetstatnltcp:
  "Linux Netstat NL TCP"
  #----------------------------------------------------------------------------------------------------------------
  def __init__( self, parent = None ):
    self.name = "Linux Netstat NL TCP"
    self.parent = parent
    self.verbose = parent.verbose
    self.ggparent = parent.ggparent
    self.filename_time_extension = parent.filename_time_extension
  #----------------------------------------------------------------------------------------------------------------
  def execute( self, seed_file, data_file ):
    if self.ggparent.testbed_tester.verbose:
      self.ggparent.logger_message_signal.emit( "Linux Netstat NL TCP is running" )
    self.results = ""
    #----------------------------------------------------------------------------------------------------------------
    try:
      self.dataFD = open( data_file + self.filename_time_extension, "r" )
    except:
      self.message_str = Globals.RED_MESSAGE + \
                         "LINUXNETSTATNLTCP: data file I/O error with \"{}\".".format( seed_file ) + \
                         Globals.SPAN_END_MESSAGE
      self.ggparent.logger_message_signal.emit(self.message_str)
      self.message_str = Globals.RED_MESSAGE + \
                         "LINUXNETSTATNLTCP: analysis terminated." + \
                         Globals.SPAN_END_MESSAGE
      self.ggparent.logger_message_signal.emit(self.message_str)
    self.message_str =  Globals.BLUE_FONT1O_BOLD_MESSAGE + \
                         "Netstat Analysis Report:" + \
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
                self.found = True
                if self.verbose == "Yes":
                  self.message_str = "FOUND listening port: {}". \
                    format( self.line.split("\n")[0].split()[3] )
                  self.ggparent.processor_message_signal.emit(self.message_str)
                  self.results += "FOUND listening port: {}\n". \
                                  format( self.line.split("\n")[0].split()[3] )
                break
            if not self.found:
              self.message_str = Globals.RED_BOLD_ONLY_MESSAGE + \
                                 "NOT FOUND: " + \
                                 Globals.SPAN_END_MESSAGE
              self.message_str += "port: {}". \
                                 format( self.keyword )
              self.ggparent.processor_message_signal.emit( self.message_str )
              self.results += "NOT FOUND: port: {}\n".format( self.keyword )
            continue
    except:
      self.message_str = Globals.RED_MESSAGE + \
                         "LINUXNETSTATNLTCP: File I/O error with \"{}\".". \
                           format( data_file + self.filename_time_extension ) + \
                         Globals.SPAN_END_MESSAGE
      self.ggparent.logger_message_signal.emit(self.message_str)
    self.message_str =  Globals.BLUE_FONT1O_BOLD_MESSAGE + \
                         "Netstat Analysis Report Completed." + \
                         Globals.SPAN_END_MESSAGE
    self.ggparent.processor_message_signal.emit(self.message_str)
    return( self.results )
#####################################################################################################################