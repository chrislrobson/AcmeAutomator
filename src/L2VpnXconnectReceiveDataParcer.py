####################################################################################################################
# Python Qt5 Testbed Tester L2vpn Xconnect Receive Data Parser
# MODULE:  L2vpnXconnectReceiveDataParcers
# Author: Christopher Robson
# Copyright by:  Christopher Robson
# Copyright date: 01Jan2016
# This software is not FREE!  Use or destribution of the software system and its
# subsystem modules, libraries, configuration file and "seed" file without the
# express permission of the author is strictly PROHIBITED!
# FUNCTION:  Module parces L2VPN data
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
# L2vpn Xconnect Receive Data Parcer
#-----------------------------------------------------------------------
class L2VpnXconnectReceiveDataParcer:
  "L2vpn Xconnect DReceive Data Parcer"
  #----------------------------------------------------------------------------------------------------------------
  def __init__( self, parent = None ):
    self.name = "L2vpn Xconnect Receive Data Parcer"
    self.parent = parent
    self.line_length = 0
    #-----------------------------------------------------------------------------------------------------------
    self.l2vpn_ac_groups_received = ""
    self.l2vpn_pw_groups_received = ""
  #----------------------------------------------------------------------------------------------------------------
  def l2vpn_xconnect_receive_data_parcer( self, device, l2vpn_data_fd, l2vpn_xconnect_received,
                                                                       l2vpn_xconnects_received  ):
    if device == "juniper":
      self.reported_data = self.parce_juniper_l2vpn_xconnect_data( device, l2vpn_data_fd,
                                                                           l2vpn_xconnect_received,
                                                                           l2vpn_xconnects_received  )
    elif device == "cisco":
      self.reported_data = self.parce_cisco_l2vpn_xconnect_data( device, l2vpn_data_fd,
                                                                         l2vpn_xconnect_received,
                                                                         l2vpn_xconnects_received  )
    return()
  #----------------------------------------------------------------------------------------------------------------
  def parce_cisco_l2vpn_xconnect_data( self, device, l2vpn_data_fd,
                                                     l2vpn_xconnect_received,
                                                     l2vpn_xconnects_received ):
    self.device = device
    self.l2vpn_data_fd = l2vpn_data_fd
    self.l2vpn_xconnects_received = l2vpn_xconnects_received
    self.l2vpn_xconnect_received = l2vpn_xconnect_received
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
                    "\"vlan ranges\":\"{} {}\",". \
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
                  self.l2vpn_ac_groups_received += "\"packets received\":\"{}\",". \
                    format( self.l2vpn_data_list[2].split( "," )[0] )
                  self.l2vpn_ac_groups_received += "\"packets sent\":\"{}\",". \
                    format( self.l2vpn_data_list[4] )
                except:
                  self.l2vpn_ac_groups_received += ""
                continue
              if self.l2vpn_data[6:].startswith( "bytes" ):
                try:
                  self.l2vpn_ac_groups_received += "\"bytes received\":\"{}\",". \
                    format( self.l2vpn_data_list[2].split( "," )[0] )
                  self.l2vpn_ac_groups_received += "\"bytes sent\":\"{}\",". \
                    format( self.l2vpn_data_list[4] )
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
                    format( self.l2vpn_data_list[2].split( "," )[0] )
                  self.l2vpn_pw_groups_received += "\"packets sent\":\"{}\",". \
                    format( self.l2vpn_data_list[4] )
                except:
                  self.l2vpn_pw_groups_received += ""
                continue
              if self.l2vpn_data[6:].startswith( "bytes" ):
                try:
                  self.l2vpn_pw_groups_received += "\"bytes received\":\"{}\",". \
                    format( self.l2vpn_data_list[2].split( "," )[0] )
                  self.l2vpn_pw_groups_received += "\"bytes sent\":\"{}\",". \
                    format( self.l2vpn_data_list[4] )
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
        self.l2vpn_xconnects_received.append(
                                             "{{\"show l2vpn xconnect detail\":" \
                                             "\"show l2vpn xconnect detail\"," \
                                             "\"device\":\"{}\"," \
                                             "\"group\":\"{}\"," \
                                             "\"xconnect\":\"{}\"," \
                                             "\"state\":\"{}\"," \
                                             "\"interwork\":\"{}\"," \
                                             "{}" \
                                             "{}}}". \
                                               format( self.device,
                                                       self.l2vpn_group_name_received,
                                                       self.l2vpn_xconnect_name_received,
                                                       self.l2vpn_group_state_received,
                                                       self.l2vpn_group_interwork_received,
                                                       self.l2vpn_ac_groups_received,
                                                       self.l2vpn_pw_groups_received
                                                      )
                                            )
        continue
    return ()
  #----------------------------------------------------------------------------------------------------------------
  #----------------------------------------------------------------------------------------------------------------
  def parce_juniper_l2vpn_xconnect_data( self, device, l2vpn_data_fd,
                                         l2vpn_xconnect_received,
                                         l2vpn_xconnects_received ):
    return()
###################################################################################################################
