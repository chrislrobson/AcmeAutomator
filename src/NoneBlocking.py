"""*************************************************************************************************
MODULE: NoneBlocking
Author: Christopher Robson
Copyright by:  Christopher Robson
Copyright date: 01Jan2016
This software is not FREE!  Use or destribution of the software system and its
subsystem modules, libraries, configuration file and "seed" file without the
express permission of the author is strictly PROHIBITED!
FUNCTION:  Module provides the interface between the GUI and the testing modules.
FUNCTION:  Class provides the interface between the GUI subsystem classes and the testing classes
           controlled by the Processor class.
           Message passing between the GUI and the testing classes is accomplished
           using Qt5 "Signal and Slot" processing system.
           Called by selecting the "Execute" button on the menu "Test DUT" and passed to the threaded "Worker" class.
           This class is the main processing loop.
           Its function is to read the seed master file, extract each command (the very first quoted word of each
           line(string) in the master seed file and using that first word, called the command control word,
           and spawn the associated comands class/methods via the importlib function
Return:  Returns to the calling class any data collected from the DUT for further
         processing by the calling class.
Errors:  Errors are logged directly to the report or logger scroll window at the subclass level via the
         Qt5 Signal/Slot flow control with messages eventual processed by the Worker class calling the thread.
Processing Flow:  GUI (select) ---> Worker (connect) ---> Processor (importlib)---> Command Classes (ssh)---> devices
                  divices (data) ---> Command Classes (signal/exception) ---> Processor (signal/exception) --->
                  Worker (signal) ---> GUI (present)
************************************************************************************************"""
"""
Python Libraries
"""
import ast
import time
import datetime
from PyQt5 import QtCore, QtWidgets
"""
Home grown stuff
"""
import GUI
from Processor import Processor
from Globals import *
from WriteListData import WriteListData
from EnableDisableButtons import EnableDisableButtons
"""
CLASS: NoneBlocking
DESCRIPTION:
INPUT: seed file with commands to execute
OUTPUT: device command output
"""
class NoneBlocking(QtWidgets.QMainWindow, GUI.GuiMainWindow):
  " None Blocking"
  """"""
  reset_next_test_signal = QtCore.pyqtSignal(object)
  def __init__(self, parent = None, qtapplication = None):
    super(NoneBlocking, self).__init__(parent)
    self.name = self.__class__.__name__
    self.parent = parent
    self.qtapplication = qtapplication
    try:
      self.qtapplication.processEvents(QtCore.QEventLoop.AllEvents)
    except Exception as error:
      print(error)
    """
    Pass console buttons to subsystem so operator can manipulate GUI
    """
    self.menu_test = self.parent.menubar.menuTest
    self.consoleDutTabWidget = self.parent.consoleDutTabWidget
    self.logsListWidget = self.parent.logsListWidget
    self.consoleListWidget = self.parent.consoleListWidget
    self.verbose = False  # Commandline verbose flag (not the same flag as the seed file verbose!
    """
    Speed button processing some, this class is called a lot so set the reference here
    """
    self.button_controls = EnableDisableButtons()
    """
    Initialize the thread called Worker
    """
    self.thread = Worker(self)
    self.thread.moveToThread(self.thread)
    """
    We connect the standard finished() and terminated() signals from the
    thread to the same slot in the widget. This will reset the user
    interface when the thread stops running.
    The custom "Thread has run" signal is connected to the
    generate_the_report() slot so that we can update the viewer window
    with the completed test run report.
    """
    self.thread.test_run_done_signal.connect(self.generate_the_report)
    self.reset_next_test_signal.connect(self.reset_for_next_test_run)
    self.thread.console_message_signal.connect(self.print_console_messages)
    self.thread.logger_message_signal.connect(self.print_logger_messages)
    self.thread.create_tab_signal.connect(self.create_tab)
    self.thread.report_message_signal.connect(self.print_report_messages)
  """
  Setup reports and logger tab windows
  Here all console/report messages will be displayed 
  """
  def setup_reports_window(self, consoleDutTabWidget, tab_id):
    self.consoleDutTabWidget = consoleDutTabWidget
    self.tab_id = tab_id
    WriteListData(self).message_window_initializer(self.consoleDutTabWidget, self.tab_id)
    return ()
  """
  Debug diagnostic flags handling
  """
  def set_debug_flag(self, debug = False):
    self.debug = debug
    return ()
  """
  Set QEventLoop calling
  """
  def set_qtapplication(self, qtapplication = None):
    self.qtapplication = qtapplication
    return ()
  """
  Verbose diagnostic flags handling
  """
  def set_verbose_flag(self, verbose = False):
    self.verbose = verbose
    return ()
  """
  Returns delay timer between DUT runs
  """
  def get_delay_timer(self):
    return (self.delay_timer)
  """
  Set delay timer between DUT runs
  """
  def set_delay_timer(self, delay_timer = 0):
    self.delay_timer = delay_timer
    return ()
  """
  Returns count of test to run
  """
  def get_run_count(self):
    return (self.run_count)
  """
  Set count of test run so far
  """
  def set_run_count(self, run_count = 1):
    self.set_ran_count(0)
    self.run_count = run_count
    return ()
  """
  Returns count of tests that have run
  """
  def get_ran_count(self):
    return (self.ran_count)
  """
  Set count of test that have run
  """
  def set_ran_count(self, ran_count = 0):
    self.ran_count = ran_count
    return ()
  """
  Prints any messages from the subsystem processes via the signal/slot bus.
  """
  @QtCore.pyqtSlot(object)
  def print_logger_messages(self, message):
    if not isinstance(message, str) or message == None or len(message) == 0:
      WriteListData(self).write_list_data(list_widget = self.logsListWidget, data = "Logger Report - Invalid data received!", color = Globals.RED, bold = "bold", fontsize = 14)
      return ()
    try:
      self.message = ast.literal_eval(message)
      try:
        self.color = self.message["color"]
      except:
        self.color = "black"
      try:
        self.weight = self.message["weight"]
      except:
        self.weight = "normal"
      try:
        self.capitalize = self.message["capitalize"]
      except:
        self.capitalize = ""
      try:
        self.fontsize = int(self.message["fontsize"])
      except:
        self.fontsize = 12
      try:
        self.text = self.message["text"]
      except:
        self.text = self.message
    except:
      self.text = message
      WriteListData(self).write_list_data(list_widget = self.logsListWidget, data = self.text, qtapplication = self.qtapplication)
      return()
    WriteListData(self).write_list_data(list_widget = self.logsListWidget, data = self.text, color = self.color,
                                         bold = self.weight, capitalize = self.capitalize,
                                         fontsize = self.fontsize, qtapplication = self.qtapplication)
    return ()
  """
  Prints any messages from the subsystem processes via the signal/slot bus.
  """
  @QtCore.pyqtSlot(object)
  def print_console_messages(self, message):
    if not isinstance(message, str) or message == None or len(message) == 0:
      WriteListData(self).write_list_data(list_widget = self.logsListWidget, data = "Console Report - Invalid data received!", color = Globals.RED, bold = "bold", fontsize = 14)
      return ()
    try:
      self.message = ast.literal_eval(message)
      try:
        self.color = self.message["color"]
      except:
        self.color = "black"
      try:
        self.weight = self.message["weight"]
      except:
        self.weight = "normal"
      try:
        self.capitalize = self.message["capitalize"]
      except:
        self.capitalize = ""
      try:
        self.fontsize = int(self.message["fontsize"])
      except:
        self.fontsize = 12
      try:
        self.text = self.message["text"]
      except:
        self.text = self.message
    except:
      self.text = message
      WriteListData(self).write_list_data(list_widget = self.consoleListWidget, data = self.text, qtapplication = self.qtapplication)
      return()
    WriteListData(self).write_list_data(list_widget = self.consoleListWidget, data = self.text, color = self.color,
                                         bold = self.weight, capitalize = self.capitalize,
                                         fontsize = self.fontsize, qtapplication = self.qtapplication)
    return ()
  """
  Create a tab for the report window used in thread subsystem processes via the signal/slot bus.
  """
  @QtCore.pyqtSlot(object, object)
  def create_tab(self, widget, tab_id):
    self.widget = widget
    self.tab_id = tab_id
    WriteListData(self).message_window_initializer(self.widget, tab_id = self.tab_id)
    return()
  """
  Prints any messages from the thread or its subsystem processes via the signal/slot bus.
  """
  @QtCore.pyqtSlot(object, object, object)
  def print_report_messages(self, message, widget, tab_id):
    self.widget = widget
    self.tab_id = tab_id
    if not isinstance(message, str) or message == None or len(message) == 0:
      WriteListData(self).write_list_data(list_widget = self.logsListWidget, data = "Print Report - Invalid data received!", color = Globals.RED, bold = "bold", fontsize = 14)
      return ()
    try:
      self.message = ast.literal_eval(message)
      try:
        self.color = self.message["color"]
      except:
        self.color = "black"
      try:
        self.weight = self.message["weight"]
      except:
        self.weight = "normal"
      try:
        self.capitalize = self.message["capitalize"]
      except:
        self.capitalize = ""
      try:
        self.fontsize = int(self.message["fontsize"])
      except:
        self.fontsize = 12
      try:
        self.text = self.message["text"]
      except:
        self.text = self.message
    except:
      self.text = message
      WriteListData(self).write_list_data(list_widget = self.widget, data = self.text, qtapplication = self.qtapplication)
      return()
    WriteListData(self).write_list_data(list_widget = self.widget, data = self.text, color = self.color,
                                         bold = self.weight, capitalize = self.capitalize,
                                         fontsize = self.fontsize, qtapplication = self.qtapplication)
    return ()
  """
  Stop all tests but stay in Testbed Autmator subsystem
  """
  @QtCore.pyqtSlot(object)
  def stop_testing(self):
    self.thread.terminate()
    self.thread.wait()
    self.set_ran_count(0)
    self.button_controls.EnableDisableButtons(self.parent.startButton, True, color = Globals.GREEN)
    self.button_controls.EnableDisableButtons(self.parent.stopButton, False)
    self.button_controls.EnableDisableButtons(self.parent.cancelButton, True, color = Globals.RED)
    return()
  """
  Terminate all tests and return to the main GUI
  """
  @QtCore.pyqtSlot(object)
  def terminate_testing(self):
    self.button_controls.EnableDisableButtons(self.parent.startButton, False)
    self.button_controls.EnableDisableButtons(self.parent.stopButton, False)
    self.button_controls.EnableDisableButtons(self.parent.cancelButton, False)
    self.menu_test.setDisabled(False)
    if self.thread.isRunning():
      self.thread.terminate()
      self.thread.wait()
    self.close()
    self.message = "All testing stopped at: {} \nAction buttons reset.".format(datetime.datetime.now().strftime("%d%b%Y-%H%M-%S"))
    WriteListData(self).write_list_data(list_widget = self.consoleListWidget, data = self.message)
    return ()
  """
  The run_thread() slot needs to do two things: disable the user
  interface widgets that are used to start a thread, and run another test (aka disable menu drop down "Test"
  start the thread with the appropriate parameters.
  """
  @QtCore.pyqtSlot(object)
  def run_thread(self):
    self.button_controls.EnableDisableButtons(self.parent.startButton, False)
    self.button_controls.EnableDisableButtons(self.parent.stopButton, True, color = Globals.RED)
    self.button_controls.EnableDisableButtons(self.parent.cancelButton, True, color = Globals.RED)
    self.menu_test.setDisabled(True)
    self.thread.start()
    return ()
  """
  The Testbed Tester has run and generated a report then "emitted"
  a signal to run this slot to print the report.
  """
  @QtCore.pyqtSlot(object)
  def generate_the_report(self, report_results):
    cnt = self.get_ran_count()
    cnt += 1
    self.set_ran_count(cnt)
    # fixme DO WE REALLY WANT THIS ??? time.sleep(self.delay_timer)
    self.results = "Test Report has been generated"
    self.reset_next_test_signal.emit(self.results)
    return ()
  """
  The reset_for_next_test_run() slot is called when a thread stops running.
  This happens because the "finished() method of Threader is connected
  to this reset_for_next_test_run() method.
  Since we usually want to let the user run the thread again,
  we reset the user interface to enable the start button to be pressed:
  """
  @QtCore.pyqtSlot(object)
  def reset_for_next_test_run(self, message):
    run_count = self.get_run_count()
    ran_count = self.get_ran_count()
    if ran_count < run_count:
      self.button_controls.EnableDisableButtons(self.parent.startButton, False)
      self.button_controls.EnableDisableButtons(self.parent.stopButton, True, color = Globals.RED)
      self.button_controls.EnableDisableButtons(self.parent.cancelButton, True, color = Globals.RED)
      self.run_thread()
    else:
      self.set_ran_count(0)
      self.button_controls.EnableDisableButtons(self.parent.startButton, True, color = Globals.GREEN)
      self.button_controls.EnableDisableButtons(self.parent.stopButton, False)
      self.button_controls.EnableDisableButtons(self.parent.cancelButton, True, color = Globals.RED)
      self.message = "All test runs have completed at: {} \n".format(datetime.datetime.now().strftime("%d%b%Y-%H%M-%S"))
      WriteListData(self).write_list_data(list_widget = self.consoleListWidget, data = self.message)
    return()
"""
CLASS: Worker
DESCRIPTION:  The worker thread is implemented as a PyQt thread rather than a
             Python thread since we want to take advantage of the signals and
             slots mechanism to communicate with the main application.
----
INPUT: seed file with commands to execute
OUTPUT: device command output
"""
class Worker(QtCore.QThread):
  "nonBlocking Thread Process"
  """
  Remeber to match up the "object" passed here to the associated method's @QtCore.pyqtSlot statement
  For example:
  @QtCore.pyqtSlot(object, object)
  def print_report_messages(self, message, widget, tab_id):
  """
  test_run_done_signal = QtCore.pyqtSignal(object)
  console_message_signal = QtCore.pyqtSignal(object)
  logger_message_signal = QtCore.pyqtSignal(object)
  create_tab_signal = QtCore.pyqtSignal(object, object)
  report_message_signal = QtCore.pyqtSignal(object, object, object)
  nonBlocking = None
  """"""
  def __init__(self, parent = None):
    self.name = self.__class__.__name__
    self.nonBlocking = parent
    self.consoleDutTabWidget = self.nonBlocking.consoleDutTabWidget
    self.consoleListWidget = self.nonBlocking.consoleListWidget
    """
    Initialize the Threading system
    """
    QtCore.QThread.__init__(self)
    """
    The exiting attribute is used to tell the thread to stop
    processing.
    """
    self.exiting = False
  """
  Before a Worker object is destroyed, we need to ensure that it
  stops processing. For this reason, we implement the following
  method in a way that indicates to the part of the object that
  performs the processing that it must stop, and waits until it
  does so.
  """
  def __del__(self):
    if self.nonBlocking.verbose:
      self.results = "Stopping the thread process and wait for all things to end."
      self.test_run_done_signal.emit(self.results)
    self.exiting = True
    self.wait()
  """
  The start() method is a special method that sets up the thread
  and calls our implementation of the run() method. We provide the
  render() method instead of letting our own run() method take extra
  arguments because the run() method is called by PyQt itself with
  no arguments.
  The run() method is where we perform the processing that occurs
  in the thread provided by the Worker instance:
  """
  def run(self):
    """
     Call the real worker, the subsystem that communications directly
     with the DUTS to collect information and statistical data.
    """
    try:
      Processor(self).processor()
    except Exception as error:
      if error.args:
        self.message  = "{" + Globals.RED_MESSAGE
        self.message += "{}(run): failure {}NOTE(!!!) Coding violation error MUST be processed at lower level".format(self.name, error)
        self.message += " OMG, another shithead who thinks they are God's gift to coders!"
        self.message += Globals.SPAN_END_MESSAGE + "}"
        self.logger_message_signal.emit(self.message)
    """
    Single the thread has completed.
    results = string holding report data.
    """
    self.results = "Acme Automator tests completed at {}".format(datetime.datetime.now().strftime("%d%b%Y-%H%M-%S"))
    self.test_run_done_signal.emit(self.results)
"""
End of File
"""
