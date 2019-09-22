"""*************************************************************************************
FILE: InterfaceDetailAnalysisReport
CLASS:  InterfaceDetailAnalysisReport
Author: Christopher Robson
Copyright by:  Christopher Robson
Copyright date: 01Nov2017
This software is not FREE!  Use or destribution of the software system and its
subsystem modules, libraries, configuration file and "seed" file without the
express permission of the author is strictly PROHIBITED!
FUNCTION:  Module generates the report file from the AnalyzeInterfaceData results.
#NOTE:  Detailed results will print when detailedresults is set to
#       "All" to print all PASSED fields and "Yes" to ONLY print FAILED fields
*************************************************************************************"""
"""
LIBRARIES:  Python libraries
"""
import ast
import os
import datetime
"""
LIBRARIES:  Testbed Tester specific libraries
"""
from Globals import *
from AnalysisReportGenerator import AnalysisReportGenerator
from RichTextProcessor import RichTextProcessor
"""
CLASS: InterfacesDetailAnalysisReport:
DESCRIPTION: Report generation 
INPUT: 
OUTPUT:
"""
class InterfacesDetailAnalysisReport:
    "Interfaces Detail Analysis Report"
    """"""
    def __init__(self, parent = None):
        self.name = self.__class__.__name__
        self.parent = parent
    """
    CLASS: execute
    DESCRIPTION: Create "show interface detail" Analysis Edit data entry point.
                 Determines input data to process and passes this data onto processing methods.
    INPUT: "show interface detail" captured data
    OUTPUT: data ready for generating report data
    """
    def execute( self, dictionary = None, descriptor = None, data = None, decode = None):
        self.dictionary = dictionary
        """
        Extract the name of the data filenames and open up the files for processing
        """
        self.analyze_data_filename = "{}{}{}{}".format(self.dictionary['relativepath'], self.dictionary['commandpath'], self.dictionary['commands'], self.dictionary['datetime'])
        if os.stat(self.analyze_data_filename).st_size == 0:
            self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, "Analysis data file is empty!", Globals.SPAN_END_MESSAGE)
            self.dictionary['loggerwidget'].emit(self.message)
            raise Exception
        try:
            self.analyze_dataFD = open(self.analyze_data_filename, "r")
        except Exception as error:
            self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
            self.dictionary['loggerwidget'].emit(self.message)
            raise Exception
        """
        Generate the report based on device type from analysis data
        """
        self.report_analysis_data(self.analyze_dataFD)
        """
        All done
        """
        return()
    """
    METHOD: report_analysis_data(self):
    DESCRIPTION: Processes the AnalyzeInterfaceData results data
    INPUT: Master seed file entry for "commands" keyword
    OUTPUT: Word document formated report file, typically the final testcase report
    """
    def report_analysis_data(self, dataFD):
        self.dataFD = dataFD
        self.argen = AnalysisReportGenerator(self)
        self.testcase = self.argen.get_testase_dictionary()
        """
        Process the data into a formatted Microsoft Word document
        """
        try:
            for self.data_line in self.dataFD:
                if self.data_line.startswith("TESTCASE: "):
                    self.testcase["testcase"] = self.data_line.split("TESTCASETITLE: ")[0].split("TESTCASE: ")[1]
                    self.testcase["testcasetitle"] = self.data_line.split("TESTCASETITLE: ")[1].split("DATETIME: ")[0]
                    self.date_time = self.data_line.split("DATETIME: ")[1].split("\n")[0]
                    continue
                if self.data_line.startswith("CONFIGDATA: "):
                    self.testcase["configurationdata"] = self.data_line.split("CONFIGDATA: ")[1].split("\n")[0]
                    continue
                if self.data_line.startswith("CONFIGFILE: "):
                    self.configuration_files_str = "{{\'cols\':[\'{}\']}}".format(os.path.basename(self.data_line.split("CONFIGFILE: ")[1].split("\n")[0]))
                    try:
                        self.configuration_files_dict = ast.literal_eval(self.configuration_files_str)
                    except Exception as error:
                        self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                        self.dictionary['loggerwidget'].emit(self.message)
                        raise Exception
                    RichTextProcessor(self).plain_text_to_richtext_unformat(self.configuration_files_dict)
                    self.testcase["configurationfiles"].append(self.configuration_files_dict)
                    continue
                if self.data_line.startswith("PROCEDUREDATA: "):
                    self.testcase["proceduredata"] = self.data_line.split("PROCEDUREDATA: ")[1].split("\n")[0]
                    continue
                if self.data_line.startswith("PROCEDUREFILE: "):
                    self.procedure_files_str = "{{\'cols\':[\'{}\']}}".format(self.data_line.split("PROCEDUREFILE: ")[1].split("\n")[0])
                    try:
                        self.procedure_files_dict = ast.literal_eval(self.procedure_files_str)
                    except Exception as error:
                        self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                        self.dictionary['loggerwidget'].emit(self.message)
                        raise Exception
                    RichTextProcessor(self).plain_text_to_richtext_unformat(self.procedure_files_dict)
                    self.testcase["procedurefiles"].append(self.procedure_files_dict)
                    continue
                if self.data_line.startswith("REPORTTEMPLATE: "):
                    self.testcase['reporttemplate'] = self.data_line.split("REPORTTEMPLATE: ")[1].split("\n")[0]
                    continue
                if self.data_line.startswith("DATAEXPECTED: "):
                    try:
                        self.testcase["expecteddatafilename"] = self.data_line.split("DATAEXPECTED: ")[1].split("\n")[0]
                        self.report_data_files_str = "{{\'cols\':[\'{}\']}}".format(os.path.basename(self.testcase["expecteddatafilename"]))
                        self.report_data_files_dict = ast.literal_eval(self.report_data_files_str)
                    except Exception as error:
                        self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                        self.dictionary['loggerwidget'].emit(self.message)
                        raise Exception
                    RichTextProcessor(self).plain_text_to_richtext_unformat(self.report_data_files_dict)
                    self.testcase["detailedresultsfiles"].append(self.report_data_files_dict)
                    continue
                if self.data_line.startswith("DATARECEIVED: "):
                    try:
                        self.testcase["receiveddatafilename"] = self.data_line.split("DATARECEIVED: ")[1].split("\n")[0]
                        self.report_data_files_str = "{{\'cols\':[\'{}\']}}".format(os.path.basename(self.testcase["receiveddatafilename"]))
                        self.report_data_files_dict = ast.literal_eval(self.report_data_files_str)
                    except Exception as error:
                        self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                        self.dictionary['loggerwidget'].emit(self.message)
                        raise Exception
                    RichTextProcessor(self).plain_text_to_richtext_unformat(self.report_data_files_dict)
                    self.testcase["detailedresultsfiles"].append(self.report_data_files_dict)
                    continue
                if self.data_line.startswith("DETAILEDRESULTSCOMMENTS: "):
                    self.testcase["detailedresultscomments"] = self.data_line.split("DETAILEDRESULTSCOMMENTS: ")[1].split("\n")[0]
                    continue
                """
                Check if passed then write one Analysis field with the tag "Validated"
                """
                if self.data_line.startswith("PASSED: "):
                    if self.testcase["resultsdata"] == "FAILED":
                        pass
                        # FIXME REMOVE ? REPLACE THE PASS IF ONLY WANT ERRORS PRINTED SEE BELOW FIXME continue
                    else:
                        self.testcase["resultsdata"] = "PASSED"
                        self.expected_received_data = "{{\'cols\':[\'{}\',\'{}\',\'{}\']}}".format("Validated", "Validated", "Validated")
                        try:
                            self.expected_received_dict = ast.literal_eval(self.expected_received_data)
                        except Exception as error:
                            self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                            self.dictionary['loggerwidget'].emit(self.message)
                            raise Exception
                        RichTextProcessor(self).plain_text_to_richtext_format(self.expected_received_dict)
                        try:
                            self.testcase["analysisdata"][0] = self.expected_received_dict
                        except:
                            self.testcase["analysisdata"].append(self.expected_received_dict)
                    """
                    Build the Detailed Results Data section of the Testcase Report
                    """
                    if self.dictionary['detailedresults'] == 'All':
                        self.expected = self.data_line.split("EXPECTED: ")[1].split("RECEIVED: ")[0].split(":")[1]
                        try:
                            self.interface = self.data_line.split("EXPECTED: ")[1].split("RECEIVED: ")[0].split(":")[0].split(" ".join(self.data_line.split(":")[2].split()[3:]))[0]
                        except:
                            self.interface = " "
                        if self.data_line.split("EXPECTED: ")[1].startswith("show interfaces") or self.data_line.split("EXPECTED: ")[1].startswith("device"):
                            continue
                        self.field = " ".join(self.data_line.split(":")[2].split()[3:])
                        self.detailed_results_data = "{{\'cols\':[\'{}\',\'{}\',\'{}\']}}".format(self.interface, self.field, self.expected)
                        try:
                            self.detailed_results_data_dict = ast.literal_eval(self.detailed_results_data)
                        except Exception as error:
                            self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                            self.dictionary['loggerwidget'].emit(self.message)
                            raise Exception
                        RichTextProcessor(self).plain_text_to_richtext_color_format(self.detailed_results_data_dict, Globals.DARKRED, Globals.GREEN)
                        self.testcase["detailedresultsdata"].append(self.detailed_results_data_dict)
                    continue
                """
                If a failure occurred then whipout any PASSED Validated entries and fill 
                with failure data.
                """
                if self.data_line.startswith("FAILED: "):
                    if self.testcase["resultsdata"] == "PASSED":
                        self.testcase["analysisdata"] = []
                    # FIXME REMOVE ?? BUT LEAVE IN IF ONLY WANT ERRORS PRINTED   self.testcase["detailedresultsdata"] = []
                    self.testcase["resultsdata"] = "FAILED"
                    """
                    Build the Analysis section of the Testcase Report
                    """
                    self.expected = self.data_line.split("EXPECTED: ")[1].split("RECEIVED: ")[0].split(":")[1]
                    self.received = self.data_line.split("RECEIVED: ")[1].split("\n")[0].split(":")[1]
                    self.expected_received_data = "{{\'cols\':[\'{}\',\'{}\',\'{}\']}}".format(" ".join(self.data_line.split(":")[2].split()[3:]), self.expected, self.received)
                    try:
                        self.expected_received_dict = ast.literal_eval(self.expected_received_data)
                    except Exception as error:
                        self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                        self.dictionary['loggerwidget'].emit(self.message)
                        raise Exception
                    RichTextProcessor(self).plain_text_to_richtext_format(self.expected_received_dict)
                    self.testcase["analysisdata"].append(self.expected_received_dict)
                    """
                    Build the Detailed Results Data section of the Testcase Report
                    """
                    if self.dictionary['detailedresults']:
                        try:
                            self.interface = self.data_line.split("EXPECTED: ")[1].split("RECEIVED: ")[0].split(":")[0].split(" ".join(self.data_line.split(":")[2].split()[3:]))[0]
                        except:
                            self.interface = " "
                        self.field = " ".join(self.data_line.split(":")[2].split()[3:])
                        self.detailed_results_data = "{{\'cols\':[\'{}\',\'{}\',\'{}\']}}".format(self.interface, self.field, self.expected)
                        try:
                            self.detailed_results_data_dict = ast.literal_eval(self.detailed_results_data)
                        except Exception as error:
                            self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                            self.dictionary['loggerwidget'].emit(self.message)
                            raise Exception
                        RichTextProcessor(self).plain_text_to_richtext_color_format(self.detailed_results_data_dict, Globals.BLACK, Globals.BLUE, Globals.RED, True, True, True)
                        self.testcase["detailedresultsdata"].append(self.detailed_results_data_dict)
                    continue
        except Exception as error:
            self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
            self.dictionary['loggerwidget'].emit(self.message)
            raise Exception
        """
        Generate the report
        """
        # todo-debug for k, v in self.testcase.items():
        # todo-debug   print("K:{} V:{}".format(k,v))
        self.argen.generate_report(testcase = self.testcase, dictionary = self.dictionary)
        return()
"""
END of FILE
"""
