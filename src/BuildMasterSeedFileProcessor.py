####################################################################################################################
# Python Qt5 Testbed Tester Build Master Seed File Processor
# MODULE:  BuildMasterSeedFileProcessor
# Author: Christopher Robson
# Copyright by:  Christopher Robson
# Copyright date: 01Jan2016
# This software is not FREE!  Use or destribution of the software system and its
# subsystem modules, libraries, configuration file and "seed" file without the
# express permission of the author is strictly PROHIBITED!
# FUNCTION:  Module communicates with the DUT, connecting to the DUT and performing some T&E task with the DUT.
#            Message passing between the GUI and the testing modules is accomplished
#            using Qt5 "Signal and Slot" processing system.
####################################################################################################################
import importlib
from PyQt5 import QtCore, QtWidgets, QtGui
#-------------------------------------------------------------------------------------------------------------------
# Home grown stuff
#-------------------------------------------------------------------------------------------------------------------
from Globals import Globals
#-------------------------------------------------------------------------------------------------------------------
class BuildMasterSeedFileProcessor( QtCore.QThread ):
  " BuildMaster Seed File Processor Processor"
  #-----------------------------------------------------------------------------------------------------------------
  def __init__(self, parent = None):
    super(BuildMasterSeedFileProcessor, self).__init__(parent)
    self.name = " Build Master Seed File Processor"
    self.parent = parent
    self.gparent = parent.parent
  #-----------------------------------------------------------------------------------------------------------------
  def run_master_seed_file_processor_thread( self ):
    try:
      self.module = importlib.import_module( "BuildMasterSeedFileProcessor" )
      self.module_class = getattr( self.module, self.gparent.method_to_run )
      self.module_method = self.module_class( self )
      self.results = self.module_method.execute()
    except Exception as error:
      self.message_ptr = Globals.RED_MESSAGE + \
                         error.args[0] + \
                         Globals.SPAN_END_MESSAGE
      self.parent.tplseed_logger_message_signal.emit( self.message_ptr )
      raise
    return()
#-------------------------------------------------------------------------------------------------------------------
# Select Template to Process
#-------------------------------------------------------------------------------------------------------------------
class SelectTemplateToProcess:
  "Select Template to Process"
  #-----------------------------------------------------------------------------------------------------------------
  def __init__( self, parent = None ):
    self.name = "Select Template to Process"
    self.parent = parent
    self.gparent = parent.parent
  #-----------------------------------------------------------------------------------------------------------------
  def execute( self ):
    for self.item in Globals( ).get_templates_list( ):
      self.gparent.parent.templateScrollAreaWidgetContents.addItem( self.item )
    self.gparent.parent.templateScrollAreaWidgetContents.sortItems( QtCore.Qt.AscendingOrder )
    self.gparent.parent.templateScrollAreaWidgetContents.itemClicked.connect(self.process_selected_template )
    return()
  #-----------------------------------------------------------------------------------------------------------------
  def process_selected_template( self ):
    self.gparent.tplseed_logger_message_signal.emit( "Processing the selected template." )
    return()
# -------------------------------------------------------------------------------------------------------------------
# Select Template Seed File to Process
# -------------------------------------------------------------------------------------------------------------------
class SelectTemplateSeedFileToProcess:
  "Select Template to Process"
  # -----------------------------------------------------------------------------------------------------------------
  def __init__( self, parent = None ):
    self.name = "Select Template Seed File to Process"
    self.parent = parent
    self.gparent = parent.parent
  # -----------------------------------------------------------------------------------------------------------------
  def execute( self, parent = None ):
    for self.item in Globals( ).get_templates_list( ):
      self.gparent.seed_logger_message_signal.emit( self.item )

    return ()
# -------------------------------------------------------------------------------------------------------------------
# Build Master Seed Files
# -------------------------------------------------------------------------------------------------------------------
class BuildMasterSeedFiles:
  "Build Master Seed Files"
  # -----------------------------------------------------------------------------------------------------------------
  def __init__( self, parent = None ):
    self.name = "Build Master Seed Files"
    self.parent = parent
    self.gparent = parent.parent
  # -----------------------------------------------------------------------------------------------------------------
  def execute( self, parent = None ):
    self.gparent.tplseed_logger_message_signal.emit( "Building Master Seed File." )
    return ()


#-------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------
  def build_master_seed( self ):
    self.parent.simulator_message_signal.emit("Simulator has run dude!!!!!!!!!!!!!!!!!!!!!!!!!")
    self.parent.logger_message_signal.emit("Simulator BUMMER AN ERROR DUDE!!!!!!!!!!!!!!!!!!!!!!!!!")
    return()
  #-----------------------------------------------------------------------------------------------------------------
  def select_template_seed_file(self):
    if not Globals.template_seed_selections_listed:
      if not self.istemplate:
        # if not Globals.templates_selections_listed:
        self.TestbedTesterListWindow.clear()
        Globals().clear_template_seed_list()
        Globals().clear_template_seed_to_be_built_list()
        self.reportScrollAreaWidgetContents.append("Selecting template seed file to use:")
        # ?? BuildTemplateSeedFilesList(). \
        # ??   build_template_seed_files_list(ProfilesPathDialog())
        for item in Globals().get_template_seed_list():
          self.TestbedTesterListWindow.addItem(item)
          self.TestbedTesterListWindow.sortItems(QtCore.Qt.AscendingOrder)
        self.TestbedTesterListWindow.itemClicked.connect(self.template_seed_files_to_be_built)
        Globals.template_seed_selections_listed = True
        self.istemplateseed = True
        # try:
        #   self.actionSelect_Template_Seed.triggered.disconnect( self.select_template_seed_file )
        # except:
        #   pass
        # try:
        #   self.actionSelect_Templates.triggered.disconnect( self.select_templates )
        # except:
        #   pass
        try:
          self.TestbedTesterListWindow.itemClicked.disconnect(self.templates_to_be_built)
        except:
          pass
    return ()
  #-----------------------------------------------------------------------------------------------------------------
  #-----------------------------------------------------------------------------------------------------------------
  def template_seed_files_to_be_built(self, template_seed_files):
    Globals().template_seed_files_to_be_built_list.append(template_seed_files.text())
    self.reportScrollAreaWidgetContents.append(template_seed_files.text())
    self.TestbedTesterListWindow.itemClicked.disconnect(self.template_seed_files_to_be_built)
    # Globals.template_seed_selections_listed = False
    # self.actionSelect_Template_Seed.triggered.connect( self.select_templates )
    self.istemplateseed = False
    try:
      self.TestbedTesterListWindow.itemClicked.connect(self.templates_to_be_built)
    except:
      pass
    return ()
  #-----------------------------------------------------------------------------------------------------------------
  #-----------------------------------------------------------------------------------------------------------------
  def build_master_seed_files(self):
    self.templates = []
    self.seeds = []
    for item in Globals().get_template_seed_files_to_be_built_list():
      # FIXME make debug self.reportScrollAreaWidgetContents.append( item )
      self.seeds.append(item)
    for item in Globals().get_templates_to_be_built_list():
      # FIXME make debug self.reportScrollAreaWidgetContents.append( item )
      self.templates.append(item)
    if self.templates and self.seeds:
      self.TestbedTesterListWindow.clear()
      self.reportScrollAreaWidgetContents.append("Build Master Seed Files:")
      Globals.template_seed_selections_listed = False
      Globals.templates_selections_listed = False
      self.istemplate = False
      self.istemplateseed = False
      # self.actionSelect_Templates.triggered.connect( self.select_templates )
      # self.actionSelect_Template_Seed.triggered.connect( self.select_template_seed_file )
    else:
      self.reportScrollAreaWidgetContents.append("Master seed build ignored, missing template or seed files.")
    return ()
  #-----------------------------------------------------------------------------------------------------------------
  #-----------------------------------------------------------------------------------------------------------------
  def select_templates(self):
    if not Globals.templates_selections_listed:
      if not self.istemplateseed:
        # if not Globals.template_seed_selections_listed:
        self.TestbedTesterListWindow.clear()
        Globals().clear_templates_list()
        Globals().clear_templates_to_be_built_list()
        self.reportScrollAreaWidgetContents.append("Selecting template file to use:")
        # ?? BuildTemplatesList().build_templates_list(ProfilesPathDialog())
        for item in Globals().get_templates_list():
          self.TestbedTesterListWindow.addItem(item)
          self.TestbedTesterListWindow.sortItems(QtCore.Qt.AscendingOrder)
        self.TestbedTesterListWindow.itemClicked.connect(self.templates_to_be_built)
        Globals.templates_selections_listed = True
        self.istemplate = True
        # try:
        #   self.actionSelect_Templates.triggered.disconnect( self.select_templates )
        # except:
        #   pass
        # try:
        #   self.actionSelect_Template_Seed.triggered.disconnect( self.select_template_seed_file )
        # except:
        #   pass
        try:
          self.TestbedTesterListWindow.itemClicked.disconnect(self.template_seed_files_to_be_built)
        except:
          pass
    return ()
  #-----------------------------------------------------------------------------------------------------------------
  #-----------------------------------------------------------------------------------------------------------------
  def templates_to_be_built(self, template):
    Globals().templates_to_be_built_list.append(template.text())
    self.reportScrollAreaWidgetContents.append(template.text())
    self.TestbedTesterListWindow.itemClicked.disconnect(self.templates_to_be_built)
    # Globals.templates_selections_listed = False
    # self.actionSelect_Template_Seed.triggered.connect( self.select_template_seed_file )
    self.istemplate = False
    try:
      self.TestbedTesterListWindow.itemClicked.connect(self.template_seed_files_to_be_built)
    except:
      pass
    return ()
######################################################################################################################