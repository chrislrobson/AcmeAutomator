####################################################################################################################
# MyExceptions
# MODULE:  Exceptions
# Author: Christopher Robson
# Copyright by:  Christopher Robson
# Copyright date: 01Jan2016
# This software is not FREE!  Use or destribution of the software system and its
# subsystem modules, libraries, configuration file and "seed" file without the
# express permission of the author is strictly PROHIBITED!
# FUNCTION:  Module provides the results custom made exceptions specific to Testbed Autmator.
####################################################################################################################
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
# Exceptions
#------------------------------------------------------------------------------------------------------------------
class MyExceptions( Exception ):
  "Testbed Tester Exceptions"
  #----------------------------------------------------------------------------------------------------------------
  def __init__( self, MyExceptions ):
    self.name = "Testbed Tester Exceptions"
    pass
#----------------------------------------------------------------------------------------------------------------
class SwitchProcessorBusy(MyExceptions):
  "Switch Processor Busy"
  #---------------------------------------------------------------------------------------------------------------
  def __init__(self, message):
    super(SwitchProcessorBusy, self).__init__(message)
    self.name = "Switch Processor Busy"
    self.message = message
    self.messages = {message}
#----------------------------------------------------------------------------------------------------------------
class XMLKeyError( MyExceptions ):
  "XML Key Error"
  # ---------------------------------------------------------------------------------------------------------------
  def __init__( self, message ):
    super( XMLKeyError, self ).__init__( message )
    self.name = "XML Key Error."
    self.message = message
    self.messages = { message }
#----------------------------------------------------------------------------------------------------------------
class NotAnError( MyExceptions ):
  "Not An Error"
  #---------------------------------------------------------------------------------------------------------------
  def __init__( self, message ):
    super( NotAnError, self ).__init__( message )
    self.name = "Not An Error"
    self.message = message
    self.messages = { message }
#----------------------------------------------------------------------------------------------------------------
class CriticalFailure( MyExceptions ):
  "Critical Failure"
  #---------------------------------------------------------------------------------------------------------------
  def __init__( self, message ):
    super( CriticalFailure, self ).__init__( message )
    self.name = "Critical Failure, session terminated."
    self.message = message
    self.messages = {message}
#----------------------------------------------------------------------------------------------------------------
class ProcessReplyError( MyExceptions ):
  "Processor Reply error"
  # ---------------------------------------------------------------------------------------------------------------
  def __init__( self, message ):
    super( ProcessReplyError, self ).__init__( message )
    self.name = "Switch Processor Busy"
    self.message = message
    self.messages = { message }
#----------------------------------------------------------------------------------------------------------------
class MissingDictionaryEntry(MyExceptions):
  "Missing Dictionary Entry"
  #--------------------------------------------------------------------------------------------------------------
  def __init__( self, message ):
    super( MissingDictionaryEntry, self).__init__( message )
    self.name = "Missing Dictionary Entry"
    self.message = message
    self.messages = {message}
#----------------------------------------------------------------------------------------------------------------
class SSHReadChannelTimeout( MyExceptions ):
  "SSH Read Channel Timeout"
  #--------------------------------------------------------------------------------------------------------------
  def __init__(self, message):
    super( SSHReadChannelTimeout, self ).__init__( message )
    self.name = "SSH Read Channel Timeout"
    self.message = message
    self.messages = {message}

#----------------------------------------------------------------------------------------------------------------
class SSHReadAuthenicationError(MyExceptions):
  "SSH Read Channel Timeout"
  #--------------------------------------------------------------------------------------------------------------
  def __init__(self, message):
    super(SSHReadAuthenicationError, self).__init__(message)
    self.name = "SSH Authentication Error"
    self.message = message
    self.messages = {message}
#----------------------------------------------------------------------------------------------------------------
class SSHSocketError( MyExceptions ):
  "SSH Read Channel Timeout"
  # --------------------------------------------------------------------------------------------------------------
  def __init__(self, message):
    super( SSHSocketError, self ).__init__( message )
    self.name = "SSH Socket Error"
    self.message = message
    self.messages = {message}
#----------------------------------------------------------------------------------------------------------------
class SSHConnectionError( MyExceptions ):
  "SSH Connection Error"
  #--------------------------------------------------------------------------------------------------------------
  def __init__( self, message ):
    super( SSHConnectionError, self ).__init__( message )
    self.name = "SSH Connection Error"
    self.message = message
    self.messages = { message }
#----------------------------------------------------------------------------------------------------------------
class SSHSendError( MyExceptions ):
  "SSH Connection Error"
  # --------------------------------------------------------------------------------------------------------------
  def __init__( self, message ):
    super( SSHSendError, self ).__init__( message )
    self.name = "SSH Connection Error"
    self.message = message
    self.messages = { message }
#----------------------------------------------------------------------------------------------------------------
class CommandDictionaryError( MyExceptions ):
  "SSH Connection Error"
  # --------------------------------------------------------------------------------------------------------------
  def __init__( self, message ):
    super( CommandDictionaryError, self ).__init__( message )
    self.name = "SSH Connection Error"
    self.message = message
    self.messages = { message }
#----------------------------------------------------------------------------------------------------------------
class DUTCommandError( MyExceptions ):
  "SSH Connection Error"
  # --------------------------------------------------------------------------------------------------------------
  def __init__( self, message ):
    super( DUTCommandError, self ).__init__( message )
    self.name = "SSH Connection Error"
    self.message = message
    self.messages = { message }
#----------------------------------------------------------------------------------------------------------------
class HostCommandError( MyExceptions ):
  "SSH Connection Error"
  # --------------------------------------------------------------------------------------------------------------
  def __init__( self, message ):
    super( HostCommandError, self ).__init__( message )
    self.name = "SSH Connection Error"
    self.message = message
    self.messages = { message }
#----------------------------------------------------------------------------------------------------------------
class PermissionDenied( MyExceptions ):
  "Permission denied"
  #---------------------------------------------------------------------------------------------------------------
  def __init__( self, message ):
    super( PermissionDenied, self ).__init__( message )
    self.name = "Permission Denied"
    self.message = message
    self.messages = {message}
#----------------------------------------------------------------------------------------------------------------
class SendFileFailed( MyExceptions ):
  "Send File Failed"
  #---------------------------------------------------------------------------------------------------------------
  def __init__( self, message ):
    super( SendFileFailed, self ).__init__( message )
    self.name = "Send File Failed"
    self.message = message
    self.messages = {message}
#----------------------------------------------------------------------------------------------------------------
class UploadAborted( MyExceptions ):
  "Upload Aborted"
  #---------------------------------------------------------------------------------------------------------------
  def __init__( self, message ):
    super( UploadAborted, self ).__init__( message )
    self.name = "Permission Denied"
    self.message = message
    self.messages = {message}
#----------------------------------------------------------------------------------------------------------------
class KeyFailed( MyExceptions ):
  "Key Failed"
  #---------------------------------------------------------------------------------------------------------------
  def __init__( self, message ):
    super( KeyFailed, self ).__init__( message )
    self.name = "Key Failed"
    self.message = message
    self.messages = {message}
#----------------------------------------------------------------------------------------------------------------
class UnknownCommand( MyExceptions ):
  "Upload Aborted"
  #---------------------------------------------------------------------------------------------------------------
  def __init__( self, message ):
    super( UnknownCommand, self ).__init__( message )
    self.name = "Unknown Command"
    self.message = message
    self.messages = {message}