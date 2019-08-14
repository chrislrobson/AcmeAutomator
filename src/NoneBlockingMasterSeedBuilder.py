####################################################################################################################
# Python Qt5 Testbed Tester System
# MODULE:  
# Author: Christopher Robson
# Copyright by:  Christopher Robson
# Copyright date: 01Jan2016
# This software is not FREE!  Use or destribution of the software system and its
# subsystem modules, libraries, configuration file and "seed" file without the
# express permission of the author is strictly PROHIBITED!
# FUNCTION:  Module provides the inetrface between the GUI and the testing modules.
#            This interface consist of two main pieces, a window that is used to display
#            collected data and a messaging channel between the testing modules and the
#            display window.
#            Message passing between the GUI and the testing modules is accomplished
#            using Qt5 "Signal and Slot" processing system.
####################################################################################################################
import sys
import time
import datetime
from PyQt5 import QtCore, QtWidgets, QtGui
#-------------------------------------------------------------------------------------------------------------------
# Home grown stuff
#-------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------
from Globals import *
#--------------------------------------------------------------------------------------------------------------------
from BuildSeedFileProcessor import BuildMasterSeedFileProcessor
#--------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------
try:
  _encoding = QtWidgets.QApplication.UnicodeUTF8
  def _translateMSFP(context, text, disambig):
    return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
  def _translateMSFP(context, text, disambig):
    return QtWidgets.QApplication.translate(context, text, disambig)
#--------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------
class NoneBlockingMasterSeedBuilder( QtWidgets.QDialog ):
  " None Blocking Master Seed Builder"
  #-----------------------------------------------------------------------------------------------------------------
  def __init__(self, parent = None ):
    super( NoneBlockingMasterSeedBuilder, self).__init__( parent )
    #FIXME REMOVE THIS CODE BELOW
    Globals().templates_file_list.append( "template_file_examplle_01.tpl" )
    Globals().templates_file_list.append( "template_file_examplle_02.tpl" )
    Globals().templates_file_list.append( "template_file_examplle_03.tpl" )
    #FIXME REMOVE THIS CODE ABOVE
    #---------------------------------------------------------------------------------------------------------------
    self.parent = parent
    self.name = " None Blocking Master Seed Builder"
    self.verbose = False
    self.method_to_run = ""
    # -----------------------------------------------------------------------
    # Initialize the thread called Worker
    # -----------------------------------------------------------------------
    self.thread = Worker( self )
    self.thread.moveToThread(self.thread)
    # -----------------------------------------------------------------------
    # The main window in this example is just a QWidget.
    # We create a single Worker instance that we can reuse as required.
    # The user interface consist of a window for outputing the test report
    # results string and a "Start" button to initiate a new test run.
    # -----------------------------------------------------------------------
    self.viewer = QtWidgets.QWidget(self)
    self.viewer.setObjectName("TestbedTesterBuildMasterSeedFileWindow")
    self.viewer.setMinimumSize(QtCore.QSize(890, 850))
    self.viewer.resize(self.sizeHint())
    # ---------------------------------------------------------------------------------------------------------------
    self.mainMenubar = QtWidgets.QMenuBar(self.viewer)
    self.mainMenubar.setGeometry(QtCore.QRect(0, 0, 1600, 23))
    self.mainMenubar.setObjectName("mainMenubar")
    self.menuUtilities = QtWidgets.QMenu(self.mainMenubar)
    self.menuUtilities.setObjectName("menuUtilities")
    self.actionExecute_Build_Master_Seed_File = QtWidgets.QAction(self.viewer)
    self.actionExecute_Build_Master_Seed_File.setObjectName("actionExecute_Build_Master_Seed_File")
    self.actionSelect_Template = QtWidgets.QAction(self.viewer)
    self.actionSelect_Template.setObjectName( "actionSelect_Template" )
    self.actionSelect_Template_Seed_File = QtWidgets.QAction(self.viewer)
    self.actionSelect_Template_Seed_File.setObjectName( "actionSelect_Template_Seed_File" )
    self.menuUtilities.setTitle(_translateMSFP("TestbedTesterMainWindow", "Utilities", None))
    self.actionSelect_Template.setText( _translateMSFP( "TestbedTesterMainWindow", "Select Template", None ) )
    self.actionSelect_Template_Seed_File.setText( _translateMSFP( "TestbedTesterMainWindow",
                                                                  "Select Template Seed File", None ) )
    self.mainMenubar.addAction(self.menuUtilities.menuAction())
    self.mainMenubar.addAction(self.menuUtilities.menuAction())
    self.menuUtilities.addAction(self.actionSelect_Template)
    self.menuUtilities.addSeparator()
    self.menuUtilities.addAction( self.actionSelect_Template_Seed_File )
    self.menuUtilities.addSeparator()
    self.menuUtilities.addAction(self.actionExecute_Build_Master_Seed_File)
    self.menuUtilities.addSeparator()
    self.retranslate_master_seed_processor_menu( self.viewer )
    self.actionExecute_Build_Master_Seed_File.triggered.connect( self.build_master_seed_files )
    self.actionSelect_Template.triggered.connect( self.select_template_to_process )
    self.actionSelect_Template_Seed_File.triggered.connect( self.select_template_seed_file_to_process )
    # FIXME USED ON OTHER MENU BUT DOESNT WORK HERE WHY ??? -> self.viewer.setMenuBar(self.mainMenubar)
    # ---------------------------------------------------------------------------------------------------------------
    self.MasterSeedFileMainWindow = QtWidgets.QWidget(self.viewer)
    self.MasterSeedFileMainWindow.setGeometry(QtCore.QRect(10, 30, 870, 800))
    self.templateMessageCentralWidget = QtWidgets.QWidget(self.MasterSeedFileMainWindow)
    self.templateMessageCentralWidget.setObjectName("templateMessageCentralWidget")

    self.tplseedMessageScrollAreaTitle = QtWidgets.QLabel(self.templateMessageCentralWidget)
    self.tplseedMessageScrollAreaTitle.setGeometry(QtCore.QRect(400, 0, 150, 20))
    self.tplseedMessageScrollAreaTitle.setText("Messages")
    self.templateSeedScrollAreaTitle = QtWidgets.QLabel(self.templateMessageCentralWidget)
    self.templateSeedScrollAreaTitle.setGeometry(QtCore.QRect(600, 145, 150, 30))
    self.templateSeedScrollAreaTitle.setText("Template Seed Files")
    self.templateScrollAreaTitle = QtWidgets.QLabel(self.templateMessageCentralWidget)
    self.templateScrollAreaTitle.setGeometry(QtCore.QRect(150, 145, 150, 30))
    self.templateScrollAreaTitle.setText("Template Files")

    self.tplseedMessageScrollArea = QtWidgets.QScrollArea(self.templateMessageCentralWidget)
    self.tplseedMessageScrollArea.setGeometry(QtCore.QRect(0, 25, 870, 120))
    # ---- FIXME WHY PALLETET DOESNT WORK !!!!! --------
    self.palette = QtGui.QPalette()
    self.brush = QtGui.QBrush(QtGui.QColor(233, 185, 110))
    self.brush.setStyle(QtCore.Qt.SolidPattern)
    self.palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, self.brush)
    self.tplseedMessageScrollArea.setPalette(self.palette)
    # ----- FIXME ??????
    self.tplseedMessageScrollArea.setFrameShape(QtWidgets.QFrame.WinPanel)
    self.tplseedMessageScrollArea.setLineWidth(2)
    self.tplseedMessageScrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
    self.tplseedMessageScrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
    self.tplseedMessageScrollArea.setWidgetResizable(True)
    self.tplseedMessageScrollArea.setObjectName("tplseedMessageScrollArea")
    self.tplseedMessageScrollAreaContents = QtWidgets.QTextEdit()
    self.tplseedMessageScrollAreaContents.setGeometry(QtCore.QRect(0, 0, 600, 100))
    self.tplseedMessageScrollAreaContents.setObjectName("tplseedMessageScrollAreaContents")
    # FIXME REMOVE LATER ! self.tplseedMessageScrollAreaContents.append("This is the report Window, click the \"Start\" "
    # FIXME REMOVE LATER !                                               "button to initiate a test run.")
    self.tplseedMessageScrollArea.setWidget(self.tplseedMessageScrollAreaContents)
    # ------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------
    self.templateCentralWidget = QtWidgets.QWidget(self.MasterSeedFileMainWindow)
    self.templateCentralWidget.setObjectName("templateCentralWidget")
    self.templateScrollArea = QtWidgets.QScrollArea(self.templateCentralWidget)
    self.templateScrollArea.setGeometry(QtCore.QRect(0, 170, 440, 620))
    self.templateScrollArea.setFrameShape(QtWidgets.QFrame.WinPanel)
    self.templateScrollArea.setLineWidth(2)
    self.templateScrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
    self.templateScrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
    self.templateScrollArea.setWidgetResizable(True)
    self.templateScrollArea.setObjectName("templateScrollArea")
    # FIXME self.templateScrollAreaWidgetContents = QtWidgets.QTextEdit()
    self.templateScrollAreaWidgetContents = QtWidgets.QListWidget( self.templateCentralWidget )
    self.templateScrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 170, 440, 620))
    self.templateScrollAreaWidgetContents.setFrameShape(QtWidgets.QFrame.WinPanel)
    self.templateScrollAreaWidgetContents.setLineWidth(2)
    self.templateScrollAreaWidgetContents.setObjectName("templatescrollAreaWidgetContents")
    # FIXME ???????? self.templateScrollArea.setWidget(self.templateScrollAreaWidgetContents)
    #FIXME REMOVE self.templateListWindow = QtWidgets.QListWidget( self.templateCentralWidget )
    #FIXME REMOVE self.templateListWindow.setGeometry(QtCore.QRect(0, 170, 440, 620))
    #FIXME REMOVE self.templateListWindow.setFrameShape(QtWidgets.QFrame.WinPanel)
    #FIXME REMOVE self.templateListWindow.setLineWidth(2)
    #FIXME REMOVE self.templateListWindow.setObjectName("templateListWindow")
    # ------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------
    self.templateSeedCentralWidget = QtWidgets.QWidget(self.MasterSeedFileMainWindow)
    self.templateSeedCentralWidget.setObjectName("templateSeedCentralWidget")
    self.templateSeedScrollArea = QtWidgets.QScrollArea(self.templateSeedCentralWidget)
    self.templateSeedScrollArea.setGeometry(QtCore.QRect(450, 170, 420, 620))
    self.templateSeedScrollArea.setFrameShape(QtWidgets.QFrame.WinPanel)
    self.templateSeedScrollArea.setLineWidth(2)
    self.templateSeedScrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
    self.templateSeedScrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
    self.templateSeedScrollArea.setWidgetResizable(True)
    self.templateSeedScrollArea.setObjectName("templateSeedScrollArea")
    self.templateSeedScrollAreaWidgetContents = QtWidgets.QTextEdit()
    self.templateSeedScrollAreaWidgetContents.setGeometry(QtCore.QRect(450, 170, 420, 620))
    self.templateSeedScrollAreaWidgetContents.setObjectName("templateSeedScrollAreaWidgetContents")
    # FIXME REMOVE LATER ! self.templateSeedScrollAreaWidgetContents.setText("Template seed data goes here!")
    self.templateSeedScrollArea.setWidget(self.templateSeedScrollAreaWidgetContents)
    # -----------------------------------------------------------------------
    # We connect the standard finished() and terminated() signals from the
    # thread to the same slot in the widget. This will reset the user
    # interface when the thread stops running.
    # The custom "Thread has run" signal is connected to the
    # generate_the_report() slot so that we can update the viewer window
    # with the completed test run report.
    # -----------------------------------------------------------------------
    self.thread.tplseed_logger_message_signal.connect(self.print_tplseed_thread_messages)
    self.thread.template_logger_message_signal.connect(self.print_template_thread_messages)
    self.thread.seed_logger_message_signal.connect(self.print_seed_thread_messages)
  #-----------------------------------------------------------------------------------------------------------------
  #-----------------------------------------------------------------------------------------------------------------
  def retranslate_master_seed_processor_menu( self, TestbedTesterMainWindow ):
    self.menuUtilities.setTitle(_translateMSFP("TestbedTesterMainWindow", "Utilities", None))
    self.actionExecute_Build_Master_Seed_File.setText(_translateMSFP("TestbedTesterMainWindow",
                                                                     "Build Master", None))
  #-----------------------------------------------------------------------------------------------------------------
  #-----------------------------------------------------------------------------------------------------------------
  def run_thread(self):
    self.thread.start()
    if self.verbose:
      self.tplseedMessageScrollAreaContents.append( "Running Template Seed file building process." )
    return ()
  # ----------------------------------------------------------------------------------------------------------------
  # Select Template to Process
  # ----------------------------------------------------------------------------------------------------------------
  def select_template_to_process( self ):
    self.method_to_run = "SelectTemplateToProcess"
    self.run_thread()
    return ()
  #----------------------------------------------------------------------------------------------------------------
  # Select Template to Process
  #----------------------------------------------------------------------------------------------------------------
  def select_template_to_preprocess( self ):
    self.method_to_run = "SelectTemplateToProcess"
    self.run_thread()
    return ()
  #----------------------------------------------------------------------------------------------------------------
  # Select Template Seed File to Process
  #----------------------------------------------------------------------------------------------------------------
  def select_template_seed_file_to_process( self ):
    self.method_to_run = "SelectTemplateSeedFileToProcess"
    self.run_thread()
    return ()
  # ----------------------------------------------------------------------------------------------------------------
  # Build Master Seed Files
  # ----------------------------------------------------------------------------------------------------------------
  def build_master_seed_files( self ):
    self.method_to_run = "BuildMasterSeedFiles"
    self.run_thread()
    return ()
  # ----------------------------------------------------------------------------------------------------------------
  # Debug diagnostic flags handling
  # ----------------------------------------------------------------------------------------------------------------
  def set_debug_flag( self, debug = False ):
    self.debug = debug
    return ()
  # ----------------------------------------------------------------------------------------------------------------
  # Verbose diagnostic flags handling
  # ----------------------------------------------------------------------------------------------------------------
  def set_verbose_flag( self, verbose = False ):
    self.verbose = verbose
    return ()
  # -----------------------------------------------------------------------------------------------------------------
  # Prints any messages from the subsystem processes via the signal/slot bus.
  # -----------------------------------------------------------------------------------------------------------------
  def print_seed_thread_messages( self, message ):
    self.templateSeedScrollAreaWidgetContents.append( message )
    return ()
  # -----------------------------------------------------------------------------------------------------------------
  # Prints any messages from the thread or its subsystem processes via the signal/slot bus.
  # -----------------------------------------------------------------------------------------------------------------
  def print_template_thread_messages( self, message ):
    self.templateScrollAreaWidgetContents.append( message )
    return ()
  #-----------------------------------------------------------------------------------------------------------------
  # Prints any messages from the thread or its subsystem processes via the signal/slot bus.
  #-----------------------------------------------------------------------------------------------------------------
  def print_tplseed_thread_messages(self, message):
    self.tplseedMessageScrollAreaContents.append(message)
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
class Worker(QtCore.QThread):
  " None Blocking Master Seed Builder Worker"
  buildtemplateseed_signal = QtCore.pyqtSignal( object )
  tplseed_logger_message_signal = QtCore.pyqtSignal( object )
  template_logger_message_signal = QtCore.pyqtSignal( object )
  seed_logger_message_signal = QtCore.pyqtSignal( object )
  #-----------------------------------------------------------------------------------------------------------------
  def __init__(self, parent = None):
    self.name = " None Blocking Master Seed Builder Worker"
    #-----------------------------------------------------------------------
    self.parent = parent
    #-----------------------------------------------------------------------
    # Initialize the Threading system
    #-----------------------------------------------------------------------
    QtCore.QThread.__init__(self)
    if self.parent.verbose:
      self.tplseed_logger_message_signal.emit( "Template Seed Building is running." )
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
    if self.parent.verbose:
      thread_message = "Stopping the thread process and " \
                       "wait for all things to end."
      self.parent.logger_message_signal.emit( thread_message )
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
  def run( self ):
    #-----------------------------------------------------------------------
    # Call the real worker, the subsystem that communications directly
    # with the DUTS to collect information and statistical data.
    #-----------------------------------------------------------------------
    BuildMasterSeedFileProcessor( self ).run_master_seed_file_processor_thread()
    #-----------------------------------------------------------------------
    # Single the thread has completed.
    # results = string holding report data.
    #-----------------------------------------------------------------------
    results = "Testbed Tester thread completed at {}".format( datetime.datetime.now().strftime( "%d%b%Y-%H%M-%S" ) )
    if self.parent.verbose:
      thread_message =  "Selection has completed."
      self.tplseed_logger_message_signal.emit( thread_message )
#-------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------

