"""***************************************************************************************************************
FILE: Globals
MODULE:   Globals
Author: Christopher Robson
Copyright by:  Christopher Robson
Copyright date: 01Jan2016
This software is not FREE!  Use or destribution of the software system and its
subsystem modules, libraries, configuration file and "seed" file without the
express permission of the author is strictly PROHIBITED!
FUNCTION:  Class provides global variables.  While its better not to use globals for the intial and until
           they can be changed, this system make use of them.
           #fixme SO THIS FILE SHOULD SHRINK OVER TIME !
***************************************************************************************************************"""
"""
CLASS: Globals
DESCRIPTION: Hold variables that must pass between threads/subsystems 
INPUT: 
OUTPUT: 
"""
class Globals():
    "Globals"
    """
    Used to validate and install Analysis Seed file dictionary
    elements.
    """
    analysis_seed_dictionary = {'testcase': '0.0',
                                'seed': '',
                                'seedpath': '',
                                'data': '',
                                'datapath': '',
                                'stdout': '',
                                'verbose': '',
                                'fileoutput': '',
                                'issave': '',
                                'scanlines': '',
                                'analysisreportpath': '',
                                'exactfilename': '',
                                'filename': '',
                                'interfaces': '',
                                'device': '',
                                'reporttemplate': ''
                                }
    """"""
    show_command_counter = 0
    dut_command_counter = 0
    password_to_use = "geTest"
    user_to_use = "test"
    SSHRECEIVETRANSMITBUFFER = 256000
    ssh_connection_dict = []
    ssh_loop_cnt = 0
    selected_interfaces = ""  # List of interfaces to run matches against for methods such as ShowInterfaces.
    # fixme REMOVE THIS LATER #---------------------------------------------------------------------------------------------------------------
    # fixme REMOVE THIS LATER # Files to use to fill in the data fields of the template files
    # fixme REMOVE THIS LATER #---------------------------------------------------------------------------------------------------------------
    # fixme REMOVE THIS LATER template_seed_selections_listed = False
    # fixme REMOVE THIS LATER template_seed_files_list = []
    # fixme REMOVE THIS LATER template_seed_files_list_dict = []
    # fixme REMOVE THIS LATER template_seed_files_to_be_built_list = []
    # fixme REMOVE THIS LATER #---------------------------------------------------------------------------------------------------------------
    # fixme REMOVE THIS LATER # Canned master profile files used to build individual master-profile.prf files
    # fixme REMOVE THIS LATER #---------------------------------------------------------------------------------------------------------------
    # fixme REMOVE THIS LATER templates_selections_listed = False
    # fixme REMOVE THIS LATER templates_file_list = []
    # fixme REMOVE THIS LATER templates_file_list_dict = []
    # fixme REMOVE THIS LATER templates_to_be_built_list = []
    """"""
    playbook_list = []
    playbook_to_be_tested_list = []
    """"""
    request_command_counter = 0
    dut_selections_listed = False
    dut_ip_to_be_tested_list = []
    dut_ip_list = []
    dut_filename_list = []
    dut_ip_list_dict = { }
    """
    Directory paths
    """
    relativepath = ""
    initial_directory = relativepath + "/.AcmeAutomator/"
    profiles_directory = relativepath + "/.AcmeAutomator/profiles/"
    diagram = profiles_directory + "LABTopology.png"
    """"""
    # Template Seed File variables used to automate the process of seed file creation
    """"""
    templates_directory = relativepath + profiles_directory + "/.AcmeAutomator/templates/"
    templates_list = []
    template_file = ""
    template_seed_directory = relativepath + profiles_directory + "/.AcmeAutomator/templateseed/"
    template_seed_list = []
    template_seed_file = ""
    show_file_list = []
    search_filename = None
    """"""
    inventory_directory = "./"
    inventory_file_directory = "./"
    """
    HTML Hex Colors as found at www.w3schools.com/colors/
    """
    # color chart string definitions
    # "#RRGGBB"
    # RR = RED
    # GG = GREEN
    # BB = BLUE
    BLACK       = "#000000"
    YELLOW      = "#FFFF00"
    LIGHTYELLOW = "#FFFFD7"
    RED         = "#FF0000"
    DARKRED     = "#5F0000"
    LIGHTGREEN  = "#00FF00"
    GREEN       = "#008000"
    BLUE        = "#0000FF"
    DARKGREEN   = "#00aa00"
    """
    Canned messages 
    """
    # CRITICAL This are designed to be used with the "format" calls aka [string].format()
    # CRITICAL therefore "{" and "}" will need doubling if used.
    NORMAL_MESSAGE = "<span style=\"font-size:8pt; font-weight:normal;\" >"
    BOLD_MESSAGE = "<span style=\"font-size:10pt; font-weight:bold;\" >"
    RED_ONLY_MESSAGE = "<span style=\" color:red;\" >"
    RED_BOLD_ONLY_MESSAGE = "<span style=\"font-weight:bold; color:red;\" >"
    ORANGE_MESSAGE = "\"color\":\"orange\",\"weight\":\"extrabold\",\"fontsize\":\"12\",\"text\":\""
    BLACK_MESSAGE = "\"color\":\"black\",\"weight\":\"normal\",\"fontsize\":\"12\",\"text\":\""
    RED_MESSAGE = "\"color\":\"red\",\"weight\":\"extrabold\",\"fontsize\":\"12\",\"text\":\""
    RED_MESSAGE_oldway = "<span style=\"font-size:12pt; font-weight:bold; color:red;\" >"
    BLUE_FONT1O_BOLD_MESSAGE = "<span style=\"font-size:10pt; font-weight:bold; color:blue;\" >"
    BLUE_ONLY_MESSAGE = "<span style=\"color:blue;\" >"
    BLUE_MESSAGE = "<span style=\"font-size:12pt; font-weight:bold; color:blue;\" >"
    PURPLE_MESSAGE = "<span style=\"font-size:16pt; font-weight:bold; color:purple;\" >"
    SPAN_END_MESSAGE = "\""
    SPAN_END_MESSAGE_oldway = "</span>"
    PROFILES_DIRECTORY_MESSAGE = \
        "<span style=\" font-size:12pt; font-weight:bold; color:blue;\" >" + "Profiles directory:  " + "</span>"
    PROFILES_DIRECTORY_CHANGE_MESSAGE = \
        "<span style=\" font-size:12pt; font-weight:bold; color:red;\" >" + "Profiles directory changed to:  " + "</span>"
    PLEASE_WAIT_MESSAGE = \
        "<span style=\" font-size:16pt; font-weight:bold; color:purple;\" >" + " *** PLEASE WAIT *** " + "</span>"
    """"""
    def __init__(self):
        self.name = " Globals"
    """"""
    def get_tba_globals( self ):
        return( Globals().dut_selections_listed,
                Globals().dut_ip_to_be_tested_list, Globals.dut_ip_list,
                Globals().dut_filename_list,
                Globals().dut_ip_list_dict,
                Globals().profiles_directory, Globals.diagram,
                Globals().RED_MESSAGE, Globals.BLUE_MESSAGE,
                Globals().PURPLE_MESSAGE, Globals.SPAN_END_MESSAGE,
                Globals().PROFILES_DIRECTORY_MESSAGE,
                Globals().PLEASE_WAIT_MESSAGE )
    """"""
    def get_playbook_list( self ):
        return (Globals( ).playbook_list)
    """"""
    def clear_playbook_list(self):
        """
        For some damn reason to clear this you MUST do value[:] = []
        value = [] will NOT clear the variable!
        """
        Globals().playbook_list[:] = []
        Globals().playbook_to_be_tested_list[:] = []
        return ()
    """"""
    def set_dut_ip_list_dict( self, new_dut_ip_item ):
        Globals().dut_ip_list_dict.append = new_dut_ip_item
        return (Globals().dut_ip_list_dict)
    """"""
    def get_dut_ip_list_dict( self ):
        return (Globals().dut_ip_list_dict)
    """"""
    def clear_dut_ip_list( self ):
        Globals().dut_ip_list = []
        return()
    """"""
    def set_dut_ip_list( self, new_dut_ip_item ):
        Globals().dut_ip_list.append = new_dut_ip_item
        return (Globals().dut_ip_list)
    """"""
    def get_dut_ip_list( self ):
        return (Globals().dut_ip_list)
    """"""
    def clear_dut_to_be_tested_list( self ):
        Globals().dut_ip_to_be_tested_list[:] = []
        return ()
    """"""
    def get_dut_to_be_tested_list( self ):
        return ( Globals().dut_ip_to_be_tested_list )
    """"""
    def set_dut_to_be_tested_list( self, new_dut_ip_item ):
        Globals().dut_ip_to_be_tested_list.append = new_dut_ip_item
        return ( Globals().dut_ip_to_be_tested_list )
    """"""
    def get_show_file_list( self ):
        return ( Globals().show_file_list )
    """"""
    def set_show_file_list( self, show_filename ):
        Globals().show_file_list.append( show_filename )
        return ( Globals().show_file_list )
    """"""
    def clear_show_file_list( self ):
        Globals.show_file_list = []
        return()
    """"""
    def get_templates_list( self ):
        return (Globals.templates_file_list)
    """"""
    def get_template_seed_list( self ):
        return (Globals.template_seed_files_list)
    """"""
    def clear_template_seed_list( self ):
        Globals.template_seed_files_list[:] = []
        return()
    """"""
    def clear_template_seed_to_be_built_list( self ):
        Globals.template_seed_files_to_be_built_list[:] = []
        return()
    """"""
    def get_template_seed_files_to_be_built_list( self ):
        return (Globals.template_seed_files_to_be_built_list)
    """"""
    def clear_templates_list( self ):
        Globals.templates_file_list[:] = []
        return()
    """"""
    def clear_templates_to_be_built_list( self ):
        Globals.templates_to_be_built_list[:] = []
        return()
    """"""
    def get_templates_to_be_built_list( self ):
        return (Globals.templates_to_be_built_list)
"""
PRINT function color setter class
USE:  print( "{}{}{}{}".format( "My color is", bcolors.OKBLUE, "blue", bcolors.ENDC ) )
"""
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
"""
End of File
"""

