####################################################################################################################
# Python Qt5 Testbed Tester Show Interface Status String Parser
# MODULE:  ShowInterfaceStatusSeedAnalysisFileBuilder
# Author: Christopher Robson
# Copyright by:  Christopher Robson
# Copyright date: 01Jan2016
# This software is not FREE!  Use or destribution of the software system and its
# subsystem modules, libraries, configuration file and "seed" file without the
# express permission of the author is strictly PROHIBITED!
# FUNCTION:  Module parses a Cisco 7600 "show interfaces status reply per line returning
#            a string to be converted to a dictionary
####################################################################################################################
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
# Home grown
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
# Show Interface Status SeedAnalysis File Builder
#------------------------------------------------------------------------------------------------------------------
class ShowInterfaceStatusStringParser:
  "Show Interface Status String Parser"
  #----------------------------------------------------------------------------------------------------------------
  def __init__( self, parent = None ):
    self.name = "Show Interface Status String Pareser"
  #----------------------------------------------------------------------------------------------------------------
  #----------------------------------------------------------------------------------------------------------------
  # FIXME !!! IF THERE EERY WAS UGLY CODE THIS IS iT BUT IT GETS THE JOB DONE !!!
  # FIXME REWORK THIS IS A HIGH PRIORITY!!!!
  # FIXME The challange is to process a string where the "onlY constant is "some" field locations
  # FIXME Fields line the name may or maynot be present and the duplex field may bleed into the
  # FIXME vlan field to its left (aka Cisco crappy formatting strikes again !!)
  #   123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890
  #   0        1         2         3         4         5         6         7         8         9
  #   Fa4/1        "NIPR IOS testing  connected    routed       full    100 100BaseFX MM
  #   Gi7/1                           notconnect   1            full   1000 No Transceiver
  #----------------------------------------------------------------------------------------------------------------
  def show_interface_status_string_parser( self, status_data ):
    self.interface = ""
    self.name = ""
    self.status = ""
    self.vlan = ""
    self.duplex = ""
    self.speed = ""
    self.type_intf = ""
    length_str = len( status_data )
    i = 0
    for x in range( length_str ):
      if status_data[x] == " ":
        break
      else:
        self.interface += status_data[i]
        i += 1
    r = length_str - i
    o = i
    for x in range( r ):
      if i > 31:
        break
      if status_data[o + x] == " ":
        i += 1
        continue
      else:
        r = length_str - i
        o = i
        for x in range( r ):
          if i > 31:
            break
          else:
            self.name += status_data[o + x]
            i += 1
    self.name = " ".join( self.name.replace( "\"", "" ).split() )
    r = length_str - i
    o = i
    for x in range( r ):
      if status_data[o + x] == " ":
        r = length_str - i
        o = i
        for x in range( r ):
          if status_data[o + x] == " ":
            i += 1
            continue
          else:
            break
        break
      else:
        self.status += status_data[o + x]
        i += 1
    r = length_str - i
    o = i
    for x in range( r ):
      if status_data[o + x] == " ":
        r = length_str - i
        o = i
        for x in range( r ):
          if status_data[o + x] == " ":
            i += 1
            continue
          else:
            break
        break
      else:
        self.vlan += status_data[o + x]
        i += 1
    r = length_str - i
    o = i
    for x in range( r ):
      if status_data[o + x] == " ":
        r = length_str - i
        o = i
        for x in range( r ):
          if status_data[o + x] == " ":
            i += 1
            continue
          else:
            break
        break
      else:
        self.duplex += status_data[o + x]
        i += 1
    r = length_str - i
    o = i
    for x in range( r ):
      if status_data[o + x] == " ":
        r = length_str - i
        o = i
        for x in range( r ):
          if status_data[o + x] == " ":
            i += 1
            continue
          else:
            break
        break
      else:
        self.speed += status_data[o + x]
        i += 1
    r = length_str - i
    o = i
    for x in range( r ):
      if status_data[o + x] == "\n":
        continue
      else:
        self.type_intf += status_data[o + x]
    #--------------------------------------------------------------------------------------------------------------
    return( self.interface,
            self.name,
            self.status,
            self.vlan,
            self.duplex,
            self.speed,
            self.type_intf
          )
####################################################################################################################
