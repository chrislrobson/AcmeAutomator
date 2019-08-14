"""*******************************************************************************************
* FILE: CallClass
* PROJECT: DataCollectionAnalysisReportingAutomation
* CLASS(s): CallClass
* MEMBER(s):
* AUTHOR: Christopher L. Robson (UID): 
* DATE: 9/23/18 TIME: 09:30:00
* COPYRIGHT (c): 9/23/18 Christopher L. Robson. All rights reserved.
*                This software is not FREE!  Use or destribution of the software system
*                and its subsystem modules, libraries, configuration file and "seed" file
*                without the express permission of the author is strictly PROHIBITED!
* DESCRIPTION: This class is called to build a dynamic function call.
*              The module "MUST" contain a Class name Exactly named after the module name,
*              for example:  module: "FooBar.py" must have the class "class FooBar:" defined.
*              The calling program can either provide the method to execute or use the default.
*              Calling classes are required to call this class with try/except to catch errors
*******************************************************************************************"""
"""
System libraires
"""
import importlib
"""
Home grown libraires
"""
from Globals import *
"""
CLASS: CallClass
METHOD: CallClass
DESCRIPTION: Calls a class created from a passed keyword string
INPUT: Module/Class/Method[optional]/Arguments[optional]
OUTPUT: Returns of function call or try/exception errors
"""

class CallClass():
  "Call Class"

  def __init__(self, parent = None):
    super(CallClass, self).__init__()
    self.name = self.__class__.__name__
    self.parent = parent

  def call_class(self, module_name = "", class_name = "", method_name = "execute", dictionary = None, data = None, decode = None, descriptor = None):
    self.module_name = module_name
    self.class_name = class_name
    self.method_name = method_name
    self.dictionary = dictionary
    self.data = data
    self.decode = decode
    self.descriptor = descriptor
    try:
      self.module = importlib.import_module(self.module_name)
      self.module_class = getattr( self.module, self.class_name)
      self.class_address = self.module_class(self.parent)               # notes call class but pass the caller's reference pointer
      self.class_method = getattr(self.class_address, self.method_name)
      return(self.class_method(dictionary = self.dictionary, descriptor = self.descriptor, data = self.data, decode = self.decode))
    except Exception as error:
      if error.args:
        self.message = "{{{}CallClass({}): {}{}}}".format(Globals.RED_MESSAGE, self.class_name, error.args[0], Globals.SPAN_END_MESSAGE)
        try:
          # notes "logger_message_signal" has to come from the parent because not all parents pass a dictionary thru CallClass
          self.parent.logger_message_signal.emit(self.message)
        except Exception as error:
          self.message = "{{{}{} logger EMIT error: {}{}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
          raise Exception(self.message)
      raise Exception

"""*******************************************************************************************
End of CallClass
*******************************************************************************************"""