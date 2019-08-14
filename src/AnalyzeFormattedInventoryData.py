"""************************************************************************************
CLASS: AnalyzeFormattedInventoryData
Author: Christopher Robson
Copyright by:  Christopher Robson
Copyright date: 01Nov2017
This software is not FREE!  Use or destribution of the software system and its
subsystem modules, libraries, configuration file and "seed" file without the
express permission of the author is strictly PROHIBITED!
FUNCTION:  Module analysizing inventory data collected into XML formatted file.
***********************************************************************************"""
"""
LIBRARIES:  Python libraries
"""
import datetime
import ast
"""
LIBRARIES:  Home grown specific libraries
"""
from Globals import *
"""
CLASS: AnalyzeFormattedInventoryData:
DESCRIPTION: Analysis show chassis hardware data 
INPUT: "show chassis hardware detailed | display xml" captured data
OUTPUT: File containing data ready for Excel report generator
"""
class AnalyzeFormattedInventoryData:
  "Analyze Formatted Inventory Data"
  """"""
  def __init__(self, parent = None):
    self.parent = parent
    self.name = self.__class__.__name__
    self.search_item_sheet_row = 1
    self.search_item_sheet_column = 1
    self.item_row_no = 1
    self.item_column_no = 1
    self.ToC_initialized = 0
    """
    Maintain a list of inventory analyzsis data filenames:
    This allows the seed file to hold multiple data file.
    Field format:
    element 1:  testcase number
    element 2:  search template
    element 3:  inventory data
    """
    self.testcase_number_element    = 0
    self.testcase_title_element     = 1
    self.inventory_search_data      = 2
    self.inventory_data             = 3
    self.analyze_seed_file_list = []
  """
   CLASS: execute:
   DESCRIPTION: Create "show chassis hardware detail" inventory analysis data entry point.
                Determines input data to process and passes this data onto processing methods.
   INPUT: "show chassis" captured data
   OUTPUT: data ready for generating report data
   """
  def execute( self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dictionary = dictionary
    self.table_of_content_list = []
    """
    Process inventory data now
    """
    if self.dictionary["verbose"] == 'Yes':
      self.message = "{} started at: {}.".format(self.name, datetime.datetime.now().strftime("%d%b%Y-%H%M-%S"))
      self.dictionary['loggerwidget'].emit(self.message)
    self.message = "Building Inventory Analysis Report Data: {}{}.".format(self.dictionary["savepath"], self.dictionary["filename"])
    self.dictionary['loggerwidget'].emit(self.message)
    """
    Get the file where the analyze data is saved
    """
    try:
      self.analsis_data_filename = "{}{}{}{}".format(self.dictionary["relativepath"], self.dictionary["savepath"], self.dictionary["filename"], self.dictionary["datetime"])
    except Exception as error:
      self.message = "{{{}{}: {} {}{}}}".format(Globals.RED_MESSAGE, self.name, error, self.analyze_seed_filename, Globals.SPAN_END_MESSAGE)
      self.dictionary['loggerwidget'].emit(self.message)
      raise Exception
    """
    Get the file that contains testcase info such as search seed data, collect data and testcase numbers
    """
    self.analyze_seed_filename = "{}{}{}".format(self.dictionary["relativepath"], self.dictionary["commandpath"], self.dictionary["commands"])
    """
    Extract the name of the data filenames and open up the files for processing
    """
    try:
      with open( self.analyze_seed_filename, "r" ) as self.seedFD:
        for self.seed_element in self.seedFD:
          if self.seed_element.startswith( "#" ):
            continue
          try:
            self.seed_dict = ast.literal_eval( self.seed_element.split( ";" )[0] )
          except Exception as error:
            self.seedFD.close()
            self.message = "{{{}{}: {} {}{}}}".format(Globals.RED_MESSAGE, self.name, error, self.analyze_seed_filename, Globals.SPAN_END_MESSAGE)
            self.dictionary['loggerwidget'].emit(self.message)
            raise Exception
          """
          Build list of paired data files and associated state information
          such as testcase number and a place holder for testcase pass/fail results
          """
          try:
            self.analyze_seed_file_list.append( (
                                                "{}".format( self.seed_dict["testcase"] ),
                                                "{}".format( self.seed_dict["testcasetitle"] ),
                                                "{}{}{}".format( self.dictionary['relativepath'],
                                                                 self.seed_dict["inventorysearchseedpath"],
                                                                 self.seed_dict["inventorysearchdata"]),
                                                "{}{}{}".format( self.dictionary['relativepath'],
                                                                 self.seed_dict["inventorydatapath"],
                                                                 self.seed_dict["inventorydata"] +
                                                                 self.dictionary['datetime']
                                                               ),
                                                []
                                               )
                                             )
          except Exception as error:
            self.seedFD.close()
            self.message = "{{{}{}: {} -- List file error{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
            self.dictionary['loggerwidget'].emit(self.message)
            raise Exception
    except Exception as error:
      self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
      self.dictionary['loggerwidget'].emit(self.message)
      raise Exception
    """
    Process the inventory data
    """
    self.analysis_data_file(self.analyze_seed_file_list, self.analsis_data_filename)
    return ()
  """
  METHOD: analysis_data_file( self ):
  DESCRIPTION: Create "show interface detail" Analysis data
  INPUT: "show interface detail" captured data
  OUTPUT: Analysis data ready for report generation
  """
  def analysis_data_file(self, analyze_seed_file_list, analsis_data_filename):
    self.analsis_data_filename = analsis_data_filename
    self.analyze_seed_file_list = analyze_seed_file_list
    self.filename = ""
    try:
      self.analysis_fd = open(self.analsis_data_filename, 'a')
    except Exception as error:
      self.message = "{{{}{}: {} - {}{}}}".format(Globals.RED_MESSAGE, self.name, error, self.analsis_data_filename, Globals.SPAN_END_MESSAGE)
      self.dictionary['loggerwidget'].emit(self.message)
    """
    Sequence through each testcase for this device
    primarly to remove leading spaces and associate assign testcase number, title and search criteria to the collected data.
    This information is used later for the Excel Table of Contents (search data) and sheet titles.
    """
    for self.analyze_element in self.analyze_seed_file_list:
      self.analysis_fd.write("<testcasenumber {}>\n".format(self.analyze_element[self.testcase_number_element]))
      self.analysis_fd.write("<testcasetitle>{}</testcasetitle>\n".format(self.analyze_element[self.testcase_title_element]))
      self.analysis_fd.write("<searchseedfile>{}</searchseedfile>\n".format(self.analyze_element[self.inventory_search_data]))
      try:
        with open(self.analyze_element[self.inventory_data], 'r' ) as self.xml_file_FD:
          self.received_data = self.xml_file_FD.read()
          self.xml_file_FD.close()
          self.split_received_data = self.received_data.split( "\n" )
          self.stripped_spaces_data = ""
          for self.i in range( len( self.split_received_data ) ):
            if self.split_received_data[self.i].startswith( "<rpc-reply" ):
              self.stripped_spaces_data = "\n".join( self.received_data.split( "\n" )[self.i:] )
              break
          if not self.stripped_spaces_data:
            self.message = "{{{}{}: Skipping {}, not an XML file{}}}".format(Globals.BLUE_MESSAGE, self.name, self.analyze_element[self.inventory_data], Globals.SPAN_END_MESSAGE)
            self.dictionary['loggerwidget'].emit(self.message)
            continue
          else:
            self.stripped_trailing_data = self.stripped_spaces_data.split( "</rpc-reply>" )
            self.clean_data =  self.stripped_trailing_data[0]  + "</rpc-reply>"
            for self.line in self.clean_data.split( "\n" ):
              self.new_line = self.line.lstrip( " " )
              if self.new_line.startswith( "\n" ):
                continue
              else:
                self.analysis_fd.write("{}\n".format(self.new_line))
      except Exception as error:
        self.message = "{{{}{}: {} {}{}}}".format(Globals.RED_MESSAGE, self.name, error, self.analyze_seed_filename, Globals.SPAN_END_MESSAGE)
        self.dictionary['loggerwidget'].emit(self.message)
        raise Exception
      """
      Close out this testcase's XML block of data
      """
      self.analysis_fd.write("</testcasenumber>\n")
    """"""
    self.analysis_fd.close()
    return()
"""
End of File
"""

