"""
Received Mac Filter Data Dictionary
MODULE:  Mac Filter Data Dictionary
Author: Christopher Robson
Copyright by:  Christopher Robson
Copyright date: 08Oct2017
!! THIS CLASS IS PROPRIETARY AND MAY NOT BE REUSED BY ANYONE BUT THE AUTHOR!!
THIS MODULE DOES NOT BELONG TO ANY CONTRACTING COMPANY OR THE GOVERNMENT!
IT WAS DEVELOPED ON THE AUTHORS OWN PERSONAL TIME !!!!!!!!!!!!!!!!!!!!
This software is not FREE!  Use or destribution of the software system and its
subsystem modules, libraries, configuration file and "seed" file without the
express permission of the author is strictly PROHIBITED!
FUNCTION:  This data structure contains the "show interface extensive"
           MAC/Filter tags for analysis engine
"""
macfilterselector = \
   [
     # Mac statistics
     ("Total octets ","total octets receive: total octets transmit:"),
     ("Total packets ","total packets receive: total packets transmit:"),
     ("Unicast packets ","unicast packets receive: unicast packets transmit:"),
     ("Broadcast packets ","broadcast packets receive: broadcast packets transmit:"),
     ("Multicast packets ","multicast packets receive: multicast packets transmit:"),
     ("CRC/Align errors ","crc/align errors receive: crc/align errors transmit:"),
     ("FIFO errors ","fifo errors receive: fifo errors transmit:"),
     ("MAC control frames ","control frames receive: control frames transmit:"),
     ("MAC pause frames ","pause frames receive: pause frames transmit:"),
     ("Oversized frames ","oversized frames receive:"),
     ("Jabber frames ","jabber frames receive:"),
     ("Fragment frames ","fragment frames receive:"),
     ("VLAN tagged frames ","vlan tagged frames receive:"),
     ("Code violations ","code violations receive:"),
     ("Total errors ","total errors receive: total errors transmit:")
   ]
"""
END of FILE
"""
