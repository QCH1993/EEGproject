# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Data_info.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DataInfo(object):
    def setupUi(self, DataInfo):
        DataInfo.setObjectName("DataInfo")
        DataInfo.resize(640, 480)
        self.verticalLayout = QtWidgets.QVBoxLayout(DataInfo)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_data_info = QtWidgets.QLabel(DataInfo)
        self.label_data_info.setText("")
        self.label_data_info.setObjectName("label_data_info")
        self.verticalLayout.addWidget(self.label_data_info)
        self.buttonBox = QtWidgets.QDialogButtonBox(DataInfo)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(DataInfo)
        self.buttonBox.accepted.connect(DataInfo.accept)
        self.buttonBox.rejected.connect(DataInfo.reject)
        QtCore.QMetaObject.connectSlotsByName(DataInfo)

    def retranslateUi(self, DataInfo):
        _translate = QtCore.QCoreApplication.translate
        DataInfo.setWindowTitle(_translate("DataInfo", "Dialog"))

