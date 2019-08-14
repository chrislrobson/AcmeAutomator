##################################################################################################################
# Applications
#  Applications
# Author: Christopher Robson
# Copyright by:  Christopher Robson
# Copyright date: 01Jan2016
# This software is not FREE!  Use or destribution of the software system and its
# subsystem modules, libraries, configuration file and "seed" file without the
# express permission of the author is strictly PROHIBITED!
##################################################################################################################
import subprocess
##################################################################################################################
class Applications:
  "Testbed Tester Office Application"
  #---------------------------------------------------------------------------------------------------------------
  def __init__(self):
    self.name = "Testbed Tester Applications"
  #---------------------------------------------------------------------------------------------------------------
  def run_office( self ):
    cmd_list = []
    cmd = ""
    cmd = "xfce4-terminal -e libreoffice"
    cmd_strs_list = cmd.split()
    for item in cmd_strs_list:
      cmd_list.append( item )
    output = subprocess.Popen( cmd_list,
                               stdout = subprocess.PIPE,
                               stderr = subprocess.PIPE )
##################################################################################################################
