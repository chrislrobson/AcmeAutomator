"""************************************************************************************************************
Received Decode Data Dictionary
MODULE:  Decode Data Dictionary
Author: Christopher Robson
Copyright by:  Christopher Robson
Copyright date: 08Oct2017
 CRITICAL !! THIS CLASS IS PROPRIETARY AND MY NOT BE REUSED BY ANYONE BUT THE AUTHOR!!
 CRITICAL THIS MODULE DOES NOT BELONG TO ANY CONTRACTING COMPANY OR THE GOVERNMENT!
This software is not FREE!  Use or destribution of the software system and its
subsystem modules, libraries, configuration file and "seed" file without the
express permission of the author is strictly PROHIBITED!
FUNCTION:  Module reads in show command data from a and splits it into a dictionary for processing.
BUILDING THE ORDERED DICTIONARY:
An Ordered Dictionary is built such that a "key" is created from typically each colon or comma seperated word
then a "value" for the associated key is extracted from the string following the key.
Using the "show interface detail" as an example, the associated output for interface data
reported within the first line is:
"Physical interface: ge-0/0/0, Administratively down, Physical link is Down"
The Testbed Tester will first extract the decoder class to call from the
first string seperation as delimited by the first colon, aka, "Physical interface"
This string is morphed into a class name called "PhysicalInterface" and called to process the
current data.
This same string is also morphed into the "key"string, aka, the all lowercase string "physical_interface".
Note spaces must be replaced with underscores or the Ordered Diction processing logical will fail.
Next the remaining string following the key string, aka,
"ge-0/0/0, Administratively down, Physical link is Down" is built into a string which can be converted
to a dictionary element for later analysis processing.
For exmaple, this string would become a string, with some added wrapping characters,
ready to be converted to a dictionary element as show here:
'{"interface":"ge-0/0/0","administration state":"down","link state":" Down"}'
This is used to create the finally Ordered Dictionary KEY:VALUE element,
for this example, it would become something like this:
('physical_interface', '{"interface":"ge-0/0/0","administration state":"down","link state":" Down"}')
EXTRACTION KEY:VALUES from the ORDRED DICTIONARY DURING THE ANALYSIS PROCESS:
To extract the values from each key for use during the analysis logical process,
the following python logical is exploited:
for key, value in list(ORDERED DICTIONARY RECEIVED DATA):
  for key_baseline, value_baseline in list(ORDERED DICTIONARY BASELINE):
    if key == key_baseline and value == value_baseline:
      PASS
    else:
      FAIL
Extracting example:
  self.physical_interface_str = self.decoded[self.key]
  self.physical_interface_dict = ast.literal_eval( self.physical_interface_str )
  self.physical_interface = self.physical_interface_dict["interface"]
****************************************************************************************************************"""
"""
Python Libraries
"""
import os
import importlib
import re
import ahocorasick
"""
Script Libraries
"""
from Globals import *
from MacDataDictionary import *
from CallClass import CallClass
"""
CLASS: DecoderInfo
DESCRIPTION: Decoder instance structures
INPUT: Data string from the router command
OUTPUT: Decoder information such as the class to process the router data
"""
class DecoderInfo:
  "Decoder Info"
  """
  Utility used to convert received data string into a class name string
  """
  decoder_utility = None
  """
  The data string built by importlib from the data received that is converted to a Class
  """
  decoder_class = ""
  """
  Class name string used as the string converted to the class called to process the current data
  """
  decoder_class_name = ""
  """
  Class name string used as dictionary key that has process the data
  """
  decoder_class_name_key = ""
  decoder_class_name_key_added = ""
  """
  Ordered Dictionary structure of decoed data
  """
  decoded_data = None
  """"""
  interface_tag = ""
  """
  The protocol_mesh_tag is used to allow reentry of decoders based on
  statistical data being processed, aka, Protocol or Mesh data
  Protocol_mesh_tag set to "protocol" when processing the Protocol subset,
  likewise set to "mesh" processing Mesh subset
  Reset to "" whenever new Physical or Logical inetreface set being processed.
  """
  protocol_mesh_tag = ""
  """
  Remember location of file data indexes and
  block of data beginning( this is a leading whitespace count, 
  aka, indentation of the data.  Typically this is used to
  determine when the next block processing starts
  """
  previous_index = 0
  current_index = 0
  next_index = 0
  block_index = 0
  previous_block_index = 0
  next_block_index = 0
  """
  DEBUG ONLY FLAG
  """
  debug_flag = False
""""""
"""
CLASS: BlockLocation
DESCRIPTION:  Process block index and/or indentation
INPUT: Current file index and/or indentation
OUTPUT: Sets previous and/or next file index
"""
class BlockLocation:
  "Set Block Location"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def set_block_index( self, index ):
    self.index = index
    self.decoder_instance.block_index = self.index
    return()
  """"""
  def get_block_index( self ):
    return( self.decoder_instance.block_index  )
  """"""
  def set_block_indentation( self, file_descriptor ):
    self.file_descriptor = file_descriptor
    """
    Back track thru the file so it can be determined
    when this block of data is completed.  This is accomplished
    by determining when the number of leading spaces, aka, indentation
    returns to the beginning of the count matching the blocks
    beginning, typicall when the line is indented by 4 spaces.
    """
    self.file_descriptor.seek( self.decoder_instance.previous_index )
    self.previous_data = next( self.file_descriptor )
    self.decoder_instance.block_indentation = len( self.previous_data ) - len( self.previous_data.lstrip() )
    """
    Return the file index location and start processing this block of data
    until the line being processed leading white spaces match the starting
    block location, indecating a new block is beginning
    """
    self.file_descriptor.seek( self.decoder_instance.current_index )
    return( self.decoder_instance.block_indentation )
  """"""
  def get_block_indentation( self ):
    return( self.decoder_instance.block_indentation  )
"""
CLASS: PhysicalInterface
DESCRIPTION: Decode physical interface received data.
INPUT: class to decode data
OUTPUT: decoded data
"""
class PhysicalInterface:
  "Physical Interface"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.data = data
    self.data_list = self.data.split()
    self.dictionary = dictionary
    self.decoder_instance.decoder_class_name_key = " ".join( re.findall( "[A-Z][^A-Z]*",
                                                                         self.__class__.__name__ ) ).lower()
    self.decoder_instance.decoder_class_name_key += " {} ".format( self.data.split( "interface:" )[1].
                                                    split()[0].split( "," )[0].lstrip().replace( ":", "." )
                                                                )
    try:
      self.value = "\"{}\":\"{}\"".format( "interface",
                                           self.data.split( "interface:" )[1].
                                           split()[0].split( "," )[0].lstrip().replace( ":", "." ) )
      try:
        self.value += ",\"{}\":\"{}\"".format( "administration state",
                                               self.data.split( "," )[1].split()[1].lstrip() )
      except:
        self.value += ",\"{}\":\"{}\"".format( "administrative state",
                                               self.data.split( "," )[1].split()[0].lstrip() )
      self.value += ",\"{}\":\"{}\"".format( "link state",
                                             self.data.split( "link is" )[1].lstrip() )
      self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key[:-1]] = \
                                         "{{{}}}".format( self.value )
    except Exception as error:
      self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
      self.dictionary['loggerwidget'].emit(self.message)
      raise Exception
    return()
"""
CLASS: LogicalInterface
DESCRIPTION: Decode logical interface received data.
INPUT: class to decode data
OUTPUT: decoded data
"""
class LogicalInterface:
  "Logical Interface"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.data = data
    self.data_list = self.data.split()
    self.decoder_instance.decoder_class_name_key = " ".join( re.findall( "[A-Z][^A-Z]*",
                                                                         self.__class__.__name__
                                                                       )
                                                           ).lower()
    self.decoder_instance.decoder_class_name_key += " {} ".format( self.data.split()[2].
                                                                   lstrip()
                                                                 )
    self.decoder_instance.decoder_class_name_key_added = ""
    try:
      self.value = "\"{}\":\"{}\"".format( "interface",
                                           self.data.split( "interface" )[1].
                                           split()[0].lstrip().replace( ":", "." ) )
      self.value += ",\"{}\":\"{}\"".format( "index",
                                             self.data.split( "Index" )[1].split()[0][:-1].lstrip() )
      self.value += ",\"{}\":\"{}\"".format( "snmp ifindex",
                                             self.data.split( "SNMP ifIndex" )[1].split()[0][:-1].lstrip() )
      ## Ignore Juniper debug info self.value += ",\"{}\":\"{}\"".format( "generation",
      ## Ignore Juniper debug info                        self.data.split( "Generation" )[1][:-1].lstrip().strip() )
      self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key[:-1]] = \
                                         "{{{}}}".format( self.value )
    except Exception as error:
      self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
      self.dictionary['loggerwidget'].emit(self.message)
      raise Exception
    return()
"""
CLASS: Description
DESCRIPTION:
INPUT:
OUTPUT:
"""
class Description:
  "Description"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.data = data
    try:
      self.value = "\"description\":\"{}\"".format( self.data.split( "Description:" )[1].replace( ":", "." ) )
    except:
      pass
    self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                       self.decoder_instance.decoder_class_name_key_added] = \
                                       "{{{}}}".format( self.value )
    return()
"""
CLASS: CurrentAddress
DESCRIPTION:
INPUT:
OUTPUT:
"""
class CurrentAddress:
  "Current Address"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.data = data
    self.data_list = self.data.split()
    self.value = ""
    """
    Replace colon with "~" so dictionary functions work properly
    """
    try:
      self.value = "\"current address\":\"{}\"".format( self.data_list[2].split( "," )[0].replace( ":", "." ) )
    except:
      pass
    try:
      if self.value == "":
        self.value = "\"hardware address\":\"{}\"".format( self.data_list[5].replace( ":", "." ) )
      else:
        self.value += ",\"hardware address\":\"{}\"".format( self.data_list[5].replace( ":", "." ) )
    except:
      pass
    self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                       self.decoder_instance.decoder_class_name_key_added] = \
                                       "{{{}}}".format( self.value )
    return()
"""
CLASS: LastFlapped
DESCRIPTION:
INPUT:
OUTPUT:
"""
class LastFlapped:
  "Last Flapped"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.data = data
    self.data_list = self.data.split()
    self.field_data = ""
    try:
      self.field_data += self.data_list[3].lstrip().strip()
    except:
      pass
    try:
      self.field_data += self.data_list[4].lstrip().strip()
    except:
      pass
    try:
      self.field_data += self.data_list[5].lstrip().strip()
    except:
      pass
    self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                       self.decoder_instance.decoder_class_name_key_added] = \
                                       "{{\"last flapped\":\"{}\"}}".\
                                         format( self.field_data.replace( ":", "." ) )
    return()
"""
CLASS: StatisticsLastCleared
DESCRIPTION:
INPUT:
OUTPUT:
"""
class StatisticsLastCleared:
  "Statistics Last Cleared"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.data = data
    self.data_list = self.data.split()
    try:
      self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                       self.decoder_instance.decoder_class_name_key_added] = \
                                           "{{\"last cleared\":\"{} {} {}\"}}".format( self.data_list[3].strip(),
                                           self.data_list[4].strip().replace( ":", "." ),
                                           self.data_list[5].strip().replace( ":", "." )  )
    except:
      try:
        self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                           self.decoder_instance.decoder_class_name_key_added] = \
                                           "{{\"last cleared\":\"{}\"}}".\
                                             format( self.data_list[3].strip().replace( ":", "." ) )
      except:
        pass
    return()
"""
CLASS: EgressIngressCoSQueues
DESCRIPTION: This class is a primary controlling class for 
             EGRESS, Ingress and CoS queues statistcial data collection
INPUT:
OUTPUT:
"""
class EgressIngressCoSQueues:
  "Egress, Ingress, CoS Queues"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
    self.que_count = 0
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.que_being_processed = " ".join( data.lower().split( ":" )[0].split() )
    self.que_count = int( data.split( "," )[1].split()[0] )
    for self.data in self.dataFD:
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.data )
      self.class_to_execute = "".join( self.data.split( ":" )[0].title().split() )
      self.decoder_instance.decoder_class_name_key_added = "{}".format( self.que_being_processed )
      if not self.class_to_execute in "QueueCounters" and \
         not self.class_to_execute in "QueueNumbers" or \
         self.class_to_execute == "":
        break
      try:
        CallClass(self).call_class(module_name = "DecodeDataProcessor",
                                   class_name = self.class_to_execute, method_name = "execute",
                                   dictionary = self.dictionary, data = self.data, descriptor = self.dataFD)
      except Exception as error:
        self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
        self.dictionary['loggerwidget'].emit(self.message)
        raise Exception( error )
    self.decoder_instance.current_index = self.decoder_instance.previous_index
    self.dataFD.seek( self.decoder_instance.current_index )
    return()
"""
CLASS: Policer
DESCRIPTION:
INPUT:
OUTPUT:
"""
class Policer:
  "Policer"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
    self.previous_length = self.parent.previous_length
    self.current_length = self.parent.line_length
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.block_location = BlockLocation( self )
    self.block_location.set_block_indentation( self.dataFD )
    self.data_previous = " ".join( data.split() ).replace( " :", ":" )
    """
    Set the file pointer back so the Policer line is extracted
    Extracted tag Policer data then call the DecoderProcessor class 
    """
    self.dataFD.seek( self.decoder_instance.previous_index )
    self.decoder_instance.decoder_class_name_key_added = self.name.lower()
    for self.data in self.dataFD:
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.data )
      self.leading_space_count = len( self.data ) - len( self.data.lstrip() )
      if self.leading_space_count <= self.block_location.get_block_indentation() and \
        " ".join( self.data.split() ).replace( " :", ":" ) != self.data_previous:
        break
      self.data = self.data.lstrip()
      try:
        self.line_index, self.decoder_instance = CallClass(self).call_class(module_name = os.path.basename(__file__).split('.py')[0],
                                                                            class_name = 'DecoderProcessor', method_name = "execute",
                                                                            dictionary = self.dictionary, data = self.data,
                                                                            descriptor = self.dataFD)
        break
      except Exception as error:
        break
    return()
"""
CLASS: DecoderProcessorWrapper
DESCRIPTION: Preprocessing to set up for calling the DecoderPRocessor class
INPUT:
OUTPUT:
"""
class DecoderProcessorWrapper:
  "Decoder Processor Wrapper"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.block_location = BlockLocation( self )
    self.block_location.set_block_indentation( self.dataFD )
    self.data_previous = " ".join( data.split() ).replace( " :", ":" )
    """
    Reset the file pointer, loop must start at first line
    """
    self.decoder_instance.current_index = self.decoder_instance.previous_index
    self.dataFD.seek( self.decoder_instance.current_index )
    for self.data in self.dataFD:
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.data )
      self.leading_space_count = len( self.data ) - len( self.data.lstrip() )
      if self.leading_space_count <= self.block_location.get_block_indentation() and \
        " ".join( self.data.split() ).replace( " :", ":" ) != self.data_previous:
        break
      self.data = " ".join( data.split() ).replace( " :", ":" )
      try:
        CallClass(self).call_class(module_name = os.path.basename(__file__).split('.py')[0],
                                   class_name = 'DecoderProcessor', method_name = "execute",
                                   dictionary = self.dictionary, data = self.data, descriptor = self.dataFD)
      except Exception as error:
        self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
        self.dictionary['loggerwidget'].emit(self.message)
        raise Exception( error )
    self.decoder_instance.current_index = self.decoder_instance.previous_index
    self.dataFD.seek( self.decoder_instance.current_index )
    return()
"""
CLASS: VCIWrapper
DESCRIPTION:
INPUT:
OUTPUT:
"""
class VCIWrapper:
  "VCI Wrapper"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.data = data
    self.block_location = BlockLocation( self )
    self.block_location.set_block_indentation( self.dataFD )
    self.vci_data = "\"vci\":\"{}\",".format( self.data.split()[1] )
    for self.data in self.dataFD:
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.data )
      self.leading_space_count = len( self.data ) - len( self.data.lstrip() )
      if self.leading_space_count <= self.block_location.get_block_indentation():
        break
      self.data = self.data.lstrip()
      if self.data.startswith( "VPI/VCI Swapping:" ):
        self.vci_data += "\"vpi/vci swapping\":\"{}\",".\
          format( self.data.split( "VPI/VCI Swapping:" )[1][:-1].lstrip() )
      elif self.data.startswith( "Flags:" ):
        self.vci_data += "\"flags\":\"{}\",".\
          format( self.data.split( "Flags:" )[1][:-1].lstrip() )
      elif self.data.startswith( "Total down time:" ):
        self.vci_data += "\"total down time\":\"{}\",".\
          format( self.data.split( "Total down time:" )[1].split( "," )[0].lstrip() )
        self.vci_data += "\"last down\":\"{}\",".\
          format( self.data.split( "Last down:" )[1][:-1].lstrip() )
      elif self.data.startswith( "ATM per-VC transmit statistics:" ):
        for self.data in self.dataFD:
          self.decoder_instance.previous_index = self.decoder_instance.current_index
          self.decoder_instance.current_index += len( self.data )
          self.data = self.data.lstrip()
          if self.data.startswith( "Traffic statistics:" ):
            self.decoder_instance.current_index = self.decoder_instance.previous_index
            self.dataFD.seek( self.decoder_instance.previous_index )
            break
          if self.data.startswith( "Tail queue packet drops:" ):
            self.vci_data += "\"ATM per-VC transmit drops\":\"{}\",".\
                          format( self.data.split( "Tail queue packet drops:" )[1][:-1].lstrip() )
      elif self.data.startswith( "Traffic statistics:" ):
        for self.data in self.dataFD:
          self.decoder_instance.previous_index = self.decoder_instance.current_index
          self.decoder_instance.current_index += len( self.data )
          self.data = " ".join( self.data.split() ).replace( " :", ":" )
          if self.data.startswith( "Input bytes:" ):
            self.vci_data += "\"traffic input bytes\":\"{}\",".\
              format( self.data.split( "Input bytes:" )[1].lstrip().replace( "\n", "" ) )
          elif self.data.startswith( "Output bytes:" ):
            self.vci_data += "\"traffic output bytes\":\"{}\",".\
              format( self.data.split( "Output bytes:" )[1].lstrip().replace( "\n", "" ) )
          elif self.data.startswith( "Input packets:" ):
            self.vci_data += "\"traffic input packets\":\"{}\",".\
              format( self.data.split( "Input packets:" )[1].lstrip().replace( "\n", "" ) )
          elif self.data.startswith( "Output packets:" ):
            self.vci_data += "\"traffic output packets\":\"{}\",".\
              format( self.data.split( "Output packets:" )[1].lstrip().replace( "\n", "" ) )
          else:
            self.decoder_instance.current_index = self.decoder_instance.previous_index
            self.dataFD.seek( self.decoder_instance.previous_index )
            break
      elif self.data.startswith( "OAM F5 cell statistics:" ):
        for self.data in self.dataFD:
          self.decoder_instance.previous_index = self.decoder_instance.current_index
          self.decoder_instance.current_index += len( self.data )
          self.data = " ".join( self.data.split() ).replace( " :", ":" )
          if self.data.startswith( "Total received:" ):
            self.vci_data += "\"oam f5 cell total received\":\"{}\",".\
              format( self.data.split( "Total received:" )[1].split( "," )[0].lstrip() )
            self.vci_data += "\"oam f5 cell total sent\":\"{}\",".\
              format( self.data.split( "Total sent:" )[1].lstrip() )
          elif self.data.startswith( "Loopback received:" ):
            self.vci_data += "\"oam f5 cell loopback received\":\"{}\",".\
              format( self.data.split( "Loopback received:" )[1].split( "," )[0].lstrip() )
            self.vci_data += "\"oam f5 cell loopback sent\":\"{}\",".\
              format( self.data.split( "Loopback sent:" )[1].lstrip() )
          elif self.data.startswith( "RDI received:" ):
            self.vci_data += "\"oam f5 cell rdi received\":\"{}\",".\
              format( self.data.split( "RDI received:" )[1].split( "," )[0].lstrip() )
            self.vci_data += "\"oam f5 cell rdi sent\":\"{}\",".\
              format( self.data.split( "RDI sent:" )[1].lstrip() )
          elif self.data.startswith( "AIS received:" ):
            self.vci_data += "\"oam f5 cell ais received\":\"{}\",".\
              format( self.data.split( "AIS received:" )[1].split( "," )[0].lstrip() )
            self.vci_data += "\"oam f5 cell ais sent\":\"{}\",".\
              format( self.data.split( "AIS sent:" )[1].lstrip() )
          elif self.data.startswith( "Last received:" ):
            self.vci_data += "\"oam f5 cell last received\":\"{}\",".\
              format( self.data.split( "Last received:" )[1].split( "," )[0].lstrip() )
            self.vci_data += "\"oam f5 cell last sent\":\"{}\",".\
              format( self.data.split( "Last sent:" )[1].lstrip() )
          else:
            break
    self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                       self.decoder_instance.decoder_class_name_key_added] = \
                                       "{{{}}}".format( self.vci_data[:-1] )
    self.decoder_instance.current_index = self.decoder_instance.previous_index
    self.dataFD.seek( self.decoder_instance.current_index )
    return()
"""
CLASS: CEInfo
DESCRIPTION:
INPUT:
OUTPUT:
"""
class CEInfo:
  "CE Info"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.data = data
    self.data_list = self.data.split()
    self.unique_id = 0
    self.ce_data = ""
    self.protocol_field = False
    for self.data in self.dataFD:
      self.data_previous = self.data
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.data )
      self.data_list = " ".join( self.data.split( ":" ) ).split()
      self.data = " ".join( self.data_list )
      if self.data.startswith( "CE Tx" ):
        try:
          self.ce_data += "\"ce tx packets\":\"{}\",".format( self.data_list[2].lstrip() )
          self.ce_data += "\"ce tx bytes\":\"{}\",".format( self.data_list[3].lstrip() )
        except:
          pass
      elif self.data.startswith( "CE Rx" ):
        try:
          self.ce_data += "\"ce rx packets\":\"{}\",".format( self.data_list[2].lstrip() )
          self.ce_data += "\"ce rx bytes\":\"{}\",".format( self.data_list[3].lstrip() )
        except:
          pass
      elif self.data.startswith( "CE Rx Forwarded" ):
        try:
          self.ce_data += "\"ce rx forwarded packets\":\"{}\",".format( self.data_list[3].lstrip() )
          self.ce_data += "\"ce rx forwarded bytes\":\"{}\",".format( self.data_list[4].lstrip() )
        except:
          pass
      elif self.data.startswith( "CE Strayed" ):
        try:
          self.ce_data += "\"ce strayed packets\":\"{}\",".format( self.data_list[2].lstrip() )
          self.ce_data += "\"ce strayed bytes\":\"{}\",".format( self.data_list[3].lstrip() )
        except:
          pass
      elif self.data.startswith( "CE Lost" ):
        try:
          self.ce_data += "\"ce lost packets\":\"{}\",".format( self.data_list[2].lstrip() )
          self.ce_data += "\"ce lost bytes\":\"{}\",".format( self.data_list[3].lstrip() )
        except:
          pass
      elif self.data.startswith( "CE Malformed" ):
        try:
          self.ce_data += "\"ce malformed packets\":\"{}\",".format( self.data_list[2].lstrip() )
          self.ce_data += "\"ce malformed bytes\":\"{}\",".format( self.data_list[3].lstrip() )
        except:
          pass
      elif self.data.startswith( "CE Misinserted" ):
        try:
          self.ce_data += "\"ce misinserted packets\":\"{}\",".format( self.data_list[2].lstrip() )
          self.ce_data += "\"ce misinserted bytes\":\"{}\",".format( self.data_list[3].lstrip() )
        except:
          pass
      elif self.data.startswith( "CE AIS dropped" ):
        try:
          self.ce_data += "\"ce ais dropped packets\":\"{}\",".format( self.data_list[3].lstrip() )
          self.ce_data += "\"ce ais dropped bytes\":\"{}\",".format( self.data_list[4].lstrip() )
        except:
          pass
      elif self.data.startswith( "CE Dropped" ):
        try:
          self.ce_data += "\"ce dropped packets\":\"{}\",".format( self.data_list[2].lstrip() )
          self.ce_data += "\"ce dropped bytes\":\"{}\",".format( self.data_list[3].lstrip())
        except:
          pass
      elif self.data.startswith( "CE Overrun Events" ):
        try:
          self.ce_data += "\"ce overrun events packets\":\"{}\",".format( self.data_list[3].lstrip() )
          self.ce_data += "\"ce overrun events bytes\":\"{}\",".format( self.data_list[4].lstrip() )
        except:
          pass
      elif self.data.startswith( "CE Underrun Events" ):
        try:
          self.ce_data += "\"ce underrun events packets\":\"{}\",".format( self.data_list[3].lstrip() )
          self.ce_data += "\"ce underrun events bytes\":\"{}\",".format( self.data_list[4].lstrip() )
        except:
          pass
      elif self.data.startswith( "Protocol" ):
        self.protocol_field = True
        self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                           self.decoder_instance.decoder_class_name_key_added] = \
                                           "{{{}}}".format( self.ce_data[:-1] )
        try:
          """
          Decode the first line then any associated blocks.
          """
          self.decoder_instance.decoder_class_name_key_added += \
               " {}".format( " ".join( self.data_previous.split( ":", 1 )[0].lower().split() ) )
          DecoderProcessor(self).execute(dictionary = self.dictionary, descriptor = self.dataFD, data = self.data)
          self.dataFD.seek( self.decoder_instance.previous_index )
          self.data_previous = " ".join( data.split() ).replace( " :", ":" )
          self.block_location = BlockLocation( self )
          self.block_location.set_block_indentation( self.dataFD )
          for self.data in self.dataFD:
            self.decoder_instance.previous_index = self.decoder_instance.current_index
            self.decoder_instance.current_index += len( self.data )
            self.data_list = " ".join( self.data.split( ":" ) ).split()
            self.data = " ".join( self.data_list )
            self.leading_space_count = len( self.data ) - len( self.data.lstrip() )
            if self.leading_space_count <= self.block_location.get_block_indentation() and \
                    " ".join( self.data.split() ).replace( " :", ":" ) != self.data_previous:
              self.dataFD.seek( self.decoder_instance.previous_index )
              break
            """
            String leading/trailing spaces and any before a colon so
            using the converting structure is clean
            """
            self.data_string_to_convert_to_class = " ".join( self.data.split() ).replace( " :", ":" )
            """
            Extract the Decoder class that will process this line of data.
            Execute to the class
            """
            self.decoder_list = self.decoder_instance.decoder_utility. \
              find_decoder( self.data_string_to_convert_to_class,
                            self.decoder_instance.decoder_utility.decoder_automaton )
            self.decoder_instance.decoder_class = self.decoder_list[0][1]
            self.decoder_instance.decoder_class_name_key_added += \
                " {} {}".format( " ".join( self.decoder_list[0][0].lower().split() )[:-1], str( self.unique_id ) )
            CallClass(self).call_class(module_name = os.path.basename(__file__).split('.py')[0], class_name = self.decoder_instance.decoder_class,
                                       dictionary = self.dictionary, descriptor = self.dataFD, data = self.data, decode = None)
        except Exception as error:
          pass
      else:
        break
    if not self.protocol_field:
      self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                         self.decoder_instance.decoder_class_name_key_added] = \
                                         "{{{}}}".format( self.ce_data[:-1] )
    self.dataFD.seek( self.decoder_instance.previous_index )
    self.decoder_instance.current_index = self.decoder_instance.previous_index
    return()
"""
CLASS: KeepaliveStatistics
DESCRIPTION:
INPUT:
OUTPUT:
"""
class KeepaliveStatistics:
  "Keepalive Statistics"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.data = data
    self.keepalive_data = ""
    for self.data in self.dataFD:
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.data )
      self.data = self.data.lstrip().replace( " :", ":" )
      if self.data.startswith( "Input:" ):
        try:
          self.keepalive_data += \
            "\"input\":\"{}\",".format( self.data.split( "Input:" )[1].split()[0] )
          self.keepalive_data += \
            "\"last received\":\"{}\",".format( self.data.split( "Input:" )[1].lstrip().split( " ", 1 )[1][:-1] )
        except:
          pass
      elif self.data.startswith( "Output:" ):
        self.keepalive_data += \
          "\"output\":\"{}\",".format( self.data.split( "Output:" )[1].split()[0] )
        self.keepalive_data += \
          "\"last sent\":\"{}\",".format( self.data.split( "Output:" )[1].lstrip().split( " ", 1 )[1][:-1] )
      else:
        break   # all done
    self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                       self.decoder_instance.decoder_class_name_key_added] = \
                                       "{{{}}}".format( self.keepalive_data[:-1] )
    self.dataFD.seek( self.decoder_instance.previous_index )
    self.decoder_instance.current_index = self.decoder_instance.previous_index
    return()
"""
CLASS: PCSStatistics
DESCRIPTION:
INPUT:
OUTPUT:
"""
class PCSStatistics:
  "PCS Statistics"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.data = data
    self.pcs_data = ""
    for self.data in self.dataFD:
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.data )
      self.data = self.data.lstrip()
      if self.data.startswith( "Bit errors" ):
        self.pcs_data += \
          "\"bit errors\":\"{}\",".format( self.data.split( "Bit errors" )[1].lstrip()[:-1] )
      elif self.data.startswith( "Errored blocks" ):
        self.pcs_data += \
          "\"errored blocks\":\"{}\",".format( self.data.split( "Errored blocks" )[1].lstrip()[:-1] )
      else:
        break   # all done
    self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                       self.decoder_instance.decoder_class_name_key_added] = \
                                       "{{{}}}".format( self.pcs_data[:-1] )
    self.dataFD.seek( self.decoder_instance.previous_index )
    self.decoder_instance.current_index = self.decoder_instance.previous_index
    return()
"""
CLASS: PreclassifierStatistics
DESCRIPTION:
INPUT:
OUTPUT:
"""
class PreclassifierStatistics:
  "Preclassifier statistics"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.data = data
    self.data_list = self.data.split()
    self.preclass_counters = ""
    self.best_effort_counter = 0
    for self.data in self.dataFD:
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.data )
      if self.data.lstrip().startswith( "Traffic Class" ):
        continue
      self.data_list = self.data.split()
      if not self.data_list[0].startswith( "best-effort" ):
        break
      try:
        self.preclass_counters += "\"best-effort {}\":{{\"received packets\":\"{}\",".\
                                    format( self.best_effort_counter, self.data_list[1].lstrip() ) + \
                                  "\"transmitted packets\":\"{}\",".format( self.data_list[2].lstrip() ) + \
                                  "\"dropped packets\":\"{}\"}},".format( self.data_list[3].lstrip() )
        self.best_effort_counter += 1
      except Exception as error:
        self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
        self.dictionary['loggerwidget'].emit(self.message)
        raise Exception( error )
    self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                       self.decoder_instance.decoder_class_name_key_added] = \
                                       "{{{}}}".format( self.preclass_counters[:-1] )
    self.dataFD.seek( self.decoder_instance.previous_index )
    self.decoder_instance.current_index = self.decoder_instance.previous_index
    return()
"""
CLASS: ProtocolVplsMtu
DESCRIPTION:  
INPUT: 
OUTPUT: decoded[] element
"""
class ProtocolVplsMtu:
  "Protocol Vpls Mtu"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.data = data
    self.block_location = BlockLocation( self )
    self.block_location.set_block_indentation( self.dataFD )
    self.data_previous = " ".join( data.split() ).replace( " :", ":" )
    self.unique_id = 0
    self.original_tag = self.decoder_instance.decoder_class_name_key_added
    DecoderProcessor(self).execute(dictionary = self.dictionary, descriptor = self.dataFD, data = self.data)
    for self.data in self.dataFD:
      self.unique_id += 1
      self.decoder_instance.decoder_class_name_key_added = self.original_tag
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.data )
      self.leading_space_count = len( self.data ) - len( self.data.lstrip() )
      if self.leading_space_count <= self.block_location.get_block_indentation() and \
              " ".join( self.data.split() ).replace( " :", ":" ) != self.data_previous:
        break
      """
      Process blocks associated with the VPLS Protocol
      """
      try:
        """
        String leading/trailing spaces and any before a colon so
        using the converting structure is clean
        """
        self.data_string_to_convert_to_class = " ".join( self.data.split() ).replace( " :", ":" )
        """
        Extract the Decoder class that will process this line of data.
        Execute to the class
        """
        self.decoder_list = self.decoder_instance.decoder_utility. \
          find_decoder( self.data_string_to_convert_to_class,
                        self.decoder_instance.decoder_utility.decoder_automaton )
        self.decoder_instance.decoder_class = self.decoder_list[0][1]
        self.decoder_instance.decoder_class_name_key_added += \
          " {} {}".format( " ".join( self.decoder_list[0][0].lower().split() )[:-1], str( self.unique_id ) )
        CallClass(self).call_class(module_name = os.path.basename(__file__).split('.py')[0], class_name = self.decoder_instance.decoder_class,
                                   dictionary = self.dictionary, descriptor = self.dataFD, data = self.data, decode = None)
      except Exception as error:
        pass
    self.dataFD.seek( self.decoder_instance.previous_index )
    self.decoder_instance.current_index = self.decoder_instance.previous_index
    return()
"""
CLASS: ProtocolInetMtu
DESCRIPTION:  
INPUT: 
OUTPUT: decoded[] element
"""
class ProtocolInetMtu:
  "Protocol Inet Mtu"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.data = data
    self.block_location = BlockLocation( self )
    self.block_location.set_block_indentation( self.dataFD )
    self.data_previous = " ".join( data.split() ).replace( " :", ":" )
    self.unique_id = 0
    self.original_tag = self.decoder_instance.decoder_class_name_key_added
    DecoderProcessor(self).execute(dictionary = self.dictionary, descriptor = self.dataFD, data = self.data)
    for self.data in self.dataFD:
      self.unique_id += 1
      self.decoder_instance.decoder_class_name_key_added = self.original_tag
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.data )
      self.leading_space_count = len( self.data ) - len( self.data.lstrip() )
      if self.leading_space_count <= self.block_location.get_block_indentation() and \
              " ".join( self.data.split() ).replace( " :", ":" ) != self.data_previous:
        break
      """
      Process blocks associated with the Inet Protocol
      """
      try:
        """
        String leading/trailing spaces and any before a colon so
        using the converting structure is clean
        """
        self.data_string_to_convert_to_class = " ".join( self.data.split() ).replace( " :", ":" )
        """
        Extract the Decoder class that will process this line of data.
        Execute to the class
        """
        self.decoder_list = self.decoder_instance.decoder_utility. \
          find_decoder( self.data_string_to_convert_to_class,
                        self.decoder_instance.decoder_utility.decoder_automaton )
        self.decoder_instance.decoder_class = self.decoder_list[0][1]
        self.decoder_instance.decoder_class_name_key_added += \
          " {} {}".format( " ".join( self.decoder_list[0][0].lower().split() )[:-1], str( self.unique_id ) )
        CallClass(self).call_class(module_name = os.path.basename(__file__).split('.py')[0], class_name = self.decoder_instance.decoder_class,
                                   dictionary = self.dictionary, descriptor = self.dataFD, data = self.data, decode = None)
      except Exception as error:
        pass
    self.dataFD.seek( self.decoder_instance.previous_index )
    self.decoder_instance.current_index = self.decoder_instance.previous_index
    return()
"""
CLASS: ProtocolInet6Mtu
DESCRIPTION:  
INPUT: 
OUTPUT: decoded[] element
"""
class ProtocolInet6Mtu:
  "Protocol Inet6 Mtu"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.data = data
    self.block_location = BlockLocation( self )
    self.block_location.set_block_indentation( self.dataFD )
    self.data_previous = " ".join( data.split() ).replace( " :", ":" )
    self.unique_id = 0
    self.original_tag = self.decoder_instance.decoder_class_name_key_added
    DecoderProcessor(self).execute(dictionary = self.dictionary, descriptor = self.dataFD, data = self.data)
    for self.data in self.dataFD:
      self.unique_id += 1
      self.decoder_instance.decoder_class_name_key_added = self.original_tag
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.data )
      self.leading_space_count = len( self.data ) - len( self.data.lstrip() )
      if self.leading_space_count <= self.block_location.get_block_indentation() and \
              " ".join( self.data.split() ).replace( " :", ":" ) != self.data_previous:
        break
      """
      Process blocks associated with the Inet6 Protocol
      """
      try:
        """
        String leading/trailing spaces and any before a colon so
        using the converting structure is clean
        """
        self.data_string_to_convert_to_class = " ".join( self.data.split() ).replace( " :", ":" )
        """
        Extract the Decoder class that will process this line of data.
        Execute to the class
        """
        self.decoder_list = self.decoder_instance.decoder_utility. \
          find_decoder( self.data_string_to_convert_to_class,
                        self.decoder_instance.decoder_utility.decoder_automaton )
        self.decoder_instance.decoder_class = self.decoder_list[0][1]
        self.decoder_instance.decoder_class_name_key_added += \
          " {} {}".format( " ".join( self.decoder_list[0][0].lower().split() )[:-1], str( self.unique_id ) )
        CallClass(self).call_class(module_name = os.path.basename(__file__).split('.py')[0], class_name = self.decoder_instance.decoder_class,
                                   dictionary = self.dictionary, descriptor = self.dataFD, data = self.data, decode = None)
      except Exception as error:
        pass
    self.dataFD.seek( self.decoder_instance.previous_index )
    self.decoder_instance.current_index = self.decoder_instance.previous_index
    return()
"""
CLASS: ProtocolMplsMtu
DESCRIPTION:  
INPUT: 
OUTPUT: decoded[] element
"""
class ProtocolMplsMtu:
  "Protocol Mpls Mtu"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.data = data
    self.block_location = BlockLocation( self )
    self.block_location.set_block_indentation( self.dataFD )
    self.data_previous = " ".join( data.split() ).replace( " :", ":" )
    self.unique_id = 0
    self.original_tag = self.decoder_instance.decoder_class_name_key_added
    DecoderProcessor(self).execute(dictionary = self.dictionary, descriptor = self.dataFD, data = self.data)
    for self.data in self.dataFD:
      self.unique_id += 1
      self.decoder_instance.decoder_class_name_key_added = self.original_tag
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.data )
      self.leading_space_count = len( self.data ) - len( self.data.lstrip() )
      if self.leading_space_count <= self.block_location.get_block_indentation() and \
              " ".join( self.data.split() ).replace( " :", ":" ) != self.data_previous:
        break
      """
      Process blocks associated with the Mpls Protocol
      """
      try:
        """
        String leading/trailing spaces and any before a colon so
        using the converting structure is clean
        """
        self.data_string_to_convert_to_class = " ".join( self.data.split() ).replace( " :", ":" )
        """
        Extract the Decoder class that will process this line of data.
        Execute to the class
        """
        self.decoder_list = self.decoder_instance.decoder_utility. \
          find_decoder( self.data_string_to_convert_to_class,
                        self.decoder_instance.decoder_utility.decoder_automaton )
        self.decoder_instance.decoder_class = self.decoder_list[0][1]
        self.decoder_instance.decoder_class_name_key_added += \
          " {} {}".format( " ".join( self.decoder_list[0][0].lower().split() )[:-1], str( self.unique_id ) )
        CallClass(self).call_class(module_name = os.path.basename(__file__).split('.py')[0], class_name = self.decoder_instance.decoder_class,
                                   dictionary = self.dictionary, descriptor = self.dataFD, data = self.data, decode = None)
      except Exception as error:
        pass
    self.dataFD.seek( self.decoder_instance.previous_index )
    self.decoder_instance.current_index = self.decoder_instance.previous_index
    return()
"""
CLASS: ProtocolMultiserverMtu
DESCRIPTION:  
INPUT: 
OUTPUT: decoded[] element
"""
class ProtocolMultiserverMtu:
  "Protocol Multiserver Mtu"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.data = data
    self.block_location = BlockLocation( self )
    self.block_location.set_block_indentation( self.dataFD )
    self.data_previous = " ".join( data.split() ).replace( " :", ":" )
    self.unique_id = 0
    self.original_tag = self.decoder_instance.decoder_class_name_key_added
    DecoderProcessor(self).execute(dictionary = self.dictionary, descriptor = self.dataFD, data = self.data)
    for self.data in self.dataFD:
      self.unique_id += 1
      self.decoder_instance.decoder_class_name_key_added = self.original_tag
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.data )
      self.leading_space_count = len( self.data ) - len( self.data.lstrip() )
      if self.leading_space_count <= self.block_location.get_block_indentation() and \
              " ".join( self.data.split() ).replace( " :", ":" ) != self.data_previous:
        break
      """
      Process blocks associated with the Multiserver Protocol
      """
      try:
        """
        String leading/trailing spaces and any before a colon so
        using the converting structure is clean
        """
        self.data_string_to_convert_to_class = " ".join( self.data.split() ).replace( " :", ":" )
        """
        Extract the Decoder class that will process this line of data.
        Execute to the class
        """
        self.decoder_list = self.decoder_instance.decoder_utility. \
          find_decoder( self.data_string_to_convert_to_class,
                        self.decoder_instance.decoder_utility.decoder_automaton )
        self.decoder_instance.decoder_class = self.decoder_list[0][1]
        self.decoder_instance.decoder_class_name_key_added += \
          " {} {}".format( " ".join( self.decoder_list[0][0].lower().split() )[:-1], str( self.unique_id ) )
        CallClass(self).call_class(module_name = os.path.basename(__file__).split('.py')[0], class_name = self.decoder_instance.decoder_class,
                                   dictionary = self.dictionary, descriptor = self.dataFD, data = self.data, decode = None)
      except Exception as error:
        pass
    self.dataFD.seek( self.decoder_instance.previous_index )
    self.decoder_instance.current_index = self.decoder_instance.previous_index
    return()
"""
CLASS: ProtocolIsoMtu
DESCRIPTION:  
INPUT: 
OUTPUT: decoded[] element
"""
class ProtocolIsoMtu:
  "Protocol Iso Mtu"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.data = data
    self.block_location = BlockLocation( self )
    self.block_location.set_block_indentation( self.dataFD )
    self.data_previous = " ".join( data.split() ).replace( " :", ":" )
    self.unique_id = 0
    self.original_tag = self.decoder_instance.decoder_class_name_key_added
    DecoderProcessor(self).execute(dictionary = self.dictionary, descriptor = self.dataFD, data = self.data)
    for self.data in self.dataFD:
      self.unique_id += 1
      self.decoder_instance.decoder_class_name_key_added = self.original_tag
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.data )
      self.leading_space_count = len( self.data ) - len( self.data.lstrip() )
      if self.leading_space_count <= self.block_location.get_block_indentation() and \
              " ".join( self.data.split() ).replace( " :", ":" ) != self.data_previous:
        break
      """
      Process blocks associated with the Iso Protocol
      """
      try:
        """
        String leading/trailing spaces and any before a colon so
        using the converting structure is clean
        """
        self.data_string_to_convert_to_class = " ".join( self.data.split() ).replace( " :", ":" )
        """
        Extract the Decoder class that will process this line of data.
        Execute to the class
        """
        self.decoder_list = self.decoder_instance.decoder_utility. \
          find_decoder( self.data_string_to_convert_to_class,
                        self.decoder_instance.decoder_utility.decoder_automaton )
        self.decoder_instance.decoder_class = self.decoder_list[0][1]
        self.decoder_instance.decoder_class_name_key_added += \
          " {} {}".format( " ".join( self.decoder_list[0][0].lower().split() )[:-1], str( self.unique_id ) )
        CallClass(self).call_class(module_name = os.path.basename(__file__).split('.py')[0], class_name = self.decoder_instance.decoder_class,
                                   dictionary = self.dictionary, descriptor = self.dataFD, data = self.data, decode = None)
      except Exception as error:
        pass
    self.dataFD.seek( self.decoder_instance.previous_index )
    self.decoder_instance.current_index = self.decoder_instance.previous_index
    return()
"""
CLASS: ProtocolCccMtu
DESCRIPTION:  
INPUT: 
OUTPUT: decoded[] element
"""
class ProtocolCccMtu:
  "Protocol Ccc Mtu"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.data = data
    self.block_location = BlockLocation( self )
    self.block_location.set_block_indentation( self.dataFD )
    self.data_previous = " ".join( data.split() ).replace( " :", ":" )
    self.unique_id = 0
    self.original_tag = self.decoder_instance.decoder_class_name_key_added
    DecoderProcessor(self).execute(dictionary = self.dictionary, descriptor = self.dataFD, data = self.data)
    for self.data in self.dataFD:
      self.decoder_instance.decoder_class_name_key_added = self.original_tag
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.data )
      self.leading_space_count = len( self.data ) - len( self.data.lstrip() )
      if self.leading_space_count <= self.block_location.get_block_indentation() and \
              " ".join( self.data.split() ).replace( " :", ":" ) != self.data_previous:
        break
      """
      Process blocks associated with the CCC Protocol
      """
      self.unique_id += 1
      try:
        """
        String leading/trailing spaces and any before a colon so
        using the converting structure is clean
        """
        self.data_string_to_convert_to_class = " ".join( self.data.split() ).replace( " :", ":" )
        """
        Extract the Decoder class that will process this line of data.
        Execute to the class
        """
        self.decoder_list = self.decoder_instance.decoder_utility. \
          find_decoder( self.data_string_to_convert_to_class,
                        self.decoder_instance.decoder_utility.decoder_automaton )
        self.decoder_instance.decoder_class = self.decoder_list[0][1]
        self.decoder_instance.decoder_class_name_key_added += \
          " {} {}".format( " ".join( self.decoder_list[0][0].lower().split() )[:-1], str( self.unique_id ) )
        CallClass(self).call_class(module_name = os.path.basename(__file__).split('.py')[0], class_name = self.decoder_instance.decoder_class,
                                   dictionary = self.dictionary, descriptor = self.dataFD, data = self.data, decode = None)
      except Exception as error:
        pass
    self.dataFD.seek( self.decoder_instance.previous_index )
    self.decoder_instance.current_index = self.decoder_instance.previous_index
    return()
"""
CLASS: Protocol61Mtu
DESCRIPTION:  
INPUT: 
OUTPUT: decoded[] element
"""
class Protocol61Mtu:
  "Protocol 61 Mtu"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.data = data
    self.block_location = BlockLocation( self )
    self.block_location.set_block_indentation( self.dataFD )
    self.data_previous = " ".join( data.split() ).replace( " :", ":" )
    self.unique_id = 0
    self.original_tag = self.decoder_instance.decoder_class_name_key_added
    DecoderProcessor(self).execute(dictionary = self.dictionary, descriptor = self.dataFD, data = self.data)
    for self.data in self.dataFD:
      self.unique_id += 1
      self.decoder_instance.decoder_class_name_key_added = self.original_tag
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.data )
      self.leading_space_count = len( self.data ) - len( self.data.lstrip() )
      if self.leading_space_count <= self.block_location.get_block_indentation() and \
              " ".join( self.data.split() ).replace( " :", ":" ) != self.data_previous:
        break
      """
      Process blocks associated with the 61 Protocol
      """
      try:
        """
        String leading/trailing spaces and any before a colon so
        using the converting structure is clean
        """
        self.data_string_to_convert_to_class = " ".join( self.data.split() ).replace( " :", ":" )
        """
        Extract the Decoder class that will process this line of data.
        Execute to the class
        """
        self.decoder_list = self.decoder_instance.decoder_utility. \
          find_decoder( self.data_string_to_convert_to_class,
                        self.decoder_instance.decoder_utility.decoder_automaton )
        self.decoder_instance.decoder_class = self.decoder_list[0][1]
        self.decoder_instance.decoder_class_name_key_added += \
          " {} {}".format( " ".join( self.decoder_list[0][0].lower().split() )[:-1], str( self.unique_id ) )
        CallClass(self).call_class(module_name = os.path.basename(__file__).split('.py')[0], class_name = self.decoder_instance.decoder_class,
                                   dictionary = self.dictionary, descriptor = self.dataFD, data = self.data, decode = None)
      except Exception as error:
        pass
    self.dataFD.seek( self.decoder_instance.previous_index )
    self.decoder_instance.current_index = self.decoder_instance.previous_index
    return()
"""
CLASS: Protocol85Mtu
DESCRIPTION:  
INPUT: 
OUTPUT: decoded[] element
"""
class Protocol85Mtu:
  "Protocol 85 Mtu"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.data = data
    self.block_location = BlockLocation( self )
    self.block_location.set_block_indentation( self.dataFD )
    self.data_previous = " ".join( data.split() ).replace( " :", ":" )
    self.unique_id = 0
    self.original_tag = self.decoder_instance.decoder_class_name_key_added
    DecoderProcessor(self).execute(dictionary = self.dictionary, descriptor = self.dataFD, data = self.data)
    for self.data in self.dataFD:
      self.unique_id += 1
      self.decoder_instance.decoder_class_name_key_added = self.original_tag
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.data )
      self.leading_space_count = len( self.data ) - len( self.data.lstrip() )
      if self.leading_space_count <= self.block_location.get_block_indentation() and \
              " ".join( self.data.split() ).replace( " :", ":" ) != self.data_previous:
        break
      """
      Process blocks associated with the 85 Protocol
      """
      try:
        """
        String leading/trailing spaces and any before a colon so
        using the converting structure is clean
        """
        self.data_string_to_convert_to_class = " ".join( self.data.split() ).replace( " :", ":" )
        """
        Extract the Decoder class that will process this line of data.
        Execute to the class
        """
        self.decoder_list = self.decoder_instance.decoder_utility. \
          find_decoder( self.data_string_to_convert_to_class,
                        self.decoder_instance.decoder_utility.decoder_automaton )
        self.decoder_instance.decoder_class = self.decoder_list[0][1]
        self.decoder_instance.decoder_class_name_key_added += \
          " {} {}".format( " ".join( self.decoder_list[0][0].lower().split() )[:-1], str( self.unique_id ) )
        CallClass(self).call_class(module_name = os.path.basename(__file__).split('.py')[0], class_name = self.decoder_instance.decoder_class,
                                   dictionary = self.dictionary, descriptor = self.dataFD, data = self.data, decode = None)
      except Exception as error:
        pass
    self.dataFD.seek( self.decoder_instance.previous_index )
    self.decoder_instance.current_index = self.decoder_instance.previous_index
    return()
"""
CLASS: ProtocolTnpMtu
DESCRIPTION:  
INPUT: 
OUTPUT: decoded[] element
"""
class ProtocolTnpMtu:
  "Protocol Tnp Mtu"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.data = data
    self.block_location = BlockLocation( self )
    self.block_location.set_block_indentation( self.dataFD )
    self.data_previous = " ".join( data.split() ).replace( " :", ":" )
    self.unique_id = 0
    self.original_tag = self.decoder_instance.decoder_class_name_key_added
    DecoderProcessor(self).execute(dictionary = self.dictionary, descriptor = self.dataFD, data = self.data)
    for self.data in self.dataFD:
      self.unique_id += 1
      self.decoder_instance.decoder_class_name_key_added = self.original_tag
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.data )
      self.leading_space_count = len( self.data ) - len( self.data.lstrip() )
      if self.leading_space_count <= self.block_location.get_block_indentation() and \
              " ".join( self.data.split() ).replace( " :", ":" ) != self.data_previous:
        break
      """
      Process blocks associated with the Tnp Protocol
      """
      try:
        """
        String leading/trailing spaces and any before a colon so
        using the converting structure is clean
        """
        self.data_string_to_convert_to_class = " ".join( self.data.split() ).replace( " :", ":" )
        """
        Extract the Decoder class that will process this line of data.
        Execute to the class
        """
        self.decoder_list = self.decoder_instance.decoder_utility. \
          find_decoder( self.data_string_to_convert_to_class,
                        self.decoder_instance.decoder_utility.decoder_automaton )
        self.decoder_instance.decoder_class = self.decoder_list[0][1]
        self.decoder_instance.decoder_class_name_key_added += \
          " {} {}".format( " ".join( self.decoder_list[0][0].lower().split() )[:-1], str( self.unique_id ) )
        CallClass(self).call_class(module_name = os.path.basename(__file__).split('.py')[0], class_name = self.decoder_instance.decoder_class,
                                   dictionary = self.dictionary, descriptor = self.dataFD, data = self.data, decode = None)
      except Exception as error:
        pass
    self.dataFD.seek( self.decoder_instance.previous_index )
    self.decoder_instance.current_index = self.decoder_instance.previous_index
    return()
"""
CLASS: ProtocolMlpppMultilinkBundle
DESCRIPTION:  
INPUT: 
OUTPUT: decoded[] element
"""
class ProtocolMlpppMultilinkBundle:
  "Protocol Mlppp Multilink Bundle"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.data = data
    self.block_location = BlockLocation( self )
    self.block_location.set_block_indentation( self.dataFD )
    self.data_previous = " ".join( data.split() ).replace( " :", ":" )
    self.unique_id = 0
    self.original_tag = self.decoder_instance.decoder_class_name_key_added
    DecoderProcessor(self).execute(dictionary = self.dictionary, descriptor = self.dataFD, data = self.data)
    for self.data in self.dataFD:
      self.unique_id += 1
      self.decoder_instance.decoder_class_name_key_added = self.original_tag
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.data )
      self.leading_space_count = len( self.data ) - len( self.data.lstrip() )
      if self.leading_space_count <= self.block_location.get_block_indentation() and \
              " ".join( self.data.split() ).replace( " :", ":" ) != self.data_previous:
        break
      """
      Process blocks associated with the Mlppp Multilink Bundle Protocol
      """
      try:
        """
        String leading/trailing spaces and any before a colon so
        using the converting structure is clean
        """
        self.data_string_to_convert_to_class = " ".join( self.data.split() ).replace( " :", ":" )
        """
        Extract the Decoder class that will process this line of data.
        Execute to the class
        """
        self.decoder_list = self.decoder_instance.decoder_utility. \
          find_decoder( self.data_string_to_convert_to_class,
                        self.decoder_instance.decoder_utility.decoder_automaton )
        self.decoder_instance.decoder_class = self.decoder_list[0][1]
        self.decoder_instance.decoder_class_name_key_added += \
          " {} {}".format( " ".join( self.decoder_list[0][0].lower().split() )[:-1], str( self.unique_id ) )
        CallClass(self).call_class(module_name = os.path.basename(__file__).split('.py')[0], class_name = self.decoder_instance.decoder_class,
                                   dictionary = self.dictionary, descriptor = self.dataFD, data = self.data, decode = None)
      except Exception as error:
        pass
    self.dataFD.seek( self.decoder_instance.previous_index )
    self.decoder_instance.current_index = self.decoder_instance.previous_index
    return()
"""
CLASS: AutonegotiationInformation
DESCRIPTION:  
INPUT: 
OUTPUT: decoded[] element
"""
class AutonegotiationInformation:
  "Autonegotiation Information"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.value = ""
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.data = data
    self.block_location = BlockLocation( self )
    self.block_location.set_block_indentation( self.dataFD )
    self.data_previous = " ".join( self.data.split() ).replace( " :", ":" )
    self.decoder_instance.decoder_class_name_key_added = "{}".\
         format( self.data.split( ":" )[0].lstrip().strip().lower() )
    for self.data in self.dataFD:
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.data )
      self.data_list = self.data.split()
      self.leading_space_count = len( self.data ) - len( self.data.lstrip() )
      if self.leading_space_count <= self.block_location.get_block_indentation() and \
          " ".join( self.data.split() ).replace( " :", ":" ) != self.data_previous:
        break
      self.data = " ".join( self.data_list )
      """"""
      if self.data.startswith( "Negotiation status" ):
        self.value += "\"{}\":\"{}\",".format( self.data.split( ":" )[0].strip().lower(),
                                               self.data.split( ":" )[1].lstrip().strip().lower() )
      elif self.data.startswith( "Link partner" ):
        self.data = next( self.dataFD )
        self.decoder_instance.previous_index = self.decoder_instance.current_index
        self.decoder_instance.current_index += len( self.data )
        self.leading_space_count = len( self.data ) - len( self.data.lstrip() )
        if self.leading_space_count <= self.block_location.get_block_indentation() and \
            " ".join( self.data.split() ).replace( " :", ":" ) != self.data_previous:
          break
        self.total_count = len( self.data.split( "," ) )
        for count in range( self.total_count ):
          try:
            self.value += "\"link partner {}\":\"{}\",".\
                 format(
                         self.data.split( "," )[count].split( ":" )[0].lstrip().strip().lower(),
                         self.data.split( "," )[count].split( ":" )[1].lstrip().strip().lower().replace( "\n", "" )
                       )
          except:
            break
      elif self.data.startswith( "Local resolution:" ):
        self.data = next( self.dataFD )
        self.decoder_instance.previous_index = self.decoder_instance.current_index
        self.decoder_instance.current_index += len( self.data )
        self.leading_space_count = len( self.data ) - len( self.data.lstrip() )
        if self.leading_space_count <= self.block_location.get_block_indentation() and \
            " ".join( self.data.split() ).replace( " :", ":" ) != self.data_previous:
          break
        self.total_count = len( self.data.split( "," ) )
        for count in range( self.total_count ):
          try:
            self.value += "\"local resolution {}\":\"{}\",".\
                 format(
                         self.data.split( "," )[count].split( ":" )[0].lstrip().strip().lower(),
                         self.data.split( "," )[count].split( ":" )[1].lstrip().strip().lower().replace( "\n", "" )
                       )
          except:
            break
      else:
        break
    self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                       self.decoder_instance.decoder_class_name_key_added] = \
                                       "{{{}}}".format( self.value[:-1] )
    self.dataFD.seek( self.decoder_instance.previous_index )
    self.decoder_instance.current_index = self.decoder_instance.previous_index
    return()
"""
CLASS: SonetProcessor
DESCRIPTION:  
INPUT: 
OUTPUT: decoded[] element
"""
class SonetProcessor:
  "Sonet Processor"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.value = ""
    self.data = data
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.block_location = BlockLocation( self )
    self.block_location.set_block_indentation( self.dataFD )
    self.data_previous = " ".join( self.data.split() ).replace( " :", ":" )
    self.decoder_instance.decoder_class_name_key_added = "{}".\
         format( self.data.split( ":" )[0].lstrip().strip().lower() )
    """
    Adjust pointer back so we know which SONET is being processed
    # FIXME For some reason this HAS to be done just before the
    # FIXME forloop and after the above BlockLocation class call????
    """
    self.dataFD.seek( self.decoder_instance.previous_index, 0 )
    self.decoder_instance.current_index = self.decoder_instance.previous_index
    for self.data in self.dataFD:
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.data )
      self.data_list = self.data.split()
      self.data = " ".join( self.data_list ).replace( " :", ":" )
      """"""
      if self.data.startswith( "SONET alarms:" ):
        self.value += "\"{}\":\"{}\",".format( self.data.split( ":" )[0].strip().lower(),
                                               self.data.split( ":" )[1].lstrip().strip().lower() )
      elif self.data.startswith( "SONET defects:" ):
        self.value += "\"{}\":\"{}\",".format( self.data.split( ":" )[0].strip().lower(),
                                               self.data.split( ":" )[1].lstrip().strip().lower() )
      elif self.data.startswith( "SONET PHY:" ) or \
          self.data.startswith( "SONET section:" ) or \
          self.data.startswith( "SONET line:" ) or \
          self.data.startswith( "SONET path:" ):
        for self.data in self.dataFD:
          self.decoder_instance.previous_index = self.decoder_instance.current_index
          self.decoder_instance.current_index += len( self.data )
          self.leading_space_count = len( self.data ) - len( self.data.lstrip() )
          if self.leading_space_count <= self.block_location.get_block_indentation() and \
              " ".join( self.data.split() ).replace( " :", ":" ) != self.data_previous:
            self.dataFD.seek( self.decoder_instance.previous_index )
            self.decoder_instance.current_index = self.decoder_instance.previous_index
            break
          """"""
          self.data_list = self.data.split()
          self.count = len( self.data_list )
          self.sonet_name = ""
          self.seconds = ""
          self.counters = ""
          self.state = ""
          self.sonet_name_flag = False
          self.seconds_flag = False
          self.counters_flag = False
          self.state_flag = False
          for self.index in range( self.count ):
            if not self.data_list[self.index].isdigit() and \
                not self.sonet_name_flag:
              self.sonet_name += self.data_list[self.index].lower() + " "
              continue
            if self.data_list[self.index].isdigit() and \
                not self.seconds_flag:
              self.sonet_name_flag = True
              self.seconds_flag = True
              self.seconds = self.data_list[self.index]
              continue
            if self.data_list[self.index].isdigit() and \
                not self.counters_flag:
              self.counters_flag = True
              self.counters = self.data_list[self.index]
              continue
            if not self.data_list[self.index].isdigit() and \
                self.sonet_name_flag:
              self.state_flag = True
              self.state += self.data_list[self.index].lower() + " "
              continue
          self.sonet_name = self.sonet_name.strip()
          self.state = self.state.strip()
          if self.sonet_name and self.seconds and self.counters and self.state:
            self.value += "\"{} seconds\":\"{}\",\"{} count\":\"{}\",\"{} state\":\"{}\",". \
              format(
              self.sonet_name,
              self.seconds,
              self.sonet_name,
              self.counters,
              self.sonet_name,
              self.state
            )
          elif self.sonet_name and self.seconds and self.counters and not self.state:
            self.value += "\"{} seconds\":\"{}\",\"{} count\":\"{}\",". \
              format(
              self.sonet_name,
              self.seconds,
              self.sonet_name,
              self.count
            )
          else:
            self.value += "\"{} seconds\":\"{}\",". \
              format(
              self.sonet_name,
              self.seconds
            )
      else:
        break
    self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                       self.decoder_instance.decoder_class_name_key_added] = \
                                       "{{{}}}".format( self.value[:-1] )
    self.dataFD.seek( self.decoder_instance.previous_index )
    self.decoder_instance.current_index = self.decoder_instance.previous_index
    return()
"""
CLASS: PayloadPointerProcessor
DESCRIPTION:  
INPUT: 
OUTPUT: decoded[] element
"""
class PayloadPointerProcessor:
  "Payload Pointer Processor"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.value = ""
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.data = data
    self.block_location = BlockLocation( self )
    self.block_location.set_block_indentation( self.dataFD )
    self.data_previous = " ".join( self.data.split() ).replace( " :", ":" )
    self.decoder_instance.decoder_class_name_key_added = "{}".\
         format( self.data.split( ":" )[0].lstrip().strip().lower() )
    for self.data in self.dataFD:
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.data )
      self.data_list = self.data.split()
      self.leading_space_count = len( self.data ) - len( self.data.lstrip() )
      if self.leading_space_count <= self.block_location.get_block_indentation() and \
          " ".join( self.data.split() ).replace( " :", ":" ) != self.data_previous:
        break
      self.data = " ".join( self.data_list )
      """"""
      try:
        self.value += "\"{}\":\"{}\",".\
             format(
                     self.data.split( ":" )[0].lstrip().strip().lower(),
                     self.data.split( ":" )[1].lstrip().strip().replace( "\n", "" )
                   )
      except:
        break
    self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                       self.decoder_instance.decoder_class_name_key_added] = \
                                       "{{{}}}".format( self.value[:-1] )
    self.dataFD.seek( self.decoder_instance.previous_index )
    self.decoder_instance.current_index = self.decoder_instance.previous_index
    return()
"""
CLASS: ReceivedTransmittedSonetOverheadProcessor
DESCRIPTION:  
INPUT: 
OUTPUT: decoded[] element
"""
class ReceivedTransmittedSonetOverheadProcessor:
  "Received Sonet Overhead Processor"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.value = ""
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.data = data
    self.block_location = BlockLocation( self )
    self.block_location.set_block_indentation( self.dataFD )
    self.data_previous = " ".join( data.split() ).replace( " :", ":" )
    self.decoder_instance.decoder_class_name_key_added = "{}".\
         format( self.data.split( ":" )[0].lstrip().strip().lower() )
    for self.data in self.dataFD:
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.data )
      self.data_list = self.data.split()
      self.leading_space_count = len( self.data ) - len( self.data.lstrip() )
      if self.leading_space_count <= self.block_location.get_block_indentation() and \
          " ".join( self.data.split() ).replace( " :", ":" ) != self.data_previous:
        break
      self.data = " ".join( self.data_list )
      """"""
      self.total_count = len( self.data.split( "," ) )
      for count in range( self.total_count ):
        try:
          self.value += "\"{}\":\"{}\",". \
            format(
            self.data.split( "," )[count].split( ":" )[0].lstrip().strip().lower(),
            self.data.split( "," )[count].split( ":" )[1].lstrip().strip().lower().replace( "\n", "" )
          )
        except:
          break
    self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                       self.decoder_instance.decoder_class_name_key_added] = \
                                       "{{{}}}".format( self.value[:-1] )
    self.dataFD.seek( self.decoder_instance.previous_index )
    self.decoder_instance.current_index = self.decoder_instance.previous_index
    return()
"""
CLASS: ReceivedTransmittedPathTraceProcessor
DESCRIPTION:  
INPUT: 
OUTPUT: decoded[] element
"""
class ReceivedTransmittedPathTraceProcessor:
  "Received Transmitted Path Trace Processor"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.value = ""
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.data = data
    self.block_location = BlockLocation( self )
    self.block_location.set_block_indentation( self.dataFD )
    self.data_previous = " ".join( data.split() ).replace( " :", ":" )
    self.decoder_instance.decoder_class_name_key_added = "{}".\
         format( self.data.split( ":" )[0].lstrip().strip().lower() )
    if self.data.startswith( "Transmitted" ):
      self.value += "\"{}\":\"{}\",".format( self.data.split( ":" )[0].strip().lower(),
                                             self.data.split( ":" )[1].lstrip().strip().lower().replace( "\n", "" ) )
      """
      Set the file pointer to the hex dumpped data we done care about.
      """
      self.data = next( self.dataFD )
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.data )
    elif self.data.startswith( "Received" ):
      if self.data.split( ":" )[1].lstrip().strip().lower().replace( "\n", "" ) != "":
        self.value += "\"{}\":\"{}\",".format( self.data.split( ":" )[0].strip().lower(),
                                               self.data.split( ":" )[1].lstrip().strip().lower().replace( "\n", "" ) )
        """
        Set the file pointer to the hex dumpped data we done care about.
        """
        self.data = next( self.dataFD )
        self.decoder_instance.previous_index = self.decoder_instance.current_index
        self.decoder_instance.current_index += len( self.data )
      else:
        for self.data in self.dataFD:
          self.decoder_instance.previous_index = self.decoder_instance.current_index
          self.decoder_instance.current_index += len( self.data )
          self.data_list = self.data.split()
          self.leading_space_count = len( self.data ) - len( self.data.lstrip() )
          if self.leading_space_count <= self.block_location.get_block_indentation() and \
              " ".join( self.data.split() ).replace( " :", ":" ) != self.data_previous:
            break
          self.data_rcv = " ".join( self.data_list )
          """"""
          if self.data_rcv.startswith( "Host name" ):
            self.value += "\"{}\":\"{}\",".format( self.data_rcv.split( ":" )[0].strip().lower(),
                                                   self.data_rcv.split( ":" )[1].lstrip().strip().lower().replace( "\n", "" ) )
          elif self.data_rcv.startswith( "Interface" ):
            self.value += "\"{}\":\"{}\",".format( self.data_rcv.split( ":" )[0].strip().lower(),
                                                   self.data_rcv.split( ":" )[1].lstrip().strip().lower().replace( "\n", "" ) )
          elif self.data_rcv.startswith( "IP Address" ):
            self.value += "\"{}\":\"{}\",".format( self.data_rcv.split( ":" )[0].strip().lower(),
                                                   self.data_rcv.split( ":" )[1].lstrip().strip().lower().replace( "\n", "" ) )
          else:
            break
    """
    Get the file pointer past the hex dumpped data we done care about.
    """
    self.leading_space_count = len( self.data ) - len( self.data.lstrip() )
    if not self.leading_space_count <= self.block_location.get_block_indentation() and \
        " ".join( self.data.split() ).replace( " :", ":" ) != self.data_previous:
      for self.data in self.dataFD:
        self.decoder_instance.previous_index = self.decoder_instance.current_index
        self.decoder_instance.current_index += len( self.data )
        self.leading_space_count = len( self.data ) - len( self.data.lstrip() )
        if self.leading_space_count <= self.block_location.get_block_indentation() and \
            " ".join( self.data.split() ).replace( " :", ":" ) != self.data_previous:
          break
    """"""
    self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                       self.decoder_instance.decoder_class_name_key_added] = \
                                       "{{{}}}".format( self.value[:-1] )
    self.dataFD.seek( self.decoder_instance.previous_index )
    self.decoder_instance.current_index = self.decoder_instance.previous_index
    return()
"""
CLASS: T1Ds3Processor
DESCRIPTION:  
INPUT: 
OUTPUT: decoded[] element
"""
class T1Ds3Processor:
  "T1/DS3 Processor"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.value = ""
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.data = data
    self.block_location = BlockLocation( self )
    self.block_location.set_block_indentation( self.dataFD )
    self.data_previous = " ".join( data.split() ).replace( " :", ":" )
    self.decoder_instance.decoder_class_name_key_added = "{}".\
         format( self.data.split( ":" )[0].lstrip().strip().lower() )
    for self.data in self.dataFD:
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.data )
      self.leading_space_count = len( self.data ) - len( self.data.lstrip() )
      if self.leading_space_count <= self.block_location.get_block_indentation() and \
          " ".join( self.data.split() ).replace( " :", ":" ) != self.data_previous:
        break
      if self.data.find( ":" ) != -1:
        self.value += "\"{}\":\"{}\",".format( self.data.split( ":" )[0].lstrip().strip().lower(),
                                              self.data.split( ":" )[1].lstrip().strip().lower() )
        continue
      """"""
      self.data_list = self.data.split()
      self.count = len( self.data_list )
      self.sonet_name = ""
      self.seconds = ""
      self.counters = ""
      self.state = ""
      self.sonet_name_flag = False
      self.seconds_flag = False
      self.counters_flag = False
      self.state_flag = False
      for self.index in range( self.count ):
        if not self.data_list[self.index].isdigit() and \
           not self.sonet_name_flag:
          self.sonet_name += self.data_list[self.index].lower() + " "
          continue
        if self.data_list[self.index].isdigit() and \
           not self.seconds_flag:
          self.sonet_name_flag = True
          self.seconds_flag = True
          self.seconds = self.data_list[self.index]
          continue
        if self.data_list[self.index].isdigit() and \
           not self.counters_flag:
          self.counters_flag = True
          self.counters = self.data_list[self.index]
          continue
        if not self.data_list[self.index].isdigit() and \
               self.sonet_name_flag:
          self.state_flag = True
          self.state += self.data_list[self.index].lower() + " "
          continue
      self.sonet_name = self.sonet_name.strip()
      self.state = self.state.strip()
      if self.sonet_name and self.seconds and self.counters and self.state:
        self.value += "\"{} seconds\":\"{}\",\"{} count\":\"{}\",\"{} state\":\"{}\",". \
          format(
          self.sonet_name,
          self.seconds,
          self.sonet_name,
          self.counters,
          self.sonet_name,
          self.state
        )
      elif self.sonet_name and self.seconds and self.counters and not self.state:
        self.value += "\"{} seconds\":\"{}\",\"{} count\":\"{}\",". \
            format(
            self.sonet_name,
            self.seconds,
            self.sonet_name,
            self.count
          )
      else:
        self.value += "\"{} seconds\":\"{}\",". \
              format(
              self.sonet_name,
              self.seconds
            )
    self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                       self.decoder_instance.decoder_class_name_key_added] = \
                                       "{{{}}}".format( self.value[:-1] )
    self.dataFD.seek( self.decoder_instance.previous_index )
    self.decoder_instance.current_index = self.decoder_instance.previous_index
    return()
"""
CLASS: HdlcSatopConfiguration
DESCRIPTION:  
INPUT: 
OUTPUT: decoded[] element
"""
class HdlcSatopConfiguration:
  "HDLC/SAToP Configuration"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.value = ""
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.data = data
    self.block_location = BlockLocation( self )
    self.block_location.set_block_indentation( self.dataFD )
    self.data_previous = " ".join( self.data.split() ).replace( " :", ":" )
    self.decoder_instance.decoder_class_name_key_added = "{}".\
         format( self.data.split( ":" )[0].lstrip().strip().lower() )
    for self.data in self.dataFD:
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.data )
      self.data_list = self.data.split()
      self.leading_space_count = len( self.data ) - len( self.data.lstrip() )
      if self.leading_space_count <= self.block_location.get_block_indentation() and \
          " ".join( self.data.split() ).replace( " :", ":" ) != self.data_previous:
        break
      self.data = " ".join( self.data_list )
      """"""
      self.total_count = len( self.data.split( "," ) )
      if self.total_count > 0:
        for count in range( self.total_count ):
          try:
            self.value += "\"{}\":\"{}\",". \
              format(
              self.data.split( "," )[count].split( ":" )[0].lstrip().strip().lower(),
              self.data.split( "," )[count].split( ":" )[1].lstrip().strip().lower().replace( "\n", "" )
            )
          except:
            break
      else:
        self.value += "\"{}\":\"{}\",".\
             format(
                     self.data.split( ":" )[0].lstrip().strip().lower(),
                     self.data.split( ":" )[1].lstrip().strip().lower().replace( "\n", "" )
                   )
    self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                       self.decoder_instance.decoder_class_name_key_added] = \
                                       "{{{}}}".format( self.value[:-1] )
    self.dataFD.seek( self.decoder_instance.previous_index )
    self.decoder_instance.current_index = self.decoder_instance.previous_index
    return()
"""
CLASS: AtmStatusProcessor
DESCRIPTION:  
INPUT: 
OUTPUT: decoded[] element
"""
class AtmStatusProcessor:
  "ATM Status Processor"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.value = ""
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.data = data
    self.block_location = BlockLocation( self )
    self.block_location.set_block_indentation( self.dataFD )
    self.data_previous = " ".join( self.data.split() ).replace( " :", ":" )
    self.decoder_instance.decoder_class_name_key_added = "{}".\
         format( self.data.split( ":" )[0].lstrip().strip().lower() )
    for self.data in self.dataFD:
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.data )
      self.data_list = self.data.split()
      self.leading_space_count = len( self.data ) - len( self.data.lstrip() )
      if self.leading_space_count <= self.block_location.get_block_indentation() and \
          " ".join( self.data.split() ).replace( " :", ":" ) != self.data_previous:
        break
      self.data = " ".join( self.data_list )
      """"""
      self.value += "\"{}\":\"{}\",".\
           format(
                   self.data.split( ":" )[0].lstrip().strip().lower(),
                   self.data.split( ":" )[1].lstrip().strip().lower().replace( "\n", "" )
                 )
    self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                       self.decoder_instance.decoder_class_name_key_added] = \
                                       "{{{}}}".format( self.value[:-1] )
    self.dataFD.seek( self.decoder_instance.previous_index )
    self.decoder_instance.current_index = self.decoder_instance.previous_index
    return()
"""
CLASS: AtmStatisticsProcessor
DESCRIPTION:  
INPUT: 
OUTPUT: decoded[] element
"""
class AtmStatisticsProcessor:
  "ATM Statistics Processor"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.value = ""
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.data = data
    self.block_location = BlockLocation( self )
    self.block_location.set_block_indentation( self.dataFD )
    self.data_previous = " ".join( self.data.split() ).replace( " :", ":" )
    self.decoder_instance.decoder_class_name_key_added = "{}".\
         format( self.data.split( ":" )[0].lstrip().strip().lower() )
    for self.data in self.dataFD:
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.data )
      self.data_list = self.data.split()
      self.leading_space_count = len( self.data ) - len( self.data.lstrip() )
      if self.leading_space_count <= self.block_location.get_block_indentation() and \
          " ".join( self.data.split() ).replace( " :", ":" ) != self.data_previous:
        break
      self.data = " ".join( self.data_list )
      """"""
      self.total_count = len( self.data.split( "," ) )
      if self.total_count > 0:
        for count in range( self.total_count ):
          try:
            self.value += "\"{}\":\"{}\",". \
              format(
              self.data.split( "," )[count].split( ":" )[0].lstrip().strip().lower(),
              self.data.split( "," )[count].split( ":" )[1].lstrip().strip().lower().replace( "\n", "" )
            )
          except:
            break
      else:
        self.value += "\"{}\":\"{}\",".\
             format(
                     self.data.split( ":" )[0].lstrip().strip().lower(),
                     self.data.split( ":" )[1].lstrip().strip().lower().replace( "\n", "" )
                   )
    self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                       self.decoder_instance.decoder_class_name_key_added] = \
                                       "{{{}}}".format( self.value[:-1] )
    self.dataFD.seek( self.decoder_instance.previous_index )
    self.decoder_instance.current_index = self.decoder_instance.previous_index
    return()
"""
CLASS: PacketForwardingEngineConfiguration
DESCRIPTION:  
INPUT: 
OUTPUT: decoded[] element
"""
class PacketForwardingEngineConfiguration:
  "Packet Forwarding Engine Configuration"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.value = ""
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.data = data
    self.dataFD.seek( self.decoder_instance.previous_index )
    self.decoder_instance.current_index = self.decoder_instance.previous_index
    self.block_location = BlockLocation( self )
    self.block_location.set_block_indentation( self.dataFD )
    self.data_previous = " ".join( self.data.split() ).replace( " :", ":" )
    self.decoder_instance.decoder_class_name_key_added = "{}".\
         format( self.data.split( ":" )[0].lstrip().strip().lower() )
    for self.data in self.dataFD:
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.data )
      self.leading_space_count = len( self.data ) - len( self.data.lstrip() )
      if self.leading_space_count <= self.block_location.get_block_indentation() and \
          " ".join( self.data.split() ).replace( " :", ":" ) != self.data_previous:
        break
      self.data_list = self.data.split()
      self.data = " ".join( self.data_list )
      """"""
      if self.data.startswith( "VPI" ):
        self.decoder_instance.decoder_class_name_key_added = \
             " {} ".format( self.data.lstrip().strip().lower() )
        continue
      else:
        self.total_count = len( self.data.split( "," ) )
        if self.total_count > 0:
          for count in range( self.total_count ):
            try:
              self.value += "\"{}\":\"{}\",". \
                format(
                        self.data.split( "," )[count].split( ":" )[0].lstrip().strip().lower(),
                        self.data.split( "," )[count].split( ":" )[1].lstrip().strip().lower().replace( "\n", "" )
                      )
            except:
              break
        else:
          self.value += "\"{}\":\"{}\",". \
            format(
                    self.data.split( ":" )[0].lstrip().strip().lower(),
                    self.data.split( ":" )[1].lstrip().strip().lower().replace( "\n", "" )
                  )
    self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                       self.decoder_instance.decoder_class_name_key_added] = \
                                       "{{{}}}".format( self.value[:-1] )
    self.dataFD.seek( self.decoder_instance.previous_index )
    self.decoder_instance.current_index = self.decoder_instance.previous_index
    return()
"""
CLASS: InputOutputErrorsProcessor
DESCRIPTION:  
INPUT: 
OUTPUT: decoded[] element
"""
class InputOutputErrorsProcessor:
  "Input Output Errors Processor"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.data = data
    self.block_location = BlockLocation( self )
    self.block_location.set_block_indentation( self.dataFD )
    self.data_previous = " ".join( data.split() ).replace( " :", ":" )
    self.unique_id = 0
    self.original_tag = self.decoder_instance.decoder_class_name_key_added
    for self.data in self.dataFD:
      self.unique_id += 1
      self.decoder_instance.decoder_class_name_key_added = self.original_tag
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.data )
      self.leading_space_count = len( self.data ) - len( self.data.lstrip() )
      if self.leading_space_count <= self.block_location.get_block_indentation() and \
              " ".join( self.data.split() ).replace( " :", ":" ) != self.data_previous:
        break
      """
      Process blocks associated with Input/Output Errors
      """
      try:
        """
        String leading/trailing spaces and any before a colon so
        using the converting structure is clean
        """
        self.data_string_to_convert_to_class = " ".join( self.data.split() ).replace( " :", ":" )
        CallClass(self).call_class(module_name = os.path.basename(__file__).split('.py')[0],
                                   class_name = 'DecoderProcessor', method_name = "execute",
                                   dictionary = self.dictionary, data = self.data, descriptor = self.dataFD)
      except Exception as error:
        self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
        self.dictionary['loggerwidget'].emit(self.message)
        raise Exception(error)
    self.dataFD.seek( self.decoder_instance.previous_index )
    self.decoder_instance.current_index = self.decoder_instance.previous_index
    return()
"""
CLASS: IngressTrafficStatisticsAtPacketForwardingEngine
DESCRIPTION:
INPUT:
OUTPUT:
"""
class IngressTrafficStatisticsAtPacketForwardingEngine:
  "Ingress Traffic Statistics At Packet Forwarding Engine"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.traffic_stats = ""
    for self.data in self.dataFD:
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.data )
      self.data_list = " ".join( self.data.split( ":" ) ).split()
      self.data = " ".join( self.data_list )
      if self.data.startswith( "Input bytes" ):
        self.traffic_stats += "\"ingress FE input bytes\":\"{}\",".format( self.data_list[2].lstrip() )
        try:
          self.traffic_stats += "\"ingress FE input bytes bps\":\"{}\",".format( self.data_list[3].lstrip() )
        except:
          pass
      elif self.data.startswith( "Output bytes" ):
        self.traffic_stats += "\"ingress FE output bytes\":\"{}\",".format( self.data_list[2].lstrip() )
        try:
          self.traffic_stats += "\"ingress FE output bytes bps\":\"{}\",".format( self.data_list[3].lstrip() )
        except:
          pass
      elif self.data.startswith( "Input packets" ):
        self.traffic_stats += "\"ingress FE input packets\":\"{}\",".format( self.data_list[2].lstrip() )
        try:
          self.traffic_stats += "\"ingress FE input packets pps\":\"{}\",".format( self.data_list[3].lstrip() )
        except:
          pass
      elif self.data.startswith( "Output packets" ):
        self.traffic_stats += "\"ingress FE output packets\":\"{}\",".format( self.data_list[2].lstrip() )
        try:
          self.traffic_stats += "\"ingress FE output packets pps\":\"{}\",".format( self.data_list[3].lstrip() )
        except:
          pass
      elif self.data.startswith( "Drop bytes" ):
        self.traffic_stats += "\"ingress FE drop bytes\":\"{}\",".format( self.data_list[2].lstrip() )
        try:
          self.traffic_stats += "\"ingress FE drop bytes pps\":\"{}\",".format( self.data_list[3].lstrip() )
        except:
          pass
      elif self.data.startswith( "Drop packets" ):
        self.traffic_stats += "\"ingress FE drop packets\":\"{}\",".format( self.data_list[2].lstrip() )
        try:
          self.traffic_stats += "\"ingress FE drop packets pps\":\"{}\",".format( self.data_list[3].lstrip() )
        except:
          pass
      else:
        break
    self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                       self.decoder_instance.decoder_class_name_key_added] = \
                                       "{{{}}}".format( self.traffic_stats[:-1] )
    self.dataFD.seek( self.decoder_instance.previous_index )
    self.decoder_instance.current_index = self.decoder_instance.previous_index
    return()
"""
CLASS: CosInformation
DESCRIPTION:
INPUT:
OUTPUT:
"""
class CosInformation:
  "Cos Information"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.cos_info_stats = ""
    self.decoder_instance.decoder_class_name_key_added = "{}".format( " ".join( re.findall( "[A-Z][^A-Z]*",
                                                                                            self.__class__.__name__ ) ).lower() )
    for self.data in self.dataFD:
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.data )
      if self.data.startswith( "\n" ):
        break
      self.leading_space_count = len( self.data ) - len( self.data.lstrip() )
      self.data_list = " ".join( self.data.split() ).replace( " :", ":" ).split()
      self.data = " ".join( self.data_list )
      self.data_list = self.data.split()
      if self.data.startswith("Direction:"):
        self.cos_info_direction = "\"direction\":\"{}\",".format(self.data_list[1].lstrip())
      elif self.data.startswith("CoS transmit queue Bandwidth Buffer Priority Limit"):
        self.data = next( self.dataFD )
        self.decoder_instance.previous_index = self.decoder_instance.current_index
        self.decoder_instance.current_index += len( self.data )
        continue
      elif self.data_list[0].isdigit():
        try:
          self.cos_info_stats += "\"transmit queue {} percentage\":\"{}\",".format( self.data_list[0], self.data_list[2].lstrip())
          self.cos_info_stats += "\"transmit queue {} bandwidth bps\":\"{}\",".format( self.data_list[0], self.data_list[3].lstrip())
          self.cos_info_stats += "\"transmit queue {} bandwidth bps percentage\":\"{}\",".format( self.data_list[0], self.data_list[4].lstrip())
          self.cos_info_stats += "\"transmit queue {} buffer usec\":\"{}\",".format( self.data_list[0], self.data_list[5].lstrip())
          self.cos_info_stats += "\"transmit queue {} priority\":\"{}\",".format( self.data_list[0], self.data_list[6].lstrip())
          self.cos_info_stats += "\"transmit queue {} limit\":\"{}\",".format( self.data_list[0], self.data_list[7].lstrip())
        except:
          pass
      else:
        break
    self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                       self.decoder_instance.decoder_class_name_key_added] = \
                                       "{{{}{}}}".format( self.cos_info_direction, self.cos_info_stats[:-1] )
    self.dataFD.seek( self.decoder_instance.previous_index )
    self.decoder_instance.current_index = self.decoder_instance.previous_index
    return()
"""
CLASS: MacStatisticsProcessor
DESCRIPTION:
INPUT:
OUTPUT:
"""
class MacStatistics:
  "Mac Statistics"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
    self.mac_automaton = ahocorasick.Automaton()  # initialize
    for ( self.key, self.cat ) in macfilterselector:
      self.mac_automaton.add_word(self.key, (self.cat, self.key))  # add keys and categories
    self.mac_automaton.make_automaton()
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.value = ""
    self.decoder_instance.decoder_class_name_key_added = "{}". \
      format( " ".join( re.findall( "[A-Z][^A-Z]*",
                                    self.__class__.__name__ ) ).lower() )
    for self.data in self.dataFD:
      self.data_list = self.data.split()
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.data )
      self.selector_tag = ""
      for end_index, ( self.selector_tag, self.selector_key ) in self.mac_automaton.iter( self.data ):
          break
      if not self.selector_tag:
        break
      if self.selector_tag.split()[-1].startswith( "transmit:" ):
        self.value += "\"{}\":\"{}\",".format( "{}receive".format( self.selector_tag.split( "receive:" )[0] ),
                                               self.data.split("\n")[0].split()[-1] )
        self.value += "\"{}\":\"{}\",".format( "{}transmit".format( self.selector_tag.
                                                                    split( "receive:" )[1].
                                                                    split( "transmit:" )[0].lstrip() ),
                                               self.data.split("\n")[0].split()[-2] )
      elif self.selector_tag.split()[-1].startswith( "receive:" ):
        self.value += "\"{}\":\"{}\",".format( "{}receive".format( self.selector_tag.split( "receive:" )[0] ),
                                               self.data.split("\n")[0].split()[-1] )
      else:
        break
    self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                       self.decoder_instance.decoder_class_name_key_added] = \
                                       "{{{}}}".format( self.value[:-1] )
    self.dataFD.seek( self.decoder_instance.previous_index )
    self.decoder_instance.current_index = self.decoder_instance.previous_index
    return()
"""
CLASS: FilterStatistics
DESCRIPTION:
INPUT:
OUTPUT:
"""
class FilterStatistics:
  "Filter Statistics"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.value = ""
    self.decoder_instance.decoder_class_name_key_added = "{}".\
         format( " ".join( re.findall( "[A-Z][^A-Z]*",
                                       self.__class__.__name__ ) ).lower() )
    for self.data in self.dataFD:
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.data )
      self.data_list = self.data.split()
      self.data = " ".join( self.data_list )
      """"""
      if self.data.startswith( "CAM " ):
        self.value += "\"cam destination filters\":\"{}\",".format( self.data_list[3].split( "," )[0] )
        self.value += "\"cam source filters\":\"{}\",".format( self.data_list[-1] )
      elif self.data.startswith( "Input " ):
        self.value += "\"{}\":\"{}\",".format( " ".join( self.data.split()[:-1] ).lower(), self.data[-1] )
      elif self.data.startswith( "Output " ):
        self.value += "\"{}\":\"{}\",".format( " ".join( self.data.split()[:-1] ).lower(), self.data[-1] )
      else:
        break
    self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                       self.decoder_instance.decoder_class_name_key_added] = \
                                       "{{{}}}".format( self.value[:-1] )
    self.dataFD.seek( self.decoder_instance.previous_index )
    self.decoder_instance.current_index = self.decoder_instance.previous_index
    return()
"""
CLASS: LabelSwitchedTrafficStatistics
DESCRIPTION:
INPUT:
OUTPUT:
"""
class LabelSwitchedTrafficStatistics:
  "Label Switched Traffic Statistics"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dataFD = descriptor
    self.dictionary = dictionary
    for self.data in self.dataFD:
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.data )
      self.data_list = " ".join( self.data.split() ).replace( " :", ":" ).split()
      self.data = " ".join( self.data_list )
      self.decoder_instance.decoder_class_name_key_added = "{}".format( " ".join( re.findall( "[A-Z][^A-Z]*",
                                                               self.__class__.__name__ ) ).lower() )
      if self.data.startswith( "Input bytes:" ) or \
         self.data.startswith( "Input packets:" ) or \
          self.data.startswith( "Input packets:" ) or \
          self.data.startswith( "Output packets:" ):
        """
        Must be counters for top level traffic statistics so the
        file pointer needs to be adjust back one line so the call
        to the counter processor is getting the first line of data correctly
        """
        self.dataFD.seek( self.decoder_instance.previous_index )
        self.decoder_instance.current_index = self.decoder_instance.previous_index
      else:
        """
        No more counters to process exit this class
        """
        break
      """
      Process the counters
      """
      try:
        CallClass(self).call_class(module_name = os.path.basename(__file__).split('.py')[0],
                                   class_name = 'InputOutputStatistics', method_name = "execute",
                                   dictionary = self.dictionary, data = self.data, descriptor = self.dataFD)
      except Exception as error:
        break
    self.dataFD.seek( self.decoder_instance.previous_index )
    self.decoder_instance.current_index = self.decoder_instance.previous_index
    return()
"""
CLASS: DroppedTrafficStatistics
DESCRIPTION:
INPUT:
OUTPUT:
"""
class DroppedTrafficStatistics:
  "Dropped Traffic Statistics"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dataFD = descriptor
    self.dictionary = dictionary
    for self.data in self.dataFD:
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.data )
      self.data_list = " ".join( self.data.split() ).replace( " :", ":" ).split()
      self.data = " ".join( self.data_list )
      self.decoder_instance.decoder_class_name_key_added = "{}".format( " ".join( re.findall( "[A-Z][^A-Z]*",
                                                               self.__class__.__name__ ) ).lower() )
      if self.data.startswith( "Input bytes:" ) or \
         self.data.startswith( "Input packets:" ) or \
          self.data.startswith( "Input packets:" ) or \
          self.data.startswith( "Output packets:" ):
        """
        Must be counters for top level traffic statistics so the
        file pointer needs to be adjust back one line so the call
        to the counter processor is getting the first line of data correctly
        """
        self.dataFD.seek( self.decoder_instance.previous_index )
        self.decoder_instance.current_index = self.decoder_instance.previous_index
      else:
        """
        No more counters to process exit this class
        """
        break
      """
      Process the counters
      """
      try:
        CallClass(self).call_class(module_name = os.path.basename(__file__).split('.py')[0],
                                   class_name = 'InputOutputStatistics', method_name = "execute",
                                   dictionary = self.dictionary, data = self.data, descriptor = self.dataFD)
      except Exception as error:
        break
    self.dataFD.seek( self.decoder_instance.previous_index )
    self.decoder_instance.current_index = self.decoder_instance.previous_index
    return()
"""
CLASS: TrafficStatistics
DESCRIPTION:
INPUT:
OUTPUT:
"""
class TrafficStatistics:
  "Traffic Statistics"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dataFD = descriptor
    self.dictionary = dictionary
    for self.data in self.dataFD:
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.data )
      self.data_list = " ".join( self.data.split() ).replace( " :", ":" ).split()
      self.data = " ".join( self.data_list )
      self.decoder_instance.decoder_class_name_key_added = "{}".format( " ".join( re.findall( "[A-Z][^A-Z]*",
                                                               self.__class__.__name__ ) ).lower() )
      if "IPv6 transit statistics:" in self.data or \
         "Transit statistics:" in self.data or \
         "Local statistics:" in self.data:
        self.decoder_instance.decoder_class_name_key_added += " {}".format( " ".join( " ".join(self.data.split()).lower().
                                                      split( "statistics:" )[0].split() ) )
      elif self.data.startswith( "Input bytes:" ) or \
          self.data.startswith( "Input packets:" ) or \
          self.data.startswith( "Input packets:" ) or \
          self.data.startswith( "Output packets:" ):
        """
        Must be counters for top level traffic statistics so the
        file pointer needs to be adjust back one line so the call
        to the counter processor is getting the first line of data correctly
        """
        self.dataFD.seek( self.decoder_instance.previous_index )
        self.decoder_instance.current_index = self.decoder_instance.previous_index
      else:
        """
        No more counters to process exit this class
        """
        break
      """
      Process the counters
      """
      try:
        CallClass(self).call_class(module_name = os.path.basename(__file__).split('.py')[0],
                                   class_name = 'InputOutputStatistics', method_name = "execute",
                                   dictionary = self.dictionary, data = self.data, descriptor = self.dataFD)
      except Exception as error:
        break
    self.dataFD.seek( self.decoder_instance.previous_index )
    self.decoder_instance.current_index = self.decoder_instance.previous_index
    return()
"""
CLASS: InputOuputStatistics
DESCRIPTION:
INPUT:
OUTPUT:
"""
class InputOutputStatistics:
  "Input Output Statistics"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.traffic_stats = ""
    for self.data in self.dataFD:
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.data )
      self.data_list = " ".join( self.data.split( ":" ) ).split()
      self.data = " ".join( self.data_list )
      try:
        if self.data.startswith( "Input bytes" ):
          self.traffic_stats += "\"input bytes\":\"{}\",".format( self.data_list[2].lstrip() )
          try:
            self.traffic_stats += "\"input bytes bps\":\"{}\",".format( self.data_list[3].lstrip() )
          except:
            pass
        elif self.data.startswith( "Output bytes" ):
          self.traffic_stats += "\"output bytes\":\"{}\",".format( self.data_list[2].lstrip() )
          try:
            self.traffic_stats += "\"output bytes bps\":\"{}\",".format( self.data_list[3].lstrip() )
          except:
            pass
        elif self.data.startswith( "Input packets" ):
          self.traffic_stats += "\"input packets\":\"{}\",".format( self.data_list[2].lstrip() )
          try:
            self.traffic_stats += "\"input packets pps\":\"{}\",".format( self.data_list[3].lstrip() )
          except:
            pass
        elif self.data.startswith( "Output packets" ):
          self.traffic_stats += "\"output packets\":\"{}\",".format( self.data_list[2].lstrip() )
          try:
            self.traffic_stats += "\"output packets pps\":\"{}\",".format( self.data_list[3].lstrip() )
          except:
            pass
        else:
          break
      except Exception as error:
        self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
        self.dictionary['loggerwidget'].emit(self.message)
        raise Exception( error )
    self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                       self.decoder_instance.decoder_class_name_key_added] = \
                                       "{{{}}}".format( self.traffic_stats[:-1] )
    self.dataFD.seek( self.decoder_instance.previous_index )
    self.decoder_instance.current_index = self.decoder_instance.previous_index
    return()
"""
CLASS: BundleLinksInformation
DESCRIPTION:
INPUT:
OUTPUT:
"""
class BundleLinksInformation:
  "Bundle Links Information"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.link_data = ""
    for self.data in self.dataFD:
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.data )
      self.data_list = " ".join( self.data.split( ":" ) ).split()
      self.data = " ".join( self.data_list )
      if self.data.startswith( "Active bundle links" ):
        self.link_data += "\"active bundle links\":\"{}\",".format( self.data_list[3].lstrip() )
      elif self.data.startswith( "Removed bundle links" ):
        self.link_data += "\"removed bundle links\":\"{}\",".format( self.data_list[3].lstrip() )
      elif self.data.startswith( "Disabled bundle links" ):
        self.link_data += "\"disabled bundle links\":\"{}\",".format( self.data_list[3].lstrip() )
      else:
        break
    self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                       self.decoder_instance.decoder_class_name_key_added] = \
                                       "{{{}}}".format( self.link_data[:-1] )
    self.dataFD.seek( self.decoder_instance.previous_index )
    self.decoder_instance.current_index = self.decoder_instance.previous_index
    return()
"""
CLASS: BundleOptions
DESCRIPTION:
INPUT:
OUTPUT:
"""
class BundleOptions:
  "Bundle Options"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.link_data = ""
    for self.data in self.dataFD:
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.data )
      self.data_list = " ".join( self.data.split( ":" ) ).split()
      self.data = " ".join( self.data_list )
      if self.data.startswith( "MRRU" ):
        self.value = self.data.split( "MRRU" )[1]
        self.link_data += "\"mrru\":\"{}\",".format( self.value.lstrip() )
      elif self.data.startswith( "Remote MRRU" ):
        self.value = self.data.split( "Remote MRRU" )[1]
        self.link_data += "\"remote mrru\":\"{}\",".format( self.value.lstrip() )
      elif self.data.startswith( "Drop timer period" ):
        self.value = self.data.split( "Drop timer period" )[1]
        self.link_data += "\"drop timer period\":\"{}\",".format( self.value.lstrip() )
      elif self.data.startswith( "Inner PPP Protocol field compression" ):
        self.value = self.data.split( "Inner PPP Protocol field compression" )[1]
        self.link_data += "\"inner ppp protocol field compression\":\"{}\",".format( self.value.lstrip() )
      elif self.data.startswith( "Sequence number format" ):
        self.value = self.data.split( "Sequence number format" )[1]
        self.link_data += "\"sequence number format\":\"{}\",".format( self.value.lstrip() )
      elif self.data.startswith( "Fragmentation threshold" ):
        self.value = self.data.split( "Fragmentation threshold" )[1]
        self.link_data += "\"fragmentation threshold\":\"{}\",".format( self.value.lstrip() )
      elif self.data.startswith( "Links needed to sustain bundle" ):
        self.value = self.data.split( "Links needed to sustain bundle" )[1]
        self.link_data += "\"links needed to sustain bundle\":\"{}\",".format( self.value.lstrip() )
      elif self.data.startswith( "Multilink classes" ):
        self.value = self.data.split( "Multilink classes" )[1]
        self.link_data += "\"multilink classes\":\"{}\",".format( self.value.lstrip() )
      elif self.data.startswith( "Link layer overhead" ):
        self.value = self.data.split( "Link layer overhead" )[1]
        self.link_data += "\"link layer overhead\":\"{}\",".format( self.value.lstrip() )
      else:
        break
    self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                       self.decoder_instance.decoder_class_name_key_added] = \
                                       "{{{}}}".format( self.link_data[:-1] )
    self.dataFD.seek( self.decoder_instance.previous_index )
    self.decoder_instance.current_index = self.decoder_instance.previous_index
    return()
"""
CLASS: MultilinkClassStatus
DESCRIPTION:
INPUT:
OUTPUT:
"""
class MultilinkClassStatus:
  "Multilink Class Status"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.link_data = ""
    for self.data in self.dataFD:
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.data )
      self.data_list = " ".join( self.data.split( ":" ) ).split()
      self.data = " ".join( self.data_list )
      if self.data.startswith( "Received sequence number" ):
        self.value = self.data.split( "Received sequence number" )[1]
        self.link_data += "\"received sequence number\":\"{}\",".format( self.value.lstrip() )
      elif self.data.startswith( "Transmit sequence number" ):
        self.value = self.data.split( "Transmit sequence number" )[1]
        self.link_data += "\"transmit sequence number\":\"{}\",".format( self.value.lstrip() )
      elif self.data.startswith( "Packet drops" ):
        self.value = self.data.split( "Packet drops" )[1]
        self.link_data += "\"packet drops\":\"{}\",".format( self.value.lstrip() )
      elif self.data.startswith( "Fragment drops" ):
        self.value = self.data.split( "Fragment drops" )[1]
        self.link_data += "\"fragment drops\":\"{}\",".format( self.value.lstrip() )
      elif self.data.startswith( "MRRU exceeded" ):
        self.value = self.data.split( "MRRU exceeded" )[1]
        self.link_data += "\"mrru exceeded\":\"{}\",".format( self.value.lstrip() )
      elif self.data.startswith( "Fragment timeout" ):
        self.value = self.data.split( "Fragment timeout" )[1]
        self.link_data += "\"fragment timeout\":\"{}\",".format( self.value.lstrip() )
      elif self.data.startswith( "Missing sequence number" ):
        self.value = self.data.split( "Missing sequence number" )[1]
        self.link_data += "\"missing sequence number\":\"{}\",".format( self.value.lstrip() )
      elif self.data.startswith( "Out-of-order sequence number" ):
        self.value = self.data.split( "Out-of-order sequence number" )[1]
        self.link_data += "\"out-of-order sequence number\":\"{}\",".format( self.value.lstrip() )
      elif self.data.startswith( "Out-of-range sequence number" ):
        self.value = self.data.split( "Out-of-range sequence number" )[1]
        self.link_data += "\"out-of-range sequence number\":\"{}\",".format( self.value.lstrip() )
      elif self.data.startswith( "Packet data buffer overflow" ):
        self.value = self.data.split( "Packet data buffer overflow" )[1]
        self.link_data += "\"packet data buffer overflow\":\"{}\",".format( self.value.lstrip() )
      elif self.data.startswith( "Fragment data buffer overflow" ):
        self.value = self.data.split( "Fragment data buffer overflow" )[1]
        self.link_data += "\"fragment data buffer overflow\":\"{}\",".format( self.value.lstrip() )
      elif self.data.startswith( "Multilink class drop timeout" ):
        self.value = self.data.split( "Multilink class drop timeout" )[1]
        self.link_data += "\"multilink class drop timeout\":\"{}\",".format( self.value.lstrip() )
      else:
        break
    self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                       self.decoder_instance.decoder_class_name_key_added] = \
                                       "{{{}}}".format( self.link_data[:-1] )
    self.dataFD.seek( self.decoder_instance.previous_index )
    self.decoder_instance.current_index = self.decoder_instance.previous_index
    return()
"""
CLASS: StatisticsFramesFpsBytesBps
DESCRIPTION: This class is a primary controlling class for statistcial data collection
             for logical insterfaces such as the LSQ interface.
INPUT:
OUTPUT:
"""
class StatisticsFramesFpsBytesBps:
  "Statistics Frames Fps Bytes Bps"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dataFD = descriptor
    self.dictionary = dictionary
    for self.data in self.dataFD:
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.data )
      self.class_to_execute = "".join( " ".join( self.data.split() ).title().split() ).replace( " :", ":" ).replace( ":", "" )
      self.decoder_instance.decoder_class_name_key_added = "interface statistics "
      try:
        CallClass(self).call_class(module_name = os.path.basename(__file__).split('.py')[0],
                                   class_name = self.class_to_execute, method_name = "execute",
                                   dictionary = self.dictionary, data = self.data, descriptor = self.dataFD)
      except Exception as error:
        break
    self.dataFD.seek( self.decoder_instance.previous_index )
    self.decoder_instance.current_index = self.decoder_instance.previous_index
    return()
"""
CLASS: Bundle
DESCRIPTION:
INPUT:
OUTPUT:
"""
class Bundle:
  "Bundle"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.decoder_instance.decoder_class_name_key_added = "bundle "
    for self.data in self.dataFD:
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.data )
      self.data = " ".join( self.data.split() ).replace( " :", ":" )
      self.data_list = self.data.split()
      if self.data.startswith( "Multilink:" ):
        self.tag = "multilink "
        continue
      if self.data.startswith( "Network:" ):
        self.tag = "network "
        continue
      if self.data.startswith( "Input:" ):
        self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                           self.decoder_instance.decoder_class_name_key_added +
                                           self.tag +
                                           "input"] = \
        "{{\"frames\":\"{}\",\"fps\":\"{}\",\"bytes\":\"{}\",\"bps\":\"{}\"}}".\
                                    format( self.data_list[1].lstrip(),
                                            self.data_list[2].lstrip(),
                                            self.data_list[3].lstrip(),
                                            self.data_list[4].lstrip()
                                          )
      elif self.data.startswith( "Output:" ):
        self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                           self.decoder_instance.decoder_class_name_key_added +
                                           self.tag +
                                           "output"] = \
          "{{\"frames\":\"{}\",\"fps\":\"{}\",\"bytes\":\"{}\",\"bps\":\"{}\"}}".\
                                    format( self.data_list[1].lstrip(),
                                            self.data_list[2].lstrip(),
                                            self.data_list[3].lstrip(),
                                            self.data_list[4].lstrip()
                                          )
      else:
        break
    self.dataFD.seek( self.decoder_instance.previous_index )
    self.decoder_instance.current_index = self.decoder_instance.previous_index
    return()
"""
CLASS: Ipv6TransitStatisticsPacketsBytes
DESCRIPTION:
INPUT:
OUTPUT:
"""
class Ipv6TransitStatisticsPacketsBytes:
  "IPV6 Transit Statistics Packets Bytes"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.decoder_instance.decoder_class_name_key_added = "ipv6 transit statistics "
    self.stat_data = ""
    for self.data in self.dataFD:
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.data )
      self.data = " ".join( self.data.split() ).replace( " :", ":" )
      self.data_list = self.data.split()
      if self.data.startswith( "Network:" ):
        self.tag = "network "
        continue
      if self.data.startswith( "Input:" ):
        self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                           self.decoder_instance.decoder_class_name_key_added +
                                           self.tag +
                                           "input"] = \
                                           "{{\"packet\":\"{}\",\"bytes\":\"{}\"}}".\
                                                         format( self.data_list[1].lstrip(),
                                                                 self.data_list[2].lstrip()
                                                               )
      elif self.data.startswith( "Output:" ):
        self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                           self.decoder_instance.decoder_class_name_key_added +
                                           self.tag +
                                           "output"] = \
                                          "{{\"packet\":\"{}\",\"bytes\":\"{}\"}}".\
                                                        format( self.data_list[1].lstrip(),
                                                                self.data_list[2].lstrip()
                                                              )
      else:
        break
    self.dataFD.seek( self.decoder_instance.previous_index )
    self.decoder_instance.current_index = self.decoder_instance.previous_index
    return()
"""
CLASS: MultilinkDetailStatistics
DESCRIPTION:
INPUT:
OUTPUT:
"""
class MultilinkDetailStatistics:
  "Multilink Detail Statistics"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.decoder_instance.decoder_class_name_key_added = "multilink detailed statistics "
    self.tag = ""
    self.second_tag = ""
    for self.data in self.dataFD:
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.data )
      self.data = " ".join( self.data.split() ).replace( " :", ":" )
      self.data_list = self.data.split()
      if self.data.startswith( "Bundle:" ):
        self.tag = "bundle "
        continue
      if self.data.startswith( "Fragments:" ):
        self.second_tag = "fragments "
        continue
      if self.data.startswith( "Non-fragments:" ):
        self.second_tag = "non-fragments "
        continue
      if self.data.startswith( "LFI:" ):
        self.second_tag = "lfi "
        continue
      if self.data.startswith( "Input:" ):
        self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                           self.decoder_instance.decoder_class_name_key_added +
                                           self.tag + self.second_tag +
                                           "input"] = \
          "{{\"frames\":\"{}\",\"fps\":\"{}\",\"bytes\":\"{}\",\"bps\":\"{}\"}}".format( self.data_list[1],
                                                                                        self.data_list[2],
                                                                                        self.data_list[3],
                                                                                        self.data_list[4]
                                                                                        )
      elif self.data.startswith( "Output:" ):
        self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                           self.decoder_instance.decoder_class_name_key_added +
                                           self.tag + self.second_tag +
                                           "input"] = \
          "{{\"frames\":\"{}\",\"fps\":\"{}\",\"bytes\":\"{}\",\"bps\":\"{}\"}}".format( self.data_list[1],
                                                                                        self.data_list[2],
                                                                                        self.data_list[3],
                                                                                        self.data_list[4]
                                                                                        )
      else:
        break
    self.dataFD.seek( self.decoder_instance.previous_index )
    self.decoder_instance.current_index = self.decoder_instance.previous_index
    return()
"""
CLASS: Link
DESCRIPTION:
INPUT:
OUTPUT:
"""
class Link:
  "Link"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.decoder_instance.decoder_class_name_key_added = "link_"
    self.block_location = BlockLocation( self )
    self.block_location.set_block_indentation( self.dataFD )
    self.tag = ""
    for self.data in self.dataFD:
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.data )
      self.leading_space_count = len( self.data ) - len( self.data.lstrip() )
      self.data = " ".join( self.data.split() ).replace( " :", ":" )
      self.data_list = self.data.split()
      if self.leading_space_count <= self.block_location.get_block_indentation():
        break
      if self.leading_space_count == 6:
        self.tag = "{} ".format( self.data_list[0] )
        continue
      if self.data.startswith( "Up time:" ):
        self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                           self.decoder_instance.decoder_class_name_key_added +
                                           self.tag +
                                           "up time"] = \
                                           "{{\"up time\":\"{}\"}}".format( self.data_list[2] )
        continue
      if self.data.startswith( "Input:" ):
        self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                           self.decoder_instance.decoder_class_name_key_added +
                                           self.tag +
                                           "input"] = \
          "{{\"frames\":\"{}\",\"fps\":\"{}\",\"bytes\":\"{}\",\"bps\":\"{}\"}}".format( self.data_list[1],
                                                                                        self.data_list[2],
                                                                                        self.data_list[3],
                                                                                        self.data_list[4]
                                                                                        )
        continue
      if self.data.startswith( "Output:" ):
        self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                           self.decoder_instance.decoder_class_name_key_added +
                                           self.tag +
                                           "output"] = \
          "{{\"frames\":\"{}\",\"fps\":\"{}\",\"bytes\":\"{}\",\"bps\":\"{}\"}}".format( self.data_list[1],
                                                                                        self.data_list[2],
                                                                                        self.data_list[3],
                                                                                        self.data_list[4]
                                                                                        )
        continue
    self.dataFD.seek( self.decoder_instance.previous_index )
    self.decoder_instance.current_index = self.decoder_instance.previous_index
    return()
"""
CLASS: FrameExceptions
DESCRIPTION:
INPUT:
OUTPUT:
"""
class FrameExceptions:
  "Frame Exceptions"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.exception_data = ""
    for self.data in self.dataFD:
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.data )
      self.data_list = " ".join( self.data.split( ":" ) ).split()
      self.data = " ".join( self.data_list )
      if self.data.startswith( "Oversized frames" ):
        self.exception_data += "\"oversized frames\":\"{}\",".format( self.data_list[2] )
      elif self.data.startswith( "Errored input frames" ):
        self.exception_data += "\"errored input frames\":\"{}\",".format( self.data_list[3] )
      elif self.data.startswith( "Input on disabled link/bundle" ):
        self.exception_data += "\"input on disabled link/bundle\":\"{}\",".format( self.data_list[4] )
      elif self.data.startswith( "Output for disabled link/bundle" ):
        self.exception_data += "\"output for disabled link/bundle\":\"{}\",".format( self.data_list[4] )
      elif self.data.startswith( "Queuing drops" ):
        self.exception_data += "\"queuing drops\":\"{}\",".format( self.data_list[2] )
      else:
        break
    self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                       self.decoder_instance.decoder_class_name_key_added] = \
                                       "{{{}}}".format( self.exception_data[:-1] )
    self.dataFD.seek( self.decoder_instance.previous_index )
    self.decoder_instance.current_index = self.decoder_instance.previous_index
    return()
"""
CLASS: BufferingExceptions
DESCRIPTION:
INPUT:
OUTPUT:
"""
class BufferingExceptions:
  "Buffering Exceptions"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.exception_data = ""
    for self.data in self.dataFD:
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.data )
      self.data_list = " ".join( self.data.split( ":" ) ).split()
      self.data = " ".join( self.data_list )
      if self.data.startswith( "Packet data buffer overflow" ):
        self.exception_data += "\"packet data buffer overflow\":\"{}\",".format( self.data_list[4] )
      elif self.data.startswith( "Fragment data buffer overflow" ):
        self.exception_data += "\"fragment data buffer overflow\":\"{}\",".format( self.data_list[4] )
      else:
        break
    self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                       self.decoder_instance.decoder_class_name_key_added] = \
                                       "{{{}}}".format( self.exception_data[:-1] )
    self.dataFD.seek( self.decoder_instance.previous_index )
    self.decoder_instance.current_index = self.decoder_instance.previous_index
    return()
"""
CLASS: AssemblyExceptions
DESCRIPTION:
INPUT:
OUTPUT:
"""
class AssemblyExceptions:
  "Assembly Exceptions"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.exception_data = ""
    for self.data in self.dataFD:
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.data )
      self.data_list = " ".join( self.data.split( ":" ) ).split()
      self.data = " ".join( self.data_list )
      if self.data.startswith( "Fragment timeout" ):
        self.exception_data += "\"frame timeout\":\"{}\",".format( self.data_list[2] )
      elif self.data.startswith( "Missing sequence number" ):
        self.exception_data += "\"missing sequence number\":\"{}\",".format( self.data_list[3] )
      elif self.data.startswith( "Out-of-order sequence number" ):
        self.exception_data += "\"out-of-order sequence number\":\"{}\",".format( self.data_list[3] )
      elif self.data.startswith( "Out-of-range sequence number" ):
        self.exception_data += "\"out-of-range sequence number\":\"{}\",".format( self.data_list[3] )
      else:
        break
    self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                       self.decoder_instance.decoder_class_name_key_added] = \
                                       "{{{}}}".format( self.exception_data[:-1] )
    self.dataFD.seek( self.decoder_instance.previous_index )
    self.decoder_instance.current_index = self.decoder_instance.previous_index
    return()
"""
CLASS: HardwareErrorsSticky
DESCRIPTION:
INPUT:
OUTPUT:
"""
class HardwareErrorsSticky:
  "Hardware Errors Sticky"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.exception_data = ""
    for self.data in self.dataFD:
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.data )
      self.data_list = " ".join( self.data.split( ":" ) ).split()
      self.data = " ".join( self.data_list )
      if self.data.startswith( "Data memory error" ):
        self.exception_data += "\"data memory error\":\"{}\",".format( self.data_list[3] )
      elif self.data.startswith( "Control memory error" ):
        self.exception_data += "\"control memory error\":\"{}\",".format( self.data_list[3] )
      else:
        break
    self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                       self.decoder_instance.decoder_class_name_key_added] = \
                                       "{{{}}}".format( self.exception_data[:-1] )
    self.dataFD.seek( self.decoder_instance.previous_index )
    self.decoder_instance.current_index = self.decoder_instance.previous_index
    return()
"""
CLASS: QueueCounters
DESCRIPTION:
INPUT:
OUTPUT:
"""
class QueueCounters:
  "Queue Counters"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
    self.que_count = self.parent.que_count
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.queue_counters = ""
    for self.data in self.dataFD:
      self.data_list = self.data.split()
      self.que_count -= 1
      if self.que_count < 0 or not self.data_list[0].isdigit():
        self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                     self.decoder_instance.decoder_class_name_key_added +
                     " counters"] = "{{{}}}".format( self.queue_counters[:-1] )
        """
        Reset file pointer back one line so the new
        correct line is processed next
        """
        self.dataFD.seek( self.decoder_instance.current_index )
        break
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.data )
      try:
        self.queue_counters += "\"queue counter {} queued packets\":\"{}\"," \
                               "\"queue counter {} transmitted packets\":\"{}\"," \
                               "\"queue counter {} dropped packets\":\"{}\",".\
                               format(
                                       self.data_list[0],
                                       self.data_list[1],
                                       self.data_list[0],
                                       self.data_list[2],
                                       self.data_list[0],
                                       self.data_list[3]
                                     )
      except:
        try:
          self.queue_counters += "\"queue counters {} {} queued packets\":\"{}\"," \
                                 "\"queue counters {} {} transmitted packets\":\"{}\"," \
                                 "\"queue counters {} {} dropped packets\":\"{}\",". \
            format(
                    self.data_list[0],
                    self.data_list[1],
                    self.data_list[2],
                    self.data_list[0],
                    self.data_list[1],
                    self.data_list[3],
                    self.data_list[0],
                    self.data_list[1],
                    self.data_list[4]
                  )
        except:
          pass
    return()
"""
CLASS: QueueNumber
DESCRIPTION:
INPUT:
OUTPUT:
"""
class QueueNumber:
  "Queue Number"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
    self.que_count = self.parent.que_count
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.queue_number = ""
    for self.data in self.dataFD:
      self.data_list = self.data.split()
      self.que_count -= 1
      if self.que_count < 0 or not self.data_list[0].isdigit():
        self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                           self.decoder_instance.decoder_class_name_key_added +
                                           " numbers"] = "{{{}}}".format( self.queue_number[:-1] )
        """
        Reset file pointer back one line so the new
        correct line is processed next
        """
        self.dataFD.seek( self.decoder_instance.current_index )
        break
      self.decoder_instance.previous_index = self.decoder_instance.current_index
      self.decoder_instance.current_index += len( self.data )
      try:
        self.queue_number += "\"queue numbers {}\":{{\"mapped forwarding classes\":\"{}\"}},".\
                               format( self.data_list[0],
                                       self.data_list[1] )
      except Exception as error:
        self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
        self.dictionary['loggerwidget'].emit(self.message)
        raise Exception( error )
    return()
"""
CLASS: InterfaceTransmitStatistics
DESCRIPTION:
INPUT:
OUTPUT:
"""
class InterfaceTransmitStatistics:
  "Interface Transmit Statistics"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.data = data
    self.data_list = self.data.split()
    try:
      self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                         self.decoder_instance.decoder_class_name_key_added] = \
                  "{{\"{}\":\"{}\"}}".format( "interface transmit statistics", self.data_list[3] )
    except Exception as error:
      self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
      self.dictionary['loggerwidget'].emit(self.message)
      raise Exception( error )
    return()
"""
CLASS: DecoderProcessor
DESCRIPTION: Generic processor for each show command report data.
INPUT:  Single input line from show command report data.
OUTPUT: Analysis seed data associated to each input line.
"""
class DecoderProcessor:
  "Decoder Processor"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.decoder_instance = self.parent.decoder_instance
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.data = data.replace( " :", ":" )
    self.data_list = self.data.split()
    self.lines = iter(self.data_list)
    self.index = 0
    self.key = ""
    self.value = ""
    self.key_value_pairs = ""
    self.key_value_pairs_str = ""
    self.key_value_pairs_dist_str = ""
    self.key_value_pairs_dist = {}
    self.colon_flag = False
    try:
      self.key = next(self.lines) + " "
      self.key = self.key.lower()
      while(True):
        self.index = self.key.rfind(":")
        if self.index == -1:
          self.key += next(self.lines) + " "
        else:
          self.colon_flag = True
          self.value = ""
          while(True):
            self.value += next(self.lines) + " "
            self.index = self.value.rfind(":")
            if not self.index == -1:
              self.value_index = self.value.rfind(",")
              if self.value_index == -1:
                if "".join( self.value.split( ":" )[0].split()[:-1] ) == "":
                  self.key = self.value.lstrip().strip().lower()
                  self.value = next(self.lines) + " "
                  continue
                self.mod_key = "\"{}\":".format(self.key.split(":")[0])
                self.new_key_value_pair = self.mod_key + "\"{}\"". \
                     format( " ".join( self.value.split( ":" )[0].split()[:-1] ) )
                self.key = "{}{}:".format( "".join( self.key.split( ":" ) ),
                                          self.value.split( ":" )[0].split()[-1].lower().lstrip() )
              else:
                self.mod_key = "\"{}\":".format(self.key.split(":")[0].lower())
                self.new_key_value_pair = self.mod_key + "\"{}\"".\
                     format( self.value[:self.value_index] )
                self.key = self.value[self.value_index + 2:-1]
              break
          if self.key_value_pairs == "":
            self.key_value_pairs += self.new_key_value_pair
          else:
            self.key_value_pairs += "," + self.new_key_value_pair
    except StopIteration:
      if not self.colon_flag :
        self.data_list = self.data.split()
        self.lines = iter(self.data_list)
        self.key = ""
        self.value = ""
        self.key_value_pairs = ""
        self.key_value_pairs_str = ""
        self.key_value_pairs_dist = {}
        try:
          self.key = next(self.lines) + " "
          self.value = ""
          while (True):
            self.value += next(self.lines) + " "
            self.index = self.value.rfind(",")
            if self.index == -1:
              self.key += self.value
              self.value = ""
              continue
            if not self.index == -1:
              self.new_key_value_pair = "\"{}\":\"{}\"".\
                   format(self.key[:-1], self.value[:self.index])
              self.value = ""
            if self.key_value_pairs == "":
              self.key_value_pairs += self.new_key_value_pair
              self.key = ""
            else:
              self.key_value_pairs += "," + self.new_key_value_pair
              self.key = ""
        except StopIteration:
          self.key_value_pairs += ",\"{}\":\"{}\"".\
               format(" ".join( self.key.split()[:-1] ), self.key.split()[-1])
          self.key_value_pairs_dist_str = "{{{}}}".format( self.key_value_pairs )
      else:
        self.mod_key = "\"{}\":".format(self.key.split(":")[0].lower())
        if not len( self.key_value_pairs )  > 0:
          self.key_value_pairs = self.mod_key + "\"{}\"".format( self.value.strip() )
        else:
          self.key_value_pairs += "," + self.mod_key + "\"{}\"".format( self.value.strip().rstrip(",") )
        self.key_value_pairs_dist_str = "{{{}}}".format( self.key_value_pairs )
    # notes DEBUG CODE
    # notes DEBUG CODE try:
    # notes DEBUG CODE    self.key_value_pairs_dist = ast.literal_eval(self.key_value_pairs_dist_str)
    # notes DEBUG CODE except Exception as error:
    # notes DEBUG CODE    print(error)
    # notes DEBUG CODE for self.key, self.value in self.key_value_pairs_dist.items():
    # notes DEBUG CODE    print("{} : {}".format(self.key, self.value))
    # notes DEBUG CODE # FIXME DEBUG CODE
    self.decoder_instance.decoded_data[self.decoder_instance.decoder_class_name_key +
                                       self.decoder_instance.decoder_class_name_key_added] = \
                                       self.key_value_pairs_dist_str
    return()
"""
CLASS: NoOperation
DESCRIPTION: Ignore the data being analysis at this point
INPUT: Analysis data from devices
OUTPUT: Nothing
"""
class NoOperation:
  "No Operation"
  """"""
  def __init__( self, parent = None, decoder_instance = None ):
    self.name = self.__class__.__name__
    self.parent = parent
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dataFD = descriptor
    self.dictionary = dictionary
    self.data = data
    self.data = self.data.lstrip()
    """
    Ignore Juniper support data.
    """
    if self.data.startswith( "Generation" ) and self.dictionary['device'] == "juniper":
      return()
    try:
      print("NoOperation with: {} {} {}".format( self.data.split()[0], self.data.split()[1], self.data.split()[2] ))
    except:
      try:
        print( "NoOperation with: {} {}".format( self.data.split()[0], self.data.split()[1] ) )
      except:
        try:
          print( "NoOperation with: {}".format( self.data.split()[0] ) )
        except Exception as error:
          self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
          self.dictionary['loggerwidget'].emit(self.message)
          raise Exception( "NoOperation failed to print!" )
    return()
"""
End of File
"""
