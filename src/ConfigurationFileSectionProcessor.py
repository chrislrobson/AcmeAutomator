#####################################################################################################################
# Python Qt5 Testbed Tester Configuration File Section Processor
# Author: Christopher Robson
# Copyright by:  Christopher Robson
# Copyright date: 01Jan2016
# This software is not FREE!  Use or destribution of the software system and its
# subsystem modules, libraries, configuration file and "seed" file without the
# express permission of the author is strictly PROHIBITED!
# FUNCTION: These classes create the selected sections of a configuration file
#####################################################################################################################
import itertools
from PyQt5 import QtCore
import ipaddress
from netaddr import *
#-------------------------------------------------------------------------------------------------------------------
# Home grown stuff
#-------------------------------------------------------------------------------------------------------------------
import MainGUI
from Globals import *
#-------------------------------------------------------------------------------------------------------------------
class ConfigurationFileSectionProcessor( QtCore.QThread ):
  " Configuration File Section Processor"
  #-----------------------------------------------------------------------------------------------------------------
  def __init__(self, parent = None ):
    super( ConfigurationFileSectionProcessor, self).__init__( parent )
    self.parent = parent
    self.name = " Configuration File Section Processor"
  #-----------------------------------------------------------------------------------------------------------------
  def configuration_file_section_processor( self ):
    pass
#-------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------
class MANAGEMENT:
  #-----------------------------------------------------------------------------------------------------------------
  def __init__(self, parent = None ):
    self.parent = parent
    self.name = "MANAGEMENT"
    self.row_count = parent.row_count
    self.section = []
  #-----------------------------------------------------------------------------------------------------------------
  def execute( self, cell ):
    self.cell = cell
    self.cell_data = next( self.cell )
    self.count_str = self.cell_data.value.split()[1]
    if not self.count_str.isdigit():
      self.count = 1
    else:
      self.counter = int( self.count_str )
    self.cell_repeater = itertools.tee( self.cell, self.counter )
    for self.cell_current in self.cell_repeater:
      for i in range( self.row_count ):
        self.cell_data = next( self.cell_current )
        if isinstance(self.cell_data.value, str):
          if self.cell_data.value.isupper() and self.cell_data.value in self.__class__.__name__:
            pass
          elif self.cell_data.value.isupper() and not self.cell_data.value in self.__class__.__name__:
            break
          else:
            self.section.append( self.cell_data.value )
      self.section.append( "!" )
    self.section.append( "!" )
    return( self.section, self.cell_current )
#-------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------
class VRF:
  #-----------------------------------------------------------------------------------------------------------------
  def __init__(self, parent = None ):
    self.parent = parent
    self.name = "VRF"
    self.row_count = parent.row_count
    self.section = []
  #-----------------------------------------------------------------------------------------------------------------
  def execute( self, cell ):
    self.count = 0
    self.cell = cell
    self.cell_data = next( self.cell )
    self.count_str = self.cell_data.value.split()[1]
    if not self.count_str.isdigit():
      self.counter = 1
    else:
      self.counter = int( self.count_str )
    self.cell_repeater = itertools.tee( self.cell, self.counter )
    for self.cell_current in self.cell_repeater:
      for i in range( self.row_count ):
        self.cell_data = next( self.cell_current )
        if isinstance(self.cell_data.value, str):
          if self.cell_data.value.isupper() and self.cell_data.value in self.__class__.__name__:
            pass
          elif self.cell_data.value.startswith( "ENDSECTION" ):
            self.count += 1
            break
          elif self.cell_data.value.isupper() and not self.cell_data.value in self.__class__.__name__:
            break
          elif self.cell_data.value.startswith( "vrf definition" ):
            a = ""
            b = ""
            l = 0
            for chr in self.cell_data.value.split()[2]:
              #-------------------------------------------------------------------------------------------------
              # FIXME This is really ugly code to only digitize last characters if numbers
              # FIXME FIND A BETTER WAY LATER IT WORKS NOW SO MOB+VE ON TO OTHER PROBLEMS
              if chr.isdigit() and a.__len__():
                b += chr
                l = len(b)
              else:
                if b: # OOps last character was a digit before ascii treat as character
                  a += b
                  b = ""
                  l = 0
                a += chr
            c = int(b) + self.count
            self.section.append( "{} {} {}{number:0{width}d}".format( self.cell_data.value.split()[0],
                                                                        self.cell_data.value.split()[1],
                                                                        a, width=l, number=c ) )
          elif "rd" in self.cell_data.value:
            self.section.append( "{} {}:{}".\
                                   format( self.cell_data.value.split()[0],
                                           int( self.cell_data.value.split()[1].split( ":" )[0] ) + self.count,
                                           int( self.cell_data.value.split()[1].split( ":" )[1] ) + self.count ) )
          elif "export" in self.cell_data.value or "import" in self.cell_data.value:
            self.section.append( "{} {} {}:{}".\
                                   format( self.cell_data.value.split()[0],
                                           self.cell_data.value.split()[1],
                                           int( self.cell_data.value.split()[2].split( ":" )[0] ) + self.count,
                                           int( self.cell_data.value.split()[2].split( ":" )[1] ) + self.count ) )
          else:
            self.section.append( "{}".format( self.cell_data.value ) )
      self.section.append( "!" )
    self.section.append( "!" )
    return( self.section, self.cell_current )
#-------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------
class VLAN:
  #-----------------------------------------------------------------------------------------------------------------
  def __init__( self, parent = None ):
    self.parent = parent
    self.name = "VLN"
    self.row_count = parent.row_count
    self.section = []
  #-----------------------------------------------------------------------------------------------------------------
  def execute( self, cell ):
    self.count = 0
    self.cell = cell
    self.cell_data = next( self.cell )
    self.count_str = self.cell_data.value.split()[1]
    if not self.count_str.isdigit():
      self.counter = 1
    else:
      self.counter = int( self.count_str )
    self.cell_repeater = itertools.tee( self.cell, self.counter )
    for self.cell_current in self.cell_repeater:
      for i in range( self.row_count ):
        self.cell_data = next( self.cell_current )
        if isinstance( self.cell_data.value, str ):
          if self.cell_data.value.isupper() and self.cell_data.value in self.__class__.__name__:
            pass
          elif self.cell_data.value.startswith( "ENDSECTION" ):
            self.count += 1
            break
          elif self.cell_data.value.isupper() and not self.cell_data.value in self.__class__.__name__:
            self.count += 1
            break
          elif self.cell_data.value.startswith( "interface" ):
            self.vlan = str( int( self.cell_data.value.split( "." )[1] ) + self.count )
            self.section.append( "{}.{}".format( self.cell_data.value.split( "." )[0], self.vlan ) )
          elif self.cell_data.value.startswith( "description" ) or \
               self.cell_data.value.startswith( "encapsulation" ):
            self.vlan = str( int( self.cell_data.value.split()[-1] ) + self.count )
            self.descrip_encap_str = ""
            for word in self.cell_data.value.split()[:-1]:
              self.descrip_encap_str += "{} ".format( word )
            self.descrip_encap_str += "{}".format( self.vlan )
            self.section.append( "{}".format( self.descrip_encap_str ) )
          elif self.cell_data.value.startswith( "vrf forwarding" ):
            a = ""
            b = ""
            l = 0
            for chr in self.cell_data.value.split()[2]:
              # -------------------------------------------------------------------------------------------------
              # FIXME This is really ugly code to only digitize last characters if numbers
              # FIXME FIND A BETTER WAY LATER IT WORKS NOW SO MOB+VE ON TO OTHER PROBLEMS
              if chr.isdigit() and a.__len__():
                b += chr
                l = len( b )
              else:
                if b:  # OOps last character was a digit before ascii treat as character
                  a += b
                  b = ""
                  l = 0
                a += chr
            c = int( b ) + self.count
            self.section.append( "{} {} {}{number:0{width}d}".format( self.cell_data.value.split()[0],
                                                                        self.cell_data.value.split()[1],
                                                                        a, width = l, number = c ) )
          elif self.cell_data.value.startswith( "ip address" ):
            self.ip_mask = self.cell_data.value.split()[-1]
            self.next_ip = IPAddress( self.cell_data.value.split()[-2] ) + self.count
            self.ip_subnet = IPNetwork( "{}/{}".format( self.next_ip, self.ip_mask ) ).cidr
            for self.host in ipaddress.ip_network( "{}".format( self.ip_subnet.cidr ) ).hosts():
              if str( self.next_ip ) == self.host.exploded:
                break
            else:
              self.next_ip = IPAddress( str( self.next_ip ) ) + 1
            self.section.append( "{} {}".format( self.next_ip, self.cell_data.value.split()[-1] ) )
          else:
            self.section.append( "{}".format( self.cell_data.value ) )
      self.section.append( "!" )
    self.section.append( "!" )
    return (self.section, self.cell_current)
#-------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------
class BGP:
  #-----------------------------------------------------------------------------------------------------------------
  def __init__( self, parent = None ):
    self.parent = parent
    self.name = "BGP"
    self.row_count = parent.row_count
    self.section = []
    self.ip_mask = "255.255.255.255"
  #-----------------------------------------------------------------------------------------------------------------
  def execute( self, cell ):
    self.count = 0
    self.cell = cell
    self.cell_data = next( self.cell )
    self.count_str = self.cell_data.value.split()[1]
    if not self.count_str.isdigit():
      self.counter = 1
    else:
      self.counter = int( self.count_str )
    self.cell_repeater = itertools.tee( self.cell, self.counter )
    for self.cell_current in self.cell_repeater:
      for i in range( self.row_count ):
        self.cell_data = next( self.cell_current )
        if isinstance( self.cell_data.value, str ):
          if self.cell_data.value.isupper() and self.cell_data.value in self.__class__.__name__:
            pass
          elif self.cell_data.value.startswith( "SUBNETMASK" ):
            self.ip_mask = self.cell_data.value.split()[1]
          elif self.cell_data.value.startswith( "ENDSECTION" ):
            self.count += 1
            break
          elif self.cell_data.value.isupper() and not self.cell_data.value in self.__class__.__name__:
            self.count += 1
            break
          elif self.cell_data.value.startswith( "neighbor" ):
            self.ip_mask = self.cell_data.value.split()[-1]
            self.next_ip = IPAddress( self.cell_data.value.split()[-2] ) + self.count
            self.ip_subnet = IPNetwork( "{}/{}".format( self.next_ip, self.ip_mask ) ).cidr
            for self.host in ipaddress.ip_network( "{}".format( self.ip_subnet.cidr ) ).hosts():
              if str( self.next_ip ) == self.host.exploded:
                break
            else:
              self.next_ip = IPAddress( str( self.next_ip ) ) + 1
            self.section.append( "{} {}".format( self.next_ip, self.cell_data.value.split()[-1] ) )
          else:
            self.section.append( "{}".format( self.cell_data.value ) )
      self.section.append( "!" )
    self.section.append( "!" )
    return (self.section, self.cell_current)
#-------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------
class IPSLA:
  # -----------------------------------------------------------------------------------------------------------------
  def __init__( self, parent = None ):
    self.parent = parent
    self.name = "IPSLA"
    self.row_count = parent.row_count
    self.section = []
    self.ip_mask = "255.255.255.255"
  # -----------------------------------------------------------------------------------------------------------------
  def execute( self, cell ):
    self.count = 0
    self.cell = cell
    self.cell_data = next( self.cell )
    self.count_str = self.cell_data.value.split()[1]
    if not self.count_str.isdigit():
      self.counter = 1
    else:
      self.counter = int( self.count_str )
    self.cell_repeater = itertools.tee( self.cell, self.counter )
    for self.cell_current in self.cell_repeater:
      for i in range( self.row_count ):
        self.cell_data = next( self.cell_current )
        if isinstance( self.cell_data.value, str ):
          if self.cell_data.value.isupper() and self.cell_data.value in self.__class__.__name__:
            pass
          elif self.cell_data.value.split()[0] == "SUBNETMASK":
            self.ip_mask = self.cell_data.value.split()[1]
          elif self.cell_data.value.startswith( "ENDSECTION" ):
            self.count += 1
            break
          elif self.cell_data.value.isupper() and not self.cell_data.value in self.__class__.__name__:
            self.count += 1
            break
          elif self.cell_data.value.startswith( "ip sla" ) and self.cell_data.value.split()[-1].isdigit():
            self.vlan = str( int( self.cell_data.value.split()[-1] ) + self.count )
            self.ipsla_str = ""
            for word in self.cell_data.value.split()[:-1]:
              self.ipsla_str += "{} ".format( word )
            self.ipsla_str += "{}".format( self.vlan )
            self.section.append( "{}".format( self.ipsla_str ) )
          elif self.cell_data.value.startswith( "ip sla" ) and self.cell_data.value.split()[2].isalpha():
            self.section.append( "{}".format( self.cell_data.value ) )
          elif self.cell_data.value.startswith( "icmp-echo" ) and \
               self.cell_data.value.split()[1].split( "." )[0].isdigit():
            self.next_ip = IPAddress( self.cell_data.value.split()[1] ) + self.count
            self.ip_subnet = IPNetwork( "{}/{}".format( self.next_ip, self.ip_mask ) ).cidr
            for self.host in ipaddress.ip_network( "{}".format( self.ip_subnet.cidr ) ).hosts():
              if str( self.next_ip ) == self.host.exploded:
                break
            else:
              self.next_ip = IPAddress( str( self.next_ip ) ) + 1
            self.section.append( "{} {}".format( self.next_ip, self.cell_data.value.split()[-1] ) )
          else:
            self.section.append( "{}".format( self.cell_data.value ) )
      self.section.append( "!" )
    self.section.append( "!" )
    return (self.section, self.cell_current)
####################################################################################################################
