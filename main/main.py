import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebChannel import QWebChannel


from MainWindow import MainWindow
from controller_FileController import FileController
from controller_PredictController import PredictController
from controller_ModelTrainController import ModelTrainController
from controller_DataController import *

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 主程序框
    win = MainWindow()

    # 数据处理
    channel = QWebChannel()  # 数据交互对象

    # 注册交互模块
    predictController = PredictController(win)
    modelTrainController = ModelTrainController(win)
    DataController = DataController(win)

    channel.registerObject("predict", predictController)
    channel.registerObject("train", modelTrainController)
    channel.registerObject("data", DataController)


    # 设置通道
    win.browser.page().setWebChannel(channel)

    # 显示
    win.show()

    sys.exit(app.exec_())
