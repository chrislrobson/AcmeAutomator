####################################################################################################################
# PyQt5HostPauser
# This program runs as a stand alone pause
#
# To use this class, set up a seed file with the following configuration:
# {"hostcommand":{'device':'juniper','stdout':'Yes','fileoutput':'Yes','verbose':'No',
# 'loopcnt':'240','delay':'.5','prompt':'test@T4K-P90-re','secondaryprompt':'password:',
# 'additionalprompt':'(yes/no)?','commandpath':'./.AcmeAutomator/myARCHIVES/profiles/OS-TESTING/',
# 'commands':'192.168.69.28-p90-PyQt5TestbedAutomatorHostPauser.prf','pwd':'geTest',
# 'savepath':'./.AcmeAutomator/myARCHIVES/OS-TESTING/192.168.69.28/',
# 'filename':'192.168.69.28-p90-DIFF-Compare-Report'}};
#
# The conent of 192.168.69.28-p90-PyQt5TestbedAutomatorHostPauser.prf is either one of these:
#  python ./PyQt4TestbedAutomatorHostPauser.py [delay time] typically "240"
#  OR
#  /usr/local/bin/PyQt5TestbedAutomatorHostPauser [delay time] typically "240"
####################################################################################################################
import sys
import time
#-------------------------------------------------------------------------------------------------------------------
class PyQt5TestbedAutomatorPauser( ):
  def __init__( self, time_delay ):
    time.sleep( int( float( time_delay ) ) )
#--------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
  try:
    time_delay = sys.argv[1]
  except:
    print( "Usage:  TestbedAutomatorPauser [delay in seconds]" )
    sys.exit( 1 )
  print( "Pausing system for %s seconds" % time_delay )
  PyQt5TestbedAutomatorPauser( time_delay )
  print( "Timer has exspired" )
#####################################################################################################################