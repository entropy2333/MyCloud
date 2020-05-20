# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\coding\python\MyCloud\qt\UI\share.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ShareWindow(object):
    def setupUi(self, ShareWindow):
        ShareWindow.setObjectName("ShareWindow")
        ShareWindow.resize(516, 345)
        self.centralwidget = QtWidgets.QWidget(ShareWindow)
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
        self.minButton = QtWidgets.QPushButton(self.widget_3)
        self.minButton.setGeometry(QtCore.QRect(350, 0, 41, 28))
        self.minButton.setText("")
        self.minButton.setObjectName("minButton")
        self.closeButton = QtWidgets.QPushButton(self.widget_3)
        self.closeButton.setGeometry(QtCore.QRect(390, 0, 41, 28))
        self.closeButton.setText("")
        self.closeButton.setObjectName("closeButton")
        ShareWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(ShareWindow)
        QtCore.QMetaObject.connectSlotsByName(ShareWindow)

    def retranslateUi(self, ShareWindow):
        _translate = QtCore.QCoreApplication.translate
        ShareWindow.setWindowTitle(_translate("ShareWindow", "分享"))
        self.pushButton_2.setText(_translate("ShareWindow", "注册"))
