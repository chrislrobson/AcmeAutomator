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
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap


class App(QWidget):

  def __init__(self):
    super().__init__()
    self.title = 'PyQt5 image - pythonspot.com'
    self.left = 10
    self.top = 10
    self.width = 640
    self.height = 480
    self.initUI()

  def initUI(self):
    self.setWindowTitle(self.title)
    self.setGeometry(self.left, self.top, self.width, self.height)

    # Create widget
    label = QLabel(self)
    pixmap = QPixmap('./.AcmeAutomator/myARCHIVES/NETWORK-MAP/Testbed-Tester-ISIS-Map.png')
    label.setPixmap(pixmap)
    self.resize(pixmap.width(), pixmap.height())

    self.show()


if __name__ == '__main__':
  app = QApplication(sys.argv)
  ex = App()
  sys.exit(app.exec_())
