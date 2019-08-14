"""****************************************************************************************
Received Decode Juniper Data Dictionary
MODULE:  Decode Juniper Data Dictionary
Author: Christopher Robson
Copyright by:  Christopher Robson
Copyright date: 08Oct2017
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
FUNCTION:  This data structure contains, for example,  the "show interface detail"
           start of a line which is used to call the class that will
           decode and process the associated data.  Classes are defined in the
           file "DecoderProcessor.py".
****************************************************************************************"""
from DecodeDataProcessor import *
decoders = \
   [
     ("Physical interface:", "PhysicalInterface"),
     ("Interface index:", "DecoderProcessor"),
     ("Type:", "DecoderProcessor"),
     ("Description:", "Description"),
     ("Link-level type:", "DecoderProcessor"),
     ("Speed:", "DecoderProcessor"),
     ("Loopback:", "DecoderProcessor"),
     ("Clocking:", "DecoderProcessor"),
     ("Pad to minimum frame size:", "DecoderProcessor"),
     ("Device flags:", "DecoderProcessor"),
     ("Interface flags:", "DecoderProcessor"),
     ("Link type:", "DecoderProcessor"),
     ("Link flags:", "DecoderProcessor"),
     ("Schedulers:", "DecoderProcessor"),
     ("Interface preservation:", "DecoderProcessor"),
     ("LCP state:", "DecoderProcessor"),
     ("NCP state:", "DecoderProcessor"),
     ("CHAP state:", "DecoderProcessor"),
     ("PAP state:", "DecoderProcessor"),
     ("Hold-times:", "DecoderProcessor"),
     ("Damping:", "DecoderProcessor"),
     ("Current address:", "CurrentAddress"),
     ("Last flapped:", "LastFlapped"),
     ("Statistics last cleared:", "StatisticsLastCleared"),
     ("Ingress traffic statistics at Packet Forwarding Engine:", "IngressTrafficStatisticsAtPacketForwardingEngine"),
     ("Ingress queues:", "EgressIngressCoSQueues"),
     ("Egress queues:", "EgressIngressCoSQueues"),
     ("CoS queues:", "EgressIngressCoSQueues"),
     # the follow are sub-classes to class "EgressIngressCoSQueues"
     # therefor called via that class
     # ("Queue counters:", "QueueCounters"),
     # ("Queue number:", "QueueNumber"),
     ("Frame exceptions:", "FrameExceptions"),
     ("Buffering exceptions:", "BufferingExceptions"),
     ("Assembly exceptions:", "AssemblyExceptions"),
     ("Hardware errors (sticky):", "HardwareErrorsSticky"),
     ("Bundle links information:", "BundleLinksInformation"),
     ("Bundle options:", "BundleOptions"),
     ("Statistics Frames fps Bytes bps", "StatisticsFramesFpsBytesBps"),
     # the follow are sub-classes to class "StatisticsFramesFpsBytesBps"
     # therefor called via that class
     #  ("Link:", "Link"),
     #  ("Multilink detail statistics:", "MultilinkDetailStatistics"),
     #  ("IPV6 Transit Statistics Packets Bytes", "IPV6TransitStatisticsPacketsBytes"),
     ("Multilink class 0 status:", "MultilinkClassStatus"),
     ("Active alarms:", "DecoderProcessor"),
     ("Active defects:", "DecoderProcessor"),
     ("Received SONET overhead:", "ReceivedTransmittedSonetOverheadProcessor"),
     ("Transmitted SONET overhead:", "ReceivedTransmittedSonetOverheadProcessor"),
     ("Received path trace:", "ReceivedTransmittedPathTraceProcessor"),
     ("Transmitted path trace:", "ReceivedTransmittedPathTraceProcessor"),
     ("Payload pointer", "PayloadPointerProcessor"),
     ("SONET", "SonetProcessor"),
     #  ("SONET alarms:", "DecoderProcessor"),
     #  ("SONET defects:", "DecoderProcessor"),
     ("Keepalive settings:", "DecoderProcessor"),
     ("Keepalive statistics:", "KeepaliveStatistics"),
     ("PCS statistics", "PCSStatistics"),
     ("CE info", "CEInfo"),
     ("VCI", "VCIWrapper"),
     ("ATM status:", "AtmStatusProcessor"),
     ("ATM Statistics:", "AtmStatisticsProcessor"),
     ("T1 media:", "DecoderProcessorWrapper"),
     # handled by above wrapper - ("T1 media:", "T1Ds3Processor"),
     ("DS3 media:", "DecoderProcessorWrapper"),
     # handled by above wrapper - ("DS3 media:", "T1Ds3Processor"),
     ("DSU configuration:", "DecoderProcessorWrapper"),
     ("DS1 alarms:", "DecoderProcessorWrapper"),
     ("DS1 defects:", "DecoderProcessorWrapper"),
     ("DS1 BERT configuration:", "DecoderProcessorWrapper"),
     ("DS1 thresholds:", "DecoderProcessorWrapper"),
     ("DS3 alarms:", "DecoderProcessorWrapper"),
     ("DS3 defects:", "DecoderProcessorWrapper"),
     ("DS3 BERT configuration:", "DecoderProcessorWrapper"),
     ("DS3 thresholds:", "DecoderProcessorWrapper"),
     ("Preclassifier statistics:", "PreclassifierStatistics"),
     ("Interface transmit statistics:", "InterfaceTransmitStatistics"),
     ("Logical interface", "LogicalInterface"),
     ("Flags:", "DecoderProcessor"),
     ("Bandwidth:", "DecoderProcessor"),
     ("Label-switched interface (LSI) traffic statistics:", "LabelSwitchedTrafficStatistics"),
     ("Dropped traffic statistics due to STP State:", "DroppedTrafficStatistics"),
     ("Input errors:", "InputOutputErrorsProcessor"),
     ("Output errors:", "InputOutputErrorsProcessor"),
     ("MAC statistics:", "MacStatistics"),
     ("Filter statistics:", "FilterStatistics"),
     ("CoS information:", "CosInformation"),
     ("Autonegotiation information:", "AutonegotiationInformation"),
     ("Packet Forwarding Engine configuration:", "PacketForwardingEngineConfiguration"),
     ("HDLC configuration:", "HdlcSatopConfiguration"),
     ("SAToP configuration:", "HdlcSatopConfiguration"),
     ("Traffic statistics:", "TrafficStatistics"),
     ("Local statistics:", "LocalStatistics"),
     ("Max nh cache:", "DecoderProcessor"),
     ("Protocol inet, MTU:", "ProtocolInetMtu"),
     ("Protocol inet6, MTU:", "ProtocolInet6Mtu"),
     ("Protocol multiservice, MTU:", "ProtocolMultiserverMtu"),
     ("Protocol vpls, MTU:", "ProtocolVplsMtu"),
     ("Protocol iso, MTU:", "ProtocolIsoMtu"),
     ("Protocol mpls, MTU:", "ProtocolMplsMtu"),
     ("Protocol ccc, MTU:", "ProtocolCccMtu"),
     ("Protocol 61, MTU:", "Protocol61Mtu"),
     ("Protocol 85, MTU:", "Protocol85Mtu"),
     ("Protocol tnp, MTU:", "ProtocolTnpMtu"),
     ("Protocol mlppp, Multilink bundle:", "ProtocolMlpppMultilinkBundle"),
     ("Flags:", "DecoderProcessor"),
     ("Addresses, Flags:", "DecoderProcessor"),
     ("Routing Instance:", "DecoderProcessor"),
     ("Destination:", "DecoderProcessor"),
     ("Broadcast:", "DecoderProcessor"),
     ("INET6 Address Flags:", "DecoderProcessor"),
     ("Policer:", "DecoderProcessorWrapper"),
     ("Physical info:", "DecoderProcessor"),
     ("Input Filters:", "DecoderProcessor"),
     ("Output Filters:", "DecoderProcessor"),
     ("Alternate link address:", "DecoderProcessor"),
     ("L2 circuit cell bundle size:", "DecoderProcessor"),
     # Generation is Juniper debug ergo ignore it
     ("Generation:", "NoOperation")
   ]
"""********************************************************************************************************
End of File
********************************************************************************************************"""
