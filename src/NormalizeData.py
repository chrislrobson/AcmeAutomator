"""
Testbed Tester Normalize Data
MODULE:  NormalizeData
Author: Christopher Robson
Copyright by:  Christopher Robson
Copyright date: 01Jan2016
This software is not FREE!  Use or destribution of the software system and its
subsystem modules, libraries, configuration file and "seed" file without the
express permission of the author is strictly PROHIBITED!
FUNCTION:  This class strips transmitted data of special charactesr such a tabs and CRs.
"""
import re
"""
CLASS: NormalizeData
DESCRIPTION: Strips control characters from received data 
INPUT: receive data
OUTPUT: received data void of control characters such as \r
"""
class NormalizeData():
  "Normalize Data"
  """"""
  def __init__(self, parent = None):
    self.name = self.__class__.__name__
    self.parent = parent
  """"""
  def normalize_data(self, dictionary = None, data = None):
    self.dictionary = dictionary
    self.data = data
    return ( self.normalize_ctlH( self.normalize_linefeeds(self.data)))
  """"""
  def normalize_linefeeds( self, data ):
    try:
      newline = re.compile( r'(\r\r\r\n|\r\r\n|\r\n\r|\r\n|\n\r)' )
    except Exception as error:
      raise
    return (newline.sub( '\n', data ))
  """"""
  def normalize_ctlH( self, data ):
    return (data.replace( "\x08", " " ))
  """"""
  def strip_prompt(self, dictionary = None, data = None ):
    self.data = data
    self.dictionary = dictionary
    self.data_list = data.split( "\n" )
    self.prompt_str = self.data_list[-1]
    self.reply_action = self.dictionary['processreply'].find_prompt( self.prompt_str, self.dictionary['processreply'].prompt_automation )
    if self.reply_action:
      self.data = ""
      for self.item in self.data_list[:-1]:
       self.data += self.item + "\n"
    return( self.data )
"""
End of File
"""
