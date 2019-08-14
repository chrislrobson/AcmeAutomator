"""*********************************************************************************************************
Python Qt5 Testbed Tester Unility
MODULE:  Utility
Author: Christopher Robson
Copyright by:  Christopher Robson
Copyright date: 01Jan2016
This software is not FREE!  Use or destribution of the software system and its
subsystem modules, libraries, configuration file and "seed" file without the
express permission of the author is strictly PROHIBITED!
FUNCTION:  Module performs various utility functions such as find prompt or command strings.
HOWTO:
    # This should be called at program startup, for example when the GUI is first initialized
    # so the prompt scanner is ready to process before data is received.
    is_prompt = FindPrompt()
    # This is called by the low level data receiver for each block of data being received.
    prompt_str = is_prompt.find_prompt( received_data, is_prompt.prompt_automaton )
    if prompt_str:
       print( "Yes" )
    else:
       print( "No" )
notes:  When building the strings found, the class "Utility" will return a list of matching string found in
the database LIST.  Its CRITICAL, therefore, to have seed files coded with the prompt keyword as exact as possible.
For example, a given "complete prompt from a device might be as follows:
"tester@devicename>"
CRITICAL There for the seed file "prompt" keyword must be set to that exact string, "tester@devicename"
HOWEVER, notice the seed file's "prompt" keyword maybe better without including the trailing ">" (greater-than)
character.  Nor should the prompt keyword include a trailing "#" (number sign) character.  In this
way, the script can process replies without concern about which subsystem it is within,
(aka configuration mode, etc).  Another words in the seed file prompt keyword has a trailing ">"
character, then any script configuration commands will not be processed correctly. likewise
if the "#" character is the last prompt keyword character when in the command mode.
************************************************************************************************************"""
"""
Python libraries
"""
"""
NOTE: ahocorasick libraries is installed via the PIP "pyahocorasick" archives
"""
import ahocorasick
import re
"""
Local libraries
"""
"""
CLASS: Utility
FUNCTION: Used to find specific strings
INPUT: Block of data to scan for string
OUTPUT: String if found or -1 if not
"""
class Utility:
  "Utility"
  """"""
  def __init__(self, prompt_string_dictionary ):
    self.name = self.__class__.__name__
    self.prompt_keys = prompt_string_dictionary.prompts
    self.prompt_automaton = self.make_prompt_automaton( self.prompt_keys )
  """"""
  def make_prompt_automaton( self, prompt_keys ):
    self.prompt_automaton = ahocorasick.Automaton( )    # initialize
    for ( self.key, self.cat ) in prompt_keys:
      self.prompt_automaton.add_word( self.key, ( self.cat, self.key ))  # add keys and categories
    self.prompt_automaton.make_automaton()             # generate automaton
    return( self.prompt_automaton )
  """"""
  def get_prompt_length( self ):
    return( len( self.prompt_keys ) )
  """"""
  def get_prompt_element( self, index ):
    return( self.prompt_keys[index] )
  """"""
  def find_prompt(self, receive_data, prompt_automaton):
    self.found_last = []
    # todo-debug
    # todo-debug print(repr(receive_data))
    # todo-debug print("{}(receive_data): {}".format(self.name, receive_data))
    # todo-debug
    """
    First do a short scan from the end of the data for the terminating string
    the theory is the prompt is the last word in the data.  However, this
    is not always the case, for example, when a question is returned as the reply
    message.
    """
    self.received_prompt = re.sub( "\n+", " ", receive_data ).strip().split()[-1]
    for self.end_index, (self.action, self.keyw) in prompt_automaton.iter(self.received_prompt):
      self.found_last.append(( self.keyw, self.action))
    """
    When nothing is found, a longer scan must be done starting from the
    beginning of the received data but only done when the last few words done match search data,
    the theory is we try avoiding scanning really huge amounts of data everytime
    """
    if not self.found_last:
      for self.end_index, (self.action, self.keyw) in prompt_automaton.iter(receive_data):
        self.found_last.append((self.keyw, self.action))
    return(self.found_last)
  """
  This method is used when all the received data must be scanned when looking for a
  reply which is probably NOT the last few words in the received buffer.  For example,
  a password error such as "Permission denied" will included the prompt string as the 
  last received data but the program needs to detect the error message prior to the prompt.
  """
  def scan_reply(self, receive_data, prompt_automaton):
    self.found_last = []
    # todo-debug
    # todo-debug print(repr(receive_data))
    # todo-debug print("{}(receive_data): {}".format(self.name, receive_data))
    # todo-debug
    for self.end_index, (self.action, self.keyw) in prompt_automaton.iter(receive_data):
      self.found_last.append((self.keyw, self.action))
    return(self.found_last)
  """"""
  def set_prompt_string( self, key, value ):
    for self.key_found, self.value_found in enumerate( self.prompt_keys ):
      if self.value_found[0] == key:
        self.replace_prompt_string( self.value_found, key, value )
        break
    else:
      self.prompt_keys.append( ( key, value ) )
      self.prompt_automaton = self.make_prompt_automaton( self.prompt_keys )
    return()
  """"""
  def replace_prompt_string( self, key, new_key, value ):
    try:
      self.index = self.prompt_keys.index( key )
      self.prompt_keys.remove( key )
    except ValueError as error:
      pass
    self.prompt_keys.insert( self.index, ( new_key, value) )
    self.prompt_automaton = self.make_prompt_automaton( self.prompt_keys )
    return()
  """"""
  def set_first_last_prompt_string( self, first = None, last = None ):
    if not first or not last:
      self.first = self.prompt_keys[0]
      self.last = self.prompt_keys[-1]
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
      self.prompt_keys.remove( self.first )
      self.prompt_keys.insert( 0, self.first_element )
      self.prompt_keys.remove( self.last )
      self.prompt_keys.append( self.last_element )
    except Exception as error:
      pass
    self.prompt_automaton = self.make_prompt_automaton( self.prompt_keys )
    return ()
  """
  Holds a database of test PASSED or FAILED test result information
  """
  def make_test_results_automaton( self, prompt_keys ):
    test_results_automaton = ahocorasick.Automaton( )    # initialize
    for ( key, cat1, cat2, cat3, cat4, cat5,cat6 ) in prompt_keys:
      test_results_automaton.add_word( key, ( cat6, cat5, cat4, cat3, cat2, cat1, key ) )  # add keys and categories
    test_results_automaton.make_automaton()             # generate automaton
    return( test_results_automaton )
  """"""
  def find_test_results( self, receive_data, prompt_automaton ):
    results_found = []
    try:
      for end_index, ( value6, value5, value4, value3, value2, value1, keyw ) in prompt_automaton.iter( receive_data ):
        results_found.append( ( keyw, value1, value2, value3, value4, value5, value6 ) )
    except:
      pass
    return( results_found )
  """"""
  def set_test_results_string( self, key, value1, value2, value3, value4, value5, value6 ):
    for self.key_found, self.value_found in enumerate( self.prompt_keys ):
      if self.value_found[0] == key:
        self.replace_test_results_string( self.value_found, key, value1, value2, value3, value4, value5, value6 )
        break
    else:
      self.prompt_keys.append( ( key, value1, value2, value3, value4, value5, value6 ) )
      self.prompt_automaton = self.make_test_results_automaton( self.prompt_keys )
    return()
  """"""
  def replace_test_results_string( self, key, new_key, value1, value2, value3, value4, value5, value6 ):
    try:
      self.index = self.prompt_keys.index( key )
      self.prompt_keys.remove( key )
    except ValueError as error:
      pass
    self.prompt_keys.insert( self.index, ( new_key, value1, value2, value3, value4, value5, value6 ) )
    self.prompt_automaton = self.make_test_results_automaton( self.prompt_keys )
    return ()
"""
END OF FILE
"""

