####################################################################################################################
# Python Qt5 Testbed Tester Build Seed File
# MODULE:  BuildSeedFile
# Author: Christopher Robson
# Copyright by:  Christopher Robson
# Copyright date: 01Jan2016
# This software is not FREE!  Use or destribution of the software system and its
# subsystem modules, libraries, configuration file and "seed" file without the
# express permission of the author is strictly PROHIBITED!
# FUNCTION:  Module scans for prompt string replies from sent commands.
####################################################################################################################
import time
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
# Home grown
#------------------------------------------------------------------------------------------------------------------
from Globals import *
from Utility import Utility
import ReceivedDataReplyDictionary
from Exceptions import *
from SSHChannelProcessor import SendDataThroughSSHChannel
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
# Build Seed File
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
class BuildTemplateFiles:
  "Build Seed File"
  #------------------------------------------------------------------------------------------------------------
  def __init__( self ):
    self.name = "Build Seed File"
  #------------------------------------------------------------------------------------------------------------
  def build_template_files( self, templates_list ):
    self.templates_list = templates_list
    for self.template in self.templates_list:
      self.build_seed_from_template( self.template )
    return()
  #------------------------------------------------------------------------------------------------------------
  def build_seed_from_template( self, template ):
    self.template = template
    for self.template in self.templates_list:
      self.build_seed_from_template( self.template )
    return()