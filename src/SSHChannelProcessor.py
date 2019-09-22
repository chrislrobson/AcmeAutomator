"""************************************************************************************************
Python SSHCahnnelProcessor
MODULE:   SSH Channel Processor
Author: Christopher Robson
Copyright by:  Christopher Robson
Copyright date: 01Jan2016
This software is not FREE!  Use or destribution of the software system and its
subsystem modules, libraries, configuration file and "seed" file without the
express permission of the author is strictly PROHIBITED!
FUNCTION:  Module provides the results from a network device "configure save" command suite.
           Message passing between the GUI and the testing modules is accomplished
           using Qt5 "Signal and Slot" processing system.
***********************************************************************************************"""
"""
Python Libraries
"""
import paramiko
import time
import re
import os
import socket
""""""
"""
Home grown libraries
"""
from Globals import *
from Exceptions import *
from NormalizeData import NormalizeData
""""""
"""
CLASS: SSHChannel
FUNCTION: Set up channel between devices
INPUT:
OUTPUT:
"""
class SSHChannel( object ):
    "SSH Channel"
    """"""
    def __init__( self, parent = None ):
        self.name = self.__class__.__name__
        self.parent = parent
        self.gparent = parent.parent
    """"""
    def ssh_channel_initilization( self, ssh_connection_dict ):
        """
        Start by initializing the prompt string processor object.  This object is used to scan each
        data received buffer for a session terminating string from a session transmitted command
        to a device.
        """
        try:
            ssh_connection_dict['processreply'].set_prompt_string(ssh_connection_dict['prompt'], "Continue")
        except:
            ssh_connection_dict['processreply'].set_prompt_string(ssh_connection_dict['#'], "Continue")
        try:
            self.ssh_ip = ssh_connection_dict['ip']
        except:
            raise MissingDictionaryEntry( "{}: SSH_CONNECTION_DICT[ip] is missing!".format(self.name) )
        try:
            self.ssh_host = ssh_connection_dict['host']
        except:
            self.ssh_host = self.ssh_ip
        """
        SSH_DEVICE needed to handle stupid Cisco dynamic replies, OMG I hate that company!
        """
        try:
            self.ssh_device = ssh_connection_dict['device']
        except:
            self.ssh_device = ""
        try:
            if ssh_connection_dict['username'] == "NONE":
                self.ssh_username = Globals.user_to_use
            else:
                self.ssh_username = ssh_connection_dict['username']
        except:
            raise MissingDictionaryEntry("{}: SSH_CONNECTION_DICT[username] is missing!".format(self.name))
        try:
            if ssh_connection_dict['password'] == "NONE":
                self.ssh_password = Globals.password_to_use
            else:
                self.ssh_password = ssh_connection_dict['password']
        except:
            self.ssh_password = ""
        try:
            self.ssh_port = int( float( ssh_connection_dict['port'] ) )
        except:
            raise MissingDictionaryEntry("{}: SSH_CONNECTION_DICT[port] is missing!".format(self.name))
        try:
            self.ssh_secret = ssh_connection_dict['secret']
        except:
            raise MissingDictionaryEntry("{}: SSH_CONNECTION_DICT[secret] is missing!".format(self.name))
        try:
            self.ssh_verbose = ssh_connection_dict['verbose']
        except:
            self.ssh_verbose = False
        try:
            self.ssh_delay = float( ssh_connection_dict['delay'] )
        except:
            self.ssh_delay = .1
        try:
            self.ssh_timeout = ssh_connection_dict['sshtimeout']
        except:
            self.ssh_timeout = 8
        try:
            self.ssh_use_keys = ssh_connection_dict['usekeys']
        except:
            self.ssh_use_keys = False
        try:
            self.ssh_key_file = int( float( ssh_connection_dict['keyfile'] ) )
        except:
            self.ssh_key_file = None
        try:
            self.ssh_use_key_policy = ssh_connection_dict['usekeypolicy']
            self.ssh_key_policy = paramiko.RejectPolicy()
        except:
            self.ssh_key_policy = paramiko.AutoAddPolicy()
        try:
            self.ssh_use_system_host_keys = ssh_connection_dict['usesystemhostkeys']
        except:
            self.ssh_use_system_host_keys = False
        try:
            self.ssh_use_alternate_host_keys = ssh_connection_dict['usealternatehostkeys']
        except:
            self.ssh_use_alternate_host_keys = False
        try:
            self.ssh_alternate_key_file = int( float( ssh_connection_dict['alternatekeyfile'] ) )
        except:
            self.ssh_alternate_key_file = None
        #-----------------------------------------------------------------------------------------------
        try:
            self.ssh_proxy_configuration_file = ssh_connection_dict['proxyconfigurationfile']
        except:
            self.ssh_proxy_configuration_file = None
        """
        Convert Paramiko connection parameters to a dictionary
        """
        self.paramiko_dict = \
            {
                'hostname':self.ssh_host,
                'port':self.ssh_port,
                'username':self.ssh_username,
                'password':self.ssh_password,
                'look_for_keys':self.ssh_use_keys,
                'allow_agent':False,
                'key_filename':self.ssh_key_file,
                'timeout':self.ssh_timeout,
            }
        """
        Check if using SSH 'config' file mainly for SSH proxy support (updates ssh_connect_params)
        """
        if self.ssh_proxy_configuration_file:
            self.ssh_proxy_configuration_file( self.paramiko_dict )
        """
        Create instance of SSHClient object
        """
        self.ssh_connection_pre = paramiko.SSHClient()
        """
        Load host_keys for better SSH security
        """
        if self.ssh_use_system_host_keys:
            self.ssh_connection_pre.load_system_host_keys()
        if self.ssh_use_alternate_host_keys and os.path.isfile( self.ssh_alternate_key_file ):
            self.ssh_connection_pre.load_host_keys( str( self.ssh_alternate_key_file ) )
        """
        Default is to automatically add untrusted hosts (make sure appropriate for your env)
        """
        self.ssh_connection_pre.set_missing_host_key_policy( self.ssh_key_policy )
        """
        initiate SSH connection
        """
        try:
            self.ssh_connection_pre.connect( **self.paramiko_dict )
        except socket.error as error:
            raise SSHSocketError( "{}: Socket Error: {}:{}, error is: {}.".format(self.name, self.ssh_host, self.ssh_port, error.args[0] ) )
        except paramiko.ssh_exception.AuthenticationException as auth_err:
            raise SSHReadAuthenicationError( "{}: Authentication failure: "
                                             "unable to connect {ip}:{port}\n {msg}".format(self.name,
                                                                                            ip = self.ssh_host, port = self.ssh_port,  msg = str(auth_err) ) )
        """
        Setup the ineteractive shell connection and then wait a second for it to stablize
        """
        self.ssh_connection = self.ssh_connection_pre.invoke_shell()
        self.ssh_connection.settimeout( self.ssh_timeout)
        self.parent.ssh_handle = self.ssh_connection
        if self.ssh_verbose:
            self.message_str = "Interactive SSH session established."
            self.gparent.logger_message_signal.emit( self.message_str )
        return( self.ssh_connection )
    """"""
    def ssh_proxy_configuration( self, paramiko_dict ):
        """
        Update SSH connection parameters based on contents of SSH 'config' file
        This method modifies the connect_dict dictionary, returns None
        Use SSHConfig to generate source content.
        """
        try:
            ssh_config_instance = paramiko.SSHConfig()
            with open( self.parent.ssh_proxy_configuration_file ) as f:
                ssh_config_instance.parse(f)
                host_specifier = "{0}:{1}".format( self.parent.ssh_host, self.parent.ssh_port )
                source = ssh_config_instance.lookup( host_specifier )
        except:
            source = {}
        """"""
        if source.get( 'proxycommand' ):
            proxy = paramiko.ProxyCommand( source['proxycommand'] )
        elif source.get('ProxyCommand'):
            proxy = paramiko.ProxyCommand( source['proxycommand'] )
        else:
            proxy = None
        """
        Only update 'hostname', 'sock', 'port', and 'username'
        For 'port' and 'username' only update if using object defaults
        """
        if paramiko_dict['port'] == 22:
            paramiko_dict['port'] = int(source.get('port', self.parent.ssh_port))
        if paramiko_dict['username'] == '':
            paramiko_dict['username'] = source.get('username', self.parent.ssh_username)
        if proxy:
            paramiko_dict['sock'] = proxy
        paramiko_dict['hostname'] = source.get('hostname', self.parent.ssh_host)
        return()
"""
CLASS: SendDataThroughSSHChannel
FUNCTION: Sends data between devices through ssh channel
INPUT:  Sending data
OUTPUT: Received data
NOTE:  Its important(critical actually) that the commands to remove paused output
(such as Juniper's "no-more" and Cisco's "term length 0") be implemented and character
screen length (such as Juniper's "set cli screen-width 1024" and Cisco's "term width 512")
be implemented or the receiver will either truncate input or hang!!
"""
class SendDataThroughSSHChannel(SSHChannel):
    "Send Data Through SSH Channel"
    """"""
    def __init__(self, parent = None):
        super( SendDataThroughSSHChannel, self).__init__(parent)
        self.name = self.__class__.__name__
        self.parent = parent
        self.ssh_connection = self.parent.ssh_handle
        self.data_buffer_size = Globals().SSHRECEIVETRANSMITBUFFER
    """"""
    def send_data_through_ssh_channel(self, dictionary = None, data = "", delay = .5, read_timeout = 90):
        self.elapse_time = time.time() + read_timeout
        self.data = data
        self.delay = delay
        self.cmd_dict = dictionary
        """"""
        try:
            self.clear_buffer()
        except Exception as error:
            raise Exception("{}: {}".format(self.name, error))
        try:
            # todo-debug
            # todo-debug self.parent.ggparent.logger_message_signal.emit(self.data)
            # todo-debug print("{}(self.data): {}".format(self.name, self.data))
            # todo-debug
            self.ssh_connection.sendall("{}\n".format(self.data.rsplit('\n')[0])) # Assure command string is terminated with carriage return
            """
            Be ready for the top level call to put a delay in.  Typically this is used with file transfer commands such
            as Juniper "file copy".  What happens without it is this:  Paramiko is still reading data when the call to
            self.ssh_connection.recv() is made, which will return data but NOT all the data being transmitted from the
            router and reading by Paramiko before completing the transfer.  By putting a half-second delay (or more) this
            allows Paramiko time to complete the reading of incoming data.  Typically, this delay is NOT required by
            other commands such as show.  File transfers are much slower.
            """
            time.sleep(self.delay * 1)
        except socket.error as error:
            self.ssh_connection.close()
            self.message = "{{{}{}: data error: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
            self.cmd_dict['loggerwidget'].emit(self.message)
            raise Exception
        except Exception as error:
            self.message = "{{{}{}: data error: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
            self.cmd_dict['loggerwidget'].emit(self.message)
            raise Exception
        self.output = ""
        for justincaseloopcnt in range(512):
            """
            Because of Cisco's horrible formatted replies we have to look back some "guessed" amount
            of characters so we can determine how to process the reply.  This issue is ONLY with
            Cisco devices, so up yours!
            """
            if self.ssh_connection.recv_ready():
                try:
                    self.output += self.ssh_connection.recv( self.data_buffer_size ).decode('utf-8', 'ignore')
                    # todo-debug
                    # todo-debug self.cmd_dict['loggerwidget'].emit(self.output)
                    # todo-debug print("{}(self.output): {}".format(self.name, self.output))
                    # todo-debug
                    self.output_normalized = NormalizeData(self).normalize_data(dictionary = self.cmd_dict, data = self.output)
                    self.output_split = self.output_normalized.split()
                    self.buff_word_count = 50
                    self.output_word_count = len(self.output_split)
                    if self.output_word_count < self.buff_word_count:
                        self.buff_word_count = self.output_word_count
                except Exception as error:
                    self.message = "{{{}{}: data receive error: {}{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                    self.cmd_dict['loggerwidget'].emit(self.message)
                    raise Exception
                try:
                    self.last_word = " ".join(self.output_split[-self.buff_word_count:])
                    if self.last_word:
                        self.reply_action = self.cmd_dict['processreply'].find_prompt(self.last_word, self.cmd_dict['processreply'].prompt_automation)
                        if self.reply_action:
                            break
                except Exception as error:
                    self.message = "{{{}{}: error {} scanning for prompt character!{}}}".format(Globals.RED_MESSAGE, self.name, error, Globals.SPAN_END_MESSAGE)
                    self.cmd_dict['loggerwidget'].emit(self.message)
                    raise Exception
                self.elapse_time = time.time() + read_timeout
            else:
                """
                Typically there isnt a delay teherefore long scan the receive buffer for why a prompted wasnt found, 
                for example a logout terminating message from host.  In some cases the prompt string may change
                such as when ssh'ing to a host followed by new command to run a CLI which has a different prompt string.
                For example the sequence:
                ssh -l username hostIP
                telnet 127.0.0.1 port (at this point the target host, if this port is busy will force a logout)
                otherwise....
                Look to see if it maybe an unknown prompt by checking the last character as either a "#" or "$" and assume its a new prompt.
                """
                self.possible_prompt = self.output.replace('\r',' ').replace('\n',' ').split()[-1]
                self.reply_action = self.cmd_dict['processreply'].find_prompt_full_scan(self.output, self.cmd_dict['processreply'].prompt_automation)
                if self.reply_action:
                    break
                elif self.possible_prompt.endswith('#') or self.possible_prompt.endswith('$'):
                    self.cmd_dict['processreply'].set_prompt_string(self.possible_prompt, "Continue")
                    break
                """
                Didnt find prompt so possibly nothing came in yet, so wait and try again.
                """
                time.sleep(self.delay * 1)
                # todo-debug
                # todo-debug a = int(self.delay + 1)
                # todo-debug print("Timed delayed count:{}".format(a))
                # todo-debug
            """
            Typically, this isnt hit unless no prompt string is found.  Since the usual "#" and "$" ending characters have been check for
            already, this means a new prompt string has come in and needs to be applied to the "ReceivedDataReplyDictionary.py" manually.
            We could just grap the last word of the buffer and make it a new prompt but there is no way to know if its not a corruptted
            buffer.  Ergo just time out and let the software engineer debug for a possible new string to be coded.
            """
            if self.elapse_time < time.time():
                self.message = "{{{}{}: Timeout while waiting for received data containing expected termination character!{}}}".format(Globals.RED_MESSAGE, self.name, Globals.SPAN_END_MESSAGE)
                self.cmd_dict['loggerwidget'].emit(self.message)
                raise Exception
        else:  # nobreak#
            self.message = "{{{}{}: No prompt string was received, unexpected termination of buffer read!{}}}".format(Globals.RED_MESSAGE, self.name, Globals.SPAN_END_MESSAGE)
            self.cmd_dict['loggerwidget'].emit(self.message)
            raise Exception
        return(self.output)
    """"""
    def clear_buffer(self):
        if self.ssh_connection.recv_ready():
            return(self.ssh_connection.recv(Globals().SSHRECEIVETRANSMITBUFFER ).decode('utf-8', 'ignore'))
        else:
            return(None)
"""****************************************************************************************************
End of File
****************************************************************************************************"""
