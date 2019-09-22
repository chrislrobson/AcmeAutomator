"""********************************************************************************************
Seed Commandline Preprocessor
MODULE:  SeedCommandLinePreprocessor
Author: Christopher Robson
Copyright by:  Christopher Robson
Copyright date: 01Jan2016
This software is not FREE!  Use or destribution of the software system and its
subsystem modules, libraries, configuration file and "seed" file without the
express permission of the author is strictly PROHIBITED!
FUNCTION:  Module decodes the string looking for starting comment character or sleep function
*********************************************************************************************"""
"""
System libraries
"""
import time
"""
Home grown libraries
"""
from PauseButtonControl import PauseButtonControl
"""
CLASS: Seed Command Line Processor
DESCRIPTION: Determines if string line has control characters such as comment character or sleep function call
INPUT: String to process
OUTPUT: True if line is to be processed or False if line is commented or sleep function
"""
class SeedCommandlinePreprocessor():
    "Seed Commandline Preprocessor"
    """"""
    def __init__(self, parent=None):
        self.name = self.__class__.__name__
        self.parent = parent
    """"""
    def preprocessor(self, message_signal = None, data = None):
        self.data = data
        self.logger_message_signal = message_signal
        """
        Special AcmeAutomator directives MUST be first or they are processes as a comment
        """
        if self.data.startswith("#@@!!sleep "):
            self.logger_message_signal.emit("Operating System sleep issued for {} seconds".format(self.data.split()[1]))
            time.sleep(int(float(self.data.split()[1])))
            return( False )
        elif self.data.startswith("#@@!!prompt "):
            self.new_prompt = self.data.split()[1].split('\n')[0]
            self.parent.dictionary['processreply'].set_prompt_string(self.new_prompt, "Continue")
            return (False)
        elif self.data.startswith("#@@!!pause"):
            try:
                PauseButtonControl(self).pause_system()
            except Exception as error:
                self.logger_message_signal.emit(str(error))
                raise Exception
            return( False )
        elif  self.data.startswith('{\n') or self.data.startswith('}\n') or \
                self.data.startswith('\r\n'):
            return( False )
        elif self.data.startswith("#"):
            return( False )
        elif self.data.startswith("!"):
            return( False )
        elif self.data.startswith("\n"):
            return( False )
        return( True )
    """"""
    def iscommented(self, data = None):
        self.data = data
        if  self.data.startswith('{\n') or self.data.startswith('}\n') or self.data.startswith('\r\n'):
            return( False )
        elif self.data.startswith("#"):
            return( False )
        elif self.data.startswith("!"):
            return( False )
        elif self.data.startswith("\n"):
            return( False )
        return( True )
"""
End of File
"""