"""*******************************************************************************************************
Received DecoderFactory
MODULE:  DecoderFactory
Author: Christopher Robson
Copyright by:  Christopher Robson
Copyright date: 08Oct2017
FIXME !! THIS CLASS IS PROPRIETARY AND MY NOT BE REUSED BY ANYONE BUT THE AUTHOR!!
FIXME THIS MODULE DOES NOT BELONG TO ANY CONTRACTING COMPANY OR THE GOVERNMENT!
FIXME IT WAS DEVELOPED ON THE AUTHORS OWN PERSONAL TIME !!!!!!!!!!!!!!!!!!!!
This software is not FREE!  Use or destribution of the software system and its
subsystem modules, libraries, configuration file and "seed" file without the
express permission of the author is strictly PROHIBITED!
FUNCTION:  Module take an input string and converts to a CLASS.
*******************************************************************************************************"""
"""
Script libraries
"""
from Globals import *
from CallClass import CallClass
"""
CLASS __STR__
DESCRIPTION: __str__ override function which converts input into a class
INPUT: Network device output data
OUTPUT: Class output data based on class called
"""
class __str__(object):
  def __str__(message):
    pass
  def decode(self, dictionary = None, decoder_instance = None, descriptor = None, data = "", index = None):
    self.name = "DecoderFactory"
    self.dictionary = dictionary
    self.decoder_instance = decoder_instance
    self.dataFD = descriptor
    self.data = data
    self.logger_message_signal = self.dictionary['loggerwidget'] # notes needed by CallClass for error messages
    if self.data.startswith( "\n" ):
      return()
    """
    Remove multiple spaces before the colon, 
    making it cleaner to determine which decoder to use
    """
    try:
      self.data_list = self.data.split()
      self.data = " ".join( self.data_list )
    except Exception as error:
      self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
      self.dictionary['loggerwidget'].emit(self.message)
      raise Exception
    if self.dictionary['device'] == 'juniper':
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
        self.decoder_list = self.decoder_instance.decoder_utility.find_decoder(self.data_string_to_convert_to_class,
                                                                               self.decoder_instance.decoder_utility.decoder_automaton )
        for self.class_string, self.class_name in self.decoder_list:
          if self.data_string_to_convert_to_class.startswith( self.class_string ):
            break
        else:
          self.message = "{{{}DecoderFactory: Invalid class: {} - {}{}}}".format(Globals.RED_MESSAGE, self.class_string, self.data_string_to_convert_to_class, Globals.SPAN_END_MESSAGE)
          self.dictionary['loggerwidget'].emit(self.message)
          raise Exception
        self.decoder_instance.decoder_class = self.class_name
        self.decoder_instance.decoder_class_name = self.class_string
        if self.decoder_instance.decoder_class_name[-1] == ":":
          self.decoder_instance.decoder_class_name_key_added = " ".join( self.decoder_instance.decoder_class_name.lower().split() )[:-1]
        else:
          self.decoder_instance.decoder_class_name_key_added = " ".join(self.decoder_instance.decoder_class_name.lower().split())
        CallClass(self).call_class(module_name = "DecodeDataProcessor",
                                   class_name = self.class_name, method_name = "execute",
                                   dictionary = self.dictionary, data = self.data, descriptor = self.dataFD)
      except Exception as error:
        if error.args:
          self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, "DecoderFactory:", error, Globals.SPAN_END_MESSAGE)
          self.dictionary['loggerwidget'].emit(self.message)
        raise Exception
      return()
    """
    TenGigE0/2/0/0 is administratively down, line protocol is administratively down 
      Interface state transitions: 0
      Hardware is TenGigE, address is 10f3.1160.65fc (bia 10f3.1160.65fc)
      Layer 1 Transport Mode is LAN
      Description: R91-R93_Hu0/7/0/1 - MDA 100GE troubleshooting
      Internet address is 33.20.91.253/30
      MTU 4484 bytes, BW 10000000 Kbit (Max: 10000000 Kbit)
         reliability 255/255, txload 0/255, rxload 0/255
      Encapsulation ARPA,
      Full-duplex, 10000Mb/s, link type is force-up
      output flow control is off, input flow control is off
      Carrier delay (up) is 10 msec
      loopback not set,
      ARP type ARPA, ARP timeout 04:00:00
      Last input never, output never
      Last clearing of "show interface" counters 2w3d
      30 second input rate 0 bits/sec, 0 packets/sec
      30 second output rate 0 bits/sec, 0 packets/sec
         0 packets input, 0 bytes, 0 total input drops
         0 drops for unrecognized upper-level protocol
         Received 0 broadcast packets, 0 multicast packets
                  0 runts, 0 giants, 0 throttles, 0 parity
         0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored, 0 abort
         0 packets output, 0 bytes, 0 total output drops
         Output 0 broadcast packets, 0 multicast packets
         0 output errors, 0 underruns, 0 applique, 0 resets
         0 output buffer failures, 0 output buffers swapped out
         0 carrier transitions
    """
    if self.dictionary['device'] == 'cisco':
      try:
        self.decoder_str = self.data.split()
        self.decoder_list = self.decoder_instance.decoder_utility.find_decoder(self.data_string_to_convert_to_class,
                                                                               self.decoder_instance.decoder_utility.decoder_automaton )
        for self.decoder_tuple in self.decoder_list:
          self.decoder = self.decoder_tuple[1]
          break
        CallClass(self).call_class(module_name = "DecodeDataProcessor",
                                   class_name = self.decoder_instance.decoder_class_name_key_added, method_name = "execute",
                                   dictionary = self.dictionary, data = self.data, descriptor = self.dataFD)
      except Exception as error:
        raise Exception( error )
      return( self.decoded )
"""
End of File
"""
