"""***************************************************************************************************************
FILE: StyleSheet
MODULE:   StyleSheet
Author: Christopher Robson
Copyright by:  Christopher Robson
Copyright date: 01Jan2016
This software is not FREE!  Use or destribution of the software system and its
subsystem modules, libraries, configuration file and "seed" file without the
express permission of the author is strictly PROHIBITED!
FUNCTION:  Class provides style sheets
Return:  Returns stylesheets
***************************************************************************************************************"""
"""
Python Libraries
"""
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QFile, QTextStream, QFileInfo
"""
CLASS: StyleSheet
DESCRIPTION:  Style sheet processor
INPUT: Stylesheet to use
OUTPUT: Stylesheet
"""
class StyleSheet:
    "Style Sheet"
    """"""
    def __init__(self, parent = None):
      self.name = self.__class__.__name__
      self.parent = parent
    """"""
    def get(self, stylesheet = None):
        self.stylesheet = "{}/{}".format(self.parent.stylesheethome, stylesheet)
        if (QFileInfo.exists(self.stylesheet)):
            self.file_descriptor = QFile(self.stylesheet)
            self.file_descriptor.open(QFile.ReadOnly | QFile.Text)
            self.stylesheet_data = QTextStream(self.file_descriptor).readAll()
            self.file_descriptor.close()
            return(self.stylesheet_data)
        else:
            raise Exception("{}: {} not found.".format(self.name, self.stylesheet))
"""********************************************************************************************************************
End of File
********************************************************************************************************************"""
