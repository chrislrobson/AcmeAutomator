#!/usr/bin/python
#####################################################################################################################
# Python Qt5 Testbed Tester GUI Seed File Builder
# Author: Christopher Robson
# Copyright by:  Christopher Robson
# Copyright date: 01Jan2016
# This software is not FREE!  Use or destribution of the software system and its
# subsystem modules, libraries, configuration file and "seed" file without the
# express permission of the author is strictly PROHIBITED!
# FUNCTION:  Main GUI interface and processing for the Seed File Building process.
# Developed from QT-Designer, PCUIC4( 5 ) and then heavely modified.
#####################################################################################################################
#--------------------------------------------------------------------------------------------------------------------
# PyQt5 Libraries
#--------------------------------------------------------------------------------------------------------------------
from PyQt5 import QtCore, QtGui, QtWidgets
#--------------------------------------------------------------------------------------------------------------------
# Home Grown
#--------------------------------------------------------------------------------------------------------------------
class GUISeedFileBuilderMainWindow( object ):
  "GUI Seed File Builder Main Window"
  #------------------------------------------------------------------------------------------------------------------
  def __init__( self ):
    self.name = "GUI Seed File Builder Main Window"
  #------------------------------------------------------------------------------------------------------------------
  def setupGUI( self, SeedFileBuilderMainWindow ):
    SeedFileBuilderMainWindow.setObjectName( "SeedFileBuilderMainWindow" )
    SeedFileBuilderMainWindow.resize( 852, 1066 )
    self.centralwidget = QtWidgets.QWidget( SeedFileBuilderMainWindow )
    self.centralwidget.setObjectName( "centralwidget" )
    #----------------------------------------------------------------------------------------------------------------
    self.template_ListWidget = QtWidgets.QListWidget( self.centralwidget )
    self.template_ListWidget.setGeometry( QtCore.QRect( 10, 60, 411, 761 ) )
    self.template_ListWidget.setLineWidth(2)
    self.template_ListWidget.setAcceptDrops( True )
    self.template_ListWidget.setAutoFillBackground( False )
    self.template_ListWidget.setVerticalScrollBarPolicy( QtCore.Qt.ScrollBarAlwaysOn )
    self.template_ListWidget.setSizeAdjustPolicy( QtWidgets.QAbstractScrollArea.AdjustToContents )
    self.template_ListWidget.setEditTriggers( QtWidgets.QAbstractItemView.SelectedClicked )
    self.template_ListWidget.setProperty( "isWrapping", False )
    self.template_ListWidget.setResizeMode( QtWidgets.QListView.Adjust )
    self.template_ListWidget.setWordWrap( False )
    self.template_ListWidget.setObjectName( "templateListWidget" )
    font = QtGui.QFont()
    font.setFamily("DejaVu Serif")
    font.setPointSize(28)
    font.setBold(True)
    font.setWeight(75)
    self.template_label = QtWidgets.QLabel( self.centralwidget )
    self.template_label.setGeometry( QtCore.QRect( 20, 10, 381, 41 ) )
    self.template_label.setFont(font)
    self.template_label.setObjectName("templatelabel")
    #----------------------------------------------------------------------------------------------------------------
    self.seed_ListWidget = QtWidgets.QListWidget( self.centralwidget )
    self.seed_ListWidget.setGeometry( QtCore.QRect( 430, 60, 411, 761 ) )
    self.seed_ListWidget.setAcceptDrops( True )
    self.seed_ListWidget.setAutoFillBackground( False )
    self.seed_ListWidget.setVerticalScrollBarPolicy( QtCore.Qt.ScrollBarAlwaysOn )
    self.seed_ListWidget.setSizeAdjustPolicy( QtWidgets.QAbstractScrollArea.AdjustToContents )
    self.seed_ListWidget.setEditTriggers( QtWidgets.QAbstractItemView.SelectedClicked )
    self.seed_ListWidget.setProperty( "isWrapping", False )
    self.seed_ListWidget.setResizeMode( QtWidgets.QListView.Adjust )
    self.seed_ListWidget.setWordWrap( False )
    self.seed_ListWidget.setObjectName( "seedListWidget" )
    self.seed_label = QtWidgets.QLabel( self.centralwidget )
    self.seed_label.setGeometry( QtCore.QRect( 480, 10, 291, 41 ) )
    font = QtGui.QFont(  )
    font.setFamily( "DejaVu Serif" )
    font.setPointSize( 28 )
    font.setBold( True )
    font.setWeight( 75 )
    self.seed_label.setFont( font )
    self.seed_label.setObjectName( "seedlabel" )
    #----------------------------------------------------------------------------------------------------------------
    self.message_ListWidget = QtWidgets.QListWidget( self.centralwidget )
    self.message_ListWidget.setGeometry( QtCore.QRect( 10, 860, 831, 161 ) )
    self.message_ListWidget.setAcceptDrops( True )
    self.message_ListWidget.setAutoFillBackground( False )
    self.message_ListWidget.setVerticalScrollBarPolicy( QtCore.Qt.ScrollBarAlwaysOn )
    self.message_ListWidget.setSizeAdjustPolicy( QtWidgets.QAbstractScrollArea.AdjustToContents )
    self.message_ListWidget.setEditTriggers( QtWidgets.QAbstractItemView.SelectedClicked )
    self.message_ListWidget.setProperty( "isWrapping", False )
    self.message_ListWidget.setResizeMode( QtWidgets.QListView.Adjust )
    self.message_ListWidget.setWordWrap( False )
    self.message_ListWidget.setObjectName( "messageListWidget" )
    self.message_label = QtWidgets.QLabel( self.centralwidget )
    self.message_label.setGeometry( QtCore.QRect( 150, 820, 101, 41 ) )
    font = QtGui.QFont(  )
    font.setFamily( "Waree" )
    font.setPointSize( 16 )
    font.setBold( True )
    font.setWeight( 75 )
    self.message_label.setFont( font )
    self.message_label.setObjectName( "messagelabel" )
    #----------------------------------------------------------------------------------------------------------------
    SeedFileBuilderMainWindow.setCentralWidget( self.centralwidget )
    self.statusbar = QtWidgets.QStatusBar( SeedFileBuilderMainWindow )
    self.statusbar.setObjectName( "statusbar" )
    SeedFileBuilderMainWindow.setStatusBar( self.statusbar )
    self.menubar = QtWidgets.QMenuBar( SeedFileBuilderMainWindow )
    self.menubar.setGeometry( QtCore.QRect( 0, 0, 852, 20 ) )
    self.menubar.setObjectName( "menubar" )
    self.menuFile = QtWidgets.QMenu( self.menubar )
    self.menuFile.setObjectName( "menuFile" )
    self.menuConfiguration = QtWidgets.QMenu( self.menubar )
    self.menuConfiguration.setObjectName( "menuConfiguration" )
    self.menuHelp = QtWidgets.QMenu( self.menubar )
    self.menuHelp.setObjectName( "menuHelp" )
    #----------------------------------------------------------------------------------------------------------------
    SeedFileBuilderMainWindow.setMenuBar( self.menubar )
    self.actionPrintFiles = QtWidgets.QAction(SeedFileBuilderMainWindow)
    self.actionPrintFiles.setObjectName("actionPrintFiles")
    self.actionListTemplateFiles = QtWidgets.QAction( SeedFileBuilderMainWindow )
    self.actionListTemplateFiles.setObjectName( "actionListTemplateFiles" )
    self.actionListSeedFiles = QtWidgets.QAction( SeedFileBuilderMainWindow )
    self.actionListSeedFiles.setObjectName( "actionListSeedFiles" )
    self.actionExit = QtWidgets.QAction( SeedFileBuilderMainWindow )
    self.actionExit.setObjectName( "actionExit" )
    self.actionBuild_Seed_Files = QtWidgets.QAction( SeedFileBuilderMainWindow )
    self.actionBuild_Seed_Files.setObjectName( "actionBuild_Seed_Files" )
    self.actionBuild_IP_Address_List = QtWidgets.QAction(SeedFileBuilderMainWindow)
    self.actionBuild_IP_Address_List.setObjectName("actionBuild_IP_Address_List")
    self.actionAbout = QtWidgets.QAction( SeedFileBuilderMainWindow )
    self.actionAbout.setObjectName( "actionAbout" )
    self.menuFile.addSeparator(  )
    self.menuFile.addAction( self.actionListTemplateFiles )
    self.menuFile.addSeparator(  )
    self.menuFile.addAction( self.actionListSeedFiles )
    self.menuFile.addSeparator(  )
    self.menuFile.addAction(self.actionPrintFiles)
    self.menuFile.addSeparator()
    self.menuFile.addAction( self.actionExit )
    self.menuConfiguration.addSeparator()
    self.menuConfiguration.addAction(self.actionBuild_IP_Address_List)
    self.menuConfiguration.addSeparator()
    self.menuConfiguration.addAction(self.actionBuild_Seed_Files)
    self.menuHelp.addSeparator()
    self.menuHelp.addAction( self.actionAbout )
    self.menubar.addAction( self.menuFile.menuAction(  ) )
    self.menubar.addAction( self.menuConfiguration.menuAction(  ) )
    self.menubar.addAction( self.menuHelp.menuAction(  ) )
    self.retranslateGUI( SeedFileBuilderMainWindow )
    QtCore.QMetaObject.connectSlotsByName( SeedFileBuilderMainWindow )
    return(  )
  #---------------------------------------------------------------------------------------------------------------
  def retranslateGUI( self, SeedFileBuilderMainWindow ):
    _translate = QtCore.QCoreApplication.translate
    SeedFileBuilderMainWindow.setWindowTitle( _translate( "SeedFileBuilderMainWindow", "Seed File Builder" ) )
    self.template_ListWidget.setSortingEnabled( True )
    self.seed_ListWidget.setSortingEnabled( True )
    self.template_label.setText( _translate( "SeedFileBuilderMainWindow", "Template File List" ) )
    self.seed_label.setText( _translate( "SeedFileBuilderMainWindow", "Seed File List" ) )
    self.message_label.setText( _translate( "SeedFileBuilderMainWindow", "Messages" ) )
    self.menuFile.setTitle( _translate( "SeedFileBuilderMainWindow", "file" ) )
    self.menuConfiguration.setTitle( _translate( "SeedFileBuilderMainWindow", "Configuration" ) )
    self.menuHelp.setTitle( _translate( "SeedFileBuilderMainWindow", "Help" ) )
    self.actionListTemplateFiles.setText( _translate( "SeedFileBuilderMainWindow", "List Template Files" ) )
    self.actionListSeedFiles.setText( _translate( "SeedFileBuilderMainWindow", "List Seed Files" ) )
    self.actionPrintFiles.setText( _translate( "SeedFileBuilderMainWindow", "Print Files" ) )
    self.actionExit.setText( _translate( "SeedFileBuilderMainWindow", "Exit" ) )
    self.actionBuild_Seed_Files.setText( _translate( "SeedFileBuilderMainWindow", "Build Seed Files" ) )
    self.actionBuild_IP_Address_List.setText( _translate( "SeedFileBuilderMainWindow", "Build IP Address List" ) )
    self.actionAbout.setText( _translate( "SeedFileBuilderMainWindow", "About" ) )
    return(  )
#####################################################################################################################

