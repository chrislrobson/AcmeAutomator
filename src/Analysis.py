"""****************************************************************************************
TestbedTester Analysis
MODULE:   Analysis
Author: Christopher Robson
Copyright by:  Christopher Robson
Copyright date: 01Jan2016
This software is not FREE!  Use or destribution of the software system and its
subsystem modules, libraries, configuration file and "seed" file without the
express permission of the author is strictly PROHIBITED!
FUNCTION:  Module analysis report data from network devices
***************************************************************************************"""
"""
Python Linraries
"""
import datetime
"""
TestbedTester Libraries and classes
"""
from Globals import *
from CallClass import CallClass
"""
CLASS: analysis
FUNCTION: Calls classes which perform analysis of show data
INPUT:
OUTPUT:
"""
class Analysis:
    "Analysis"
    """"""
    def __init__( self, parent = None ):
        self.name = self.__class__.__name__
        self.parent = parent
        self.ip = parent.parent.ip
        self.ssh_handle = parent.parent.ssh_handle
        self.analysis_results = self.parent.parent.analysis_results
        self.report_file_list = self.parent.parent.report_file_list
        self.logger_message_signal = None
    """"""
    def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
        self.analysis_dict = dictionary
        """
         Start by initializing the prompt string processor object if its provided.  This object is used to scan each
         data received buffer for a session terminating string from a session transmitted command to a device.
         Typically, this key/value pair are not used but when logging into a base ssytem (aka linux for example)
         running a subsystem application (such as FFRouting) and the subsystems commandline processes is to be
         executed, the reply message's prompt may change.  Therefore, the user needs to provide that string in the
         seed file for addition to the the reply list named "prompt" in the file "RecievedDataReplyDictionary.py"
         """
        try:
            self.dictionary['processreply'].set_prompt_string(self.dictionary['prompt'], "Continue")
        except:
            pass
        """
        Extract the class to call and the associated dictionary
        """
        self.analysis_class = list( self.analysis_dict.keys() )[0]
        self.dictionary = list( self.analysis_dict.values() )[0]
        self.logger_message_signal = self.dictionary['loggerwidget']
        if self.dictionary['verbose']:
            self.message = "Analysis command started at: {}.".format( datetime.datetime.now().strftime( "%d%b%Y-%H%M-%S" ) )
            self.dictionary['loggerwidget'].emit(self.message)
        try:
            return(CallClass(self).call_class(module_name = self.analysis_class, class_name = self.analysis_class, method_name = "execute", dictionary = self.dictionary))
        except Exception as error:
            if error.args:
                self.message = "{{{}ANALYSIS: File I/O error with {} error reported: {}{}}}".format(Globals.RED_MESSAGE, self.analysis_class, error.args[0],Globals.SPAN_END_MESSAGE )
                self.dictionary['loggerwidget'].emit( self.message )
            raise Exception
"""****************************************************************************************************************
END of FILE
****************************************************************************************************************"""
