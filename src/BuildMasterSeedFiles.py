#####################################################################################################################
# Python Qt5 Testbed Tester Build Master Seed Files
# Author: Christopher Robson
# Copyright by:  Christopher Robson
# Copyright date: 01Jan2016
# This software is not FREE!  Use or destribution of the software system and its
# subsystem modules, libraries, configuration file and "seed" file without the
# express permission of the author is strictly PROHIBITED!
# FUNCTION:  Main GUI interface and processing for the Seed File Building process.
# Developed from QT-Designer, PCUIC4(5) and then heavely modified.
#####################################################################################################################
#--------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------
# PyQt5 Libraries
#--------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------
import ntpath
#--------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------
# Home Grown
#--------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------
# Main Window processor
#--------------------------------------------------------------------------------------------------------------------
class BuildMasterSeedFiles:
  " Build Master Seed Files"
  #------------------------------------------------------------------------------------------------------------------
  def __init__( self, parent = None ):
    self.name = " Build Master Seed Files"
    self.parent = parent
  #------------------------------------------------------------------------------------------------------------------
  def build_master_seed_file( self ):
    self.template_file = self.parent.template_file_to_use
    self.seed_file = self.parent.seed_file_to_use
    self.ip_addresses = self.parent.ip_addresses
    self.parent.message_ListWidget.addItem( "BUILDING MASTER SEED FILE:" )
    for self.ip_address in self.ip_addresses:
      self.parent.message_ListWidget.addItem( self.ip_address +
                                              "-" + ntpath.basename( self.template_file ) +
                                              "-" + ntpath.basename( self.seed_file ) )

