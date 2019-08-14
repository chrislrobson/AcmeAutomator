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
import time
#-------------------------------------------------------------------------------------------------------------------
class PyQt5PauseButton( QtWidgets.QWidget ):
  def __init__( self, time_delay ):
    QtWidgets.QWidget.__init__( self )
    self.layout = QtWidgets.QWidget( self )
    self.pictureArea = QtWidgets.QLabel( self.layout )
    self.pictureArea.setGeometry(QtCore.QRect(10, 0, 1280, 1000))
    self.pictureArea.setFrameShape(QtWidgets.QFrame.Box)
    self.pictureArea.setFrameShadow(QtWidgets.QFrame.Raised)
    self.pictureArea.setLineWidth(2)
    self.pictureArea.setText( "" )
    self.pictureArea.setPixmap(QtGui.QPixmap( "./.AcmeAutomator/myARCHIVES/NETWORK-MAP/Testbed-Juniper-ISIS.png" ))
    self.pictureArea.setObjectName( "pictureArea" )
    # FIXME need to locate this in window self.buttonlayout = QtWidgets.QVBoxLayout( self.layout )
    # FIXME need to locate this in window self.buttonContinue = QtWidgets.QPushButton( 'Time Delay for %s seconds' % time_delay,self )
    # FIXME need to locate this in window self.buttonContinue.setStyleSheet( "color: blue;" + \
    # FIXME need to locate this in window                                "font-weight: bold;" + \
    # FIXME need to locate this in window                                "font-size: 16pt;" + \
    # FIXME need to locate this in window                                "background-color: white;" )
    # FIXME need to locate this in window self.buttonContinue.clicked.connect( self.handleContinue )
    # FIXME need to locate this in window self.buttonContinue.setGeometry( QtCore.QRect(100, 100, 450, 280) )
    # FIXME need to locate this in window self.buttonlayout.addWidget( self.buttonContinue )
    #time.sleep( int( float( time_delay ) ) )
  def handleContinue( self ):
    sys.exit( 0 )
#--------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
  app1 = QtWidgets.QApplication( sys.argv )
  try:
    time_delay = sys.argv[1]
  except:
    print( "Usage:  PyQt4TestbedAutomatorPauser [delay time in seconds]" )
    sys.exit( 1 )
  window = PyQt5PauseButton( time_delay )
  window.setWindowTitle( "Testbed Automator Lab Topology Mapper" )
  #window.setGeometry( 0,0,300,100 )
  window.setGeometry( QtCore.QRect(0, 0, 1300, 1000) )
  window.show( )
  app1.exec_( )
#####################################################################################################################