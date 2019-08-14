####################################################################################################################
"""
Testbed Tester DecoderUtility
MODULE:  DecoderUtility
Author: Christopher Robson
Copyright by:  Christopher Robson
Copyright date: 01Jan2016
This software is not FREE!  Use or destribution of the software system and its
subsystem modules, libraries, configuration file and "seed" file without the
express permission of the author is strictly PROHIBITED!
FUNCTION:  Module determines the decoder to use which is derived from the input string.
FIXME !!!!!!!!!!!!!!!!!!!!!!!!!!!!
Needs to be combined with Utility whihc finds prompt but both class basically do same thing !!!
FIXME !!!!!!!!!!!!!!!!!!!!!!!!!!!
"""
"""
Python libraries
"""
import ahocorasick
"""
CLASS: DecoderUtility
DESCRIPTION: Deterrmines the class to use for decoding device output data
INPUT: Devie output data
OUTPUT: Class to call which will process device output data
"""
class DecoderUtility:
  "Decoder Utility"
  """"""
  def __init__(self, decoder_string_dictionary ):
    self.name = "Decoder Utility"
    self.decoder_keys = decoder_string_dictionary.decoders
    self.decoder_automaton = self.make_decoder_automaton( self.decoder_keys )
  """"""
  def make_decoder_automaton( self, decoder_keys ):
    self.decoder_keys = decoder_keys
    self.decoder_automaton = ahocorasick.Automaton( )    # initialize
    for (self.key, self.cat) in self.decoder_keys:
      self.decoder_automaton.add_word(self.key, (self.cat, self.key))  # add keys and categories
    self.decoder_automaton.make_automaton()             # generate automaton
    return( self.decoder_automaton )
  """"""
  def get_decoder_length( self ):
    return( len( self.decoder_keys ) )
  """"""
  def get_decoder_element( self, index ):
    return( self.decoder_keys[index] )
  """"""
  def find_decoder( self, receive_data, decoder_automaton ):
    self.receive_data = receive_data
    self.decoder_automaton = decoder_automaton
    self.found_last = []
    for end_index, ( self.action, self.keyw ) in self.decoder_automaton.iter( self.receive_data ):
      self.found_last.append( ( self.keyw, self.action ) )
    return( self.found_last )
  """"""
  def set_decoder_string( self, key, value ):
    self.key = key
    self.value = value
    for self.key_found, self.value_found in enumerate( self.decoder_keys ):
      if self.value_found[0] == self.key:
        self.replace_decoder_string( self.value_found, self.key, self.value )
        break
    else:
      self.decoder_keys.append( ( self.key, self.value ) )
      self.decoder_automaton = self.make_decoder_automaton( self.decoder_keys )
    return()
  """"""
  def replace_decoder_string( self, key, new_key, value ):
    self.new_key = new_key
    self.key = key
    self.value = value
    try:
      self.index = self.decoder_keys.index( self.key )
      self.decoder_keys.remove( self.key )
    except ValueError as error:
      pass
    self.decoder_keys.insert( self.index, ( self.new_key, self.value) )
    self.decoder_automaton = self.make_decoder_automaton( self.decoder_keys )
    return()
  """"""
  def set_first_last_decoder_string( self, first = None, last = None ):
    if not first or not last:
      self.first = self.decoder_keys[0]
      self.last = self.decoder_keys[-1]
      self.first_element = list( self.first )
      self.last_element = list( self.last )
    else:
      self.first = first
      self.last = last
      self.first_element = list( self.first )
      self.last_element = list( self.last )
    """"""
    self.first_element[1] = "STARTANALYSIS"
    self.last_element[1] = "STOPANALYSIS"
    try:
      self.decoder_keys.remove( self.first )
      self.decoder_keys.insert( 0, self.first_element )
      self.decoder_keys.remove( self.last )
      self.decoder_keys.append( self.last_element )
    except Exception as error:
      pass
    self.decoder_automaton = self.make_decoder_automaton( self.decoder_keys )
    return ()
  """
  TEST RESULTS AUTOMATION
  """
  def make_test_results_automaton( self, decoder_keys ):
    self.decoder_keys = decoder_keys
    test_results_automaton = ahocorasick.Automaton( )    # initialize
    for ( key, cat1, cat2, cat3, cat4, cat5,cat6 ) in self.decoder_keys:
      test_results_automaton.add_word( key, ( cat6, cat5, cat4, cat3, cat2, cat1, key ) )  # add keys and categories
    test_results_automaton.make_automaton()             # generate automaton
    return( test_results_automaton )
  """"""
  def find_test_results( self, receive_data, decoder_automaton ):
    results_found = []
    try:
      for end_index, ( value6, value5, value4, value3, value2, value1, keyw ) in decoder_automaton.iter( receive_data ):
        results_found.append( ( keyw, value1, value2, value3, value4, value5, value6 ) )
    except:
      pass
    return( results_found )
  """"""
  def set_test_results_string( self, key, value1, value2, value3, value4, value5, value6 ):
    for self.key_found, self.value_found in enumerate( self.decoder_keys ):
      if self.value_found[0] == key:
        self.replace_test_results_string( self.value_found, key, value1, value2, value3, value4, value5, value6 )
        break
    else:
      self.decoder_keys.append( ( key, value1, value2, value3, value4, value5, value6 ) )
      self.decoder_automaton = self.make_test_results_automaton( self.decoder_keys )
    return()
  """"""
  def replace_test_results_string( self, key, new_key, value1, value2, value3, value4, value5, value6 ):
    try:
      self.index = self.decoder_keys.index( key )
      self.decoder_keys.remove( key )
    except ValueError as error:
      pass
    self.decoder_keys.insert( self.index, ( new_key, value1, value2, value3, value4, value5, value6 ) )
    self.decoder_automaton = self.make_test_results_automaton( self.decoder_keys )
    return ()
####################################################################################################################

