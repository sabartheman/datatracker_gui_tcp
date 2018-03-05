import systempconv
from PyQt4 import QtCore, QtGui, uic

form_class = uic.loadUiType("pyqt_test.ui")


class MyWindowClass(QtGui.QmainWindow, form_class):
    def __init__(self, parent=None):
        QtGui.QmainWindow.__init__(self,parent)
        self.setupUi(self)




app = QtGui.QApplication(sys.argv)
myWindow = MyWindowClass(None)
MyWindow.show()
app.exec_()
