"""*******************************************************************************************
* FILE: GuiStart
* PROJECT: DataCollectionAnalysisReportingAutomation
* CLASS(s): GuiStart
* MEMBER(s):
* AUTHOR: Christopher L. Robson (UID): 
* DATE: 9/17/18 TIME: 13:24:00
* COPYRIGHT (c): 9/17/18 Christopher L. Robson. All rights reserved.
*                This software is not FREE!  Use or destribution of the software system
*                and its subsystem modules, libraries, configuration file and "seed" file
*                without the express permission of the author is strictly PROHIBITED!
* DESCRIPTION:  Main GUI interface and processing.  Developed from QT-Designer,
*               PCUIC4(5) and then heavely modified.
*
*******************************************************************************************"""
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QFileDialog
import sys
import os
import shutil
import subprocess
"""
#  Home grown libraries
"""
import GUI
from Globals import Globals
from SSHToDevice import SSHToDevice
from ProfilesPathDialog import ProfilesPathDialog
from Applications import Applications
from TerminalWindow import TerminalWindow
from ExcelWorkbookNoneBlockingProcessor import ExcelWorkbookNoneBlockingProcessor
from BuildTemplateFiles import BuildTemplateFiles
from BuildSeedFileProcessor import BuildSeedFileProcessor
from BuildTemplateFileList import BuildTemplateFileList
from BuildSeedFileList import BuildSeedFileList
from Mapper import Mapper
from NoneBlocking import NoneBlocking
from Capitalization import Capitalization
from BoldType import BoldType
from WriteListData import WriteListData
from EnableDisableButtons import EnableDisableButtons
from SeedCommandlinePreprocessor import SeedCommandlinePreprocessor
"""
CLASS: GuiStart
METHOD: __init__
DESCRIPTION: called by the startup script DCARAS.py after the commandline options are processed
INPUT: Commandline arguements and QT5 QApplications class 
OUTPUT: 
"""
class GuiStart( QtWidgets.QMainWindow, GUI.GuiMainWindow ):
    def __init__( self, args ):
        super( GuiStart, self ).__init__()
        self.name = self.__class__.__name__
        self.none_blocking = None
        self.istemplate = False
        self.istemplateseed = False
        self.args = args
        Globals.show_command_counter = 0
        Globals.dut_command_counter = 0
        """
        Speed button processing some, this class is called a lot so set the reference here
        """
        self.write_list_data = WriteListData(parent = self)
        """
        Save commandline arguments for later reference
        """
        Globals.relativepath = self.args.relativepath
        if Globals.relativepath:
            sys.path.append(Globals.relativepath)
        Globals.password_to_use = self.args.password_to_use
        Globals.user_to_use = self.args.user_to_use
        self.directory_str = "{}".format(self.args.networkMasterTestsetProfile)
        try:
            if not self.args.networkMasterTestsetProfile.startswith( "~" ):
                Globals.initial_directory = "{}{}".format( self.args.relativepath,
                                                           self.args.networkMasterTestsetProfile.split( "/." )[0] )
            else:
                Globals.initial_directory = "{}/.{}".format( os.path.expanduser( '~' ),
                                                             self.args.networkMasterTestsetProfile.split( "/." )[1] )
        except:
            print( "System directory \"{}\" not correct!".format( self.args.networkMasterTestsetProfile ) )
            sys.exit()
        self.diagram_str   = "{}".format(self.args.networkDiagramProfile)
        self.templates_str   = "{}".format(self.args.templatesProfileFile)
        self.template_seed_str   = "{}".format(self.args.templateSeedFile)
        self.verbose       = self.args.verbose
        self.debug         = self.args.debug
        self.run_counter   = int( float( self.args.run_counter ) )
        self.delay_timer   = int( float( self.args.delay_timer ) )
        Globals.search_filename = args.searchList
        Globals.inventory_directory = "{}".format(args.inventory_directory)
        Globals.inventory_file_directory = "{}".format(args.inventory_file_directory)
        """
        Build the main GUI
        """
        self.actionExecuteTest = None
        self.actionExit = None
        self.actionChangeProfilesDirectory = None
        self.actionSelectPlaybook = None
        self.actionSelectDeviceUnderTest = None
        self.actionClearDUTSelections = None
        self.actionAbout = None
        self.actionDocumentation = None
        self.startButton = None
        self.pauseButton = None
        self.stopButton = None
        self.cancelButton = None
        self.gui_main_window(self)
        """
        Establish callbacks 
        """
        self.menubar.actionExecuteTest.triggered.connect( lambda: self.execute_test( QtWidgets.QApplication ) )
        self.menubar.actionExit.triggered.connect( lambda: self.exit_system( QtWidgets.QApplication ))
        self.menubar.actionChangeProfilesDirectory.triggered.connect( self.change_profiles_directory )
        self.menubar.actionSelectPlaybook.triggered.connect( self.select_dut_playbook )
        self.menubar.actionSelectDeviceUnderTest.triggered.connect( self.select_devices )
        self.menubar.actionClearDUTSelections.triggered.connect( self.clear_devices )
        self.menubar.actionAbout.triggered.connect( self.about_the_system )
        self.menubar.actionDocumentation.triggered.connect( self.documentation_of_system )
        self.startButton.clicked.connect( lambda: self.testbed_tester_start( QtWidgets.QApplication ) )
        self.pauseButton.clicked.connect( lambda: self.testbed_tester_pause( QtWidgets.QApplication ) )
        self.stopButton.clicked.connect( lambda: self.testbed_tester_stop( QtWidgets.QApplication ) )
        self.cancelButton.clicked.connect( lambda: self.testbed_tester_cancel( QtWidgets.QApplication ) )

        # notes KEEP FOR DEBUGGING self.actionMapNetwork.triggered.connect( self.map_network )

        """
        set the profiles directory variable and diagram and its path then paint it in widget
        """
        self.ppd = ProfilesPathDialog( )
        self.ppd.templates_dialog( self.templates_str )
        self.ppd.template_seed_dialog( self.template_seed_str )
        self.ppd.profiles_dialog( self.directory_str )
        self.write_list_data.write_list_data(list_widget = self.consoleListWidget, data = self.ppd.get_profiles_directory(), color="darkgreen", bold="demibold", sorted=False)
        """"""
        self.statusBarMessages.showMessage("System is operational")
    """
    """
    def terminate_program( self ):
        self.message = "Acme Automator terminated"
        self.write_list_data.write_list_data( self.consoleListWidget, self.message)
        sys.exit()
    """
    """
    @QtCore.pyqtSlot()
    def build_master_seed_file( self ):
        BuildSeedFileProcessor( self ).build_seed_file_processor()
        return()
    """
    """
    def clear_template_file_selection( self ):
        Globals.template_file = ""
        Globals.templates_list = []
        self.message = "Template files cleared "
        self.write_list_data.write_list_data( self.consoleListWidget, self.message)
    """
    """
    def list_and_select_template_file( self ):
        BuildTemplateFileList( ).template_file_list( )
        self.TestbedTesterListWindow.clear()
        for item_list in Globals.templates_list:
            self.TestbedTesterListWindow.addItem( item_list )
            self.TestbedTesterListWindow.sortItems( QtCore.Qt.AscendingOrder )
        self.TestbedTesterListWindow.itemClicked.connect( self.select_template_file )
        return ()
    """
    """
    def select_template_file( self, selected_file ):
        if Globals.template_file:
            return()
        Globals.template_file = selected_file.text( )
        self.message = "Template file: {}".format(selected_file.text())
        self.write_list_data.write_list_data( self.consoleListWidget, self.message)
        return ()
    """
    """
    def clear_seed_file_selection( self ):
        Globals.template_seed_file = ""
        Globals.template_seed_list = []
        self.message = "Template Seed files cleared "
        self.write_list_data.write_list_data( self.consoleListWidget, self.message)
    """
    """
    def list_and_select_seed_file( self ):
        BuildSeedFileList().seed_file_list( )
        self.TestbedTesterListWindow.clear()
        for item_list in Globals.template_seed_list:
            self.TestbedTesterListWindow.addItem( item_list )
            self.TestbedTesterListWindow.sortItems( QtCore.Qt.AscendingOrder )
        self.TestbedTesterListWindow.itemClicked.connect( self.select_seed_file )
        return()
    """
    """
    def select_seed_file( self, selected_file ):
        if Globals.template_seed_file:
            return()
        Globals.template_seed_file = selected_file.text()
        self.message = "Template file: {}".format(selected_file.text())
        self.write_list_data.write_list_data( self.consoleListWidget, self.message)
        return()
    """
    """
    @QtCore.pyqtSlot()
    def execute_test( self, QtWidgets_QApplication ):
        self.started = True
        self.results = ""
        Globals.show_command_counter = 0
        Globals.dut_command_counter = 0

        self.statusBarMessages.showMessage("Executing test")

        self.button_control = EnableDisableButtons()
        self.button_control.EnableDisableButtons(self.startButton, False)
        self.button_control.EnableDisableButtons(self.stopButton, True, color = Globals.RED)
        self.button_control.EnableDisableButtons(self.cancelButton, True, color = Globals.RED)
        self.button_control.EnableDisableButtons(self.pauseButton, True, color = Globals.GREEN)
        self.write_list_data.write_list_data(list_widget = self.consoleListWidget, data = "*** please wait ***".format(), color="purple", bold="extrabold",
                                             capitalize="upper", fontsize=26 )
        self.write_list_data.write_list_data(list_widget = self.consoleListWidget, data = "Tests are running".format(), color="black", bold="normal",
                                             capitalize="", fontsize=12 )
        self.none_blocking = NoneBlocking(parent = self, qtapplication = QtWidgets_QApplication)
        self.none_blocking.set_verbose_flag(self.verbose)
        self.none_blocking.set_debug_flag(self.debug)
        self.none_blocking.set_run_count(self.run_counter)
        self.none_blocking.set_delay_timer(self.delay_timer)
        QtWidgets_QApplication.processEvents(QtCore.QEventLoop.AllEvents)
        self.none_blocking.run_thread()
        return()
    """
    """
    @QtCore.pyqtSlot()
    def testbed_tester_start( self, QtWidgets_QApplication ):
        try:
            self.none_blocking.run_thread()
        except Exception as error:
            self.write_list_data.write_list_data(list_widget = self.consoleListWidget, data = "Please \"Execute\" test before slecting Start, "
                                                                                              "action ignored.".format(), color="red", bold="extrabold",
                                                 capitalize="", fontsize=16 )
        return()
    """
    """
    @QtCore.pyqtSlot()
    def testbed_tester_pause( self, QtWidgets_QApplication ):
        try:
            self.output = subprocess.Popen("python3 PauseButtonMain.py", stdout = subprocess. PIPE,stderr = subprocess.PIPE, shell=True)
            self.outputresults, self.err = self.output.communicate()
        except Exception as error:
            self.write_list_data.write_list_data(list_widget = self.consoleListWidget, data = "Paused failed: {}".format(error), color="red", bold="extrabold", fontsize=16 )
        return()
    """
    """
    @QtCore.pyqtSlot()
    def testbed_tester_stop( self, QtWidgets_QApplication ):
        try:
            self.none_blocking.stop_testing()
        except Exception as error:
            self.write_list_data.write_list_data(list_widget = self.consoleListWidget, data = "Please \"Execute\" test before selecting Stop, "
                                                                                              "action ignored.".format(), color="red", bold="extrabold", fontsize=16 )
        return()
    """
    """
    @QtCore.pyqtSlot()
    def testbed_tester_cancel( self, QtWidgets_QApplication ):
        try:
            self.none_blocking.terminate_testing()
            self.clear_devices()
        except Exception as error:
            self.write_list_data.write_list_data(list_widget = self.consoleListWidget, data = "Please \"Execute\" test before selecting Cancel, "
                                                                                              "action ignored.".format(), color="red", bold="extrabold", fontsize=16 )
        return()
    """
    """
    def exit_system(self, QtWidgets_QApplication):
        QtWidgets_QApplication.closeAllWindows()
        QtWidgets_QApplication.exit()
        print( "Exit system!" )
        sys.exit()
    """
    Change profiles directory
    # notes >> QFileDialog.getOpenFileNames <--- "s" plural user can select multiple files NOT used here  !
    """
    def change_profiles_directory( self ):
        self.clear_devices()
        self.options = QFileDialog.Options()
        self.options |= QFileDialog.AnyFile
        self.options |= QFileDialog.DontUseNativeDialog
        self.selection = QFileDialog.getOpenFileName(self.parent(), "Select seed file containing profiles directory",
                                                     Globals.initial_directory, "", options = self.options)
        if self.selection[0].find( "-Profiles-Directory") == -1:
            self.write_list_data.write_list_data(list_widget = self.consoleListWidget,
                                                 data = "Not a valid profiles seed file, please try again.".format(),
                                                 color="#FF00FF", bold="normal", capitalize="", fontsize=12 )
            return()
        self.ppd = ProfilesPathDialog( )
        self.ppd.profiles_dialog(self.selection[0])
        self.write_list_data.write_list_data(list_widget = self.consoleListWidget, data = self.ppd.get_profiles_directory(),
                                             color="darkgreen", bold="normal", fontsize=12)
        self.clear_devices(False)
    """
    Clear all selection and their DUT display
    """
    def clear_devices( self, flag=True ):
        if flag and Globals().get_dut_ip_list() or Globals().get_dut_to_be_tested_list() or Globals().get_playbook_list():
            self.write_list_data.write_list_data(list_widget = self.consoleListWidget, data = "Cleared devices to be tested list.",
                                                 color="black", bold="normal", fontsize=12)
            self.statusBarMessages.showMessage("Cleared devices to be tested list")
            self.dutListWidget.clear()
        Globals().clear_dut_ip_list()
        Globals().clear_dut_to_be_tested_list( )
        Globals().clear_playbook_list()
        try:
            self.dutListWidget.itemClicked.disconnect( self.set_profiles_directory )
        except:
            pass
        try:
            self.dutListWidget.itemClicked.disconnect( self.device_to_be_tested )
        except:
            pass
        try:
            self.dutListWidget.itemClicked.disconnect( self.playbook_to_be_tested )
        except:
            pass
    """
    Select DUT playbook
    """
    @QtCore.pyqtSlot()
    def select_dut_playbook( self ):
        self.clear_devices()
        self.options = QFileDialog.Options()
        self.options |= QFileDialog.AnyFile
        self.options |= QFileDialog.DontUseNativeDialog
        self.duts_list, self.files = QFileDialog.getOpenFileNames(self.parent(), "Select Playbook with Devices Under Test",
                                                                  Globals.initial_directory, "", options = self.options)
        for self.dut in self.duts_list:
            if self.dut.startswith("plabook-") or self.dut.endswith(".pbk"):
                Globals.playbook_list.append(self.dut)
                self.write_list_data.write_list_data(list_widget = self.dutListWidget, data = "{}".format(os.path.basename(self.dut)), color="black", bold="normal", fontsize=12 )
                try:
                    with open(self.dut, 'r') as self.playbook_FD:
                        for self.playbook_dut in self.playbook_FD:
                            self.playbook_dut = self.playbook_dut.split('\n')[0]
                            if not SeedCommandlinePreprocessor(self).iscommented(data = self.playbook_dut):
                                continue
                            else:
                                if self.playbook_dut.endswith("-master-profile.prf"):
                                    self.dutname = "{}".format(str(os.path.basename(self.playbook_dut).split("-master-profile.prf")[0]).replace("-", " - "))
                                    Globals.dut_ip_to_be_tested_list.append(self.dutname)
                                    Globals.dut_ip_list.append("  {}  ".format(self.dutname))
                                    Globals.dut_ip_list_dict.update(
                                        {str(os.path.basename(self.playbook_dut).split("-master-profile.prf")[0]): os.path.basename(self.playbook_dut)})
                                    self.write_list_data.write_list_data(list_widget = self.dutListWidget, data = "{}".format(self.dutname), color = "black",
                                                                         bold = "normal", fontsize = 12)
                except Exception as error:
                    self.write_list_data.write_list_data(list_widget = self.consoleListWidget, data = "{}".format(error),
                                                         color="red", bold="extrabold", fontsize=16 )
        self.statusBarMessages.showMessage("Selected playbook(s) configured with devices for testing")
        return ()
    """
    Display/Select DUT(s) to be tested
    """
    def select_devices( self ):
        self.clear_devices()
        self.options = QFileDialog.Options()
        self.options |= QFileDialog.AnyFile
        self.options |= QFileDialog.DontUseNativeDialog
        """
        While self.files isnt used below it allows self.duts_list contains the list of files with access it as a offset
        """
        self.duts_list, self.files = QFileDialog.getOpenFileNames(self.parent(), "Select Device Under Test",
                                                                  Globals.initial_directory, "", options = self.options)
        for self.dut in self.duts_list:
            if self.dut.endswith("-master-profile.prf"):
                self.dutname = "{}".format(str(os.path.basename(self.dut).split("-master-profile.prf")[0]).replace("-", " - "))
                Globals.dut_ip_to_be_tested_list.append(self.dutname)
                Globals.dut_ip_list.append("  {}  ".format(self.dutname))
                Globals.dut_ip_list_dict.update({str(os.path.basename(self.dut).split("-master-profile.prf")[0]):os.path.basename(self.dut)})
                self.write_list_data.write_list_data(list_widget = self.dutListWidget, data = "{}".format(self.dutname), color = "black",
                                                     bold = "normal", fontsize = 12)
        self.statusBarMessages.showMessage("Selected devices for testing")
        return()
    """
    SSSH to Device
    """
    def ssh_to_device( self ):
        self.message = "Spawning SSH session."
        self.write_list_data.write_list_data( self.consoleListWidget, self.message)
        self.results = SSHToDevice(). \
            ssh_to_device( ProfilesPathDialog().get_profiles_directory() )
        if self.results.find( "FAILED" ) != -1:
            self.results_parse = self.results.split( "\n" )
            for self.results_str in self.results_parse:
                self.write_list_data.write_list_data(list_widget = self.consoleListWidget, data = "{}".format( self.result_str ), color="red", bold="extrabold", fontsize=16)
        return()
    """
    """
    def map_network(self):
        self.write_list_data.write_list_data("{}".format("Mapping the network"), color="black", bold="normal", fontsize=12)
        self.map_image = Mapper( self ).mapper()
        # fixme NEEDS WORKS HERE !!!!
        self.image_parent_window = QMainWindow()
        self.image_display_window = MessagesProcessor()
        self.image_display_window.message_window_initializer()
        return ()
    """
    """
    def build_inventory_file_list(self):
        self.message = "{}Inventory files to process:{}".format(Globals.BLUE_FONT1O_BOLD_MESSAGE, Globals.SPAN_END_MESSAGE)
        self.write_list_data.write_list_data( self.consoleListWidget, self.message)
        self.path = Globals.inventory_file_directory
        Globals().clear_show_file_list()
        try:
            for content in os.listdir( self.path ):
                Globals().set_show_file_list( self.path + content )
            for self.file_list in Globals().get_show_file_list():
                self.write_list_data.write_list_data( self.consoleListWidget, self.file_list)
        except Exception as error:
            self.message = "{}Build inventory file list error: {}{}".format(Globals.BLUE_FONT1O_BOLD_MESSAGE, error, Globals.SPAN_END_MESSAGE)
            self.write_list_data.write_list_data( self.consoleListWidget, self.message)
        return()
    """
    """
    def select_excel_template( self ):
        self.message = "Running Excel Workbook Template Processor Subsystem."
        self.write_list_data.write_list_data( self.consoleListWidget, self.message)
        self.testbed_tester_inventory_process = ExcelWorkbookNoneBlockingProcessor( self )
        self.testbed_tester_inventory_process.set_verbose_flag( self.verbose )
        self.testbed_tester_inventory_process.set_debug_flag( self.debug )
        self.testbed_tester_inventory_process.set_run_count( self.run_counter )
        self.testbed_tester_inventory_process.set_delay_timer( self.delay_timer )
        self.testbed_tester_inventory_process.run_thread()
        return ()
    """
    """
    def about_the_system( self ):
        self.write_list_data.write_list_data(list_widget = self.consoleListWidget, data = "{}".format("This is the Multiple Network Device "
                                                                                                      "Configuration and Traffic Generator System!"),
                                             color="black", bold="normal", fontsize=12)
        return()
    """
    """
    def documentation_of_system( self ):
        self.write_list_data.write_list_data(list_widget = self.consoleListWidget, data = "{}".format("If you need documentation on how to use this system, "
                                                                                                      "find a new career path cause you suck at this!"),
                                             color="black", bold="normal", fontsize=12)
        return()
"""*******************************************************************************************
End of Main
*******************************************************************************************"""