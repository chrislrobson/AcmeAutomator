#!/bin/sh
pwd=`pwd`
cd src
/usr/bin/python3 AcmeAutomator.py -l 1 -t 1 -d -U AcmeAutomator -P AcmeAutomator -R ${pwd}/ -C .AcmeAutomator/.AcmeAutomator-Templates-Directory -g .AcmeAutomator/.AcmeAutomator-Diagram-File-Directory -m .AcmeAutomator/.AcmeAutomator-Profiles-Directory -S InventoryKeywordSearchList -I .AcmeAutomator/myARCHIVES/INVENTORIES-EXCEL-REPORTS/ -F .AcemAutomator/myARCHIVES/INVENTORIES-SHOW-REPORTS/ -E .AcmeAutomator/.AcmeAutomator-Template-Seed-Directory
