"""*********************************************************************************************************
Received Data Reply Dictionary
MODULE:  ReceivedDataReplyDictionary (C)
Author: Christopher Robson
Copyright by:  Christopher Robson
Copyright date: 01Jan2016
!!!!!!!!!!!!!!! COPYRIGHT WARNING !!!!!!!!!!!!!!!!!!
THIS CLASS IS PRIVATELY OWNED AND MAY NOT BE REUSED BY ANYONE BUT THE AUTHOR or AUTHOR'S PERMISSION!
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
FUNCTION:  Module provides prompt strings to scan for to indicate end of a block of data from a device.
The compare must be a exact as possible to overcome duplication producing WRONG replies
DONT HARD CODE PROMPTS HERE SUCH AS ( "test@", "Continue"),
it MUST be done via seed file "prompt" keyword!!!
notes:  When building the strings found, the class "Utility" will return a list of matching string found in
the database LIST.  Its CRITICAL, therefore, to have seed files coded with the prompt keyword as exact as possible.
For example, a given "complete prompt from a device might be as follows:
"tester@devicename>"
CRITICAL There for the seed file "prompt" keyword must be set to that exact string, "tester@devicename"
HOWEVER, notice the seed file's "prompt" keyword maybe better without including the trailing ">" (greater-than)
character.  Nor should the prompt keyword include a trailing "#" (number sign) character.  In this
way, the script can process replies without concern about which subsystem it is within,
(aka configuration mode, etc).  Another words in the seed file prompt keyword has a trailing ">"
character, then any script configuration commands will not be processed correctly. likewise
if the "#" character is the last prompt keyword character when in the command mode.
**********************************************************************************************************"""
prompts = \
   [
     ( "[yes,no] (no)", "SendYes"),
     ( "[yes,no](no)", "SendYes"),
     ( "[yes/no] (no)", "SendYes"),
     ( "[yes/no](no)", "SendYes"),
     ( "[yes,no]:", "SendYes"),
     ( "[yes/no]:", "SendYes"),
     ( "[yes,no]?", "SendYes"),
     ( "[yes/no]?", "SendYes"),
     ( "show configuration failed", "SendConfigurationFailed"),
     ( "Uncommitted changes found, commit them before exiting(yes/no/cancel)? [cancel]:", "SendNo"),
     ( "4 * * *", "SendCtrlC"),
     ( "4   *  *  *", "SendCtrlC"),
     ( "4 ? ? ? ", "SendCtrlC"),
     ( "4   ?  ?  ?", "SendCtrlC"),
     ( "....................", "SendCtrlC"),
     ( "UUUUUUUUUUUUUUUUUUUU", "SendCtrlC"),
     ( "ping: sendto: No route to host", "SendCtrlC"),
     ( "Do you wish to proceed? [no]:", "SendYes"),
     ( "continue connecting (yes/no)? ", "SendYes"),
     ( "Delete filename [", "SendYes"),
     ( "Delete everything under this level? [yes,no] (no)", "SendYes"),
     ( "Discard uncommitted changes? [yes,no] (yes)", "SendYes"),
     ( "Uncommitted changes found, commit them before exiting", "SendNo"),
     ( "Destination filename [", "SendYes"),
     ( "Please type 'yes' or 'no': ", "SendYes"),
     ( "[confirm]", "SendCarriageReturn"),
     ( "Destination file name (control-c to abort):", "SendCarriageReturn"),
     ( "Do you want to overwrite? [no]", "SendYes"),
     ( "Reset ISIS process", "SendYes"),
     ( "Are you sure you want to continue connecting (yes/no)? ", "SendYes"),
     ( "No such file or directory", "Continue"),
     ( "Building configuration..", "Continue"),
     ( "Disconnected", "Continue"),
     ( "Connecting to", "ReceiveMoreData"), #FIXME handles broken F'ing Cisco crap which splits this string into two transmissions MORONS!
     ( "Resolving mastership", "ResolvingMaster"),
     ( "Password:", "SendPassword"),
     ( "password:", "SendPassword"),
     ( "error: could not send local copy of file", "SendFileFailed"),
     ( "Permission denied", "PermissionDenied"),
     ( "Could not chdir to home directory", "IgnoreCommand"),
     ( "unknown command", "UknownCommand"),
     ( "Upload aborted.", "UploadAborted"),
     ( "% Invalid input detected at '^' marker", "SendCtrlC"),
     ( "% Couldn't open file ", "SendAbort"),
     ( "can't read key type", "KeyFailed"),
     ( "Not ready for mastership switch, try after", "WaitProcessor"),
   ]
"""
END of FILE
"""
