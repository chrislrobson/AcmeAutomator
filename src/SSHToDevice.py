##################################################################################################################
# SSHToDevice
# Multiple Network Device Configuration and Traffic Generator Terminal Window
# Author: Christopher Robson
# Copyright by:  Christopher Robson
# Copyright date: 01Jan2016
# This software is not FREE!  Use or destribution of the software system and its
# subsystem modules, libraries, configuration file and "seed" file without the
# express permission of the author is strictly PROHIBITED!
##################################################################################################################
import subprocess
import ast
import os
#-----------------------------------------------------------------------------------------------------------------
# Home grown
#-----------------------------------------------------------------------------------------------------------------
from Globals import Globals
#-----------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------
class SSHToDevice:
  "SSH to Device"
  #---------------------------------------------------------------------------------------------------------------
  def __init__( self ):
    self.name = "SSH to Device"
    self.cmd = "xfce4-terminal --geometry 100x40+5+40"
    self.cmd_ssh0 = "-x"
    self.cmd_ssh1 = "ssh"
  #---------------------------------------------------------------------------------------------------------------
  #---------------------------------------------------------------------------------------------------------------
  def ssh_to_device( self, profile_directory ):
    dut_ip_test_list = Globals().get_dut_to_be_tested_list()
    dut_ip_to_be_tested_dict = Globals().get_dut_ip_list_dict()
    if not dut_ip_test_list:
      return ("SSHToDevice FAILED: NO devices selected test has aborted!\n")
    for dut_ip in dut_ip_test_list:
      self.cmd_list = self.cmd.split()
      self.ip = dut_ip.split()[0]
      self.ip_and_name = "".join( dut_ip.split( ) )
      dut_filename = dut_ip_to_be_tested_dict[self.ip_and_name]
      try:
        with open( profile_directory +
                   dut_filename, 'r' ) as devicectlFD:
          for devicectl in devicectlFD:
            if devicectl == '{\n' or devicectl == '}\n' or \
               devicectl == '\r\n' or devicectl == '\n' :
              continue
            elif devicectl.startswith( '#' ):
              continue
            else:
              try:
                devicectl_dict   = ast.literal_eval( devicectl.split( ';' )[0] )
              except:
                return( "SSHToDevice: FAILED to parse SSH user id." )
              try:
                comm_dict = devicectl_dict['connect']
              except:
                continue
              try:
                comm_network_dict = comm_dict['sshchannel']
                title_msg = "--title=USERNAME: {}".format( comm_network_dict['username'] )
                self.cmd_list.append( title_msg )
                self.cmd_list.append( self.cmd_ssh0 )
                self.cmd_list.append( self.cmd_ssh1 )
                self.cmd_list.append( "-l" )
                self.cmd_list.append( comm_network_dict['username'] )
                break
              except:
                return( "SSHToDevice: FAILED to parse SSH user id." )
      except:
        return( "SSHToDevice: FAILED to open configuration seed file." )
      self.cmd_list.append( self.ip )
      output = subprocess.Popen( self.cmd_list,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE )
    return( " SSHToDevice: Successful")
##################################################################################################################
