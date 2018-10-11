__author__ = '井翔宇'
# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'img_math.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
# 基于百度人工智能的人脸对比技术

import sys
import base64
import json
import tkinter as tk
from aip import AipFace
from tkinter import filedialog
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    # 默认人脸图片路径
    def __init__(self):
        self.label_img1_path = ''
        self.label_img2_path = ''

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(998, 729)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # 选择图片一 按钮
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(130, 20, 75, 23))
        self.pushButton.setObjectName("pushButton")

        # 选择图片二 按钮
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(720, 20, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")

        # 人脸对比按钮
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(430, 470, 75, 23))
        self.pushButton_3.setObjectName("pushButton_3")

        # 显示图片一 label
        self.label_img1 = QtWidgets.QLabel(self.centralwidget)
        self.label_img1.setGeometry(QtCore.QRect(60, 110, 400, 300))
        self.label_img1.setText("")
        self.label_img1.setObjectName("label_img1")

        # 显示图片二 labe2
        self.label_img2 = QtWidgets.QLabel(self.centralwidget)
        self.label_img2.setGeometry(QtCore.QRect(530, 120, 400, 300))
        self.label_img2.setText("")
        self.label_img2.setObjectName("label_img2")

        # 比对结果框
        self.result_math = QtWidgets.QTextEdit(self.centralwidget)
        self.result_math.setGeometry(QtCore.QRect(340, 540, 331, 111))
        self.result_math.setObjectName("result_math")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 998, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # 选择人脸图片并显示在label1
    def select_img(self):
        root = tk.Tk()
        root.withdraw()
        self.label_img1_path = filedialog.askopenfilename() # 弹出文件选择框并获取文件路径
        png = QtGui.QPixmap(self.label_img1_path).scaled(self.label_img1.width(), self.label_img1.height()) # 图片自适应大小
        self.label_img1.setPixmap(png)                      # 向lable中写入图片

    # 选择人脸图片并显示在label2
    def select_img2(self):
        root = tk.Tk()
        root.withdraw()
        self.label_img2_path = filedialog.askopenfilename()
        png = QtGui.QPixmap(self.label_img2_path).scaled(self.label_img2.width(), self.label_img2.height())
        self.label_img2.setPixmap(png)

    # 人脸匹配
    def ai_math_face(self):
        """ 你的 APPID AK SK """
        APP_ID = '14313252'
        API_KEY = 'g7bnDTUUK9SMzIsKIHMyqPTw'
        SECRET_KEY = 'sAxOW2M48QOmPUxQeEza3yYbdFyCGH0Y'

        client = AipFace(APP_ID, API_KEY, SECRET_KEY)

        """ 调用人脸比对 """
        result_json=client.match([
            {
                'image': str(base64.b64encode(open(self.label_img1_path, 'rb').read()),'utf-8'),
                'image_type': 'BASE64',
            },
            {
                'image': str(base64.b64encode(open(self.label_img2_path, 'rb').read()),'utf-8'),
                'image_type': 'BASE64',
            }
        ]);

        result = result_json['result']
        if result_json['error_code'] == 0:
            self.result_math.setText("相似度:" + str(result['score']) + '%') # 在结果框中显示数据
        else:
            self.result_math.setText("错误信息:" + str(result_json['error_msg'])) # 在结果框中显示数据

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "图片一"))
        self.pushButton_2.setText(_translate("MainWindow", "图片二"))
        self.pushButton_3.setText(_translate("MainWindow", "人脸对比"))

        self.pushButton.clicked.connect(self.select_img)      # 选择人脸图片1
        self.pushButton_2.clicked.connect(self.select_img2)   # 选择人脸图片2
        self.pushButton_3.clicked.connect(self.ai_math_face)  # 做对比


def show_MainWindow():
    app = QtWidgets.QApplication(sys.argv)  # 首先必须实例化QApplication类，作为GUI主程序入口
    MainWindow = QtWidgets.QMainWindow()    # 实例化QtWidgets.QMainWindow类，创建自带menu的窗体类型QMainWindow
    ui = Ui_MainWindow()                      # 实例UI类
    ui.setupUi(MainWindow)                  # 设置窗体UI
    MainWindow.show()                       # 显示窗体
    sys.exit(app.exec_())                   # 当来自操作系统的分发事件指派调用窗口时，

if __name__ == "__main__":
    show_MainWindow()  # 调用显示窗体的方法