# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\coding\python\MyCloud\qt\UI\main_window.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1432, 934)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(50, 20, 1181, 51))
        self.widget.setObjectName("widget")
        self.minButton = QtWidgets.QPushButton(self.widget)
        self.minButton.setGeometry(QtCore.QRect(1090, 10, 41, 41))
        self.minButton.setText("")
        self.minButton.setObjectName("minButton")
        self.closeButton = QtWidgets.QPushButton(self.widget)
        self.closeButton.setGeometry(QtCore.QRect(1130, 10, 41, 41))
        self.closeButton.setText("")
        self.closeButton.setObjectName("closeButton")
        self.name = QtWidgets.QLabel(self.widget)
        self.name.setGeometry(QtCore.QRect(90, 10, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.name.setFont(font)
        self.name.setObjectName("name")
        self.logo = QtWidgets.QLabel(self.widget)
        self.logo.setGeometry(QtCore.QRect(30, 4, 51, 41))
        self.logo.setText("")
        self.logo.setObjectName("logo")
        self.widget_2 = QtWidgets.QWidget(self.centralwidget)
        self.widget_2.setGeometry(QtCore.QRect(50, 70, 211, 661))
        self.widget_2.setObjectName("widget_2")
        self.listView = QtWidgets.QListView(self.widget_2)
        self.listView.setGeometry(QtCore.QRect(20, 20, 171, 621))
        self.listView.setObjectName("listView")
        self.widget_3 = QtWidgets.QWidget(self.centralwidget)
        self.widget_3.setGeometry(QtCore.QRect(260, 70, 971, 661))
        self.widget_3.setObjectName("widget_3")
        self.tableWidget = QtWidgets.QTableWidget(self.widget_3)
        self.tableWidget.setGeometry(QtCore.QRect(20, 20, 931, 621))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MyCloud"))
        self.name.setText(_translate("MainWindow", "iDrive"))
