import json

from PyQt5.QtCore import pyqtProperty, pyqtSlot
from PyQt5.QtWidgets import QWidget
from domain_Data import *


class DataController(QWidget):
    def __init__(self, win):
        super().__init__()
        self.win = win

    @pyqtSlot(result=str)
    def get_model_info(self):
        Data().load_models()
        return json.dumps(Data.model_info)

    @pyqtSlot(result=str)
    def get_info(self):
        Data().flushInfo()
        return json.dumps(Data.current_info)

    # 模型所有数据获取
    modelInfo = pyqtProperty(str, fget=get_model_info)

    # def get_predict_list_log(self):
    #     return json.dumps(Data)

    # 预测之后数据获取

    # predictInfo = pyqtProperty(str, fget=get_predict_list_log, fset=get_predict_list_log)

