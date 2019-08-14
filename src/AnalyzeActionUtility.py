"""
Testbed Tester AnalyzeActionUtility
MODULE:  AnalyzeActionUtility
Author: Christopher Robson
Copyright by:  Christopher Robson
Copyright date: 01Jan2016
This software is not FREE!  Use or destribution of the software system and its
subsystem modules, libraries, configuration file and "seed" file without the
express permission of the author is strictly PROHIBITED!
FUNCTION:  Module determines the analyze_action to use which is derived from the input string.
FIXME !!!!!!!!!!!!!!!!!!!!!!!!!!!!
Needs to be combined with Utility whihc finds prompt but both class basically do same thing !!!
FIXME !!!!!!!!!!!!!!!!!!!!!!!!!!!
"""
"""
Python libraries
"""
import ahocorasick
"""
CLASS: AnalyzeActionUtility
DESCRIPTION: Deterrmines the class to use for decoding device output data
INPUT: Devie output data
OUTPUT: Class to call which will process device output data
"""
class AnalyzeActionUtility:
  "Analyze Action Utility"
  """"""
  def __init__(self, analyze_action_string_dictionary ):
    self.name = self.__class__.__name__
    self.analyze_action_keys = analyze_action_string_dictionary.analyze_actions
    self.analyze_action_automaton = self.make_analyze_action_automaton( self.analyze_action_keys )
  """"""
  def make_analyze_action_automaton( self, analyze_action_keys ):
    self.analyze_action_keys = analyze_action_keys
    self.analyze_action_automaton = ahocorasick.Automaton( )    # initialize
    for (self.key, self.cat) in self.analyze_action_keys:
      self.analyze_action_automaton.add_word(self.key, (self.cat, self.key))  # add keys and categories
    self.analyze_action_automaton.make_automaton()             # generate automaton
    return( self.analyze_action_automaton )
  """"""
  def get_analyze_action_length( self ):
    return( len( self.analyze_action_keys ) )
  """"""
  def get_analyze_action_element( self, index ):
    return( self.analyze_action_keys[index] )
  """"""
  def find_analyze_action( self, action, analyze_action_automaton ):
    self.action_len = len( action )
    self.action = action
    self.analyze_action_automaton = analyze_action_automaton
    self.found_last = []
    for end_index, ( self.action, self.keyw ) in self.analyze_action_automaton.iter( self.action ):
      if self.action_len == len( self.keyw ):
        self.found_last.append( ( self.keyw, self.action ) )
    return( self.found_last )
  """"""
  def set_analyze_action_string( self, key, value ):
    self.key = key
    self.value = value
    for self.key_found, self.value_found in enumerate( self.analyze_action_keys ):
      if self.value_found[0] == self.key:
        self.replace_analyze_action_string( self.value_found, self.key, self.value )
        break
    else:
      self.analyze_action_keys.append( ( self.key, self.value ) )
      self.analyze_action_automaton = self.make_analyze_action_automaton( self.analyze_action_keys )
    return()
  """"""
  def replace_analyze_action_string( self, key, new_key, value ):
    self.new_key = new_key
    self.key = key
    self.value = value
    try:
      self.index = self.analyze_action_keys.index( self.key )
      self.analyze_action_keys.remove( self.key )
    except ValueError as error:
      pass
    self.analyze_action_keys.insert( self.index, ( self.new_key, self.value) )
    self.analyze_action_automaton = self.make_analyze_action_automaton( self.analyze_action_keys )
    return()
  """"""
  def set_first_last_analyze_action_string( self, first = None, last = None ):
    if not first or not last:
      self.first = self.analyze_action_keys[0]
      self.last = self.analyze_action_keys[-1]
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
      self.analyze_action_keys.remove( self.first )
      self.analyze_action_keys.insert( 0, self.first_element )
      self.analyze_action_keys.remove( self.last )
      self.analyze_action_keys.append( self.last_element )
    except Exception as error:
      pass
    self.analyze_action_automaton = self.make_analyze_action_automaton( self.analyze_action_keys )
    return ()
  """
  TEST RESULTS AUTOMATION
  """
  def make_test_results_automaton( self, analyze_action_keys ):
    self.analyze_action_keys = analyze_action_keys
    test_results_automaton = ahocorasick.Automaton( )    # initialize
    for ( key, cat1, cat2, cat3, cat4, cat5,cat6 ) in self.analyze_action_keys:
      test_results_automaton.add_word( key, ( cat6, cat5, cat4, cat3, cat2, cat1, key ) )  # add keys and categories
    test_results_automaton.make_automaton()             # generate automaton
    return( test_results_automaton )
  """"""
  def find_test_results( self, action, analyze_action_automaton ):
    results_found = []
    try:
      for end_index, ( value6, value5, value4, value3, value2, value1, keyw ) in analyze_action_automaton.iter( action ):
        results_found.append( ( keyw, value1, value2, value3, value4, value5, value6 ) )
    except:
      pass
    return( results_found )
  """"""
  def set_test_results_string( self, key, value1, value2, value3, value4, value5, value6 ):
    for self.key_found, self.value_found in enumerate( self.analyze_action_keys ):
      if self.value_found[0] == key:
        self.replace_test_results_string( self.value_found, key, value1, value2, value3, value4, value5, value6 )
        break
    else:
      self.analyze_action_keys.append( ( key, value1, value2, value3, value4, value5, value6 ) )
      self.analyze_action_automaton = self.make_test_results_automaton( self.analyze_action_keys )
    return()
  """"""
  def replace_test_results_string( self, key, new_key, value1, value2, value3, value4, value5, value6 ):
    try:
      self.index = self.analyze_action_keys.index( key )
      self.analyze_action_keys.remove( key )
    except ValueError as error:
      pass
    self.analyze_action_keys.insert( self.index, ( new_key, value1, value2, value3, value4, value5, value6 ) )
    self.analyze_action_automaton = self.make_test_results_automaton( self.analyze_action_keys )
    return ()
"""
END of FILE
"""

