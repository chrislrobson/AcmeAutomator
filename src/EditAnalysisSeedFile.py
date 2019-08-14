####################################################################################################################
# Python Qt5 Testbed Tester Edit Analysis Seed File
# MODULE:  EditAnalysisSeedFile:w
# Author: Christopher Robson
# Copyright by:  Christopher Robson
# Copyright date: 01Jan2016
# This software is not FREE!  Use or destribution of the software system and its
# subsystem modules, libraries, configuration file and "seed" file without the
# express permission of the author is strictly PROHIBITED!
# FUNCTION:  Module allows an engineer to modify seed file Key:Value data.
####################################################################################################################
import datetime
import os
import shutil
import ast
import collections
import subprocess
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
# Home grown
#------------------------------------------------------------------------------------------------------------------
from Globals import *
from Exceptions import *
from SeedDictionary import SeedCommandDictionaryProcessor
from SeedCommandlinePreprocessor import SeedCommandlinePreprocessor
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
# Edit Analysis Seed File
#-----------------------------------------------------------------------
class EditAnalysisSeedFile:
  "Edit Analysis Seed File"
  #----------------------------------------------------------------------------------------------------------------
  def __init__( self, parent = None ):
    self.name = "Edit Analysis Seed File"
    self.parent = parent
    self.seed = parent.seed
    self.gparent = parent.parent.parent.parent
    self.filename_time_extension = self.parent.filename_time_extension
    self.cmd_list = parent.cmd_list
    self.with_line_numbers = "No"
    self.debug = False
    self.detail_interfaces_detail_analysis_filename = ""
    self.detail_interfaces_detail_data_filename = ""
    self.detail_interfaces_detail_analysis_fd = None
    self.detail_data_fd = None
    self.start_analysis_flag = False
    self.show_interfaces_detail_table = []
    self.interfaces_to_match = ""
  #----------------------------------------------------------------------------------------------------------------
  def execute( self ):
    self.results = ""
    self.received_data = ""
    #----------------------------------------------------------------------------------------------------------------
    self.interfaces_to_match = self.cmd_list[SeedCommandDictionaryProcessor.interfaces]
    self.userpath = os.path.expanduser( "~" ) + "/"
    if self.cmd_list[SeedCommandDictionaryProcessor.verbose] == 'Yes':
      self.message_str = \
        "Editing Analysis Seed File command started at: {}".\
          format( datetime.datetime.now().strftime( "%d%b%Y-%H%M-%S" ) )
      self.gparent.processor_message_signal.emit(self.message_str)
    self.message_str = "Editing Analysis seed file: {}.".\
          format( self.cmd_list[SeedCommandDictionaryProcessor.commands] )
    self.gparent.logger_message_signal.emit( self.message_str )
    try:
      self.source_analysis_seed_file = str( self.cmd_list[SeedCommandDictionaryProcessor.commandpath] ) + \
                               str( self.cmd_list[SeedCommandDictionaryProcessor.commands] )
    except:
      raise Exception( "{}: EditingAnalysisSeedFile file I/O error with \"{}\". "
                       "Editing Analysis Seed File Command terminated. ".
                       format( self.name,
                               self.cmd_list[SeedCommandDictionaryProcessor.commands] )  )
    try:
      self.source_analysis_seed_file_fd = open( self.source_analysis_seed_file, "r" )
      self.working_analysis_seed_file_fd = open( "/tmp/WorkingAnalysisSeedFile", "w+" )
    except:
      raise Exception( "EditingAnalysisSeedFile file I/O error with \"{}\"".
                       format( "Source(or Target)AnalysisSeedFile.tmp" ) )
    try:
      self.build_edit_analysis_seed_file( self.source_analysis_seed_file_fd, self.working_analysis_seed_file_fd )
    except Exception as error:
      print( error )
    self.source_analysis_seed_file_fd.close()
    self.working_analysis_seed_file_fd.close()
    self.cmd = ["/bin/gvim", "/tmp/WorkingAnalysisSeedFile"
               ]
    try:
      self.output = subprocess.Popen( self.cmd,
                                      stdout = subprocess.PIPE,
                                      stderr = subprocess.PIPE
                                    )
      try:
        self.outputresults, self.err = self.output.communicate()
        if self.output.returncode != 0:
          if self.cmd_list[SeedCommandDictionaryProcessor.verbose] == 'Yes':
            self.message_str = Globals.RED_ONLY_MESSAGE + \
                               "EDITANALYSISSEEDFILE: failed error {}.".format( self.output.returncode ) + \
                               Globals.SPAN_END_MESSAGE
            self.gparent.logger_message_signal.emit( self.message_str )
          raise Exception( "EDITANALYSISSEEDFILE: failed error {}.".format( self.output.returncode ) )
      except Exception as error:
        if self.cmd_list[SeedCommandDictionaryProcessor.verbose] == 'Yes':
          self.message_str = Globals.RED_ONLY_MESSAGE + \
                             "{}: failed: {}\n {}.".format( self.name, self.cmd, error ) + \
                             Globals.SPAN_END_MESSAGE
          self.gparent.logger_message_signal.emit( self.message_str )
      # FIXME NEEDS TESTING MAY NOT WORK self.results = str( self.outputresults, "utf-8" )
      # FIXME NEEDS TESTING MAY NOT WORK self.err_str = str( self.err, "utf-8" )
      # FIXME NEEDS TESTING MAY NOT WORK if self.err_str != "":
      # FIXME NEEDS TESTING MAY NOT WORK   raise Exception( "{}: failed error {}.".format( self.name, self.err_str ) )
    except Exception as error:
      raise Exception( error )
    try:
      self.working_analysis_seed_file_fd = open( "/tmp/WorkingAnalysisSeedFile", "r" )
      try:
        self.build_new_analysis_seed_file( self.working_analysis_seed_file_fd,
                                         self.cmd_list[SeedCommandDictionaryProcessor.archivefilenameFD] )
      except Exception as error:
        print(error)
      self.working_analysis_seed_file_fd.close()
      self.cmd_list[SeedCommandDictionaryProcessor.archivefilenameFD].close()
      os.remove( "/tmp/WorkingAnalysisSeedFile" )
    except Exception as error:
      print( error )
    return()
  #----------------------------------------------------------------------------------------------------------------
  # FIXME more places oop'ing these two methods below would be a good idea, aka, factories maybe or importlib's
  #----------------------------------------------------------------------------------------------------------------
  def build_edit_analysis_seed_file( self, analysis_seed_file_fd, working_analysis_seed_file_fd  ):
    for self.analysis_seed_file_item in analysis_seed_file_fd:
      self.convert_string = ""
      try:
        for self.item_dict1 in self.analysis_seed_file_item.rsplit(";"):
          if self.item_dict1 == "\n":
            continue
          self.cvt_it = self.item_dict1.split( "{", 1 )[1].rsplit( "}", 1 )[0]
          self.cvt_it = self.cvt_it.replace( "\",\"", "\"),(\"" ).\
                                    replace( ":", "," ).\
                                    replace( "{", "[(" ).\
                                    replace( "},", ")]),(" ).\
                                    replace( "}", ")]" )
          self.cvt_it = "({}),".format( self.cvt_it )
        self.convert_string += "[{}]".format( self.cvt_it[:-1] )
      except IndexError:
        raise IndexError( "Input string parsing error." )
      try:
        self.convert_string_triple = ast.literal_eval( self.convert_string )
      except Exception as error:
        raise Exception( error )
      try:
        self.ordered_dictionary = collections.OrderedDict( self.convert_string_triple )
      except Exception as error:
        raise( error )
      for self.key, self.value in self.ordered_dictionary.items():
        if self.key.startswith( "show " ):
          working_analysis_seed_file_fd.write( "\n<------------ SECTION BREAK -------------->\n" )
          working_analysis_seed_file_fd.write( "{}\t:\t{}\n".format( self.key, self.value ) )
          continue
        if self.key.startswith( "show interfaces" ):
          working_analysis_seed_file_fd.write( "\n<------------ SECTION BREAK -------------->\n" )
          working_analysis_seed_file_fd.write( "{}\t:\t{}\n".format( self.key, self.value ) )
          continue
        if self.key.startswith( "show mpls traffic-eng tunnels tabular" ):
          working_analysis_seed_file_fd.write( "\n<------------ SECTION BREAK -------------->\n" )
          working_analysis_seed_file_fd.write( "{}\t:\t{}\n".format( self.key, self.value ) )
          continue
        if not isinstance(self.value, str):
          for self.subkey, self.subvalue in self.value:
            working_analysis_seed_file_fd.write( "{}: {}\t \t{}\n".format( self.key, self.subkey, self.subvalue ) )
        else:
          working_analysis_seed_file_fd.write( "{}\t:\t{}\n".format( self.key, self.value ) )
    return()
  #----------------------------------------------------------------------------------------------------------------
  # FIXME more places oop'ing these two methods below would be a good idea, aka, factories maybe or importlib's
  # FIXME and all the use of a,b,c variables so so damn HUGLY CLEAN UP!!!!
  #----------------------------------------------------------------------------------------------------------------
  def build_new_analysis_seed_file( self, working_analysis_seed_file_fd, new_analysis_seed_file_fd ):
    self.first = False
    self.first_interface = False
    self.bundle_flag = False
    self.first_bundle_flag = ""
    self.index = 0
    for self.item in working_analysis_seed_file_fd:
      self.index += len( self.item )
      self.first_l2vpn = True
      if self.item.startswith( "\n" ):
        continue
      if self.item.startswith( "<------------ SECTION BREAK -------------->" ) and not self.first_interface:
        self.first_interface = True
        continue
      if self.item.startswith( "<------------ SECTION BREAK -------------->" ) and self.first_interface:
        self.command_str += "};\n"
        new_analysis_seed_file_fd.write( self.command_str )
        self.first = False
        self.bundle_flag = False
        self.first_bundle_flag = ""
        continue
      if self.item.startswith( "show " ) and not self.first:
        self.command_str = "{{\"{}\"".format( self.item.split( "\n" )[0].replace( "\t", "" ).replace( ":", "\":\"" ) )
        self.first = True
      elif self.item.startswith( "show " ) and self.first:
        self.command_str += "};\n"
        new_analysis_seed_file_fd.write( self.command_str )
        self.command_str = "{{\"{}\"".format( self.item.split( "\n" )[0].replace( "\t", "" ).replace( ":", "\":\"" ) )
      elif self.item.startswith( "number of bundled interfaces" ):
        try:
          self.bundle_count = int( self.item.split()[5] )
          self.command_str += ",\"{}\"".format( self.item.split( "\n" )[0].replace( "\t", "" ).replace( ":", "\":\"" ) )
          self.bundle_flag = True
          self.bundle_cnt = 1
          for self.item in working_analysis_seed_file_fd:
            self.index += len( self.item )
            if not self.item.startswith( "bundle" ):
              self.command_str += "\"}"
              self.working_analysis_seed_file_fd.seek( self.index - len( self.item ) )
              self.index -= len( self.item )
              self.bundle_cnt += 1
              break
            if self.bundle_flag and not self.first_bundle_flag == "" and \
               self.item.startswith( "bundle {}".format( int( self.bundle_cnt ) ) ):
              self.cvt_it = self.item.split( "\n" )[0].split( ":" )[1]
              self.cvt_it = "\":\"".join( self.cvt_it.split() )
              self.command_str += "\",\"{}".format( self.cvt_it )
            elif self.bundle_flag and not self.first_bundle_flag == "" and not \
                 self.item.startswith( "bundle {}".format( int( self.bundle_cnt ) ) ):
              self.command_str += "\"}"
              self.first = False
              self.first_bundle_flag = ""
              self.working_analysis_seed_file_fd.seek( self.index - len( self.item ) )
              self.index -= len( self.item )
              self.bundle_cnt += 1
            elif self.bundle_flag and self.first_bundle_flag == "":
              self.first_bundle_flag = self.item.split( ":" )[0]
              self.cvt_it = self.item.split( "\n" )[0].split( ":" )[1]
              self.cvt_it = " ".join( self.cvt_it.split() )
              self.cvt_it_final = ",\"{}\":".format( self.first_bundle_flag )
              self.cvt_it_final += "{\"" + self.cvt_it.replace( "\t", "" ).replace( " ", "\":\"" )
              self.command_str += "{}".format( self.cvt_it_final )
        except:
          self.bundle_count = 0
      elif self.item.startswith( "intf" ):
        self.command_str += ",\"intf {}\":". \
                              format( " ".join( self.item.split( ":" )[0].
                                                split( "intf" )[1].
                                                split() ) ) + "{"
        a = " ".join( self.item.split( ":" )[1].split( "\t", 1 )[0].split() )
        b = self.item.split( ":" )[1].split( "\t", 1 )[1].replace( "\t", "" ).replace( "\n", "" )
        try:
          c = b.split()
        except:
          c = []
        f = " ".join( c )
        self.command_str += "\"{}\":\"{}\",".format( a, f )
        for self.item in working_analysis_seed_file_fd:
          if self.item.startswith( "\n" ):
            self.index += len( self.item )
            continue
          if self.item.startswith( "<------------ SECTION BREAK -------------->" ):
            self.working_analysis_seed_file_fd.seek( self.index )
            self.command_str = self.command_str[:-1]
            self.command_str += "}"
            break
          if self.item.startswith( "neighborpw" ) or \
              self.item.startswith( "acgroup" ) or \
              self.item.startswith( "pwgroup" ):
            self.working_analysis_seed_file_fd.seek( self.index )
            break
          self.index += len( self.item )
          a = " ".join( self.item.split( ":" )[1].split( "\t", 1 )[0].split() )
          b = self.item.split( ":" )[1].split( "\t", 1 )[1].replace( "\t", "" ).replace( "\n", "" )
          try:
            c = b.split()
          except:
            c = []
          f = " ".join( c )
          self.command_str += "\"{}\":\"{}\",".format( a, f )
        self.command_str = self.command_str[:-1]
        self.command_str += "}"
        self.first_l2vpn = False
      elif self.item.startswith( "acgroup" ):
        self.command_str += ",\"acgroup {}\":".\
                            format( " ".join( self.item.split( ":" )[0].
                                                        split( "acgroup" )[1].
                                                        split() ) ) + "{"
        a = " ".join( self.item.split( ":" )[1].split( "\t", 1 )[0].split() )
        b = self.item.split( ":" )[1].split( "\t", 1 )[1].replace( "\t", "" ).replace( "\n", "" )
        try:
          c = b.split()
        except:
          c = []
        f = " ".join( c )
        self.command_str += "\"{}\":\"{}\",".format( a, f )
        for self.item in working_analysis_seed_file_fd:
          if self.item.startswith( "\n" ):
            self.index += len( self.item )
            continue
          if self.item.startswith( "<------------ SECTION BREAK -------------->" ):
            self.working_analysis_seed_file_fd.seek( self.index )
            self.command_str = self.command_str[:-1]
            self.command_str += "}"
            break
          if self.item.startswith( "neighborpw" ) or \
             self.item.startswith( "intf" ) or \
             self.item.startswith( "pwgroup" ):
            self.working_analysis_seed_file_fd.seek( self.index )
            break
          self.index += len( self.item )
          a = " ".join( self.item.split( ":" )[1].split( "\t", 1 )[0].split() )
          b = self.item.split( ":" )[1].split( "\t", 1 )[1].replace( "\t", "" ).replace( "\n", "" )
          try:
            c = b.split()
          except:
            c = []
          f = " ".join(c)
          self.command_str += "\"{}\":\"{}\",".format(a,f)
        self.command_str = self.command_str[:-1]
        self.command_str += "}"
      elif self.item.startswith( "pwgroup" ):
        self.command_str += ",\"pwgroup {}\":".\
                            format( " ".join( self.item.split( ":" )[0].
                                                        split( "pwgroup" )[1].
                                                        split() ) ) + "{"
        a = " ".join( self.item.split( ":" )[1].split( "\t", 1 )[0].split() )
        b = self.item.split( ":" )[1].split( "\t", 1 )[1].replace( "\t", "" ).replace( "\n", "" )
        try:
          c = b.split()
        except:
          c = []
        f = " ".join( c )
        self.command_str += "\"{}\":\"{}\",".format( a, f )
        for self.item in working_analysis_seed_file_fd:
          if self.item.startswith( "\n" ):
            self.index += len( self.item )
            continue
          if self.item.startswith( "<------------ SECTION BREAK -------------->" ):
            self.working_analysis_seed_file_fd.seek( self.index )
            self.command_str = self.command_str[:-1]
            self.command_str += "}"
            break
          if self.item.startswith( "neighborpw" ) or \
             self.item.startswith( "intf" ):
            self.working_analysis_seed_file_fd.seek( self.index )
            break
          self.index += len( self.item )
          try:
            a = " ".join( self.item.split( ":" )[1].split( "\t", 1 )[0].split() )
            b = self.item.split( ":" )[1].split( "\t", 1 )[1].replace( "\t", "" ).replace( "\n", "" )
            try:
              c = b.split()
            except:
              c = []
            f = " ".join(c)
            self.command_str += "\"{}\":\"{}\",".format(a,f)
          except:
            pass
        self.command_str = self.command_str[:-1]
        self.command_str += "}"
      elif self.item.startswith( "neighborpw" ):
        self.command_str += ",\"neighborpw {}\":". \
                              format( " ".join( self.item.split( ":" )[0].
                                                split( "neighborpw" )[1].
                                                split() ) ) + "{"
        a = " ".join( self.item.split( ":" )[1].split( "\t", 1 )[0].split() )
        b = self.item.split( ":" )[1].split( "\t", 1 )[1].replace( "\t", "" ).replace( "\n", "" )
        try:
          c = b.split()
        except:
          c = []
        f = " ".join( c )
        self.command_str += "\"{}\":\"{}\",".format( a, f )
        for self.item in working_analysis_seed_file_fd:
          if self.item.startswith( "\n" ):
            self.index += len( self.item )
            continue
          if self.item.startswith( "<------------ SECTION BREAK -------------->" ):
            self.working_analysis_seed_file_fd.seek( self.index )
            self.command_str = self.command_str[:-1]
            self.command_str += "}"
            break
          if self.item.startswith( "acgroup" ) or \
              self.item.startswith( "intf" ) or \
              self.item.startswith( "pwgroup" ):
            self.working_analysis_seed_file_fd.seek( self.index )
            break
          self.index += len( self.item )
          a = " ".join( self.item.split( ":" )[1].split( "\t", 1 )[0].split() )
          b = self.item.split( ":" )[1].split( "\t", 1 )[1].replace( "\t", "" ).replace( "\n", "" )
          try:
            c = b.split()
          except:
            c = []
          f = " ".join( c )
          self.command_str += "\"{}\":\"{}\",".format( a, f )
        self.command_str = self.command_str[:-1]
        self.command_str += "}"
      else:
        self.command_str += ",\"{}\"".format( self.item.split( "\n" )[0].replace( "\t", "" ).replace( ":", "\":\"" ) )
    self.command_str += "};\n"
    new_analysis_seed_file_fd.write( self.command_str )
    return()
#################################################################################################################