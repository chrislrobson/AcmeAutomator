####################################################################################################################
# Python Qt5 Testbed Tester Show MPLS TrafficEng Tunnels Seed Analysis File Builder
# MODULE:  ShowMplsTrafficEngTunnelsSeedAnalysisFileBuilder
# Author: Christopher Robson
# Copyright by:  Christopher Robson
# Copyright date: 01Jan2016
# This software is not FREE!  Use or destribution of the software system and its
# subsystem modules, libraries, configuration file and "seed" file without the
# express permission of the author is strictly PROHIBITED!
# FUNCTION:  Module builds a seed file for analysizing collected data.
####################################################################################################################
import datetime
import binascii
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
# Home grown
#------------------------------------------------------------------------------------------------------------------
from Globals import *
from Exceptions import *
from SeedDictionary import SeedCommandDictionaryProcessor,\
                                                                SeedCommandlinePreprocessor
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
# Show Mpls TrafficEng Tunnels Seed Analysis File Builder
#-----------------------------------------------------------------------
class ShowMplsTrafficEngTunnelsSeedAnalysisFileBuilder:
  "Show Mpls TrafficEng Tunnels Seed Analysis File Builder"
  #----------------------------------------------------------------------------------------------------------------
  def __init__( self, parent = None ):
    self.name = "Show Mpls TrafficEng Tunnels Seed Analysis File Builder"
    self.parent = parent
    self.seed = parent.seed
    self.gparent = parent.parent.parent.parent
    self.filename_time_extension = self.parent.filename_time_extension
    self.cmd_list = parent.cmd_list
    self.with_line_numbers = "No"
    self.debug = False
    self.mpls_analysis_filename = ""
    self.mpls_data_filename = ""
    self.mpls_analysis_fd = None
    self.mpls_data_fd = None
    self.prepare_analysis_flag = False
    self.start_analysis_flag = False
    self.start_but_skip_one_analysis_flag = False
    self.mpls_table = []
    #-----------------------------------------------------------------------------------------------------------
    self.rsvp_global_neighbor = ""
    self.rsvp_interface_neighbor = ""
    self.rsvp_interface = ""
    self.rsvp_refresh_reduction = ""
    self.rsvp_remote_epoch = ""
    self.rsvp_out_of_order_count = ""
    self.rsvp_retransmitted_count = ""
  #----------------------------------------------------------------------------------------------------------------
  def execute( self ):
    #----------------------------------------------------------------------------------------------------------------
    self.interfaces_to_match = self.cmd_list[SeedCommandDictionaryProcessor.interfaces]
    self.device_being_matched = self.cmd_list[SeedCommandDictionaryProcessor.device]
    if self.cmd_list[SeedCommandDictionaryProcessor.verbose] == 'Yes':
      self.message_str = \
        "Build Show Mpls TrafficEng Tunnels Seed File command started at: {}\n".\
          format( datetime.datetime.now().strftime( "%d%b%Y-%H%M-%S" ) )
      self.gparent.processor_message_signal.emit(self.message_str)
    self.message_str = "Building seed file: {}.".\
          format( self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] )
    self.gparent.logger_message_signal.emit( self.message_str )
    try:
      self.analysis_filename = str( self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] )
      self.mpls_analysis_fd = open( self.analysis_filename, "w+" )
    except:
      raise Exception( "{}: ShowMplsTrafficEngTunnelsSeedAnalysisFileBuilder file I/O error with \"{}\". "
                       "Build Show Mpls TrafficEng Tunnels Seed File Command terminated. ".
                       format( self.name,
                               self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] )  )
    self.data_filename = self.cmd_list[SeedCommandDictionaryProcessor.commandpath] + \
                         self.cmd_list[SeedCommandDictionaryProcessor.commands] + \
                         self.filename_time_extension
    self.device = self.cmd_list[SeedCommandDictionaryProcessor.device]
    if self.device == "":
      raise CriticalFailure( "ShowMplsTrafficEngTunnelsSeedAnalysisFileBuilder: Invalid seed file!" )
    try:
      with open( self.data_filename, "r" ) as self.mpls_data_fd:
        for self.mpls_data in self.mpls_data_fd:
          if self.start_analysis_flag and self.device == "juniper":
            self.reportFD = self.build_juniper_analysis_seed_file()
            self.mpls_analysis_fd.close()
            self.mpls_data_fd.close()
            break
          elif self.start_analysis_flag and self.device == "cisco":
            self.reportFD = self.build_cisco_analysis_seed_file()
            self.mpls_analysis_fd.close()
            self.mpls_data_fd.close()
            break
          elif self.mpls_data.startswith( "DUT(" ) and \
               self.mpls_data.find( ")-> show rsvp neighbors" ) != -1:
            self.start_analysis_flag = True
            continue
          else:
            continue
    except Exception as e:
      raise Exception( "ShowInterfacesDetailSeedAnalysisFileBuilder: {}".format(e) )
    return()
  #----------------------------------------------------------------------------------------------------------------
  # FIXME ANOTHER QUICK AND DIRTY FIX the nesxt two methods should be OOPed!!!!!!
  #----------------------------------------------------------------------------------------------------------------
  """
  Name: tunnel-te1001  Destination: 150.20.1.129  Ifhandle:0x8000520 (auto-tunnel mesh)
  Signalled-Name: autom_R91B-R93-ASR9010_t1001_mg1
  Status:
    Admin:    up Oper:   up   Path:  valid   Signalling: connected
    path option 10,  type dynamic  (Basis for Setup, path weight 200410)
    G-PID: 0x0800 (derived from egress interface properties)
    Bandwidth Requested: 0 kbps  CT0
    Creation Time: Tue Aug 15 15:28:50 2017 (3d17h ago)
  Config Parameters:
    Bandwidth:        0 kbps (CT0) Priority:  7  7 Affinity: 0x0/0xffff
    Metric Type: IGP (global)
    Path Selection:
      Tiebreaker: Min-fill (default)
    Hop-limit: disabled
    Cost-limit: disabled
    Path-invalidation timeout: 45000 msec (default), Action: Tear (default)
    AutoRoute:  enabled  LockDown: disabled   Policy class: not set
    Forward class: 0 (default)
    Forwarding-Adjacency: disabled
    Loadshare:          0 equal loadshares
    Auto-bw: disabled
    Fast Reroute: Enabled, Protection Desired: Node
    Path Protection: Not Enabled
    Attribute-set: IPTPE-TO-UPE-MESH (type auto-mesh)
    BFD Fast Detection: Disabled
    Reoptimization after affinity failure: Enabled
    Soft Preemption: Disabled
  Auto-tunnel Mesh:
    Group ID: 1
    Destination list: IPTPE-TO-UPE-MESH
    Unused removal timeout: not running
  History:
    Tunnel has been up for: 3d17h (since Tue Aug 15 15:28:51 UTC 2017)
    Current LSP:
      Uptime: 3d17h (since Tue Aug 15 15:43:37 UTC 2017)
    Reopt. LSP:
      Last Failure:
        LSP not signalled, identical to the [CURRENT] LSP
        Date/Time: Tue Aug 15 15:31:51 UTC 2017 [3d17h ago]
    Prior LSP:
      ID: 3 Path Option: 10
      Removal Trigger: reoptimization completed
  Path info (IS-IS 27064 level-2):
  Node hop count: 3
  Hop0: 33.20.1.5
  Hop1: 150.20.1.10
  Hop2: 150.20.1.9
  Hop3: 150.20.1.134
  Hop4: 150.20.1.133
  Hop5: 150.20.1.129
  """
  #----------------------------------------------------------------------------------------------------------------
  def build_cisco_analysis_seed_file( self ):
    self.mpls_table = []
    self.line_length = 0
    for self.mpls_data in self.mpls_data_fd:
      self.line_length += len( self.mpls_data )
      if self.mpls_data.startswith( "\n" ):
        continue
      else:
        self.mpls_data_list = self.mpls_data.split()
        if self.mpls_data.startswith( "Name" ):
          self.name_received = self.mpls_data_list[1]
          self.destination = self.mpls_data_list[3]
          self.ifhandle = self.mpls_data_list[4].split( ":" )[1]
          self.autotunnel = self.mpls_data_list[5]
          continue
        if self.mpls_data.startswith( "Signalled-Name:" ):
          self.signal_name = self.mpls_data_list[1]
          continue
        if self.mpls_data_list[0].startswith( "Admin" ):
          self.admin_status = self.mpls_data_list[1]
          self.oper_status = self.mpls_data_list[3]
          self.path_status = self.mpls_data_list[5]
          self.signalling_status = self.mpls_data_list[7]
          continue
        if self.mpls_data_list[0].startswith( "path" ):
          self.path_option = self.mpls_data_list[2]
          self.type = self.mpls_data_list[4]
          self.basic_for =  self.mpls_data_list[7]
          self.path_weight = self.mpls_data_list[10]
          continue
        if self.mpls_data_list[0].startswith( "G-PID" ):
          self.gpid = self.mpls_data_list[1]
          self.derived = self.mpls_data_list[4]
          continue
        if self.mpls_data_list[0].startswith( "Bandwidth" ):
          self.kbps = self.mpls_data_list[2]
          self.derived = self.mpls_data_list[4]
          continue
    Bandwidth Requested: 0 kbps  CT0
    Creation Time: Tue Aug 15 15:28:50 2017 (3d17h ago)


                      #-----------------------------------------------------------------------------------------
                      self.mpls_table.append( "{" + \
                                                   "\"show rsvp neighbors detail\":\"show rsvp neighbors detail\"," \
                                                   "\"device\":\"{}\"," \
                                                   "\"rsvp global neighbor\":\"{}\"," \
                                                   "\"rsvp interface neighbor\":\"{}\"," \
                                                   "\"rsvp interface\":\"{}\"," \
                                                   "\"rsvp refresh reduction\":\"{}\"," \
                                                   "\"rsvp remote epoch\":\"{}\"," \
                                                   "\"rsvp out of order count\":\"{}\"," \
                                                   "\"rsvp retransmitted count\":\"{}\"".
                                                        format( self.device,
                                                                self.rsvp_global_neighbor,
                                                                self.rsvp_interface_neighbor,
                                                                self.rsvp_interface,
                                                                self.rsvp_refresh_reduction,
                                                                self.rsvp_remote_epoch,
                                                                self.rsvp_out_of_order_count,
                                                                self.rsvp_retransmitted_count) + \
                                                   "};")
                      break
            break
    #-------------------------------------------------------------------------------------------------------------
    for seed_dictionary in self.mpls_table:
      # FIXME DEBUG ONLY print(seed_dictionary)
      try:
        self.mpls_analysis_fd.write(seed_dictionary + "\n")
      except:
        print("Seed dictionary file write failed.")
    return()
  #----------------------------------------------------------------------------------------------------------------
  #----------------------------------------------------------------------------------------------------------------
  def build_juniper_analysis_seed_file( self ):
    mpls_table = []
    for self.mpls_data in self.mpls_data_fd:
      if self.mpls_data.startswith( "\n" ):
        break
      else:
        try:
          self.interface = self.mpls_data.split()[0]
        except:
          self.interface = ""
        try:
          self.system = self.mpls_data.split()[1]
        except:
          self.system = ""
        try:
          self.level = self.mpls_data.split()[2]
        except:
          self.level = ""
        try:
          self.state = self.mpls_data.split()[3]
        except:
          self.state = ""
        try:
          self.hold = self.mpls_data.split()[4]
        except:
          self.hold = ""
        try:
          self.snpa = self.mpls_data.split()[5]
        except:
          self.snpa = ""
        mpls_table.append( "{" + \
                                     "\"show rsvp neighbors\":\"show_mpls\",\"device\":\"juniper\"," \
                                     "\"interface\":\"{}\",\"system\":\"{}\"," \
                                     "\"level\":\"{}\",\"state\":\"{}\"," \
                                     "\"hold\":\"{}\",\"snpa\":\"{}\"".format( self.interface,
                                                                               self.system,
                                                                               self.level,
                                                                               self.state,
                                                                               self.hold,
                                                                               self.snpa ) + \
                                     "};")
    for seed_dictionary in mpls_table:
      # FIXME DEBUG print(seed_dictionary)
      try:
        self.mpls_analysis_fd.write(seed_dictionary + "\n")
      except:
        print("Seed dictionary file write failed.")
    return()
###################################################################################################################
