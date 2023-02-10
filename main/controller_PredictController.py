import json
import os
import pickle

import numpy as np
from PyQt5.QtCore import pyqtProperty, pyqtSlot
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5 import QtWidgets

from domain_Data import save_predict_result
from util import PredictThread


class PredictController(QWidget):

    # def get_file_path(self):
    def __init__(self, win):
        super().__init__()
        self.win = win

    @pyqtSlot(str, result=bool)
    def main_predict(self, predict_config_str):
        # 加载模型训练数据
        PredictThread(predict_config_str).start()
        return True


    @pyqtSlot(result=str)
    def getFileName(self):
        file_name, file_type = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件", os.getcwd(),
                                                                     "All Files(*);;Text Files(*.txt)")
        print(file_name)
        return file_name

    # def PyQt52WebValue(self):
    #     print("666")
    #
    # def Web2PyQt5Value(self, str):
    #     QMessageBox.information(self, "网页来的信息", str)
    #     self.win.calljs("")
    #
    # value = pyqtProperty(str, fget=PyQt52WebValue, fset=Web2PyQt5Value)
