# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Sensor_edit.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Sensor_edit(object):
    def setupUi(self, Sensor_edit):
        Sensor_edit.setObjectName("Sensor_edit")
        Sensor_edit.resize(803, 496)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Sensor_edit)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.TODO = QtWidgets.QWidget(Sensor_edit)
        self.TODO.setMinimumSize(QtCore.QSize(200, 0))
        self.TODO.setObjectName("TODO")
        self.horizontalLayout.addWidget(self.TODO)
        self.sensor_diagram = MatplotlibWidget(Sensor_edit)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.sensor_diagram.sizePolicy().hasHeightForWidth())
        self.sensor_diagram.setSizePolicy(sizePolicy)
        self.sensor_diagram.setMinimumSize(QtCore.QSize(460, 460))
        self.sensor_diagram.setObjectName("sensor_diagram")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.sensor_diagram)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout.addWidget(self.sensor_diagram)

        self.retranslateUi(Sensor_edit)
        QtCore.QMetaObject.connectSlotsByName(Sensor_edit)

    def retranslateUi(self, Sensor_edit):
        _translate = QtCore.QCoreApplication.translate
        Sensor_edit.setWindowTitle(_translate("Sensor_edit", "Sensor_edit"))

from MatplotlibWidget import MatplotlibWidget
