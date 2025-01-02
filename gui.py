# Form implementation generated from reading ui file 'qt/main_window.ui'
#
# Created by: PyQt6 UI code generator 6.8.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_myBookAppWindow(object):
    def setupUi(self, myBookAppWindow):
        myBookAppWindow.setObjectName("myBookAppWindow")
        myBookAppWindow.resize(1280, 720)
        myBookAppWindow.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(parent=myBookAppWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.sideMenuFrame = QtWidgets.QFrame(parent=self.centralwidget)
        self.sideMenuFrame.setGeometry(QtCore.QRect(0, 0, 250, 720))
        self.sideMenuFrame.setStyleSheet("background-color: rgb(244, 242, 233);")
        self.sideMenuFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.sideMenuFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.sideMenuFrame.setObjectName("sideMenuFrame")
        self.myBookButton = QtWidgets.QPushButton(parent=self.sideMenuFrame)
        self.myBookButton.setGeometry(QtCore.QRect(30, 150, 201, 81))
        self.myBookButton.setStyleSheet("color: rgb(0, 0, 0);\n"
"font: 20pt \"Ubuntu Sans\";")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("qt/../assets/icons8-book-shelf-64.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.myBookButton.setIcon(icon)
        self.myBookButton.setIconSize(QtCore.QSize(32, 32))
        self.myBookButton.setObjectName("myBookButton")
        self.titleLabel = QtWidgets.QLabel(parent=self.sideMenuFrame)
        self.titleLabel.setGeometry(QtCore.QRect(30, 20, 181, 71))
        self.titleLabel.setStyleSheet("color: rgb(0, 0, 0);\n"
"font: 600 22pt \"Ubuntu Sans\";")
        self.titleLabel.setObjectName("titleLabel")
        self.mySearchButton = QtWidgets.QPushButton(parent=self.sideMenuFrame)
        self.mySearchButton.setGeometry(QtCore.QRect(30, 250, 201, 81))
        self.mySearchButton.setStyleSheet("color: rgb(0, 0, 0);\n"
"font: 20pt \"Ubuntu Sans\";")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("qt/../assets/icons8-search-64.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.mySearchButton.setIcon(icon1)
        self.mySearchButton.setIconSize(QtCore.QSize(32, 32))
        self.mySearchButton.setObjectName("mySearchButton")
        self.mainFrame = QtWidgets.QFrame(parent=self.centralwidget)
        self.mainFrame.setGeometry(QtCore.QRect(250, 0, 1030, 720))
        self.mainFrame.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.mainFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.mainFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.mainFrame.setObjectName("mainFrame")
        self.sectionLabel = QtWidgets.QLabel(parent=self.mainFrame)
        self.sectionLabel.setGeometry(QtCore.QRect(90, 0, 181, 90))
        self.sectionLabel.setStyleSheet("color: rgb(0, 0, 0);\n"
"font: 600 22pt \"Ubuntu Sans\";")
        self.sectionLabel.setObjectName("sectionLabel")
        self.pageFrame = QtWidgets.QFrame(parent=self.mainFrame)
        self.pageFrame.setGeometry(QtCore.QRect(0, 90, 1030, 630))
        self.pageFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.pageFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.pageFrame.setObjectName("pageFrame")
        self.myBookButton_2 = QtWidgets.QPushButton(parent=self.mainFrame)
        self.myBookButton_2.setGeometry(QtCore.QRect(13, 13, 64, 64))
        self.myBookButton_2.setStyleSheet("color: rgb(0, 0, 0);\n"
"font: 20pt \"Ubuntu Sans\";\n"
"\n"
" background-color: white;\n"
" border-style: solid;\n"
" border-width:1px;\n"
" border-radius:50px;")
        self.myBookButton_2.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("qt/../assets/icons8-back-64.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.myBookButton_2.setIcon(icon2)
        self.myBookButton_2.setIconSize(QtCore.QSize(32, 32))
        self.myBookButton_2.setObjectName("myBookButton_2")
        myBookAppWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(myBookAppWindow)
        QtCore.QMetaObject.connectSlotsByName(myBookAppWindow)

    def retranslateUi(self, myBookAppWindow):
        _translate = QtCore.QCoreApplication.translate
        myBookAppWindow.setWindowTitle(_translate("myBookAppWindow", "My Book App"))
        self.myBookButton.setText(_translate("myBookAppWindow", "Mis Libros"))
        self.titleLabel.setText(_translate("myBookAppWindow", "My Book App"))
        self.mySearchButton.setText(_translate("myBookAppWindow", "Búsqueda"))
        self.sectionLabel.setText(_translate("myBookAppWindow", "Mis Libros"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    myBookAppWindow = QtWidgets.QMainWindow()
    ui = Ui_myBookAppWindow()
    ui.setupUi(myBookAppWindow)
    myBookAppWindow.show()
    sys.exit(app.exec())
