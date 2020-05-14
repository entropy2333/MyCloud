# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\coding\python\MyCloud\qt\UI\register.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_RegisterWindow(object):
    def setupUi(self, RegisterWindow):
        RegisterWindow.setObjectName("RegisterWindow")
        RegisterWindow.resize(516, 345)
        self.centralwidget = QtWidgets.QWidget(RegisterWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 50, 441, 271))
        self.widget.setObjectName("widget")
        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setGeometry(QtCore.QRect(160, 220, 101, 31))
        font = QtGui.QFont()
        font.setFamily("幼圆")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.widget_3 = QtWidgets.QWidget(self.centralwidget)
        self.widget_3.setGeometry(QtCore.QRect(10, 20, 441, 31))
        self.widget_3.setObjectName("widget_3")
        self.pushButton_3 = QtWidgets.QPushButton(self.widget_3)
        self.pushButton_3.setGeometry(QtCore.QRect(350, 0, 41, 28))
        self.pushButton_3.setText("")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.widget_3)
        self.pushButton_4.setGeometry(QtCore.QRect(390, 0, 41, 28))
        self.pushButton_4.setText("")
        self.pushButton_4.setObjectName("pushButton_4")
        RegisterWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(RegisterWindow)
        QtCore.QMetaObject.connectSlotsByName(RegisterWindow)

    def retranslateUi(self, RegisterWindow):
        _translate = QtCore.QCoreApplication.translate
        RegisterWindow.setWindowTitle(_translate("RegisterWindow", "注册"))
        self.pushButton_2.setText(_translate("RegisterWindow", "注册"))
