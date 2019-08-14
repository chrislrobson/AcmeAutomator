#####################################################################################################################
# Python Qt5 Testbed Tester Create Master Seed From Excel Processor
# Author: Christopher Robson
# Copyright by:  Christopher Robson
# Copyright date: 01Jan2016
# This software is not FREE!  Use or destribution of the software system and its
# subsystem modules, libraries, configuration file and "seed" file without the
# express permission of the author is strictly PROHIBITED!
# FUNCTION: This class create a master seed file from an excel workbook
#####################################################################################################################
from PyQt5 import QtCore, QtWidgets
#-------------------------------------------------------------------------------------------------------------------
# Home grown stuff
#-------------------------------------------------------------------------------------------------------------------
import GUI
from ExcelWorkbookProcessor import ExcelWorkbookProcessor
#-------------------------------------------------------------------------------------------------------------------
class ExcelWorkbookNoneBlockingProcessor( QtWidgets.QMainWindow, GUI.GuiMainWindow ):
  " Excel Workbook None Blocking Processor"
  #-----------------------------------------------------------------------------------------------------------------
  reset_next_test_signal = QtCore.pyqtSignal( object )
  def __init__(self, parent = None ):
    super( ExcelWorkbookNoneBlockingProcessor, self).__init__( parent )
    self.parent = parent
    self.name = " Excel Workbook None Blocking Processor"
    self.verbose = False
    #
    # Initialize the thread called Worker
    #
    self.thread = ExcelWorkbookProcessorThread( self )
    self.thread.moveToThread(self.thread)
    #
    # We connect the standard finished() and terminated() signals from the
    # thread to the same slot in the widget. This will reset the user
    # interface when the thread stops running.
    #
    self.thread.logger_message_signal.connect(self.print_thread_messages)
    self.thread.simulator_message_signal.connect(self.print_logger_messages)
    self.thread.processor_message_signal.connect(self.print_logger_messages)
  #---
  # Debug diagnostic flags handling
  #---
  def set_debug_flag( self, debug = False ):
    self.debug = debug
    return ()
  #---
  # Verbose diagnostic flags handling
  #---
  def set_verbose_flag( self, verbose = False ):
    self.verbose = verbose
    return ()
  #----
  # Returns delay timer between DUT runs
  #----
  def get_delay_timer(self):
    return ( self.delay_timer )
  #----
  # Set delay timer between DUT runs
  #----
  def set_delay_timer( self, delay_timer = 0 ):
    self.delay_timer = delay_timer
    return ()
  #----
  # Returns count of test to run
  #----
  def get_run_count(self):
    return ( self.run_count )
  #----
  # Set count of test run so far
  #----
  def set_run_count( self, run_count = 1 ):
    self.set_ran_count( 0 )
    self.run_count = run_count
    return ()
  #----
  # Returns count of tests that have run
  #----
  def get_ran_count(self):
    return (self.ran_count)
  #----
  # Set count of test that have run
  #----
  def set_ran_count( self, ran_count = 0 ):
    self.ran_count = ran_count
    return ()
  #----
  # Prints any messages from the subsystem processes via the signal/slot bus.
  #----
  def print_logger_messages( self, message ):
    self.parent.logScrollAreaWidgetContents.append( message )
    return ()
  #----
  # Prints any messages from the thread or its subsystem processes via the signal/slot bus.
  #----
  def print_thread_messages( self, message ):
    self.parent.reportScrollAreaWidgetContents.append( message )
    return ()
  #------------------------------------------------------------------------------------------------------------------
  # Stop all tests but stay in Testbed Autmator subsystem
  # -----------------------------------------------------------------------
  def stop_testing( self ):
    self.thread.terminate()
    self.thread.wait()
    self.set_ran_count( 0 )
    if self.verbose:
      self.parent.reportScrollAreaWidgetContents.append( "Stopped Testbed Tester inventory processing." )
    self.parent.startButton.setEnabled(True)
    self.parent.stopButton.setEnabled( False )
    self.parent.cancelButton.setEnabled( True )
    return()
  #------
  # Terminate all tests and return to the main GUI
  # -----------------------------------------------------------------------
  def terminate_testing( self ):
    self.parent.startButton.setEnabled( False )
    self.parent.stopButton.setEnabled( False )
    self.parent.cancelButton.setEnabled( False )
    self.thread.terminate()
    self.thread.wait()
    self.close()
    if self.verbose:
      self.parent.reportScrollAreaWidgetContents.append("Terminated Testbed Tester inventory processing!")
    return ()
  #-----------------------------------------------------------------------
  # The run_thread() slot needs to do two things: disable the user
  # interface widgets that are used to start a thread, and
  # start the thread with the appropriate parameters.
  #-----------------------------------------------------------------------
  def run_thread( self ):
    self.parent.startButton.setEnabled( False )
    self.parent.stopButton.setEnabled( False )
    self.parent.cancelButton.setEnabled( False )
    self.thread.start()
    if self.verbose:
      self.parent.reportScrollAreaWidgetContents.append( "Started another inventory process." )
      ### FIXME WHEN BUTTONS WORK ADD self.parent.reportScrollAreaWidgetContents.append( "Started another inventory process. "
      ### FIXME WHEN BUTTONS WORK ADD                                                    "The \"Start button\" has been disabled." )
    return ()
#-------------------------------------------------------------------------------------------------------------------
# Now that we have seen how an instance of the Window class uses the
# worker thread, let us take a look at the thread's implementation.
#
# The Worker Thread
#
# The worker thread is implemented as a PyQt thread rather than a
# Python thread since we want to take advantage of the signals and
# slots mechanism to communicate with the main application.
#-------------------------------------------------------------------------------------------------------------------
class ExcelWorkbookProcessorThread(QtCore.QThread):
  "Testbed Tester Excel Workbook Processor Thread"
  test_run_done_signal = QtCore.pyqtSignal( object )
  logger_message_signal = QtCore.pyqtSignal( object )
  simulator_message_signal = QtCore.pyqtSignal( object )
  processor_message_signal = QtCore.pyqtSignal( object )
  testbed_tester = None
  #-----------------------------------------------------------------------------------------------------------------
  def __init__(self, parent = None):
    self.name = "Testbed Autmator Excel Workbook Processor Thread Process"
    #-----------------------------------------------------------------------
    # Initialize the Testbed Tester configuration accesses
    #-----------------------------------------------------------------------
    #self.testbed_tester = testbed_tester
    self.testbed_tester = parent
    #-----------------------------------------------------------------------
    # Initialize the Threading system
    #-----------------------------------------------------------------------
    QtCore.QThread.__init__(self)
    if self.testbed_tester.verbose:
      self.testbed_tester.reportScrollAreaWidgetContents.append( "Excel Workbook Processor Thread has been enabled." )
    #-----------------------------------------------------------------------
    # The exiting attribute is used to tell the thread to stop
    # processing.
    #-----------------------------------------------------------------------
    self.exiting = False
  #-----------------------------------------------------------------------
  # Before a Worker object is destroyed, we need to ensure that it
  # stops processing. For this reason, we implement the following
  # method in a way that indicates to the part of the object that
  # performs the processing that it must stop, and waits until it
  # does so.
  #-----------------------------------------------------------------------
  def __del__(self):
    if self.testbed_tester.verbose:
      thread_message = "Stopping the thread process and " \
                       "wait for all things to end."
      self.logger_message_signal.emit( thread_message)
    self.exiting = True
    self.wait()
  #-----------------------------------------------------------------------
  # The start() method is a special method that sets up the thread
  # and calls our implementation of the run() method. We provide the
  # render() method instead of letting our own run() method take extra
  # arguments because the run() method is called by PyQt itself with
  # no arguments.
  # The run() method is where we perform the processing that occurs
  # in the thread provided by the Worker instance:
  #-----------------------------------------------------------------------
  def run(self):
    #-----------------------------------------------------------------------
    # Call the real worker, the subsystem that processes the inventory
    #-----------------------------------------------------------------------
    ExcelWorkbookProcessor( self ).process_workbook()
    if self.testbed_tester.verbose:
      thread_message = "Testbed Tester Excel Workbook processing has completed."
      self.logger_message_signal.emit( thread_message )
####################################################################################################################
# Exit point of IE521NetworkDeviceInventoryControl.py
####################################################################################################################
