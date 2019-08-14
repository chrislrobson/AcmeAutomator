"""
FILE: RichTextProcessor
CLASS: RichTextProcessor
Author: Christopher Robson
Copyright by:  Christopher Robson
Copyright date: 03Oct2017
This software is not FREE!  Use or destribution of the software system and its
subsystem modules, libraries, configuration file and "seed" file without the
express permission of the author is strictly PROHIBITED!
FUNCTION:  Module applies python-docx-template RichText changes to targeted text
"""
"""
LIBRARIES:  Python libraries
"""
from docxtpl import DocxTemplate, RichText
"""
LIBRARIES:  Testbed Tester specific libraries
"""
from Globals import *
"""
CLASS: RichTextProcessor
DESCRIPTION: Converts normal text to python-docx-template RichText format
INPUT: normal plain text within a predefined dictionary structure
OUTPUT: RichText formated text within a predefined dictionary structure
----------------
NOTES on RichText parameters:
"size" = Is muliple of 2, that is if the Word document font is to be
        set at Font:10 then size needs to be 2x10 or 20!
"myScriptStyle" = This sytle format is first defined withon the Word document
                  as a new style with the name "myScriptStyle".  It is this new
                  style parameters that are then inheritted by this class 
"""
class RichTextProcessor:
  "RichText Processor"
  def __init__(self, parent = None):
    self.name = "RichText Processor"
    self.parent = parent
  """"""
  def plain_text_to_richtext_color_format( self, plain_text_dict,
                                           color0 = Globals.BLACK,
                                           color1 = Globals.BLACK,
                                           color2 = Globals.BLACK,
                                           bold0 = False,
                                           bold1 = False,
                                           bold2 = False ):
    self.plain_text_dict = plain_text_dict
    for self.item in self.plain_text_dict.items():
      for self.textlist in self.item:
        if not isinstance( self.textlist, str ):
          self.textlist[0] = RichText( self.textlist[0],
                                       color = color0, size = 20,
                                       style = 'myScriptStyle',
                                       bold = bold0 )
          self.textlist[1] = RichText( self.textlist[1],
                                       color = color1, size = 20,
                                       style = 'myScriptStyle',
                                       bold = bold1 )
          self.textlist[2] = RichText( self.textlist[2],
                                       color = color2, size = 20,
                                       style = 'myScriptStyle',
                                       bold = bold2 )
    return()
  """"""
  def plain_text_to_richtext_format(self, plain_text_dict ):
    self.plain_text_dict = plain_text_dict
    for self.item in self.plain_text_dict.items():
      for self.textlist in self.item:
        if not isinstance( self.textlist, str ):
          self.textlist[0] = RichText( self.textlist[0], size = 20, style = 'myScriptStyle' )
          self.textlist[1] = RichText( self.textlist[1], color = Globals.BLUE, bold = True, size = 20, style = 'myScriptStyle' )
          self.textlist[2] = RichText( self.textlist[2], color = Globals.RED, bold = True, size = 20, style = 'myScriptStyle' )
    return()
  """"""
  def plain_text_to_richtext_unformat(self, plain_text_dict ):
    self.plain_text_dict = plain_text_dict
    for self.item in self.plain_text_dict.items():
      for self.textlist in self.item:
        if not isinstance( self.textlist, str ):
          self.textlist[0] = RichText( self.textlist[0], size = 20, style = 'myScriptStyle' )
    return()
  """"""
  def plain_text_to_richtext_formatted_attributes(self, plain_text_dict, color_selection, font_selection ):
     self.plain_text_dict = plain_text_dict
     for self.item in self.plain_text_dict.items():
       for self.textlist in self.item:
         if not isinstance( self.textlist, str ):
           self.textlist[0] = RichText( self.textlist[0], size = 20, style = 'myScriptStyle' )
           self.textlist[1] = RichText( self.textlist[1], color = Globals.BLUE, bold = True, size = 20, style = 'myScriptStyle' )
           #FIXME REMOVE self.textlist[2] = RichText( self.textlist[2] )
           self.textlist[2] = RichText( self.textlist[2], color = Globals.RED, bold = True, size = 20, style = 'myScriptStyle' )
     return()
"""
END of FILE
"""
