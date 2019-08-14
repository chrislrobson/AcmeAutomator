"""********************************************************************************************************
Process ProcessReply
MODULE:  ProcessReply (C)
Author: Christopher Robson
Copyright by:  Christopher Robson
Copyright date: 01Jan2016
!!!!!!!!!!!!!!! COPYRIGHT WARNING !!!!!!!!!!!!!!!!!!
THIS CLASS IS PRIVATELY OWNED AND MAY NOT BE REUSED BY ANYONE BUT THE AUTHOR
While the author has obviously no time to review every single Python program on the Internet,
to date nothing has been found resembling the technic and more specifically the extent of
typical network device responses collected included wihtin this system.  The network device
response message strings used to create the "prompt" list in file ReceivedDataReplyDictionary.py
have NOT been taken from any vendor's properity specification but collected through pain stacking
device "black box" quering and testing, thus, contributing to the copyright nature of this Python
file and associated Python/Data files.
This software is not FREE!  Use or destribution of the software system and its
subsystem modules, libraries, configuration file and "seed" file without the
express permission of the author is strictly PROHIBITED!
FUNCTION:  Module processes replies issued to the network device.  It is called when a block of data
           is received from the device.  Its calls class associated to prompt string to determine what
           prompt string has been returned from the network device.  The prompt string determines the
           response action to take when processing the received block of data such as replying with the
           correct password string.
RETURN:  True if message replies are successful otherwise False:
********************************************************************************************************"""
"""
Python libraires
"""
import importlib
import time
import re
"""
Home grown libraires
"""
from Globals import *
from Exceptions import *
from SSHChannelProcessor import SendDataThroughSSHChannel
from CallClass import CallClass
"""
CLASS: SendYes
DESCRIPTION: Responses to any yes/no queries
INPUT: Received data
OUTPUT: Errors cause exceptions
"""
class SendYes(MyExceptions):
  "Send Yes"
  """"""
  def __init__(self, parent = None):
    self.name = self.__class__.__name__
    self.parent = parent
    self.ssh_handle = parent.ssh_handle
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dictionary = dictionary
    self.received_data = data
    try:
      self.received_data = SendDataThroughSSHChannel(self).send_data_through_ssh_channel(dictionary = self.dictionary, data = "yes\n")
      if self.dictionary['verbose']:
        self.message = "{{YES sent to DUT.\n"
        self.message += "{}".format(self.received_data)
        self.dictionary['loggerwidget'].emit(self.message)
      self.reply_action = self.dictionary['processreply'].find_prompt(self.received_data, self.dictionary['processreply'].prompt_automaton)
      for self.action_type in self.reply_action:
        if not "Continue" in self.action_type:
          self.reply = self.action_type[1]
          break
      else:
        self.reply = self.action_type[1]
      try:
        self.results = CallClass(self).call_class(module_name = "ProcessReply", class_name = self.reply,
                                                  method_name = "execute", dictionary = self.dictionary, data = self.received_data)
      except Exception as error:
        self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
        self.dictionary['loggerwidget'].emit(self.message)
        raise Exception
    except Exception as error:
      self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
      self.dictionary['loggerwidget'].emit(self.message)
      raise Exception
    return()
"""
CLASS: SendNo
DESCRIPTION: Send no, typically used to terminate configuration failures
INPUT: Received data
OUTPUT: Errors cause exceptions
"""
class SendNo(MyExceptions):
  "Send No"
  """"""
  def __init__(self, parent = None):
    self.name = self.__class__.__name__
    self.parent = parent
    self.ssh_handle = parent.ssh_handle
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dictionary = dictionary
    self.received_data = data
    try:
      try:
       self.received_data = SendDataThroughSSHChannel(self).send_data_through_ssh_channel(dictionary = self.dictionary, data = "no\n")
      except Exception as error:
        print(error)
      if self.dictionary['verbose']:
        self.message = "NO sent to DUT.\n{}".format(self.received_data)
        self.dictionary['loggerwidget'].emit(self.message)
      self.reply_action = self.dictionary['processreply'].scan_reply(self.received_data, self.dictionary['processreply'].prompt_automaton)
      for self.action_type in self.reply_action:
        if not "Continue" in self.action_type:
          self.reply = self.action_type[1]
          break
      else:
        """
        No WAS set up to catch any following commits the enegineer has in the seed file.  Answer "no" so the
        original configuration is not whipped out.  AKA, another crappy F'ed up Cisco code logic.
        After answering "no", program resets the "Do you wish to proceed to the default "yes"
        """
        if "Continue" in self.action_type:
          self.reply_action = self.dictionary['processreply'].set_prompt_string("Do you wish to proceed? [no]:", "SendYes")
        self.reply = self.action_type[1]
      try:
        self.results = CallClass(self).call_class(module_name = "ProcessReply", class_name = self.reply,
                                                  method_name = "execute", dictionary = self.dictionary, data = self.received_data)
      except Exception as error:
        self.message = "{{{}{}: {}{}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
        self.dictionary['loggerwidget'].emit(self.message)
        raise Exception
    except Exception as error:
      self.message = "{{{}{}: {}{}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
      self.dictionary['loggerwidget'].emit(self.message)
      raise Exception
    return ()
"""
CLASS: SendClear
DESCRIPTION: Clears any failed configuration attempts
INPUT: Received data
OUTPUT: Excpetion is generated to terminate command
"""
class SendClear(MyExceptions):
  "Send Clear"
  """"""
  def __init__(self, parent=None):
    self.name = self.__class__.__name__
    self.parent = parent
    self.ssh_handle = parent.ssh_handle
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dictionary = dictionary
    self.received_data = data
    try:
      self.received_data = ""
      self.received_data = \
        SendDataThroughSSHChannel(self).send_data_through_ssh_channel(dictionary = self.dictionary, data = "clear\n")
      if self.dictionary['verbose']:
        self.message = "Clear sent to DUT.\n{}".format(self.received_data)
        self.dictionary['loggerwidget'].emit(self.message)
      self.reply_action = self.dictionary['processreply'].scan_reply(self.received_data, self.dictionary['processreply'].prompt_automaton)
      for self.action_type in self.reply_action:
        if not "Continue" in self.action_type:
          self.reply = self.action_type[1]
          break
      else:
        """
        No set up to catch any following commits the enegineer has in the seed file.  Answer "no" so the
        original configuration is not whipped out.  AKA, another crappy Cisco code logic.
        After answering "no", program resets the "Do you wish to proceed to the default "yes"
        """
        if "Continue" in self.action_type:
          self.reply_action = self.dictionary['processreply'].set_prompt_string("Do you wish to proceed? [no]:", "SendNo")
        self.reply = self.action_type[1]
      try:
        self.results = CallClass(self).call_class(module_name = "ProcessReply", class_name = self.reply,
                                                  method_name = "execute", dictionary = self.dictionary, data = self.received_data)
      except Exception as error:
        self.message = "{{{}{}: {}{}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
        self.dictionary['loggerwidget'].emit(self.message)
        raise Exception
    except Exception as error:
      self.message = "{{{}{}: {}{}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
      self.dictionary['loggerwidget'].emit(self.message)
      raise Exception
    self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, "A CLEAR was sent to DUT must terminate process!", Globals.SPAN_END_MESSAGE)
    self.dictionary['loggerwidget'].emit(self.message)
    raise Exception
"""
CLASS: SendConfigurationFailed
DESCRIPTION: 
INPUT: 
OUTPUT: 
"""
class SendConfigurationFailed(MyExceptions):
  "Send Configuration Failed"
  """"""
  def __init__(self, parent=None):
    self.name = self.__class__.__name__
    self.parent = parent
    self.ssh_handle = parent.ssh_handle
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dictionary = dictionary
    self.received_data = data
    self.show_failed = re.compile("show configuration failed load")
    if self.show_failed.search(self.received_data):
      self.send_message = "show configuration failed load detail\n"
    else:
      self.send_message = "show configuration failed inheritance\n"
    try:
      self.received_data = ""
      self.received_data = SendDataThroughSSHChannel(self).send_data_through_ssh_channel(dictionary = self.dictionary, data = self.send_message)
      if self.dictionary['verbose']:
        self.message = "show configuration failed\" sent to DUT. Error returned is:\n{}".format(self.received_data)
        self.dictionary['loggerwidget'].emit(self.message)
      self.received_data = SendDataThroughSSHChannel(self).send_data_through_ssh_channel(dictionary = self.dictionary, data = "clear\n")
      if self.dictionary['verbose']:
        self.message = "Clear sent to DUT.\n{}".format(self.received_data)
        self.dictionary['loggerwidget'].emit(self.message)
      self.reply_action = self.dictionary['processreply'].scan_reply(self.received_data, self.dictionary['processreply'].prompt_automaton)
      for self.action_type in self.reply_action:
        if not "Continue" in self.action_type:
          self.reply = self.action_type[1]
          break
      else:
        """
        No set up to catch any following commits the enegineer has in the seed file.  Answer "no" so the
        original configuration is not whipped out.  AKA, another crappy Cisco code logic.
        After answering "no", program resets the "Do you wish to proceed to the default "yes"
        """
        if "Continue" in self.action_type:
          self.reply_action = self.dictionary['processreply'].set_prompt_string("Do you wish to proceed? [no]:", "SendNo")
        self.reply = self.action_type[1]
      try:
        self.results = CallClass(self).call_class(module_name = "ProcessReply", class_name = self.reply,
                                                  method_name = "execute", dictionary = self.dictionary, data = self.received_data)
      except Exception as error:
        self.message = "{{{}{}: {}{}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
        self.dictionary['loggerwidget'].emit(self.message)
        raise Exception
    except Exception as error:
      self.message = "{{{}{}: {}{}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
      self.dictionary['loggerwidget'].emit(self.message)
      raise Exception
    self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, "A CLEAR was sent to DUT must terminate process!", Globals.SPAN_END_MESSAGE)
    self.dictionary['loggerwidget'].emit(self.message)
    raise Exception
"""
CLASS: SendCtrlC
DESCRIPTION: Send Control-C to terminate current error state with device
INPUT: Received data
OUTPUT: Errors cause exceptions
"""
class SendCtrlC(MyExceptions):
  "Send CtrlC"
  """"""
  def __init__(self, parent=None):
    self.name = self.__class__.__name__
    self.parent = parent
    self.ssh_handle = parent.ssh_handle
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dictionary = dictionary
    self.received_data = data
    try:
      self.received_data = SendDataThroughSSHChannel(self).send_data_through_ssh_channel(dictionary = self.dictionary, data = "\x03\n")
      if self.dictionary['verbose']:
        self.message = "Control-C sent to DUT.\n{}".format(self.received_data)
        self.dictionary['loggerwidget'].emit(self.message)
      self.reply_action = self.dictionary['processreply'].scan_reply(self.received_data, self.dictionary['processreply'].prompt_automaton)
      for self.action_type in self.reply_action:
        if not "Continue" in self.action_type:
          self.reply = self.action_type[1]
          break
      else:
        self.reply = self.action_type[1]
      try:
        self.results = CallClass(self).call_class(module_name = "ProcessReply", class_name = self.reply,
                                                  method_name = "execute", dictionary = self.dictionary, data = self.received_data)
      except Exception as error:
        self.message = "{{{}{}: {}{}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
        self.dictionary['loggerwidget'].emit(self.message)
        raise Exception
    except Exception as error:
      self.message = "{{{}{}: {}{}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
      self.dictionary['loggerwidget'].emit(self.message)
      raise Exception
    return ()
"""
CLASS: SendPassword
DESCRIPTION: Sends password to device
INPUT: Password from seed file or user's default
OUTPUT: Permission denied cause exception error
"""
class SendPassword(MyExceptions):
  "Send Password"
  """"""
  def __init__(self, parent = None):
    self.name = self.__class__.__name__
    self.parent = parent
    self.ssh_handle = parent.ssh_handle
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dictionary = dictionary
    self.password = self.dictionary['pwd']
    self.received_data = data
    try:
      self.received_data = SendDataThroughSSHChannel(self).send_data_through_ssh_channel(dictionary = self.dictionary, data = self.password)
      if self.dictionary['verbose']:
        self.message = "Password {} sent to DUT.\n{}".format(self.password, self.received_data)
        self.dictionary['loggerwidget'].emit(self.message)
      self.reply_action = self.dictionary['processreply'].scan_reply(self.received_data, self.dictionary['processreply'].prompt_automaton)
      for self.action_type in self.reply_action:
        if not "Continue" in self.action_type:
          self.reply = self.action_type[1]
          break
      else:
        self.reply = self.action_type[1]
      try:
        self.results = CallClass(self).call_class(module_name = "ProcessReply", class_name = self.reply,
                                                  method_name = "execute", dictionary = self.dictionary, data = self.received_data)
      except Exception as error:
        if error.args:
          self.message = "{{{}{}: {}{}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
          self.dictionary['loggerwidget'].emit(self.message)
        raise Exception
    except Exception as error:
      if error.args:
        self.message = "{{{}{}: {}{}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
        self.dictionary['loggerwidget'].emit(self.message)
      raise Exception
    return ()
"""
CLASS: SendCarriageReturn
DESCRIPTION: Sends carriage return to prompted questions
INPUT: Received data
OUTPUT: Errors cause exception
"""
class SendCarriageReturn(MyExceptions):
  "Send Carriage Return"
  """"""
  def __init__(self, parent = None):
    self.name = self.__class__.__name__
    self.parent = parent
    self.ssh_handle = parent.ssh_handle
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dictionary = dictionary
    self.received_data = data
    try:
      self.received_data = SendDataThroughSSHChannel(self).send_data_through_ssh_channel(dictionary = self.dictionary, data = "\n", delay = self.dictionary['delay'])
      if self.dictionary['verbose']:
        self.message = "{}: Carriage return sent to DUT. ".format(self.name)
        self.message += "{}".format(self.received_data)
        self.dictionary['loggerwidget'].emit(self.message)
      self.reply_action = self.dictionary['processreply'].scan_reply(self.received_data, self.dictionary['processreply'].prompt_automaton)
      for self.action_type in self.reply_action:
        if not "Continue" in self.action_type:
          self.reply = self.action_type[1]
          break
      else:
        self.reply = self.action_type[1]
      try:
        self.results = CallClass(self).call_class(module_name = "ProcessReply", class_name = self.reply,
                                                  method_name = "execute", dictionary = self.dictionary, data = self.received_data)
        if self.dictionary['verbose'] and self.results:
          self.message = "{}".format(self.results)
          self.dictionary['loggerwidget'].emit(self.message)
      except Exception as error:
        self.message = "{{{}{}: {}{}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
        self.dictionary['loggerwidget'].emit(self.message)
        raise Exception
    except Exception as error:
      self.message = "{{{}{}: {}{}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
      self.dictionary['loggerwidget'].emit(self.message)
      raise Exception
    return()
"""
CLASS: SendReturn
DESCRIPTION: Sends return character only
INPUT: Recieved data
OUTPUT: Errors cause exception
"""
class SendReturn(MyExceptions):
  "Send Return"
  """"""
  def __init__(self, parent = None):
    self.name = self.__class__.__name__
    self.parent = parent
    self.ssh_handle = parent.ssh_handle
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dictionary = dictionary
    self.received_data = data
    try:
      self.received_data = SendDataThroughSSHChannel(self).send_data_through_ssh_channel(dictionary = self.dictionary, data = "\r")
      if self.dictionary['verbose']:
        self.message = "Return only sent to DUT.\n{}".format(self.received_data)
        self.dictionary['loggerwidget'].emit(self.message)
      self.reply_action = self.dictionary['processreply'].scan_reply(self.received_data, self.dictionary['processreply'].prompt_automaton)
      for self.action_type in self.reply_action:
        if not "Continue" in self.action_type:
          self.reply = self.action_type[1]
          break
      else:
        self.reply = self.action_type[1]
      try:
        self.results = CallClass(self).call_class(module_name = "ProcessReply", class_name = self.reply,
                                                  method_name = "execute", dictionary = self.dictionary, data = self.received_data)
      except Exception as error:
        self.message = "{{{}{}: {}{}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
        self.dictionary['loggerwidget'].emit(self.message)
        raise Exception
    except Exception as error:
      self.message = "{{{}{}: {}{}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
      self.dictionary['loggerwidget'].emit(self.message)
      raise Exception
    return ()
"""
CLASS: SendUsername
DESCRIPTION: TOBE COMPLETE~!!!!!!
INPUT: 
OUTPUT: 
"""
class SendUsername(MyExceptions):
  "Send Username"
  """"""
  def __init__(self, parent = None):
    self.name = self.__class__.__name__
    self.parent = parent
    self.ssh_handle = parent.ssh_handle
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dictionary = dictionary
    self.data = data
    try:
      self.received_data = SendDataThroughSSHChannel(self).send_data_through_ssh_channel(dictionary = self.dictionary, data = self.data)
      if self.dictionary['verbose']:
        self.message = "Username sent to DUT.\n{}".format(self.received_data)
        self.dictionary['loggerwidget'].emit(self.message)
      self.reply_action = self.dictionary['processreply'].scan_reply(self.received_data, self.dictionary['processreply'].prompt_automaton)
      for self.action_type in self.reply_action:
        if not "Continue" in self.action_type:
          self.reply = self.action_type[1]
          break
      else:
        self.reply = self.action_type[1]
      try:
        self.results = CallClass(self).call_class(module_name = "ProcessReply", class_name = self.reply,
                                                  method_name = "execute", dictionary = self.dictionary, data = self.received_data)
      except Exception as error:
        self.message = "{{{}{}: {}{}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
        self.dictionary['loggerwidget'].emit(self.message)
        raise Exception
    except Exception as error:
      self.message = "{{{}{}: {}{}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
      self.dictionary['loggerwidget'].emit(self.message)
      raise Exception
    return()
"""
CLASS: SendAbort
DESCRIPTION: Send abort, typically sent to cancel current configuration process
INPUT: Received data
OUTPUT: Forces excpetion to terminate current request.
"""
class SendAbort(MyExceptions):
  "Send Abort"
  """"""
  def __init__(self, parent = None):
    self.name = self.__class__.__name__
    self.parent = parent
    self.ssh_handle = parent.ssh_handle
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dictionary = dictionary
    self.received_data = data
    try:
      self.received_data = \
        SendDataThroughSSHChannel(self).send_data_through_ssh_channel(dictionary = self.dictionary, data = "abort\n")
      if self.dictionary['verbose']:
        self.message = "Abort sent to DUT.\n{}".format(self.received_data)
        self.dictionary['loggerwidget'].emit(self.message)
      self.reply_action = self.dictionary['processreply'].find_prompt(self.received_data, self.dictionary['processreply'].prompt_automaton)
      for self.action_type in self.reply_action:
        if not "Continue" in self.action_type:
          self.reply = self.action_type[1]
          break
      else:
        self.reply = self.action_type[1]
      try:
        self.results = CallClass(self).call_class(module_name = "ProcessReply", class_name = self.reply,
                                                  method_name = "execute", dictionary = self.dictionary, data = self.received_data)
      except Exception as error:
        self.message = "{{{}{}: {}{}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
        self.dictionary['loggerwidget'].emit(self.message)
        raise Exception
    except Exception as error:
      self.message = "{{{}{}: {}{}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
      self.dictionary['loggerwidget'].emit(self.message)
      raise Exception
    self.message = "{}: {}".format(Globals.RED_MESSAGE, self.name, "An abort was sent to DUT must terminate process!", Globals.SPAN_END_MESSAGE)
    self.dictionary['loggerwidget'].emit(self.message)
    raise Exception
"""
CLASS: Continue
DESCRIPTION: Does nothing, called typically to just finish out current request keyword processing actions
INPUT: Received data
OUTPUT: Nothing is returned
"""
class Continue:
  "Continue"
  """"""
  def __init__(self, parent = None):
    self.name = self.__class__.__name__
    self.parent = parent
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dictionary = dictionary
    self.data = data
    if self.dictionary['verbose'] and self.data:
      self.dictionary['loggerwidget'].emit(self.data)
    return()
"""
CLASS: IgnoreCommand
DESCRIPTION: Does nothing, called typically to just finish out current request keyword processing actions
INPUT: Received data
OUTPUT: Nothing is returned
"""
class IgnoreCommand:
  "Ignore Command"
  """"""
  def __init__(self, parent = None):
    self.name = self.__class__.__name__
    self.parent = parent
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.data = data
    self.dictionary = dictionary
    if self.dictionary['verbose'] and self.data:
      self.dictionary['loggerwidget'].emit(self.data)
    return()
"""
CLASS: ResolvingMaster
DESCRIPTION: Does nothing, called typically to just finish out current request keyword processing actions
INPUT: Received data
OUTPUT: Nothing is returned
"""
class ResolvingMaster:
  "Resolving Master"
  """"""
  def __init__(self, parent = None):
    self.name = self.__class__.__name__
    self.parent = parent
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.data = data
    self.dictionary = dictionary
    if self.dictionary['verbose'] and self.data:
      self.dictionary['loggerwidget'].emit(self.data)
    return()
"""
CLASS: WaitProcessor
DESCRIPTION: Called in response to device message "Not ready for mastership switch"
INPUT: Received data
OUTPUT: Raises the exception to retry request.
"""
class WaitProcessor(MyExceptions):
  "Wait Processor"
  """"""
  def __init__(self, parent = None):
    self.name = self.__class__.__name__
    self.parent = parent
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.data = data
    self.dictionary = dictionary
    self.seconds = ""
    if "try after" in self.data:
      self.first_aprt, self.seconds_str = self.data.split("try after", 1)
      self.seconds = self.seconds_str.split()[0]
    if not self.seconds.isdigit():
      self.seconds = "240"
    self.seconds_int = int(float(self.seconds))
    if self.dictionary['verbose']:
      self.message = "Waiting for {} seconds before retrying.".format(self.seconds)
      self.dictionary['loggerwidget'].emit(self.message)
    time.sleep(self.seconds_int)
    raise SwitchProcessorBusy("Retry sending message")
"""
CLASS: KeyFailed
DESCRIPTION: Responsed to ssh key failure
INPUT: Received data
OUTPUT: Raises termination exception
"""
class KeyFailed(MyExceptions):
  "Key Failed"
  """"""
  def __init__(self, parent = None):
    self.name = self.__class__.__name__
    self.parent = parent
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dictionary = dictionary
    self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, "SSH key failed, cannot connect to device", Globals.SPAN_END_MESSAGE)
    self.dictionary['loggerwidget'].emit(self.message)
    raise Exception
"""
CLASS: UnknownCommand
DESCRIPTION: PROCESS unknown replies
INPUT: Received data
OUTPUT: Raises exception to terminate current session
"""
class UnknownCommand(MyExceptions):
  "Unkown Command"
  """"""
  def __init__(self, parent = None):
    self.name = self.__class__.__name__
    self.parent = parent
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dictionary = dictionary
    self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, "Unknown command sent to device.", Globals.SPAN_END_MESSAGE)
    self.dictionary['loggerwidget'].emit(self.message)
    raise Exception
"""
CLASS: UploadAborted
DESCRIPTION: SCP upload aborted message.
INPUT: received data buffer
OUTPUT: buffer
NOTE: This method never really gets called because the command line prompt is received.
"""
class UploadAborted(MyExceptions):
  "Upload Aborted"
  """"""
  def __init__(self, parent = None):
    self.name = self.__class__.__name__
    self.parent = parent
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dictionary = dictionary
    self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, "File upload to device aborted.", Globals.SPAN_END_MESSAGE)
    self.dictionary['loggerwidget'].emit(self.message)
    raise Exception
"""
CLASS: 
DESCRIPTION: 
INPUT: 
OUTPUT: 
"""
class PermissionDenied(MyExceptions):
  "Permission Denied"
  """"""
  def __init__(self, parent = None):
    self.name = self.__class__.__name__
    self.parent = parent
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dictionary = dictionary
    self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, "Login failed.", Globals.SPAN_END_MESSAGE)
    self.dictionary['loggerwidget'].emit(self.message)
    raise Exception
"""
CLASS: SendFileFailed
DESCRIPTION: 
INPUT: 
OUTPUT: 
"""
class SendFileFailed(MyExceptions):
  "Send File Failed"
  """"""
  def __init__(self, parent = None):
    self.name = self.__class__.__name__
    self.parent = parent
  """"""
  def execute(self, dictionary = None, descriptor = None, data = None, decode = None):
    self.dictionary = dictionary
    self.message = "{{{}{}: {}{}}}".format(Globals.RED_MESSAGE, self.name, "Sending file to server failed.", Globals.SPAN_END_MESSAGE)
    self.dictionary['loggerwidget'].emit(self.message)
    raise Exception
"""
CLASS: Failed
DESCRIPTION: Process Failed messages from the Analysis class
INPUT: Testcase data which failed epected data values
OUTPUT: Testcase seed file results data 
"""
class Failed(MyExceptions):
  "Failed"
  """"""
  def __init__(self, parent = None):
    self.name = self.__class__.__name__
    self.parent = parent
    self.dictionary = self.parent.cmdline_dict
  """"""
  def execute(self, element):
    try:
      self.element_clean = element[0].replace("<", "[").replace(">", "]")
      self.element = element
      self.message = "{{Test Case: "
      self.message +=  Globals.BOLD_MESSAGE + "{} ".format(self.element[1])
      self.message +=  Globals.NORMAL_MESSAGE + "{} ".format(self.element_clean)
      self.message += "{" + Globals.RED_MESSAGE + "{} ".format(element[2]) + Globals.SPAN_END_MESSAGE + "}"
      self.message += Globals.NORMAL_MESSAGE + "{} ".format(self.element[3]) + Globals.SPAN_END_MESSAGE + "}"
      self.dictionary['loggerwidget'].emit(self.message)
    except Exception as error:
      self.message = "{{{}{}: {}{}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
      self.dictionary['loggerwidget'].emit(self.message)
      raise Exception
    return(self.message)
"""
CLASS: Passed
DESCRIPTION: Process Passed messages from the Analysis class
INPUT: Testcase data which failed epected data values
OUTPUT: Testcase seed file results data 
"""
class Passed(MyExceptions):
  "Passed"
  """"""
  def __init__(self, parent = None):
    self.name = self.__class__.__name__
    self.parent = parent
    self.dictionary = self.parent.cmdline_dict
  """"""
  def execute(self, element):
    try:
      self.element_clean = element[0].replace("<", "[").replace(">", "]")
      self.element = element
      self.message = "{{Test Case: "
      self.message +=  Globals.BOLD_MESSAGE + "{} ".format(self.element[1])
      self.message +=  Globals.NORMAL_MESSAGE + "{} ".format(self.element_clean)
      self.message += Globals.BLUE_MESSAGE + "{} ".format(element[2]) + Globals.SPAN_END_MESSAGE + "}"
      self.message += Globals.NORMAL_MESSAGE + "{} ".format(self.element[3]) + Globals.SPAN_END_MESSAGE + "}"
      self.dictionary['loggerwidget'].emit(self.message)
    except Exception as error:
      self.message = "{{{}{}: {}{}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
      self.dictionary['loggerwidget'].emit(self.message)
      raise Exception
    return (self.message)
"""*************************************************************************************************************
End of File
*************************************************************************************************************"""
