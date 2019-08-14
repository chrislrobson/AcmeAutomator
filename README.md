# AcmeAutomator
Network device management and testing tool (my retirement fun project ;-)

This project is a desktop application (anti-web app ;-) to manage and test network devices (either hosts, routers or switches).

The project is still under development, so documentation is slim, bugs exist, new and old deprecated code prevails so use at your own risk.

Python 3 (Python 2 not support) is the core language (anti-java coder here :-).

PyQt5 is the core desktop GUI used.

The project was inspired by years of watching network engineers (me being one) "hand-jamming" configurations, painfully cutting/pasting statistical data collected into reports, followed by long hours reviewing/analyzing the data looking for anomalies (errors, things out of order), further still then having to spend time generating the results.

This project attempts to automate, end-to-end, the network device testing processes, from device configuraiton, statistical data collection to data analysis and automating anomaly reporting.

A use case example (actually used in its early first release development stages) is router operating system upgrade validation and performance impact studies.  Specifically, this software was used to validate OS upgrade testing of Juniper MX series and CISCO ASR series routers.

History.  The first release was a quick and dirty prototype to address a job requirement, written in Python 2 with very limited GUI features (using PyQt4).  Then after retiring and bored, I rewrote the entire system in Python 3 using PyQt5, added threading and many enhancements.  For a short 3 month period, I rewrote the system in C++(Qt5) but abandoned that effort when it didnt prove to add much benefit (and wasn't as much fun as Python coding :-), switching back Python 3.
