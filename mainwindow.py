# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(999, 893)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 640, 111, 17))
        self.label.setObjectName("label")
        self.pushButton_forward = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_forward.setGeometry(QtCore.QRect(270, 770, 51, 25))
        self.pushButton_forward.setObjectName("pushButton_forward")
        self.pushButton_select_dir_xml = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_select_dir_xml.setGeometry(QtCore.QRect(490, 680, 89, 25))
        self.pushButton_select_dir_xml.setObjectName("pushButton_select_dir_xml")
        self.checkBox_create_xml = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_create_xml.setGeometry(QtCore.QRect(620, 670, 191, 23))
        self.checkBox_create_xml.setObjectName("checkBox_create_xml")
        self.lineEdit_xml_dir_path = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_xml_dir_path.setGeometry(QtCore.QRect(150, 680, 331, 25))
        self.lineEdit_xml_dir_path.setObjectName("lineEdit_xml_dir_path")
        self.pushButton_back = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_back.setGeometry(QtCore.QRect(150, 770, 51, 25))
        self.pushButton_back.setObjectName("pushButton_back")
        self.lineEdit_video_file_path = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_video_file_path.setGeometry(QtCore.QRect(150, 640, 331, 25))
        self.lineEdit_video_file_path.setObjectName("lineEdit_video_file_path")
        self.pushButton_play = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_play.setGeometry(QtCore.QRect(210, 770, 51, 25))
        self.pushButton_play.setObjectName("pushButton_play")
        self.pushButton_select_video_file = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_select_video_file.setGeometry(QtCore.QRect(490, 640, 89, 25))
        self.pushButton_select_video_file.setObjectName("pushButton_select_video_file")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 680, 121, 20))
        self.label_2.setObjectName("label_2")
        self.label_cur_frame_id = QtWidgets.QLabel(self.centralwidget)
        self.label_cur_frame_id.setGeometry(QtCore.QRect(150, 810, 51, 17))
        self.label_cur_frame_id.setObjectName("label_cur_frame_id")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(20, 810, 141, 17))
        self.label_4.setObjectName("label_4")
        self.label_video = QtWidgets.QLabel(self.centralwidget)
        self.label_video.setGeometry(QtCore.QRect(20, 20, 960, 540))
        self.label_video.setText("")
        self.label_video.setObjectName("label_video")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 730, 141, 17))
        self.label_3.setObjectName("label_3")
        self.lineEdit_Proc_time = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_Proc_time.setGeometry(QtCore.QRect(160, 720, 71, 31))
        self.lineEdit_Proc_time.setObjectName("lineEdit_Proc_time")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(260, 730, 111, 17))
        self.label_7.setObjectName("label_7")
        self.lineEdit_freq_xmls = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_freq_xmls.setGeometry(QtCore.QRect(370, 720, 71, 31))
        self.lineEdit_freq_xmls.setObjectName("lineEdit_freq_xmls")
        self.label_xml = QtWidgets.QLabel(self.centralwidget)
        self.label_xml.setGeometry(QtCore.QRect(30, 580, 341, 31))
        self.label_xml.setText("")
        self.label_xml.setObjectName("label_xml")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(470, 730, 91, 17))
        self.label_5.setObjectName("label_5")
        self.lineEdit_name_object = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_name_object.setGeometry(QtCore.QRect(560, 720, 101, 31))
        self.lineEdit_name_object.setObjectName("lineEdit_name_object")
        self.checkBox_tracker = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_tracker.setGeometry(QtCore.QRect(630, 640, 81, 23))
        self.checkBox_tracker.setObjectName("checkBox_tracker")
        self.checkBox_label_img = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_label_img.setGeometry(QtCore.QRect(810, 640, 111, 23))
        self.checkBox_label_img.setObjectName("checkBox_label_img")
        self.pushButton_save_xml = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_save_xml.setGeometry(QtCore.QRect(820, 670, 97, 27))
        self.pushButton_save_xml.setObjectName("pushButton_save_xml")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 999, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Video file path:"))
        self.pushButton_forward.setText(_translate("MainWindow", "Fwd"))
        self.pushButton_select_dir_xml.setText(_translate("MainWindow", "Select"))
        self.checkBox_create_xml.setText(_translate("MainWindow", "Create_xml_by tracker"))
        self.pushButton_back.setText(_translate("MainWindow", "Bck"))
        self.pushButton_play.setText(_translate("MainWindow", "Play"))
        self.pushButton_select_video_file.setText(_translate("MainWindow", "Select"))
        self.label_2.setText(_translate("MainWindow", "Directory to xml:"))
        self.label_cur_frame_id.setText(_translate("MainWindow", "--/--"))
        self.label_4.setText(_translate("MainWindow", "Current frame id: "))
        self.label_3.setText(_translate("MainWindow", "Processing time, ms:"))
        self.label_7.setText(_translate("MainWindow", "Frequency xmls:"))
        self.label_5.setText(_translate("MainWindow", "Object class:"))
        self.checkBox_tracker.setText(_translate("MainWindow", "Tracker"))
        self.checkBox_label_img.setText(_translate("MainWindow", "Label Img"))
        self.pushButton_save_xml.setText(_translate("MainWindow", "Save XML"))
