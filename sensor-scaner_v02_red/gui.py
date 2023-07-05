import sys
from PyQt5 import QtWidgets
import PyQt5
from PyQt5.QtCore import QDate, pyqtSignal, Qt
from PyQt5 import uic
import requests

from scan_data import ScanData
import config

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('gui.ui', self)
        self.url = config.url
        try:
            self.content = requests.get(self.url).text
            self.data = ScanData(self.content) 
            self.listShops.addItems(self.data.get_named_points())
        except requests.exceptions.ConnectionError:
            self.title.setText('PROBLEMS WITH CONNECTION')
        except requests.exceptions.MissingSchema :
            self.title.setText('URL-ADDRESS IS FAILED')
        except:
            self.title.setText('SOMETHING FAILED = push UPDATE')
        else:
            self.title.setText('SENSOR_SCANER')

        self.pushClose.clicked.connect(self.close)
        self.pushUpdate.clicked.connect(self.update)

        self.listShops.clicked.connect(self.select_shop)

        self.listSubShops.clicked.connect(self.select_sub_shop)

    def select_shop(self):
        self.listSubShops.clear()
        self.listSubShops.addItems(self.data.get_named_points()[self.listShops.currentItem().text()])

    def select_sub_shop(self):
        self.listSensors.clear()
        current = self.listSubShops.currentItem().text()
        self.listSensors.addItems(self.data.sensor_info(self.data.get_point(current)[0]))

    def update(self):
        self.listShops.clear()
        self.listSubShops.clear()
        self.listSensors.clear()
        try:
            self.content = requests.get(self.url).text
            self.data = ScanData(self.content) 
            self.listShops.addItems(self.data.get_named_points())
        except requests.exceptions.ConnectionError:
            self.title.setText('PROBLEMS WITH CONNECTION')
        except requests.exceptions.MissingSchema :
            self.title.setText('URL-ADDRESS IS FAILED')
        except:
            self.title.setText('SOMETHING FAILED = push UPDATE')
        else:
            self.title.setText('SENSOR_SCANER')


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

