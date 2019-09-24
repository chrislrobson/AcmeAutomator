# AcmeAutomator
Network device management and testing tool (my retirement fun project ;-)

This project is a desktop application (anti-web app ;-) to manage and test network devices (either hosts, routers or switches).

The project is still under development, so documentation is slim, bugs exist, new and old deprecated code prevails so use at your own risk.

Python 3 (Python 2 not support) is the core language (anti-java coder here :-).

PyQt5 is the core desktop GUI used.

The project was inspired by years of watching network engineers (me being one) "hand-jamming" configurations, painfully cutting/pasting statistical data collected into reports, followed by long hours reviewing/analyzing the data looking for anomalies (errors, things out of order), further still, then having to spend time generating the results.

This project attempts to automate, end-to-end, the network device testing processes, from device configuraiton, statistical data collection to data analysis and automating anomaly reporting.

A use case example (actually used in its early first release development stages) is router operating system upgrade validation and performance impact studies.  Specifically, this software was used to validate OS upgrade testing of Juniper MX series and CISCO ASR series routers.

The profiles directory contains example of files used by the system.  Typically, thesse files are referenced as "seed" files because they feed information to the software to control its actions.  It is suggested the reader study the format and use of these files since they control the action of the system.  Yes, the files can be complex, to overcome this complexity, early protoype code development to create an automated file generator has started.  However, this is a low priority effort.

Also, when considering making seed files, I try making individual files for each Device Under Test (DUT).  That is, if the test calls for a delay between sessions, instead of making a single file to support multiple DUT, I'll create a delay seed file for each DUT.  In this way, each device can be control independendly with out having to later go back and re-engineer a new seed file.  Basically, the design of a test's "Playbook" and "Story" telling is completely flexible and up to the engineer.  Experience from past testing, when I was first using the software on actually testing, quickly taught me, very painfilly I might add, individual seed files per DUT was faster, and much easier to manage and control, despite increasing the number of seed files.

UPDATES:

22Sep2019:  The PowerPoint file "AcmeAutoomator-BGP-OSPF-ISIS-Testbed.pptx" illustrates the baseline testbed used for this development effort.  All routers in the testbed are virtual machines running as guest systems on a iMAC host.  Each VM consist of a Fedora 30 XFCE spin running FRRouting software.  The testbed topology is fashioned after what might be a typical WAN-LAN topology using Customer-Edge routers connecting through ISP Provider-Edge and Provider core routers.  CE routers are configured as OSPF routers.  The PE routers exchange routes through BGP.  The P router core routes using ISIS.

History.  The first release was a quick and dirty prototype to address a job requirement, written in Python 2 with very limited GUI features (using PyQt4).  Then after retiring and bored, I rewrote the entire system in Python 3 using PyQt5, added threading and many enhancements.  For a short 3 month period, I rewrote the system in C++(Qt5) but abandoned that effort when it didnt prove to add much benefit (and wasn't as much fun as Python coding :-), switching back Python 3.

Required shell variable:  export STYLESHEETHOME=/$HOME/.AcmeAutomator/stylesheets

Example of command line run options:

/usr/bin/python3 AcmeAutomator.py -l 1 -t 1 -d -U AcmeAutomator -P AcmeAutomator -R ${pwd}/ -C .AcmeAutomator/.AcmeAutomator-Templates-Directory -g .AcmeAutomator/.AcmeAutomator-Diagram-File-Directory -m .AcmeAutomator/.AcmeAutomator-Profiles-Directory -S InventoryKeywordSearchList -I .AcmeAutomator/myARCHIVES/INVENTORIES-EXCEL-REPORTS/ -F .AcemAutomator/myARCHIVES/INVENTORIES-SHOW-REPORTS/ -E .AcmeAutomator/.AcmeAutomator-Template-Seed-Directory

Configuraiton notes:

AcmeAutomator is completely flexiable as to were associated configuration and report files are located but it is suggested these file (called seed file), output files and stylesheet files be located in the following directory structure:

AcmeAutomator root directory:

$HOME/.AcmeAutomator

Microsoft template files used for generating reports:

$HOME/.AcmeAutomator/REPORT-TEMPLATES

PyQt5 stylesheets:

$HOME/.AcmeAutomator/stylesheets

AcmeAutomator seed files:

$HOME/.AcmeAutomator/profiles

Report file storage:

$HOME/.AcmeAutomator/reports/[device name or IP]
