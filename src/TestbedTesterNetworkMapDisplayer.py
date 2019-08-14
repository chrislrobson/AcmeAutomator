####################################################################################################################
# PyQt5TestbedAutomatorPauseButton
# This program runs as a stand alone  network map displayer
#
# To use this class, set up a seed file with the following configuration:
# {"hostcommand":{'device':'juniper','stdout':'Yes','fileoutput':'Yes','verbose':'No',
# 'loopcnt':'240','delay':'.5','prompt':'test@T4K-P90-re','secondaryprompt':'password:',
# 'additionalprompt':'(yes/no)?','commandpath':'./.AcmeAutomator/myARCHIVES/profiles/OS-TESTING/',
# 'commands':'192.168.69.28-p90-PyQt4TestbedAutomatorPauseButton.prf','pwd':'geTest',
# 'savepath':'./.AcmeAutomator/myARCHIVES/OS-TESTING/192.168.69.28/',
# 'filename':'192.168.69.28-p90-DIFF-Compare-Report'}};
#
# The conent of 192.168.69.28-p90-PyQt4TestbedAutomatorPauseButton.prf is either one of these:
#  python ./PyQt5TestbedAutomatorPauseButton.py [delay time] typically "240"
#  OR
#  /usr/local/bin/PyQt5TestbedAutomatorPauseButton [delay time] typically "240"
####################################################################################################################
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import time
#-------------------------------------------------------------------------------------------------------------------
class IsisMap( QWidget ):
  def __init__( self, time_delay ):
    QWidget.__init__( self )
    self.isis_map = QWidget( self )
    self.isis_map.setWindowTitle( "Testbed Automator Lab Topology Mapper" )
    self.pictureArea = QLabel( self.isis_map )
    self.pictureArea.setFrameShape(QtWidgets.QFrame.Box)
    self.pictureArea.setFrameShadow(QtWidgets.QFrame.Raised)
    self.pictureArea.setLineWidth(2)
    self.isis_map_pixmap = QPixmap( "./.AcmeAutomator/myARCHIVES/NETWORK-MAP/Testbed-Tester-ISIS-Map.png" )
    self.pictureArea.setPixmap(self.isis_map_pixmap)
    self.pictureArea.resize(self.isis_map_pixmap.width(), self.isis_map_pixmap.height())
    self.isis_map.resize(self.isis_map_pixmap.width(), self.isis_map_pixmap.height())
    self.pictureArea.setObjectName( "pictureArea" )
#--------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
  debug = False
  app1 = QtWidgets.QApplication( sys.argv )
  try:
    time_delay = sys.argv[1]
    if sys.argv[2] == "True":
      debug = True
  except:
    print( "Usage:  PyQt4TestbedAutomatorPauser [delay time in seconds] True/False" )
    sys.exit( 1 )
  window = IsisMap( time_delay )
  if not debug:
    window.setWindowFlag(Qt.FramelessWindowHint)
  window.show( )
  app1.exec_( )
#####################################################################################################################