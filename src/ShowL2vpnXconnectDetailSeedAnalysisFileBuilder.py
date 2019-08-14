####################################################################################################################
# Python Qt5 Testbed Tester Show L2vpn Xconnect Detail Seed Analysis File Builder
# MODULE:  ShowL2vpnXconnectDetailSeedAnalysisFileBuilder
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
from SeedDictionary import SeedCommandDictionaryProcessor
from SeedCommandlinePreprocessor import SeedCommandlinePreprocessor
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
# Show L2vpn Xconnect Detail Seed Analysis File Builder
#-----------------------------------------------------------------------
class ShowL2vpnXconnectDetailSeedAnalysisFileBuilder:
  "Show L2vpn Xconnect Detail Seed Analysis File Builder"
  #----------------------------------------------------------------------------------------------------------------
  def __init__( self, parent = None ):
    self.name = "Show L2vpn Xconnect Detail Seed Analysis File Builder"
    self.parent = parent
    self.seed = parent.seed
    self.gparent = parent.parent.parent.parent
    self.filename_time_extension = self.parent.filename_time_extension
    self.cmd_list = parent.cmd_list
    self.with_line_numbers = "No"
    self.debug = False
    self.l2vpn_xconnect_analysis_filename = ""
    self.l2vpn_xconnect_data_filename = ""
    self.l2vpn_xconnect_analysis_fd = None
    self.l2vpn_data_fd = None
    self.prepare_analysis_flag = False
    self.start_analysis_flag = False
    self.start_but_skip_one_analysis_flag = False
    self.l2vpn_xconnect_table = []
    self.line_length = 0
    #-----------------------------------------------------------------------------------------------------------
    self.l2vpn_ac_groups_received = ""
    self.l2vpn_pw_groups_received = ""
  #----------------------------------------------------------------------------------------------------------------
  def execute( self ):
    #----------------------------------------------------------------------------------------------------------------
    self.interfaces_to_match = self.cmd_list[SeedCommandDictionaryProcessor.interfaces]
    self.device_being_matched = self.cmd_list[SeedCommandDictionaryProcessor.device]
    if self.cmd_list[SeedCommandDictionaryProcessor.verbose] == 'Yes':
      self.message_str = \
        "Build Show L2vpn Xconnect Detail Seed File command started at: {}\n".\
          format( datetime.datetime.now().strftime( "%d%b%Y-%H%M-%S" ) )
      self.gparent.processor_message_signal.emit(self.message_str)
    self.message_str = "Building seed file: {}.".\
          format( self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] )
    self.gparent.logger_message_signal.emit( self.message_str )
    try:
      self.analysis_filename = str( self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] )
      self.l2vpn_xconnect_analysis_fd = open( self.analysis_filename, "w+" )
    except:
      raise Exception( "{}: ShowL2vpnXconnectDetailSeedAnalysisFileBuilder file I/O error with \"{}\". "
                       "Build Show L2vpn Xconnect Detail Seed File Command terminated. ".
                       format( self.name,
                               self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] )  )
    self.data_filename = self.cmd_list[SeedCommandDictionaryProcessor.commandpath] + \
                         self.cmd_list[SeedCommandDictionaryProcessor.commands] + \
                         self.filename_time_extension
    self.device = self.cmd_list[SeedCommandDictionaryProcessor.device]
    if self.device == "":
      raise CriticalFailure( "ShowL2vpnXconnectDetailSeedAnalysisFileBuilder: Invalid seed file!" )
    try:
      with open( self.data_filename, "r" ) as self.l2vpn_data_fd:
        for self.l2vpn_data in self.l2vpn_data_fd:
          self.line_length += len( self.l2vpn_data )
          if self.start_analysis_flag and self.device == "juniper":
            self.reportFD = self.build_juniper_analysis_seed_file()
            self.l2vpn_xconnect_analysis_fd.close()
            self.l2vpn_data_fd.close()
            break
          elif self.start_analysis_flag and self.device == "cisco":
            self.reportFD = self.build_cisco_analysis_seed_file()
            self.l2vpn_xconnect_analysis_fd.close()
            self.l2vpn_data_fd.close()
            break
          elif self.l2vpn_data.startswith( "DUT(" ) and \
               self.l2vpn_data.find( ")-> show l2vpn xconnect detail" ) != -1:
            self.start_analysis_flag = True
            continue
          else:
            continue
    except Exception as e:
      raise Exception( "ShowL2vpnXconnectDetailSeedAnalysisFileBuilder: {}".format(e) )
    return()
  #----------------------------------------------------------------------------------------------------------------
  # FIXME ANOTHER QUICK AND DIRTY FIX the nesxt two methods should be OOPed!!!!!!
  #----------------------------------------------------------------------------------------------------------------
  #----------------------------------------------------------------------------------------------------------------
  def build_cisco_analysis_seed_file( self ):
    self.l2vpn_xconnect_table = []
    for self.l2vpn_data in self.l2vpn_data_fd:
      self.line_length += len( self.l2vpn_data )
      if self.l2vpn_data.startswith( "\n" ):
        continue
      self.l2vpn_data_list = self.l2vpn_data.split()
      if self.l2vpn_data.startswith( "Group" ):
        self.first_group = True
        self.l2vpn_ac_groups_received = ""
        self.l2vpn_pw_groups_received = ""
        try:
          self.l2vpn_group_name_received = " ".join( self.l2vpn_data.split( "," )[0].split( "Group" )[1].split() )
        except:
          self.l2vpn_group_name_received = ""
        try:
          self.l2vpn_xconnect_name_received = " ".join( self.l2vpn_data.split( "," )[1].split( "XC" )[1].split())
        except:
          self.l2vpn_xconnect_name_received = ""
        try:
          self.l2vpn_group_state_received = " ".join( self.l2vpn_data.split( ";" )[0].split( "is" )[1].split() )
        except:
          self.l2vpn_group_state_received = ""
        try:
          self.l2vpn_group_interwork_received = self.l2vpn_data.split( ";" )[1].split()[1].split( "\n" )[0]
        except:
          self.l2vpn_group_interwork_received = ""
        #------------------------------------------------------------------------------------------------------
        for self.l2vpn_data in self.l2vpn_data_fd:
          if self.l2vpn_data.startswith( "Group" ):
            self.l2vpn_data_fd.seek( self.line_length )
            break
          self.line_length += len( self.l2vpn_data )
          self.l2vpn_data_list = self.l2vpn_data.split()
          if self.l2vpn_data.startswith( "\n" ):
            continue
          if self.l2vpn_data[2:].startswith( "AC:" ):
            try:
              self.l2vpn_ac_groups_received += "\"intf {}\":{{\"state\":\"{}\"}}". \
                format( self.l2vpn_data_list[1].replace( ",", "" ), self.l2vpn_data_list[4] )
              self.ac_title = "acgroup {}".format( self.l2vpn_data_list[1].replace( ",", "" ) )
            except:
              self.l2vpn_ac_groups_received += ""
            if self.first_group:
              self.l2vpn_ac_groups_received += ",\"{}\":{{".format( self.ac_title )
            for self.l2vpn_data in self.l2vpn_data_fd:
              self.first_group = False
              if self.l2vpn_data.startswith( "Group" ) or \
                 self.l2vpn_data[2:].startswith( "AC" ) or \
                 self.l2vpn_data[2:].startswith( "PW" ):
                self.l2vpn_data_fd.seek( self.line_length )
                self.l2vpn_ac_groups_received = self.l2vpn_ac_groups_received[:-1] + "},"
                self.first_group = True
                break
              self.line_length += len( self.l2vpn_data )
              self.l2vpn_data_list = self.l2vpn_data.split()
              if self.l2vpn_data[4:].startswith( "Type ATM VC" ):
                try:
                  self.l2vpn_ac_groups_received += \
                       "\"vpi/vci\":\"{}\",".format( self.l2vpn_data_list[5] )
                  self.l2vpn_ac_groups_received += \
                    "\"number ranges\":\"\","
                except:
                  self.l2vpn_ac_groups_received += ""
                continue
              if self.l2vpn_data[4:].startswith( "Type Ethernet" ):
                try:
                  self.l2vpn_ac_groups_received += \
                    "\"vpi/vci\":\"\","
                  self.l2vpn_ac_groups_received += \
                    "\"number ranges\":\"\","
                except:
                  self.l2vpn_ac_groups_received += ""
                continue
              if self.l2vpn_data[4:].startswith( "Type VLAN" ):
                try:
                  self.l2vpn_ac_groups_received += "\"vpi/vci\":\"\","
                  self.l2vpn_ac_groups_received += \
                    "\"number ranges\":\"{}\",".format( self.l2vpn_data_list[4] )
                except:
                  self.l2vpn_ac_groups_received += ""
                continue
              if self.l2vpn_data[4:].startswith( "VLAN ranges" ):
                try:
                  self.l2vpn_ac_groups_received += \
                       "\"vlan ranges\":\"{} {}\",".\
                       format( self.l2vpn_data_list[2].replace( "[", "" ).replace( ",", "" ),
                               self.l2vpn_data_list[3].replace( "]", "" ) )
                except:
                  self.l2vpn_ac_groups_received += ""
                continue
              if self.l2vpn_data[4:].startswith( "MTU" ):
                try:
                  self.l2vpn_ac_groups_received += \
                      "\"mtu\":\"{}\",".format( self.l2vpn_data_list[1].replace( ";", "" ))
                  self.l2vpn_ac_groups_received += \
                    "\"xc id\":\"{}\",".format( self.l2vpn_data_list[4].replace( ";", "" ) )
                  self.l2vpn_ac_groups_received += \
                    "\"internetwork\":\"{}\",".format( self.l2vpn_data_list[6] )
                except:
                  self.l2vpn_ac_groups_received += ""
                continue
              if self.l2vpn_data[6:].startswith( "packets" ):
                try:
                  self.l2vpn_ac_groups_received += "\"packets received\":\"{}\",".\
                       format( "0" )
                  self.l2vpn_ac_groups_received += "\"packets sent\":\"{}\",".\
                       format( "0" )
                  # FIXME self.l2vpn_ac_groups_received += "\"packets received\":\"{}\",". \
                  # FIXME   format( self.l2vpn_data_list[2].split( "," )[0] )
                  # FIXME self.l2vpn_ac_groups_received += "\"packets sent\":\"{}\",". \
                  # FIXME   format( self.l2vpn_data_list[4] )
                except:
                  self.l2vpn_ac_groups_received += ""
                continue
              if self.l2vpn_data[6:].startswith( "bytes" ):
                try:
                  self.l2vpn_ac_groups_received += "\"bytes received\":\"{}\",".\
                       format( "0" )
                  self.l2vpn_ac_groups_received += "\"bytes sent\":\"{}\",".\
                       format( "0" )
                  # FIXME self.l2vpn_ac_groups_received += "\"bytes received\":\"{}\",". \
                  # FIXME   format( self.l2vpn_data_list[2].split( "," )[0] )
                  # FIXME self.l2vpn_ac_groups_received += "\"bytes sent\":\"{}\",". \
                  # FIXME   format( self.l2vpn_data_list[4] )
                except:
                  self.l2vpn_ac_groups_received += ""
                continue
              if self.l2vpn_data[6:].startswith( "drops" ):
                try:
                  self.l2vpn_ac_groups_received += "\"illegal vlans\":\"{}\",". \
                       format( self.l2vpn_data.split()[3].replace( ",", "" ) )
                  self.l2vpn_ac_groups_received += "\"illegal length\":\"{}\",". \
                       format( self.l2vpn_data_list[6] )
                except:
                  self.l2vpn_ac_groups_received += ""
              continue
            continue
          if self.l2vpn_data[2:].startswith( "PW:" ):
            try:
              self.l2vpn_pw_groups_received += "\"neighborpw {}\":{{\"id\":\"{}\",\"state\":\"{}\",\"mode\":\"{}\"}}". \
                format( self.l2vpn_data_list[2].replace( ",", "" ),
                        self.l2vpn_data_list[5].replace( ",", "" ),
                        self.l2vpn_data_list[8],
                        self.l2vpn_data_list[10] )
              self.pw_title = "pwgroup {}".format( self.l2vpn_data_list[2].replace( ",", "" ) )
            except:
              self.l2vpn_pw_groups_received += ""
            if self.first_group:
              self.l2vpn_pw_groups_received += ",\"{}\":{{".format( self.pw_title )
            for self.l2vpn_data in self.l2vpn_data_fd:
              self.first_group = False
              if self.l2vpn_data.startswith( "Group" ) or \
                 self.l2vpn_data[2:].startswith( "AC" ) or \
                 self.l2vpn_data[2:].startswith( "PW" ):
                self.l2vpn_data_fd.seek( self.line_length )
                self.l2vpn_pw_groups_received = self.l2vpn_pw_groups_received[:-1] + "},"
                self.first_group = True
                break
              self.line_length += len( self.l2vpn_data )
              self.l2vpn_data_list = self.l2vpn_data.split()
              if self.l2vpn_data.startswith( "\n" ):
                continue
              if self.l2vpn_data[4:].startswith( "PW class" ):
                try:
                  self.l2vpn_pw_groups_received += \
                    "\"class\":\"{}\",".format( self.l2vpn_data_list[2].replace( ",", "" ) )
                  self.l2vpn_pw_groups_received += \
                    "\"xc id\":\"{}\",".format( self.l2vpn_data_list[5] )
                except:
                  self.l2vpn_pw_groups_received += ""
                continue
              if self.l2vpn_data[4:].startswith( "Encapsulation" ):
                try:
                  self.l2vpn_pw_groups_received += \
                    "\"encapsulation\":\"{}\",".format( self.l2vpn_data_list[1].replace( ",", "" ) )
                  self.l2vpn_pw_groups_received += \
                    "\"protocol\":\"{}\",".format( self.l2vpn_data_list[3] )
                except:
                  self.l2vpn_pw_groups_received += ""
                continue
              if self.l2vpn_data[4:].startswith( "Source address" ):
                try:
                  self.l2vpn_pw_groups_received += \
                    "\"source address\":\"{}\",".format( self.l2vpn_data_list[2] )
                except:
                  self.l2vpn_pw_groups_received += ""
                continue
              if self.l2vpn_data[4:].startswith( "PW type" ):
                try:
                  self.pw_type = \
                       self.l2vpn_data.split( "," )[0][len(self.l2vpn_data_list[0]) +
                                                       len(self.l2vpn_data_list[1]) + 6:]
                  self.l2vpn_pw_groups_received += \
                    "\"type\":\"{}\",".format( self.pw_type )
                  self.l2vpn_pw_groups_received += \
                    "\"control word\":\"{}\",".format( self.l2vpn_data.split( "," )[1].
                                                                       split( "word" )[1].split()[0] )
                  self.l2vpn_pw_groups_received += \
                    "\"interworking\":\"{}\",".format( self.l2vpn_data.split( "," )[2].split()[1] )
                except:
                  self.l2vpn_pw_groups_received += ""
                continue
              if self.l2vpn_data[4:].startswith( "PW backup" ):
                try:
                  self.l2vpn_pw_groups_received += \
                    "\"backup\":\"{}\",".format( self.l2vpn_data_list[2] )
                  self.l2vpn_pw_groups_received += \
                    "\"delay\":\"{} {}\",".format( self.l2vpn_data_list[4], self.l2vpn_data_list[5] )
                except:
                  self.l2vpn_pw_groups_received += ""
                continue
              if self.l2vpn_data[4:].startswith( "Sequencing" ):
                try:
                  self.l2vpn_pw_groups_received += \
                    "\"sequence\":\"{}\",".format( " ".join( self.l2vpn_data_list[1:] ) )
                except:
                  self.l2vpn_pw_groups_received += ""
                continue
              if self.l2vpn_data[4:].startswith( "PW Status" ):
                try:
                  self.l2vpn_pw_groups_received += \
                    "\"status\":\"{}\",".format( self.l2vpn_data_list[2] )
                except:
                  self.l2vpn_pw_groups_received += ""
                continue
              if self.l2vpn_data[6:].startswith( "Label" ):
                try:
                  self.l2vpn_pw_groups_received += \
                    "\"label\":\"{} {}\",".format( self.l2vpn_data_list[1], self.l2vpn_data_list[2] )
                except:
                  self.l2vpn_pw_groups_received += ""
                continue
              if self.l2vpn_data[6:].startswith( "Group ID" ):
                try:
                  self.l2vpn_pw_groups_received += \
                    "\"group id\":\"{} {}\",".format( self.l2vpn_data_list[2], self.l2vpn_data_list[3] )
                except:
                  self.l2vpn_pw_groups_received += ""
                continue
              if self.l2vpn_data[6:].startswith( "Interface" ):
                try:
                  self.l2vpn_pw_groups_received += \
                    "\"interface\":\"{} {}\",".format( self.l2vpn_data_list[1], self.l2vpn_data_list[2] )
                except:
                  self.l2vpn_pw_groups_received += ""
                continue
              if self.l2vpn_data[6:].startswith( "MTU" ):
                try:
                  self.l2vpn_pw_groups_received += \
                    "\"mtu\":\"{} {}\",".format( self.l2vpn_data_list[1], self.l2vpn_data_list[2] )
                except:
                  self.l2vpn_pw_groups_received += ""
                continue
              if self.l2vpn_data[6:].startswith( "Control word" ):
                try:
                  self.l2vpn_pw_groups_received += \
                    "\"status control word\":\"{} {}\",".format( self.l2vpn_data_list[2], self.l2vpn_data_list[3] )
                except:
                  self.l2vpn_pw_groups_received += ""
                continue
              if self.l2vpn_data[6:].startswith( "PW type" ):
                try:
                  self.l2vpn_pw_groups_received += \
                    "\"pw type\":\"{} {}\",".format( self.l2vpn_data_list[2], self.l2vpn_data_list[3] )
                except:
                  self.l2vpn_pw_groups_received += ""
                continue
              if self.l2vpn_data[6:].startswith( "VCCV" ):
                try:
                  self.l2vpn_pw_groups_received += \
                    "\"vccv {} type\":\"{} {}\",".format( self.l2vpn_data_list[1],
                                                          self.l2vpn_data_list[3],
                                                          self.l2vpn_data_list[4] )
                except:
                  self.l2vpn_pw_groups_received += ""
                continue
              if self.l2vpn_data[6:].startswith( "packets" ):
                try:
                  self.l2vpn_pw_groups_received += "\"packets received\":\"{}\",". \
                    format( "0" )
                  self.l2vpn_pw_groups_received += "\"packets sent\":\"{}\",". \
                    format( "0" )
                  # FIXME self.l2vpn_pw_groups_received += "\"packets received\":\"{}\",". \
                  # FIXME   format( self.l2vpn_data_list[2].split( "," )[0] )
                  # FIXME self.l2vpn_pw_groups_received += "\"packets sent\":\"{}\",". \
                  # FIXME   format( self.l2vpn_data_list[4] )
                except:
                  self.l2vpn_pw_groups_received += ""
                continue
              if self.l2vpn_data[6:].startswith( "bytes" ):
                try:
                  self.l2vpn_pw_groups_received += "\"bytes received\":\"{}\",". \
                    format( "0" )
                  self.l2vpn_pw_groups_received += "\"bytes sent\":\"{}\",". \
                    format( "0" )
                  # FIXME self.l2vpn_pw_groups_received += "\"bytes received\":\"{}\",". \
                  # FIXME   format( self.l2vpn_data_list[2].split( "," )[0] )
                  # FIXME self.l2vpn_pw_groups_received += "\"bytes sent\":\"{}\",". \
                  # FIXME   format( self.l2vpn_data_list[4] )
                except:
                  self.l2vpn_pw_groups_received += ""
                continue
              if self.l2vpn_data[6:].startswith( "drops" ):
                try:
                  self.l2vpn_pw_groups_received += "\"illegal vlans\":\"{}\",". \
                    format( self.l2vpn_data.split()[3].replace( ",", "" ) )
                  self.l2vpn_pw_groups_received += "\"illegal length\":\"{}\",". \
                    format( self.l2vpn_data_list[6] )
                except:
                  self.l2vpn_pw_groups_received += ""
              continue
            continue
        #-----------------------------------------------------------------------------------------
        if self.l2vpn_pw_groups_received == "":
          self.l2vpn_ac_groups_received = self.l2vpn_ac_groups_received[:-1]
          self.l2vpn_ac_groups_received += "}"
        elif self.l2vpn_ac_groups_received == "":
          self.l2vpn_pw_groups_received = self.l2vpn_pw_groups_received[:-1]
          self.l2vpn_pw_groups_received += "}"
        else:
          self.l2vpn_pw_groups_received = self.l2vpn_pw_groups_received[:-1]
        self.l2vpn_xconnect_table.append( # "{" + \
                                          "{{\"show l2vpn xconnect detail\":" \
                                          "\"show l2vpn xconnect detail\"," \
                                          "\"device\":\"{}\"," \
                                          "\"group\":\"{}\"," \
                                          "\"xconnect\":\"{}\"," \
                                          "\"state\":\"{}\"," \
                                          "\"interwork\":\"{}\"," \
                                          "{}" \
                                          "{}}};". \
                                            format( self.device,
                                                    self.l2vpn_group_name_received,
                                                    self.l2vpn_xconnect_name_received,
                                                    self.l2vpn_group_state_received,
                                                    self.l2vpn_group_interwork_received,
                                                    self.l2vpn_ac_groups_received,
                                                    self.l2vpn_pw_groups_received
                                                  ) #+ \
                                          # "};"
                                         )
        continue
    #-------------------------------------------------------------------------------------------------------------
    for seed_dictionary in self.l2vpn_xconnect_table:
      # FIXME DEBUG ONLY print(seed_dictionary)
      try:
        self.l2vpn_xconnect_analysis_fd.write(seed_dictionary + "\n")
      except:
        print("Seed dictionary file write failed.")
    return()
  #----------------------------------------------------------------------------------------------------------------
  #----------------------------------------------------------------------------------------------------------------
  def build_juniper_analysis_seed_file( self ):
    self.l2vpn_xconnect_table = []
    for self.l2vpn_data in self.l2vpn_data_fd:
      if self.l2vpn_data.startswith( "\n" ):
        break
      else:
        try:
          self.interface = self.l2vpn_data.split()[0]
        except:
          self.interface = ""
        try:
          self.system = self.l2vpn_data.split()[1]
        except:
          self.system = ""
        try:
          self.level = self.l2vpn_data.split()[2]
        except:
          self.level = ""
        try:
          self.state = self.l2vpn_data.split()[3]
        except:
          self.state = ""
        try:
          self.hold = self.l2vpn_data.split()[4]
        except:
          self.hold = ""
        try:
          self.snpa = self.l2vpn_data.split()[5]
        except:
          self.snpa = ""
        self.l2vpn_xconnect_table.append( # "{" + \
                                     "{{\"show l2vpn xconnect detail\":\"show_l2vpn_xconnect\",\"device\":\"juniper\"," \
                                     "\"interface\":\"{}\",\"system\":\"{}\"," \
                                     "\"level\":\"{}\",\"state\":\"{}\"," \
                                     "\"hold\":\"{}\",\"snpa\":\"{}\"}};".format( self.interface,
                                                                                  self.system,
                                                                                  self.level,
                                                                                  self.state,
                                                                                  self.hold,
                                                                                  self.snpa ) # + \
                                     # "};"
                                    )
    for seed_dictionary in self.l2vpn_xconnect_table:
      # FIXME DEBUG print(seed_dictionary)
      try:
        self.l2vpn_xconnect_analysis_fd.write(seed_dictionary + "\n")
      except:
        print("Seed dictionary file write failed.")
    return()
###################################################################################################################
