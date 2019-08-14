####################################################################################################################
"""
FILE: ReportGenerator
CLASS: ReportGenerator
Author: Christopher Robson
Copyright by:  Christopher Robson
Copyright date: 03Oct2017
This software is not FREE!  Use or destribution of the software system and its
subsystem modules, libraries, configuration file and "seed" file without the
express permission of the author is strictly PROHIBITED!
FUNCTION:  Module creates the testcase report document.
"""
"""
LIBRARIES:  Python libraries
"""
from docxtpl import DocxTemplate, RichText
import datetime
import os
"""
LIBRARIES:  Testbed Tester specific libraries
"""
from Globals import *
from Exceptions import *
from SeedDictionary import SeedCommandDictionaryProcessor, \
  SeedCommandlinePreprocessor
"""
CLASS: TestcaseReportGenerator
DESCRIPTION: Takes the testcase data to builds a test report 
INPUT: "show" captured data 
OUTPUT: Testcase Report
"""
class ReportGenerator:
  "Report Generator"
  def __init__(self, parent = None):
    self.name = "Report Generator"
    self.parent = parent
    #self.filename_time_extension = parent.parent.filename_time_extension
    self.filename_time_extension = datetime.datetime.now().strftime( "-%d%b%Y-%H%M-%S" )
    self.template_filename = "Testcase-Physical-Interface-Template-Version-1.docx"
    """
    Initialize a test set of report data used if no real data is passed.
    """
    self.testcase_report ="{}{}".format( "~/myARCHIVES/profiles/REPORT-TEMPLATES/",
                                           self.template_filename )
    self.report_filename = "{}{}{}".format( "~/myARCHIVES/REPORTS/"
                                                "Testcase-Report-EXAMPLE",
                                                self.filename_time_extension,
                                                ".docx" )
    self.testcase_init = {
      'testcase_number':RichText( "1.1.1",
                           style = 'myScriptTestcase' ),
      'testcase_title':RichText( "Title of the testcase",
                                 style = 'myScriptTestcase'),
      'description_label':RichText( 'Description:',
                                    style = 'myScriptLabel'),
      'description_data':RichText( "Description of the testcase",
                                   style = 'myScriptStyle'),
      'procedure_label':RichText( "Procedure:",
                                  style = 'myScriptLabel' ),
      'configuration_data_title':RichText( "Title for configuration commands used for testcase",
                                           style = 'myScriptStyle' ),
      'configuration_data':RichText( "List of configuration commands used for testcase",
                                     style = 'myScriptStyle' ),
      'procedure_data_title': RichText( "Title for procedures taken in a testcase",
                                        style = 'myScriptStyle' ),
      'procedure_data':RichText( "Procedure steps taken in a testcase",
                                 style = 'myScriptStyle' ),
      'passfail_criteria_label':RichText('Pass/Fail Criteria:',
                                         style = 'myScriptLabel' ),
      'passfail_criteria_data':RichText( "Description of what is a Pass or Fail of the testcase",
                                         style = 'myScriptStyle' ),
      'result_label':RichText( 'Results:',
                               style = 'myScriptLabel'),
      'result_data':RichText( "PASSED/FAILED".upper(), color = "darkBlue", bold = True,
                              style = 'myScriptStatusStyle'),
      'status_label':RichText( 'Status:',
                               style = 'myScriptLabel'),
      'status_data':RichText( "Status of the testcase".upper(), color = "darkBlue", bold = True,
                              style = 'myScriptStatusStyle'),
      'analysis_label':RichText( 'Analysis:',
                                 style = 'myScriptLabel'),
      'analysis_data':RichText( "Analysis of the report data from the testcase",
                                style = 'myScriptStyle'),
      'detailed_results_label':RichText( 'Results:',
                                        style='myScriptLabel'),
      'detailed_results_data': RichText( "Report data from the testcase",
                                         style = 'myScriptStyle')
    }
  """
  METHOD: testcase_report_generator
  FUNCTION: Creates the test report
  INPUT: Dictionary key:value pairs of testcase data
         and test report file template and report filename
  OUTPUT: Test report
  """
  def report_generator( self, testcase = None ):
    self.testcase = testcase
    if not self.testcase:
      """
      Convert relative file path to actual
      """
      if self.testcase_report.startswith( "~" ):
        try:
          self.testcase_report = os.path.expanduser( '~' ) + self.testcase_report.split( "~" )[1]
        except Exception as error:
          raise Exception( "REPORTGENERATOR: {}".format( error ) )
      if self.report_filename.startswith( "~" ):
        try:
          self.report_filename = os.path.expanduser( '~' ) + self.report_filename.split( "~" )[1]
        except Exception as error:
          raise Exception( "REPORTGENERATOR: {}".format( error ) )
      self.context = self.testcase_init
      # FIXME
      # FIXME DEBUG CODE
      #  for k,v in self.context.items():
      #    print( "K: {} - V: {}".format(k,v) )
      """
      Create the Microsoft Word document template to populate with DEBUG test data
      """
      try:
        self.testcase_report = DocxTemplate( self.testcase_report )
      except Exception as error:
        raise Exception( "REPORTGENERATOR: {}".format( error ) )
    else:
      """
      Use the Testcase data passed to the Testcase Report Generator.
      Data is passed as dictionary key:value pairs.
      """
      try:
        self.report_filename_str = self.testcase["reportfilename"].split( "." )[0]
        self.report_filename_suffix = self.testcase["reportfilename"].split( "." )[1]
        self.report_filename = "{}{}{}".format( self.report_filename_str,
                                                self.filename_time_extension,
                                                self.report_filename_suffix )
      except:
        self.report_filename = "{}{}{}.doc".format( self.report_filename_str,
                                                    self.filename_time_extension,
                                                    self.report_filename_suffix )
      """
      Convert relative file path to actual
      """
      if self.testcase_report.startswith( "~" ):
        try:
            self.testcase_report = os.path.expanduser( '~' ) + self.testcase_report.split( "~" )[1]
        except Exception as error:
          raise Exception( "REPORTGENERATOR: {}".format( error ) )
      if self.report_filename.startswith( "~" ):
        try:
          self.report_filename = os.path.expanduser( '~' ) + self.report_filename.split( "~" )[1]
        except Exception as error:
          raise Exception( "REPORTGENERATOR: {}".format( error ) )
      """
      Create the Microsoft Word document template to populate with actual test data
      """
      try:
        self.testcase_report = DocxTemplate( self.testcase["templatefilename"] )
      except Exception as error:
        raise Exception( "REPORTGENERATOR: {}".format( error ) )
      self.context = {
          'testcase':RichText( self.testcase["testcase"],
                               style = 'myScriptTestcase' ),
          'testcase_description':RichText( self.testcase["testcasetitle"],
                                           style = 'myScriptTestcase'),
          'description_label':RichText( 'Description:',
                                        style = 'myScriptLabel'),
          'description_data':RichText( self.testcase["descriptiondata"],
                                       style = 'myScriptStyle'),
          'procedure_label':RichText( "Procedure:",
                                      style = 'myScriptLabel' ),
          'configuration_title_data':RichText( self.testcase["configurationtitle"],
                                               style = 'myScriptStyle' ),
          'configuration_data':RichText( self.testcase["configurationdata"],
                                         style = 'myScriptStyle' ),
          'procedure_title_data': RichText( self.testcase["proceduretitle"],
                                            style = 'myScriptStyle' ),
          'procedure_data':RichText( self.testcase["proceduredata"],
                                     style = 'myScriptStyle' ),
          'passfail_criteria_label':RichText('Pass/Fail Criteria:',
                                              style = 'myScriptLabel' ),
          'passfail_criteria_data':RichText( self.testcase["criteriadata"],
                                             style = 'myScriptStyle' ),
          'result_label':RichText( 'Results:',
                                   style = 'myScriptLabel'),
          'passfail_data':RichText( self.testcase["resultsdata"].upper(), bold = True,
                                    style = 'myScriptStatusStyle'),
          'status_label':RichText( 'Status:',
                                   style = 'myScriptLabel'),
          'status_data':RichText( self.testcase["statusdata"].upper(), bold = True,
                                  style = 'myScriptStatusStyle'),
          'analysis_label':RichText( 'Analysis:',
                                     style = 'myScriptLabel'),
          'analysis_data':RichText( self.testcase["analysisdata"],
                                    style = 'myScriptStyle'),
          'detailedresults_label':RichText( 'Results:',
                                            style='myScriptLabel'),
          'detailedresults_data': RichText( self.testcase["detailedresultsdata"],
                                            style = 'myScriptStyle')
      }
    """
    Process the tescase data, building the test report Word document
    """
    try:
      self.testcase_report.render( self.context )
    except Exception as error:
      raise Exception( "REPORTGENERATOR: {}".format( error ) )
    try:
      self.testcase_report.save( self.report_filename )
    except Exception as error:
      raise Exception( "REPORTGENERATOR: {}".format( error ) )
    return()
""""""
# FIXME Debug ONLY
if __name__ == "__main__":
  try:
    main = ReportGenerator().report_generator()
  except Exception as error:
    print(error)
  print("DONE")
####################################################################################################################

