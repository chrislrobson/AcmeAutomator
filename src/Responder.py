####################################################################################################################
# Python Qt5 Testbed Tester Save
# MODULE:  
# Author: Christopher Robson
# Copyright by:  Christopher Robson
# Copyright date: 01Jan2016
# This software is not FREE!  Use or destribution of the software system and its
# subsystem modules, libraries, configuration file and "seed" file without the
# express permission of the author is strictly PROHIBITED!
# FUNCTION:  Module provides the results from a network device "configure save" command suite.
#            Message passing between the GUI and the testing modules is accomplished
#            using Qt5 "Signal and Slot" processing system.
####################################################################################################################
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
# Home grown
#------------------------------------------------------------------------------------------------------------------
from Globals import *
#------------------------------------------------------------------------------------------------------------------
# ProcessResponse
# calling method: reply_to_send = ProcessResponse().process_response( "Do you wish to proceed? [no]: " )
#------------------------------------------------------------------------------------------------------------------
class ProcessResponse:
  "Process Respnse"
  #----------------------------------------------------------------------------------------------------------------
  def __init__(self):
    self.name = "Process Response"
  #----------------------------------------------------------------------------------------------------------------
  def process_response( self, response ):
    return( Globals.responses.get( response ) )
####################################################################################################################
