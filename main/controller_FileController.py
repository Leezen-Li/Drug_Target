import json
import os

from PyQt5.QtCore import pyqtProperty
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5 import QtWidgets


class FileController(QWidget):
    file_path = ""

    # def get_file_path(self):
    def __init__(self, win):
        super().__init__()
        self.win = win

    def PyQt52WebValue(self):
        print("666")

    def Web2PyQt5Value(self, str):
        QMessageBox.information(self, "网页来的信息", str)
        self.win.calljs("")

    value = pyqtProperty(str, fget=PyQt52WebValue, fset=Web2PyQt5Value)

    def open_file(self, message):
        fileName, fileType = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件", os.getcwd(),
                                                                   "All Files(*);;Text Files(*.txt)")
        print(fileName)
        print(fileType)

    def return_open_file(self):
        return json.dumps({'name': "李志坚", "age": 18})

    getPath = pyqtProperty(str, fget=return_open_file, fset=open_file)
