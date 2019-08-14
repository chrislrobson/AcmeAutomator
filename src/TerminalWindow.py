##################################################################################################################
# TerminalWindow
# Multiple Network Device Configuration and Traffic Generator Terminal Window
# Author: Christopher Robson
# Copyright by:  Christopher Robson
# Copyright date: 01Jan2016
# This software is not FREE!  Use or destribution of the software system and its
# subsystem modules, libraries, configuration file and "seed" file without the
# express permission of the author is strictly PROHIBITED!
##################################################################################################################
import subprocess
##################################################################################################################
class TerminalWindow:
  "Testbed Tester Terminal"
  #---------------------------------------------------------------------------------------------------------------
  def __init__(self):
    self.name = "Testbed Tester Terminal"
  #---------------------------------------------------------------------------------------------------------------
  def run_terminal_window( self ):
    cmd_list = []
    cmd = ""
    cmd = "xfce4-terminal --geometry 100x40+5+40"
    cmd_strs_list = cmd.split()
    for item in cmd_strs_list:
      cmd_list.append( item )
    output = subprocess.Popen( cmd_list,
                               stdout = subprocess.PIPE,
                               stderr = subprocess.PIPE )
##################################################################################################################
