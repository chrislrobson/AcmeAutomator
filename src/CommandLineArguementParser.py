"""
MODULE: Commandline Arguement Parser
Author: Christopher Robson
Copyright by:  Christopher Robson
Copyright date: 01Jan2016
This software is not FREE!  Use or destribution of the software system and its
subsystem modules, libraries, configuration file and "seed" file without the
express permission of the author is strictly PROHIBITED!
Yes I will sue your ass off if you decode, destribute or do ANYTHING without my expressed permission.
This includes any government agency, any company or any employee of those orgainizations.
THIS IS NOT FREE SOFTWARE
FUNCTION:  Processes any commandline options
"""
"""
LIBRARIES:  Python libraries
"""
import argparse
"""
LIBRARIES:  Testbed Tester specific libraries
"""
"""
CLASS: CommandLineArguementParser
DESCRIPTION: Processes commandline options
INPUT: options
OUTPUT: decodes to program options
"""
#------------------------------------------------------------------------------------------------------------------
class CommandLineArguementParser:
  " Command Line Argument Parser"
  #----------------------------------------------------------------------------------------------------------------
  def __init__( self ):
    self.name = self.__class__.__name__
  #----------------------------------------------------------------------------------------------------------------
  def command_line_arguement_parser( self ):
    parser = argparse.ArgumentParser( )
    parser.add_argument( '-Y', "--welcomeframed", action = "store_true",
                         default = False,
                         dest = "welcomeframed",
                         help = "Welcome window is framed" )
    parser.add_argument( '-W', "--commandline", action = "store_true",
                         default = False,
                         dest = "command_line_dump",
                         help = "Command line dump" )
    parser.add_argument( '-U', "--User", action = "store",
                         default = "test",
                         dest = "user_to_use",
                         help = "Global user" )
    parser.add_argument( '-R',"--relative-directory-path",action = "store",
                         default = None,
                         dest = "relativepath",
                         help = "Relative path to directory" )
    parser.add_argument( '-P', "--Password", action = "store",
                         default = "geTest",
                         dest = "password_to_use",
                         help = "Global password" )
    parser.add_argument( '-A', "--All-IPs", action = "store_true",
                           default = False,
                           dest = "do_all_IPs",
                           help = "If set all IP addresses will be processed" )
    parser.add_argument( '-F', "--inventory-show-file-directory", action="store",
                         default="./",
                         dest="inventory_file_directory",
                         help="Directory containing inventory files.")
    parser.add_argument( '-I', "--inventory-directory", action="store",
                         default = "./",
                         dest="inventory_directory",
                         help="Directory for storing inventory excel report files.")
    parser.add_argument( '-D', "--device-list", action = "store",
                           default = None,
                           dest = "deviceList",
                           help = "IP address list of devices to inventory or a file "
                                  "containing a list of files. File \"MUST\" be provided "
                                  "and have extension \".py\"." )
    parser.add_argument( '-S', "--search", action="store",
                         default=None,
                         dest="searchList",
                         help="Searches for an part or part number" )
    parser.add_argument( '-X', "--xml-file", action="store",
                         default=None,
                         dest="xml_file",
                         help="XML files is the input to process" )
    parser.add_argument( '-b',"--bgp-test-profile",action = "store",
                         default = 1,
                         dest = "bgpProfiles",
                         help = "BGP test profiles" )
    parser.add_argument( '-a',"--again-counter",action = "store",
                         default = 1,
                         dest = "retransmitCounter",
                         help = "Again send command counter" )
    parser.add_argument( '-Q',"--archive-current-state",action = "store_true",
                         default = False,
                         dest = "archiveCurrentDeviceState",
                         help = "Archive the current state of each device" )
    parser.add_argument( '-T',"--TCP-verbose",action = "store_true",
                         default = False,
                         dest = "tcpVerbose",
                         help = "Display TCP traffic" )
    parser.add_argument( '-l',"--run-count",action = "store",
                         default = 1,
                         dest = "run_counter",
                         help = "Testbed Autmator repeat test run count" )
    parser.add_argument( '-L',"--app-repeat-count",action = "store",
                         default = 1,
                         dest = "appTestRepeatCount",
                         help = "Repeat application Test by count" )
    parser.add_argument( '-G',"--gen-Pkt-traffic",action = "store_true",
                         default = False,
                         dest = "genPktTraffic",
                         help = "Generate Packet traffic" )
    parser.add_argument( '-z',"--gen-App-traffic",action = "store_true",
                         default = False,
                         dest = "genAppTraffic",
                         help = "Generate Application TCP traffic" )
    parser.add_argument( '-B',"--baseline-network",action = "store_true",
                         default = False,
                         dest = "baselineNetwork",
                         help = "Program each device with a baseline configuration" )
    parser.add_argument( '-d',"--debug",action = "store_true",
                         default = False,
                         dest = "debug",
                         help = "Debug flag enabled" )
    parser.add_argument( '-x',"--xmt-port",action = "store",
                         default = 0,
                         dest = "droneXmtPort",
                         help = "Drone transmit port" )
    parser.add_argument( '-r',"--rcv-port",action = "store",
                         default = 0,
                         dest = "droneRcvPort",
                         help = "Drone receive port" )
    parser.add_argument( '-m',"--master-profile-file",action = "store",
                         default = "./TestbedTester/MasterProfiles.prf",
                         dest = "networkMasterTestsetProfile",
                         help = "Network master testset profile" )
    parser.add_argument( '-C',"--template-profile-file",action = "store",
                         default = "./TestbedTester/Templates.prf",
                         dest = "templatesProfileFile",
                         help = "Template profile file" )
    parser.add_argument( '-E',"--template-seed-file",action = "store",
                         default = "./TestbedTester/TemplateSeedFile.prf",
                         dest = "templateSeedFile",
                         help = "Template Seed file" )
    parser.add_argument( '-g',"--diagram-profile-file",action = "store",
                         default = "./TestbedTester/labtopology.png",
                         dest = "networkDiagramProfile",
                         help = "Network diagram profile" )
    parser.add_argument( '-p',"--profile-file",action = "store",
                         default = None,
                         dest = "networkDeviceProfile",
                         help = "Network device profile" )
    parser.add_argument( '-c',"--config-files",action = "store",
                         default = None,
                         dest = "networkDeviceConfigFiles",
                         help = "Network device config file(s)" )
    parser.add_argument( '-i',"--ixia-file",action = "store",
                         default = None,
                         dest = "networkDeviceIxiaFile",
                         help = "Network device Ixia file" )
    parser.add_argument( '-V',"--valid-config-File",action = "store",
                         default = None,
                         dest = "validateConfigFile",
                         help = "Validate configuration file" )
    parser.add_argument( '-Z',"--validate-network",action = "store_true",
                         default = False,
                         dest = "validateNetwork",
                         help = "Validate the network configurations" )
    parser.add_argument( '-s',"--logger",action = "store",
                         default = None,
                         dest = "set_logger()",
                         help = "Enable logging" )
    parser.add_argument( '-t',"--timer",action = "store",
                         default = 0,
                         dest = "delay_timer",
                         help = "Time delay between traffic gneration sequences" )
    parser.add_argument( '-v',"--verbose",action = "store_true",
                         default = False,
                         dest = "verbose",
                         help = "Turn on verbose output printing" )
    parser.add_argument( '-N',"--No-Test",action = "store_true",
                         default = True,
                         dest = "noTestFlag",
                         help = "No test will be run" )
    return (parser)

