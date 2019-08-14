"""************************************************************************************
FILE: AnalyzeInterfaceData
CLASS:  AnalyzeInterfaceData
Author: Christopher Robson
Copyright by:  Christopher Robson
Copyright date: 01Nov2017
This software is not FREE!  Use or destribution of the software system and its
subsystem modules, libraries, configuration file and "seed" file without the
express permission of the author is strictly PROHIBITED!
FUNCTION:  Module analysizing collected data.
***********************************************************************************"""
"""
LIBRARIES:  Python libraries
"""
import ast
import datetime
"""
LIBRARIES:  Home grown specific libraries
"""
from Globals import *
from WriteDataToDiskFile import WriteDataToDiskFile
"""
CLASS: AnalyzeInterfaceData:
DESCRIPTION: Analysis show interface detail data 
INPUT: "show interface detail" captured data
OUTPUT: File containing data ready for Report generator
"""
class AnalyzeInterfaceData:
  "Analyze Interface Data"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.report_template = ""
    """
    Maintain a list of paired analyzsis data filenames:
    [(baseline-data,to-check-data),...]
    This allows the seed file to hold multiple data file pairs.
    Field format:
    element 1:  testcase number
    element 2:  report template
    element 2:  baseline data
    element 3:  to be checked data
    element 4:  Pass or fail data (format string "PASSED: [interface] [key]:[value]" )
    """
    self.testcase_number_element    = 0
    self.testcase_title_element     = 1
    self.config_file_element        = 2
    self.report_template_element    = 3
    self.baseline_data_element      = 4
    self.to_be_checked_data_element = 5
    self.pass_fail_data_element     = 6
    self.analyze_seed_file_list = []
  """
  CLASS: execute:
  DESCRIPTION: Create "show interface detail" Analysis Edit data entry point.
               Determines input data to process and passes this data onto processing methods.
  INPUT: "show interface detail" captured data
  OUTPUT: data ready for generating report data
  """
  def execute( self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dictionary = dictionary
    self.device = self.dictionary["device"]
    if self.dictionary["verbose"] == 'Yes':
      self.message = "{} started at: {}.".format(self.name, datetime.datetime.now().strftime("%d%b%Y-%H%M-%S"))
      self.dictionary['loggerwidget'].emit(self.message)
    self.message = "Building Analysis Report Data: {}{}.".format(self.dictionary["savepath"], self.dictionary["filename"])
    self.dictionary['loggerwidget'].emit(self.message)
    """
    Get the file where the analyze data is saved
    """
    try:
      self.analsis_report_filename = "{}{}{}{}".format(self.dictionary["relativepath"], self.dictionary["savepath"], self.dictionary["filename"], self.dictionary["datetime"])
      self.analysis_report_fd = open(self.analsis_report_filename, "w+")
    except:
      raise Exception( "{}: file I/O error with \"{}\"".format( self.name, self.analsis_report_filename))
    """
    Get the file that contains testcase info such as seed data and testcse numbers
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
                                                                 self.seed_dict["configfilepath"],
                                                                 self.seed_dict["configfile"]),
                                                "{}{}{}".format( self.dictionary['relativepath'],
                                                                 self.seed_dict["reporttemplatepath"],
                                                                 self.seed_dict["reporttemplate"]),
                                                "{}{}{}".format( self.dictionary['relativepath'],
                                                                 self.seed_dict["databaselinepath"],
                                                                 self.seed_dict["databaseline"] +
                                                                 self.dictionary['datetime']
                                                               ),
                                                "{}{}{}".format( self.dictionary['relativepath'],
                                                                 self.seed_dict["datatocheckpath"],
                                                                 self.seed_dict["datatocheck"] +
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
    Process the statistcial data
    """
    if self.device == "juniper":
      self.analysis_data_file( self.analyze_seed_file_list, self.analsis_report_filename, self.analysis_report_fd)
    elif self.device == "cisco":
      self.analysis_data_file( self.analyze_seed_file_list, self.analsis_report_filename, self.analysis_report_fd)
    """
    All done
    """
    return()
  """
  METHOD: analysis_data_file( self ):
  DESCRIPTION: Create "show interface detail" Analysis data
  INPUT: "show interface detail" captured data
  OUTPUT: Analysis data ready for report generation
  """
  def analysis_data_file( self, analyze_seed_file_list, analsis_report_filename, analysis_report_fd):
    self.analysis_report_fd = analysis_report_fd
    self.analsis_report_filename = analsis_report_filename
    self.analyze_seed_file_list = analyze_seed_file_list
    for self.analyze_element in self.analyze_seed_file_list:
      self.testcase_number = self.analyze_element[self.testcase_number_element]
      for self.testcase_index, self.testcase_being_run in enumerate( self.analyze_seed_file_list ):
        if self.testcase_number == self.testcase_being_run[self.pass_fail_data_element]:
          break
      self.analyze_baseline_filename = self.analyze_element[self.baseline_data_element]
      self.analyze_to_check_filename = self.analyze_element[self.to_be_checked_data_element]
      self.report_template = self.analyze_element[self.report_template_element]
      try:
        with open( self.analyze_baseline_filename, "r" ) as self.testcase_baseline_FD:
          try:
            self.testcase_to_check_FD = open( self.analyze_to_check_filename, "r" )
          except Exception as error:
            self.testcase_baseline_FD.close()
            self.message = "{{{}{}: {} {}{}}}".format(Globals.RED_MESSAGE, self.name, error, self.analyze_to_check_filename, Globals.SPAN_END_MESSAGE)
            self.dictionary['loggerwidget'].emit(self.message)
            raise Exception
          self.found_testcase_flag = False
          for self.testcase_baseline_data in self.testcase_baseline_FD:
            self.testcase_to_check_data = next( self.testcase_to_check_FD )

            # todo-debug DEBUG CODE print( "BASELINE: {}".format( self.testcase_baseline_data  ) )
            # todo-debug DEBUG CODE print( "TO CHECK: {}".format( self.testcase_to_check_data  ) )

            if self.testcase_baseline_data == "\n":
              continue
            self.found_testcase_flag = True
            try:
              self.data_baseline_dict = ast.literal_eval( self.testcase_baseline_data[:-2] )
              self.data_to_check_dict = ast.literal_eval( self.testcase_to_check_data[:-2] )
            except Exception as error:
              self.testcase_baseline_FD.close()
              self.message = "{{{}{}: {} {}{}}}".format(Globals.RED_MESSAGE, self.name, error, self.data_baseline_dict, Globals.SPAN_END_MESSAGE)
              self.dictionary['loggerwidget'].emit(self.message)
              raise Exception
            self.found_key_value_flag = False
            for self.baseline_key, self.baseline_value in self.data_baseline_dict.items():

              # todo-debug if self.baseline_key.startswith("logical interface ge-0/0/0.1 protocol inet, mtu"):
              # todo-debug   try:
              # todo-debug     if not isinstance( self.baseline_value, str ):
              # todo-debug       for k, v in self.baseline_value.items():
              # todo-debug         print("KEY: {}, VALUE:{}".format(k,v))
              # todo-debug         if k.find("received path trace") != -1:
              # todo-debug           break
              # todo-debug   except Exception as error:
              # todo-debug     print( error )

              self.found_key_value_flag = True
              if not isinstance( self.data_baseline_dict[self.baseline_key], str ):
                try:
                  self.value_baseline_dict = {}
                  self.value_to_check_dict = {}
                  self.value_baseline_dict = self.data_baseline_dict[self.baseline_key]
                  self.value_to_check_dict = self.data_to_check_dict[self.baseline_key]
                except Exception as error:
                  """
                  Got here because primary keys do not match, indicating major mismatch in data collected!
                  """
                  if not self.value_baseline_dict:
                    self.invalid_baseline_key = list(self.data_baseline_dict.keys())[self.pass_fail_data_element]
                    self.invalid_value_baseline_key = list(self.data_baseline_dict.keys())[self.pass_fail_data_element]
                    self.invalid_dict = list(self.data_baseline_dict.values())[self.pass_fail_data_element]
                    self.invalid_value_baseline_dictionary = "{{\"{}\":\"{}\"}}".format(list(self.invalid_dict.keys())[0],list(self.invalid_dict.values())[0])
                  else:
                    self.invalid_baseline_key = self.baseline_key
                    self.invalid_value_baseline_key = list(self.data_baseline_dict.keys())[self.pass_fail_data_element]
                    self.invalid_dict = list(self.data_baseline_dict.values())[self.pass_fail_data_element]
                    self.invalid_value_baseline_dictionary = "{{\"{}\":\"{}\"}}".format(list(self.invalid_dict.keys())[0],list(self.invalid_dict.values())[0])
                  if not self.value_to_check_dict:
                    self.invalid_check_key = list(self.data_to_check_dict.keys())[self.pass_fail_data_element]
                    self.invalid_value_check_key = list(self.data_to_check_dict.keys())[self.pass_fail_data_element]
                    self.invalid_dict = list(self.data_baseline_dict.values())[self.pass_fail_data_element]
                    self.invalid_value_check_dictionary = "{{\"{}\":\"{}\"}}".format(list(self.invalid_dict.keys())[0],list(self.invalid_dict.values())[0])
                  else:
                    self.invalid_check_key = list(self.data_to_check_dict.keys())[self.pass_fail_data_element]
                    self.invalid_value_check_key = list(self.data_to_check_dict.keys())[self.pass_fail_data_element]
                    self.invalid_dict = list(self.data_baseline_dict.values())[self.pass_fail_data_element]
                    self.invalid_value_check_dictionary = "{{\"{}\":\"{}\"}}".format(list(self.invalid_dict.keys())[0],list(self.invalid_dict.values())[0])
                  self.analyze_seed_file_list[self.
                    testcase_index][self.pass_fail_data_element]. \
                      append("FAILED: EXPECTED: {} {}:{} "
                             "RECEIVED: {} {}:{} ".
                             format(self.invalid_baseline_key,
                                    self.invalid_value_baseline_key,
                                    self.invalid_value_baseline_dictionary,
                                    self.invalid_check_key,
                                    self.invalid_value_check_key,
                                    self.invalid_value_check_dictionary))
                  continue
                self.found_value_key_value_flag = False
                for self.value_baseline_key, \
                    self.value_baseline_value in self.value_baseline_dict.items():
                  """
                  Process key:values that are dictionaries
                  """
                  self.found_value_key_value_flag = True
                  """
                  Process key:values where value is NOT a dictionary
                  """
                  self.value_to_check_data = self.value_to_check_dict[self.value_baseline_key]

                  # todo-debug DEBUG CODE ONLY if self.value_baseline_key.find( "received path trace" ) != -1:
                  # todo-debug DEBUG CODE ONLY   print( self.value_baseline_key )

                  try:
                    self.action_list = self.dictionary['analyzeaction']. \
                                          find_analyze_action( self.value_baseline_key,
                                                               self.dictionary['analyzeaction'].analyze_action_automaton )
                  except Exception as error:
                    self.testcase_baseline_FD.close()
                    self.message = "{{{}{}: {} -- getting Action failed{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                    self.dictionary['loggerwidget'].emit(self.message)
                    raise Exception
                  if self.action_list and self.action_list[0][1] == "ignore":
                    continue
                  if self.action_list and self.action_list[0][1] == ">":
                    # FIXME Probably should do this test instead ?? if int( self.value_baseline_data_value ) >= \
                    # FIXME which then requires the "state" of the interface we tested at the same time.yy
                    try:
                      if int( self.value_baseline_value ) > int( self.value_to_check_data ):
                          self.analyze_seed_file_list[self.
                            testcase_index][self.pass_fail_data_element]. \
                            append("FAILED: EXPECTED: {} {}:{} "
                                   "RECEIVED: {} {}:{} ".
                                   format( self.baseline_key,
                                           self.value_baseline_key,
                                           self.value_baseline_dict[self.value_baseline_key],
                                           self.baseline_key,
                                           self.value_baseline_key,
                                           self.value_to_check_dict[self.value_baseline_key]))
                      else:
                        self.analyze_seed_file_list[self.
                          testcase_index][self.pass_fail_data_element]. \
                          append("PASSED: EXPECTED: {} {}:{} "
                                 "RECEIVED: {} {}:{} ".
                                 format( self.baseline_key,
                                         self.value_baseline_key,
                                         self.value_baseline_dict[self.value_baseline_key],
                                         self.baseline_key,
                                         self.value_baseline_key,
                                         self.value_to_check_dict[self.value_baseline_key]))
                    except Exception as error:
                      self.testcase_baseline_FD.close()
                      self.message = "{{{}{}: {} -- Greater-Then test failed{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                      self.dictionary['loggerwidget'].emit(self.message)
                      raise Exception
                  elif self.action_list and self.action_list[0][1] == "not zero":
                    try:
                      if int( self.value_baseline_value ) == 0 or int( self.value_to_check_data ) == 0:
                        self.analyze_seed_file_list[self.
                          testcase_index][self.pass_fail_data_element]. \
                          append("FAILED: EXPECTED: {} {}:{} "
                                 "RECEIVED: {} {}:{} ".
                                 format( self.baseline_key,
                                         self.value_baseline_key,
                                         self.value_baseline_dict[self.value_baseline_key],
                                         self.baseline_key,
                                         self.value_baseline_key,
                                         self.value_to_check_dict[self.value_baseline_key]))
                      else:
                        self.analyze_seed_file_list[self.
                          testcase_index][self.pass_fail_data_element]. \
                          append("PASSED: EXPECTED: {} {}:{} "
                                 "RECEIVED: {} {}:{} ".
                                 format( self.baseline_key,
                                         self.value_baseline_key,
                                         self.value_baseline_dict[self.value_baseline_key],
                                         self.baseline_key,
                                         self.value_baseline_key,
                                         self.value_to_check_dict[self.value_baseline_key]))
                    except Exception as error:
                      self.testcase_baseline_FD.close()
                      self.message = "{{{}{}: {} -- Equal-To-Zerro test failed{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                      self.dictionary['loggerwidget'].emit(self.message)
                      raise Exception
                  elif self.action_list and self.action_list[0][1] == "less than":
                    try:
                      if int(self.value_baseline_value) > 0 and \
                              int(self.value_to_check_data) == 0:
                        """
                        Test for baseline is NOT zero and to-check is NOT zero but can be <, = or > baseline
                        """
                        self.analyze_seed_file_list[self.
                          testcase_index][self.pass_fail_data_element]. \
                          append("FAILED: EXPECTED: {} {}:{} "
                                 "RECEIVED: {} {}:{} ".
                                 format(self.baseline_key,
                                        self.value_baseline_key,
                                        self.value_baseline_dict[self.value_baseline_key],
                                        self.baseline_key,
                                        self.value_baseline_key,
                                        self.value_to_check_dict[self.value_baseline_key]))
                      else:
                        self.analyze_seed_file_list[self.
                          testcase_index][self.pass_fail_data_element]. \
                          append("PASSED: EXPECTED: {} {}:{} "
                                 "RECEIVED: {} {}:{} ".
                                 format( self.baseline_key,
                                         self.value_baseline_key,
                                         self.value_baseline_dict[self.value_baseline_key],
                                         self.baseline_key,
                                         self.value_baseline_key,
                                         self.value_to_check_dict[self.value_baseline_key]))
                    except Exception as error:
                      self.testcase_baseline_FD.close()
                      self.message = "{{{}{}: {} -- Less-Than test failed{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                      self.dictionary['loggerwidget'].emit(self.message)
                      raise Exception
                  elif self.action_list and self.action_list[0][1] == "pass":
                    """
                    Typically these are values which not worth checking or difficult.
                    For example, TSN will need more thought than simple ">" or "="
                    analysis
                    """
                    pass
                  elif not self.value_baseline_value == self.value_to_check_data:
                    self.analyze_seed_file_list[self.
                      testcase_index][self.pass_fail_data_element]. \
                      append("FAILED: EXPECTED: {} {}:{} "
                             "RECEIVED: {} {}:{} ".
                             format( self.baseline_key,
                                     self.value_baseline_key,
                                     self.value_baseline_dict[self.value_baseline_key],
                                     self.baseline_key,
                                     self.value_baseline_key,
                                     self.value_to_check_dict[self.value_baseline_key]))
                  else:
                    self.analyze_seed_file_list[self.
                      testcase_index][self.pass_fail_data_element]. \
                      append("PASSED: EXPECTED: {} {}:{} "
                             "RECEIVED: {} {}:{} ".
                             format( self.baseline_key,
                                     self.value_baseline_key,
                                     self.value_baseline_dict[self.value_baseline_key],
                                     self.baseline_key,
                                     self.value_baseline_key,
                                     self.value_to_check_dict[self.value_baseline_key]))
                else:
                  if not self.found_value_key_value_flag:
                    self.analyze_seed_file_list[self.
                      testcase_index][self.pass_fail_data_element]. \
                      append("FAILED: EXPECTED: {} {}:{} "
                             "RECEIVED: {} {}:{} ".
                             format( self.baseline_key,
                                     self.value_baseline_key,
                                     self.value_baseline_dict[self.value_baseline_key],
                                     self.baseline_key,
                                     self.value_baseline_key,
                                     self.value_to_check_dict[self.value_baseline_key]))
              else:
                """
                Process key:values where value is NOT a dictionary
                """
                if self.baseline_value == self.data_to_check_dict[self.baseline_key]:
                  self.analyze_seed_file_list[self.
                       testcase_index][self.pass_fail_data_element].\
                       append( "PASSED: EXPECTED: {} {}:{} "
                               "RECEIVED: {} {}:{} ".
                               format( self.baseline_key,
                                       self.baseline_key,
                                       self.data_baseline_dict[self.baseline_key],
                                       self.baseline_key,
                                       self.baseline_key,
                                       self.data_to_check_dict[self.baseline_key] ))
                else:
                  self.analyze_seed_file_list[self.
                    testcase_index][self.pass_fail_data_element]. \
                    append("FAILED: EXPECTED: {} {}:{} "
                           "RECEIVED: {} {}:{} ".
                           format( self.baseline_key,
                                   self.baseline_key,
                                   self.data_baseline_dict[self.baseline_key],
                                   self.baseline_key,
                                   self.baseline_key,
                                   self.data_to_check_dict[self.baseline_key]))
            else:
                if not self.found_key_value_flag:
                  self.analyze_seed_file_list[self.
                    testcase_index][self.pass_fail_data_element]. \
                    append("FAILED: EXPECTED: {} {}:{} "
                           "RECEIVED: {} {}:{} ".
                           format( self.baseline_key,
                                   self.baseline_key,
                                   self.data_baseline_dict[self.baseline_key],
                                   self.baseline_key,
                                   self.value_baseline_key,
                                   self.data_to_check_dict[self.baseline_key]))
          else:
            if not self.found_testcase_flag:
              self.testcase_baseline_FD.close()
              self.message = "{{{}{}: Testcase not found, {}{}}}".format(Globals.RED_MESSAGE, self.name, self.analyze_baseline_filename, Globals.SPAN_END_MESSAGE)
              self.dictionary['loggerwidget'].emit(self.message)
              raise Exception
      except Exception as error:
        self.message = "{{{}{}: {} {}{}}}".format(Globals.RED_MESSAGE, self.name, error, self.analyze_baseline_filename, Globals.SPAN_END_MESSAGE)
        self.dictionary['loggerwidget'].emit(self.message)
        raise Exception
      """
      Write the analysis data to the report file
      self.dictionary['datetime']
      """
      try:
        self.analysis_report_fd.write( "TESTCASE: {} TESTCASETITLE: {} DATETIME: {}\n".
             format( self.analyze_seed_file_list[self.testcase_index][self.testcase_number_element],
                     self.analyze_seed_file_list[self.testcase_index][self.testcase_title_element],
                     self.dictionary['datetime'][1:] ) )
        self.analysis_report_fd.write( "CONFIGDATA: {}\n".
             format( "Configurations will be found in the configuration files listed." ) )
        self.analysis_report_fd.write( "CONFIGFILE: {}\n".
             format( self.analyze_seed_file_list[self.testcase_index][self.config_file_element] ) )
        # FIXME PROCEDUREDATA !!
        # FIXME This should be data contained in a file, extracted as a single string !
        self.analysis_report_fd.write( "PROCEDUREDATA: {}\n".
             format( "Each of the above procedures is performed on all interfaces." ) )
        self.analysis_report_fd.write( "REPORTTEMPLATE: {}\n".
             format( self.analyze_seed_file_list[self.testcase_index][self.report_template_element] ) )
        self.analysis_report_fd.write( "DATAEXPECTED: {}\n".
             format( self.analyze_seed_file_list[self.testcase_index][self.baseline_data_element] ) )
        self.analysis_report_fd.write( "DATARECEIVED: {}\n".
             format( self.analyze_seed_file_list[self.testcase_index][self.to_be_checked_data_element] ) )
        self.analysis_report_fd.write( "DETAILEDRESULTSCOMMENTS: {}\n".
             format( "Additional details are found in the reports list below." ) )
      except Exception as error:
        self.message = "{{{}{}: {} {}{}}}".format(Globals.RED_MESSAGE, self.name, error, self.analyze_baseline_filename, Globals.SPAN_END_MESSAGE)
        self.dictionary['loggerwidget'].emit(self.message)
        raise Exception
      """
      Write test results to disk file
      """
      WriteDataToDiskFile(self).write_data_to_disk_file(dictionary = self.dictionary,
                                                        data = self.analyze_seed_file_list[self.testcase_index][self.pass_fail_data_element],
                                                        filename = self.analsis_report_filename,
                                                        descriptor = self.analysis_report_fd )
      self.analysis_report_fd.close()
      # todo-debug DEBUG CODE
      # todo-debug DEBUG CODE for i in self.analyze_seed_file_list[self.testcase_index][self.pass_fail_data_element]:
      # todo-debug DEBUG CODE   if i.startswith( "FAILED" ):
      # todo-debug DEBUG CODE     print(i.replace("RECEIVED", "\n        RECEIVED"))
      # todo-debug DEBUG CODE
      return()
"""***********************************************************************************************************
END of FILE
**********************************************************************************************************"""

