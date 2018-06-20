# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AboutThisData.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AboutThisData(object):
    def setupUi(self, AboutThisData):
        AboutThisData.setObjectName("AboutThisData")
        AboutThisData.resize(640, 480)
        self.horizontalLayout = QtWidgets.QHBoxLayout(AboutThisData)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.LabelAboutThisData = QtWidgets.QLabel(AboutThisData)
        self.LabelAboutThisData.setObjectName("LabelAboutThisData")
        self.verticalLayout.addWidget(self.LabelAboutThisData)
        self.textAboutThisData = QtWidgets.QTextEdit(AboutThisData)
        self.textAboutThisData.setObjectName("textAboutThisData")
        self.verticalLayout.addWidget(self.textAboutThisData)
        self.buttonBox = QtWidgets.QDialogButtonBox(AboutThisData)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Abort|QtWidgets.QDialogButtonBox.Close|QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Reset)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(AboutThisData)
        self.buttonBox.accepted.connect(AboutThisData.accept)
        self.buttonBox.rejected.connect(AboutThisData.reject)
        self.buttonBox.clicked['QAbstractButton*'].connect(self.textAboutThisData.clear)
        QtCore.QMetaObject.connectSlotsByName(AboutThisData)

    def retranslateUi(self, AboutThisData):
        _translate = QtCore.QCoreApplication.translate
        AboutThisData.setWindowTitle(_translate("AboutThisData", "Dialog"))
        self.LabelAboutThisData.setText(_translate("AboutThisData", "<html><head/><body><p><span style=\" font-weight:600;\">About this data:</span></p><p><span style=\" font-style:italic;\">(please input the information you want to add below)</span></p></body></html>"))

