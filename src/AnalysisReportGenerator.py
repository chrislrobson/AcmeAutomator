"""
FILE: AnalysisReportGenerator
CLASS: AnalysisReportGenerator
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
"""
CLASS: TestcaseAnalysisReportGenerator
DESCRIPTION: Takes the testcase data to builds a test report 
INPUT: "show" captured data 
OUTPUT: Testcase AnalysisReport
"""
class AnalysisReportGenerator:
  "Analysis Report Generator"
  def __init__(self, parent = None):
    self.name = self.__class__.__name__
    self.parent = parent
    self.testcase_dictionary = {
                                 "testcase": None,
                                 "testcasetitle": None,
                                 "descriptiondata": None,
                                 "configurationtitle": None,
                                 "configurationdata": None,
                                 "configurationfiles": [],
                                 "proceduretitle": None,
                                 "proceduredata": [],
                                 "procedurefiles": [],
                                 "criteriadata": None,
                                 "resultsdata": None,
                                 "statusdata": None,
                                 "analysisdata": [],
                                 "detailedresultscomments": None,
                                 "detailedresultsdata": [],
                                 "detailedresultsfiles": [],
                                 "reportfilename": None,
                                 "expecteddatafilename": None,
                                 "receiveddatafilename": None,
                                 "reporttemplate": None
                               }
  """
  METHOD: get_testcase
  FUNCTION: Returns the testcase database
  INPUT: None
  OUTPUT: testcase dictionary
  """
  def get_testase_dictionary(self):
    return(self.testcase_dictionary)
  """
  METHOD: testcase_report_generator
  FUNCTION: Creates the test report
  INPUT: Dictionary key:value pairs of testcase data and test report file template and report filename
  OUTPUT: Test report
  """
  def analysis_report_generator(self, testcase = None, dictionary = None):
    self.testcase = testcase
    self.dictionary = dictionary
    try:
      self.testcase_report = DocxTemplate(self.testcase['reporttemplate'])
    except Exception as error:
      self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
      self.dictionary['loggerwidget'].emit(self.message)
      raise Exception
    self.analysis_context = {
        'testcase_data':RichText(self.testcase["testcase"], style = 'myScriptTestcase'),
        'testcasetitle_data':RichText(self.testcase["testcasetitle"], style = 'myScriptTestcase'),
        'description_label':RichText('Description:', style = 'myScriptLabel'),
        'description_data':RichText(self.testcase["descriptiondata"], style = 'myScriptStyle'),
        'procedure_label':RichText("Procedure:", style = 'myScriptLabel'),
        'configuration_title_data':RichText(self.testcase["configurationtitle"], style = 'myScriptStyle'),
        'configuration_data':RichText(self.testcase["configurationdata"], style = 'myScriptStyle'),
        'configuration_files':self.testcase["configurationfiles"],
        'procedure_title_data': RichText(self.testcase["proceduretitle"], style = 'myScriptStyle'),
        'procedure_data':RichText(self.testcase["proceduredata"], style = 'myScriptStyle'),
        'procedure_files':self.testcase["procedurefiles"],
        'passfail_criteria_label':RichText('Pass/Fail Criteria:', style = 'myScriptLabel'),
        'passfail_criteria_data':RichText(self.testcase["criteriadata"], style = 'myScriptStyle'),
        'result_label':RichText('Results:', style = 'myScriptLabel'),
        'results_data':RichText(self.testcase["resultsdata"].upper(), bold = True, color = "darkBlue", style = 'myScriptStatusStyle'),
        'status_label':RichText('Status:', style = 'myScriptLabel'),
        'status_data':RichText(self.testcase["statusdata"].upper(), bold = True, color = "darkBlue", style = 'myScriptStatusStyle'),
        'analysis_label':RichText('Analysis:', style = 'myScriptLabel'),
        'analysis_data':self.testcase["analysisdata"],
        'detailedresults_label':RichText('Results:', style='myScriptLabel'),
        'detailedresults_comments':RichText(self.testcase["detailedresultscomments"], style='myScriptLabel'),
        'detailedresults_data':self.testcase["detailedresultsdata"],
        'detailedresults_files':self.testcase["detailedresultsfiles"]
    }
    """
    Process the tescase data, building the test report Word document
    """
    try:
      self.testcase_report.render(self.analysis_context)
    except Exception as error:
      self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
      self.dictionary['loggerwidget'].emit(self.message)
      raise Exception
    try:
      self.testcase_report.save(self.testcase["reportfilename"])
    except Exception as error:
      self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
      self.dictionary['loggerwidget'].emit(self.message)
      raise Exception
    return()
  """
  Prepares report file fields for final report then generates the report
  """
  def generate_report(self, testcase = None, dictionary = None):
    self.testcase = testcase
    self.dictionary = dictionary
    self.testcase["statusdata"] = "COMPLETED"
    """
     Get the file where the formated report data is saved, used by AnaysisReportGenerator class
     """
    self.testcase['reportfilename'] = "{}.docx".format(self.dictionary['archivefilename'])
    self.message = "Creating analysis report file: {} for testcase {} result {}".format(self.testcase['reportfilename'], self.testcase["testcase"], self.testcase["resultsdata"])
    self.dictionary['loggerwidget'].emit(self.message)
    self.analysis_report_generator(testcase = self.testcase, dictionary = self.dictionary)
    return ()
"""
END of FILE
"""

