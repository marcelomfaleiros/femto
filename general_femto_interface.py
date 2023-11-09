# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'general_femto_interface.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_QMainWindow(object):
    def setupUi(self, QMainWindow):
        QMainWindow.setObjectName("QMainWindow")
        QMainWindow.resize(821, 760)
        self.centralwidget = QtWidgets.QWidget(QMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setMinimumSize(QtCore.QSize(0, 150))
        self.frame_2.setMaximumSize(QtCore.QSize(16777215, 200))
        self.frame_2.setStyleSheet("background-color: rgb(147, 210, 255);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_3 = QtWidgets.QFrame(self.frame_2)
        self.frame_3.setStyleSheet("background-color: rgb(255, 254, 228);")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lia_output_label = QtWidgets.QLabel(self.frame_3)
        self.lia_output_label.setMaximumSize(QtCore.QSize(120, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.lia_output_label.setFont(font)
        self.lia_output_label.setObjectName("lia_output_label")
        self.horizontalLayout_2.addWidget(self.lia_output_label)
        self.comboBox = QtWidgets.QComboBox(self.frame_3)
        self.comboBox.setMaximumSize(QtCore.QSize(200, 16777215))
        self.comboBox.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"selection-color: rgb(255, 255, 255);\n"
"")
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout_2.addWidget(self.comboBox)
        self.init_pushButton = QtWidgets.QPushButton(self.frame_3)
        self.init_pushButton.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.init_pushButton.setFont(font)
        self.init_pushButton.setStyleSheet("background-color: rgb(255, 196, 157);")
        self.init_pushButton.setObjectName("init_pushButton")
        self.horizontalLayout_2.addWidget(self.init_pushButton)
        self.verticalLayout_2.addWidget(self.frame_3)
        self.frame_6 = QtWidgets.QFrame(self.frame_2)
        self.frame_6.setStyleSheet("background-color: rgb(255, 254, 228);")
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.one_fs_pushButton = QtWidgets.QPushButton(self.frame_6)
        self.one_fs_pushButton.setMinimumSize(QtCore.QSize(40, 0))
        self.one_fs_pushButton.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.one_fs_pushButton.setFont(font)
        self.one_fs_pushButton.setStyleSheet("background-color: rgb(255, 200, 85);")
        self.one_fs_pushButton.setObjectName("one_fs_pushButton")
        self.horizontalLayout.addWidget(self.one_fs_pushButton)
        self.mone_fs_pushButton = QtWidgets.QPushButton(self.frame_6)
        self.mone_fs_pushButton.setMinimumSize(QtCore.QSize(40, 0))
        self.mone_fs_pushButton.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.mone_fs_pushButton.setFont(font)
        self.mone_fs_pushButton.setStyleSheet("background-color: rgb(255, 200, 85);")
        self.mone_fs_pushButton.setObjectName("mone_fs_pushButton")
        self.horizontalLayout.addWidget(self.mone_fs_pushButton)
        self.five_fs_pushButton = QtWidgets.QPushButton(self.frame_6)
        self.five_fs_pushButton.setMinimumSize(QtCore.QSize(40, 0))
        self.five_fs_pushButton.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.five_fs_pushButton.setFont(font)
        self.five_fs_pushButton.setStyleSheet("background-color: rgb(255, 200, 85);")
        self.five_fs_pushButton.setObjectName("five_fs_pushButton")
        self.horizontalLayout.addWidget(self.five_fs_pushButton)
        self.mfive_fs_pushButton = QtWidgets.QPushButton(self.frame_6)
        self.mfive_fs_pushButton.setMinimumSize(QtCore.QSize(40, 0))
        self.mfive_fs_pushButton.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.mfive_fs_pushButton.setFont(font)
        self.mfive_fs_pushButton.setStyleSheet("background-color: rgb(255, 200, 85);")
        self.mfive_fs_pushButton.setObjectName("mfive_fs_pushButton")
        self.horizontalLayout.addWidget(self.mfive_fs_pushButton)
        self.ten_fs_pushButton = QtWidgets.QPushButton(self.frame_6)
        self.ten_fs_pushButton.setMinimumSize(QtCore.QSize(40, 0))
        self.ten_fs_pushButton.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.ten_fs_pushButton.setFont(font)
        self.ten_fs_pushButton.setStyleSheet("background-color: rgb(255, 200, 85);")
        self.ten_fs_pushButton.setObjectName("ten_fs_pushButton")
        self.horizontalLayout.addWidget(self.ten_fs_pushButton)
        self.mten_fs_pushButton = QtWidgets.QPushButton(self.frame_6)
        self.mten_fs_pushButton.setMinimumSize(QtCore.QSize(40, 0))
        self.mten_fs_pushButton.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.mten_fs_pushButton.setFont(font)
        self.mten_fs_pushButton.setStyleSheet("background-color: rgb(255, 200, 85);")
        self.mten_fs_pushButton.setObjectName("mten_fs_pushButton")
        self.horizontalLayout.addWidget(self.mten_fs_pushButton)
        self.twenty_fs_pushButton = QtWidgets.QPushButton(self.frame_6)
        self.twenty_fs_pushButton.setMinimumSize(QtCore.QSize(40, 0))
        self.twenty_fs_pushButton.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.twenty_fs_pushButton.setFont(font)
        self.twenty_fs_pushButton.setStyleSheet("background-color: rgb(255, 200, 85);")
        self.twenty_fs_pushButton.setObjectName("twenty_fs_pushButton")
        self.horizontalLayout.addWidget(self.twenty_fs_pushButton)
        self.mtwenty_fs_pushButton = QtWidgets.QPushButton(self.frame_6)
        self.mtwenty_fs_pushButton.setMinimumSize(QtCore.QSize(40, 0))
        self.mtwenty_fs_pushButton.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.mtwenty_fs_pushButton.setFont(font)
        self.mtwenty_fs_pushButton.setStyleSheet("background-color: rgb(255, 200, 85);")
        self.mtwenty_fs_pushButton.setObjectName("mtwenty_fs_pushButton")
        self.horizontalLayout.addWidget(self.mtwenty_fs_pushButton)
        self.set_zero_pushButton = QtWidgets.QPushButton(self.frame_6)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.set_zero_pushButton.setFont(font)
        self.set_zero_pushButton.setStyleSheet("background-color: rgb(255, 102, 88);")
        self.set_zero_pushButton.setObjectName("set_zero_pushButton")
        self.horizontalLayout.addWidget(self.set_zero_pushButton)
        self.move_to_pushButton = QtWidgets.QPushButton(self.frame_6)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.move_to_pushButton.setFont(font)
        self.move_to_pushButton.setStyleSheet("background-color: rgb(213, 218, 255);")
        self.move_to_pushButton.setObjectName("move_to_pushButton")
        self.horizontalLayout.addWidget(self.move_to_pushButton)
        self.move_to_lineEdit = QtWidgets.QLineEdit(self.frame_6)
        self.move_to_lineEdit.setMinimumSize(QtCore.QSize(50, 0))
        self.move_to_lineEdit.setMaximumSize(QtCore.QSize(100, 16777215))
        self.move_to_lineEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.move_to_lineEdit.setObjectName("move_to_lineEdit")
        self.horizontalLayout.addWidget(self.move_to_lineEdit)
        self.pushButton = QtWidgets.QPushButton(self.frame_6)
        self.pushButton.setMinimumSize(QtCore.QSize(60, 0))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("background-color: rgb(213, 218, 255);")
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.lineEdit = QtWidgets.QLineEdit(self.frame_6)
        self.lineEdit.setMinimumSize(QtCore.QSize(50, 0))
        self.lineEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.verticalLayout_2.addWidget(self.frame_6)
        self.frame_4 = QtWidgets.QFrame(self.frame_2)
        self.frame_4.setStyleSheet("background-color: rgb(255, 254, 228);")
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.init_pos_label = QtWidgets.QLabel(self.frame_4)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.init_pos_label.setFont(font)
        self.init_pos_label.setObjectName("init_pos_label")
        self.horizontalLayout_3.addWidget(self.init_pos_label)
        self.init_pos_lineEdit = QtWidgets.QLineEdit(self.frame_4)
        self.init_pos_lineEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.init_pos_lineEdit.setObjectName("init_pos_lineEdit")
        self.horizontalLayout_3.addWidget(self.init_pos_lineEdit)
        self.fin_pos_label = QtWidgets.QLabel(self.frame_4)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.fin_pos_label.setFont(font)
        self.fin_pos_label.setObjectName("fin_pos_label")
        self.horizontalLayout_3.addWidget(self.fin_pos_label)
        self.fin_pos_lineEdit = QtWidgets.QLineEdit(self.frame_4)
        self.fin_pos_lineEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.fin_pos_lineEdit.setObjectName("fin_pos_lineEdit")
        self.horizontalLayout_3.addWidget(self.fin_pos_lineEdit)
        self.step_label = QtWidgets.QLabel(self.frame_4)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.step_label.setFont(font)
        self.step_label.setObjectName("step_label")
        self.horizontalLayout_3.addWidget(self.step_label)
        self.step_lineEdit = QtWidgets.QLineEdit(self.frame_4)
        self.step_lineEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.step_lineEdit.setObjectName("step_lineEdit")
        self.horizontalLayout_3.addWidget(self.step_lineEdit)
        self.verticalLayout_2.addWidget(self.frame_4)
        self.frame_5 = QtWidgets.QFrame(self.frame_2)
        self.frame_5.setStyleSheet("background-color: rgb(255, 254, 228);")
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_5)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.freerun_pushButton = QtWidgets.QPushButton(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.freerun_pushButton.setFont(font)
        self.freerun_pushButton.setStyleSheet("background-color: rgb(153, 255, 196);")
        self.freerun_pushButton.setObjectName("freerun_pushButton")
        self.horizontalLayout_4.addWidget(self.freerun_pushButton)
        self.start_pushButton = QtWidgets.QPushButton(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.start_pushButton.setFont(font)
        self.start_pushButton.setStyleSheet("background-color: rgb(153, 255, 196);")
        self.start_pushButton.setObjectName("start_pushButton")
        self.horizontalLayout_4.addWidget(self.start_pushButton)
        self.save_pushButton = QtWidgets.QPushButton(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.save_pushButton.setFont(font)
        self.save_pushButton.setStyleSheet("background-color: rgb(153, 245, 196);")
        self.save_pushButton.setObjectName("save_pushButton")
        self.horizontalLayout_4.addWidget(self.save_pushButton)
        self.clear_pushButton = QtWidgets.QPushButton(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.clear_pushButton.setFont(font)
        self.clear_pushButton.setStyleSheet("background-color: rgb(153, 235, 196);")
        self.clear_pushButton.setObjectName("clear_pushButton")
        self.horizontalLayout_4.addWidget(self.clear_pushButton)
        self.exit_pushButton = QtWidgets.QPushButton(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.exit_pushButton.setFont(font)
        self.exit_pushButton.setStyleSheet("background-color: rgb(153, 225, 196);")
        self.exit_pushButton.setObjectName("exit_pushButton")
        self.horizontalLayout_4.addWidget(self.exit_pushButton)
        self.verticalLayout_2.addWidget(self.frame_5)
        self.verticalLayout.addWidget(self.frame_2)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.graphicsView = PlotWidget(self.frame)
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout_5.addWidget(self.graphicsView)
        self.verticalLayout.addWidget(self.frame)
        QMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(QMainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 821, 21))
        self.menubar.setObjectName("menubar")
        QMainWindow.setMenuBar(self.menubar)

        self.retranslateUi(QMainWindow)
        QtCore.QMetaObject.connectSlotsByName(QMainWindow)

    def retranslateUi(self, QMainWindow):
        _translate = QtCore.QCoreApplication.translate
        QMainWindow.setWindowTitle(_translate("QMainWindow", "General Femto"))
        self.lia_output_label.setText(_translate("QMainWindow", "Lock-in output"))
        self.init_pushButton.setText(_translate("QMainWindow", "Initialize"))
        self.one_fs_pushButton.setText(_translate("QMainWindow", "1 fs"))
        self.mone_fs_pushButton.setText(_translate("QMainWindow", "-1 fs"))
        self.five_fs_pushButton.setText(_translate("QMainWindow", "5 fs"))
        self.mfive_fs_pushButton.setText(_translate("QMainWindow", "-5 fs"))
        self.ten_fs_pushButton.setText(_translate("QMainWindow", "10 fs"))
        self.mten_fs_pushButton.setText(_translate("QMainWindow", "-10 fs"))
        self.twenty_fs_pushButton.setText(_translate("QMainWindow", "20 fs"))
        self.mtwenty_fs_pushButton.setText(_translate("QMainWindow", "-20 fs"))
        self.set_zero_pushButton.setText(_translate("QMainWindow", "Set zero delay"))
        self.move_to_pushButton.setText(_translate("QMainWindow", "Move stage to (mm)"))
        self.pushButton.setText(_translate("QMainWindow", "Delay (fs)"))
        self.init_pos_label.setText(_translate("QMainWindow", "Initial Position (fs)"))
        self.fin_pos_label.setText(_translate("QMainWindow", "Final Position (fs)"))
        self.step_label.setText(_translate("QMainWindow", "Step (fs)"))
        self.freerun_pushButton.setText(_translate("QMainWindow", "Free run"))
        self.start_pushButton.setText(_translate("QMainWindow", "Start"))
        self.save_pushButton.setText(_translate("QMainWindow", "Save"))
        self.clear_pushButton.setText(_translate("QMainWindow", "Clear"))
        self.exit_pushButton.setText(_translate("QMainWindow", "Exit"))
from pyqtgraph import PlotWidget


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    QMainWindow = QtWidgets.QMainWindow()
    ui = Ui_QMainWindow()
    ui.setupUi(QMainWindow)
    QMainWindow.show()
    sys.exit(app.exec_())
