# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FullIn_Prototype_01.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QFileDialog, QAction
from PyQt5.QtGui import QPixmap
import tensorflow as tf
import cv2
import numpy as np
import segmentation_models as sm
from skimage import io, color
from PIL.ImageQt import ImageQt 
import matplotlib.pyplot as plt


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.select_button = QtWidgets.QPushButton(self.centralwidget)
        self.select_button.setGeometry(QtCore.QRect(590, 280, 151, 51))
        font = QtGui.QFont()
        font.setFamily("DB Lim X")
        font.setPointSize(18)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)

        #Button
        self.select_button.setFont(font)
        self.select_button.setStyleSheet("color: rgb(0, 0, 0);\n"
"background-color: rgba(204, 204, 204, 51);")
        self.select_button.setObjectName("select_button")

        self.analyze_button = QtWidgets.QPushButton(self.centralwidget)
        self.analyze_button.setGeometry(QtCore.QRect(590, 340, 151, 51))
        font = QtGui.QFont()
        font.setFamily("DB Lim X")
        font.setPointSize(18)
        self.analyze_button.setFont(font)
        self.analyze_button.setStyleSheet("background-color: rgba(204, 204, 204, 51);\n"
"color: rgb(0, 0, 0);")
        self.analyze_button.setObjectName("analyze_button")

        self.clear_button = QtWidgets.QPushButton(self.centralwidget)
        self.clear_button.setGeometry(QtCore.QRect(590, 400, 151, 51))
        font = QtGui.QFont()
        font.setFamily("DB Lim X")
        font.setPointSize(18)
        self.clear_button.setFont(font)
        self.clear_button.setStyleSheet("background-color: rgba(204, 204, 204, 51);\n"
"color: rgb(0, 0, 0);")
        self.clear_button.setObjectName("clear_button")

        #Show img
        self.img = QtWidgets.QLabel(self.centralwidget)
        self.img.setGeometry(QtCore.QRect(0, 0, 551, 581))
        font = QtGui.QFont()
        font.setFamily("DB Lim X")
        font.setPointSize(28)
        self.img.setFont(font)
        self.img.setStyleSheet("color: rgb(0, 0, 0);")
        self.img.setAlignment(QtCore.Qt.AlignCenter)
        self.img.setObjectName("img")

        #Show full inspiration
        self.logo = QtWidgets.QLabel(self.centralwidget)
        self.logo.setGeometry(QtCore.QRect(580, 50, 181, 201))
        self.logo.setText("")
        self.logo.setPixmap(QtGui.QPixmap("Full_inspiration.png"))
        self.logo.setScaledContents(True)
        self.logo.setObjectName("logo")

        #Show iou
        self.iou = QtWidgets.QLabel(self.centralwidget)
        self.iou.setGeometry(QtCore.QRect(560, 500, 221, 41))
        font = QtGui.QFont()
        font.setFamily("DB Lim X")
        font.setPointSize(20)
        self.iou.setFont(font)
        self.iou.setFocusPolicy(QtCore.Qt.NoFocus)
        self.iou.setStyleSheet("color: rgb(0, 0, 0);")
        self.iou.setText("")
        self.iou.setScaledContents(False)
        self.iou.setAlignment(QtCore.Qt.AlignCenter)
        self.iou.setObjectName("iou")
        MainWindow.setCentralWidget(self.centralwidget)


        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        ##Connect##
        self.select_button.clicked.connect(self.select_img)
        self.clear_button.clicked.connect(self.clear)
        self.analyze_button.clicked.connect(self.analyze)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Full Inspiration"))
        self.select_button.setText(_translate("MainWindow", "Select Image"))
        self.analyze_button.setText(_translate("MainWindow", "Analyze"))
        self.clear_button.setText(_translate("MainWindow", "Clear"))
        self.img.setText(_translate("MainWindow", "Please choose image"))
        ##Load model##
        self.rib_model = tf.keras.models.load_model('rib_model.hdf5', compile=False)
        self.lung_model = tf.keras.models.load_model('lung_model.hdf5', compile=False) 
       
    ##Function##
    def select_img(self):
        self.imagePath, _ = QFileDialog.getOpenFileName()
        pixmap = QPixmap(self.imagePath)
        self.img.setPixmap(pixmap)
        self.img.setScaledContents(True)

    def clear(self):
        self.img.setText("Please choose image")
        self.iou.setText(" ")

    def analyze(self):
        #Preprocessing
        preprocess_input = sm.get_preprocessing('resnet50')
        img = cv2.imread(self.imagePath, 1) #Read in BGR mode (1)      
        img = cv2.resize(img, (512, 512))
        img_input = np.expand_dims(img, 0)
        img_input = preprocess_input(img_input)
        #Predict
        r_y_pred = self.rib_model.predict(img_input)
        r_y_pred_argmax = np.argmax(r_y_pred, axis=3)[0,:,:]
        l_y_pred = self.lung_model.predict(img_input)
        l_y_pred_argmax = np.argmax(l_y_pred, axis=3)[0,:,:]
        #Overlay
        l_y_pred_argmax[l_y_pred_argmax>0] = 1
        r_y_pred_argmax[r_y_pred_argmax>0] = 2
        r_l_y_pred_argmax = r_y_pred_argmax + l_y_pred_argmax
        overlay = color.label2rgb(r_l_y_pred_argmax,img,colors=[(0,0,100),(100,0,0),(0,100,0)],alpha=0.005, bg_label=0, bg_color=None)
        #save
        plt.imshow(overlay)
        plt.axis("off")
        plt.savefig('Result/result.png', bbox_inches='tight')
        #Show
        self.img.setPixmap(QtGui.QPixmap('Result/result.png'))
        self.img.setScaledContents(True) 
        #Calculate IoU
        union = np.count_nonzero(r_l_y_pred_argmax == 2) + np.count_nonzero(r_l_y_pred_argmax == 3)
        intersec = np.count_nonzero(r_l_y_pred_argmax == 3)
        iou = intersec/union * 100
        #Show IoU
        if iou>85.698:
            self.iou.setText(f'Full inspiration \n(ROL: {iou:.3f}%)')
        else:
            self.iou.setText(f'Not full inspiration \n(ROL: {iou:.3f}%)') 


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
