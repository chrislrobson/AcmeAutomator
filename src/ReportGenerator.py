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
    self.template = "{}{}".\
      format( self.parent.seed_list[AnalysisSeedCommandDictionaryProcessor.seedpath],
              self.parent.parent.report_template )
    self.report_filename = \
      "{}.docx".format( self.parent.cmd_list[AnalysisSeedCommandDictionaryProcessor.analysisreportfilename] )
  """
  METHOD: testcase_report_generator
  FUNCTION: Creates the test report
  INPUT: Dictionary key:value pairs of testcase data
         and test report file template and report filename
  OUTPUT: Test report
  """
  def report_generator( self, testcase ):
    self.testcase = testcase
    try:
      self.testcase_report = DocxTemplate( self.template )
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
        'results_data':RichText( self.testcase["resultsdata"].upper(), bold = True, color = "darkBlue",
                                  style = 'myScriptStatusStyle'),
        'status_label':RichText( 'Status:',
                                 style = 'myScriptLabel'),
        'status_data':RichText( self.testcase["statusdata"].upper(), bold = True, color = "darkBlue",
                                style = 'myScriptStatusStyle'),
        'analysis_label':RichText( 'Analysis:',
                                   style = 'myScriptLabel'),
        'analysis_data':self.testcase["analysisdata"],
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
  """
  Prepares report file fields for final report then generates the report
  """
  def generate_report( self, pass_fail, testcase, reportFD, character_count ):
    self.testcase = testcase
    self.reportFD = reportFD
    self.reportFD.seek( character_count )
    for self.report_data in self.reportFD:
      self.testcase["detailedresultsdata"] += self.report_data
    self.testcase["statusdata"] = "COMPLETED"
    if pass_fail == "Failed":
      self.testcase["resultsdata"] = "FAILED"
      self.message_str = "Testcase FAILED!"
    else:
      self.testcase["resultsdata"] = "PASSED"
      self.message_str = "Testcase PASSED."
    ReportGenerator(self).report_generator( self.testcase )
    self.parent.ggparent.processor_message_signal.emit(self.message_str)
    return ()
"""
END of FILE
"""

