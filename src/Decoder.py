"""*******************************************************************************************************
Received Decoder
MODULE:  Decoder
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
CLASS Decoder
DESCRIPTION: Decodes data into format acceptable for the analysis class
INPUT: Network device output data
OUTPUT: Class output data based on class called
"""
class Decoder:
    "Decoder"
    """"""
    def __init__( self, parent = None ):
        self.name = self.__class__.__name__
        self.parent = parent
    """"""
    def decode(self, dictionary = None, decoder_instance = None, descriptor = None, data = "", index = None):
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
            try:
                self.decoder_instance.decoder_class_name, self.decoder_instance.decoder_class = \
                    self.decoder_instance.decoder_utility.find_decoder(self.data_string_to_convert_to_class,
                                                        self.decoder_instance.decoder_utility.decoder_automation )
            except Exception as error:
                self.message = "{{{}Decoder: Invalid class: {}, Receive data:{} ERROR: {}{}}}".format(Globals.RED_MESSAGE,
                                                                                          self.data.split()[0],
                                                                                          self.data_string_to_convert_to_class,
                                                                                          error, Globals.SPAN_END_MESSAGE)
                self.dictionary['loggerwidget'].emit(self.message)
                raise Exception
            if self.decoder_instance.decoder_class_name[-1] == ":":
                self.decoder_instance.decoder_class_name_key_added = " ".join( self.decoder_instance.decoder_class_name.lower().split() )[:-1]
            else:
                self.decoder_instance.decoder_class_name_key_added = " ".join(self.decoder_instance.decoder_class_name.lower().split())
            CallClass(self).call_class(module_name = "DecodeDataProcessor",
                                       class_name = self.decoder_instance.decoder_class, method_name = "execute",
                                       dictionary = self.dictionary, data = self.data, descriptor = self.dataFD)
        except Exception as error:
            if error.args:
                self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, "Decoder:", error, Globals.SPAN_END_MESSAGE)
                self.dictionary['loggerwidget'].emit(self.message)
            raise Exception
        return()
"""**************************************************************************************************
End of File
**************************************************************************************************"""
