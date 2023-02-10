import json
import shutil
from time import time

from PyQt5.QtCore import pyqtProperty, pyqtSlot
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtWidgets
from queue import Queue

from util import *


class ModelTrainController(QWidget):

    def __init__(self, win):
        super().__init__()
        self.win = win

    @pyqtSlot(str, result=bool)
    def model_train(self, train_config_str):
        print("开始训练")
        train_config = json.loads(train_config_str)
        # 获取前端训练对象
        param_data = {**ModelDataClass(), **train_config}
        # 子线程开启进行模型训练
        TrainThread(param_data).start()
        return True

    @pyqtSlot(str, result=bool)
    def deleteModel(self, delete_config_str):
        param_data = json.loads(delete_config_str)
        DeleteThread(param_data).start()
        return True


