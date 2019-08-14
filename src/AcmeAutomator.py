#!/usr/bin/python3
"""*****************************************************************************************************************
* FILE: AcmeAutomator.py
* PROJECT: AcmeAutomtor data collection analysis reporting automation system
* Author: Christopher Robson
* Copyright by:  Christopher Robson
* Copyright date: 01Jan2016
!!!!!!!!!!!!!!! COPYRIGHT WARNING !!!!!!!!!!!!!!!!!!
THIS SYSTEM IS PRIVATELY OWNED AND MAY NOT BE REUSED BY ANYONE BUT THE AUTHOR
UNLESS GIVEN PERMISSION BY THE AUTHOR.
While it is impossible for the author to review every single Python program on the Internet,
to date nothing has been found resembling this system, more specifically the unique extent of
design and technology used within this system and its network device anomaly analysis processing
and reporting.
This software is not FREE!  Use or distribution of the software system and its
subsystem modules, libraries, configuration file and "seed" file without the
express permission of the author is strictly PROHIBITED!
* While the author has obviously no time to review every single Python program on the Internet,
* to date nothing has been found resembling the technic and more specifically the extent of
* typical network device responses collected included wihtin this system.
* This software is not FREE!  Use or distribution of the software system and its
* subsystem modules, libraries, configuration file and "seed" file without the
* express permission of the author is strictly PROHIBITED!
* Yes I will sue your ass off if you decode, distribute or do ANYTHING without my expressed permission.
* This includes any government agency, any company or any employee of those orgainizations.
* THIS IS NOT FREE SOFTWARE
* FUNCTION:  Main GUI interface.  Starting point of this system.
***************************************************************************************************************"""
"""
LIBRARIES:  Python libraries
"""
import sys
import time
from PyQt5 import QtWidgets
"""
LIBRARIES:  Acme Automator specific libraries
"""
from GuiStart import GuiStart
from PopupWindow import ImageDisplay, PopupListWindow
from CommandLineArguementParser import CommandLineArguementParser
"""
CLASS: AcmeAutomator
DESCRIPTION: Acme Automator main function
INPUT: Command liine options
OUTPUT: Test results
"""
def AcmeAutomator():
    sys_argv = sys.argv
    parser = CommandLineArguementParser().command_line_arguement_parser( )
    args = parser.parse_args( )
    app = QtWidgets.QApplication( sys_argv )
    form = GuiStart( args )
    form.show( )
    """
    Dump command line options
    """
    if args.command_line_dump:
        command_line_options_list = "{}".format("Acme Automator Command Line Arguments")
        for line in repr( args ).split(", "):
            command_line_options_list += "{}".format(line.replace( "=", " = " )) + "\n"
        # fixme VERTICAL scroll nNOT WORKING HERE !!!!!!!!!!!!!!!!!!!
        popup = PopupListWindow(title="Commandline Options", width = 800, height = 800)
        popup.write_popup_message(message = command_line_options_list, title = "Command Line Options")
    """
    Print vanity window, 
    Assign it to a variable so it stays alive, else it will never display
    """
    if args.welcomeframed:
        welcome_image = "AcmeAutomatorWelcome.png"
        welcome_title = "Welcome to the Acme Automator"
        keep_it_alive = ImageDisplay(title=welcome_title, image=welcome_image, framed=args.welcomeframed)
    """
    Execute system
    """
    app.exec_( )
"""
CLASS: main
DESCRIPTION: Acme Automator main function
INPUT: Command liine options
OUTPUT: Test results
"""
if __name__ == "__main__":
    main = AcmeAutomator()
"""**********************************************************************************************
End of file
**********************************************************************************************"""

